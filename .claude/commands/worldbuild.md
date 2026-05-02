# /worldbuild - World & Character Creation

> Build comprehensive world and character system from core seed.
> **CRITICAL**: Generate fixed prose_style.md to prevent style feedback loops.

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

### 🔴 CRITICAL: Prose Style Definition (防风格正反馈)

**问题根源**: WRITER agent读取前一章摘要时会继承风格特征，导致风格逐章放大（如"来自"链式结构）。
**解决**: 在WORLD阶段生成固定的 `prose_style.md`，所有章节统一参考此文件。

**生成 prose_style.md 内容：**

```markdown
# 写作风格规范（固定参考，所有章节统一使用）

## 基调（从core_seed.md Genre提取）

[Genre对应的风格基调，例如：]
- Hard Sci-Fi/Thriller: 克制冷峻、白描为主、对话简短有力、心理融入动作
- 参考作品：麦家《风声》、双雪涛《飞行家》

## 句式结构规则（强制执行）

### ✅ 正确句式模式

1. **长短交替**: 短句（10-20%）+ 中句（40-50%）+ 长句（30-40%）
   - 示例：`他走进来，脚步平稳，但带着某种陌生的迟疑——眼睛是银色的，和庇护所中那些古老画像一模一样。`

2. **复合句优先**: 使用逗号连接子句，避免连续独立短句
   - 示例：`波形在眼前重新排列，数值的变动暗示某种新模式正在形成。`

3. **感官融入动作**: 不用"看见/感到"，直接描写现象
   - 示例：`警报的红光映在咖啡杯边缘，倒计时在无声中下降。`

### 🔴 禁止句式模式

1. **链式推导结构**: 连续使用"X来自Y。Y来自Z。"句式
   - 🔴 FORBIDDEN: `机会来自塑造碰撞。塑造来自林昭计算。计算来自轨道力学。`
   - ✅ CORRECT: `塑造碰撞的机会源于林昭的轨道力学计算——一种牺牲商业保留轨道生存的方案。`

2. **精度描述链**: 连续使用"数值来自/数值显示"句式
   - 🔴 FORBIDDEN: `数值来自追踪数据。数据的数值显示轨道高度七百五十公里。`
   - ✅ CORRECT: `追踪数据显示轨道高度约750公里，数值来自ISTMO实时更新。`

3. **连续短句（铁律八）**: 连续≤15字符短句超过2个
   - 🔴 FORBIDDEN: `韦伯沉默。沉默来自接受。接受来自价值超过损失。`
   - ✅ CORRECT: `韦伯沉默，接受了轨道价值超过商业损失的计算结果。`

4. **重复结构开头**: 同一段落中连续3+句使用相同开头词
   - 🔴 FORBIDDEN: `物体的数值来自...传播的碎片来自...生成的碎片数量来自...`
   - ✅ CORRECT: 使用不同的开头词：数值、碎片、数量、轨道、碰撞...

## 对话风格（从character_dynamics.md提取）

[每个主要角色的对话特征，例如：]
- 林昭: 技术语言为主，句子简短，情感压抑在动作中
- 韦伯: 商业思维，直接质问，数据驱动
- 帕特尔: 学术语态，理论化表达，谨慎推测

## 情绪表达规则

- **禁止直接情绪词**: 很恐惧/很愤怒/很悲伤
- **融入动作**: 情绪通过微动作表达（攥拳、别过脸、指尖敲桌）
- **融入环境**: 情绪通过环境映射（警报红光、冷掉的咖啡、沉默的会议室）

## 章节末尾规则

**章节末尾不得使用链式总结结构。**
- 🔴 FORBIDDEN: 末尾20+行使用"X来自Y"链式句式
- ✅ CORRECT: 使用复合句、场景描写、悬念钩子结束

## 验证方法

每章完成后检查：
- "来自"出现次数 ≤ 5次/章（链式结构检测）
- "数值"开头连续 ≤ 2次
- 连续短句 ≤ 2个
```

Save to `memory/prose_style.md`.

**WHY THIS MATTERS:**
- 固定风格文件打破正反馈循环
- WRITER读取prose_style.md而非前一章摘要的风格特征
- 所有章节使用统一的句式规则

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
  
✓ Prose Style Defined
  Output: memory/prose_style.md
  🔴 CRITICAL: All chapters will reference this fixed style
  
Next: Run /outline to generate plot architecture
```