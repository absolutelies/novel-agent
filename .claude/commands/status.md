# /status - Progress Viewer

> Display current project progress and next steps.

## Usage

```
/status                    — Show full progress summary
/status --brief            — Brief one-line status
/status --history          — Show full history log
/status --files            — List all generated files
/status --next             — Show only next step recommendation
```

## Display

### Full Status

```
=== NOVEL WRITING PROJECT ===

Project ID: {project_id}
Genre: {genre}
Theme: {user_prompt}

=== PROGRESS ===

Status: {status}
Current Chapter: {current}/{total} ({percent}%)
Words Written: {words_written}/{target_words}

=== TIMELINE ===

Created: {created_at}
Last Updated: {last_updated}
Duration: {days} days

=== COMPLETED STAGES ===

{history entries with timestamps}

=== FILES ===

Architecture:
- ✓ core_seed.md ({size})
- ✓ character_dynamics.md ({size})
- ✓ world_building.md ({size})
- ✓ plot_architecture.md ({size})
- ✓ chapter_blueprint.md ({size})

State:
- ✓ character_state.md ({size})
- ✓ global_summary.md ({size})

Chapters:
- Chinese: {count} chapters

=== NEXT STEP ===

{recommended action}

Example: "Run /write to generate chapter 5"
Example: "Project complete! Run /novel-agent --status anytime"
```

### Brief Status

```
[{project_id}] Status: {status} | Chapters: {current}/{total} | Words: {words_written}
```

### Files List

```
Generated Files:

memory/
├── core_seed.md ✓
├── character_dynamics.md ✓
├── world_building.md ✓
├── plot_architecture.md ✓
├── chapter_blueprint.md ✓
├── character_state.md ✓
├── global_summary.md ✓
└── progress.json ✓

output/chapters/
├── chapter_001.md ✓
├── chapter_002.md ✓
└── ...

output/zh-CN/
├── chapter_001.md ✓
├── chapter_002.md ✓
├── ...
└── novel_full_zh.md ✓
```

## State Interpretation

| Status | Meaning | Next Action |
|--------|---------|-------------|
| INIT | Project created | Run `/idea` |
| IDEA | Core seed generated | Run `/worldbuild` |
| CHARACTERS | Characters created | Run `/worldbuild --world` |
| WORLD | World built | Run `/outline` |
| PLOT | Plot designed | Run `/outline --blueprint` |
| BLUEPRINT | Chapters planned | Run `/write` |
| CHAPTERS | Chapters written | Project complete |
| DONE | Finished | No action needed |