# /worldbuild - World & Character Creation

> Build comprehensive world and character system from core seed.

## Usage

```
/worldbuild                          — Generate full world and characters
/worldbuild --characters             — Only generate/update characters
/worldbuild --world                  — Only generate/update world
/worldbuild --revise "<suggestions>" — Revise based on suggestions
```

## Dependencies

Requires `memory/core_seed.md` to exist. Run `/idea` first if missing.

## Process

### Characters Generation

Read `memory/core_seed.md` and generate:
1. Character profiles (5-10 core characters)
2. Each with:
   - Background, appearance, role
   - Core drive triangle (surface/deep/soul)
   - **Language profile** (speaking style, word choice, emotional expression)
   - Character arc design
   - Relationship conflict web

3. Initial character states for each

Save to:
- `memory/character_dynamics.md`
- `memory/character_state.md`

### World Building Generation

Read `core_seed.md` and `character_dynamics.md`, generate:
1. Three-dimensional world matrix:
   - Physical: space, timeline, rules
   - Social: power structure, taboos, economics
   - Metaphorical: symbols, environment-psychology

2. With conflict potentials and character connections

Save to `memory/world_building.md`.

### Update Progress

Update `memory/progress.json`:
- status → WORLD (if --world only)
- status → CHARACTERS → WORLD (if full)
- Add history entry

## Output Format

After completion, show summary:

```
✓ Character Dynamics Complete
  Characters created: [count]
  Output: memory/character_dynamics.md
  
✓ World Building Complete
  Locations defined: [count]
  Power structures: [count]
  Output: memory/world_building.md
  
Next: Run /outline to generate plot architecture
```