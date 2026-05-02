# /outline - Plot Architecture & Chapter Blueprint

> Design three-act structure and detailed chapter-by-chapter blueprint.
> **🔴 CRITICAL: Output MUST be 100% English.** Blueprint is the foundation for Chinese novel generation.

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
- `memory/core_seed.md` (English)
- `memory/character_dynamics.md` (English)
- `memory/world_building.md` (English)

Run `/idea` and `/worldbuild` first if missing.

## 🔴 Language Requirement

**All output files MUST be 100% English:**
- `plot_architecture.md` - English
- `chapter_blueprint.md` - English
- `chapter_blueprint_act1-4.md` - English

**Why English Blueprint?**
- Blueprint is the structural foundation, not the prose output
- Writer agent reads English Blueprint → writes Chinese novel
- Language separation ensures structural clarity vs prose creativity

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

5. **🔴 Opening Type Rotation (防开头模板化)**

   **问题**: 连续章节使用相同开头结构（如"角色+屏幕+数据"）导致机械感
   **解决**: 强制每章开头类型轮换，确保多样化

   **开头类型库（必须轮换使用）：**

   | 类型 | 示例结构 | 适用场景 |
   |------|---------|----------|
   | **感官切入** | 声音/气味/触觉开头，无角色在场 | 悬念、氛围营造 |
   | **对话切入** | 直接对话开头，无铺垫 | 张力场景、冲突 |
   | **动作切入** | 角色正在做某事，无心理描写 | 紧急场景、转折 |
   | **悬念切入** | 问题/谜团开头，无解答 | 神秘、发现 |
   | **环境切入** | 地点描写开头，无角色 | 氛围、时空转换 |
   | **回忆切入** | 闪回开头，连接过去 | 背景、动机揭示 |

   **轮换规则：**
   - 相同开头类型连续使用 ≤ 2章
   - 每5章必须包含 ≥ 3种不同开头类型
   - Cold Open必须标注开头类型（供Writer参考）

   **Blueprint格式更新：**
   ```
   | Element | Specific Content |
   | Cold Open | [开头类型: 悬念切入] + [具体场景] |
   ```

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