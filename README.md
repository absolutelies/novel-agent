# Novel-Agent

> AI-powered novel generation framework with isolated subagents for consistent quality across all chapters.

---

## What is Novel-Agent?

Novel-Agent is an AI orchestration framework that generates full-length Chinese novels through a phase-gate architecture:

- **Isolated Subagents**: Each phase uses fresh context to prevent quality degradation
- **Phase Gates**: Programmatic enforcement ensures no phase skipping
- **Direct Chinese Output**: No English intermediate - writes Chinese prose directly
- **Eight Iron Laws**: Automated quality validation with strict prose rules
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

---

## Architecture

```
ORCHESTRATOR
    │ spawns isolated agents (fresh context each)
    ↓
┌─────────┬─────────┬─────────┬─────────┬─────────┐
│ IDEATOR │ WORLD   │ ARCHI-  │ WRITER  │ TEST    │
│ Agent   │ BUILDER │ TECT    │ Agents  │ Agent   │
│         │ Agent   │ Agent   │ (中文)  │         │
└─────────┴─────────┴─────────┴─────────┴─────────┘

Each agent: ISOLATED context → No degradation across 40+ chapters
```

### Phase Gates (Strict Enforcement)

```
INIT → IDEA → WORLD → BLUEPRINT → CHAPTERS → COMPILE → TEST → DONE
 │      │       │         │          │          │        │
 ▼      ▼       ▼         ▼          ▼          ▼        ▼
folder seed.md char.md  blueprint  中文章节   merged    11 checks
created ✓?     ✓?       ✓?        ✓?         ✓?       ✓?

IF CHECK FAILS → REGENERATE THAT PHASE (never skip)
```

---

## Eight Iron Laws (八条铁律)

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

---

## Commands

| Command | Description |
|---------|-------------|
| `/novel-agent "<desc>"` | Create new project + generate (default: 40 chapters) |
| `/novel-agent "<desc>" --chapters N` | Specify chapter count |
| `/novel-agent "<desc>" --quick` | Quick mode (10 chapters, light polish) |
| `/novel-agent --project <name>` | Resume existing project |
| `/novel-agent --status` | Show current progress |
| `/novel-agent --list` | List all projects |
| `/novel-agent --test-only` | Test existing project |

---

## Project Structure

```
novels/[project_name]/
├── memory/
│   ├── core_seed.md           # Story concept
│   ├── character_dynamics.md  # Characters + language profiles
│   ├── world_building.md      # World dimensions
│   ├── chapter_blueprint.md   # TV structure for ALL chapters
│   ├── character_names.json   # Chinese name mappings
│   ├── world_terms.json       # Terminology glossary
│   └── progress.json          # Phase tracking
└── output/
    ├── chapters/              # Draft chapters
    └── final/zh-CN/           # Final Chinese output
        ├── chapter_001.md ~ chapter_N.md
        └── novel_full_zh.md   # Complete merged novel
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
| Chapter count | - | = configured count |
| Word count | - | ≥2000 per chapter |
| Dialogue format | 铁律二 | merged quotes |
| Punctuation | - | Chinese quotes "" |

**Critical check fails → regenerate affected chapters immediately**

---

## Configuration

| Setting | Default | Override |
|---------|---------|----------|
| Total chapters | 40 | `--chapters N` |
| Words per chapter | 3000 | `--words N` |
| Auto-test | enabled | `--no-test` |
| Polish | disabled | `--polish` |
| Quick mode | disabled | `--quick` (10 chapters) |

---

## Files

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

---

## License

MIT License