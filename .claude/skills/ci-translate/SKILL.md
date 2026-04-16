---
name: ci-translate
description: CodeIgniter RST 英译中翻译工具。用于翻译用户指南 `.rst` 文档，并在同一流程中完成英文备份、guard 校验、静态审查、按报告修订后再定稿。用户要求翻译 CodeIgniter 文档、章节或页面为中文时应使用此 skill。
argument-hint: <file-path>
---

CodeIgniter 用户指南（Sphinx + reStructuredText）翻译 skill。

**工作流**：备份英文原文 → 翻译 → guard → 审查 → 修订 → guard → 定稿 → 清理备份

**使用方法**
```bash
/ci-translate source/libraries/caching.rst
```

## 参数

- 只接受一个参数：待翻译的 `.rst` 文件路径
- 文件路径为 `$ARGUMENTS`
- 记作 `FILE_PATH="$ARGUMENTS"`

## 任务目标

1. 生成可直接提交的中文 `.rst`
2. 保持 reST/Sphinx 结构零破坏
3. 保证信息零遗漏、零增添、零篡改
4. 在退出前完成 guard + 审查闭环，而不是只翻译不验收

## 执行步骤

### 1. 备份英文原文

```bash
cp "$FILE_PATH" "$FILE_PATH.en.bak"
```

一律以 `$FILE_PATH.en.bak` 作为英文对照源；

### 2. 翻译并回写原文件

读取 `$FILE_PATH.en.bak`，将英文 `.rst` 翻译为中文后覆盖写回 `$FILE_PATH`。

翻译时遵守以下统一规则。

#### A. 格式零破坏（关键规则 + 示例）

以下内容**只翻译可见中文内容，不改结构本身**。

**A1. reST 指令保持英文**

```rst
❌ 错误：
.. 注意:: 此方法已弃用。

✅ 正确：
.. note:: 此方法已弃用。
```

指令名 `.. note::`、`.. warning::`、`.. code-block::`、`.. deprecated::`、`.. versionadded::`、`.. php:method::` 等**必须保持英文**。

**A2. 交叉引用保持英文**

```rst
❌ 错误：详见 :文档:`incoming`。

✅ 正确：详见 :doc:`incoming`。

❌ 错误：使用 :方法:`find()`。

✅ 正确：使用 :meth:`find()`。
```

角色名 `:doc:`、`:meth:`、`:class:`、`:func:`、`:ref:` 等**必须保持英文**，反引号内的目标也保持英文。

**A3. 段落结尾双冒号必须保留**

```rst
❌ 错误：设置变量如下：
❌ 错误：设置变量如下：：

✅ 正确：设置变量如下::
```

RST 中 `::` 表示后续缩进内容为代码块/文字块，**严禁改为中文冒号**。

**A4. 其他保持原样的元素**

- 显式目标、锚点：`.. _label:` 保持原样
- 替换标记：`|substitution|` 保持原样
- 缩进、空行、列表层级、表格对齐不要“顺手格式化”

#### B. 代码与字面量零翻译

以下内容**一律保持英文原样**。

**B1. 代码块内容不翻译**

```rst
❌ 错误：
.. code-block:: php

    $配置 = new 配置();  // 翻译了变量名和类名
    $配置->设置('键', '值');  // 翻译了方法和参数

✅ 正确：
.. code-block:: php

    $config = new Config();  // 完全保持英文
    $config->set('key', 'value');  // 完全保持英文
```

**B2. 行内字面量不翻译**

```rst
❌ 错误：调用 ``查找()`` 方法查询数据库。

✅ 正确：调用 ``find()`` 方法查询数据库。
```

**B3. 类名、方法名、属性、常量不翻译**

```rst
❌ 错误：会话类提供会话管理功能。

✅ 正确：Session 类提供会话管理功能。

❌ 错误：使用邮件类发送邮件。

✅ 正确：使用 Email 类发送邮件。
```

**B4. 配置键、参数名、URL、文件路径不翻译**

```rst
❌ 错误：设置 ``数据库.主机`` 为 ``本地主机``。

✅ 正确：设置 ``database.hostname`` 为 ``localhost``。
```

**保持英文的完整清单**：代码块、命令行示例、配置片段、日志输出、行内字面量 ``...`` 内的内容、类名、方法名、属性、常量、配置键、命名空间、文件路径、URL、HTTP 头字段名、状态码、参数名。

#### C. 信息零遗漏（高危风险点）

翻译时必须逐项核对，**严禁遗漏或弱化**以下信息。

**C1. 版本限定（Critical）**

```rst
英文：This feature is only available in 4.3 or later.
❌ 错误：此功能在 4.3 版本可用。（遗漏了 only 和 or later）
✅ 正确：此功能仅在 4.3 或更高版本中可用。

英文：Before 4.0, use the legacy syntax.
❌ 错误：4.0 版本使用传统语法。（时间关系错误）
✅ 正确：4.0 之前请使用传统语法。
```

**C2. 语气强度（Critical）**

```rst
英文：You must set this parameter.
❌ 错误：你需要设置此参数。（must → 需要，弱化）
✅ 正确：你必须设置此参数。

英文：This is required.
❌ 错误：这是建议的。（required → 建议，严重弱化）
✅ 正确：这是必需的。

英文：Not allowed in production.
❌ 错误：不建议在生产环境使用。（not allowed → 不建议）
✅ 正确：不允许在生产环境使用。
```

**C3. 条件与前提（Major）**

```rst
英文：If configured, this feature will auto-enable.
❌ 错误：此功能将自动启用。（遗漏了 if configured 条件）
✅ 正确：如已配置，此功能将自动启用。

英文：When enabled, call this method.
❌ 错误：调用此方法。（遗漏了 when enabled 前提）
✅ 正确：启用后调用此方法。

英文：Unless specified, the default is used.
❌ 错误：使用默认值。（遗漏了 unless）
✅ 正确：除非另有指定，使用默认值。
```

**C4. 技术细节（Critical）**

```rst
英文：Returns null if not found.
❌ 错误：找不到返回空。（null 被模糊化）
✅ 正确：未找到时返回 null。

英文：Set timeout to 60 seconds.
❌ 错误：设置超时。（遗漏 60 seconds）
✅ 正确：设置 60 秒超时。

英文：The $id parameter (int) must be positive.
❌ 错误：参数 $id 必须为正数。（遗漏了 int 类型）
✅ 正确：参数 ``$id`` (int) 必须为正数。
```

**信息遗漏检查清单**：
- [ ] 版本/时间限定：`4.3 or later`、`before 4.0`、`since 4.2`
- [ ] 语气强度：`must`（必须）、`should`（应该）、`only`（仅）、`required`（必需）、`not allowed`（不允许）
- [ ] 条件与前提：`if`（如果）、`when`（当...时）、`before`（在...前）、`after`（在...后）、`unless`（除非）
- [ ] 安全警告与限制
- [ ] 数值、版本号、参数名、返回值、类型、配置键

不要补写原文没有的解释，也不要弱化或强化原意。

#### D. 中文表达规则

翻译腔是中文技术文档最常见的质量问题。以下规则的核心思路是：**中文技术文档不需要明确主语时就不需要主语，不需要代词时就不用代词，不需要指示词时就不用指示词。**

**D1. 意义驱动重写**

先理解原意，再用自然中文重写；**不要逐句硬贴英文句式**。

```rst
英文：When you need to validate user input before saving it to the database, you should use the Validation class which provides comprehensive validation rules and custom error messages that can be displayed to users.

❌ 直译腔：当你需要在使用数据库保存数据之前进行验证的时候，你应该使用 Validation 类，它提供了全面的验证规则和可以展示给用户的自定义错误消息。

✅ 重写：保存到数据库前如需验证用户输入，应使用 Validation 类。该类提供全面的验证规则和自定义错误消息。
```

**D2. 消除冗余代词（最重要）**

这是翻译腔的根源。英文习惯用代词指代，中文技术文档通常不需要。以下逐类列出常见模式。

**D2a. 删除“你/你的/你们”**

英文技术文档用“you”作为泛指读者，中文不需要这个代词。

| 模式 | ❌ 翻译腔 | ✅ 地道中文 |
|------|----------|-----------|
| You can use... | 你可以使用... | 可使用... / 使用... |
| You should... | 你应该... | 应... / 应该... |
| You must... | 你必须... | 必须... |
| You may want to... | 你可能想要... | 如需...可... |
| You will need to... | 你将需要... | 需要... |
| Your data | 你的数据 | 数据 |
| Your application | 你的应用 | 应用 |
| Your project | 你的项目 | 项目 |
| Your configuration | 你的配置 | 配置 |
| If you have... | 如果你有... | 如有... / 如果有... |
| When you call... | 当你调用...时 | 调用...时 |
| Once you set... | 一旦你设置了... | 设置...后 |

**D2b. 删除“它/它们/其”**

英文用 it/they/its 指代前文提到的事物，中文技术文档通常省略或直接用名词。

| 模式 | ❌ 翻译腔 | ✅ 地道中文 |
|------|----------|-----------|
| It provides... | 它提供了... | 提供... |
| It returns... | 它返回... | 返回... |
| It allows... | 它允许... | 允许... / 支持... |
| It will... | 它会... | 将... / 会... |
| Its value | 它的值 | 值 |
| Its configuration | 它的配置 | 配置 |
| They are used to... | 它们被用于... | 用于... |

**D2c. 慎用“这/这个/这些/该”**

“这/该”不是完全禁用，但**每出现一次都要审视是否真的需要**。

| 模式 | ❌ 翻译腔 | ✅ 地道中文 |
|------|----------|-----------|
| This allows... | 这允许... | 允许... / 由此可... |
| This means... | 这意味着... | 即... / 也就是说... |
| This method... | 这个方法... | 此方法... |
| This feature... | 这个功能... | 此功能... |
| This process... | 这个过程... | 该过程... / 过程... |
| This case... | 这种情况下 | 此情况... / ...时 |

**D2d. 删除冗余的“的”**

中文技术文档中，“的”字经常被不必要地保留。

| 模式 | ❌ 翻译腔 | ✅ 地道中文 |
|------|----------|-----------|
| The configuration of... | ...的配置 | ...配置 |
| Available options | 可用的选项 | 可用选项 |
| The returned value | 返回了的值 | 返回值 |

**D3. 中英文间距**

中文与英文/数字之间加**半角空格**；数字与单位**不加空格**。

```rst
❌ 错误：CodeIgniter4
✅ 正确：CodeIgniter 4

❌ 错误：HTTP请求
✅ 正确：HTTP 请求

❌ 错误：50 ms
✅ 正确：50ms
```

**D4. 标点规范**

中文句子使用**全角标点**。

**D5. 拆分长句 + 主动语态 + 动词化**

超长英文句（>25词）优先拆成 2–3 个中文短句；优先动词化表达，减少“进行……的……”和被动语态。

```rst
英文：Data is validated before being saved to the database.
❌ 被动：数据在被保存到数据库之前被验证。
✅ 主动：保存到数据库前先验证数据。
```

**D6. 恰当处理英文后置定语与从句（防范长句嵌套）**

英文常使用 `that/which/who/where` 引导的后置定语从句。翻译时应根据从句长度灵活处理：
- **短从句**：可自然转化为中文的前置定语，保持句子紧凑。
- **长从句或嵌套从句**：**严禁**直译为冗长的“……的”前置定语。应将其拆分为并列短句，或转化为条件状语。

```rst
英文：It returns an array that contains all the user profiles.
❌ 翻译腔（带多余代词）：它返回一个包含了所有用户信息的数组。
❌ 错误拆分（太零碎）：返回一个数组，包含所有用户信息。
✅ 地道中文（短定语）：返回一个包含所有用户信息的数组。

英文：The push() method is used to push a new value onto a session value that is an array.
❌ 翻译腔（长/生硬定语）：将新值推入为数组的 Session 值中。
✅ 地道中文（转条件）：如果 Session 值是数组，可使用 push() 方法追加新值。
✅ 地道中文（拆分）：push() 方法用于向数组类型的 Session 值中添加新元素。
```

#### E. 术语与译名

优先遵循项目现有中文用户指南；同一文档内必须保持一致。翻译时遇到以下术语必须使用标准译法：

**核心框架术语（强制一致）**

| 英文 | 中文 | 说明 |
|------|------|------|
| helper | 辅助函数 | ❌ 禁止：帮助函数、助手函数 |
| controller | 控制器 | ❌ 禁止：控制者、控制器类 |
| model | 模型 | 指 MVC 中的 Model 层 |
| view | 视图 | 指 MVC 中的 View 层 |
| route / routing | 路由 | 动词/名词统一 |
| filter(s) | 过滤器 | 指 HTTP 过滤器 |
| migration(s) | 迁移 | 概念语境下不用"迁移文件" |
| validation | 验证 | ❌ 禁止：校验、合法性检查 |
| config / configuration | 配置 | 名词/动词统一 |
| library | 库 | 语境依赖，不强制统一 |
| middleware | 中间件 | 标准技术译法 |
| request | 请求 | HTTP 请求 |
| response | 响应 | HTTP 响应 |
| session | 会话 | PHP Session 机制 |
| cookie | Cookie | 不翻译 |
| cache / caching | 缓存 | 动词/名词统一 |
| database | 数据库 | 不缩写为 DB |
| query | 查询 | 数据库查询 |
| entity | 实体 | 数据实体 |
| repository | 仓库 | 仓储模式 |
| HTTP header | HTTP 标头 | ❌ 禁止：HTTP 头、头部 |

**补充约束**：

- CodeIgniter 类名、方法名、常量、配置键一律保留英文
- `library` 不做单一死板映射：优先沿用当前章节或现有文档的既有译法；若无既有上下文，再按项目约定判断
- 类名翻译时与中文字符间加空格：`Session 类`、`Config 实例`

#### F. 翻译执行步骤（在心里执行，不输出过程）

**步骤 1：通读理解**
- 先完整阅读整段/整节，理解核心语义和逻辑关系。

**步骤 2：抽取信息点**
- 标记所有必须保留的信息：版本限定、条件、限制、步骤、例外、警告、数值、参数名。

**步骤 3：中文重组**
- 用自然中文重新组织，不要硬贴英文句式。
- 遇到 `that is... / which is...` 等后置定语，**坚决拆分为短句或转化为条件句**，拒绝超长前置定语。
- 删除冗余代词，优先主动语态和动词化表达。

**步骤 4：格式保护**
- 确保 reST 指令、角色、代码块、字面量等原样保留。

**步骤 5：逐项核对**
- 对照英文原文，检查“条件、限制、版本限定”是否遗漏，代码、字面量是否被误译。

**步骤 6：消除翻译腔（关键步骤）**
- 逐句检查是否有“你/你的/它/它们/这/这个/这些”。
- 遇到“这允许/这意味着/这将”改为“可/即/将”。
- 遇到“你可以/你应该”删除“你”；遇到“它会/它返回”删除“它”。
- 删除不必要的“的”字（“X的配置”→“X配置”）。

**步骤 7：术语和排版检查**
- 确认标准术语、中英文空格、全角标点、标题装饰线长度。

### 3. 运行 guard

翻译完成后立即运行：

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/validate-rst.py" --no-build "$FILE_PATH"
```

如果失败，先修复格式问题，再重复执行，直到 guard 通过。

### 4. 进行静态审查

审查目标不是“只生成一份报告”，而是驱动修订并最终定稿。审查必须以 `$FILE_PATH.en.bak` 为英文对照源。

**审查重点与检查方法**：

| 检查项 | 检查方法 | 问题级别 |
|--------|----------|----------|
| **reST 元素** | 搜索中文指令名/角色名，检查双冒号 | Critical |
| **代码块/限定词** | 检查代码是否被翻译，only/must 等限制词是否遗漏 | Critical |
| **术语一致性** | 搜索 helper/controller/validation 等关键术语 | Major |
| **翻译腔-代词** | 扫描“你可以/你应该/你的/它会/它的/这允许”等模式 | Major |
| **翻译腔-长定语** | 检查是否有从句直译导致的“为……的”、“用于……的”冗长嵌套 | Major |
| **排版规范** | 检查中英文间距、连续“的”字 | Minor |

**快速问题定位模式**：

```bash
# 格式破坏（Critical）
grep -n "\.\. 注意::\|\.\. 警告::" "$FILE_PATH"        # 中文指令
grep -n "：文档：\|：方法：" "$FILE_PATH"              # 中文角色
grep -n "：：$\|：$" "$FILE_PATH"                      # 冒号错误

# 翻译腔扫描（Major，重点扫描）
grep -n "你可以\|你应该\|你的\|你要\|你将" "$FILE_PATH"      # 你/你的
grep -n "它会\|它返回\|它提供\|它们\|它的" "$FILE_PATH"       # 它/它们
grep -n "这允许\|这意味着\|这将\|这是因为" "$FILE_PATH"      # 这...
grep -n "为.*的\|是一个.*的" "$FILE_PATH"                # 潜在的直译长定语/从句嵌套
```

### 5. 审查报告格式

以 Markdown 输出，必须包含：总体结论、Critical 风险、Major 风险、Minor 风险、术语快照、格式扫描摘要。
每条具体问题需给出：**位置、原文、译文、问题、建议、影响**。

### 6. 按报告修订并复验

- 只要还有 Critical 或 Major，就必须继续修订 `$FILE_PATH`
- 每轮修订后都要重新运行 guard 并再次审查，直到无严重问题。

### 7. 定稿与收尾

定稿条件：guard 通过，审查无 Critical / Major，译文术语一致、表达自然无长定语嵌套。
完成后删除备份：`rm -f "$FILE_PATH.en.bak"`

## 翻译质量快速检查清单（翻译完成后自查）

提交前逐项勾选：

**格式安全（Critical）**
- [ ] 所有 `.. directive::` 指令名和 `:role:` 角色名保持英文
- [ ] 段落结尾 `::` 未改为中文冒号
- [ ] 代码块内容和 ``...`` 字面量完全未翻译

**信息完整（Critical）**
- [ ] 版本限定词（or later / only）、语气强度（must）完整
- [ ] 条件和前提（if/when/unless）完整
- [ ] 技术细节（数值、参数名、类型、返回值）未遗漏

**术语一致（Major）**
- [ ] helper → 辅助函数；controller → 控制器；validation → 验证
- [ ] 类名/方法名/配置键保留英文

**中文表达（Major/Minor）**
- [ ] **已将 `that is...` 等英文定语从句拆分为短句或条件状语，无冗长嵌套**
- [ ] 无“你/你的/它/它们/这/这个”等冗余代词或指示词
- [ ] 中英文间有空格，数字与单位无空格，使用全角标点
- [ ] 长句已拆分，无连续“的”字

## 输出要求

- 默认只给用户简短结果摘要：已翻译、guard 是否通过、是否经过修订、是否还有残留风险。
- **不要**把内部翻译步骤或长篇分析全部回贴给用户。
- 仅当仍有未解决风险，或用户明确要求时，再附上完整审查报告。
- 不要声称“已构建 / 已运行”，除非真正执行了对应命令。

## 参考资源

**翻译前必读**：
1. `examples/translation-examples.md` — 翻译正例对照
2. `examples/common-errors.md` — 错误模式库（格式破坏、翻译腔、长句嵌套）
3. `templates/detailed-report.md` — 审查报告模板
4. `examples/review-report-example.md` — 完整审查报告示例
