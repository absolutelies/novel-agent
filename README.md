# Novel-Agent

> AI-powered novel generation framework with isolated subagents for consistent quality across all chapters.

---

## What is Novel-Agent?

Novel-Agent is an AI orchestration framework that generates full-length Chinese novels through a phase-gate architecture:

- **Isolated Subagents**: Each phase uses fresh context to prevent quality degradation
- **Phase Gates**: Programmatic enforcement ensures no phase skipping
- **Direct Chinese Output**: No English intermediate - writes Chinese prose directly
- **Ten Iron Laws**: Automated quality validation with strict prose rules
- **Default 40 Chapters**: Scales to any length without degradation

---

## Quick Start

```bash
/novel-agent "your story description"

# Examples:
/novel-agent "cyberpunk mystery with AI detective in Neo-Tokyo"
/novel-agent "ancient Egypt where gods are dormant AI awakening" --chapters 20
/novel-agent "space detective on Mars colonies" --quick
```

**Default**: 40 chapters, direct Chinese output, auto-test enabled.

---

## Examples

### Full Novel (40 chapters)
```bash
/novel-agent "Ancient Egypt where gods are dormant AI awakening"
```
Output: 40 chapters, ~120,000 words in Chinese, auto-tested

### Custom Chapter Count
```bash
/novel-agent "Space detective on Mars colonies" --chapters 20
```
Output: 20 chapters, ~60,000 words in Chinese

### Quick Test
```bash
/novel-agent "Cyberpunk hacker discovers AI conspiracy" --chapters 5 --quick
```
Output: 5 chapters, faster generation

### Resume Project
```bash
/novel-agent --project egypt_ai_gods
```
Continues from last incomplete phase

---

## Architecture

### The Problem: Context Window Pollution

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

### The Solution: Orchestrator + Isolated Subagents

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

### Writer Agent Strategy

#### Sequential Batch Mode (Default)

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

#### Context Provided to Writer Agent

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

### Comparison: Old vs New Architecture

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

### Simplified Pipeline: Direct Chinese Output

#### Old Approach (Complex)
```
Blueprint → English Chapters → Polish → Translate → Chinese Chapters → Compile
```

#### New Approach (Simplified)
```
Blueprint → Chinese Chapters → [Polish*] → Compile → Test
```

**Benefits:**
- Eliminates English intermediate step
- Reduces phases from 9 to 6
- Maintains quality by writing Chinese directly
- Polish optional (triggered by `--polish` or test failure)

---

## 🔴 Language Flow（语言流程）

**Blueprint阶段之前：🇺🇸 全部英文 | chapter_summary阶段之后：🇨🇳 全部中文**

```
INIT ───→ IDEA ───→ WORLD ───→ BLUEPRINT ───→ [语言切换点] ───→ CHAPTERS ───→ TEST
  │         │          │           │                    │            │           │
  🇺🇸       🇺🇸        🇺🇸         🇺🇸                  🇨🇳          🇨🇳         🇨🇳
folder   core_seed   char_dyn    blueprint           prose_style   中文章节    测试报告
                      world       plot_arch           char_state
                      (英文)       (英文)              global_sum
                                                       chapter_sum
                                                       (全部中文)
```

| Phase | Output Files | Language |
|-------|-------------|----------|
| IDEA | `core_seed.md` | 🇺🇸 English |
| WORLD | `character_dynamics.md`, `world_building.md` | 🇺🇸 English |
| WORLD | `prose_style.md` | 🇨🇳 中文规则（风格规范） |
| BLUEPRINT | `chapter_blueprint.md`, `plot_architecture.md` | 🇺🇸 English |
| **语言切换点** | Writer读取英文Blueprint → 输出中文小说 | |
| CHAPTERS | `chapter_XXX.md` | 🇨🇳 中文 |
| CHAPTERS | `chapter_summary_XXX.md`, `character_state.md`, `global_summary.md` | 🇨🇳 中文 |

---

## Phase Gates (Strict Enforcement)

```
INIT ───→ IDEA ───→ WORLD ───→ BLUEPRINT ───→ CHAPTERS ───→ [POLISH*] ───→ COMPILE ───→ TEST ───→ DONE
  │        │         │           │              │              │*           │           │
  ▼        ▼         ▼           ▼              ▼              ▼opt         ▼           ▼
folder   seed.md   char.md    blueprint.md   ALL中文章节    polish?      merge      11 checks
created  EXISTS?   EXISTS?    HAS ALL?       in zh-CN/      (--polish)   files      PASS?
          MUST ✓    MUST ✓     MUST ✓         MUST ✓         SKIP↓       MUST ✓     MUST ✓

IF CHECK FAILS → REGENERATE THAT PHASE (never skip)
```

### Verification Details

| Phase | File Checked | Content Requirement |
|-------|-------------|---------------------|
| IDEA | `core_seed.md` | ≥200 words, ≥5 terms in glossary |
| WORLD | `character_dynamics.md`, `world_building.md` | ≥6 chars with language profiles, ≥15 terms |
| BLUEPRINT | `chapter_blueprint.md` | Explicit beats for ALL chapters (count verified) |
| CHAPTERS | `output/final/zh-CN/chapter_*.md` | ≥3000 words per chapter, 10 iron laws passed |
| COMPILE | `novel_full_zh.md` | Correct merge, proper formatting |
| TEST | `test_report.md` | 11 checks passed |

---

## Ten Iron Laws (十条铁律)

| Iron Law | Rule | Validation |
|----------|------|------------|
| 铁律一 | No TV structure markers in output | grep `## 【冷开场】` |
| 铁律二 | Merge dialogue quotes (Chinese format) | Format check |
| 铁律三 | No meta-info markers | grep `第四章完成` |
| 铁律四 | Em-dash density ≤5% | `count(——)/len ≤ 0.05` |
| 铁律五 | All names must be translated | grep English names |
| 铁律六 | Chinese purity (no English embedding) | grep lowercase English |
| 铁律七 | Deep POV (filter words ≤5/chapter) | Count `看见/听到/感到` |
| 铁律八 | No consecutive short sentences (≤2) | Sentence length check |
| 铁律九 | No chain deduction structures | `"来自" ≤ 5次/章` |
| 铁律十 | No template phrase substitutes | `"的内容是" ≤ 3次/章` |

### 铁律九：禁止链式推导结构

| 🔴 FORBIDDEN（链式推导） | ✅ CORRECT（复合句表达） |
|---|---|
| `机会来自塑造碰撞。塑造来自林昭计算。计算来自轨道力学。` | `塑造碰撞的机会源于林昭的轨道力学计算——一种基于帕特尔理论的牺牲方案。` |

### 铁律十：禁止模板句式替代

| 🔴 FORBIDDEN（模板替代） | ✅ CORRECT（个性表达） |
|---|---|
| `数据的内容是轨道参数` | `数据携带轨道参数——一组精确到毫秒的碰撞预测` |
| `沉默五秒。然后他开口。` | `五秒的沉默。咖啡杯在他手里转了一圈。然后："好。"` |

---

## Commands

| Command | Description |
|---------|-------------|
| `/novel-agent "<desc>"` | Create new project + generate (default: 40 chapters) |
| `/novel-agent "<desc>" --chapters N` | Specify chapter count |
| `/novel-agent "<desc>" --quick` | Quick mode (10 chapters, light polish) |
| `/novel-agent "<desc>" --polish` | Enable polish phase |
| `/novel-agent --project <name>` | Resume existing project |
| `/novel-agent --status` | Show current progress |
| `/novel-agent --list` | List all projects |
| `/novel-agent --test-only` | Test existing project |

---

## Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--chapters` | 5-100 | **40** | Total chapters |
| `--quick` | - | - | 10 chapters, faster |
| `--polish` | - | - | Enable polish phase |
| `--no-test` | - | - | Disable auto-test |

---

## What Happens Automatically

```
┌─────────────────────────────────────────────────────────────┐
│  1. INIT      → Create project folder structure              │
│  2. IDEA      → Generate story concept (web search + seed)   │
│  3. WORLD     → Build characters + world + glossary          │
│  4. BLUEPRINT → Design ALL chapter beats (TV structure)      │
│  5. CHAPTERS  → Write ALL chapters directly in Chinese       │
│  6. COMPILE   → Merge into novel_full_zh.md                  │
│  7. TEST      → Auto-validate quality (11 checks)            │
└─────────────────────────────────────────────────────────────┘
```

**Each phase uses isolated agents - no quality degradation.**

---

## Output Files

```
novels/<project_name>/
├── memory/
│   ├── core_seed.md           # Story concept (🇺🇸 English)
│   ├── character_dynamics.md  # Characters + language profiles (🇺🇸 English)
│   ├── world_building.md      # World dimensions (🇺🇸 English)
│   ├── prose_style.md         # Writing style rules (🇨🇳 中文)
│   ├── chapter_blueprint.md   # TV structure for ALL chapters (🇺🇸 English)
│   ├── character_names.json   # Chinese name mappings
│   ├── world_terms.json       # Terminology glossary
│   ├── character_state.md     # Character continuity (🇨🇳 中文)
│   ├── global_summary.md      # Story progress (🇨🇳 中文)
│   └── progress.json          # Phase tracking
│
├── output/
│   ├── chapters/              # Draft chapters
│   └── final/zh-CN/           # Final Chinese output (🇨🇳 中文)
│       ├── chapter_001.md ~ chapter_N.md
│       └── novel_full_zh.md   # Complete merged novel
│
└── test_report.md             # Quality validation
```

---

## Output Format: Novel Prose (Not Script)

**IMPORTANT**: Output is standard novel prose, NOT film script format.

TV structure is **INTERNAL pacing guide only** - never appears in output files.

### What you get:
```
第1章 觉醒

大埃及博物馆在凌晨两点四十七分沉睡在黑暗中...

[自然段落]
[对话场景]
[故事推进]

...张力建立...
...高潮...
...结尾悬念...
```

### NOT film script (FORBIDDEN):
```
## 【冷开场】      ← 严禁输出
## 【第一幕】      ← 严禁输出
## 【尾声】        ← 严禁输出
```

---

## Quality Validation (11 Checks)

| Check | Iron Law | Threshold |
|-------|----------|-----------|
| Script markers | 铁律一 | 0 occurrences |
| Meta-info | 铁律三 | 0 occurrences |
| English vocabulary | 铁律六 | 0 embedded words |
| POV filter words | 铁律七 | ≤5 per chapter |
| Em-dash density | 铁律四 | ≤5% |
| Name translation | 铁律五 | 0 English names |
| Sentence rhythm | 铁律八 | ≤2 consecutive short |
| Chain deduction | 铁律九 | "来自" ≤5 per chapter |
| Template phrases | 铁律十 | "的内容是" ≤3 per chapter |
| Chapter count | - | = configured count |
| Word count | - | ≥2000 per chapter |

**Critical check fails → regenerate affected chapters immediately**

---

## Chinese Quality Requirements

| Requirement | Example |
|-------------|---------|
| All names translated | `Elena` → `埃琳娜` |
| No English embedding | ❌ `是某种更 coherent 的东西` |
| Pure Chinese prose | ✓ `是某种更连贯的东西` |
| No script markers | ❌ `## 【第一幕】` |

---

## Command Files

```
.claude/commands/
├── novel-agent.md           # Main orchestrator
├── novel-agent-execution.md # Execution guide
├── idea.md                  # IDEA phase
├── worldbuild.md            # WORLD phase
├── outline.md               # BLUEPRINT phase
├── write.md                 # CHAPTERS phase
├── polish.md                # Polish phase
├── translate.md             # Translation helpers
└── status.md                # Progress tracking
```

---

## Why Novel-Agent?

| Problem | Single-Context Approach | Novel-Agent Solution |
|---------|------------------------|---------------------|
| Quality degradation | Ch1 good, Ch40 garbage | Fresh context per agent |
| Phase skipping | Documentation only | Programmatic gates |
| Blueprint truncation | "[Chapters 4-40...]" | Full coverage enforced |
| Scalability | ~10 chapters max | 40+ chapters easy |
| Error recovery | Restart everything | Regenerate phase only |
| Style amplification | "来自" chain grows | prose_style.md fixed rules |

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

## Resuming Interrupted Projects

```bash
/novel-agent --project <name>
```

Orchestrator:
1. Reads `progress.json`
2. Finds last completed phase
3. Resumes from next phase
4. Re-verifies previous outputs

---

## Checking Progress

```bash
/novel-agent --status
```

Shows:
- Current phase
- Completed phases
- Chapters written
- Test status

---

## Tips

### 1. Start Small for Testing
```bash
/novel-agent "test story" --chapters 3 --quick
```

### 2. Use Detailed Descriptions
```bash
/novel-agent "Cyberpunk Tokyo 2077. Memory trader discovers neural implants harvesting memories. Yakuza involvement. Protagonist's sister was first victim."
```
More context = better story seed.

### 3. Resume After Errors
```bash
/novel-agent --project <name>
```
Only failed phase regenerated, not entire novel.

---

## Troubleshooting

### Phase Fails 3 Times
- Orchestrator pauses
- Reports error to user
- Check `progress.json` for details

### Blueprint Truncated
- Orchestrator detects incomplete
- Respawns architect agent
- Enforces explicit beats for ALL chapters

### Quality Check Fails
- Check `test_report.md` for details
- Regenerate specific phase:
  ```bash
  /novel-agent --project <name>
  ```

---

## File Locations

| File | Location |
|------|----------|
| Project folder | `novels/<project_name>/` |
| Progress tracking | `memory/progress.json` |
| Chinese novel | `output/final/zh-CN/novel_full_zh.md` |
| Test report | `test_report.md` |
| All projects index | `novels/projects_index.json` |

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

---

## License

MIT License