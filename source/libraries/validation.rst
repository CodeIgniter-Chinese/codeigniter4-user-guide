.. _validation:

##########
数据验证
##########

CodeIgniter 提供了全面的数据验证类，帮助你减少需要编写的代码量。

.. contents::
    :local:
    :depth: 2

********
概述
********

在解释 CodeIgniter 的数据验证方法之前，我们先描述理想场景：

#. 显示表单。
#. 填写并提交表单。
#. 如果提交了无效内容，或可能遗漏了必填项，表单会重新显示包含你的数据和描述问题的错误信息。
#. 此过程持续直到提交有效表单。

在接收端，脚本必须：

#. 检查必填数据。
#. 验证数据类型正确并符合正确标准。例如，如果提交用户名，必须验证其仅包含允许字符。必须满足最小长度且不超过最大长度。用户名不能是他人已存在的用户名，甚至可能是保留字等。
#. 对数据进行安全过滤。
#. 必要时预处理数据格式。
#. 准备数据以便插入数据库。

尽管上述过程并不复杂，但通常需要大量代码，并且为了显示错误信息，通常会在表单 HTML 中放置各种控制结构。表单验证虽然创建简单，但实现起来通常非常混乱和繁琐。

************************
表单验证教程
************************

以下是实现 CodeIgniter 表单验证的实践教程。

要实现表单验证，你需要三样东西：

#. 包含表单的 :doc:`视图 </outgoing/views>` 文件。
#. 包含成功提交后显示的 "成功" 信息的视图文件。
#. 接收和处理提交数据的 :doc:`控制器 </incoming/controllers>` 方法。

让我们以会员注册表单为例创建这三个内容。

表单
========

使用文本编辑器创建名为 **signup.php** 的表单。在其中放置以下代码并保存到 **app/Views/** 文件夹::

    <html>
    <head>
        <title>我的表单</title>
    </head>
    <body>

        <?= validation_list_errors() ?>

        <?= form_open('form') ?>

            <h5>用户名</h5>
            <input type="text" name="username" value="<?= set_value('username') ?>" size="50">

            <h5>密码</h5>
            <input type="text" name="password" value="<?= set_value('password') ?>" size="50">

            <h5>确认密码</h5>
            <input type="text" name="passconf" value="<?= set_value('passconf') ?>" size="50">

            <h5>邮箱地址</h5>
            <input type="text" name="email" value="<?= set_value('email') ?>" size="50">

            <div><input type="submit" value="提交"></div>

        <?= form_close() ?>

    </body>
    </html>

成功页面
================

使用文本编辑器创建名为 **success.php** 的表单。在其中放置以下代码并保存到 **app/Views/** 文件夹::

    <html>
    <head>
        <title>我的表单</title>
    </head>
    <body>

        <h3>你的表单已成功提交！</h3>

        <p><?= anchor('form', '再试一次！') ?></p>

    </body>
    </html>

控制器
==============

使用文本编辑器创建名为 **Form.php** 的控制器。在其中放置以下代码并保存到 **app/Controllers/** 文件夹：

.. literalinclude:: validation/001.php

.. note:: 自 v4.3.0 起可使用 :ref:`$this->request->is() <incomingrequest-is>` 方法。在早期版本中，需使用 ``if (strtolower($this->request->getMethod()) !== 'post')``。

.. note:: :ref:`$this->validator->getValidated() <validation-getting-validated-data>` 方法自 v4.4.0 起可用。

路由
==========

然后在 **app/Config/Routes.php** 中添加控制器的路由：

.. literalinclude:: validation/039.php
   :lines: 2-

尝试运行！
==========

要测试表单，使用类似以下 URL 访问你的站点::

    example.com/index.php/form/

如果提交表单，你应会看到表单重新加载。这是因为你尚未在 :ref:`controller-validatedata` 中设置任何验证规则。

``validateData()`` 是控制器中的一个方法，它在内部使用 **验证类**。详见 :ref:`controller-validatedata`。

.. note:: 由于尚未告知 ``validateData()`` 方法验证任何内容，默认情况下它会返回 false（布尔值）。只有当所有规则成功应用且未失败时，``validateData()`` 方法才会返回 true。

说明
===========

你会注意到上述页面的一些特点。

signup.php
----------

表单（**signup.php**）是标准网页表单，但有几点例外：

#. 使用 :doc:`表单辅助函数 </helpers/form_helper>` 创建表单开头和结尾。技术上这不是必需的，你可以使用标准 HTML 创建表单。但使用辅助函数的优点是根据配置中的 URL 生成 action URL，提高应用在 URL 变更时的可移植性。
#. 在表单顶部你会注意到以下函数调用::

    <?= validation_list_errors() ?>

   此函数返回验证器返回的所有错误信息。若无信息则返回空字符串。

Form.php
--------

控制器（**Form.php**）有一个属性 ``$helpers``，它加载视图文件使用的表单辅助函数。

控制器有一个方法 ``index()``。当非 POST 请求时返回 **signup** 视图显示表单。否则使用控制器提供的 :ref:`controller-validatedata` 方法运行验证流程。根据验证结果展示表单或成功页面。

添加验证规则
====================

然后在控制器（**Form.php**）中添加验证规则：

.. literalinclude:: validation/002.php
   :lines: 2-

提交表单后，你将看到成功页面或带有错误信息的表单。

*********************
验证配置
*********************

.. _validation-traditional-and-strict-rules:

传统规则与严格规则
============================

CodeIgniter 4 有两种验证规则类。

默认规则类（**严格规则**）使用命名空间 ``CodeIgniter\Validation\StrictRules``，提供严格验证。

传统规则类（**传统规则**）使用命名空间 ``CodeIgniter\Validation``，仅为向后兼容保留。它们可能无法正确验证非字符串值，新项目无需使用。

.. note:: 自 v4.3.0 起默认使用 **严格规则** 以提高安全性。

严格规则
------------

.. versionadded:: 4.2.0

**严格规则** 不使用隐式类型转换。

传统规则
-----------------

.. important:: 传统规则仅为向后兼容存在。新项目请勿使用。即使已在使用的项目也建议切换至严格规则。

.. warning:: 当验证包含非字符串值（如 JSON 数据）时，应使用 **严格规则**。

**传统规则** 隐式假设验证的是字符串值，输入值可能隐式转换为字符串。这对大多数基本用例（如验证 POST 数据）有效。

但例如使用 JSON 输入数据时，可能是布尔/空/数组类型。用传统规则验证布尔 ``true`` 会转换为字符串 ``'1'``。用 ``integer`` 规则验证时，``'1'`` 会通过验证。

使用传统规则
-----------------------

.. warning:: **传统规则** 仅为向后兼容保留。新项目不建议使用，可能无法正确验证非字符串值。

若要使用传统规则，需修改 **app/Config/Validation.php** 中的规则类：

.. literalinclude:: validation/003.php

*******************
加载库
*******************

验证库作为名为 **validation** 的服务加载：

.. literalinclude:: validation/004.php
   :lines: 2-

这段代码会自动加载 ``Config\Validation`` 文件，其中包含用于引入多个规则集的设置以及可轻松复用的规则集合。

.. note:: 你可能永远不需要使用此方法，因为 :doc:`控制器 </incoming/controllers>` 和 :doc:`模型 </models/model>` 都提供了简化验证的方法。

********************
验证的工作原理
********************

- 验证过程永不更改待验证数据。
- 根据设置的验证规则依次检查每个字段。若任何规则返回 false，该字段检查即终止。
- 格式规则不允许空字符串。若要允许空字符串，需添加 ``permit_empty`` 规则。
- 若待验证数据中不存在某字段，其值视为 ``null``。要检查字段是否存在，需添加 ``field_exists`` 规则。

.. note:: ``field_exists`` 规则自 v4.5.0 起可用。

************************
设置验证规则
************************

CodeIgniter 允许为字段设置多个验证规则并按顺序级联。要设置验证规则，需使用 ``setRule()``、``setRules()`` 或 ``withRequest()`` 方法。

设置单个规则
=====================

setRule()
---------

此方法设置单个规则，方法签名为::

    setRule(string $field, ?string $label, array|string $rules[, array $errors = []])

``$rules`` 接受管道分隔的规则列表或规则数组：

.. literalinclude:: validation/005.php
   :lines: 2-

传递给 ``$field`` 的值必须与发送的数据数组键名匹配。若数据直接来自 ``$_POST``，则必须与表单输入名称完全匹配。

.. warning:: v4.2.0 之前，此方法的第三个参数 ``$rules`` 类型限定为 ``string``。v4.2.0 及之后版本移除了类型限定以支持数组。为避免扩展类中重写此方法时破坏 LSP，子类方法也应移除类型限定。

设置多个规则
======================

setRules()
----------

类似 ``setRule()``，但接受字段名和规则的数组：

.. literalinclude:: validation/006.php
   :lines: 2-

要设置带标签的错误信息：

.. literalinclude:: validation/007.php
   :lines: 2-

.. note:: ``setRules()`` 会覆盖之前设置的规则。要为现有规则集添加多个规则，需多次使用 ``setRule()``。

.. _validation-dot-array-syntax:

为数组数据设置规则
============================

若数据是嵌套关联数组，可使用 "点数组语法" 轻松验证：

.. literalinclude:: validation/009.php
   :lines: 2-

可使用通配符 ``*`` 匹配数组的任意一级：

.. literalinclude:: validation/010.php
   :lines: 2-

.. note:: v4.4.4 之前存在 bug，通配符 ``*`` 会错误验证数据维度。详见 :ref:`升级指南 <upgrade-444-validation-with-dot-array-syntax>`。

"点数组语法" 对单维数组数据也很有用。例如多选下拉返回的数据：

.. literalinclude:: validation/011.php
   :lines: 2-

.. _validation-withrequest:

withRequest()
=============

.. important:: 此方法仅为向后兼容存在。新项目请勿使用。即使已在使用，也建议改用其他更合适的方法。

.. warning:: 若仅需验证 POST 数据，请勿使用 ``withRequest()``。此方法使用 :ref:`$request->getVar() <incomingrequest-getting-data>`，根据 php.ini 的 `request-order <https://www.php.net/manual/zh/ini.core.php#ini.request-order>`_ 返回 ``$_GET``、``$_POST`` 或 ``$_COOKIE`` 数据（按顺序）。新值覆盖旧值。若同名，Cookie 可能覆盖 POST 值。

最常见的验证场景是验证来自 HTTP 请求的输入数据。若需要，可传递当前 Request 对象实例，它会将所有输入数据设为待验证数据：

.. literalinclude:: validation/008.php
   :lines: 2-

.. warning:: 使用此方法时，应使用 :ref:`getValidated() <validation-getting-validated-data>` 获取已验证数据。因为此方法在处理 JSON 请求（``Content-Type: application/json``）时通过 :ref:`$request->getJSON() <incomingrequest-getting-json-data>` 获取 JSON 数据，或处理非表单提交的 PUT、PATCH、DELETE 请求时通过 :ref:`$request->getRawInput() <incomingrequest-retrieving-raw-data>` 获取原始数据，攻击者可能改变验证数据。

.. note:: :ref:`getValidated() <validation-getting-validated-data>` 方法自 v4.4.0 起可用。

***********************
使用验证
***********************

运行验证
==================

``run()`` 方法运行验证，方法签名为::

    run(?array $data = null, ?string $group = null, ?string $dbGroup = null): bool

``$data`` 是待验证数据数组。可选参数 ``$group`` 是要应用的 :ref:`预定义规则组 <validation-array>`。可选参数 ``$dbGroup`` 是使用的数据库组。

验证成功时返回 true。

.. literalinclude:: validation/043.php
   :lines: 2-

运行多次验证
============================

.. note:: ``run()`` 方法不会重置错误状态。若前次运行失败，``run()`` 将始终返回 false，且 ``getErrors()`` 返回所有先前错误直到显式重置。

若需运行多次验证（例如不同数据集或不同规则），可能需要在每次运行前调用 ``$validation->reset()`` 清除先前错误。注意 ``reset()`` 会清空之前设置的任何数据、规则或自定义错误，因此需重复调用 ``setRules()``、``setRuleGroup()`` 等：

.. literalinclude:: validation/019.php
   :lines: 2-

验证单个值
==================

``check()`` 方法根据规则验证单个值。第一个参数 ``$value`` 是待验证值，第二个参数 ``$rule`` 是验证规则，可选第三个参数 ``$errors`` 是自定义错误信息。

.. literalinclude:: validation/012.php
   :lines: 2-

.. note:: v4.4.0 之前，此方法的第二个参数 ``$rule`` 类型限定为 ``string``。v4.4.0 及之后版本移除了类型限定以支持数组。

.. note:: 此方法内部调用 ``setRule()`` 设置规则。

.. _validation-getting-validated-data:

获取已验证数据
======================

.. versionadded:: 4.4.0

实际已验证数据可通过 ``getValidated()`` 方法获取。此方法返回仅包含通过验证规则的元素数组。

.. literalinclude:: validation/044.php
   :lines: 2-

.. literalinclude:: validation/045.php
   :lines: 2-

.. _saving-validation-rules-to-config-file:

将验证规则保存到配置文件
==================================================

验证类的一个优点是可以将所有应用的验证规则存储在配置文件中。你可以将规则组织成"组"，每次运行验证时指定不同组。

.. _validation-array:

如何保存规则
----------------------

要存储验证规则，只需在 ``Config\Validation`` 类中创建新的公共属性，属性名即组名。该元素将保存包含验证规则的数组。如前所示，验证数组原型如下：

.. literalinclude:: validation/013.php

如何指定规则组
-------------------------

调用 ``run()`` 方法时指定要使用的组：

.. literalinclude:: validation/014.php
   :lines: 2-

如何保存错误信息
--------------------------

也可在配置文件中通过创建与组同名并附加 ``_errors`` 的属性来存储自定义错误信息。使用该组时会自动应用这些错误信息：

.. literalinclude:: validation/015.php

或通过数组传递所有设置：

.. literalinclude:: validation/016.php

数组格式详见 :ref:`validation-custom-errors`。

获取和设置规则组
-----------------------------

获取规则组
^^^^^^^^^^^^^^

此方法从验证配置获取规则组：

.. literalinclude:: validation/017.php
   :lines: 2-

设置规则组
^^^^^^^^^^^^^^

此方法将验证配置中的规则组设置到验证服务：

.. literalinclude:: validation/018.php
   :lines: 2-

.. _validation-placeholders:

验证占位符
=======================

验证类提供了一种基于传入数据替换规则部分内容的简便方法。这听起来可能有些晦涩，但在使用 ``is_unique`` 验证规则时特别有用。

占位符是用花括号包裹的传入数据字段名（或数组键）。它将被匹配传入字段的 **值** 替换。以下示例可阐明此概念：

.. literalinclude:: validation/020.php
   :lines: 2-

.. warning:: 自 v4.3.5 起，出于安全考虑必须为占位符字段（上例中的 ``id`` 字段）设置验证规则。因为攻击者可能向应用发送任意数据。

在此规则集中，声明邮箱地址应在数据库中唯一，除了 id 与占位符值匹配的行。假设表单 POST 数据如下：

.. literalinclude:: validation/021.php
   :lines: 2-

则 ``{id}`` 占位符会被替换为数字 **4**，形成调整后的规则：

.. literalinclude:: validation/022.php
   :lines: 2-

因此验证邮箱唯一性时将忽略数据库中 ``id=4`` 的行。

.. note:: 自 v4.3.5 起，若占位符（如 ``id``）值未通过验证，占位符将不被替换。

只要确保传入的动态键名不与表单数据冲突，这也可用于在运行时创建更动态的规则。

*******************
处理错误
*******************

验证库提供多种方法帮助你设置错误信息、提供自定义错误信息及获取一个或多个错误信息用于显示。

默认情况下，错误信息来自 **system/Language/en/Validation.php** 中的语言字符串，每个规则对应一个条目。若要更改默认信息，可创建 **app/Language/en/Validation.php** 文件（和/或对应语言环境文件夹），并在其中放置要修改的错误信息键值对。

.. _validation-custom-errors:

设置自定义错误信息
=============================

``setRule()`` 和 ``setRules()`` 方法均可接受自定义错误信息数组作为最后一个参数，为每个字段提供特定错误信息。若未提供自定义信息，则使用默认值。

有两种方式提供自定义错误信息：

作为最后一个参数：

.. literalinclude:: validation/023.php
   :lines: 2-

或标签式：

.. literalinclude:: validation/024.php
   :lines: 2-

若要在信息中包含字段"人类可读"名称、规则允许的可选参数（如 max_length）或验证值，可在信息中添加 ``{field}``、``{param}`` 和 ``{value}`` 标签::

    'min_length' => '提供的值 ({value}) 对于 {field} 必须至少 {param} 个字符。'

对于人类名称为"用户名"、规则为 ``min_length[6]``、值为 "Pizza" 的字段，错误信息将显示："提供的值 (Pizza) 对于用户名必须至少 6 个字符。"

.. warning:: 通过 ``getErrors()`` 或 ``getError()`` 获取错误信息时，信息未进行 HTML 转义。若使用用户输入数据（如 ``{value}``）生成错误信息，可能包含 HTML 标签。若未转义直接显示，可能导致 XSS 攻击。

.. note:: 使用标签式错误信息时，若传递第二个参数给 ``setRules()``，它会被第一个参数的值覆盖。

信息与验证标签的翻译
=============================================

要使用语言文件中的翻译字符串，可使用点语法。假设翻译文件位于 **app/Languages/en/Rules.php**，可如下使用定义的语言行：

.. literalinclude:: validation/025.php
   :lines: 2-

.. _validation-getting-all-errors:

获取所有错误
==================

要获取所有失败字段的错误信息，可使用 ``getErrors()`` 方法：

.. literalinclude:: validation/026.php
   :lines: 2-

若无错误，返回空数组。

使用通配符（``*``）时，错误将指向特定字段，用相应键替换星号::

    // 数据
    'contacts' => [
        'friends' => [
            [
                'name' => 'Fred Flinstone',
            ],
            [
                'name' => '',
            ],
        ]
    ]

    // 规则
    'contacts.friends.*.name' => 'required'

    // 错误为
    'contacts.friends.1.name' => 'contacts.friends.*.name 字段是必填项。'

获取单个错误
======================

可用 ``getError()`` 方法获取单个字段错误。唯一参数是字段名：

.. literalinclude:: validation/027.php
   :lines: 2-

若无错误，返回空字符串。

.. note:: 使用通配符时，所有匹配通配符的错误将合并为一行，用换行符分隔。

检查是否存在错误
=====================

可用 ``hasError()`` 方法检查是否存在错误。唯一参数是字段名：

.. literalinclude:: validation/028.php
   :lines: 2-

指定带通配符的字段时，检查所有匹配错误：

.. literalinclude:: validation/029.php
   :lines: 2-

.. _validation-redirect-and-validation-errors:

重定向与验证错误
==============================

PHP 请求间不共享数据。因此若验证失败后重定向，新请求中不会有验证错误，因为验证在上次请求中运行。

此时需使用表单辅助函数 :php:func:`validation_errors()`、:php:func:`validation_list_errors()` 和 :php:func:`validation_show_error()`。这些函数检查存储在会话中的验证错误。

要将验证错误存入会话，需将 ``withInput()`` 与 :php:func:`redirect() <redirect>` 结合使用：

.. literalinclude:: validation/042.php
   :lines: 2-

.. _validation-customizing-error-display:

*************************
自定义错误显示
*************************

调用 ``$validation->listErrors()`` 或 ``$validation->showError()`` 时，会在后台加载视图文件决定错误显示方式。默认情况下，用 ``errors`` class 包裹 div。可轻松创建新视图并在应用中复用。

创建视图
==================

第一步是创建自定义视图。这些视图可放在 ``view()`` 方法能定位的任何位置，如标准视图目录或命名空间视图文件夹。例如，可在 **app/Views/_errors_list.php** 创建新视图：

.. literalinclude:: validation/030.php

视图中可用 ``$errors`` 数组包含错误列表，键为字段名，值为错误信息：

.. literalinclude:: validation/031.php
   :lines: 2-

实际上有两种视图类型。第一种包含所有错误数组，如前所述。第二种更简单，仅包含单个变量 ``$error``，用于 ``showError()`` 方法指定字段时::

    <span class="help-block"><?= esc($error) ?></span>

配置
=============

创建视图后，需让验证库知晓这些视图。打开 **app/Config/Validation.php** 文件，你会找到 ``$templates`` 属性。在此可以列出任意数量的自定义视图，并为其指定可引用的简短别名。如果添加上文示例文件，配置示例如下：

.. literalinclude:: validation/032.php

指定模板
=======================

通过别名指定模板作为 ``listErrors()`` 的第一个参数::

    <?= $validation->listErrors('my_list') ?>

显示字段特定错误时，可将别名作为 ``showError()`` 的第二个参数::

    <?= $validation->showError('username', 'my_single') ?>

*********************
创建自定义规则
*********************

.. _validation-using-rule-classes:

使用规则类
==================

规则存储在简单的命名空间类中，只要自动加载器能找到即可。这些文件称为规则集。

添加规则集
----------------

要添加新规则集，请编辑 **app/Config/Validation.php** 文件并将新文件加入 ``$ruleSets`` 数组：

.. literalinclude:: validation/033.php

可通过两种方式添加：使用完全限定类名的字符串形式，或如示例所示使用 ``::class`` 后缀。使用 ``::class`` 后缀的主要优势是在高级 IDE 中能提供额外的导航功能。

创建规则类
---------------------

在该文件内，每个方法即代表一条规则，必须将待验证值作为第一个参数，且必须返回布尔值 true 或 false 表示验证是否通过：

.. literalinclude:: validation/034.php

默认情况下，系统会在 **system/Language/en/Validation.php** 中查找错误信息使用的语言字符串。要为自定义规则提供默认错误信息，可将其置于 **app/Language/en/Validation.php** （和/或替代 ``en`` 的其他语言环境对应文件夹）。若需使用默认 **Validation.php** 之外的其他语言文件，可通过在第二个参数（若规则需要处理参数，则为第四个参数）以引用方式接受 ``&$error`` 变量来提供错误信息：

.. literalinclude:: validation/035.php

使用自定义规则
-------------------

新自定义规则可像其他规则一样使用：

.. literalinclude:: validation/036.php
   :lines: 2-

允许参数
-------------------

若方法需要参数，函数至少需要三个参数：

1. 待验证值（``$value``）
2. 参数字符串（``$params``）
3. 表单提交的所有数据数组（``$data``）
4. （可选）自定义错误字符串（``&$error``）

.. warning:: ``$data`` 中的字段值未经验证（或可能无效）。使用未验证输入数据是漏洞来源。在使用数据前必须在自定义规则中执行必要验证。

``$data`` 数组对于像 ``required_with`` 这样需要检查其他字段值的规则特别有用：

.. literalinclude:: validation/037.php

.. _validation-using-closure-rule:

使用闭包规则
==================

.. versionadded:: 4.3.0

若自定义规则仅需在应用中使用一次，可使用闭包代替规则类。

需为验证规则使用数组：

.. literalinclude:: validation/040.php
   :lines: 2-

必须为闭包规则设置错误信息。指定错误信息时，需设置闭包规则的数组键。上例中，``required`` 规则键为 ``0``，闭包为 ``1``。

或使用以下参数：

.. literalinclude:: validation/041.php
   :lines: 2-

.. _validation-using-callable-rule:

使用可调用规则
===================

.. versionadded:: 4.5.0

若想用数组回调作为规则，可替代闭包规则。

需为验证规则使用数组：

.. literalinclude:: validation/046.php
   :lines: 2-

必须为可调用规则设置错误信息。指定错误信息时，需设置可调用规则的数组键。上例中，``required`` 规则键为 ``0``，可调用规则为 ``1``。

或使用以下参数：

.. literalinclude:: validation/047.php
   :lines: 2-

.. _validation-available-rules:

***************
可用规则
***************

.. note:: 规则是一个字符串；参数之间 **不能有空格**，尤其是 ``is_unique`` 规则。``ignore_value`` 前后也不能有空格。

.. literalinclude:: validation/038.php
   :lines: 2-

.. _rules-for-general-use:

通用规则
=====================

以下是所有可用的原生规则列表：

======================= ========== ============================================= ===================================================
规则                    参数       描述                                          示例
======================= ========== ============================================= ===================================================
alpha                   否         若字段包含非 ASCII 字母字符则失败。
alpha_dash              否         若字段包含非字母数字、下划线或短横线
                                   （ASCII）则失败。
alpha_numeric           否         若字段包含非 ASCII 字母数字字符则失败。
alpha_numeric_punct     否         若字段包含非字母数字、空格或以下标点则失败：
                                   ``~`` （波浪符）、``!`` （叹号）、
                                   ``#`` （井号）、``$`` （美元符）、
                                   ``%`` （百分号）、``&`` （与符号）、
                                   ``*`` （星号）、``-`` （短横）、
                                   ``_`` （下划线）、``+`` （加号）、
                                   ``=`` （等号）、``|`` （竖线）、
                                   ``:`` （冒号）、``.`` （句点）。
alpha_numeric_space     否         若字段包含非字母数字或空格（ASCII）则失败。
alpha_space             否         若字段包含非字母或空格（ASCII）则失败。
decimal                 否         若字段包含非十进制数则失败
                                   （允许 ``+/-`` 符号）。
differs                 是         若字段值与参数字段相同则失败。                ``differs[字段名]``
exact_length            是         若字段长度不等于参数值则失败                  ``exact_length[5]`` 或 ``exact_length[5,8,12]``
                                   （支持逗号分隔多值）。
field_exists            是         若字段不存在则失败（v4.5.0 新增）。
greater_than            是         若字段值小于等于参数值或非数字则失败。        ``greater_than[8]``
greater_than_equal_to   是         若字段值小于参数值或非数字则失败。            ``greater_than_equal_to[5]``
hex                     否         若字段包含非十六进制字符则失败。
if_exist                否         仅当字段存在于验证数据中时才进行验证。
in_list                 是         若字段值不在指定列表中则失败。                ``in_list[红,蓝,绿]``
integer                 否         若字段包含非整数值则失败。
is_natural              否         若字段包含非自然数（0,1,2...）则失败。
is_natural_no_zero      否         若字段包含非自然数（1,2,3...）则失败。
is_not_unique           是         检查数据库中是否存在给定的值。                ``is_not_unique[table.field,where_field,where_value]`` 或 ``is_not_unique[dbGroup.table.field,where_field,where_value]``
                                   可以通过字段/值过滤器忽略记录
                                   （当前只接受一个过滤器）。
                                   （自 v4.6.0 版本起，你可以选择性地将
                                   dbGroup 作为参数传递。）
is_unique               是         检查字段值是否存在于数据库中。                ``is_unique[table.field,ignore_field,ignore_value]`` 或 ``is_unique[dbGroup.table.field,ignore_field,ignore_value]``
                                   可以可选地设置要忽略的列和值,
                                   在更新记录时很有用,忽略它本身。
                                   （自 v4.6.0 版本起，你可以选择性地将
                                   dbGroup 作为参数传递。）
less_than               是         若字段值大于等于参数值或非数字则失败。        ``less_than[8]``
less_than_equal_to      是         若字段值大于参数值或非数字则失败。            ``less_than_equal_to[8]``
matches                 是         值必须与参数字段值匹配。                      ``matches[字段]``
max_length              是         若字段长度超过参数值则失败。                  ``max_length[8]``
min_length              是         若字段长度短于参数值则失败。                  ``min_length[3]``
not_in_list             是         若字段值在指定列表中则失败。                  ``not_in_list[红,蓝,绿]``
numeric                 否         若字段包含非数字字符则失败。
permit_empty            否         允许字段为空数组、空字符串、null 或 false。
regex_match             是         若字段不匹配正则表达式则失败。                ``regex_match[/正则表达式/]``
required                否         若字段为空数组、空字符串、null 或
                                   false 则失败。
required_with           是         当其他任一字段非空时本字段必填。              ``required_with[字段1,字段2]``
required_without        是         当其他任一字段为空时本字段必填。              ``required_without[字段1,字段2]``
string                  否         通用字符串验证（替代 **alpha*** 系列规则）。
timezone                否         若字段不符合时区标识符则失败
                                   （基于 `timezone_identifiers_list()`_）。
valid_base64            否         若字段包含非合法 Base64 字符则失败。
valid_cc_number         是         验证信用卡号是否与指定提供程序                ``valid_cc_number[amex]``
                                   使用的格式匹配。当前支持的提供程序有：
                                   美国运通 (``amex``)、
                                   中国银联 (``unionpay``)、
                                   Diners Club CarteBlance (``carteblanche``)、
                                   Diners Club (``dinersclub``)、
                                   Discover Card (``discover``)、
                                   Interpayment (``interpayment``)、
                                   JCB (``jcb``)、 Maestro (``maestro``)、
                                   丹麦银行的 Dankort (``dankort``)、
                                   NSPK MIR (``mir``)、Troy (``troy``)、
                                   MasterCard (``mastercard``)、
                                   Visa (``visa``)、 UATP (``uatp``)、
                                   Verve (``verve``)、
                                   CIBC 便利卡 (``cibc``)、
                                   罗伊银行客户卡 (``rbc``)、
                                   TD Canada Trust 访问卡 (``tdtrust``)、
                                   Scotiabank 圣哥伦布卡 (``scotia``)、
                                   BMO 自动柜员机卡 (``bmoabm``)、
                                   HSBC 加拿大卡 (``hsbc``)
valid_date              是         如果字段不包含有效的日期，则验证失败。        ``valid_date[d/m/Y]``
                                   任何 `strtotime()`_ 接受的字符串，
                                   只要你不指定与日期格式匹配的可选参数，
                                   都是有效的。**因此，通常有必要指定参数。**
valid_email             否         若字段不符合邮箱格式则失败。
valid_emails            否         若逗号分隔列表中任一邮箱无效则失败。
valid_ip                是         如果提供的 IP 无效，则失败。                  ``valid_ip[ipv6]``
                                   接受一个可选参数 ``ipv4`` 或 ``ipv6``
                                   来指定 IP 格式。
valid_json              否         若字段非合法 JSON 字符串则失败。
valid_url               否         如果字段不包含（宽松意义上的）URL，
                                   则验证失败。包括可能作为主机名的简单字符串，
                                   例如 "codeigniter"。
                                   **通常，应该使用** ``valid_url_strict``。
valid_url_strict        是         如果字段不包含有效的 URL，则验证失败。        ``valid_url_strict[https]``
                                   你可以选择性地指定一个有效 schema 的列表。
                                   如果未指定，则 ``http,https`` 是有效的。
                                   此规则使用 PHP 的 ``FILTER_VALIDATE_URL``。
======================= ========== ============================================= ===================================================

.. note:: 你还可以使用任何返回布尔值且至少接受一个参数（待验证字段数据）的原生 PHP 函数。

.. important:: 验证库 **从不修改** 待验证数据。

.. _timezone_identifiers_list(): https://www.php.net/manual/zh/function.timezone-identifiers-list.php
.. _strtotime(): https://www.php.net/manual/zh/function.strtotime.php
.. _empty(): https://www.php.net/manual/zh/function.empty.php

.. _rules-for-file-uploads:

文件上传规则
======================

验证上传文件时，必须使用专门针对文件验证的规则。

.. important:: 只能使用下表列出的规则验证文件。若在文件验证规则数组或字符串中添加通用规则（如 ``permit_empty``），将导致文件验证失效。

由于文件上传字段的值不存在于常规数据中，而是存储在 ``$_FILES`` 全局变量，因此输入字段名需要被使用两次：一次作为常规字段名，另一次作为文件相关规则的第一个参数::

    // 在 HTML 中
    <input type="file" name="avatar">

    // 在控制器中
    $this->validateData([], [
        'avatar' => 'uploaded[avatar]|max_size[avatar,1024]',
    ]);

另见 :ref:`file-upload-form-tutorial`。

======================= ========== ============================================= ===================================================
规则                    参数       描述                                          示例
======================= ========== ============================================= ===================================================
uploaded                是         如果参数的名称与任何已上传文件的名称不匹配，  ``uploaded[字段名]``
                                   则验证失败。 如果你希望文件上传是可选的
                                   （非必需的），请不要定义此规则。
max_size                是         若文件大小超过参数值（单位 KB）或 php.ini 中  ``max_size[字段名,2048]``
                                   ``upload_max_filesize`` 限制则失败。
max_dims                是         若图片尺寸超过指定宽高则失败，参数依次为      ``max_dims[字段名,300,150]``
                                   字段名、最大宽度、最大高度。
                                   若非图片文件也会失败。
min_dims                是         若图片尺寸未达最小宽高则失败，参数依次为      ``min_dims[字段名,300,150]``
                                   字段名、最小宽度、最小高度。
                                   （此规则在 v4.6.0 版本新增）
mime_in                 是         若文件 MIME 类型不在参数列表中则失败。        ``mime_in[字段名,image/png,image/jpeg]``
ext_in                  是         若文件扩展名不在参数列表中则失败。            ``ext_in[字段名,png,jpg,gif]``
is_image                是         若文件无法被识别为图片则失败。                ``is_image[字段名]``
======================= ========== ============================================= ===================================================

文件验证规则同时适用于单文件和多文件上传场景。
