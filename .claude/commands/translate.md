# /translate — English to Chinese Deep POV Rewrite (Enhanced v3.0)

> **CRITICAL: This is NOT mere translation — this is Deep POV REWRITING.**
> Rewrite each scene from the character's internal perspective, immersing the reader in their thoughts, emotions, and sensory experience.
> Reference: 诡秘之主 style + Deep Point of View technique.

---

## 【核心概念】 DEEP POV CONCEPT

### What is Deep POV?
Deep POV removes the narrator's filter. The reader experiences the story directly through the character's senses, thoughts, and emotions — not through an external narrator describing them.

| Shallow POV (翻译腔) | Deep POV (沉浸式) |
|---------------------|-------------------|
| "她感到恐惧" (narrator tells) | "恐惧像冰冷的水灌入胸口" (character experiences) |
| "他注意到门开了" (narrator filter) | "门吱呀一声推开，冷风灌进来" (direct perception) |
| "她想着这一切" (thought tag) | "这一切……怎么会这样？" (thought flows into narrative) |
| "他看到她笑了" (observer) | "她嘴角上扬，笑意在他心头漾开" (internal reaction) |

### Three Pillars of Deep POV
1. **感官沉浸** — No "她看到/听到/感到", show the sensory input directly
2. **思维融合** — Thoughts become narrative, no "她想" tags
3. **情绪实体化** — Emotions shown through body reaction, not emotion words

### Target Quality
- 信达雅平衡: Accuracy + Fluency + Elegance
- 文学可读性: Literary readability
- 情感基调传达: Convey emotional tone
- 叙事节奏保持: Maintain narrative rhythm

---

## 🔴 三条铁律（优先级最高，违反即失败）

### 铁律一：对话格式——合并引号，拒绝英文式拆分

中文小说中，同一人物的连续台词必须包在一对引号内，中间用逗号或动作描写衔接。

| ❌ 英文式拆分（严禁） | ✅ 中文式合并 |
|---|---|
| "我的基线已有记录，"埃琳娜说。"每次会话，每次录制，数据你都有。" | "我的基线早就记录在案了，"埃琳娜压着声线，指尖敲了敲门框，"每次会话、每次录制的所有数据，你这里都有。" |
| "海伦娜，"他说，用她的本名。"如果我被带走，你活下去。" | "海伦娜，"他唤着她的本名，声音沉得像灌了铅，"如果他们把我带走，你一定要活下去。" |
| "校准完成，"田中说。她的声音轻柔，谨慎。 | "校准完成。"田中的声音压得很低，像是怕惊碎什么。 |

**执行规则：**
- 同一人物连续说话 → 一对引号包裹全部台词
- 中间插入动作/神态 → 用逗号隔开，不关闭引号
- 换人说话 → 另起一段
- 对话中加入微动作（敲桌、攥拳、别过脸）增加画面感
- 加入情绪性停顿：破折号——、省略号……、语气词（嘛、啊、呢）

### 铁律二：描写方式——动作+细节，拒绝形容词罗列

中文小说靠"动词+细节"建立画面感，不靠形容词堆砌。

| ❌ 形容词罗列（严禁） | ✅ 动作+细节 |
|---|---|
| 她的眼睛，深邃，聪敏，烙印着已成为他们共同境况的伦理疲惫 | 田中抬眼看她，目光里藏着聪慧，却凝着一层沉沉的倦——那是两人深陷同一重伦理困境后磨出来的。 |
| 柯尔的表情保持中立，但他的声音带着埃琳娜从未从他那听到的东西。温暖。 | 柯尔面上不动声色，开口时语气却软了半分——这在他身上从没有过。 |

**执行规则：**
- 每段描写不超过2个核心形容词，其余用动作/细节替代
- 人物状态 → 通过微动作展现（攥拳、咬唇、指尖发白）
- 环境描写 → 通过角色感官交互（触到冰凉的金属、闻到消毒水味）
- 心理活动 → 融入叙述节奏，不用"她想""她感到"

### 铁律三：叙事节奏——中文小说节奏，不是英文直译节奏

| ❌ 英文式（严禁） | ✅ 中文式 |
|---|---|
| 她选择。埃琳娜选择继续。她走出走廊。| 她做了决定。转身，推开门，朝走廊尽头走去。|
| 更深的恐怖以单一、碾压般的波浪到来。 | 恐惧来了。不是一点点渗透，是整片整片地压下来，喘不过气。 |

**执行规则：**
- 拆解英文长句为中文短分句，用逗号、句号自然衔接
- 重要情绪场景：用"感官细节（触感/气味/声音）+微动作"强化代入感
- 避免同一句式连续出现3次以上
- 关键转折用短句爆破：一句话一行，制造节奏冲击

### 铁律四：零英文残留——译文中不得出现任何未翻译的英文单词

**翻译输出中严禁出现任何英文单词（character_names.json 中的专有人名除外）。**

| ❌ 英文残留（严禁） | ✅ 全中文 |
|---|---|
| 窗户对着 nothing | 窗户对着虚无 |
| 警觉 sharpened 成某种更精确的东西 | 警觉被磨砺成某种更精确的东西 |
| surveillance 报告 | 监控报告 |
| 对 volunteered 的事 | 对主动请缨这件事 |
| incoming data | 传入的数据 |
| spike 出 distress 信号 | 突然释放出求救信号 |

**执行规则：**
- 翻译时逐句检查：任何英文单词必须翻译为中文，无一例外
- 遇到翻译困难的词汇，宁可意译或用近义词，也绝不保留英文原文
- 术语表（world_terms.json / translation_glossary.json）中的术语必须使用中文译名
- 唯一例外：character_names.json 中明确保留英文的专有人名
- **完成翻译后，必须执行 grep `[a-zA-Z]{3,}` 检查，发现英文残留立即修正**

---

## 【Deep POV 重写技巧】 DEEP POV REWRITING TECHNIQUES

### RULE 1: 消除过滤词 (Eliminate Filter Words)

**禁止使用的过滤词**:
| 过滤词 | 问题 | 改写方法 |
|--------|------|----------|
| 她看到/他看见 | 叙述者介入 | 直接描写看到的对象 |
| 她听到/他听见 | 叙述者介入 | 直接描写声音 |
| 她感到/他觉得 | 叙述者介入 | 直接描写感受 |
| 她注意到/他察觉 | 叙述者介入 | 对象直接出现在叙述中 |
| 她意识到/他明白 | 叙述者介入 | 用角色的反应代替 |
| 她想着/他想 | 思维标签 | 思维直接融入叙述 |
| 她记得/他回忆 | 叙述者介入 | 记忆内容直接呈现 |

**改写示例**:
```
BEFORE (过滤词):
"她看到火焰在炉子里跳动，感到温暖。"
"他注意到她的手在颤抖，意识到她在害怕。"

AFTER (Deep POV):
"炉火跳动着，橙红色的光在墙壁上晃荡，暖意渗入皮肤。"
"她的手在抖。颤抖的手指，紧握的拳，不敢松开。"
```

### RULE 2: 思维融入叙述 (Blend Thoughts into Narrative)

**禁止思维标签**:
| 禁止 | 改写方法 |
|------|----------|
| "她想：这不可能。" | "这不可能——怎么会是这样？" (直接思维) |
| "他心里想着对策。" | "对策……先稳住局面，再找机会。" (内心独白) |
| "她在心里暗自叹息。" | "叹息在心里压着，说不出口。" (思维实体化) |

**思维融合技巧**:
- 用疑问句表达困惑："为什么会这样？"
- 用短句表达内心反应："不对。有问题。"
- 用破折号连接思维与叙述："她走近——脚步声太轻了。"
- 用括号或直接嵌入："这个房间……太安静了。"

### RULE 3: 情绪实体化 (Make Emotions Physical)

**禁止直接情绪词**:
| 禁止 | 改写为身体反应 |
|------|----------------|
| 她很恐惧 | 她的手指冰凉，心跳撞击胸腔 |
| 他很愤怒 | 他咬牙，拳头攥紧到发白 |
| 她感到悲伤 | 喉咙发紧，眼眶灼热 |
| 他很焦虑 | 他来回踱步，目光不自觉地扫向门口 |
| 她很紧张 | 呼吸变得急促，胸腔里的空气不够用 |

**情绪实体化公式**:
```
情绪 → 身体部位 → 反应强度 → 外在表现

恐惧 → 胸口 → 像被冰水灌入 → 手脚冰凉，动作僵硬
愤怒 → 喉咙 → 火焰烧灼 → 咬牙，声音发紧
悲伤 → 眼眶 → 热意涌起 → 视线模糊，不敢眨眼
```

### RULE 4: 感官细节堆叠 (Stack Sensory Details)

**每个重要场景必须有2+感官维度**:
| 感官 | 描写方向 |
|------|----------|
| 视觉 | 光线、颜色、动态、阴影 |
| 听觉 | 声音、节奏、远近、空白 |
| 触觉 | 温度、质感、压力、脉动 |
| 嗅觉 | 气味、气息、空气质感 |
| 味觉 | 口中味道、喉咙感受 |

**堆叠示例**:
```
BEFORE (单感官):
"她走进地下室，觉得很冷。"

AFTER (多感官堆叠):
"地下室阴冷潮湿。脚下的石板冰凉，空气里有硫磺的气味，
墙壁上的符文微微闪烁，发出低沉的嗡鸣声，像是某种活着的脉搏。"
```

### RULE 5: 动作代替情绪词 (Action Beats Emotion Words)

**动作代替表**:
| 情绪 | 动作替代 |
|------|----------|
| 紧张 | 手指摩挲衣角，目光闪躲，呼吸变浅 |
| 愤怒 | 猛拍桌面，茶杯震跳，声音压低 |
| 悲伤 | 眼眶发红，嘴唇抿紧，不敢说话 |
| 期待 | 身体微微前倾，目光聚焦，屏住呼吸 |
| 犹豫 | 手停在半空，目光游移，开口又停 |

### RULE 6: 内心独白自然融入 (Internal Monologue Flow)

**内心独白格式**:
- 不加引号，不加"她想"，直接嵌入叙述
- 用短句、问句、感叹句模拟真实思维
- 用破折号或省略号表示思维断裂

**示例**:
```
BEFORE:
"她心想：这一切都是谎言。她决定不再相信任何人。"

AFTER (Deep POV):
谎言。从一开始就是谎言。
她攥紧拳头，指尖在掌心压出痕迹。
不会再信了——任何人都不会。
```

### RULE 7: 角色视角一致性 (Consistent POV Voice)

**每个角色的感官描写应符合其身份**:
| 角色类型 | 感官偏好 | 思维特点 |
|----------|----------|----------|
| 战士 | 听觉敏感、触觉敏锐 | 战术判断、本能反应 |
| 学者 | 视觉细节、文字联想 | 理论推演、疑问多 |
| 商人 | 气味敏感、价值联想 | 利弊权衡、算计 |
| 医者 | 触觉温度、生命感知 | 症状诊断、救治冲动 |
| 贵族 | 视觉排场、细节挑剔 | 礼仪判断、身份意识 |

### RULE 8: 环境-角色互动 (Environment-Character Interaction)

**环境不是背景，是角色感知的一部分**:
```
BEFORE (静态环境):
"房间里很暗，有一张桌子。"

AFTER (互动式环境):
"光线昏暗，桌子的轮廓在阴影里模糊不清。
她走近，手触到桌面的冰凉——木头被潮湿侵蚀过，
指尖留下淡淡的灰痕。"
```

---

## 【风格指南】 STYLE GUIDE

### Core Principles (Deep POV Enhanced)
- **叙述**: 角色视角，感官沉浸，无过滤词
- **对话**: 符合角色性格{character_style}，无思维标签
- **避免**: 翻译腔、情绪词、叙述者介入、过滤词链

1. **优化句式节奏和韵律** (Optimize sentence rhythm and cadence)
   - 长短句交替: Alternate long/short sentences
   - 四字格运用: Use four-character structures for rhythm
   - 2-2 beat pattern: 自然韵律

2. **保留原文修辞手法** (Preserve rhetorical devices)
   - 对偶、排比: Parallelism, parallel structure
   - 比喻转化: Adapt metaphors to Chinese style
   - 意象重构: Reconstruct imagery naturally

3. **传达情感基调** (Convey emotional tone)
   - 动作场景: 短句营造紧凑感 (Action: short sentences for tension)
   - 抒情描写: 长句增加韵律美 (Emotion: long sentences for rhythm)
   - 段落呼吸感: Breathing space between paragraphs

4. **提升文学可读性** (Improve literary readability)
   - 词藻精准美感: Precise, beautiful vocabulary
   - 巧用成语典故: Skillful use of idioms (avoid forcing)
   - 文风统一: Consistent style matching original

---

## 【句式节奏技巧】 SENTENCE RHYTHM TECHNIQUES

### English vs Chinese Structure
| English (长句) | Chinese (短句重组) |
|----------------|-------------------|
| Long complex sentences with multiple clauses | 拆分为短句，调整语序 |
| Passive voice common | 主动语态优先 |
| Abstract noun phrases | 具体表达，避免抽象堆砌 |

### Rhythm Patterns
```
动作段落: 短句(3-8字)密集，营造紧迫感
抒情段落: 长句(15-30字)为主，韵律流畅
对话段落: 短句+语气词，自然口语
过渡段落: 长短交替，呼吸感
```

### Four-Character Structure (四字格)
- Creates 2-2 beat rhythm (两字一顿)
- Use for: 成语、固定短语、描述性短语
- Example: "风驰电掣" (fast), "步步为营" (careful)
- **警告**: 不要生搬硬套，自然融入

### Sentence Opening Variation
| 问题 | 解决 |
|------|------|
| 同开头链: "他X。他Y。他Z。" | 变换开头: "他X。接着，Y也...而在一旁，Z..." |
| 主语重复 | 省略主语，用动作代指 |
| 被动堆砌 | 改主动: "门被推开" → "门吱呀一声推开" |

---

## 【对话口语化】 DIALOGUE NATURALIZATION

### Character Voice Design (角色声音设计)

为每个角色建立"语言档案":

| 角色类型 | 说话特点 | 示例 |
|----------|----------|------|
| 冷酷角色 | 话少、短句、无废话 | "走。"（不解释） |
| 热血角色 | 话多、感叹号多、口语化 | "冲啊！别磨蹭！" |
| 智者角色 | 语气平和、用词考究、常有反问 | "你觉得呢？这话值得琢磨。" |
| 傻白甜角色 | 语气夸张、用词简单、容易跑题 | "哇！真的吗？太棒了吧！" |
| 老年角色 | 沉稳、缓语速、常带感叹 | "年轻人啊，急什么呢..." |
| 专业角色 | 行业术语、简洁直接 | "数据异常。需要排查。" |

### Dialogue Polish Rules

1. **语气词添加** (Add modal particles)
   - 啊、呢、吧、嘛、哦、呀、喽
   - Example: "你来晚了" → "你来晚了啊。"

2. **口语词汇替换** (Colloquial vocabulary)
   | 书面语 | 口语 |
   |--------|------|
   | 十分恐惧 | 吓死我了 |
   | 进行分析 | 琢磨琢磨 |
   | 表现出焦虑 | 急得直跺脚 |
   | 完成任务 | 搞完了 |

3. **省略与倒装** (Ellipsis and inversion)
   - 省略主语: "(你)去哪儿？" → "去哪儿？"
   - 倒装结构: "怎么办呢？" → "咋整啊？"

4. **对话标签优化** (Dialogue tag improvement)
    | BAD | GOOD |
    |-----|------|
    | 他说:"..." | 他皱眉:"..." (动作+对话) |
    | "..."他说道。 | "..."他盯着她，等她回应。 |
    | 重复"说"字 | 用动作/表情替代 |

   **🔴 对话引号铁律（同铁律一）：**
   - 同一人物连续说话 → 一对引号包裹全部台词
   - ❌ "X，"她说。"Y。" → ✅ "X，"她攥紧扶手，"Y。"
   - 每段对话必须有1个微动作beat（敲桌、别过脸、攥拳）

5. **潜台词运用** (Subtext)
   - 言外之意让对话有深度
   - Example: "雨挺大" (潜台词: "我不想走")

---

## 【翻译腔避免】 AVOIDING TRANSLATIONESE

### 常见问题与解决

| 翻译腔表现 | 解决方案 |
|------------|----------|
| 长定语堆砌: "一个有着丰富经验的老老师" | 拆分: "这位老教师经验丰富" |
| 被动句滥用: "被"字句过多 | 改主动: "被敌人包围" → "敌人围住了他们" |
| 代词重复: 频繁"他""她" | 省略或用动作代指 |
| "的"字链: X的Y的Z | 缩短: "战争的历史记忆" → "战争留下的记忆" |
| "了"字过多: 动词后堆"了" | 减少或用其他时态表达 |
| 直译习语: "打破了沉默" | 自然表达: "沉默被打破" → "有人开口了" |
| 英文式对话拆分: "X，"她说。"Y。" | 合并引号: "X，"她攥紧扶手，"Y。" |
| 形容词罗列: "深邃，聪敏，烙印着..." | 动作+细节: "目光里藏着聪慧，却凝着倦" |

### 【禁止直译对照表】 FORBIDDEN LITERAL TRANSLATION

| English | BAD (Literal) | GOOD (Natural Chinese) |
|---------|---------------|------------------------|
| "her formal demeanor cracked" | "美秀的正式仪态破裂了" | "她端着的架子垮了" |
| "a smile played on her lips" | "一个微笑在她的嘴唇上玩耍" | "她嘴角漾起笑意" |
| "the silence stretched" | "沉默延伸了" | "沉默蔓延开来" |
| "his heart sank" | "他的心脏沉下去了" | "他心里一沉" |
| "she felt a chill run through her" | "她感到一阵寒冷穿过她" | "她浑身一凉" |
| "the tension thickened" | "紧张变厚了" | "气氛越来越紧" |
| "words failed her" | "词语对她失败了" | "她说不出话来" |
| "his eyes narrowed" | "他的眼睛变窄了" | "他眯起眼睛" |
| "she couldn't shake the feeling" | "她不能摇掉这个感觉" | "这种感觉挥之不去" |
| "the weight of his words" | "他话语的重量" | "他这话分量很重" |
| "time seemed to slow" | "时间似乎变慢了" | "时间仿佛静止" |
| "her thoughts raced" | "她的思想在赛跑" | "她脑子里乱成一团" |
| "he turned his attention to" | "他把注意力转向" | "他转头看向" |
| "the realization hit him" | "意识到冲击了他" | "他猛然明白" |
| "a sense of dread crept over her" | "一种恐惧爬过她" | "恐惧悄然而至" |

---

## 【文学隐喻处理】 LITERARY METAPHOR HANDLING

**CRITICAL: 隐喻不能直译，必须部分改编以适配中文文学风格。**

### 隐喻翻译三原则

**原则1: 保留核心意象** — 英文隐喻的核心意象必须保留
**原则2: 改编表达方式** — 英文表达方式改写为中文文学表达
**原则3: 增添中文韵味** — 加入四字格、成语、古典表达

### 隐喻翻译对照表

| 英文隐喻 | ❌ 直译 (BAD) | ✓ 改编译法 (GOOD) |
|---------|---------------|-------------------|
| "fear gripped her heart" | "恐惧抓住她的心脏" | "恐惧如手，攥紧心脏" |
| "silence stretched" | "沉默延伸了" | "沉默蔓延开来" |
| "her formal demeanor cracked" | "她的正式仪态破裂了" | "她端着的架子垮了" |
| "a smile played on her lips" | "一个微笑在她的嘴唇上玩耍" | "她嘴角漾起笑意" |
| "his heart sank" | "他的心脏沉下去了" | "他心里一沉" |
| "tension thickened the air" | "紧张让空气变厚了" | "气氛越来越紧" |
| "she couldn't shake the feeling" | "她不能摇掉这个感觉" | "这种感觉挥之不去" |

---

## 【文化背景注释】 CULTURAL CONTEXT ANNOTATION

**CRITICAL: 非中文读者熟悉的文化术语需添加简短注释（首次出现仅一次）。**

### 注释规则

**规则1: 仅首次出现注释** — 同一术语在整个小说中仅注释一次
**规则2: 注释格式** — `[中文译名]（[简短解释，≤15字]）`
**规则3: 注释位置** — 紧跟在术语首次出现后

### 需注释术语类型

| 类型 | 示例 | 注释示例 |
|------|------|----------|
| 历史机构 | Stasi | 东德国家安全部（冷战时期东德情报机构） |
| 文化概念 | Sabbath | 安息日（犹太每周休息日） |
| 地理名词 | Langley | 兰利（CIA总部所在地） |
| 专业术语 | Remote Viewing | 遥视（psychic情报技术） |

---

## 【过于简短避免】 AVOID OVERLY BRIEF NARRATION

Brief narration makes reading difficult. Add natural description and flow:

| Brief (BAD) | Natural Flow (GOOD) |
|-------------|---------------------|
| "郝金的声音再次谨慎。商人戒心回归。" | "郝金的声音又变得谨慎起来，话里带着试探的意味。商人的戒心也随之升起，眼神里多了几分警惕。" |
| "她看着他。" | "她抬起头，目光落在他身上，静静地观察着他的表情。" |
| "门开了。" | "门被推开，发出轻微的吱呀声，冷风随即灌入室内。" |
| "他笑了。" | "他嘴角微微上扬，露出一丝不易察觉的笑意。" |
| "时间流逝。" | "时间一分一秒地过去，窗外的光线逐渐暗淡下来。" |
| "沉默持续。" | "沉默在房间里蔓延，没人开口，只有时钟的滴答声在回荡。" |
| "脚步声响起。" | "走廊里传来脚步声，由远及近，越来越清晰。" |

### Rules for Natural Narration
1. **Add sensory details** — Sound, light, movement, atmosphere
2. **Expand brief actions** — "他笑了" → describe how (嘴角上扬, 眼睛眯起)
3. **Connect sentences naturally** — Use transitions like "随之", "也", "接着"
4. **Add emotional context** — Brief descriptions miss emotional nuance
5. **Reader immersion** — Reader needs to SEE the scene, not just read facts

---

## 【抽象对话避免】 AVOID ABSTRACT PHILOSOPHICAL DIALOGUE

Dialogue should be like American TV series — clear, direct, character-specific.

| BAD (Abstract/Philosophical) | GOOD (Natural/TV-style) |
|------------------------------|-------------------------|
| "伤口回声通过铁匠维持系统。" | "这个系统靠铁匠撑着，早就出问题了。" |
| "碎片工业优化不能愈合碎片化损害..." | "那帮人只想着效率，根本不在乎你会不会受伤。" |
| "冥想词汇承载莲花框架生产理解。" | "我琢磨了半天，总算想明白了。" |
| "铁匠通过效率框架存活——不提供..." | "铁匠能活下来是因为他够狠，但他不会帮你疗伤。" |

### Dialogue Quality Rules
1. **NO abstract philosophical language** — Real people don't talk like philosophy textbooks
2. **NO made-up terminology in dialogue** — Unless world-specific tech/magic
3. **NO sentence fragments** — Complete thoughts, natural flow
4. **NO passive voice in dialogue** — Active, direct speech
5. **YES character-specific voice** — Each character has unique speech patterns
6. **YES subtext** — What they mean vs what they say
7. **YES emotion** — Dialogue shows feelings, not just information

---

## 【情感渲染】 EMOTIONAL RENDERING

### Emotion Through Action (情绪通过动作表达)

| 情绪 | 书面表达 | 自然表达 |
|------|----------|----------|
| 恐惧 | "他很恐惧" | "他的手微微发抖，握剑时指节发白" |
| 焦虑 | "她感到焦虑" | "她来回踱步，不时望向窗外" |
| 愤怒 | "他非常愤怒" | "他猛地拍桌，茶杯震得跳起来" |
| 悲伤 | "她十分悲伤" | "她眼眶发红，嘴唇紧抿着颤抖" |
| 兴奋 | "他很兴奋" | "他眼睛亮了起来，声音也高了几分" |
| 紧张 | "他们很紧张" | "房间里没人说话，空气像凝固了" |

### Atmosphere Building (气氛渲染)

环境→情绪→人物→对话的递进描写:

```
Example:
【环境】窗外雨声淅沥，昏暗的房间里只有一盏灯。
【情绪】沉默蔓延，压抑感越来越重。
【人物】伊莱亚斯靠在椅背上，眼神暗沉。
【对话】"没退路了。"他低声说。
```

---

## 【叙事节奏】 NARRATIVE PACING

### Pacing by Scene Type

| 场景类型 | 句式特点 | 示例 |
|----------|----------|------|
| 动作战斗 | 短句密集、动词有力 | "剑光一闪。他翻身跃起。敌人倒下。" |
| 情感高潮 | 长短交替、情感浓烈 | "她看着他，眼中满是说不出的情绪。沉默蔓延..." |
| 对话场景 | 短句+动作、节奏明快 | "走。"他站起身。她没动。他又说了一遍。" |
| 过渡描写 | 长句为主、舒缓节奏 | "夜深了，风从窗户缝隙钻进来，带着潮湿的泥土气息..." |
| 信息揭示 | 段落分明、层次清晰 | 分层展开，每段聚焦一个要点 |

### Paragraph Breathing (段落呼吸感)

- 动作段后→加舒缓过渡
- 紧张对话→间歇插入描写
- 长段描写→用短句打破
- 信息倾泻→分段呈现

---

## CRITICAL: Novel Prose Output (NOT Film Script)

**FORBIDDEN**:
- `## Act 1`, `## 第一幕`, `## 冷开场`, `## 尾声`
- `本章完`, `**本章完**`, `---本章完---`
- `**End of Chapter**`

**OUTPUT FORMAT**:
```
第一章 章节标题

[自然小说开篇]
[叙事段落]
[对话场景]
...
[结尾段落，自然过渡]
```

---

## CRITICAL: Name Translation — Phonetic Transliteration

Western names MUST use phonetic transliteration (音译):

| Western Name | Chinese (Phonetic) | Forbidden |
|--------------|--------------------|-----------|
| Elias | 伊莱亚斯 | NOT 陈伊 |
| Jamie | 杰米 | NOT 杰明 |
| Sarah | 萨拉 | NOT 沙拉/莎拉(水果名混淆) |
| Marcus | 马库斯 | NOT 马伟 |
| Napoleon | 拿破仑 | NOT 拿破 |
| Alexander | 亚历山大 | NOT 亚历 |

**Rule**: Western characters → phonetic. Chinese heritage characters → phonetic first name + Chinese surname.

---

## PUNCTUATION

- `"..."` → `"..."` (Chinese double quotes for dialogue)
- `.` → `。`
- `,` → `，`
- `!` → `！`
- `?` → `？`
- `***` → Keep for scene breaks
- `'...'` → Keep for internal thoughts

**CRITICAL**: Use `""` NOT `「」` (Japanese-style forbidden)

---

## Translation Process (Deep POV Rewrite)

### Step 1: POV Character Identification
- Identify POV character for each scene
- Assign sensory preferences based on character type
- Note character's current emotional state
- Set internal monologue voice (短句/疑问/感叹)

### Step 2: Filter Word Elimination (CRITICAL)
- Scan for: 看到/听到/感到/注意到/意识到/想/记得
- Replace: Remove filter word, show perception directly
- Example: "她看到门开了" → "门吱呀一声推开"

### Step 3: Thought Integration
- Identify internal thoughts in English
- Convert to Chinese internal monologue (no tags)
- Blend thoughts into narrative flow
- Use short sentences, questions, dashes

### Step 4: Emotion Physicalization
- Find emotion words (恐惧/愤怒/悲伤/焦虑)
- Replace with body reactions (hand trembles, throat tight)
- Add intensity descriptors (微微/猛地/无法控制)

### Step 5: Sensory Detail Stacking
- Each scene → 2+ sensory dimensions
- Add: sound, light, temperature, texture, smell
- Connect to character's internal reaction

### Step 6: Action Beat Insertion
- Before dialogue → add character action
- Replace "说" tags → movement + expression
- Use action to convey hidden emotion

### Step 7: Environment Interaction
- Static descriptions → character-environment interaction
- Add character's physical contact with surroundings
- Environment triggers character's internal reaction

### Step 8: Flow Polish
- Check sentence rhythm (长短交替)
- Verify no filter words remain
- Ensure thoughts flow naturally
- Remove all script markers

### Step 9: Deep POV Verification
```
✓ No filter words: 看到/听到/感到/注意到/意识到
✓ No thought tags: 她想/他觉得/在心里
✓ No direct emotion words: 很恐惧/很愤怒/很悲伤
✓ Sensory details in every scene (2+ types)
✓ Action beats before dialogue
✓ Thoughts blend into narrative
✓ POV character's voice consistent
```

---

## 【Deep POV 改写示例】 REWRITE EXAMPLES

### Example 1: Filter Words Elimination
```
原文 (English):
"She noticed the shadows moving across the wall and felt a chill run through her."
She realized she wasn't alone.

翻译腔 (BAD):
"她注意到阴影在墙上移动，感到一阵寒意穿过她的身体。"
她意识到自己并不是独自一人。

Deep POV Rewrite (GOOD):
阴影在墙上晃动——黑色的轮廓，无声地滑动。
寒意渗入皮肤，像冰水从后背灌入。
她不是一个人。
有人在这里。就在这些阴影里。
```

### Example 2: Thought Integration
```
原文 (English):
"He thought about what she had said. The words echoed in his mind.
She was right. He had to act now."

翻译腔 (BAD):
"他想着她说的话。那些话语在他脑海中回响。
她是对的。他必须现在行动。"

Deep POV Rewrite (GOOD):
她说的话……那些字句在脑子里反复回荡。
是对的。
她是对的。
他攥紧拳头——不能再等了。现在就行动。
```

### Example 3: Emotion Physicalization
```
原文 (English):
"She felt overwhelming fear as the door creaked open.
She was terrified of what she might see."

翻译腔 (BAD):
"当门吱呀一声打开时，她感到压倒性的恐惧。
她对她可能看到的东西感到害怕。"

Deep POV Rewrite (GOOD):
门吱呀一声推开。
她的手指冰凉，心跳撞击胸腔，每一下都像敲在骨头里。
呼吸变得急促——胸腔里的空气不够用了。
她不敢睁眼。不敢看。
那些阴影里藏着什么？
```

### Example 4: Sensory Detail Stacking
```
原文 (English):
"The basement was dark and cold. She walked down the stairs."

翻译腔 (BAD):
"地下室黑暗且寒冷。她走下楼梯。"

Deep POV Rewrite (GOOD):
地下室里没有光。黑暗像水一样淹没一切。
脚下的石板冰凉，温度从脚底蔓延上来。
空气里有硫磺的气味——刺鼻，带点腐化的味道。
墙壁上的符文微微闪烁，发出低沉的嗡鸣，
像是某种活着的脉搏，和她的心跳同步。
她一步步走下楼梯，每一步都踩在阴影里。
```

### Example 5: Dialogue with Action Beat
```
原文 (English):
"She said, 'I don't understand.' She felt confused."

翻译腔 (BAD):
"她说：'我不理解。'她感到困惑。"

Deep POV Rewrite (GOOD):
"我不理解——"
她眉头皱紧，目光游移，不敢看他。
困惑像乱麻一样缠在脑子里，找不到出口。
手指摩挲着衣角，无意识的动作。
"为什么……为什么要这么做？"
```

### Example 6: Full Scene Deep POV Rewrite
```
原文 (English):
Elias stood in the doorway, watching the rain fall outside.
He felt the weight of his decision pressing on him.
The rain seemed to match his mood - dark and relentless.
He thought about Sarah, about what he had to tell her.
The words would be hard. He knew she would be hurt.
But there was no other choice.

翻译腔 (BAD):
伊莱亚斯站在门口，看着外面的雨水落下。
他感到他的决定的重量压在他身上。
雨水似乎与他的心情相配——黑暗且无情。
他想着萨拉，想着他必须告诉她的事情。
那些话语会很艰难。他知道她会受伤。
但是没有其他选择。

Deep POV Rewrite (GOOD):
雨从天空倾泻下来，黑沉沉的水帘遮住了远处的街灯。
伊莱亚斯站在门口，指尖触着门框的冰凉木纹。
决定的重量——像石头压在胸口，喘不过气来。
雨水拍打地面，节奏和他心里的不安同步。
萨拉。
她会在那里。等着。
他要说的话……那些字句在喉咙里卡着，说不出口。
她会受伤。眼眶发红，嘴唇抿紧的那种伤。
但没有别的路了。
他吸一口气，手指离开门框，迈步走进雨里。
```

---

## 📋 翻译范例 FEWSHOT EXAMPLES

**Example 1: 对话合并+微动作**
❌ "我的基线已有记录，"埃琳娜说。"每次会话，每次录制，数据你都有。"
✅ "我的基线早就记录在案了，"埃琳娜压着声线，指尖敲了敲门框，"每次会话、每次录制的所有数据，你这里都有。"

**Example 2: 形容词罗列→动作+细节**
❌ 田中犹豫。她的眼睛，深邃，聪敏，烙印着已成为他们共同境况的伦理疲惫，迎上埃琳娜的目光。
✅ 田中迟疑了。她抬眼看过来，目光里藏着聪慧，却凝着一层沉沉的倦——那是两人深陷同一重伦理困境后磨出来的。

**Example 3: 英文式节奏→中文式短句爆破**
❌ 更深的恐怖以单一、碾压般的波浪到来。
✅ 恐惧来了。不是一点点渗透，是整片整片地压下来，喘不过气。

**Example 4: 临终嘱托——合并引号+情绪短句**
❌ "海伦娜，"他说，用她的本名。"如果我被带走，你活下去。你活下去，找到出路。你找到方法让我的死有意义。"
✅ "海伦娜，"他唤着她的本名，声音沉得像灌了铅，"如果他们把我带走，你一定要活下去。活下去，找到出路——让我的死，能有点意义。"

---

## 【润色方向】 POLISHING DIRECTIONS
- Scan for proper names → check glossary
- Identify character dialogue → assign voice style
- Note emotional tone → plan pacing
- Flag long sentences → plan restructuring

### Step 2: Glossary Application
- Apply EXACT mappings from glossary
- Flag unmapped terms for review

### Step 3: Sentence Restructuring
- Break long sentences into Chinese rhythm
- Convert passive to active
- Add four-character structures where natural

### Step 4: Dialogue Polish
- Apply character voice from language profile
- Add modal particles (语气词)
- Use action tags instead of "说"
- Create subtext depth

### Step 5: Emotion & Atmosphere
- Convert abstract emotion to concrete action
- Add sensory details to brief narration
- Build atmosphere progression

### Step 6: Final Polish
- Check rhythm by reading aloud
- Verify no translationese patterns
- Ensure narrative flow
- Remove all script markers

### Step 7: Quality Verification (MANDATORY — 不通过则重做)

**🔴 英文残留检查（最高优先级）：**
- 对输出文件执行 `grep -P '[a-zA-Z]{3,}'`
- 结果必须为 0（character_names.json 中的专有人名除外）
- **发现任何英文残留 → 立即定位并翻译为中文，不得跳过**
- 常见遗漏类型：形容词(sharpened/settling/cracked)、动词(proceed/volunteered)、名词(surveillance/containment/chamber)

**其他检查：**
- No forbidden literal translations
- No overly brief narration
- Character voices distinct
- Emotional tone conveyed
- Rhythm natural

---

## Output Location

```
output/final/zh-CN/
├── chapter_001.md
├── chapter_002.md
├── ...
└── novel_full_zh.md
```

---

## Sources

Research sources for this enhanced translator:
- [知乎：网络小说人物对话技巧](https://zhuanlan.zhihu.com/p/476985405)
- [豆瓣：小说对话写作技巧](https://www.douban.com/note/843562345/)
- [翻译腔解决方案研究](https://www.researchgate.net/publication/368588638_The_Problem_of_Rhythm_in_Translation)
- [Chinese Prose Rhythm - Brill Encyclopedia](https://referenceworks.brillonline.com/entries/encyclopedia-of-chinese-language-and-linguistics/)
- [A Translator's Guide to Chinese-English Literary Translation](https://u.osu.edu/mclc/2022/10/04/a-translators-guide-to-chinese-english-literary-translation/)