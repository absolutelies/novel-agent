# /write - Chapter Content Generation

> Generate chapter prose in English with proper file naming.
> Output is NOVEL PROSE, not film script. TV structure is INTERNAL guidance only.

## CRITICAL: Novel Prose Output (NOT Film Script)

**OUTPUT FORMAT**: Standard novel prose with natural paragraphs and dialogue.
**FORBIDDEN**: Film script markers like "## ACT 1", "## Cold Open", "## Tag"

TV Drama Structure is **INTERNAL pacing guidance** only:
- Cold Open → Opening paragraph that hooks reader
- Act 1-5 → Natural story progression (no headers)
- Tag → Final paragraph that leaves tension

**Internal pacing reference (DO NOT output these headers):**
| TV Element | Novel Equivalent |
| Cold Open | Opening 3-5 paragraphs with hook |
| Act 1 | First 15% of chapter - setup |
| Act 2 | Rising tension - complications |
| Act 3 | Midpoint twist/revelation |
| Act 4 | Climax confrontation |
| Act 5 | Resolution aftermath |
| Tag | Final 2-3 paragraphs with tension |

---

## CRITICAL: English Output Required

1. **All content must be 100% English**
2. **File naming**: `chapter_{number}_{title_snake_case}.md`
3. **Search sources**: Only Western websites (US/EU)

---

## Usage

```bash
/write                               — Continue from current chapter
/write --chapter N                   — Generate specific chapter N
/write --chapters N-M                — Generate chapters N through M
/write --all                         — Generate all remaining chapters
/write --batch N                     — Generate next N chapters (batch mode)
```

---

## File Naming Convention

Each chapter file follows this format:

**Draft files**: `output/chapters/chapter_{number}_{title_snake_case}.md`

**Polished files**: `output/final/chapter_{number}_{title_snake_case}_polished.md`

**Examples**:
- Chapter 1 "The Awakening" → `chapter_001_the_awakening.md`
- Chapter 5 "Dark Secrets Revealed" → `chapter_005_dark_secrets_revealed.md`
- Chapter 12 "A Journey Begins" → `chapter_012_a_journey_begins.md`

**Snake case rules**:
- Lowercase only
- Spaces → underscores
- Numbers: 001, 002... (3 digits, leading zeros)
- Remove special characters
- Max 50 characters for title portion

---

## Process

### Context Files Reading (BEFORE chapter generation)

**⚠️ QUANTIZED RETRIEVAL - 只加载相关切片，不加载全文件**

**问题**: 全量加载导致 ~100KB context → Token溢出 → 质量退化
**解决**: Quantized Retrieval → 只加载当前章节相关内容 (~15-20KB)

---

### 🔒 POSITION-AWARE ORDERING (Lost-in-Middle Prevention)

**科学依据**: LLM在长context中，首尾准确率~95%，中间<50%
**策略**: 关键信息放在首尾两端，次要信息放中间

**🔴 CRITICAL: 防风格正反馈 - prose_style.md 放首位**

**MUST read these files in THIS ORDER for continuity:**

```
[START] 必读（风格+故事核心）─────────────────────────────────────
1. **Prose Style** (`memory/prose_style.md`)
   - 🔴 CRITICAL: Fixed writing style rules for ALL chapters
   - Sentence structure rules, forbidden patterns (chain structures)
   - Dialogue style, emotion expression rules
   - **Prevents style amplification: read fixed style, NOT previous chapter's style**

2. **Character Seed** (`memory/core_seed.md`)
   - Story concept, genre, core conflict
   - CRITICAL: Establishes fundamental constraints

3. **Chapter Blueprint** (Act-based files)
   - NEW: Read ONLY relevant Act file
   - If chapter 1-10: `memory/chapter_blueprint_act1.md`
   - If chapter 11-20: `memory/chapter_blueprint_act2.md`
   - etc.
   - ⚠️ Search for: "### Chapter {N}"
   - Load ~2KB instead of full 81KB blueprint
   - CRITICAL: Provides TV structure for THIS chapter only

[MIDDLE] 按需加载 ─────────────────────────────────────
4. **Character Dynamics** (Selective loading)
   - Read chapter_summary_{N-1} to identify active characters
   - Load ONLY profiles for characters appearing in Chapter N
   - Typically 2-3 profiles (~5KB)
   - Skip profiles for characters not in this chapter

5. **World Building** (Selective loading)
   - Check blueprint for locations/settings mentioned
   - Load ONLY relevant world sections
   - Typically ~3KB for relevant portions

[END] 连续性+铁律 ───────────────────────────────────────
6. **Character States** (`memory/character_state.md`)
   - Current physical/mental/social status of all characters
   - Items, abilities, resources each character holds
   - Relationship states and tensions
   - Triggered events and current goals
   - CRITICAL: This ensures character continuity across chapters

7. **Global Summary** (`memory/global_summary.md`)
   - Running story summary (compressed for efficiency)
   - Unresolved threads and suspense tracking
   - Foreshadowing status (planted, reinforced, paid off)
   - Recent 5 chapters detailed, early chapters compressed
   - CRITICAL: This ensures plot continuity across chapters

8. **Previous Chapter Summary** (`memory/chapter_summary_{N-1}.md`)
   - Only if chapter > 1
   - ⚠️ **PLOT continuity ONLY - DO NOT inherit sentence style from summary**
   - Key events, character changes, unresolved threads from previous chapter
   - Next chapter setup (hook, tension point, expected pickup)
   - CRITICAL: This ensures chapter-to-chapter continuity

[END] 铁律 ─────────────────────────────────────────────
9. **Anti-Template Quality Rules** (见下方FORBIDDEN patterns)
   - CRITICAL: Must be at END position for attention retention
```

---

**⚠️ DO NOT read previous chapter's full prose** (`output/chapters/` or `output/final/`).
Reading full prose causes style amplification feedback loops (e.g., em-dash density escalates chapter-over-chapter until text becomes fragmented gibberish).
The chapter summary contains all necessary continuity information.

**⚠️ DO NOT inherit sentence style from chapter summary.**
If summary contains chain structures ("X来自Y。Y来自Z。"), ignore that style and follow prose_style.md rules only.

---

### Pre-Chapter Preparation

For each chapter:

1. **Read Chapter Blueprint**
   - Extract metadata for target chapter
   - Get chapter title for file naming

2. **Generate Three-Chapter Summary** (for internal pacing only)
   - If chapter > 3: summarize N-3, N-2, N-1 from blueprint
   - Create current context summary for pacing reference

3. **Read Context Files** (all in English):
   - Character states
   - Global summary
   - World building

### Chapter Generation

Generate chapter prose:
- **Language**: 100% English (enforced)
- **Dialogue**: Western format (double quotes)
- **Punctuation**: Standard English
- **Word count**: {target_words} (typically 3000)

### CRITICAL: Anti-Template Quality Enforcement

**FORBIDDEN patterns (will corrupt novel quality):**

| Pattern | Example (BAD) | Required Fix |
|---------|---------------|--------------|
| **Film script headers** | `## ACT 1`, `## Cold Open`, `## Tag` | **DELETE** - Write novel prose instead |
| **Scene markers** | `## Scene 1`, `---` with labels | Natural paragraph transitions |
| Repetitive scene headers | `## ACT 1` only | **DELETE** - No headers at all |
| Template dialogue | `"X confirmed." "Y reported."` | Natural conversation with personality |
| Summary prose | `Claya analyzed the situation.` | Show: She traced patterns on the display... |
| Passive beats | `The countdown continued.` | Active: Her pulse matched the amber descent. |
| Q&A loops | Question → confirmation | Dialogue with subtext, disagreement, tension |
| Identical structures | Same pattern each scene | Vary: short punch, long flow, mix |
| Generic actions | `X approached Y.` | Specific: She stepped past the ceramic barrier... |
| Empty transitions | `Time passed.` | Specific: Three firing cycles completed... |
| **Em-dash fragmentation** | `他——的——手——在——键——盘——上` | Normal punctuation: `他的手悬在键盘上方` |
| **Em-dash overuse** | Every phrase separated by ——  | Em-dash density must stay ≤5% of paragraph character count |

**OUTPUT FORMAT FOR NOVEL:**

```
# Chapter 1 - The Awakening

[Opening paragraph - hook the reader]
[Setup paragraphs]
[Dialogue scene with natural flow]
[Rising tension]
[Midpoint revelation - no marker]
[Climax]
[Resolution]
[Final paragraph - tension for next chapter]

**End of Chapter 1**
```

**NO markers like**: ## Act 1, ## Cold Open, ## Tag, ## Scene

**REQUIRED narrative elements:**

1. **Sensory grounding** - What characters see/hear/touch/smell
   - Example: "The fired clay pulsed with residual heat, geometric patterns shifting beneath her fingers."
   - NOT: "The clay had patterns."

2. **Specific actions** - What characters DO (not think/analyze)
   - Example: "She pressed her decoder pendant against the ceramic surface, watching patterns realign."
   - NOT: "She analyzed the ceramic."

3. **Distinctive dialogue** - Each character has unique voice patterns
   - Reference `character_dynamics.md` for each character's:
     - Catchphrases/tone
     - Sentence patterns
     - Emotional expression style
   - NO characters speaking in same template style

4. **Tension beats** - Stakes rising through specific events
   - Example: "Elder Kiln's voice hardened. 'Authorization denied.' The rejection landed like a clay exposure sentence."
   - NOT: "Authorization was denied."

5. **Scene transitions** - Clear markers for time/location changes
   - Example: "---\n\n**Three firing cycles later...**\n\nThe eastern observation deck..."
   - NOT: Generic scene breaks without context

**Dialogue quality checks:**

- ✓ Does each character sound different?
- ✓ Is there subtext (characters don't say exactly what they mean)?
- ✓ Are there interruptions, deflections, evasions?
- ✗ NO perfect Q&A patterns (question → answer = forbidden)
- ✗ NO "X confirmed/reported/noted" patterns
- ✗ NO identical dialogue across characters

**Burstiness enforcement:**

Sentence length MUST vary within each paragraph:
- Mix: 5-word punch → 20-word flow → 8-word action → 30-word description
- NOT: Uniform 15-word sentences throughout

### File Saving

Save with correct naming:
```
title_snake = chapter_title.lower().replace(' ', '_').replace('-', '_')
title_snake = re.sub(r'[^\w_]', '', title_snake)[:50]
filename = f"chapter_{chapter_number:03d}_{title_snake}.md"
```

Example:
- Title: "The Memory Trader"
- Snake: "the_memory_trader"
- Filename: "chapter_001_the_memory_trader.md"

### Post-Chapter Processing (CRITICAL for continuity)

**After writing each chapter, MUST update continuity files:**

1. **Save Chapter** → `output/chapters/chapter_NNN_title.md`
   - Ensure proper file naming (snake_case title)
   - Verify word count ≥ target_words

2. **Create Chapter Output Summary** → `memory/chapter_summary_N.md`
   - Use format from `prompts/chapter_output_summary.txt`
   - Include: Key Events, Character Changes, Unresolved Threads, Foreshadowing Status
   - This file will be read by NEXT chapter's agent for continuity
   - **CRITICAL**: Without this, next chapter loses continuity

3. **Update Character States** → `memory/character_state.md`
   - Apply changes from chapter events
   - Update: Items, Physical/Mental status, Relationships, Triggered Events, Goals
   - Use tree format as specified in `prompts/character_state.txt`
   - **CRITICAL**: Character states must reflect chapter changes

4. **Update Global Summary** → `memory/global_summary.md`
   - Integrate chapter's key events into running summary
   - Preserve unresolved threads and active foreshadowing
   - Compress resolved conflicts, maintain thread tracking
   - Use format from `prompts/global_summary.txt`
   - **CRITICAL**: Global summary must stay updated for overall continuity

5. **Update Progress** → `memory/progress.json`
   - Mark chapter N as complete
   - Log word count and agent ID

---

## Output Format

Per chapter:

```
✓ Chapter {N} Complete
  Title: {chapter_title}
  Words: {count}
  Output: output/chapters/chapter_{N}_{title_snake}.md
  
Progress: {current}/{total}
```

---

## Dependencies

Requires (all must exist):
- `memory/core_seed.md` (🇺🇸 English) - Story concept
- `memory/character_dynamics.md` (🇺🇸 English) - Character profiles
- `memory/world_building.md` (🇺🇸 English) - World settings
- `memory/chapter_blueprint.md` (🇺🇸 English) - TV structure for this chapter
- `memory/prose_style.md` (🇨🇳 中文) - Writing style rules
- `memory/character_state.md` (🇨🇳 中文) - Character continuity
- `memory/global_summary.md` (🇨🇳 中文) - Plot continuity

Optional (for chapters > 1):
- `memory/chapter_summary_{N-1}.md` (🇨🇳 中文) — previous chapter's summary for continuity

**🔴 Language Flow**: 
- Blueprint阶段之前：🇺🇸 English (core_seed, character_dynamics, world_building, chapter_blueprint)
- chapter_summary阶段之后：🇨🇳 中文 (prose_style, character_state, global_summary, chapter_summary)

**⚠️ DO NOT read previous chapter's full prose** — causes style amplification feedback loops.

---

## Requirements

1. **100% English content**
2. **Correct file naming** (snake_case title)
3. **Western dialogue format**
4. **Consistent character voices**
5. **Show-don't-tell prose**