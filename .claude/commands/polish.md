# /polish - AI Trace Removal (Humanizer System)

> Remove ALL AI writing patterns through 8-round comprehensive processing.
> Makes prose human-like based on 2024 research of AI writing markers.

## Usage

```
/polish                              — Polish current chapter (auto-detect)
/polish --chapter N                  — Polish specific chapter N
/polish --all                        — Polish all chapters
/polish --depth quick                — Rounds 1-3 (fast cleanup)
/polish --depth standard             — Rounds 1-6 (thorough) [default]
/polish --depth deep                 — Rounds 1-8 (complete humanization)
/polish --depth ultra                — Rounds 1-8 + manual review (max quality)
/polish --verify                     — Run verification only (no changes)
```

---

## Depth Options

| Depth | Rounds | Focus | Time | Use Case |
|-------|--------|-------|------|----------|
| quick | 1-3 | Sentence patterns + vocabulary | Fast | Draft cleanup |
| standard | 1-6 | Through dialogue humanization | Medium | Production ready [default] |
| deep | 1-8 | Complete humanization | Longer | Publication quality |
| ultra | 1-8 + review | Maximum human quality | Longest | Final manuscript |

---

## Round Overview

### Round 1: Sentence Patterns (R1-R2)
- R1: "Not A but B" → single affirmation
- R2: Sparse formatting → merge paragraphs

### Round 2: AI Vocabulary (R3-R5, R9-R10)
- R3: Connector words → delete (Furthermore, Moreover, Additionally)
- R4: Synonym rotation → unify
- R5: Filler phrases → delete
- R9: **Delve family** → replace (TOP AI markers from research)
  - delve → explore/dig into
  - tapestry → web/mix
  - testament → proof/sign
  - symphony → mix/blend
  - realm → world/area
  - kaleidoscope → changing mix
  - nuance → detail/shade
  - myriad → many/countless
  - intricate → complex/detailed
  - ethereal → ghostly/faint
  - palpable → clear/strong
  - profound → deep/meaningful
- R10: Academic vocabulary → replace (implement, facilitate, demonstrate)

### Round 3: Rhythm & Structure (R6-R7)
- R6: Structure repetition → vary
- R7: Three-part patterns → 2 or 4 parts

### Round 4: Fiction Cliches (R11-R12)
- R11: **Body/emotion cliches** → delete
  - shivers ran down his spine
  - her heart pounded/raced
  - his breath caught
  - a wave of emotion
  - she couldn't help but
  - without thinking
- R12: AI metaphors → delete
  - like a symphony/tapestry/dance
  - wind whispered/sunlight danced

### Round 5: Dialogue Humanization (R13-R16)
- R13: Perfect → natural (fragments, interruptions, fillers)
- R14: Direct → subtext (emotion → action)
- R15: Power dynamics (speech length variation)
- R16: Conversational imperfections

### Round 6: Detail Pruning (R8)
- Remove useless details
- Protect: action scenes, intimacy, key dialogue, character appearance

### Round 7: Burstiness Injection (R17-R20)
- R17: Sentence length variation (burst patterns)
- R18: Paragraph variation (mix lengths)
- R19: Opening word variation
- R20: Ending variation

### Round 8: Final Human Pass (R21-R25)
- R21: Personal voice injection (opinions, attitude)
- R22: Imperfection injection (fragments, run-ons, And/But)
- R23: Specificity (abstract → concrete numbers/names)
- R24: Opinion/attitude (neutral → opinionated)
- R25: Grammar roughness (perfect → natural)

---

## Process

### For Each Chapter

1. **Load Draft**
   - Read from `output/chapters/chapter_NNN_*.md`

2. **Load Context**
   - Character language profiles (for dialogue round)
   - Chapter blueprint (for protected content)
   - Outline context (for R8 protection)

3. **Execute Rounds Sequentially**
   - Each round takes previous round output
   - Track all modifications per round
   - Pass modified text forward

4. **Run Verification**
   After final round, check:
   - ✓ No delve/tapestry/testament vocabulary
   - ✓ No Furthermore/Moreover connectors
   - ✓ No body emotion cliches
   - ✓ Dialogue has natural imperfections
   - ✓ Sentence length varies (burstiness)
   - ✓ Paragraphs vary in length
   - ✓ Contains fragments/run-ons
   - ✓ Has personality and voice
   - ✓ Specific numbers instead of abstract
   - ✓ Opinions/attitude present

5. **Save Polished**
   - Write to `output/final/chapter_NNN_*_polished.md`

6. **Log Progress**
   - Update progress.json with polish completion

---

## After All Chapters

Compile final novel:
```
Merge all polished chapters
Add chapter separators
Write to output/final/novel_full_polished.md
```

---

## Output Format

### Per Chapter

```
✓ Chapter {N} Polished
  Depth: {depth}
  Rounds: {rounds applied}
  Total Changes: {count}
  
  | Round | Rules | Modifications |
  |-------|-------|---------------|
  | 1 | R1-R2 | {count} |
  | 2 | R3-R5, R9-R10 | {count} |
  | 3 | R6-R7 | {count} |
  | 4 | R11-R12 | {count} |
  | 5 | R13-R16 | {count} |
  | 6 | R8 | {count} |
  | 7 | R17-R20 | {count} |
  | 8 | R21-R25 | {count} |
  
  Verification: {passes}/{total checks}
  Output: output/final/chapter_{N}_polished.md
```

### Final Compilation

```
✓ Novel Compiled
  Total chapters: {count}
  Total words: {count}
  Total modifications: {count}
  Output: output/final/novel_full_polished.md
  
Status: POLISH COMPLETE → Ready for translation
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `ai_humanizer_comprehensive.txt` | Full system documentation |
| `humanizer_master.txt` | Round execution orchestration |
| `polish_round1.txt` | R1-R2 execution |
| `polish_round2_enhanced.txt` | R3-R5, R9-R10 execution |
| `polish_round3.txt` | R6-R7 execution |
| `polish_round4_fiction.txt` | R11-R12 execution |
| `polish_round5_dialogue.txt` | R13-R16 execution |
| `polish_round4.txt` | R8 execution |
| `polish_round7_burstiness.txt` | R17-R20 execution |
| `polish_round8_human.txt` | R21-R25 execution |

---

## Key AI Markers Removed (Research-Based)

**TOP AI Vocabulary Markers** (Science Alert, ZDNet 2024):
- delve (100x more in AI)
- tapestry (AI favorite metaphor)
- testament (AI overuse)
- symphony (AI overuse)
- realm (AI favorite)
- kaleidoscope (AI pattern)
- Furthermore/Moreover/Additionally (AI connectors)

**TOP AI Fiction Cliches**:
- shivers ran down his spine
- heart pounded/raced
- breath caught
- wave of emotion
- couldn't help but

**AI Structural Patterns**:
- Uniform sentence length
- Perfect grammar
- Balanced paragraphs
- Neutral tone
- Abstract descriptions