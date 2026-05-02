# Novel-Agent Architecture Review

## Overview

Novel-Agent uses an **orchestrator + isolated subagents** architecture to solve the fundamental limitation of single-context approaches: context window pollution causes quality degradation as chapter count increases.

---

## The Problem: Context Window Pollution

Single-context approaches cannot scale:

```
Phase 1 (INIT):     ~5k tokens   → Fresh context ✓
Phase 2 (IDEA):     ~10k tokens  → Still good ✓
Phase 3 (CHAR):     ~15k tokens  → Good ✓
Phase 4 (WORLD):    ~20k tokens  → Good ✓
Phase 5 (PLOT):     ~25k tokens  → Good ✓
Phase 6 (BLUE):     ~40k tokens  → Starting to degrade ⚠
Phase 7 (CH1):      ~50k tokens  → Good ✓
Phase 7 (CH10):     ~100k tokens → Template patterns emerge ❌
Phase 7 (CH20):     ~150k tokens → Garbage output ❌
Phase 7 (CH40):     ~200k tokens → Complete degradation ❌
Phase 8 (POLISH):   ~250k tokens → Can't process properly ❌
Phase 9 (TRANSLATE): ~300k tokens → Can't translate properly ❌
```

**Symptoms of single-context failure:**
- Phase skipping (no enforcement)
- Quality degradation (template garbage at later chapters)
- Blueprint truncation ("[Chapters 4-40 continue...]")
- Pipeline stops early (only 1-10 chapters written)

---

## The Solution: Agent Orchestrator + Isolated Subagents

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│  ORCHESTRATOR (novel-agent.md)                                  │
│  - Coordinates subagents                                         │
│  - Enforces phase gates (CODE, not docs)                        │
│  - Verifies outputs before proceeding                            │
│  - Default: 40 chapters                                          │
│  - Direct Chinese output (no English intermediate)              │
└─────────────────────────────────────────────────────────────────┘
            │ spawns isolated agents (fresh context each)
            ↓
     ┌──────┴──────┬──────────┬──────────┬──────────┬──────────┐
     │             │          │          │          │          │
┌───┴───┐    ┌───┴───┐  ┌───┴───┐  ┌───┴───┐  ┌───┴───┐  ┌───┴───┐
│IDEATOR│    │WORLD  │  │ARCHI- │  │WRITER │  │POLISH │  │TEST   │
│Agent  │    │BUILDER│  │TECT   │  │Agents │  │Agent  │  │Agent  │
│       │    │Agent  │  │Agent  │  │(中文) │  │(opt)  │  │       │
└───────┘    └───────┘  └───────┘  └───────┘  └───────┘  └───────┘
```

### Key Design Principles

| Principle | Implementation | Benefit |
|-----------|---------------|---------|
| Context Isolation | Each agent starts fresh | No degradation across chapters |
| Phase Gates | File existence + content verification | No phase skipping |
| Batch Writing | Sequential (batch_size=1) | Timeout prevention |
| Programmatic Enforcement | Code checks, not docs | Can't bypass requirements |
| Direct Chinese | No English intermediate | Simplified pipeline |

---

## Phase Gate Enforcement

```
PHASE ORDER (MANDATORY - VERIFIED BY CODE):

INIT ───→ IDEA ───→ WORLD ───→ BLUEPRINT ───→ CHAPTERS ───→ [POLISH*] ───→ COMPILE ───→ TEST ───→ DONE
  │        │         │           │              │              │*           │           │
  ▼        ▼         ▼           ▼              ▼              ▼opt         ▼           ▼
folder   seed.md   char.md    blueprint.md   ALL中文章节    polish?      merge      11 checks
created  EXISTS?   EXISTS?    HAS ALL?       in zh-CN/      (--polish)   files      PASS?
         MUST ✓    MUST ✓     MUST ✓         MUST ✓         SKIP↓       MUST ✓     MUST ✓

IF CHECK FAILS → REGENERATE THAT PHASE (not skip)
```

### Verification Details

| Phase | File Checked | Content Requirement |
|-------|-------------|---------------------|
| IDEA | `core_seed.md` | ≥200 words, ≥5 terms in glossary |
| WORLD | `character_dynamics.md`, `world_building.md` | ≥6 chars with language profiles, ≥15 terms |
| BLUEPRINT | `chapter_blueprint.md` | Explicit beats for ALL chapters (count verified) |
| CHAPTERS | `output/final/zh-CN/chapter_*.md` | ≥3000 words per chapter, 8 iron laws passed |
| COMPILE | `novel_full_zh.md` | Correct merge, proper formatting |
| TEST | `test_report.md` | 11 checks passed |

---

## Writer Agent Strategy

### Sequential Batch Mode (Default)

```
batch_size = 1 (one chapter at a time)
parallel_mode = false (sequential execution)

for chapter_num = 1 to chapter_count:
    Spawn 1 agent with run_in_background: true
    Wait for completion (auto-notification)
    Update continuity files
    Create chapter_summary for next chapter
    Continue to next chapter
```

**Why Sequential:**
- Timeout prevention: Single chapter completes within window
- Continuity preserved: Each chapter reads previous summary
- Quality maintained: Fresh isolated context for each agent
- Reliable: No parallel timeout cascades

### Context Provided to Writer Agent

| File | Purpose |
|------|---------|
| `core_seed.md` | Story concept, genre, conflict |
| `character_dynamics.md` | Character profiles + language style |
| `world_building.md` | World rules, power structure |
| `chapter_blueprint.md` | TV structure for that chapter ONLY |
| `character_state.md` | Current character states |
| `global_summary.md` | Story progress summary |
| `chapter_summary_{N-1}.md` | Previous chapter summary (if N>1) |
| `character_names.json` | Chinese name mappings |
| `world_terms.json` | Terminology glossary |

---

## Comparison: Old vs New Architecture

| Factor | Single Command | Agent Orchestrator |
|--------|----------------|-------------------|
| Context quality | Degrades over time | Always fresh |
| Phase enforcement | Documentation only | Code verification |
| Scalability | ~10 chapters max | 40+ chapters easy |
| Quality consistency | Ch1 good, Ch40 bad | All chapters equal |
| Parallelization | None | Sequential batches |
| Error recovery | Manual restart | Auto-regenerate phase |
| Blueprint coverage | Truncates early | Full coverage forced |
| Language pipeline | English → Translate | Direct Chinese |
| Test validation | None | Auto-test (11 checks) |

---

## Eight Iron Laws Enforcement

Each Writer Agent must verify before exiting:

| Iron Law | Check | Threshold |
|----------|-------|-----------|
| 铁律一 | grep script markers | 0 occurrences |
| 铁律二 | dialogue format check | merged quotes |
| 铁律三 | grep meta-info | 0 occurrences |
| 铁律四 | em-dash density | ≤5% |
| 铁律五 | grep English names | 0 occurrences |
| 铁律六 | grep embedded English | 0 occurrences |
| 铁律七 | filter word count | ≤5 per chapter |
| 铁律八 | consecutive short sentences | ≤2 |

---

## Progress Tracking

```json
{
  "project": "project_name",
  "status": "IN_PROGRESS",
  "chapter_count": 40,
  "phases": {
    "init": {"status": "complete"},
    "idea": {"status": "complete", "agent_id": "...", "verified": true},
    "world": {"status": "complete", "agent_id": "...", "verified": true},
    "blueprint": {"status": "complete", "chapter_count_verified": 40},
    "chapters": {"status": "in_progress", "completed_count": 5},
    "compile": {"status": "pending"},
    "test": {"status": "pending"}
  }
}
```

---

## Simplified Pipeline: Direct Chinese Output

### Old Approach (Complex)
```
Blueprint → English Chapters → Polish → Translate → Chinese Chapters → Compile
```

### New Approach (Simplified)
```
Blueprint → Chinese Chapters → [Polish*] → Compile → Test
```

**Benefits:**
- Eliminates English intermediate step
- Reduces phases from 9 to 6
- Maintains quality by writing Chinese directly
- Polish optional (triggered by `--polish` or test failure)

---

## Conclusion

**The orchestrator + isolated subagents architecture solves all observed failures:**

| Problem | Solution |
|---------|----------|
| Context pollution | Fresh context per agent |
| Phase skipping | Programmatic phase gates |
| Blueprint truncation | Explicit chapter count verification |
| Quality degradation | Isolated writer agents |
| Language pipeline complexity | Direct Chinese output |

**Result: Consistent quality from Chapter 1 to Chapter 40+.**