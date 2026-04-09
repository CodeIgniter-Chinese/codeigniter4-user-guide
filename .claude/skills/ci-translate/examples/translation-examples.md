# CodeIgniter 文档翻译示例对照

本文档展示典型翻译场景的正确处理方式，供翻译时参考。

## 1. reST 指令处理

### 示例 1：note/warning 指令

**英文原文**：
```rst
.. note::
   This method is deprecated and will be removed in future versions.

.. warning::
   Do not use this method in production environments.
```

**中文译文**：
```rst
.. note::
   此方法已弃用，将在未来版本中移除。

.. warning::
   不要在生产环境中使用此方法。
```

**处理要点**：
- ✅ 指令名称 `.. note::` / `.. warning::` 保持英文原样
- ✅ 指令内容（缩进文本）需要翻译
- ✅ 缩进保持完全一致

### 示例 2：code-block 指令

**英文原文**：
```rst
.. code-block:: php

    $config = new Config();
    $config->set('key', 'value');
```

**中文译文**：
```rst
.. code-block:: php

    $config = new Config();
    $config->set('key', 'value');
```

**处理要点**：
- ✅ 指令类型 `php` 保持英文
- ✅ 代码块内容**完全不翻译**
- ✅ 缩进保持严格一致（通常是 4 个空格）

---

## 2. 交叉引用处理

### 示例 3：:doc: 角色

**英文原文**：
```rst
See :doc:`incoming` for more details.
```

**中文译文**：
```rst
详见 :doc:`incoming`。
```

**处理要点**：
- ✅ 角色 `:doc:` 保持英文
- ✅ 目标 `incoming` 保持英文（这是文件名）
- ✅ 无可见文本时，直接翻译周边句子即可

### 示例 4：:meth: 角色（带可见文本）

**英文原文**：
```rst
Use the :meth:`Model::find <find>` method to retrieve data.
```

**中文译文**：
```rst
使用 :meth:`Model::find <find>` 方法获取数据。
```

**处理要点**：
- ✅ 角色名 `:meth:` 保持英文
- ✅ 目标 `find` 保持英文
- ✅ 可见文本 `Model::find` 保持英文（这是方法名）
- ✅ 翻译周边的"method"为"方法"

---

## 3. 标题与装饰线

### 示例 5：章节标题

**英文原文**：
```rst
Configuration
=============

This section covers configuration options.
```

**中文译文**：
```rst
配置
===

本节介绍配置选项。
```

**处理要点**：
- ✅ 标题文本翻译为"配置"
- ✅ 装饰符号 `=` 保持一致
- ✅ 装饰线长度 ≥ 标题长度（这里加长到 3 个字符）

### 示例 6：子章节标题

**英文原文**：
```rst
Database Settings
-----------------

Configure your database connection here.
```

**中文译文**：
```rst
数据库设置
---------

在此配置数据库连接。
```

**处理要点**：
- ✅ 标题翻译
- ✅ 装饰符号 `-` 保持不变
- ✅ 装饰线长度调整为 9 个字符（≥ "数据库设置"的 5 个中文字符）

---

## 4. 术语翻译

### 示例 7：框架组件名

**英文原文**：
```rst
The Session class provides session management.
```

**中文译文**：
```rst
Session 类提供会话管理功能。
```

**处理要点**：
- ✅ 类名 `Session` **不翻译**
- ✅ "class" 翻译为"类"
- ✅ 中英文间距：`Session 类`

### 示例 8：方法名

**英文原文**：
```rst
Call the ``find()`` method to query the database.
```

**中文译文**：
```rst
调用 ``find()`` 方法查询数据库。
```

**处理要点**：
- ✅ 方法名 `find()` **不翻译**（包括行内字面量标记）
- ✅ "method" 翻译为"方法"

### 示例 9：标准术语

**英文原文**：
```rst
Controllers handle incoming requests.
Use helpers for common tasks.
```

**中文译文**：
```rst
控制器处理传入请求。
使用辅助函数处理常见任务。
```

**处理要点**：
- ✅ "controller" → "控制器"
- ✅ "helper" → "辅助函数"

---

## 5. 中英文间距与标点

### 示例 10：间距规范

**英文原文**：
```rst
CodeIgniter4 provides Model classes.
The default timeout is 50 ms.
```

**中文译文**：
```rst
CodeIgniter 4 提供 Model 类。
默认超时时间为 50ms。
```

**处理要点**：
- ✅ 中文与英文/数字加空格：`CodeIgniter 4`、`Model 类`
- ✅ 数字与单位不加空格：`50ms`（而不是 `50 ms`）

### 示例 11：标点规范

**英文原文**：
```rst
This is a test. It works!
```

**中文译文**：
```rst
这是一个测试。它正常工作！
```

**处理要点**：
- ✅ 中文句子使用全角标点：，。！？
- ✅ 不重复标点

---

## 6. 意义驱动重写

### 示例 12：拆分长句

**英文原文**：
```rst
When you need to validate user input before saving it to the database,
you should use the Validation class which provides comprehensive validation
rules and custom error messages that can be displayed to users.
```

**中文译文（意义驱动重写）**：
```rst
保存到数据库前如需验证用户输入，应使用 Validation 类。
该类提供全面的验证规则和自定义错误消息，可展示给用户。
```

**处理要点**：
- ✅ 拆分长句（原句 35 词 → 拆为 2 句）
- ✅ 先说结论"应使用 Validation 类"，后说功能
- ✅ 信息点完整覆盖：验证、保存前、Validation 类、验证规则、错误消息、展示给用户
- ✅ 删除冗余代词"you"

### 示例 13：主动语态与动词化

**英文原文**：
```rst
The creation of the configuration file is required for proper initialization.
```

**中文译文**：
```rst
必须创建配置文件才能正确初始化。
```

**处理要点**：
- ✅ 名词化表达 "creation" → 动词"创建"
- ✅ 被动语态 → 主动语态
- ✅ 删除冗余"proper"

---

## 7. 错误案例警示

### ❌ 错误案例 A：翻译了代码

**错误译文**：
```rst
.. code-block:: php

    $配置 = new 配置();  # ❌ 翻译了变量名
    $配置->设置('键', '值');  # ❌ 翻译了方法名
```

**正确译文**：
```rst
.. code-block:: php

    $config = new Config();  # ✅ 保持英文
    $config->set('key', 'value');  # ✅ 保持英文
```

### ❌ 错误案例 B：破坏了交叉引用

**错误译文**：
```rst
详见 :文档:`incoming`。  # ❌ 翻译了角色名
```

**正确译文**：
```rst
详见 :doc:`incoming`。  # ✅ 角色名保持英文
```

### ❌ 错误案例 C：遗漏信息点

**英文原文**：
```rst
This method is only available in version 4.3 or later.
```

**错误译文**：
```rst
此方法在 4.3 版本可用。  # ❌ 遗漏了"only"和"or later"
```

**正确译文**：
```rst
此方法仅在 4.3 或更高版本中可用。  # ✅ "only" → "仅"，"or later" → "或更高版本"
```

---

## 8. 特殊场景处理

### 示例 14：表格翻译

**英文原文**：
```rst
+----------------+--------+
| Parameter      | Type   |
+================+========+
| ``$id``        | int    |
+----------------+--------+
| ``$name``      | string |
+----------------+--------+
```

**中文译文**：
```rst
+----------------+--------+
| 参数           | 类型   |
+================+========+
| ``$id``        | int    |
+----------------+--------+
| ``$name``      | string |
+----------------+--------+
```

**处理要点**：
- ✅ 表头单元格翻译："Parameter" → "参数"，"Type" → "类型"
- ✅ 参数名 `$id` / `$name` **不翻译**（包括字面量标记）
- ✅ 类型 `int` / `string` **不翻译**
- ✅ 表格对齐和分隔符保持不变

### 示例 15：列表项翻译

**英文原文**：
```rst
- First item
- Second item with code ``example()``
- Third item with reference :meth:`find`
```

**中文译文**：
```rst
- 第一项
- 包含代码 ``example()`` 的第二项
- 包含引用 :meth:`find` 的第三项
```

**处理要点**：
- ✅ 列表标记 `-` 保持不变
- ✅ 列表项内容翻译
- ✅ 字面量和交叉引用保持英文
- ✅ 缩进保持一致

---

## 9. 复杂条件句翻译

### 示例 16：多重条件句

**英文原文**：
```rst
If you need to validate user input before saving it to the database,
and the validation rules are defined in a separate configuration file,
you should use the Validation library which supports custom rules.
```

**中文译文（意义驱动重写）**：
```rst
保存到数据库前如需验证用户输入，且验证规则定义在独立配置文件中，
应使用 Validation 库（支持自定义规则）。
```

**处理要点**：
- ✅ 拆分长句为 2 个分句，用逗号连接
- ✅ 先说前提（2 个条件），后说解决方案
- ✅ 信息点完整：验证用户输入、保存前、规则在配置文件、使用 Validation 库、支持自定义规则
- ✅ 删除冗余代词"you"

---

### 示例 17：版本变更指令

**英文原文**：
```rst
.. versionadded:: 4.3.0
   The ``$newFeature`` parameter was added.

.. deprecated:: 4.2.0
   The ``$oldMethod()`` method is deprecated. Use ``$newMethod()`` instead.
```

**中文译文**：
```rst
.. versionadded:: 4.3.0
   新增 ``$newFeature`` 参数。

.. deprecated:: 4.2.0
   ``$oldMethod()`` 方法已弃用，请使用 ``$newMethod()``。
```

**处理要点**：
- ✅ 指令名保持英文（`.. versionadded::`、`.. deprecated::`）
- ✅ 版本号保持原样
- ✅ 参数名、方法名保持英文（包括字面量标记）
- ✅ 指令内容翻译，简洁清晰
- ✅ "is deprecated" → "已弃用"（主动表达）
- ✅ "Use ... instead" → "请使用..."

---

### 示例 18：多层次列表

**英文原文**：
```rst
- Main configuration options:
  - Database settings
    - Connection parameters
    - Table prefix
  - Session settings
- Security options
  - CSRF protection
  - XSS filtering
```

**中文译文**：
```rst
- 主配置选项：
  - 数据库设置
    - 连接参数
    - 表前缀
  - 会话设置
- 安全选项
  - CSRF 保护
  - XSS 过滤
```

**处理要点**：
- ✅ 列表标记和缩进层级保持一致
- ✅ 列表项内容翻译
- ✅ 技术术语保持英文（CSRF、XSS）
- ✅ 中文简洁，无冗余词汇

---

## 总结

翻译核心原则：
1. **格式优先**：reST 结构零破坏 > 术语一致性 > 中文表达优化
2. **信息完整**：零遗漏、零增添、零篡改
3. **自然表达**：意义驱动重写，删除翻译腔，主动语态优先
4. **术语统一**：框架名不翻译，标准译法强制一致

遇到不确定时：
- 代码块/字面量 → **永远不翻译**
- 类名/方法名 → **永远不翻译**
- reST 指令/角色 → **永远不翻译**
- 长句 → **拆分**
- 被动语态 → **改主动**
- 冗余代词 → **删除**
- 版本号/参数名 → **保持原样**

---

## 总结

翻译核心原则：
1. **格式优先**：reST 结构零破坏 > 术语一致性 > 中文表达优化
2. **信息完整**：零遗漏、零增添、零篡改
3. **自然表达**：意义驱动重写，删除翻译腔，主动语态优先
4. **术语统一**：框架名不翻译，标准译法强制一致

遇到不确定时：
- 代码块/字面量 → **永远不翻译**
- 类名/方法名 → **永远不翻译**
- reST 指令/角色 → **永远不翻译**
- 长句 → **拆分**
- 被动语态 → **改主动**
- 冗余代词 → **删除**