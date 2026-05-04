# Novel Agent Orchestrator - Execution Guide

## Quick Start

```bash
/novel-agent "Ancient Egypt where gods are dormant AI awakening"
```

Default: 40 chapters, auto-test enabled.

---

## 🔴 Language Flow（语言流程）

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

**关键规则：**
- **Blueprint阶段之前：🇺🇸 全部英文**（core_seed, character_dynamics, world_building, chapter_blueprint, plot_architecture）
- **chapter_summary阶段之后：🇨🇳 全部中文**（prose_style, character_state, global_summary, chapter_summary）
- **语言切换点：** Writer agent读取英文Blueprint → 输出中文小说 → 生成中文摘要

| Phase | Output Files | Language |
|-------|-------------|----------|
| IDEA | core_seed.md | 🇺🇸 English |
| WORLD | character_dynamics.md, world_building.md, prose_style.md | 🇺🇸 English (prose_style规则用中文表述) |
| BLUEPRINT | chapter_blueprint.md, plot_architecture.md | 🇺🇸 English |
| CHAPTERS | chapter_XXX.md, chapter_summary_XXX.md, character_state.md, global_summary.md | 🇨🇳 中文 |
| TEST | test_report.md | 🇨🇳 中文 |

---

## Execution Protocol (For Claude)

### 🔴 CRITICAL: State Management Rule

**When updating ANY JSON file (progress.json, projects_index.json):**
- READ the entire file first → MODIFY the data structure in memory → WRITE the entire file back
- NEVER append to JSON — this creates duplicate keys that JSON parsers silently resolve to the last value, making state tracking unreliable
- Rule: `read → modify → atomic overwrite` for ALL JSON operations

When `/novel-agent` is invoked, follow this EXACT sequence:

### PRE-EXECUTION: Parse Arguments

```
1. Extract description from command
2. Set chapter_count = 40 (DEFAULT) unless --chapters specified
3. Set batch_size = 1 (DEFAULT - ONE chapter per batch to avoid timeout)
4. Set sequential_mode = true (DEFAULT - one agent at a time)
5. Calculate batch_count = chapter_count (each chapter is its own batch)
6. Extract project name from description (first 2 significant words)
7. Create project folder structure
```

**Sequential Background Execution (DEFAULT):**
- batch_size = 1 → ONE chapter written at a time
- Each agent uses `run_in_background: true` → non-blocking execution
- Agents spawned sequentially → timeout prevention (298s window)
- Continuity preserved → each chapter reads previous chapter's summary
- Example: 40 chapters = 40 sequential batches, one agent per batch

### PHASE EXECUTION SEQUENCE

---

## PHASE 1: INIT (Do directly, no agent)

**Actions:**
1. Create folder: `novels/<project_name>/`
2. Create subfolders: `memory/`, `output/chapters/`, `output/final/`, `output/final/zh-CN/`, `scripts/`
3. Write `memory/progress.json` with initial state
4. Copy merge script: `scripts/merge_novel.py` (from templates)
5. Update `novels/projects_index.json`
6. Set `active_project`

**Verification:**
- ✓ Folder exists
- ✓ All subfolders exist
- ✓ progress.json created
- ✓ merge_novel.py exists in scripts/

---

## PHASE 2: IDEA (Spawn Agent)

**Call Agent tool:**
```json
Agent({
  "subagent_type": "general-purpose",
  "model": "inherit",
  "description": "Generate story idea",
  "isolation": "worktree",
  "prompt": "IDEATOR AGENT for novel: <description>

TASK:
1. Web search for genre tropes on Western sites
2. Create core story concept
3. Generate one-sentence essence

OUTPUT to memory/:
- core_seed.md (≥200 words: concept, protagonist, stakes, twist)
- translation_glossary.json (≥5 initial terms)

VERIFY before exiting:
- core_seed.md exists with content
- Glossary has terms

Report: 'IDEA COMPLETE - core_seed.md created (X words, X terms)'"
})
```

**After agent returns:**
1. Read `memory/core_seed.md` - verify exists and ≥200 words
2. IF FAIL → respawn with feedback
3. Update `progress.json: phases.idea.status = "complete"`

---

## PHASE 3: WORLD + CHARACTERS + PROSE STYLE (Spawn Agent)

**🔴 CRITICAL: 此阶段必须生成 prose_style.md，防止风格正反馈放大**

**Call Agent tool:**
```json
Agent({
  "subagent_type": "general-purpose",
  "model": "inherit",
  "description": "Build world, characters, and prose style",
  "isolation": "worktree",
  "prompt": "WORLDBuilder AGENT

READ FIRST: memory/core_seed.md

TASK:
Generate characters, world, and FIXED prose style definition.

OUTPUT to memory/:
- character_dynamics.md (≥1000 words: 6+ characters with language profiles)
- world_building.md (≥800 words: physical/social/metaphorical)
- character_names.json (name → Chinese mappings)
- world_terms.json (world terminology)

🔴 CRITICAL - prose_style.md (防风格正反馈):
必须生成此文件，定义所有章节统一使用的写作风格。

内容必须包含：
1. 基调定义（从core_seed.md Genre提取）
2. 句式结构规则（长短交替比例、复合句优先）
3. 🔴 禁止句式模式：
   - 链式推导结构：连续使用\"X来自Y。Y来自Z。\"句式
   - 精度描述链：连续使用\"数值来自/数值显示\"句式
   - 连续短句：连续≤15字符短句超过2个
   - 重复结构开头：同一段落连续3+句使用相同开头词
4. 对话风格（从character_dynamics提取）
5. 情绪表达规则（禁止直接情绪词，融入动作/环境）
6. 章节末尾规则（禁止链式总结结构）
7. 验证方法（\"来自\"出现次数≤5次/章等）
8. 🔴 环境签名规则（防感官锚定重复）:
   - 每个感官锚定项必须定义为**环境签名**而非固定套话
   - 听觉锚定示例：\"生命支持系统的低频振动\" → 每次出现使用**不同描述**
     * 第一次：介绍其为环境底噪（\"六十赫兹的低鸣\"）
     * 后续：通过人物感知变化来提及（\"嗡鸣停止了\" / \"那个频率在耳道里升了一度\" / \"低鸣在某个频段上震颤\"）
     * 关键场景：听觉锚定的突然改变本身就是情节事件
   - 禁止同一感官锚定以近乎相同的句式出现超过3次
   - 禁止在章节摘要中镜像正文的感官句式

WHY: WRITER agent将读取此固定风格文件，而非继承前一章摘要的风格特征。
这打破正反馈循环，防止\"来自\"链式结构逐章放大。

ALSO CREATE INITIAL CONTINUITY FILES:
- character_state.md (initial states for all characters)
  - Use tree format from prompts/character_state.txt
  - Include: ITEMS, ABILITIES, STATUS (Physical/Mental/Social/Resources), RELATIONSHIPS, TRIGGERED EVENTS, CURRENT GOALS
  - CRITICAL: This file will be updated after each chapter

- global_summary.md (initial story state)
  - Use format from prompts/global_summary.txt
  - Brief setup summary: world state, character positions, initial tensions
  - CRITICAL: This file will be updated after each chapter

LANGUAGE PROFILES per character:
- Speaking style
- Catchphrases/tone
- Sentence patterns
- Emotional expression style
- Unique markers

VERIFY before exiting:
- All 7 files exist (character_dynamics, world_building, character_names, world_terms, prose_style, character_state, global_summary)
- Character dynamics has ≥6 characters
- Each character has language profile
- character_state.md has tree format for each character
- global_summary.md has initial story state
- prose_style.md contains 禁止链式结构规则

Report: 'WORLD COMPLETE - X characters, X world terms, prose_style.md created'"
})
```

**After agent returns:**
1. Verify all 7 files exist (character_dynamics, world_building, character_names, world_terms, prose_style, character_state, global_summary)
2. Check character count ≥6
3. Verify character_state.md has tree format
4. Verify global_summary.md has initial story state
5. **🔴 CRITICAL: Verify prose_style.md exists and contains 防风格正反馈规则**
6. Update `progress.json: phases.world.status = "complete"`

---

## PHASE 4: BLUEPRINT (Act-by-Act Generation - 防截断)

**🔴 CRITICAL: 一次性生成40章易截断 → 改用分Act生成**

### Act-by-Act Strategy

**将 {chapter_count} 章分为4个Act，逐Act生成并验证:**

```
Act划分（40章示例）:
- Act 1: Chapters 1-10 (铺垫期)
- Act 2: Chapters 11-20 (发展期)
- Act 3: Chapters 21-30 (高潮期)
- Act 4: Chapters 31-40 (结局期)

每Act生成后立即验证章节数，防止截断
```

---

### Step 1: Generate Plot Architecture

**Call Agent tool:**
```json
Agent({
  "subagent_type": "general-purpose",
  "model": "inherit",
  "description": "Generate plot architecture",
  "isolation": "worktree",
  "prompt": "ARCHITECT AGENT - Phase 1

READ FIRST: memory/core_seed.md, character_dynamics.md, world_building.md

TASK: Generate three-act plot structure

OUTPUT to memory/:
- plot_architecture.md (three-act structure with act boundaries, key turning points)

FORMAT:
- Act 1 (Chapters 1-{chapter_count/4}): Setup, inciting incident
- Act 2 (Chapters {chapter_count/4+1}-{chapter_count*2/4}): Rising action, midpoint
- Act 3 (Chapters {chapter_count*2/4+1}-{chapter_count*3/4}): Climax preparation
- Act 4 (Chapters {chapter_count*3/4+1}-{chapter_count}): Resolution

VERIFY: plot_architecture.md exists with act structure

Report: 'PLOT COMPLETE - {chapter_count} chapters structured into 4 acts'"
})
```

---

### Step 2: Generate Blueprint Act by Act (Sequential)

**For each Act, spawn separate agent:**

```
For act_num = 1 to 4:
    Spawn ARCHITECT agent for Act {act_num}
    Wait for completion
    Verify chapter count in generated section
    Append to chapter_blueprint.md (or create separate file)
    If verification fails → respawn that Act only
```

**Act Agent Prompt Template:**

```json
Agent({
  "subagent_type": "general-purpose",
  "model": "inherit",
  "description": "Generate blueprint Act {act_num}",
  "isolation": "worktree",
  "prompt": "ARCHITECT AGENT - Act {act_num} Blueprint

READ FIRST: 
- memory/core_seed.md
- memory/character_dynamics.md  
- memory/world_building.md
- memory/plot_architecture.md (刚刚生成的三幕结构)

TASK: Generate EXPLICIT TV structure for Act {act_num}

CHAPTER RANGE:
- Act 1: Chapters 1-{chapter_count/4}
- Act 2: Chapters {chapter_count/4+1}-{chapter_count*2/4}
- Act 3: Chapters {chapter_count*2/4+1}-{chapter_count*3/4}
- Act 4: Chapters {chapter_count*3/4+1}-{chapter_count}

CRITICAL REQUIREMENT:
- Generate EXPLICIT TV structure for EACH chapter in this Act
- NO placeholders like '[Chapters X-Y continue]'
- NO truncation
- Each chapter must have: Cold Open, Act 1-5, Tag with SPECIFIC beats

OUTPUT to memory/:
- chapter_blueprint_act{act_num}.md (this Act's chapters only)
- OR append to chapter_blueprint.md if using single file

BLUEPRINT FORMAT for EACH chapter:
### Chapter N - 'Title'

| Element | Specific Content |
| Cold Open | [Specific scene + dialogue lines] |
| Act 1 | [Specific scene-by-scene beats] |
| Act 2 | [Specific complications] |
| Act 3 | [Specific midpoint twist] |
| Act 4 | [Specific climax] |
| Act 5 | [Specific resolution] |
| Tag | [Specific closing hook] |

VERIFY before exiting:
- COUNT chapters in this Act's blueprint
- Must equal exactly {expected_count_for_this_act}
- If incomplete, REGENERATE (do not exit with placeholder)

Report: 'ACT {act_num} BLUEPRINT COMPLETE - verified {count} chapters'"
})
```

---

### Step 3: Assemble Full Blueprint

**After all 4 Acts complete:**

```
1. Read chapter_blueprint_act1.md, act2.md, act3.md, act4.md
2. Merge into single chapter_blueprint.md (if using single file)
   OR keep separate files (recommended for large novels)
3. COUNT total chapters = verify equals {chapter_count}
4. Update progress.json: phases.blueprint.chapter_count_verified = {count}
```

**Recommended: Keep Act-based files for WRITER efficiency:**
```
memory/
├── chapter_blueprint_act1.md (Chapters 1-10)
├── chapter_blueprint_act2.md (Chapters 11-20)
├── chapter_blueprint_act3.md (Chapters 21-30)
├── chapter_blueprint_act4.md (Chapters 31-40)
```

WRITER agent reads ONLY relevant Act file for its chapter range.

---

### Benefits of Act-by-Act Generation

| Problem | Before | After |
|---------|--------|-------|
| Truncation risk | 40章一次性生成 → 易截断 | 每Act10章 → 低风险 |
| Verification | 失败需全量重生成 | 失败只重生成该Act |
| WRITER efficiency | 加载81KB全文件 | 加载~20KB相关Act |
| Context pressure | 高 | 低 |

---

**After all Acts return:**
1. **CRITICAL: COUNT chapters in assembled blueprint**
2. If count ≠ chapter_count → respawn missing Acts
3. Update `progress.json: phases.blueprint.chapter_count_verified = {count}`
4. Update `progress.json: phases.blueprint.act_files_created = [act1, act2, act3, act4]`

---

## PHASE 5: CHAPTERS (Spawn Sequential Background Agents - 直接中文输出)

**🔴 简化流程：读取blueprint大纲 → 直接用中文写章节，无需英文章节作为中间步骤。**

**Sequential Batch Strategy:**
```
batch_size = 1 (DEFAULT - ONE chapter per batch to avoid timeout)
sequential_mode = true (DEFAULT - one agent at a time)

For chapter_num = 1 to chapter_count:
    Spawn 1 agent with run_in_background: true
    Agent reads blueprint TV structure → writes chapter directly in Chinese
    Wait for agent to complete (auto-notification)
    Update continuity files (character_state.md, global_summary.md)
    Create chapter_summary_{chapter_num}.md for next chapter
    ⚠️ RUN QUALITY MONITOR (see below)
    ⚠️ CHECK COMPRESSION TRIGGER (see below)
    Continue to next chapter
```

---

## ⚠️ PROACTIVE COMPRESSION TRIGGER (Orchestrator Responsibility)

**问题**: `compression_trigger_words: 100000` 定义但从未使用
**解决**: 在每章完成后检查，触发主动压缩

### Compression Check Protocol

**After each chapter completes, orchestrator MUST:**

1. **Read** `memory/progress.json` → get `total_words_written`
2. **Calculate** utilization = total_words_written / compression_trigger_words
3. **If utilization >= 0.7 (70% threshold):**
   ```
   ⚠️ PROACTIVE COMPRESSION TRIGGERED
   
   Actions:
   a. Spawn compression agent (background):
      - Read global_summary.md
      - Compress to max 2000 words (enforce cap)
      - Compress early chapter_summaries (chapters 1-{N-10}) to outcome-only format
      - Log compression event to compression_log
   
   b. Update progress.json:
      - Add to compression_log: {
          "triggered_at": "chapter_{N}",
          "words_before": {total},
          "compression_ratio": {ratio}
        }
   
   c. Log warning: "Proactive compression triggered at Chapter {N}"
   ```

4. **If utilization >= 0.85 (CRITICAL threshold):**
   ```
   🚨 CRITICAL COMPRESSION REQUIRED
   
   Actions:
   a. Pause chapter generation
   b. Spawn aggressive compression agent:
      - Compress global_summary.md to 1500 words
      - Compress ALL chapter_summaries except last 5 to minimal format
      - Consider splitting chapter_blueprint.md into per-act files
   
   c. Report to user: "Context health critical, compression applied"
   ```

### Compression Format for Early Chapters

**Before compression (chapter_summary format):**
```markdown
# 第N章摘要
## 时间地点: ...
## 情节要点: [详细列表]
## 角色状态变化: [详细列表]
## 伏笔管理: ...
```

**After compression (outcome-only format):**
```markdown
# 第N章摘要（压缩）
结局: [1句话描述本章最终结果]
关键变化: [角色X关系Y变化，物品Z获得/丢失]
伏笔状态: [支付/新增伏笔ID]
```

**Token savings**: ~3KB → ~500 bytes per early chapter summary

---

### Metrics to Track in progress.json

```json
{
  "context_health": {
    "estimated_tokens_per_chapter": 15000,
    "compression_count": 0,
    "last_compression_trigger": null,
    "compression_log": []
  },
  "quality_trends": {
    "template_phrase_counts": {
      "来自": [],
      "的内容是": [],
      "意味着": [],
      "数值来自": []
    },
    "opening_types_used": [],
    "last_quality_check": null,
    "warnings_triggered": []
  }
}
```

---

### 🔴 Quality Trend Monitoring (Python Script - NOT Orchestrator)

**问题**: 之前的方案要求 orchestrator（LLM）手动 grep 并更新 JSON，但 LLM 在 40 章循环中无法可靠执行程序化检查。

**解决**: 将质量监控移至 Python 脚本 `scripts/quality_monitor.py`，orchestrator 通过 bash 调用。

**After each chapter completes, orchestrator MUST run:**

```bash
python scripts/quality_monitor.py \
  --chapter output/final/zh-CN/chapter_{chapter_num:03d}.md \
  --project . \
  --chapter-num {chapter_num} \
  --update-progress
```

**Script performs automatically:**
1. Grep for: `来自`, `的内容是`, `沉默\d*秒` → count per chapter
2. Check em-dash (——) density → warn if > 0.05 (5%)
3. Check consecutive short sentences (≤15 chars) → warn if > 2 consecutive
4. Update `memory/progress.json:quality_trends` with per-chapter counts
5. Growth rate detection: if last 3 chapters show >50% growth → CRITICAL warning
6. Same opening type 3+ consecutive → WARNING

**Exit codes:**
- `0` = all clear, continue to next chapter
- `1` = warning(s) logged to progress.json, continue but log
- `2` = critical failure, **spawn rewrite agent for this chapter with strict prose_style.md enforcement**

**Orchestrator response to exit codes:**
```
If exit code 0 → continue to next chapter
If exit code 1 → log warning, continue to next chapter  
If exit code 2 → CRITICAL: Spawn rewrite agent for chapter {N}
    Rewrite agent prompt: "Rewrite chapter {N} with STRICT adherence to prose_style.md.
    The previous version was rejected for quality degradation: [insert quality_monitor error message]."
    After rewrite → re-run quality_monitor → if still code 2 → mark for human review
```

---

**Each Writer Agent Call:**

```
Agent({
   "subagent_type": "general-purpose",
   "model": "inherit",
   "description": "Write chapter {chapter_num} in Chinese",
  "isolation": "worktree",
  "run_in_background": true,
  "prompt": "=== WRITER AGENT - 第{chapter_num}章（直接中文输出）===

## 🔴 流程说明

你不需要先写英文再翻译。你直接读取 chapter_blueprint.md 中的章节大纲（英文TV结构），
然后用中文写成完整小说章节。

**输入 = 英文大纲（TV结构）**
**输出 = 中文小说正文（纯散文，无结构标记）**

---

## 📖 CONTEXT FILES - QUANTIZED RETRIEVAL (防Token溢出)

### ⚠️ CRITICAL: 只加载相关切片，不加载全文件

**问题**: 全量加载导致 ~100KB context → Token溢出 → 质量退化
**解决**: Quantized Retrieval → 只加载当前章节相关内容 (~15-20KB)

---

### 🔒 POSITION-AWARE ORDERING (Lost-in-Middle Prevention)

**科学依据**: LLM在长context中，首尾准确率~95%，中间<50%
**策略**: 关键信息放在首尾两端，次要信息放中间

**加载顺序**（严格遵循）:
```
[START] 必读 ─────────────────────────────────────────
1. memory/prose_style.md (🇨🇳 中文写作风格规范)
   🔴 CRITICAL: 固定风格规则，防止风格正反馈放大
   - 句式结构规则、禁止模式（链式推导结构）
   - 对话风格、情绪表达规则

2. memory/core_seed.md (🇺🇸 英文故事概念、GENRE、铁律)

3. **🔴 Act-based Blueprint加载**（🇺🇸 英文，强制执行）
   ⚠️ 禁止加载全量chapter_blueprint.md（81KB）
   ⚠️ 只加载对应Act文件：
   - Chapter 1-10: memory/chapter_blueprint_act1.md
   - Chapter 11-20: memory/chapter_blueprint_act2.md
   - Chapter 21-30: memory/chapter_blueprint_act3.md
   - Chapter 31-40: memory/chapter_blueprint_act4.md
   ⚠️ 搜索模式: "### Chapter {chapter_num}"
   ⚠️ 只加载当前章节TV结构 (~2KB，而非81KB全文件)

[MIDDLE] 按需加载（🇺🇸 英文）─────────────────────────────────────
4. memory/character_dynamics.md → 只加载相关角色
   ⚠️ 查看chapter_summary_{chapter_num-1}的"角色状态变化"
   ⚠️ 只加载出场角色档案 (~5KB, 2-3个角色)
    
5. memory/world_building.md → 只加载相关设定
   ⚠️ 查看blueprint中的地点/势力提及
   ⚠️ 只加载相关部分 (~3KB)

[END] 连续性+铁律（🇨🇳 中文）───────────────────────────────────────
6. memory/character_state.md ← 连续性：角色当前状态
7. memory/global_summary.md ← 连续性：故事进展摘要
8. memory/chapter_summary_{chapter_num-1}.md ← 前一章摘要（🇨🇳 中文）
9. memory/world_terms.json ← 术语表
10. memory/character_names.json ← 角色名映射
11. **十条铁律** ← CRITICAL规则必须放在END位置
```

---

### 📊 TOKEN预算估算

| 加载方式 | Token消耗 | 风险 |
|---------|----------|------|
| **全量加载** | ~100KB (80K tokens) | 质量退化、指令遗忘 |
| **Quantized** | ~15-20KB (12-16K tokens) | ✓ 安全范围内 |

**目标**: Input context ≤ 60% 有效窗口容量

---

{(If chapter_num > 1)}
⚠️ 不要读取前一章的完整正文（output/final/zh-CN/chapter_{chapter_num-1}.md）。
只读摘要文件。原因：读取完整正文会导致风格正反馈放大（如破折号密度逐章递增直到文本碎片化）。
摘要文件已包含所有必要的情节衔接信息。

---

## 🔒 ATTENTION ANCHORING (SCAN Protocol)

**科学依据**: 长对话中，指令注意力会逐渐漂移（Attention Drift）
**解决**: 每3章进行"主动生成"恢复注意力，而非被动重读

**⚠️ 当 {chapter_num} % 3 == 0 时，必须执行以下ANCHOR步骤：**

### ANCHOR步骤（仅在第3、6、9、12...章执行）

**在开始写作前，用1-2句话回答：**

```
1. 本章节的角色一致性规则是什么？
   （例如："林逸尘保持谨慎语态，不主动表露情感"）

2. 当前激活的剧情约束是什么？
   （例如："量子幽灵的身份尚未揭晓，只能暗示不能明说"）

3. 需要维护的类型惯例是什么？
   （例如："苏维埃科幻冷峻基调，避免过度温情描写"）
```

**⚠️ 这个主动生成过程比被动重读更有效恢复注意力**
**Token消耗**: ~100 tokens vs 重新加载完整指令文件 (~2000 tokens)

---

## 🔴 八条铁律

### 铁律一：TV结构是内部大纲，绝不可输出到文件

| 🔴 FORBIDDEN OUTPUT | Why |
|---|---|
| `## 【冷开场】` / `## Cold Open` | 剧本格式，严禁 |
| `## 【第一幕】` / `## Act 1` | 剧本格式，严禁 |
| `## 【第二幕】` ~ `## 【第五幕】` | 剧本格式，严禁 |
| `## 【尾声】` / `## Tag` | 剧本格式，严禁 |

### 铁律二：对话合并引号

同一人物连续台词必须包在一对引号内。

### 铁律三：输出文件 = 纯小说正文

| 🔴 FORBIDDEN | Why |
|---|---|
| `第四章完成` / `字数：约X字` | 元信息，严禁 |

### 铁律四：禁止破折号滥用（——）

破折号（——）是正常标点，用于插入语、解释、停顿、语气转折。但绝不可用于拆分每个字或每个词。

| 🔴 FORBIDDEN（破折号碎片化） | ✅ CORRECT |
|---|---|
| `他——的——手——在——键——盘——上` | `他的手在键盘上` |
| `不——是——是——在——等——茶` | `不是——是在等茶` |
| `约——零点——三——秒` | `约零点三秒` |
| `一——个——人——在——走廊——里` | `一个人在走廊里` |

**量化规则：任何段落中，破折号（——）出现次数不得超过该段落总字数的5%。如果你发现自己在每个词之间都加破折号，立即停止并重写该段落。**

### 铁律五：人名必须翻译，严禁保留英文原名

所有角色名必须使用 `character_names.json` 中定义的中文译名。绝不可保留英文原名。

| 🔴 FORBIDDEN | ✅ CORRECT |
|---|---|
| `Elena睁开眼睛` | `埃琳娜睁开眼睛` |
| `Marcus站在门口` | `马库斯站在门口` |
| `Kira说` | `凯拉说` |
| `Zara Chen` | `萨拉·陈` |

### 铁律六：中文纯度——严禁英文词汇嵌入中文句子

**所有英文词汇（除专有名词外）必须翻译为中文表达。绝不可在中文句子中嵌入英文单词。**

| 🔴 FORBIDDEN（英文嵌入） | ✅ CORRECT（中文表达） |
|---|---|
| `是某种更 coherent 的东西` | `是某种更连贯的东西` |
| `它 pulsing，发光` | `它在脉动，发出光芒` |
| `chill 她的骨头` | `寒彻她的骨头` |

### 铁律七：深度POV——禁止过滤词和思维标签

**直接体验式描写，无需"看见/听到/感到"等中介词。**

| 🔴 FORBIDDEN（过滤词） | ✅ CORRECT（直接体验） |
|---|---|
| `她看见波形重新排列` | `波形在眼前重新排列` |
| `她感到温暖闪烁` | `温暖在心中闪现` |
| `她记得祖母的样子` | `祖母的样子浮现脑海` |

**量化规则：每章过滤词出现次数不得超过5次。**

### 铁律八：禁止连续短句，必须使用长短交替节奏

中文小说节奏需要变化。连续短句（≤15字符）超过2个会产生机械感。

| 🔴 FORBIDDEN（连续短句） | ✅ CORRECT（长短交替） |
|---|---|
| `执政官沉默了很长时间。Elena等待。她没有威胁。` | `执政官沉默了很长时间，光柱中的颜色变幻不定。埃琳娜等待着，她没有威胁，没有攻击...` |

**量化规则：任何段落中，连续短句（≤15字符）不得超过2个。**

---

## 📝 OUTPUT FILES

1. **output/final/zh-CN/chapter_{chapter_num:03d}.md** ← 中文章节正文
2. **memory/chapter_summary_{chapter_num}.md** ← 章节摘要

---

## 🔴 chapter_summary_*.md 格式规范（CRITICAL - 防止风格正反馈）

**🔴 语言要求：chapter_summary 必须使用 🇨🇳 中文**

**摘要必须使用中性叙事语言，绝不可采用章节正文的风格特征。**

摘要的目的是传递**情节+状态+伏笔**，而非传递**风格+节奏+修辞**。

**为什么用中文摘要？**
- 摘要阶段之后全部使用中文（character_state, global_summary, chapter_summary）
- Writer agent读取中文摘要 → 写中文小说，减少语言切换认知负担
- 中文摘要更准确传达中文章节的情节细节

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
完成后口头说：'第{chapter_num}章完成'"
})
```

---

## PHASE 6: COMPILE (Run Python Script)

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

## PHASE 7: AUTO-TEST (Spawn Agent)

**Agent Prompt:**
```
TEST AGENT

VALIDATE output/final/zh-CN/:

CRITICAL CHECKS（铁律对应）:

1. NO SCRIPT MARKERS（铁律一）
   - No ## 【第一幕】, ## 【冷开场】 ✓/✗
   - No 【...】 bracketed headers ✓/✗

2. NO META-INFO MARKERS（铁律三）
   - No "第四章完成" / "字数：约X字" ✓/✗

3. NO ENGLISH VOCABULARY EMBEDDED（铁律六 - 新增）
   - No English words in Chinese sentences ✓/✗
   - Check for: coherent, pulsing, chill, strange, warm, cold, bright, dark, heavy, light
   - Grep for lowercase English words (exclude proper noun abbreviations like DNA, AI)
   - If ANY found → CRITICAL FAILURE

4. DEEP POV VERIFICATION（铁律七 - 新增）
   - Filter word count per chapter ≤ 5 ✓/✗
   - No thought tags: 她想/他觉得 ✓/✗
   - No direct emotion: 很恐惧/很愤怒 ✓/✗

5. EM-DASH DENSITY CHECK（铁律四）
   - ratio ≤ 5% (PASS), 5-10% (WARN), >10% (FAIL)

STANDARD CHECKS:
 6. Chapter count: = {chapter_count}?
 7. Word count: ≥{chapter_count * 2000}?
 8. Natural dialogue: merged quote format?（铁律二）

CRITICAL CHECKS:
 9. NAME TRANSLATION COMPLIANCE（铁律五）
    - No English names: Elena/Marcus/Kira/Zara ✓/✗
    - If ANY found → CRITICAL FAILURE

 10. SENTENCE RHYTHM CHECK（铁律八 - 更严格）
     - max consecutive short sentences ≤ 2 (PASS)
     - 3 consecutive (WARN)
     - ≥4 consecutive (FAIL)

 11. EM-DASH DENSITY（铁律四）
     - ratio ≤ 5% (PASS), >10% (FAIL)

OUTPUT: test_report.md with ✓/✗ for each check

If check 1, 2, 3, 4, 9, 10, or 11 FAILS → regenerate those chapters.

Report: 'TEST COMPLETE - X/11 checks passed'"
```

---

## FINAL OUTPUT

Display completion summary with all agent IDs and verification results.

---

## Resumption Logic

If `/novel-agent --project <name>` is called:

1. Read `memory/progress.json`
2. Find last completed phase
3. Resume from next incomplete phase
4. Re-verify previous phase outputs before proceeding

---

## Error Recovery

If agent fails verification 3 times:
1. Log error
2. Report to user with specific failure
3. User can choose to regenerate or adjust