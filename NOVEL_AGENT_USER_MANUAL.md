# Novel-Agent User Manual

## Quick Start

```bash
/novel-agent "your story description"
```

**Default**: 40 chapters, direct Chinese output, auto-test enabled.

---

## Commands

| Command | Description |
|---------|-------------|
| `/novel-agent "<desc>"` | Generate full novel (default: 40 chapters) |
| `/novel-agent "<desc>" --chapters N` | Specify chapter count |
| `/novel-agent "<desc>" --quick` | Quick mode (10 chapters, light polish) |
| `/novel-agent "<desc>" --polish` | Enable polish phase |
| `/novel-agent --project <name>` | Resume existing project |
| `/novel-agent --status` | Show current progress |
| `/novel-agent --list` | List all projects |
| `/novel-agent --test-only` | Test existing project |

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

## Output Files

```
novels/<project_name>/
├── memory/
│   ├── core_seed.md          (Story concept)
│   ├── character_dynamics.md (Character profiles + language)
│   ├── world_building.md     (World rules)
│   ├── chapter_blueprint.md  (TV structure for ALL chapters)
│   ├── character_names.json  (Chinese name mappings)
│   ├── world_terms.json      (Terminology)
│   └── progress.json         (Phase tracking)
│
├── output/
│   ├── chapters/             (Draft chapters)
│   └── final/zh-CN/
│       ├── chapter_001.md ~ chapter_N.md
│       └── novel_full_zh.md  (Complete Chinese novel)
│
└── test_report.md            (Quality validation)
```

---

## Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--chapters` | 5-100 | **40** | Total chapters |
| `--quick` | - | - | 10 chapters, faster |
| `--polish` | - | - | Enable polish phase |
| `--no-test` | - | - | Disable auto-test |

---

## Quality Guarantee

Auto-test validates 11 checks:

### CRITICAL checks (must pass):
- ✓ NO film script markers (## 【冷开场】, etc.)
- ✓ NO English vocabulary embedded in Chinese
- ✓ ALL names translated to Chinese

### Standard checks:
- ✓ Chapter count matches specification
- ✓ Word count ≥2000 per chapter
- ✓ POV filter words ≤5 per chapter
- ✓ Em-dash density ≤5%
- ✓ No consecutive short sentences (>2)
- ✓ Dialogue uses merged quote format
- ✓ Chinese punctuation ("")

**Critical check fails → regenerate immediately**

---

## Chinese Quality Requirements

| Requirement | Example |
|-------------|---------|
| All names translated | `Elena` → `埃琳娜` |
| No English embedding | ❌ `是某种更 coherent 的东西` |
| Pure Chinese prose | ✓ `是某种更连贯的东西` |
| No script markers | ❌ `## 【第一幕】` |

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
Test the pipeline before committing to 40 chapters.

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

## Eight Iron Laws Summary

| Iron Law | Rule | Check Method |
|----------|------|--------------|
| 铁律一 | No TV structure markers | grep |
| 铁律二 | Merge dialogue quotes | format check |
| 铁律三 | No meta-info | grep |
| 铁律四 | Em-dash ≤5% | density check |
| 铁律五 | Names translated | grep English names |
| 铁律六 | No English embedding | grep lowercase English |
| 铁律七 | Filter words ≤5/chapter | count |
| 铁律八 | No consecutive short sentences (>2) | sentence check |

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

**The agent orchestrator ensures consistent quality from Chapter 1 to Chapter 40.**