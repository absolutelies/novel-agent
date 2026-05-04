#!/usr/bin/env python3
"""
Quality Monitor — Per-Chapter Style Degradation Detector
=========================================================
Runs after each chapter generation to programmatically detect
template phrase escalation, em-dash bloat, and sentence rhythm
degradation — the early warning signs of AI output quality collapse.

Part of the Novel-Agent framework's Ten Iron Laws enforcement.
Invoked by the orchestrator after each chapter write.

Features:
- Counts template phrases: 来自, 的内容是, 沉默X秒
- Measures em-dash (——) density
- Detects consecutive short sentences (rhythm check)
- Updates progress.json with per-chapter quality trends
- Computes growth rate across last 3 chapters
- Atomic JSON overwrite (read → modify → write, never append)
- Exit codes: 0=clean, 1=warning, 2=critical (regenerate)

Usage:
    python quality_monitor.py \
        --chapter output/final/zh-CN/chapter_005.md \
        --project novels/my_project \
        --chapter-num 5 \
        --update-progress

Only stdlib — no pip installs.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Sentinel / guard value for "no data yet"
# ---------------------------------------------------------------------------
SENTINEL = -1


# ===========================================================================
# Technical abbreviation whitelist for 铁律六 (Chinese purity)
# ===========================================================================
TECHNICAL_WHITELIST = {
    "LED", "LCD", "CPU", "GPU", "RAM", "DNA", "RNA", "AI", "API",
    "URL", "HTTP", "HTTPS", "JSON", "XML", "PDF", "USB", "HDMI",
    "WiFi", "Bluetooth", "SSD", "HDD", "IP", "GPS", "SIM", "RF",
    "UV", "IR", "FM", "AM",
}


# ===========================================================================
# Chapter content analysis
# ===========================================================================

def read_chapter(chapter_path: str) -> str:
    """Read chapter text with UTF-8 encoding.

    Args:
        chapter_path: Absolute or relative path to the chapter .md file.

    Returns:
        Full chapter text as a string.

    Raises:
        FileNotFoundError: If the chapter file does not exist.
    """
    path = Path(chapter_path)
    if not path.exists():
        raise FileNotFoundError(f"Chapter file not found: {chapter_path}")
    return path.read_text(encoding="utf-8")


def count_pattern(text: str, pattern: str) -> int:
    """Count non-overlapping regex matches in text.

    Args:
        text: Full chapter content.
        pattern: Regex pattern to search for.

    Returns:
        Number of distinct matches.
    """
    return len(re.findall(pattern, text))


def count_literal(text: str, literal: str) -> int:
    """Count literal substring occurrences (faster than regex for plain strings).

    Args:
        text: Full chapter content.
        literal: Exact substring to count.

    Returns:
        Number of occurrences.
    """
    return text.count(literal)


def count_em_dashes(text: str) -> int:
    """Count Chinese em-dash occurrences (——, U+2014 U+2014).

    Each occurrence is the TWO-CHARACTER sequence ——.
    We count each pair as one em-dash.

    Args:
        text: Full chapter content.

    Returns:
        Number of em-dash pairs.
    """
    # Match the two-character sequence —— (U+2014 U+2014)
    pairs = re.findall(r'——', text)
    return len(pairs)


def get_total_chars(text: str) -> int:
    """Count total characters excluding whitespace for density calculations.

    Args:
        text: Full chapter content.

    Returns:
        Character count (excluding spaces, newlines, tabs).
    """
    return len(re.sub(r'\s', '', text))


def _strip_markdown(text: str) -> str:
    """Remove markdown block-level syntax so prose analysis is accurate.

    Strips: headings (#), code fences (```), blockquotes (>), horizontal
    rules (---, ***), and inline emphasis markers (*, _).

    Args:
        text: Raw chapter markdown.

    Returns:
        Cleaned prose text.
    """
    # Remove fenced code blocks entirely (content between ``` pairs)
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Remove heading lines (# ..., ## ...)
    text = re.sub(r'^#{1,6}\s.*$', '', text, flags=re.MULTILINE)
    # Remove horizontal rules (---, ***, ___)
    text = re.sub(r'^[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)
    # Remove blockquote markers (> at line start)
    text = re.sub(r'^>\s?', '', text, flags=re.MULTILINE)
    # Remove inline emphasis markers (*, **, __, _) that surround text
    text = re.sub(r'\*{1,3}([^*\n]+?)\*{1,3}', r'\1', text)
    text = re.sub(r'_{1,3}([^_\n]+?)_{1,3}', r'\1', text)
    # Collapse multiple blank lines into single paragraph breaks
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


def split_sentences(text: str) -> list:
    """Split Chinese text into sentences for rhythm analysis.

    Strategy:
    1. Strip markdown formatting to focus on prose.
    2. Split into paragraphs on double-newlines.
    3. Within each paragraph, split on sentence-ending punctuation
       (。, ！, ？, …, ～) followed by optional closing quotes.
    4. Filter out empty fragments and structural artifacts.

    This ensures we measure PROSE sentence rhythm, not markdown
    heading artifacts.

    Args:
        text: Full chapter content (may include markdown).

    Returns:
        List of sentence strings (stripped, non-empty, content-bearing).
    """
    # Clean markdown first
    cleaned = _strip_markdown(text)

    # Split on sentence-ending punctuation.
    # The pattern captures: text up to and including a terminal punctuation
    # mark, followed by optional closing bracket/quote and whitespace.
    # We split after the terminal punctuation so sentences retain their
    # ending mark (important for length measurement accuracy).
    parts = re.split(r'(?<=[。！？…～])[\s」』\)】"\'』\s]*', cleaned)

    # Filter to real content-bearing sentences only
    sentences = []
    for s in parts:
        stripped = s.strip()
        # Skip obviously non-sentence fragments
        if not stripped:
            continue
        if len(stripped) <= 1:
            # Single char fragments are almost always artifacts
            continue
        # Skip standalone punctuation-only lines
        if re.match(r'^[\s»「」『』【】、，。！？…～—\-–·"\'\.]+$', stripped):
            continue
        sentences.append(stripped)

    return sentences


def char_length(sentence: str) -> int:
    """Count characters in a sentence excluding whitespace.

    Args:
        sentence: A single sentence string.

    Returns:
        Visible character count.
    """
    return len(re.sub(r'\s', '', sentence))


def find_consecutive_short(
    sentences: list,
    max_len: int = 15,
    max_consecutive: int = 2,
) -> list:
    """Find runs of consecutive short sentences exceeding the limit.

    A "short" sentence is one with ≤ max_len visible characters.
    We report any run of short sentences longer than max_consecutive.

    Args:
        sentences: List of sentence strings.
        max_len: Maximum character count to be considered "short".
        max_consecutive: Maximum allowed consecutive short sentences.

    Returns:
        List of (start_index, run_length, offending_sentences) tuples
        for each violation found.
    """
    violations = []
    current_run = 0
    run_start = 0

    for i, s in enumerate(sentences):
        if char_length(s) <= max_len:
            if current_run == 0:
                run_start = i
            current_run += 1
        else:
            if current_run > max_consecutive:
                violations.append((
                    run_start,
                    current_run,
                    sentences[run_start:run_start + current_run],
                ))
            current_run = 0

    # Check final run at end of text
    if current_run > max_consecutive:
        violations.append((
            run_start,
            current_run,
            sentences[run_start:run_start + current_run],
        ))

    return violations


# ===========================================================================
# New pattern detection: section headers, phrase repetition,
# context-aware filter words, numerical density, opening repetition
# ===========================================================================

def detect_section_headers(text: str) -> tuple:
    """Detect section header markers that should NOT appear in final prose.

    Iron Law One forbids TV-structure markers like:
        ## 一, ## 十, ## 10., ## 46.7Hz

    Checks raw text BEFORE markdown stripping since ## lines are the
    very artifacts we're hunting.

    Args:
        text: Raw chapter text (before any markdown stripping).

    Returns:
        Tuple of (count: int, matches: list of matched-line strings).
    """
    # Match ## followed by Chinese numerals OR Arabic digits (possibly decimals)
    pattern = re.compile(
        r'^##\s+(?:[一二三四五六七八九十百千万亿]+|\d+(?:\.\d+)?)',
        re.MULTILINE,
    )
    matches = pattern.findall(text)
    return len(matches), [m.strip() for m in matches]


def detect_identical_phrases(
    text: str,
    min_len: int = 6,
    min_repeat: int = 3,
) -> dict:
    """Find verbatim substrings that repeat suspiciously often.

    Uses a sliding-window approach: collects all substrings of length
    min_len, counts occurrences, and reports those appearing at least
    min_repeat times.  Overlapping fragments are reduced by keeping only
    the longest non-subsumed phrase per cluster.

    Args:
        text: Full chapter content (may include markdown — stripped first).
        min_len: Minimum substring length in characters (default 6).
        min_repeat: Minimum occurrences to flag (default 3).

    Returns:
        Dict with keys:
            'count': total distinct repeated phrases found.
            'phrases': dict mapping phrase→occurrence_count.
            'max_repeat': highest repeat count for any phrase (0 if none).
    """
    # Strip markdown so we analyse prose, not formatting artifacts
    cleaned = _strip_markdown(text)

    # -------- Phase 1: sliding-window frequency map --------
    freq = {}
    n = len(cleaned)
    for i in range(n - min_len + 1):
        phrase = cleaned[i:i + min_len]
        # Skip phrases that are mostly whitespace or punctuation
        if re.match(r'^[\s「」『』【】、，。！？…～—\-–·"\'\.]{%d,}$' % min_len, phrase):
            continue
        freq[phrase] = freq.get(phrase, 0) + 1

    repeated = {p: c for p, c in freq.items() if c >= min_repeat}
    if not repeated:
        return {"count": 0, "phrases": {}, "max_repeat": 0}

    # -------- Phase 2: reduce overlapping fragments --------
    # Sort phrases by length descending; keep only those that are
    # not subsumed by a longer repeated phrase with the same count.
    sorted_phrases = sorted(repeated.items(), key=lambda x: -len(x[0]))
    kept = {}
    for phrase, cnt in sorted_phrases:
        # Check if phrase is a substring of any already-kept phrase
        subsumed = any(
            phrase in kept_phrase and len(phrase) < len(kept_phrase)
            for kept_phrase in kept
        )
        if not subsumed:
            kept[phrase] = cnt

    return {
        "count": len(kept),
        "phrases": kept,
        "max_repeat": max(kept.values()) if kept else 0,
    }


# ---------------------------------------------------------------------------
# Filter-word context helpers (铁律七 — Deep POV)
# ---------------------------------------------------------------------------

FILTER_WORDS = [
    "看见", "听到", "感到", "注意到", "意识到",
    "想", "记得", "发现", "观察", "察觉",
]


def _is_in_dialogue(text: str, pos: int) -> bool:
    """Determine whether character position *pos* is inside dialogue.

    Heuristics (in priority order):
    1. Inside 「」 brackets — the primary Chinese dialogue marker.
    2. Inside "" English double quotes (used in some novels).
    3. After a speech-verb ＋ colon pattern (说/问/道/喊/叫：).

    Args:
        text: Full chapter text.
        pos: Character index of the word being checked.

    Returns:
        True if the position is likely within dialogue.
    """
    before = text[:pos]
    after = text[pos:]

    # ---- Check 1: 「」 brackets ----
    open_count = before.count("「")
    close_count = before.count("」")
    if open_count > close_count:
        # We are inside a 「」 pair — verify there's a closing bracket ahead
        if "」" in after[:500]:
            return True

    # ---- Check 2: English double quotes ----
    last_quote = before.rfind('"')
    if last_quote != -1:
        quotes_between = before[last_quote + 1:].count('"')
        if quotes_between % 2 == 0:  # even → last_quote is an opener
            if '"' in after[:500]:
                return True

    # ---- Check 3: Speech-verb + colon ----
    # Look in preceding ~200 chars for 说/问/道/喊/叫 followed by ：
    context = before[-200:] if len(before) > 200 else before
    if re.search(r'[说问道喊叫]\s*[：:]\s*[^。！？…～\n]*$', context):
        return True

    return False


def count_filter_words_with_context(text: str) -> dict:
    """Count filter words split by narration vs. dialogue context.

    铁律七 (Deep POV) only concerns NARRATION filter words — words
    that "tell" rather than "show".  Filter words appearing inside
    dialogue are natural speech and should NOT count as violations.

    Args:
        text: Full chapter content.

    Returns:
        Dict with keys:
            "narration":       {word: count} for narration occurrences.
            "dialogue":        {word: count} for dialogue occurrences.
            "narration_total": total narration filter words.
            "dialogue_total":  total dialogue filter words.
    """
    narration = {}
    dialogue = {}

    for word in FILTER_WORDS:
        n_cnt = 0
        d_cnt = 0
        for match in re.finditer(re.escape(word), text):
            if _is_in_dialogue(text, match.start()):
                d_cnt += 1
            else:
                n_cnt += 1

        if n_cnt > 0:
            narration[word] = n_cnt
        if d_cnt > 0:
            dialogue[word] = d_cnt

    return {
        "narration": narration,
        "dialogue": dialogue,
        "narration_total": sum(narration.values()),
        "dialogue_total": sum(dialogue.values()),
    }


def detect_numerical_density(text: str) -> tuple:
    """Measure the density of sentences that contain measurements.

    A sentence is "numerical" if it pairs a number (Arabic or Chinese)
    with a measurement unit.  Too many measurement-heavy sentences
    can make prose read like a technical manual (prose_style.md
    recommends ≤8 %).

    Args:
        text: Full chapter content.

    Returns:
        Tuple of (density: float, matching_sentences: list of str).
    """
    sentences = split_sentences(text)

    # Units: Chinese and common SI/scientific abbreviations
    cn_units = r"(?:厘米|毫米|米|赫兹|转|度|秒|分|点|级)"
    en_units = r"(?:Hz|rpm|G)"
    arabic = r"\d+(?:\.\d+)?"
    chinese_num = r"[零一二三四五六七八九十百千万亿]+"

    pattern = re.compile(
        rf"({arabic}|{chinese_num})\s*({cn_units}|{en_units}|[％%])"
    )

    matching = [s for s in sentences if pattern.search(s)]
    density = len(matching) / max(len(sentences), 1)
    return round(density, 6), matching


def detect_opening_repetition(text: str) -> tuple:
    """Check whether a single character name dominates paragraph openings.

    Repeatedly opening paragraphs with the same name creates a choppy
    "name… name… name…" rhythm.  prose_style.md recommends keeping
    any single name below 12 % of paragraph openings.

    Args:
        text: Full chapter content.

    Returns:
        Tuple of (max_ratio: float, most_repeated_name: str | None,
                  count: int).
    """
    CHARACTERS = [
        "林深", "江澜", "何雨桐", "方晋", "秦墨",
        "程菲", "白小舟", "唐晓", "苏晚晴", "陆远征",
    ]

    # Split into non-empty paragraphs
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    total = len(paragraphs)
    if total == 0:
        return 0.0, None, 0

    opener_counts = {name: 0 for name in CHARACTERS}
    for para in paragraphs:
        opening = para[:6]  # first few chars suffice for a 2–3 char name
        for name in CHARACTERS:
            if opening.startswith(name):
                opener_counts[name] += 1
                break

    max_name: str = max(opener_counts, key=lambda k: opener_counts[k])  # type: ignore[no-any-return]
    max_count = opener_counts[max_name]
    ratio = max_count / total

    return round(ratio, 6), max_name, max_count


# ===========================================================================
# Progress JSON management (atomic read → modify → write)
# ===========================================================================

def progress_json_path(project_dir: str) -> Path:
    """Return the canonical path to progress.json for a project.

    Args:
        project_dir: Path to the project root (e.g., novels/my_project).

    Returns:
        Path object for memory/progress.json.
    """
    return Path(project_dir) / "memory" / "progress.json"


def load_progress(project_dir: str) -> dict:
    """Load progress.json or return a fresh default if not found.

    Never fails — returns an empty/default progress dict if the file
    is missing or unparseable, so the first chapter can bootstrap.

    Args:
        project_dir: Path to the project root.

    Returns:
        Parsed JSON as dict (possibly the default empty structure).
    """
    path = progress_json_path(project_dir)
    if not path.exists():
        return _default_progress()

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return _default_progress()
            return data
    except (json.JSONDecodeError, OSError):
        return _default_progress()


def _default_progress() -> dict:
    """Return the minimal quality_trends structure as a fresh progress dict."""
    return {
        "quality_trends": {
            "template_phrase_counts": {
                "来自": [],
                "的内容是": [],
                "沉默X秒": [],
            },
            "em_dash_density": [],
            "consecutive_short_sentences": [],
            "warnings_triggered": [],
            "last_quality_check": None,
            # ---- New pattern-detection trend lists ----
            "section_headers": [],
            "identical_phrases": [],
            "numerical_density": [],
            "opening_repetition": [],
            "filter_words_narration": [],
            "filter_words_dialogue": [],
        },
    }


def save_progress(project_dir: str, data: dict) -> None:
    """Atomically write the full progress.json.

    Uses a temp-file + rename strategy to avoid corruption if the
    write is interrupted.

    Args:
        project_dir: Path to the project root.
        data: Complete progress dict to persist.
    """
    path = progress_json_path(project_dir)
    path.parent.mkdir(parents=True, exist_ok=True)

    tmp_path = path.with_suffix(".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())

    tmp_path.replace(path)


def ensure_quality_trends(progress: dict) -> dict:
    """Guarantee the quality_trends sub-object exists in progress data.

    Mutates progress in place and returns it for convenience.

    Args:
        progress: The loaded progress dict (may lack quality_trends).

    Returns:
        Same dict with quality_trends initialized if missing.
    """
    if "quality_trends" not in progress:
        progress["quality_trends"] = {}
    qt = progress["quality_trends"]

    if "template_phrase_counts" not in qt:
        qt["template_phrase_counts"] = {
            "来自": [],
            "的内容是": [],
            "沉默X秒": [],
        }
    else:
        tpc = qt["template_phrase_counts"]
        for key in ("来自", "的内容是", "沉默X秒"):
            if key not in tpc:
                tpc[key] = []

    if "em_dash_density" not in qt:
        qt["em_dash_density"] = []
    if "consecutive_short_sentences" not in qt:
        qt["consecutive_short_sentences"] = []
    if "warnings_triggered" not in qt:
        qt["warnings_triggered"] = []
    if "last_quality_check" not in qt:
        qt["last_quality_check"] = None

    # ---- New pattern-detection trend lists ----
    for trend_key in (
        "section_headers",
        "identical_phrases",
        "numerical_density",
        "opening_repetition",
        "filter_words_narration",
        "filter_words_dialogue",
    ):
        if trend_key not in qt:
            qt[trend_key] = []

    return progress


# ===========================================================================
# Trend updating helpers
# ===========================================================================

def pad_to_length(lst: list, target_idx: int, fill: int = SENTINEL) -> list:
    """Extend list so it has at least target_idx + 1 elements.

    Chapter numbers are 1-based, so chapter N maps to index N-1.
    Missing chapters are filled with the sentinel value to preserve
    index alignment.

    Args:
        lst: The list to pad (modified in place).
        target_idx: The 0-based index the list must reach.
        fill: Value to fill missing slots with (default SENTINEL = -1).

    Returns:
        The same list (mutated).
    """
    while len(lst) <= target_idx:
        lst.append(fill)
    return lst


def update_phrase_counts(
    progress: dict,
    chapter_num: int,
    counts: dict,
) -> None:
    """Insert or overwrite per-chapter phrase counts at the correct index.

    Args:
        progress: Progress dict (mutated in place).
        chapter_num: 1-based chapter number.
        counts: Dict mapping phrase key → count for this chapter.
    """
    qt = progress["quality_trends"]
    idx = chapter_num - 1

    for key in ("来自", "的内容是", "沉默X秒"):
        arr = qt["template_phrase_counts"][key]
        pad_to_length(arr, idx)
        arr[idx] = counts.get(key, 0)


def update_em_dash_density(
    progress: dict,
    chapter_num: int,
    density: float,
) -> None:
    """Insert per-chapter em-dash density at the correct index.

    Args:
        progress: Progress dict (mutated in place).
        chapter_num: 1-based chapter number.
        density: Em-dash density as a float (0.0 to 1.0).
    """
    qt = progress["quality_trends"]
    idx = chapter_num - 1
    arr = qt["em_dash_density"]
    pad_to_length(arr, idx)
    arr[idx] = round(density, 6)


def update_short_sentence_runs(
    progress: dict,
    chapter_num: int,
    max_consecutive_found: int,
) -> None:
    """Store the maximum consecutive short-sentence run for this chapter.

    Args:
        progress: Progress dict (mutated in place).
        chapter_num: 1-based chapter number.
        max_consecutive_found: Longest run of consecutive short sentences
            found in this chapter (0 if none).
    """
    qt = progress["quality_trends"]
    idx = chapter_num - 1
    arr = qt["consecutive_short_sentences"]
    pad_to_length(arr, idx)
    arr[idx] = max_consecutive_found


def add_warning(progress: dict, warning: dict) -> None:
    """Append a warning record to the progress tracking.

    Args:
        progress: Progress dict (mutated in place).
        warning: Dict with at least 'chapter', 'severity', 'message' keys.
    """
    qt = progress["quality_trends"]
    now = datetime.now(timezone.utc).isoformat()
    warning["timestamp"] = now
    qt["warnings_triggered"].append(warning)


def set_last_check(progress: dict) -> None:
    """Update the last_quality_check timestamp to now (UTC ISO 8601).

    Args:
        progress: Progress dict (mutated in place).
    """
    progress["quality_trends"]["last_quality_check"] = (
        datetime.now(timezone.utc).isoformat()
    )


# ---- New-pattern update helpers ----

def _update_scalar_trend(
    progress: dict,
    chapter_num: int,
    key: str,
    value,
) -> None:
    """Generic helper: insert a scalar value at chapter index in a trend list.

    Args:
        progress: Progress dict (mutated in place).
        chapter_num: 1-based chapter number.
        key: Key under quality_trends (e.g. "section_headers").
        value: The value to store at this chapter's index.
    """
    qt = progress["quality_trends"]
    idx = chapter_num - 1
    if key not in qt:
        qt[key] = []
    arr = qt[key]
    pad_to_length(arr, idx)
    arr[idx] = value


def update_section_headers(
    progress: dict,
    chapter_num: int,
    count: int,
) -> None:
    """Store section-header count for this chapter.

    Args:
        progress: Progress dict (mutated in place).
        chapter_num: 1-based chapter number.
        count: Number of section-header patterns found.
    """
    _update_scalar_trend(progress, chapter_num, "section_headers", count)


def update_identical_phrases(
    progress: dict,
    chapter_num: int,
    count: int,
) -> None:
    """Store identical-phrase count for this chapter.

    Args:
        progress: Progress dict (mutated in place).
        chapter_num: 1-based chapter number.
        count: Number of distinct repeated phrases found.
    """
    _update_scalar_trend(progress, chapter_num, "identical_phrases", count)


def update_numerical_density(
    progress: dict,
    chapter_num: int,
    density: float,
) -> None:
    """Store numerical-sentence density for this chapter.

    Args:
        progress: Progress dict (mutated in place).
        chapter_num: 1-based chapter number.
        density: Numerical-density ratio (0.0 – 1.0).
    """
    _update_scalar_trend(
        progress, chapter_num, "numerical_density", round(density, 6),
    )


def update_opening_repetition(
    progress: dict,
    chapter_num: int,
    ratio: float,
) -> None:
    """Store paragraph-opening repetition ratio for this chapter.

    Args:
        progress: Progress dict (mutated in place).
        chapter_num: 1-based chapter number.
        ratio: Opening-repetition ratio (0.0 – 1.0).
    """
    _update_scalar_trend(
        progress, chapter_num, "opening_repetition", round(ratio, 6),
    )


def update_filter_words_context(
    progress: dict,
    chapter_num: int,
    narration_total: int,
    dialogue_total: int,
) -> None:
    """Store context-aware filter-word counts for this chapter.

    Args:
        progress: Progress dict (mutated in place).
        chapter_num: 1-based chapter number.
        narration_total: Filter words found in narration.
        dialogue_total: Filter words found in dialogue.
    """
    _update_scalar_trend(
        progress, chapter_num, "filter_words_narration", narration_total,
    )
    _update_scalar_trend(
        progress, chapter_num, "filter_words_dialogue", dialogue_total,
    )


# ===========================================================================
# Growth rate detection
# ===========================================================================

def growth_rate(values: list) -> float:
    """Calculate growth rate between the last value and the second-to-last.

    Uses formula: (latest - previous) / previous.
    If previous is 0 or no prior data, returns 0.0.

    Args:
        values: List of numeric values (may contain SENTINEL markers).

    Returns:
        Growth rate as a float (e.g., 0.5 = 50% growth).
    """
    # Remove sentinel slots and trailing zeros for cleaner comparison
    real_vals = [v for v in values if v != SENTINEL]
    if len(real_vals) < 2:
        return 0.0
    prev = real_vals[-2]
    latest = real_vals[-1]
    if prev == 0:
        return 0.0 if latest == 0 else float("inf")
    return (latest - prev) / prev


def last_n_real(values: list, n: int) -> list:
    """Extract the last N real (non-sentinel) values from a padded list.

    Args:
        values: List that may contain SENTINEL (-1) entries.
        n: Number of real values to return.

    Returns:
        List of at most n real values, chronologically ordered.
    """
    real = [v for v in values if v != SENTINEL]
    return real[-n:] if len(real) >= n else real


def detect_growth_spike(
    progress: dict,
    chapter_num: int,
    key: str,
    severity: str = "CRITICAL",
    threshold: float = 0.5,
) -> bool:
    """Check if the last 3 chapters show a >threshold growth spike.

    Compares the average of the last 3 entries against expected random
    variance. A spike is detected when:
    - We have at least 3 data points
    - The latest value exceeds the penultimate by more than threshold %
    - The penultimate exceeds the antepenultimate by more than threshold %

    This double-check prevents one-off noise from triggering.

    Args:
        progress: Progress dict with quality_trends populated.
        chapter_num: Current chapter number (for the warning record).
        key: The phrase key in template_phrase_counts to check.
        severity: Warning severity label (CRITICAL or WARNING).
        threshold: Fractional growth threshold (0.5 = 50%).

    Returns:
        True if a growth spike was detected and logged.
    """
    qt = progress["quality_trends"]
    values = qt["template_phrase_counts"].get(key, [])
    recent = last_n_real(values, 3)

    if len(recent) < 3:
        return False

    a, b, c = recent[0], recent[1], recent[2]

    # Skip if values are too small to be meaningful trend signals.
    # Going from 0→0→1 is "first use", not escalation.
    if c < 2:
        return False

    # Both transitions must show growth above threshold
    if a == 0 and b == 0:
        return False
    rate1 = (b - a) / max(a, 1)
    rate2 = (c - b) / max(b, 1)

    if rate1 > threshold and rate2 > threshold and c > b > a:
        msg = (
            f"{severity}: '{key}' count has grown {rate1:.0%} then "
            f"{rate2:.0%} across last 3 chapters "
            f"({a}→{b}→{c}). Template phrase escalation detected."
        )
        add_warning(progress, {
            "chapter": chapter_num,
            "severity": severity,
            "type": "growth_spike",
            "phrase": key,
            "values": [a, b, c],
            "growth_rates": [round(rate1, 3), round(rate2, 3)],
            "message": msg,
        })
        return True
    return False


def detect_flatline_pattern(
    progress: dict,
    chapter_num: int,
) -> bool:
    """Detect if the same quality metric values repeat across last 3 chapters.

    A flatline (e.g., 来自=5 for 3 consecutive chapters) suggests the
    model has settled into a rigid template — even if the values are
    within limits, the lack of variation is a warning sign.

    Args:
        progress: Progress dict with quality_trends populated.
        chapter_num: Current chapter number.

    Returns:
        True if a flatline pattern was detected.
    """
    qt = progress["quality_trends"]
    triggered = False

    for key in ("来自", "的内容是", "沉默X秒"):
        values = qt["template_phrase_counts"].get(key, [])
        recent = last_n_real(values, 3)
        if len(recent) >= 3 and recent[0] == recent[1] == recent[2]:
            # Only warn if the flatlined value is non-zero.
            # Zero across all chapters means the phrase is being avoided
            # correctly — that's the desired state, not a template problem.
            if recent[0] == 0:
                continue
            msg = (
                f"WARNING: '{key}' count flatlined at {recent[0]} "
                f"for last 3 chapters. Possible template lock-in."
            )
            add_warning(progress, {
                "chapter": chapter_num,
                "severity": "WARNING",
                "type": "flatline",
                "phrase": key,
                "value": recent[0],
                "message": msg,
            })
            triggered = True

    return triggered


# ===========================================================================
# Main quality check logic
# ===========================================================================

THRESHOLDS = {
    "来自": 5,
    "的内容是": 3,
    "沉默X秒": 2,
    "em_dash_max_density": 0.05,
    "short_sentence_max_len": 15,
    "short_sentence_max_consecutive": 3,  # 铁律八 unified: ≤3 allowed (hard sci-fi exemption)
    # ---- New pattern-detection thresholds ----
    "section_header_max": 0,
    "identical_phrase_min_count": 3,
    "numerical_density_max": 0.08,   # 8% — prose_style.md recommendation
    "opening_repetition_max": 0.12,  # 12%
    "filter_words_narration_max": 5,  # 铁律七 — narration filter words
}


def run_checks(chapter_text: str, chapter_num: int) -> dict:
    """Execute all quality checks against a chapter and return results.

    This is the core analysis function — it reads the text, counts
    patterns, computes densities, and detects sentence rhythm issues
    plus new degradation patterns (section headers, identical phrases,
    context-aware filter words, numerical density, opening repetition).

    Args:
        chapter_text: Full chapter content as a string.
        chapter_num: 1-based chapter number (for reporting).

    Returns:
        Dict with all check results:
        {
            "counts": {phrase_key: int, ...},
            "em_dash_density": float,
            "consecutive_short_violations": list,
            "max_consecutive_short": int,
            "total_chars": int,
            "section_header_count": int,
            "section_header_matches": list,
            "identical_phrase_count": int,
            "identical_phrases": dict,
            "identical_phrase_max_repeat": int,
            "filter_words": dict,          # context-aware result
            "numerical_density": float,
            "numerical_sentences": list,
            "opening_repetition_ratio": float,
            "opening_repetition_name": str | None,
            "opening_repetition_count": int,
            "warnings": list of str,
            "critical": list of str,
            "exit_code": 0|1|2,
        }
    """
    results = {
        "counts": {},
        "em_dash_density": 0.0,
        "consecutive_short_violations": [],
        "max_consecutive_short": 0,
        "total_chars": 0,
        # ---- New detector result slots ----
        "section_header_count": 0,
        "section_header_matches": [],
        "identical_phrase_count": 0,
        "identical_phrases": {},
        "identical_phrase_max_repeat": 0,
        "filter_words": {},
        "numerical_density": 0.0,
        "numerical_sentences": [],
        "opening_repetition_ratio": 0.0,
        "opening_repetition_name": None,
        "opening_repetition_count": 0,
        "warnings": [],
        "critical": [],
        "exit_code": 0,
    }

    total = get_total_chars(chapter_text)
    results["total_chars"] = total

    # ---- Template phrase counts ----
    for key, regex in (
        ("来自", r'来自'),
        ("的内容是", r'的内容是'),
        ("沉默X秒", r'沉默\d*秒'),
    ):
        count = count_pattern(chapter_text, regex)
        results["counts"][key] = count
        limit = THRESHOLDS[key]

        if count > limit:
            msg = (
                f"Ch{chapter_num}: '{key}' count={count} exceeds limit={limit}"
            )
            results["warnings"].append(msg)

    # ---- Em-dash density ----
    em_count = count_em_dashes(chapter_text)
    # Each em-dash is 2 chars (——), so total em-dash chars = em_count * 2
    em_chars = em_count * 2
    density = em_chars / max(total, 1)  # avoid div-by-zero on empty chapters
    results["em_dash_density"] = round(density, 6)

    if density > THRESHOLDS["em_dash_max_density"]:
        msg = (
            f"Ch{chapter_num}: Em-dash density={density:.4f} "
            f"exceeds limit={THRESHOLDS['em_dash_max_density']} "
            f"({em_count} dashes in {total} chars)"
        )
        results["warnings"].append(msg)

    # ---- Consecutive short sentences ----
    sentences = split_sentences(chapter_text)
    violations = find_consecutive_short(
        sentences,
        max_len=THRESHOLDS["short_sentence_max_len"],
        max_consecutive=THRESHOLDS["short_sentence_max_consecutive"],
    )
    results["consecutive_short_violations"] = violations

    if violations:
        longest = max(v[1] for v in violations)
        results["max_consecutive_short"] = longest
        msg = (
            f"Ch{chapter_num}: Found {len(violations)} run(s) of "
            f">2 consecutive short sentences (max run={longest})"
        )
        results["warnings"].append(msg)
    else:
        # No violations means every run was ≤2 consecutive — clean rhythm.
        results["max_consecutive_short"] = 0

    # ---- NEW: Section headers (铁律一) ----
    sh_count, sh_matches = detect_section_headers(chapter_text)
    results["section_header_count"] = sh_count
    results["section_header_matches"] = sh_matches

    if sh_count > THRESHOLDS["section_header_max"]:
        msg = (
            f"Ch{chapter_num}: Found {sh_count} section-header marker(s) "
            f"(limit={THRESHOLDS['section_header_max']})"
        )
        results["warnings"].append(msg)
        if sh_count >= 2:
            c_msg = (
                f"Ch{chapter_num}: CRITICAL — {sh_count} section-header "
                f"markers found (铁律一 violation)"
            )
            results["critical"].append(c_msg)

    # ---- NEW: Identical phrase repetition ----
    ip_result = detect_identical_phrases(
        chapter_text,
        min_len=6,
        min_repeat=THRESHOLDS["identical_phrase_min_count"],
    )
    results["identical_phrase_count"] = ip_result["count"]
    results["identical_phrases"] = ip_result["phrases"]
    results["identical_phrase_max_repeat"] = ip_result["max_repeat"]

    if ip_result["count"] > 0:
        msg = (
            f"Ch{chapter_num}: Found {ip_result['count']} identical phrase(s) "
            f"repeating ≥{THRESHOLDS['identical_phrase_min_count']}× "
            f"(max repeat={ip_result['max_repeat']})"
        )
        results["warnings"].append(msg)
        if ip_result["max_repeat"] >= 5:
            c_msg = (
                f"Ch{chapter_num}: CRITICAL — phrase repeated "
                f"{ip_result['max_repeat']}× (possible template lock-in)"
            )
            results["critical"].append(c_msg)

    # ---- NEW: Context-aware filter words (铁律七) ----
    fw_result = count_filter_words_with_context(chapter_text)
    results["filter_words"] = fw_result
    narration_total = fw_result["narration_total"]
    dialogue_total = fw_result["dialogue_total"]

    if narration_total > THRESHOLDS["filter_words_narration_max"]:
        msg = (
            f"Ch{chapter_num}: Narration filter words={narration_total} "
            f"exceeds limit={THRESHOLDS['filter_words_narration_max']} "
            f"(铁律七 Deep POV; dialogue={dialogue_total} excluded)"
        )
        results["warnings"].append(msg)
        if narration_total > THRESHOLDS["filter_words_narration_max"] * 2:
            c_msg = (
                f"Ch{chapter_num}: CRITICAL — narration filter words "
                f"={narration_total} (2× 铁律七 limit)"
            )
            results["critical"].append(c_msg)

    # ---- NEW: Numerical density ----
    num_density, num_sentences = detect_numerical_density(chapter_text)
    results["numerical_density"] = num_density
    results["numerical_sentences"] = num_sentences

    if num_density > THRESHOLDS["numerical_density_max"]:
        msg = (
            f"Ch{chapter_num}: Numerical density={num_density:.4f} "
            f"exceeds limit={THRESHOLDS['numerical_density_max']} "
            f"({len(num_sentences)} measurement sentences)"
        )
        results["warnings"].append(msg)

    # ---- NEW: Paragraph opening repetition ----
    open_ratio, open_name, open_count = detect_opening_repetition(
        chapter_text,
    )
    results["opening_repetition_ratio"] = open_ratio
    results["opening_repetition_name"] = open_name
    results["opening_repetition_count"] = open_count

    if open_ratio > THRESHOLDS["opening_repetition_max"]:
        msg = (
            f"Ch{chapter_num}: Opening repetition ratio={open_ratio:.4f} "
            f"exceeds limit={THRESHOLDS['opening_repetition_max']} "
            f"('{open_name}' opens {open_count} paragraphs)"
        )
        results["warnings"].append(msg)

    # Determine severity
    # - critical conditions: template phrases significantly over limit
    for key, limit in (
        ("来自", THRESHOLDS["来自"] * 2),      # double the limit → critical
        ("的内容是", THRESHOLDS["的内容是"] * 2),
        ("沉默X秒", THRESHOLDS["沉默X秒"] * 2),
    ):
        if results["counts"].get(key, 0) > limit:
            msg = (
                f"Ch{chapter_num}: CRITICAL — '{key}' count={results['counts'][key]} "
                f"far exceeds limit={THRESHOLDS[key]} (2x threshold tripped)"
            )
            results["critical"].append(msg)

    if density > THRESHOLDS["em_dash_max_density"] * 2:
        msg = (
            f"Ch{chapter_num}: CRITICAL — Em-dash density={density:.4f} "
            f"is double the limit"
        )
        results["critical"].append(msg)

    if results["max_consecutive_short"] >= 8:
        msg = (
            f"Ch{chapter_num}: CRITICAL — {results['max_consecutive_short']} "
            f"consecutive short sentences found (prose rhythm severely broken)"
        )
        results["critical"].append(msg)

    # Set exit code
    if results["critical"]:
        results["exit_code"] = 2
    elif results["warnings"]:
        results["exit_code"] = 1

    return results


# ===========================================================================
# Orchestration: tie checks + progress update together
# ===========================================================================

def run(
    chapter_path: str,
    project_dir: str,
    chapter_num: int,
    update_progress: bool = False,
) -> int:
    """Run the full quality monitoring cycle.

    1. Read and analyze the chapter.
    2. Print diagnostics to stdout.
    3. Optionally update progress.json with results.
    4. Return the appropriate exit code.

    Args:
        chapter_path: Path to the chapter .md file.
        project_dir: Path to the project root directory.
        chapter_num: 1-based chapter number.
        update_progress: If True, write results to progress.json.

    Returns:
        Exit code: 0 (clean), 1 (warning), 2 (critical).
    """
    # -------- Phase 1: Read & analyze --------
    print(f"[quality_monitor] Chapter {chapter_num}: {chapter_path}")
    chapter_text = read_chapter(chapter_path)
    results = run_checks(chapter_text, chapter_num)

    # -------- Phase 2: Print diagnostics --------
    print(f"  Total chars (excl. whitespace): {results['total_chars']}")
    for key, count in results["counts"].items():
        limit = THRESHOLDS.get(key, "?")
        flag = " ⚠" if count > limit else ""
        print(f"  '{key}': {count} (limit: {limit}){flag}")

    print(
        f"  Em-dash density: {results['em_dash_density']:.4f} "
        f"(limit: {THRESHOLDS['em_dash_max_density']})"
        f"{' ⚠' if results['em_dash_density'] > THRESHOLDS['em_dash_max_density'] else ''}"
    )
    print(
        f"  Max consecutive short sentences: {results['max_consecutive_short']} "
        f"(limit: {THRESHOLDS['short_sentence_max_consecutive']})"
        f"{' ⚠' if results['max_consecutive_short'] > THRESHOLDS['short_sentence_max_consecutive'] else ''}"
    )

    # ---- New detector diagnostics ----
    sh_flag = " ⚠" if results["section_header_count"] > THRESHOLDS["section_header_max"] else ""
    print(
        f"  Section headers: {results['section_header_count']} "
        f"(limit: {THRESHOLDS['section_header_max']}){sh_flag}"
    )

    ip_flag = " ⚠" if results["identical_phrase_count"] > 0 else ""
    print(
        f"  Identical phrases: {results['identical_phrase_count']} "
        f"(max repeat: {results['identical_phrase_max_repeat']}){ip_flag}"
    )

    fw = results["filter_words"]
    fw_flag = " ⚠" if fw.get("narration_total", 0) > THRESHOLDS["filter_words_narration_max"] else ""
    print(
        f"  Filter words (narration/dialogue): "
        f"{fw.get('narration_total', 0)}/{fw.get('dialogue_total', 0)} "
        f"(narration limit: {THRESHOLDS['filter_words_narration_max']}){fw_flag}"
    )

    nd_flag = " ⚠" if results["numerical_density"] > THRESHOLDS["numerical_density_max"] else ""
    print(
        f"  Numerical density: {results['numerical_density']:.4f} "
        f"(limit: {THRESHOLDS['numerical_density_max']}){nd_flag}"
    )

    or_flag = " ⚠" if results["opening_repetition_ratio"] > THRESHOLDS["opening_repetition_max"] else ""
    print(
        f"  Opening repetition: {results['opening_repetition_ratio']:.4f} "
        f"(name: {results['opening_repetition_name']}, "
        f"limit: {THRESHOLDS['opening_repetition_max']}){or_flag}"
    )

    # -------- Phase 3: Update progress.json --------
    if update_progress:
        progress = load_progress(project_dir)
        progress = ensure_quality_trends(progress)

        update_phrase_counts(progress, chapter_num, results["counts"])
        update_em_dash_density(progress, chapter_num, results["em_dash_density"])
        update_short_sentence_runs(
            progress, chapter_num, results["max_consecutive_short"],
        )

        # ---- New pattern-detection progress updates ----
        update_section_headers(
            progress, chapter_num, results["section_header_count"],
        )
        update_identical_phrases(
            progress, chapter_num, results["identical_phrase_count"],
        )
        update_numerical_density(
            progress, chapter_num, results["numerical_density"],
        )
        update_opening_repetition(
            progress, chapter_num, results["opening_repetition_ratio"],
        )
        fw = results["filter_words"]
        update_filter_words_context(
            progress, chapter_num,
            fw.get("narration_total", 0),
            fw.get("dialogue_total", 0),
        )

        # Log any warnings from this chapter's checks
        for w in results["warnings"]:
            add_warning(progress, {
                "chapter": chapter_num,
                "severity": "WARNING",
                "type": "threshold_violation",
                "message": w,
            })
        for c in results["critical"]:
            add_warning(progress, {
                "chapter": chapter_num,
                "severity": "CRITICAL",
                "type": "threshold_violation",
                "message": c,
            })

        # Growth rate spike detection (across last 3 chapters)
        gc = detect_growth_spike(progress, chapter_num, "来自", "CRITICAL", 0.5)
        sc = detect_growth_spike(progress, chapter_num, "的内容是", "WARNING", 0.5)
        mc = detect_growth_spike(progress, chapter_num, "沉默X秒", "WARNING", 0.5)

        # Flatline detection
        fl = detect_flatline_pattern(progress, chapter_num)

        # If growth spikes detected, escalate exit code
        if gc or sc or mc:
            if results["exit_code"] < 2:
                results["exit_code"] = 2
                print("  ⚠ Growth spike detected → escalating to CRITICAL")
        elif fl:
            if results["exit_code"] < 1:
                results["exit_code"] = 1
                print("  ⚠ Flatline pattern detected → escalating to WARNING")

        set_last_check(progress)
        save_progress(project_dir, progress)
        print(f"  ✓ progress.json updated")

    # -------- Phase 4: One-line summary --------
    if results["critical"]:
        severity = "CRITICAL"
        code = 2
    elif results["warnings"]:
        severity = "WARNING"
        code = 1
    else:
        severity = "CLEAN"
        code = 0

    counts_str = ", ".join(
        f"{k}={results['counts'][k]}" for k in ("来自", "的内容是", "沉默X秒")
    )
    fw = results["filter_words"]
    summary = (
        f"[quality_monitor] Ch{chapter_num}: {severity} | "
        f"{counts_str} | "
        f"em-dash={results['em_dash_density']:.3f} | "
        f"short-run={results['max_consecutive_short']} | "
        f"sect-hdr={results['section_header_count']} | "
        f"ident-phr={results['identical_phrase_count']} | "
        f"fw={fw.get('narration_total', 0)}/{fw.get('dialogue_total', 0)} | "
        f"num-dens={results['numerical_density']:.3f} | "
        f"open-rep={results['opening_repetition_ratio']:.3f} | "
        f"chars={results['total_chars']} | "
        f"warnings={len(results['warnings'])} critical={len(results['critical'])}"
    )
    print(summary)
    return code


# ===========================================================================
# CLI entry point
# ===========================================================================

def main() -> int:
    """Parse CLI arguments and invoke the quality monitor.

    Exit codes:
        0 — All clear, no issues.
        1 — Warnings present (non-blocking).
        2 — Critical issues (chapter should be regenerated).
    """
    parser = argparse.ArgumentParser(
        description=(
            "Quality Monitor — detect AI style degradation in novel chapters. "
            "Checks template phrases, em-dash density, and sentence rhythm."
        ),
    )
    parser.add_argument(
        "--chapter",
        required=True,
        help="Path to the chapter .md file to analyze.",
    )
    parser.add_argument(
        "--project",
        required=True,
        help="Path to the project root directory (contains memory/ folder).",
    )
    parser.add_argument(
        "--chapter-num",
        type=int,
        required=True,
        help="1-based chapter number being checked.",
    )
    parser.add_argument(
        "--update-progress",
        action="store_true",
        default=False,
        help="Write quality trends to PROJECT_DIR/memory/progress.json.",
    )

    args = parser.parse_args()

    # Resolve paths relative to CWD for robustness
    chapter_path = str(Path(args.chapter).resolve())
    project_dir = str(Path(args.project).resolve())

    try:
        exit_code = run(
            chapter_path=chapter_path,
            project_dir=project_dir,
            chapter_num=args.chapter_num,
            update_progress=args.update_progress,
        )
        return exit_code
    except FileNotFoundError as e:
        print(f"[quality_monitor] ERROR: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"[quality_monitor] UNEXPECTED ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
