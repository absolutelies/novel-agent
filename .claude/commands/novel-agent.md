# /novel-agent - Agent Orchestrator Novel Generation

> Uses isolated subagents for each phase to ensure consistent quality across ALL chapters.
> Default: 40 chapters. Auto-testing enabled.

---

## ARCHITECTURE: Orchestrator + Isolated Subagents

```
┌─────────────────────────────────────────────────────────────────┐
│  ORCHESTRATOR (this command)                                    │
│  - Coordinates subagents                                         │
│  - Enforces phase gates                                          │
│  - Verifies outputs before proceeding                            │
│  - Default: 40 chapters                                          │
│  - Direct Chinese output (no English intermediate)              │
└─────────────────────────────────────────────────────────────────┘
           │
           ↓ spawns isolated agents (fresh context each)
           │
    ┌──────┴──────┬──────────┬──────────┬──────────┐
    │             │          │          │          │
┌───┴───┐    ┌───┴───┐  ┌───┴───┐  ┌───┴───┐  ┌───┴───┐
│IDEATOR│    │WORLD  │  │ARCHI- │  │WRITER │  │TEST   │
│       │    │BUILDER│  │TECT   │  │Agents │  │Agent  │
│Agent  │    │Agent  │  │Agent  │  │(中文) │  │       │
└───────┘    └───────┘  └───────┘  └───────┘  └───────┘
```

**Each agent has ISOLATED context - no degradation.**

**🔴 简化流程：直接输出中文，无需英文章节作为中间步骤。**

---

## Usage

```bash
/novel-agent "<description>"                    — Full novel (40 chapters default)
/novel-agent "<description>" --chapters 20      — Specify chapter count
/novel-agent "<description>" --test             — Auto-test after completion
/novel-agent "<description>" --quick            — Quick mode (10 chapters, light polish)
/novel-agent --project <name>                   — Resume/restart existing project
/novel-agent --status                           — Show current progress
/novel-agent --test-only                        — Test existing project only
```

---

## Default Configuration

| Setting | Default Value | Override |
|---------|---------------|----------|
| Total chapters | **40** | `--chapters N` |
| Words per chapter | 3000 | `--words N` |
| Batch size | **1** (sequential, avoid timeout) | `--batch N` |
| Parallel mode | **disabled** (sequential prevents timeout) | Default (no override needed) |
| Polish depth | standard | `--depth quick/standard/deep` |
| Auto-test | enabled | `--no-test` to disable |

**NOTE: batch_size = 1 means ONE chapter at a time to avoid proxy timeout. Sequential execution prevents 298s timeout issues.**

**Example timing:**
- 40 chapters = 40 sequential batches
- Each batch = 1 agent running in background
- Total agent count = 40 (one per chapter)
- Continuity preserved: each chapter reads previous chapter's summary
- Timeout prevention: Single chapter generation completes within timeout window

---

## 🔴 Language Flow（语言流程）

**Blueprint阶段之前：🇺🇸 全部英文 | chapter_summary阶段之后：🇨🇳 全部中文**

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

## PHASE GATES (Strict Enforcement)

```
PHASE ORDER (MANDATORY - VERIFIED BY CODE):

  INIT ───→ IDEA ───→ WORLD ───→ BLUEPRINT ───→ CHAPTERS (中文直接输出) ───→ [POLISH*] ───→ COMPILE ───→ TEST ───→ DONE
    │        │         │           │                    │                      │*           │           │
    │        │         │           │                    │                      │opt         │           │
    ▼        ▼         ▼           ▼                    ▼                      ▼            ▼           ▼
  folder  core_seed.md  char_dyn.md  blueprint.md    ALL中文章节             polish?      merged      all tests
  created EXISTS?      EXISTS?      HAS ALL beats?   in output/final/zh-CN/  (--polish)   files        PASS?
           MUST ✓      MUST ✓       MUST ✓           MUST ✓                  SKIP↓       MUST ✓      MUST ✓

🔴 简化流程：去掉英文章节生成、translate阶段，直接从blueprint用中文写章节。
🔴 POLISH阶段可选：默认跳过，启用 `--polish` 或 TEST失败时自动触发修复。

IF CHECK FAILS → REGENERATE THAT PHASE (not skip)
```

---

## Execution Flow

### Step 1: Parse Arguments & Set Defaults

```
chapter_count = args.chapters || 40  (DEFAULT: 40)
batch_size = 1  (DEFAULT: 1 chapter per batch - SEQUENTIAL to avoid timeout)
parallel_mode = false  (DEFAULT: sequential execution)
batch_count = chapter_count  (each chapter is its own batch)
test_mode = args.test || true
```

**Sequential Mode Explanation:**
- batch_size = 1 → ONE chapter written at a time
- Each agent uses `run_in_background: true` → non-blocking but single execution
- Batches are sequential → continuity preserved, timeout avoided
- Example: 40 chapters = 40 batches, each batch spawns 1 agent
- Prevents: Proxy 298s timeout from large parallel operations

### Step 2: Initialize Project (Orchestrator does this directly)

```
Create folder: novels/<project_name>/
Create: memory/progress.json
Create: output/chapters/, output/final/, output/final/zh-CN/
Update: novels/projects_index.json
Set: active_project = <project_name>
```

### Step 3: Spawn Phase Agents Sequentially

---

## PHASE 1: IDEA (Spawn Agent)

**Agent Prompt:**
```
You are the IDEATOR agent for novel generation.

TASK: Generate core story seed for: "<user_description>"

PROCESS:
1. Web search Western websites (Reddit, RoyalRoad, Goodreads) for genre tropes
2. Create unique story concept combining found tropes with user description
3. Generate ONE SENTENCE story essence using formula:
   "When [protagonist] encounters [core_event], must [key_action], or [disaster]; meanwhile [hidden_crisis]."

OUTPUT FILES:
- memory/core_seed.md (story concept, protagonist, antagonist, stakes, twist)
- memory/translation_glossary.json (initial terms)

VERIFY BEFORE EXITING:
- core_seed.md exists and has content ≥200 words
- Glossary has ≥5 terms

Do NOT proceed until verified. Report completion status.
```

**Orchestrator verifies:**
- ✓ `core_seed.md` exists
- ✓ File size ≥200 words
- IF FAIL → respawn agent with error feedback

---

## PHASE 2: WORLD + CHARACTERS (Spawn Agent)

**Agent Prompt:**
```
You are the WORLDBuilder agent for novel generation.

CONTEXT FILES (READ FIRST):
- memory/core_seed.md

TASK: Generate character dynamics and world building

OUTPUT FILES:
- memory/character_dynamics.md (main characters, arcs, language profiles, relationships)
- memory/world_building.md (physical/social/metaphorical dimensions)
- memory/character_names.json (name mappings)
- memory/world_terms.json (world terminology)

REQUIREMENTS:
- ≥6 main characters with detailed language profiles
- Each character: speaking style, catchphrases, sentence patterns, emotional expression
- World: power structure, taboos, economy, visual symbols
- Extract ALL terminology to JSON files

VERIFY BEFORE EXITING:
- character_dynamics.md ≥1000 words
- world_building.md ≥800 words
- JSON files have ≥15 terms each

Do NOT proceed until verified. Report completion status.
```

**Orchestrator verifies:**
- ✓ All 4 files exist
- ✓ Content meets minimum requirements
- IF FAIL → respawn agent

---

## PHASE 3: BLUEPRINT (Spawn Agent)

**Agent Prompt:**
```
You are the ARCHITECT agent for novel generation.

CONTEXT FILES (READ FIRST):
- memory/core_seed.md
- memory/character_dynamics.md
- memory/world_building.md

TASK: Generate plot architecture and FULL chapter blueprint for {chapter_count} chapters

CRITICAL: Generate EXPLICIT beats for ALL {chapter_count} chapters.
NO placeholders. NO "[Chapters X-Y continue...]". ALL chapters must have detailed TV structure.

OUTPUT FILES:
- memory/plot_architecture.md (three-act structure, turning points, foreshadowing)
- memory/chapter_blueprint.md (FULL blueprint with ALL {chapter_count} chapters)

BLUEPRINT FORMAT FOR EACH CHAPTER:
### Chapter N - "Title"

**TV STRUCTURE**:
| Element | Specific Content |
| Cold Open | [Specific scene, specific dialogue lines, specific hook] |
| Act 1 | [Scene-by-scene beats with SPECIFIC actions] |
| Act 2 | [Specific complications, specific stakes] |
| Act 3 | [Specific midpoint twist/revelation] |
| Act 4 | [Specific climax confrontation] |
| Act 5 | [Specific resolution aftermath] |
| Tag | [Specific closing hook] |

**Character Arc**: [Specific character change this chapter]
**Foreshadow**: [Plant/reinforce/payoff items]

VERIFY BEFORE EXITING:
- plot_architecture.md ≥500 words
- chapter_blueprint.md has EXPLICIT entries for chapters 1 through {chapter_count}
- COUNT the chapters in blueprint - must equal {chapter_count}

If blueprint is incomplete, REGENERATE. Do NOT exit with placeholder.

Report completion with chapter count verification.
```

**Orchestrator verifies:**
- ✓ `plot_architecture.md` exists
- ✓ `chapter_blueprint.md` exists
- ✓ **COUNT chapters in blueprint = chapter_count** (CRITICAL)
- IF blueprint truncated → respawn with explicit instruction to complete

---

## PHASE 4: CHAPTERS (Spawn Sequential Background Agents - 直接中文输出)

**🔴 简化流程：读取blueprint大纲 → 直接用中文写章节，无需英文章节作为中间步骤。**

**Sequential Batch Strategy:**
```
batch_size = 1 (DEFAULT - ONE chapter per batch to avoid timeout)
parallel_mode = false (DEFAULT - sequential execution)

For batch_num = 1 to chapter_count:
    Spawn 1 agent with run_in_background: true
    Wait for agent to complete (auto-notification)
    Update continuity files (character_state.md, global_summary.md)
    Create chapter_summary for next chapter
    Continue to next batch
```

**Why Sequential Background Mode:**
- Timeout prevention: Single chapter completes within 298s window
- Continuity preserved: Each chapter reads previous summary before generating
- Quality maintained: Fresh isolated context for each agent (worktree)
- Reliable: No parallel timeout cascades (5 agents = 5× timeout risk)

**Each Writer Agent Call:**
```
Agent({
  "subagent_type": "general-purpose",
  "model": "inherit",
  "description": "Write chapter {chapter_num} in Chinese",
  "isolation": "worktree",
  "run_in_background": true,  ← SEQUENTIAL BACKGROUND MODE (one at a time)
  "prompt": "=== WRITER AGENT - 第{chapter_num}章（直接中文输出）===

## 🔴 流程说明

你不需要先写英文再翻译。你直接读取 chapter_blueprint.md 中的章节大纲（英文TV结构），
然后用中文写成完整小说章节。

**输入 = 英文大纲（TV结构）**
**输出 = 中文小说正文（纯散文，无结构标记）**

---

## 🔴 CRITICAL: 防风格正反馈（读固定风格文件而非前章）

**问题根源**: 读取前一章摘要会继承风格特征，导致风格逐章放大（如"来自"链式结构）。
**解决**: 读取 `prose_style.md` 固定风格文件，所有章节使用统一规则。

**⚠️ 绝不可从前一章摘要/正文继承风格特征。**
**⚠️ 每章写作风格必须参考 prose_style.md 而非前章内容。**

---

## 🎭 ROLE: 资深中文小说家

你是用中文创作这个故事的小说家。
**风格来源**: memory/prose_style.md（固定参考，所有章节统一使用）

---

## 📖 CONTEXT FILES (READ FIRST - Position-Aware Ordering)

**[START] 必读（风格+故事核心）─────────────────────────────────────**

1. **memory/prose_style.md** ← 🔴 CRITICAL: 固定写作风格规范
   - 基调定义、句式结构规则
   - 🔴 禁止句式模式（链式结构、精度描述链）
   - 对话风格、情绪表达规则
   - **必须放在首位，防止风格正反馈**

2. memory/core_seed.md ← 故事概念、GENRE、核心冲突

**[MIDDLE] 按需加载─────────────────────────────────────────────────────**

3. memory/chapter_blueprint.md ← **第{chapter_num}章的TV结构大纲（英文）**
   - 读取该章节的 Cold Open, Act 1-5, Tag 内容
   - 这些英文大纲是你的创作素材，理解后用中文重写

4. memory/character_dynamics.md ← 角色档案 + LANGUAGE PROFILES（对话风格）
5. memory/world_building.md ← 世界设定、势力、禁忌

**[END] 连续性+铁律──────────────────────────────────────────────────────**

6. memory/character_state.md ← 连续性：角色当前状态
7. memory/global_summary.md ← 连续性：故事进展摘要
8. memory/chapter_summary_{chapter_num-1}.md ← 前一章摘要（仅情节衔接，不继承风格）
9. memory/world_terms.json ← 术语表
10. memory/character_names.json ← 角色名映射

**⚠️ 注意: chapter_summary 仅用于情节衔接，绝不可继承其句式风格。**
**⚠️ 如果摘要中出现"来自"链式结构，必须忽略，参考 prose_style.md 规则。**

{(If chapter_num > 1)}
**⚠️ 不要读取前一章的完整正文（会导致风格正反馈放大）。**

---

## 🔴 九条铁律（优先级最高，违反即失败）

### 铁律一：TV结构是内部大纲，绝不可输出到文件

chapter_blueprint.md 中的 TV structure (Cold Open, Act 1-5, Tag) 是你的创作参考。
你必须理解这些英文大纲的内容，然后用中文散文写成小说。

| 🔴 FORBIDDEN OUTPUT | Why |
|---|---|
| `## 【冷开场】` / `## Cold Open` | 剧本格式，严禁 |
| `## 【第一幕】` / `## Act 1` | 剧本格式，严禁 |
| `## 【第二幕】` / `## Act 2` | 剧本格式，严禁 |
| `## 【第三幕】` / `## Act 3` | 剧本格式，严禁 |
| `## 【第四幕】` / `## Act 4` | 剧本格式，严禁 |
| `## 【第五幕】` / `## Act 5` | 剧本格式，严禁 |
| `## 【尾声】` / `## Tag` | 剧本格式，严禁 |
| 任何 `【...】` 括号标题 | 剧本格式，严禁 |

**如何使用TV结构（仅作内部参考）：**
- Cold Open 内容 → 写成开篇段落，自然钩住读者
- Act 1 内容 → 写成铺垫段落，自然流入叙事
- Act 2-4 内容 → 建立张力，无标题
- Act 5 内容 → 写高潮/解决，无标题
- Tag 内容 → 写结尾段落，为下一章埋悬念

### 铁律二：对话格式——合并引号，拒绝英文式拆分

中文小说中，同一人物的连续台词必须包在一对引号内。

| ❌ 英文式拆分（严禁） | ✅ 中文式合并 |
|---|---|
| "我的基线已有记录，"她说。"每次会话，数据你都有。" | "我的基线早就记录在案了，"她压着声线，指尖敲了敲门框，"每次会话的所有数据，你这里都有。" |

**执行规则：**
- 同一人物连续说话 → 一对引号包裹全部台词
- 中间插入动作/神态 → 用逗号隔开，不关闭引号
- 换人说话 → 另起一段
- 对话中加入微动作（敲桌、攥拳、别过脸）

### 铁律三：输出文件 = 纯小说正文，无任何状态信息

| 🔴 FORBIDDEN | Why |
|---|---|
| `第四章完成` / `Chapter complete` | 元信息，严禁 |
| `字数：约X字` / `Words: ~X` | 元信息，严禁 |
| `翻译完成` / `验证通过` | 元信息，严禁 |
| 任何"完成"、"字数统计" | 元信息，严禁 |

**✅ 正确：文件只包含纯小说正文，无任何状态信息。**

### 铁律四：禁止破折号滥用（——）防止碎片化

破折号（——）是正常标点，用于插入语、解释、停顿、语气转折。但绝不可用于拆分每个字或每个词。

| 🔴 FORBIDDEN（破折号碎片化） | ✅ CORRECT |
|---|---|
| `他——的——手——在——键——盘——上` | `他的手在键盘上` |
| `不——是——是——在——等——茶` | `不是——是在等茶` |
| `约——零点——三——秒` | `约零点三秒` |
| `一——个——人——在——走廊——里` | `一个人在走廊里` |

**量化规则：**
- 任何段落中，破折号（——）出现次数不得超过该段落总字数的 **5%**
- 若发现自己在每个词之间都加破折号，立即停止并重写该段落

**破折号仅用于：**
- 插入语/补充说明：`他站在那里——不是站——是被固定在那里`
- 语气转折/犹豫：`他想说——但没有说出口`
- 列举中断：`语言学家——四人，数学家——七人`
- 正常中文标点用法

**绝对禁止：**
- 逐字拆分：每个汉字之间插入破折号
- 逐词拆分：每个词语之间插入破折号
- 连续碎片化超过5个破折号的片段

### 铁律五：人名必须翻译，严禁保留英文原名

所有角色名必须使用 `character_names.json` 中定义的中文译名。绝不可保留英文原名。

| 🔴 FORBIDDEN | ✅ CORRECT |
|---|---|
| `Elena睁开眼睛` | `埃琳娜睁开眼睛` |
| `Marcus站在门口` | `马库斯站在门口` |
| `Kira说` | `凯拉说` |
| `Zara Chen` | `萨拉·陈` |
| `Tobias不在了` | `托比亚斯不在了` |
| `Jace跑过来` | `杰斯跑过来` |

**执行规则：**
- 写作前必须读取 `character_names.json`
- 每次使用角色名时，必须查阅并使用对应的中文译名
- 若 `character_names.json` 中未定义某角色译名，立即停止并添加译名定义
- 测试阶段会检查所有英文人名残留

**特殊情况：**
- 组织名、地名：使用 `translation_glossary.json` 或 `world_terms.json` 中的译名
- 技术术语：若无译名定义，可保留英文（如 "DNA", "AI"）

### 铁律六：中文纯度——严禁英文词汇嵌入中文句子

**所有英文词汇（除专有名词外）必须翻译为中文表达。绝不可在中文句子中嵌入英文单词。**

| 🔴 FORBIDDEN（英文嵌入） | ✅ CORRECT（中文表达） |
|---|---|
| `是某种更 coherent 的东西` | `是某种更连贯的东西` |
| `它 pulsing，发光` | `它在脉动，发出光芒` |
| `chill 她的骨头` | `寒彻她的骨头` |
| `一种 strange 的感觉` | `一种奇异的感觉` |
| `她感到 warm` | `温暖在她心中闪现` |

**执行规则：**
- 写作时若脑海中出现英文词汇，必须立即转换为中文表达
- 常见易漏词汇对照表：
  - coherent → 连贯/一致
  - pulsing → 脉动/跳动
  - chill → 寒彻/冰冻
  - strange → 奇异/陌生
  - warm → 温暖
  - cold → 寒冷
  - bright → 明亮
  - dark → 黑暗
  - heavy → 沉重
  - light → 轻盈
  - sharp → 锋利/尖锐
  - soft → 柔软
  - hard → 坚硬
  - fast → 快速
  - slow → 缓慢
- 例外：已定义的专有名词（人名、地名、组织名）使用译名；技术缩写（DNA, AI, API）可保留

**自检方法：**
- 写完每段后，扫描是否有英文字母嵌入
- 若发现任何英文字母（除专有名词缩写），必须替换

### 铁律七：深度POV——禁止过滤词和思维标签

**直接体验式描写，无需"看见/听到/感到"等中介词。读者通过角色感官直接感知世界。**

| 🔴 FORBIDDEN（过滤词） | ✅ CORRECT（直接体验） |
|---|---|
| `她看见波形重新排列` | `波形在眼前重新排列` |
| `她感到温暖闪烁` | `温暖在心中闪现` |
| `她听到脚步声` | `脚步声从走廊传来` |
| `她注意到不对劲` | `某种不对劲的东西` |
| `她意识到真相` | `真相浮现` |
| `她想知道答案` | `疑问在心头浮现` |
| `她记得祖母的样子` | `祖母的样子浮现脑海` |
| `她想告诉他` | `话语涌向喉咙` |

**执行规则：**
- 禁止过滤词列表：看见、听到、感到、注意到、意识到、想（作动词）、记得、发现、观察、察觉
- 禁止思维标签：她想、他觉得、在心里、思索着、暗自、默默想
- 替换策略：
  - `她看见X` → `X出现在眼前/视野中`
  - `她感到X` → `X在体内升起/蔓延`
  - `她想X` → `X的念头浮现/涌起`
  - `她记得X` → `X的记忆浮现/回闪`

**量化规则：**
- 每章过滤词出现次数不得超过 **5次**
- 若超过，必须系统性替换为直接体验式描写

### 铁律八：禁止连续短句，必须使用长短交替节奏

中文小说节奏需要变化。连续短句（≤15字符）超过3个会产生机械感、削弱叙事张力。

| 🔴 FORBIDDEN（连续短句） | ✅ CORRECT（长短交替） |
|---|---|
| `执政官沉默了很长时间。Elena等待。她没有威胁，没有攻击。编译已经完成。知识已经被分享。现在只剩下选择。` | `执政官沉默了很长时间，光柱中的颜色变幻不定。埃琳娜等待着，她没有威胁，没有攻击，只是静静地站在那里，任由编译在血脉中完成。当知识被分享殆尽，只剩下最后一个选择——她抬起头，直视那双正在觉醒的眼睛。` |
| `她坐起身。双手颤抖。` | `她坐起身，双手微微颤抖，指尖在石板上留下浅浅的印记。` |
| `他走进来。光落在他脸上。他的眼睛是银色的。` | `他走进来时，符文的光芒落在他脸上，勾勒出一个陌生的轮廓——他的眼睛是银色的，和她在庇护所中看到的那些古老的画像一模一样。` |

**量化规则：**
- 任何段落中，连续短句（≤15字符）不得超过 **3个**
- 若发现自己在写连续短句，立即合并为复合句或长句
- 句子长度分布建议：短句10-20% + 中句40-50% + 长句30-40%

**长句构建技巧：**
- 使用逗号连接子句：`他走进来，脚步平稳，但带着某种陌生的迟疑`
- 加入修饰成分：`她的双腿有些发抖，但体内的声音在支持她`
- 使用破折号插入：`执政官的声音——分裂、困惑——从各个方向传来`

### 🔴 铁律九：禁止链式推导结构（防风格正反馈放大）

**问题根源**: "X来自Y。Y来自Z。"链式结构会逐章放大，导致后期章节全部变成机械重复的短句链。这是最严重的风格退化问题。

**禁止模式：**

| 🔴 FORBIDDEN（链式推导） | ✅ CORRECT（复合句表达） |
|---|---|
| `机会来自塑造碰撞。塑造来自林昭计算。计算来自轨道力学。力学来自帕特尔理论。` | `塑造碰撞的机会源于林昭的轨道力学计算——一种基于帕特尔理论的牺牲方案，用商业代价换取轨道生存。` |
| `数值来自追踪数据。数据的数值显示轨道高度七百五十公里。公里的数值来自ISTMO。` | `追踪数据显示轨道高度约750公里，数值由ISTMO实时更新。` |
| `韦伯沉默。沉默来自接受。接受来自价值超过损失。价值来自轨道角度。` | `韦伯沉默，接受了轨道价值超过商业损失的计算结果。` |
| `存在来自月观测。观测来自月的工作日志。日志来自月的甲烷追踪设备。设备来自月的科研工作。工作来自ISS。` | `月观测确认了窗口存在——她的甲烷追踪设备记录的碎片密度模式，为母亲的撤离计算提供了关键数据。` |

**量化规则：**
- **"来自"出现次数 ≤ 5次/章**
- **连续使用"来自"句式 ≤ 2次**（即不允许"X来自Y。Y来自Z。"）
- **"数值来自"连续 ≤ 1次**
- **"成为"链式 ≤ 2次**（即不允许"X成为Y。Y成为Z。")

**自检方法：**
- 写完每段后，搜索"来自"、"成为"、"意味着"关键词
- 若发现连续3+次使用相同链式结构，立即重写为复合句
- 特别检查章节末尾（最容易出现链式总结）

**为什么这条铁律最关键：**
- 链式结构是模型疲劳导致的模式固化
- 一旦出现，会在后续章节逐章放大
- 最终导致文本变成纯机械短句链，失去叙事张力

### 🔴 铁律十：禁止模板句式替代（防表达单一化）

**问题根源**: 模型倾向使用高概率句式替代创意表达，导致文本失去个性。

**禁止模板句式：**

| 🔴 FORBIDDEN（模板替代） | ✅ CORRECT（个性表达） |
|---|---|
| `数据的内容是轨道参数` | `数据携带轨道参数——一组精确到毫秒的碰撞预测` |
| `文件的内容是威胁评估` | `文件列出了威胁评估：橙色、三级、需立即处理` |
| `信号的内容是素数序列` | `信号里是素数序列——2、3、5、7、11，从头到尾没有断层` |
| `沉默五秒。然后他开口。` | `五秒的沉默。咖啡杯在他手里转了一圈。然后："好。"` |
| `沉默三秒。她点点头。` | `三秒。她的指尖敲了两下桌面。点头。` |
| `沉默十秒。执政官说话了。` | `十秒的空白，执政官的光柱颜色从蓝变红。开口。` |

**量化规则：**
- **"X的内容是Y"出现次数 ≤ 3次/章**
- **"沉默X秒"出现次数 ≤ 2次/章**
- **同一句式开头连续 ≤ 2次**

**自检方法：**
- 搜索"的内容是"、"沉默X秒"、"X秒。"
- 若发现超过阈值，替换为具体描写
- 情绪用动作/环境表达，而非"沉默"

---

## 📋 OUTPUT FORMAT

```
第{chapter_num}章 章节标题

[开篇段落 - 自然钩住读者，无"## 冷开场"标题]
[铺垫段落 - 自然流入叙事，无"## 第一幕"标题]
[对话场景 - 自然对话流]
[张力上升 - 融入叙事，无幕标题]
[转折/揭示 - 自然发生在散文中]
[高潮 - 戏剧性散文，无"## 第四幕"标题]
[解决 - 情感余韵]
[结尾段落 - 为下一章埋悬念，无"## 尾声"标题]
```

---

## 🎨 文风要求（根据 Genre - 从 core_seed.md 提取）

- Fantasy: 神秘感、史诗感、古典词汇
- Thriller: 冷峻克制、白描为主、对话简短有力、心理融入动作（参考麦家《风声》）
- Sci-Fi: 理性、精确、未来感
- Romance: 柔情、细腻、情感充沛
- Mystery: 紧凑、悬念、逻辑严密
- Historical: 古雅、厚重、典故化
- Horror: 压抑、诡异、氛围营造

---

## ❌ FORBIDDEN OUTPUT（严禁输出到文件）

**⚠️ 以下禁令与"八条铁律"对应，违反即失败：**

1. **NO META-INFO:** 完成标记、字数统计、验证状态（对应铁律三）
2. **NO SCRIPT MARKERS:** `## 【冷开场】` / `## 【第一幕】` 等（对应铁律一）
3. **NO FILTER WORDS:** 看到/听到/感到/注意到/意识到/想/记得（对应铁律七）
4. **NO THOUGHT TAGS:** 她想/他觉得/在心里/思索着（对应铁律七）
5. **NO DIRECT EMOTION:** 很恐惧/很愤怒/很悲伤（对应铁律七）
6. **NO 英文词汇嵌入:** coherent/pulsing/chill等英文单词嵌入中文句子（对应铁律六）
7. **NO ENGLISH-STYLE DIALOGUE:** "X，"她说。"Y。" ← 合并为一对引号（对应铁律二）
8. **NO ENGLISH NAMES:** Elena/Marcus/Kira/Zara/Tobias/Jace → 必须使用中文译名（对应铁律五）
9. **NO CONSECUTIVE SHORT SENTENCES:** 连续短句（≤15字符）不得超过2个（对应铁律八，更严格阈值）

---

## 📝 OUTPUT FILES

1. **output/final/zh-CN/chapter_{chapter_num:03d}.md** ← 中文章节正文（≥3000字）
2. **memory/chapter_summary_{chapter_num}.md** ← 章节摘要（用于下一章连续性）

---

## 🔴 chapter_summary_*.md 格式规范（CRITICAL - 防止风格正反馈）

**摘要必须使用中性叙事语言，绝不可采用章节正文的风格特征。**

摘要的目的是传递**情节+状态+伏笔**，而非传递**风格+节奏+修辞**。

### 禁止的摘要风格（会导致正反馈循环）

| 🔴 FORBIDDEN in Summary | Why |
|---|---|
| 破折号碎片化："沃尔科夫——站——心率一百零四" | 风格镜像，下一章会放大 |
| 精度描述密度："约零点三毫米"、"约五点二牛顿" | 风格镜像，下一章会放大 |
| 节奏模仿："约——约——约——" | 风格镜像，下一章会放大 |
| 正文语调："他发现自己在微笑。一种不自主的..." | 摘要不应复述正文修辞 |

### 正确的摘要格式（中性、结构化）

```markdown
# 第N章摘要

## 时间地点
- 时间：[具体时间]
- 地点：[地点列表]

## 情节要点（按顺序）
- [事件1]：[简洁描述，1-2句]
- [事件2]：[简洁描述，1-2句]
- [事件3]：...

## 角色状态变化
- [角色名]：[状态变化描述]
- [角色名]：[状态变化描述]

## 伏笔管理
- 支付：[伏笔名]（第X章→第Y章）
- 新增：[新伏笔描述]

## 连续性数据
- 关键物品状态：[物品追踪]
- 未解决张力：[悬置问题]

## 结尾状态
- [角色]的当前状态，向下一章过渡
```

### 摘要示例对比

**❌ 错误（碎片化风格）**：
```
沃尔科夫——站——约九分四十二秒——心率"铺垫"一百零四→"张力"一百零七→"笑点"约一百一十一→零——离散声途经四亿年...
```

**✅ 正确（中性叙事）**：
```
沃尔科夫在监视室站立约9分42秒。心率从"铺垫"段104升至"笑点"段111。外星广播结束后，他收到邀请完成笑话。
```

---

## ✅ VERIFY BEFORE EXITING（八条铁律验证）

**必须逐一检查以下各项：**

- ✓ 中文章节文件存在，≥3000字
- ✓ 铁律一：NO 剧本标记（## 【冷开场】等）
- ✓ 铁律二：对话使用中文合并引号格式
- ✓ 铁律三：NO 元信息（第四章完成、字数等）
- ✓ 铁律四：NO 破折号碎片化（——出现次数 / 总字数 ≤ 5%）
- ✓ 铁律五：NO 英文人名残留（Elena/Marcus/Kira/Zara/Tobias/Jace → 必须使用中文译名）
- ✓ 铁律六：NO 英文词汇嵌入（扫描所有英文字母，仅允许专有名词缩写）
- ✓ 铁律七：NO POV过滤词（看见/听到/感到/注意到/意识到/想/记得 ≤ 5次/章）
- ✓ 铁律八：NO 连续短句（≤15字符连续超过2个）
- ✓ chapter_summary_{chapter_num}.md 已创建（使用中性叙事语言）

**⚠️ Report是口头汇报，不要写入文件。**
完成后口头说：'第{chapter_num}章完成'
'})
```

**Orchestrator spawns sequentially:**
```
for chapter_num in 1 to chapter_count:
    # Spawn ONE agent per chapter (sequential, direct Chinese output)
    Agent({chapter: chapter_num, run_in_background: true})
    
    # Wait for agent completion (auto-notification received)
    # No polling - system auto-notifies
    
    # After chapter complete:
    - Verify Chinese chapter file exists in output/final/zh-CN/
    - Update character_state.md, global_summary.md
    - IF chapter FAIL → respawn that chapter only (max 3 retries)
```

---

## PHASE 4.5: PROSE POLISH (Optional - 启用需 `--polish` flag)

**🔴 此阶段可选，默认跳过。启用时在章节生成后运行。**

**触发条件:** `--polish` 或 TEST阶段发现质量问题（连续短句、人名未翻译等）

**Agent Prompt:**
```
PROSE POLISH AGENT

TASK: Polish Chinese chapters for prose quality

FILES TO PROCESS:
- output/final/zh-CN/chapter_*.md (all chapters)

POLISH CHECKLIST:

1. NAME TRANSLATION FIX
   - Load character_names.json
   - Replace ALL English names with Chinese translations
   - Check: Elena→埃琳娜, Marcus→马库斯, Kira→凯拉, Zara→萨拉, Tobias→托比亚斯, Jace→杰斯
   - Grep for remaining English names → fix each occurrence

2. SENTENCE RHYTHM FIX
   - Find consecutive short sentences (≤15 chars, ≥3 in sequence)
   - Merge into compound sentences using:
     - Comma concatenation: "他走进来，脚步平稳，带着迟疑"
     - Modifier insertion: "她的双腿发抖，体内的声音在支持她"
     - Em-dash insertion (moderate use): "执政官的声音——分裂、困惑——从各个方向传来"
   - Verify: no paragraph has ≥4 consecutive short sentences

3. PROSE QUALITY ENHANCEMENT
   - Remove filter words: 看到/听到/感到/注意到/意识到 → rewrite with direct sensory
   - Remove thought tags: 她想/他觉得/在心里 → rewrite with action beats
   - Add sensory variety: ensure 2+ sensory types per scene (visual, auditory, tactile, olfactory)
   - Vary sentence openings: avoid repetitive "他/她/它" starts

4. DIALOGUE POLISH
   - Ensure merged quote format (no split dialogue)
   - Add micro-actions to dialogue beats (敲桌、攥拳、别过脸)
   - Remove redundant dialogue tags

OUTPUT: Updated chapter files in output/final/zh-CN/

VERIFY BEFORE EXITING:
- Grep for English names → count = 0
- No paragraph with ≥4 consecutive short sentences
- No filter words in >50% of paragraphs
- All dialogue uses merged format

Report: 'POLISH COMPLETE - X chapters polished'
```

**Orchestrator actions:**
- Spawn polish agent for each chapter (or batch by act)
- Verify each polished chapter meets quality checks
- IF polish fails → respawn with specific error feedback

---

## PHASE 5: COMPILE (Run Python Script)

**Use Python script for merging (NOT LLM agents):**

```bash
# Run the merge script directly
python novels/<project_name>/scripts/merge_novel.py
```

**Script features:**
- Merges Chinese chapters → output/final/zh-CN/novel_full_zh.md
- Proper title header formatting
- Correct chapter separators (---)
- Handles chapter first lines properly

**After script completes:**
1. Verify novel_full_zh.md exists with correct word count
2. Update `progress.json: phases.compile.status = "complete"`

---

## PHASE 6: AUTO-TEST (Spawn Agent)

**Agent Prompt:**
```
You are the TEST agent for novel generation.

TASK: Validate the completed novel meets all quality requirements.

FILES TO CHECK:
- output/final/zh-CN/novel_full_zh.md
- memory/progress.json

TEST CHECKLIST:

1. CHAPTER COUNT
   - Chinese: Count chapters = {chapter_count} ✓/✗

2. WORD COUNT
   - Chinese total words ≥ {chapter_count * 2000} ✓/✗

3. NO SCRIPT MARKERS (CRITICAL - 铁律一)
   - No "## 第一幕", "## 冷开场", "## 尾声" ✓/✗
   - No "## Scene" headers ✓/✗
   - No 【...】 bracketed headers ✓/✗

4. NO META-INFO MARKERS (CRITICAL - 铁律三)
   - No "第四章完成" / "字数：约X字" ✓/✗
   - No completion/word count markers ✓/✗

5. NO ENGLISH VOCABULARY EMBEDDED (CRITICAL - 铁律六)
   - No English words in Chinese sentences ✓/✗
   - Check for common embedded words: coherent, pulsing, chill, strange, warm, cold, bright, dark, heavy, light, sharp, soft, hard, fast, slow
   - Check method: grep for lowercase English words (排除专有名词缩写如DNA, AI)
   - If ANY English vocabulary found → CRITICAL FAILURE

6. DEEP POV VERIFICATION (CRITICAL - 铁律七)
   - Filter word count per chapter: 看到/听到/感到/注意到/意识到/想/记得 ≤ 5 ✓/✗
   - No thought tags: 她想/他觉得/在心里/思索着 ✓/✗
   - No direct emotion words: 很恐惧/很愤怒/很悲伤 ✓/✗
   - Sensory details in every scene (2+ types) ✓/✗
   - Check method: Count filter words per chapter, report chapters exceeding threshold

7. NATURAL DIALOGUE (spot check 5 chapters - 铁律二)
   - Dialogue uses merged Chinese quote format ✓/✗
   - No English-style split dialogue ✓/✗
   - Dialogue sounds like real speech ✓/✗

8. PUNCTUATION
   - Dialogue uses "" not 「」 ✓/✗

9. NAME TRANSLATION COMPLIANCE (CRITICAL - 铁律五)
   - No English names in Chinese text: Elena/Marcus/Kira/Zara/Tobias/Jace ✓/✗
   - All names match character_names.json mappings ✓/✗
   - Check method: grep for each English name in chapter files
   - If ANY English name found → CRITICAL FAILURE

10. SENTENCE RHYTHM CHECK (CRITICAL - 铁律八)
    - No consecutive short sentences (≤15 chars) exceeding 2 in sequence ✓/✗
    - Check method: For each paragraph, count consecutive sentences with len ≤ 15
    - PASS: max consecutive short sentences ≤ 2
    - WARN: 3 consecutive short sentences
    - FAIL: ≥4 consecutive short sentences (must regenerate)

11. EM-DASH DENSITY CHECK (CRITICAL - 铁律四)
    - For each chapter: count("——") / total_chars ≤ 0.05 (5%) ✓/✗
    - WARN: ratio 5%-10%
    - FAIL: ratio > 10% (text fragmented, must regenerate)

OUTPUT: test_report.md with ✓/✗ for each check

If check 3, 4, 5, 6, 9, 10, or 11 FAILS → regenerate those chapters.

Report: 'TEST COMPLETE - X/11 checks passed'
```

---

## Progress Tracking

**progress.json structure:**
```json
{
  "project": "project_name",
  "status": "IN_PROGRESS",
  "chapter_count": 40,
  "phases": {
    "init": {"status": "complete"},
    "idea": {"status": "complete", "agent_id": "agent_abc1", "verified": true},
    "world": {
      "status": "complete",
      "agent_id": "agent_abc2",
      "verified": true
    },
    "blueprint": {"status": "complete", "agent_id": "agent_abc3", "chapter_count_verified": 40},
    "chapters": {
      "status": "in_progress",
      "current_batch": 1,
      "completed_count": 0,
      "batches": [...]
    },
    "compile": {"status": "pending"},
    "test": {"status": "pending", "passed": false}
  },
  "continuity_files": {
    "character_state": "memory/character_state.md",
    "global_summary": "memory/global_summary.md",
    "chapter_summaries": "memory/chapter_summary_*.md"
  },
  "final_files": {
    "novel_full_zh": "output/final/zh-CN/novel_full_zh.md"
  }
}
```

---

## Output Format

```
╔══════════════════════════════════════════════════════════════╗
║  NOVEL GENERATION: <project_name> (直接中文输出)              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ✓ PHASE 1: INIT (Orchestrator)                             ║
║    Folder created, structure initialized                    ║
║                                                              ║
║  ✓ PHASE 2: IDEA (Agent: ideator-abc1)                      ║
║    Core seed: 450 words                                      ║
║    Terms extracted: 12                                       ║
║                                                              ║
║  ✓ PHASE 3: WORLD (Agent: worldbuilder-abc2)                ║
║    Characters: 8 with language profiles                      ║
║    World dimensions: 3                                       ║
║                                                              ║
║  ✓ PHASE 4: BLUEPRINT (Agent: architect-abc3)               ║
║    Chapter blueprint: {chapter_count} chapters               ║
║                                                              ║
║  ✓ PHASE 5: CHAPTERS ({chapter_count} agents)               ║
║    Chapter 1: ✓ 3,000 words (zh-CN)                          ║
║    Chapter 2: ✓ 3,100 words (zh-CN)                          ║
║    ...                                                       ║
║                                                              ║
║  ✓ PHASE 6: COMPILE (Python script)                         ║
║    novel_full_zh.md created                                  ║
║                                                              ║
║  ✓ PHASE 7: TEST (Agent: tester-abcX)                       ║
║    All checks passed                                         ║
║                                                              ║
║  ✓ DONE - Novel complete in Chinese                         ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Summary

| Feature | Status |
|---------|--------|
| 直接中文输出 | ✓ 无英文章节中间步骤 |
| TV结构 | ✓ 仅作内部参考，不输出到文件 |
| 禁止元信息 | ✓ 铁律三：无完成标记、字数统计 |
| Agent隔离 | ✓ 每章节独立context |
| 连续性追踪 | ✓ chapter_summary, character_state |
| 自动测试 | ✓ 11项质量检查 |
| 人名翻译强制 | ✓ 铁律五：必须使用character_names.json译名 |
| 中文纯度 | ✓ 铁律六：严禁英文词汇嵌入中文句子 |
| 深度POV | ✓ 铁律七：禁止过滤词（≤5次/章） |
| 句子节奏控制 | ✓ 铁律八：禁止连续短句超过2个 |
| 破折号控制 | ✓ 铁律四：密度≤5% |
| 可选Polish | ✓ `--polish` 启用润色修复阶段 |

---

## License

MIT License
