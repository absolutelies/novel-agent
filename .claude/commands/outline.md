# /outline - Plot Architecture & Chapter Blueprint

> Design three-act structure and detailed chapter-by-chapter blueprint.

## Usage

```
/outline                              — Generate full plot and blueprint
/outline --plot                       — Only generate plot architecture
/outline --blueprint                  — Only generate chapter blueprint
/outline --revise "<suggestions>"     — Revise based on suggestions
/outline --chapters N                 — Specify total chapters (overrides default)
```

## Dependencies

Requires:
- `memory/core_seed.md`
- `memory/character_dynamics.md`
- `memory/world_building.md`

Run `/idea` and `/worldbuild` first if missing.

## Process

### Plot Architecture Generation

Read all architecture files and generate:
1. Three-act suspense structure:
   - Act 1 (Trigger): anomaly signs, threads, inciting event, wrong choice
   - Act 2 (Confrontation): crossroads, pressure, false victory, soul night
   - Act 3 (Resolution): cost, nested twists, aftermath

2. Turning points (3 per act) with foreshadow mapping

3. Foreshadowing strategy (plant/reinforce/payoff schedule)

Save to `memory/plot_architecture.md`.

### Chapter Blueprint Generation

Read plot architecture and generate chapter blueprint:

**CRITICAL: Generate FULL detailed blueprints for ALL chapters (not just first 3)**

For EACH chapter (from 1 to total_chapters):

1. **TV Drama Structure (explicit beats for each chapter):**
   | Element | Required Content |
   |---------|-----------------|
   | Cold Open | Specific scene, 2-3 example dialogue lines, specific hook |
   | Act 1 | Scene-by-scene beats with specific actions (NOT generic) |
   | Act 2 | Specific complications with specific stakes |
   | Act 3 | Specific midpoint twist/revelation |
   | Act 4 | Specific climax confrontation |
   | Act 5 | Specific resolution aftermath |
   | Tag | Specific closing hook, setup for next chapter |

2. **Per-chapter metadata (≥80 words per chapter):**
   - Positioning in story arc
   - Core purpose (specific, NOT generic)
   - Suspense design (specific tension sources)
   - Foreshadowing operations (plant/reinforce/payoff)
   - Cognitive disruption level (1-5)
   - Characters involved (with specific roles this chapter)
   - Items/props used (specific)
   - Location (specific setting)
   - Chapter summary (specific events, NOT "X discovers truth")

3. **Anti-placeholder enforcement:**
   - NO "[Chapters N-M continue...]" placeholders
   - NO generic summaries like "protagonist investigates"
   - NO repeated structure across chapters
   - Each chapter must have UNIQUE specific content
   - If chapter count > 10, generate in batches but ALL must be explicit

4. **Rhythm curve** ensuring proper pacing across full blueprint

Save to `memory/chapter_blueprint.md`.

**Verification before proceeding:**
- Blueprint must contain explicit beats for chapters 1 through total_chapters
- If ANY chapter lacks detailed beats, REGENERATE before saving

### Update Progress

Update `memory/progress.json`:
- status → BLUEPRINT
- Set total_chapters
- Add history entry

## Output Format

After completion:

```
✓ Plot Architecture Complete
  Acts defined: 3
  Turning points: [count]
  Foreshadow seeds: [count]
  Output: memory/plot_architecture.md
  
✓ Chapter Blueprint Complete
  Chapters planned: {total_chapters}
  Suspense units: [count]
  Output: memory/chapter_blueprint.md
  
Next: Run /write to generate chapter content
```