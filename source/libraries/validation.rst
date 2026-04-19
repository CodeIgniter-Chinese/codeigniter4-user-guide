.. _validation:

#############
Validation 类
#############

CodeIgniter 提供了全面的 Validation 类，帮助减少需要编写的代码量。

.. contents::
    :local:
    :depth: 2

********
概述
********

在介绍 CodeIgniter 的数据验证方法之前，先描述理想场景：

#. 显示表单。
#. 填写并提交表单。
#. 如果提交的内容无效，或者遗漏了必填项，则重新显示表单，其中包含已填写的数据以及描述问题的错误消息。
#. 此过程持续进行，直到提交有效的表单。

在处理端，脚本必须：

#. 检查必填数据。
#. 验证数据类型是否正确，是否符合条件。例如，提交的用户名必须仅包含允许的字符，必须达到最小长度，不能超过最大长度。用户名不能是已有的用户名，甚至不能是保留字。等等。
#. 对数据进行安全过滤。
#. 按需预格式化数据。
#. 为数据库插入准备数据。

虽然上述过程并不复杂，但通常需要大量代码，而且为了显示错误消息，往往需要在表单 HTML 中放置各种控制结构。表单验证虽然逻辑简单，但实现起来通常非常繁琐和枯燥。

************************
表单验证教程
************************

以下是一个"动手实践"式教程，演示如何实现 CodeIgniter 的表单验证。

要实现表单验证，需要三样东西：

#. 包含表单的 :doc:`视图 </outgoing/views>` 文件。
#. 包含 "success" 消息的视图文件，在提交成功后显示。
#. 用于接收和处理提交数据的 :doc:`控制器 </incoming/controllers>` 方法。

以会员注册表单为例，来创建这三样东西。

表单
========

使用文本编辑器创建名为 **signup.php** 的表单。将以下代码放入其中，并保存到 **app/Views/** 目录::

    <html>
    <head>
        <title>My Form</title>
    </head>
    <body>

        <?= validation_list_errors() ?>

        <?= form_open('form') ?>

            <h5>Username</h5>
            <input type="text" name="username" value="<?= set_value('username') ?>" size="50">

            <h5>Password</h5>
            <input type="text" name="password" value="<?= set_value('password') ?>" size="50">

            <h5>Password Confirm</h5>
            <input type="text" name="passconf" value="<?= set_value('passconf') ?>" size="50">

            <h5>Email Address</h5>
            <input type="text" name="email" value="<?= set_value('email') ?>" size="50">

            <div><input type="submit" value="Submit"></div>

        <?= form_close() ?>

    </body>
    </html>

成功页面
================

使用文本编辑器创建名为 **success.php** 的表单。将以下代码放入其中，并保存到 **app/Views/** 目录::

    <html>
    <head>
        <title>My Form</title>
    </head>
    <body>

        <h3>Your form was successfully submitted!</h3>

        <p><?= anchor('form', 'Try it again!') ?></p>

    </body>
    </html>

控制器
==============

使用文本编辑器创建名为 **Form.php** 的控制器。将以下代码放入其中，并保存到 **app/Controllers/** 目录：

.. literalinclude:: validation/001.php

.. note:: 方法 :ref:`$this->request->is() <incomingrequest-is>` 自 v4.3.0 起可用。
    在之前版本中，需要使用
    ``if (strtolower($this->request->getMethod()) !== 'post')``。

.. note:: 方法 :ref:`$this->validator->getValidated() <validation-getting-validated-data>`
    自 v4.4.0 起可用。

路由
==========

然后在 **app/Config/Routes.php** 中为控制器添加路由：

.. literalinclude:: validation/039.php
   :lines: 2-

试试看！
========

使用类似下面的 URL 访问站点，来测试表单::

    example.com/index.php/form/

提交表单后，应该会看到表单重新加载。这是因为还没有在 :ref:`controller-validatedata` 中设置任何验证规则。

``validateData()`` 是控制器提供的方法，内部使用 **Validation 类**。详见 :ref:`controller-validatedata`。

.. note:: 由于还没有告诉 ``validateData()`` 方法需要验证什么，
    它默认 **返回 false** （布尔值 false）。只有当成功应用了
    所有规则且没有任何规则失败时，``validateData()`` 方法才会返回 true。

说明
===========

关于上述页面，有几点需要注意。

signup.php
----------

表单（**signup.php**）是一个标准网页表单，但有两处特别的地方：

#. 使用 :doc:`表单辅助函数 </helpers/form_helper>` 创建表单的起始和结束标签。严格来说，这并非必需，可以使用标准 HTML 创建表单。但使用辅助函数的好处是，它会根据配置文件中的 URL 自动生成 action URL。这使得应用在 URL 变更时更具可移植性。
#. 在表单顶部，你会注意到以下函数调用::

    <?= validation_list_errors() ?>

   此函数将返回验证器发送的任何错误消息。如果没有消息，则返回空字符串。

Form.php
--------

控制器（**Form.php**）有一个属性：``$helpers``。它加载视图文件中使用的表单辅助函数。

控制器有一个方法：``index()``。当收到非 POST 请求时，此方法返回 **signup** 视图以显示表单。否则，它使用控制器提供的 :ref:`controller-validatedata` 方法运行验证流程。根据验证是否成功，它要么重新显示表单，要么显示成功页面。

添加验证规则
====================

然后在控制器（**Form.php**）中添加验证规则：

.. literalinclude:: validation/002.php
   :lines: 2-

提交表单后，应该会看到成功页面或带有错误消息的表单。

*********************
验证配置
*********************

.. _validation-traditional-and-strict-rules:

传统规则与严格规则
============================

CodeIgniter 4 有两种验证规则类。

默认规则类（**严格规则**）的命名空间为 ``CodeIgniter\Validation\StrictRules``，提供严格的验证。

传统规则类（**传统规则**）的命名空间为 ``CodeIgniter\Validation``。它们仅为了向后兼容而提供，可能无法正确验证非字符串值，新项目不应使用。

.. note:: 自 v4.3.0 起，默认使用 **严格规则** 以提高安全性。

严格规则
------------

.. versionadded:: 4.2.0

**严格规则** 不使用隐式类型转换。

传统规则
-----------------

.. important:: 传统规则仅为了向后兼容而存在。不要在新项目中使用它们。即使已在使用，也建议切换到严格规则。

.. warning:: 验证包含非字符串值（如 JSON 数据）的数据时，应使用 **严格规则**。

**传统规则** 隐式假定验证的是字符串值，输入值可能被隐式转换为字符串值。它适用于大多数基本场景，如验证 POST 数据。

但是，例如使用 JSON 输入数据时，数据可能是 bool/null/array 类型。使用传统规则类验证布尔值 ``true`` 时，它会被转换为字符串 ``'1'``。如果使用 ``integer`` 规则验证它，``'1'`` 会通过验证。

使用传统规则
-----------------------

.. warning:: **传统规则** 仅为了向后兼容而提供。它们可能无法正确验证非字符串值，新项目不应使用。

如果需要使用传统规则，需要在 **app/Config/Validation.php** 中更改规则类：

.. literalinclude:: validation/003.php

*******************
加载库
*******************

该库以 **validation** 服务的形式加载：

.. literalinclude:: validation/004.php
   :lines: 2-

这段代码会自动加载 ``Config\Validation`` 文件，其中包含用于引入多个规则集以及可复用规则集合的设置。

.. note:: 可能永远不需要使用此方法，因为 :doc:`控制器 </incoming/controllers>` 和 :doc:`模型 </models/model>` 都提供了使验证更加简便的方法。

********************
验证的工作原理
********************

- 验证永远不会更改要验证的数据。
- 验证按照设置的验证规则逐个检查每个字段。如果任何规则返回 false，则该字段的检查在此结束。
- 格式规则不允许空字符串。如需允许空字符串，请添加 ``permit_empty`` 规则。
- 如果要验证的数据中不存在某个字段，则值被解释为 ``null``。如需检查字段是否存在，请添加 ``field_exists`` 规则。

.. note:: ``field_exists`` 规则自 v4.5.0 起可用。

************************
设置验证规则
************************

CodeIgniter 允许为给定字段设置任意数量的验证规则，按顺序级联。要设置验证规则，可使用 ``setRule()``、``setRules()`` 或 ``withRequest()`` 方法。

设置单个规则
=====================

setRule()
---------

此方法设置单个规则。方法签名为::

    setRule(string $field, ?string $label, array|string $rules[, array $errors = []])

``$rules`` 接受管道符分隔的规则列表或规则数组：

.. literalinclude:: validation/005.php
   :lines: 2-

传递给 ``$field`` 的值必须与发送的任何数据数组中的键匹配。如果数据直接取自 ``$_POST``，则必须与表单输入名称完全匹配。

.. warning:: v4.2.0 之前，此方法的第三个参数 ``$rules`` 的类型声明为 ``string``。v4.2.0 及之后版本，类型声明被移除以允许数组。为避免破坏继承类中重写此方法的 LSP 一致性，子类的此方法也应移除类型声明。

设置多个规则
======================

setRules()
----------

与 ``setRule()`` 类似，但接受字段名称及其规则的数组：

.. literalinclude:: validation/006.php
   :lines: 2-

要设置带标签的错误消息，可以这样设置：

.. literalinclude:: validation/007.php
   :lines: 2-

.. note:: ``setRules()`` 会覆盖之前设置的任何规则。要向现有规则集添加多条规则，请多次调用 ``setRule()``。

.. _validation-dot-array-syntax:

为数组数据设置规则
============================

如果数据嵌套在关联数组中，可以使用"点数组语法"来轻松验证数据：

.. literalinclude:: validation/009.php
   :lines: 2-

可以使用 ``*`` 通配符匹配数组的任意一层：

.. literalinclude:: validation/010.php
   :lines: 2-

.. note:: v4.4.4 之前，由于一个 bug，通配符 ``*`` 在错误的维度验证数据。详见 :ref:`升级说明 <upgrade-444-validation-with-dot-array-syntax>`。

"点数组语法"在处理单维数组数据时也很有用。例如，多选下拉框返回的数据：

.. literalinclude:: validation/011.php
   :lines: 2-

.. _validation-withrequest:

withRequest()
=============

.. important:: 此方法仅为了向后兼容而存在。不要在新项目中使用它。即使已在使用，也建议使用其他更合适的方法。

.. warning:: 如需验证 POST 数据，请勿使用 ``withRequest()``。此方法使用 :ref:`$request->getVar() <incomingrequest-getting-data>`，按顺序返回 ``$_GET``、``$_POST`` 或 ``$_COOKIE`` 数据（取决于 php.ini 中的 `request-order <https://www.php.net/manual/zh/ini.core.php#ini.request-order>`_）。后面的值会覆盖前面的值。如果 Cookie 与 POST 参数同名，POST 值可能会被 Cookie 覆盖。

使用 Validation 类最常见的场景是验证来自 HTTP 请求的输入数据。如果需要，可以传入当前请求实例，它会自动将所有输入数据设置为要验证的数据：

.. literalinclude:: validation/008.php
   :lines: 2-

.. warning:: 使用此方法时，应使用 :ref:`getValidated() <validation-getting-validated-data>` 方法获取已验证的数据。因为当请求为 JSON 请求（``Content-Type: application/json``）时，此方法会从 :ref:`$request->getJSON() <incomingrequest-getting-json-data>` 获取 JSON 数据；当请求为 PUT、PATCH、DELETE 请求且不是 HTML 表单 POST（``Content-Type: multipart/form-data``）时，会从 :ref:`$request->getRawInput() <incomingrequest-retrieving-raw-data>` 获取原始数据；或者从 :ref:`$request->getVar() <incomingrequest-getting-data>` 获取数据。攻击者可以更改被验证的数据。

.. note:: :ref:`getValidated() <validation-getting-validated-data>` 方法自 v4.4.0 起可用。

***********************
使用验证
***********************

运行验证
==================

``run()`` 方法运行验证。方法签名为::

    run(?array $data = null, ?string $group = null, ?string $dbGroup = null): bool

``$data`` 是要验证的数据数组。可选的第二个参数 ``$group`` 是要应用的 :ref:`预定义规则组 <validation-array>`。可选的第三个参数 ``$dbGroup`` 是要使用的数据库组。

验证成功时此方法返回 true。

.. literalinclude:: validation/043.php
   :lines: 2-

运行多个验证
============================

.. note:: ``run()`` 方法不会重置错误状态。如果之前的运行失败，``run()`` 将始终返回 false，``getErrors()`` 会返回之前所有错误，直到显式重置。

如果打算运行多个验证（例如针对不同数据集或连续应用不同规则），可能需要在每次运行前调用 ``$validation->reset()`` 以清除之前的错误。注意 ``reset()`` 会使之前设置的任何数据、规则或自定义错误失效，因此需要重复调用 ``setRules()``、``setRuleGroup()`` 等：

.. literalinclude:: validation/019.php
   :lines: 2-

验证单个值
==================

``check()`` 方法根据规则验证单个值。第一个参数 ``$value`` 是要验证的值，第二个参数 ``$rule`` 是验证规则。可选的第三个参数 ``$errors`` 是自定义错误消息。

.. literalinclude:: validation/012.php
   :lines: 2-

.. note:: v4.4.0 之前，此方法的第二个参数 ``$rule`` 的类型声明为 ``string``。v4.4.0 及之后版本，类型声明被移除以允许数组。

.. note:: 此方法在内部调用 ``setRule()`` 方法来设置规则。

.. _validation-getting-validated-data:

获取已验证的数据
======================

.. versionadded:: 4.4.0

可通过 ``getValidated()`` 方法获取实际已验证的数据。此方法仅返回通过验证规则的元素数组。

.. literalinclude:: validation/044.php
   :lines: 2-

.. literalinclude:: validation/045.php
   :lines: 2-

.. _saving-validation-rules-to-config-file:

将验证规则集保存到配置文件
==================================================

Validation 类的一项实用功能是允许将整个应用的验证规则存储在配置文件中。可以将规则组织成"组"，每次运行验证时可以指定不同的组。

.. _validation-array:

如何保存规则
----------------------

要保存验证规则，只需在 ``Config\Validation`` 类中创建以组名命名的新公共属性。该属性包含一个验证规则数组。如前所示，验证数组的原型如下：

.. literalinclude:: validation/013.php

如何指定规则组
-------------------------

调用 ``run()`` 方法时可以指定要使用的组：

.. literalinclude:: validation/014.php
   :lines: 2-

如何保存错误消息
--------------------------

也可以将这些自定义错误消息存储在配置文件中，属性名与组名相同，并追加 ``_errors``。使用该组时，这些消息会自动用于任何错误：

.. literalinclude:: validation/015.php

或者在数组中传递所有设置：

.. literalinclude:: validation/016.php

详见 :ref:`validation-custom-errors` 了解数组格式详情。

获取和设置规则组
-----------------------------

获取规则组
^^^^^^^^^^^^^^

此方法从验证配置中获取规则组：

.. literalinclude:: validation/017.php
   :lines: 2-

设置规则组
^^^^^^^^^^^^^^

此方法从验证配置中设置规则组到验证服务：

.. literalinclude:: validation/018.php
   :lines: 2-

.. _validation-placeholders:

验证占位符
=======================

Validation 类提供了一种简单的方法，可以根据传入的数据替换规则中的部分内容。这听起来可能比较抽象，但在使用 ``is_unique`` 验证规则时尤其方便。

占位符是传入的 ``$data`` 中的字段名（或数组键），用花括号包裹。它将被匹配的传入字段的 **值** 替换。下面是一个示例：

.. literalinclude:: validation/020.php
   :lines: 2-

.. warning:: 自 v4.3.5 起，出于安全原因，必须为占位符字段（上面示例代码中的 ``id`` 字段）设置验证规则。因为攻击者可以向应用发送任何数据。

在这组规则中，它声明 Email 地址在数据库中应该是唯一的，但 ``id`` 与占位符值匹配的行除外。假设表单 POST 数据如下：

.. literalinclude:: validation/021.php
   :lines: 2-

则 ``{id}`` 占位符将被替换为数字 **4**，得到以下修订后的规则：

.. literalinclude:: validation/022.php
   :lines: 2-

因此在验证电子邮件唯一性时，会忽略 ``id=4`` 的行。

.. note:: 自 v4.3.5 起，如果占位符（``id``）的值未通过验证，占位符将不会被替换。

这也可用于在运行时创建更动态的规则，只要确保传入的任何动态键不会与表单数据冲突即可。

*******************
处理错误
*******************

Validation 类提供了多种方法来帮助设置错误消息、提供自定义错误消息，以及检索一个或多个错误以进行显示。

默认情况下，错误消息派生于 **system/Language/en/Validation.php** 中的语言字符串，每个规则都有一个对应条目。如需更改默认消息，请创建文件 **app/Language/en/Validation.php** （和/或在相应语言目录中创建），并放置要更改默认值的键值对。

.. _validation-custom-errors:

设置自定义错误消息
=============================

``setRule()`` 和 ``setRules()`` 方法都可以接受自定义消息数组作为最后一个参数，这些消息将用作每个字段的特定错误。这样可以为用户提供更友好的体验，因为错误消息是针对每个实例定制的。如果未提供自定义错误消息，将使用默认值。

有两种方式提供自定义错误消息。

作为最后一个参数：

.. literalinclude:: validation/023.php
   :lines: 2-

或者标签样式：

.. literalinclude:: validation/024.php
   :lines: 2-

如果需要在消息中包含字段的"人性化"名称、某些规则允许的可选参数（如 max_length），或者被验证的值，可以分别在消息中添加 ``{field}``、``{param}`` 和 ``{value}`` 标签::

    'min_length' => 'Supplied value ({value}) for {field} must have at least {param} characters.'

对于人性化名称为 Username、规则为 ``min_length[6]``、值为 "Pizza" 的字段，将显示错误消息："Supplied value (Pizza) for Username must have at least 6 characters."

.. warning:: 使用 ``getErrors()`` 或 ``getError()`` 获取错误消息时，消息未进行 HTML 转义。如果使用用户输入数据（如 ``({value})``）构建错误消息，其中可能包含 HTML 标签。如果在显示前不转义消息，可能存在 XSS 攻击风险。

.. note:: 使用标签样式错误消息时，如果将第二个参数传递给 ``setRules()``，它会被第一个参数的值覆盖。

消息和验证标签的翻译
=============================================

要使用语言文件中的翻译字符串，只需使用点语法。假设在 **app/Languages/en/Rules.php** 有一个翻译文件。可以直接使用该文件中定义的语言行，如下所示：

.. literalinclude:: validation/025.php
   :lines: 2-

.. _validation-getting-all-errors:

获取所有错误
==================

如需获取所有失败字段的错误消息，可使用 ``getErrors()`` 方法：

.. literalinclude:: validation/026.php
   :lines: 2-

如果没有错误，将返回空数组。

使用通配符（``*``）时，错误会指向特定字段，将星号替换为相应的键::

    // 对于数据
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

    // 错误将是
    'contacts.friends.1.name' => 'The contacts.friends.*.name field is required.'

获取单个错误
======================

可使用 ``getError()`` 方法获取单个字段的错误。唯一参数是字段名称：

.. literalinclude:: validation/027.php
   :lines: 2-

如果没有错误，将返回空字符串。

.. note:: 使用通配符时，所有匹配通配符的错误都会合并为单行，并以 EOL 字符分隔。

检查是否存在错误
=====================

可使用 ``hasError()`` 方法检查是否存在错误。唯一参数是字段名称：

.. literalinclude:: validation/028.php
   :lines: 2-

使用通配符指定字段时，将检查所有匹配通配符字段的错误：

.. literalinclude:: validation/029.php
   :lines: 2-

.. _validation-redirect-and-validation-errors:

重定向与验证错误
==============================

PHP 在请求之间不共享任何内容。因此，当验证失败并重定向时，重定向后的请求中不会有验证错误，因为验证是在之前的请求中运行的。

在这种情况下，需要使用辅助函数 :php:func:`validation_errors()`、:php:func:`validation_list_errors()` 和 :php:func:`validation_show_error()`。这些函数检查存储在 Session 中的验证错误。

要将验证错误存储到 Session 中，需要在使用 :php:func:`redirect() <redirect>` 时配合 ``withInput()``：

.. literalinclude:: validation/042.php
   :lines: 2-

.. _validation-customizing-error-display:

*************************
自定义错误显示
*************************

调用 ``$validation->listErrors()`` 或 ``$validation->showError()`` 时，它会在后台加载一个视图文件来确定错误如何显示。默认情况下，用 ``errors`` class 包裹 div。可以轻松创建新视图并在整个应用中使用。

创建视图
==================

第一步是创建自定义视图。这些视图可以放在 ``view()`` 方法能找到的任何位置，即标准视图目录或任何命名空间视图文件夹。例如，可以在 **app/Views/_errors_list.php** 创建新视图：

.. literalinclude:: validation/030.php

视图中有一个名为 ``$errors`` 的数组可用，其中包含错误列表，键是有错误的字段名，值是错误消息，如下所示：

.. literalinclude:: validation/031.php
   :lines: 2-

实际上可以创建两种类型的视图。第一种包含所有错误的数组，就是刚才看到的那种。另一种类型更简单，只包含一个变量 ``$error``，其中包含错误消息。这与 ``showError()`` 方法配合使用，必须指定字段::

    <span class="help-block"><?= esc($error) ?></span>

配置
=============

创建视图后，需要让 Validation 类知道它们。打开 **app/Config/Validation.php**。在其中会找到 ``$templates`` 属性，可以列出任意数量的自定义视图，并提供一个简短的别名供引用。如果添加上面的示例文件，看起来类似这样：

.. literalinclude:: validation/032.php

指定模板
=======================

可以通过在 ``listErrors()`` 中传递别名作为第一个参数来指定要使用的模板::

    <?= $validation->listErrors('my_list') ?>

显示字段特定错误时，可以将别名作为第二个参数传递给 ``showError()`` 方法，紧跟在应显示错误的字段名之后::

    <?= $validation->showError('username', 'my_single') ?>

*********************
创建自定义规则
*********************

.. _validation-using-rule-classes:

使用规则类
==================

规则存储在简单的命名空间类中。可以存储在任何位置，只要自动加载器能找到。这些文件称为规则集（RuleSet）。

添加规则集
----------------

要添加新规则集，编辑 **app/Config/Validation.php** 并将新文件添加到 ``$ruleSets`` 数组：

.. literalinclude:: validation/033.php

可以作为完全限定类名的简单字符串添加，也可以如上所示使用 ``::class`` 后缀。使用 ``::class`` 后缀的主要好处是，它在更高级的 IDE 中提供额外的导航功能。

创建规则类
---------------------

在文件中，每个方法都是一条规则，必须接受要验证的值作为第一个参数，并且必须返回布尔值 true 或 false，表示是否通过测试：

.. literalinclude:: validation/034.php

默认情况下，系统会在 **system/Language/en/Validation.php** 中查找用于错误的语言字符串。如需为自定义规则提供默认错误消息，可以将它们放在 **app/Language/en/Validation.php** （和/或在相应语言目录中替换 ``en``）。此外，如果需要使用其他语言字符串文件代替默认的 **Validation.php**，可以通过在第二个参数（或者，如果规则需要使用参数，如下所述——第四个参数）中接受 ``&$error`` 变量来提供错误消息：

.. literalinclude:: validation/035.php

使用自定义规则
-------------------

新的自定义规则现在可以像任何其他规则一样使用：

.. literalinclude:: validation/036.php
   :lines: 2-

允许参数
-------------------

如果方法需要使用参数，函数至少需要三个参数：

1. 要验证的值（``$value``）
2. 参数字符串（``$params``）
3. 表单提交的所有数据的数组（``$data``）
4. （可选）自定义错误字符串（``&$error``），如上所述。

.. warning:: ``$data`` 中的字段值未经验证（或可能无效）。使用未经验证的输入数据是漏洞的来源。在使用 ``$data`` 中的数据之前，必须在自定义规则中执行必要的验证。

``$data`` 数组在需要检查其他提交字段值的规则中特别有用，例如 ``required_with``：

.. literalinclude:: validation/037.php

.. _validation-using-closure-rule:

使用闭包规则
==================

.. versionadded:: 4.3.0

若自定义规则仅需在应用中使用一次，可以使用闭包代替规则类。

需要使用数组作为验证规则：

.. literalinclude:: validation/040.php
   :lines: 2-

必须为闭包规则设置错误消息。指定错误消息时，为闭包规则设置数组键。在上面的代码中，``required`` 规则的键为 ``0``，闭包的键为 ``1``。

或者可以使用以下参数：

.. literalinclude:: validation/041.php
   :lines: 2-

.. _validation-using-callable-rule:

使用可调用规则
===================

.. versionadded:: 4.5.0

如需使用数组回调作为规则，可以使用它代替闭包规则。

需要使用数组作为验证规则：

.. literalinclude:: validation/046.php
   :lines: 2-

必须为可调用规则设置错误消息。指定错误消息时，为可调用规则设置数组键。在上面的代码中，``required`` 规则的键为 ``0``，可调用的键为 ``1``。

或者可以使用以下参数：

.. literalinclude:: validation/047.php
   :lines: 2-

.. _validation-available-rules:

***************
可用规则
***************

.. note:: 规则是字符串；参数之间 **不能有空格**，尤其是 ``is_unique`` 规则。``ignore_value`` 前后不能有空格。

.. literalinclude:: validation/038.php
   :lines: 2-

.. _rules-for-general-use:

通用规则
=====================

以下是所有可用的原生规则列表：

======================= ========== ============================================= ===================================================
规则                    参数       描述                                          示例
======================= ========== ============================================= ===================================================
alpha                   无         若字段为空或包含 ASCII 字母以外的内容，
                                   则校验失败。
alpha_dash              无         若字段为空或包含 ASCII 字母数字、
                                   下划线或减号以外的内容，则校验失败。
alpha_numeric           无         若字段为空或包含 ASCII 字母数字以外的内容，
                                   则校验失败。
alpha_numeric_punct     无         若字段为空或包含字母数字、
                                   空格及以下指定标点符号以外的内容，
                                   则校验失败：
                                   ``~``（波浪号）、``!``（感叹号）、
                                   ``#``（井号）、``$``（美元符号）、
                                   ``%``（百分号）、``&``（与符号）、
                                   ``*``（星号）、``-``（减号）、
                                   ``_``（下划线）、``+``（加号）、
                                   ``=``（等号）、``|``（竖线）、
                                   ``:``（冒号）、``.``（点号）。
alpha_numeric_space     无         若字段为空或包含 ASCII
                                   字母数字或空格以外的内容，则校验失败。
alpha_space             无         若字段为空或包含 ASCII
                                   字母或空格以外的内容，则校验失败。
decimal                 无         若字段不是十进制数字，则校验失败。
                                   允许带有正负号（``+`` 或 ``-``）。
differs                 是         若字段值与参数指定的字段值相同，则校验失败。  ``differs[field_name]``
exact_length            是         若字段长度不等于参数指定的值，则校验失败。    ``exact_length[5]`` 或 ``exact_length[5,8,12]``
                                   支持以逗号分隔的多个值。
field_exists            是         若字段不存在，则校验失败。
                                   （此规则自 v4.5.0 起新增）
greater_than            是         若字段值小于等于参数值，或不是数字，          ``greater_than[8]``
                                   则校验失败。
greater_than_equal_to   是         若字段值小于参数值，或不是数字，则校验失败。  ``greater_than_equal_to[5]``
hex                     无         若字段包含十六进制字符以外的内容，
                                   则校验失败。
if_exist                无         若包含此规则，则仅在待验证数据中
                                   存在该字段键名时进行校验。
in_list                 是         若字段值不在预定义列表中，则校验失败。        ``in_list[red,blue,green]``
integer                 无         若字段包含整数以外的内容，则校验失败。
is_natural              无         若字段包含自然数
                                   （``0``, ``1``, ``2``, ``3`` 等）
                                   以外的内容，则校验失败。
is_natural_no_zero      无         若字段包含非 0 自然数
                                   （``1``, ``2``, ``3`` 等）以外的内容，
                                   则校验失败。
is_not_unique           是         检查数据库中是否存在给定值。                  ``is_not_unique[table.field,where_field,where_value]`` 或 ``is_not_unique[dbGroup.table.field,where_field,where_value]``
                                   支持通过字段/值过滤掉部分记录
                                   （目前仅支持一个过滤器）。
                                   （自 v4.6.0 起，可选择性地将
                                   dbGroup 作为参数传递）
is_unique               是         检查字段值是否已存在于数据库中。              ``is_unique[table.field,ignore_field,ignore_value]`` 或 ``is_unique[dbGroup.table.field,ignore_field,ignore_value]``
                                   可选择性地设置要忽略的列和值，
                                   在更新记录时用于排除自身。
                                   （自 v4.6.0 起，可选择性地将
                                   dbGroup 作为参数传递）
less_than               是         若字段值大于等于参数值，或不是数字，          ``less_than[8]``
                                   则校验失败。
less_than_equal_to      是         若字段值大于参数值，或不是数字，              ``less_than_equal_to[8]``
                                   则校验失败。
matches                 是         字段值必须与参数指定的字段值一致。            ``matches[field]``
max_length              是         若字段长度超过参数值，则校验失败。            ``max_length[8]``
min_length              是         若字段长度短于参数值，则校验失败。            ``min_length[3]``
not_in_list             是         若字段值在预定义列表中，则校验失败。          ``not_in_list[red,blue,green]``
numeric                 无         若字段包含数字字符以外的内容，则校验失败。
permit_empty            无         允许字段接收空数组、空字符串、null
                                   或 false。验证通过后，将跳过除
                                   ``required_with`` 和 ``required_without``
                                   以外的所有其他验证规则。
regex_match             是         若字段不匹配正则表达式，则校验失败。          ``regex_match[/regex/]``
                                   **注意：** 自 v4.7.0 起，
                                   若在此规则中使用占位符，
                                   必须使用双大括号 ``{{...}}``
                                   而非单大括号 ``{...}``。
required                无         若字段是空数组、空字符串、null 或 false，
                                   则校验失败。
required_with           是         当数据中指定的任一其他字段不为                ``required_with[field1,field2]``
                                   `empty()`_ 时，此字段必填。
required_without        是         当数据中指定的任一其他字段为                  ``required_without[field1,field2]``
                                   `empty()`_ 时，此字段必填。
string                  无         **alpha*** 系列规则的通用替代方案，
                                   用于确认元素是否为字符串。
timezone                无         若字段不符合 `timezone_identifiers_list()`_
                                   定义的时区，则校验失败。
valid_base64            无         若字段包含有效的 Base64 字符以外的内容，
                                   则校验失败。
valid_cc_number         是         验证信用卡号是否符合指定发卡机构的格式。      ``valid_cc_number[amex]``
                                   支持的机构包括：
                                   American Express (``amex``),
                                   China Unionpay (``unionpay``),
                                   Diners Club CarteBlance (``carteblanche``),
                                   Diners Club (``dinersclub``),
                                   Discover Card (``discover``),
                                   Interpayment (``interpayment``),
                                   JCB (``jcb``), Maestro (``maestro``),
                                   Dankort (``dankort``), NSPK MIR (``mir``),
                                   Troy (``troy``), MasterCard (``mastercard``),
                                   Visa (``visa``), UATP (``uatp``),
                                   Verve (``verve``),
                                   CIBC Convenience Card (``cibc``),
                                   Royal Bank of Canada Client Card (``rbc``),
                                   TD Canada Trust Access Card (``tdtrust``),
                                   Scotiabank Scotia Card (``scotia``),
                                   BMO ABM Card (``bmoabm``),
                                   HSBC Canada Card (``hsbc``)
valid_date              是         若字段不包含有效日期，则校验失败。            ``valid_date[d/m/Y]``
                                   若未指定可选的日期格式参数，
                                   则任何 `strtotime()`_ 接受的字符串
                                   均视为有效。**因此通常需要指定参数。**
valid_email             无         若字段不包含有效的 Email 地址，则校验失败。
valid_emails            无         若逗号分隔列表中存在任何无效的 Email 地址，
                                   则校验失败。
valid_ip                是         若提供的 IP 无效，则校验失败。可指定可选参数  ``valid_ip[ipv6]``
                                   ``ipv4`` 或 ``ipv6`` 以限定 IP 格式。
valid_json              无         若字段不包含有效的 JSON 字符串，则校验失败。
valid_url               无         若字段不包含（宽泛意义上的）URL，
                                   则校验失败。包含可能为主机名的简单字符串
                                   （如 "codeigniter"）。
                                   **通常应使用** ``valid_url_strict``。
valid_url_strict        是         若字段不包含有效的 URL，则校验失败。          ``valid_url_strict[https]``
                                   可指定允许的协议列表。若未指定，
                                   则默认为 ``http,https``。此规则
                                   使用 PHP 的 ``FILTER_VALIDATE_URL``。
======================= ========== ============================================= ===================================================

.. note:: 还可以使用任何返回布尔值且至少允许一个参数（要验证的字段数据）的原生 PHP 函数。

.. important:: Validation 类 **永远不会更改** 要验证的数据。

.. _timezone_identifiers_list(): https://www.php.net/manual/zh/function.timezone-identifiers-list.php
.. _strtotime(): https://www.php.net/manual/zh/function.strtotime.php
.. _empty(): https://www.php.net/manual/zh/function.empty.php

.. _rules-for-file-uploads:

文件上传规则
======================

验证上传的文件时，必须使用专门为文件验证创建的规则。

.. important:: 只能使用下表中列出的规则来验证文件。因此，如果在文件验证规则数组或字符串中添加任何通用规则（如 ``permit_empty``），文件验证将无法正常工作。

由于 HTML 文件上传的内容不存在于常规数据中，而是存储在 ``$_FILES`` 全局变量中，因此需要两次指定输入字段名：一次按常规规则指定字段名，另一次则作为所有文件上传相关规则的第一个参数::

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
uploaded                是         若参数名与上传文件名不匹配，则校验失败。      ``uploaded[field_name]``
                                   如需设为可选上传（非必填），
                                   则无需定义此规则。

max_size                是         若上传文件超过第二个参数指定的大小            ``max_size[field_name,2048]``
                                   （单位为 KB），或超过 `php.ini`
                                   配置文件中 `upload_max_filesize`
                                   指令允许的最大值，则校验失败。
max_dims                是         若上传图像的最大宽度或高度超过指定值，        ``max_dims[field_name,300,150]``
                                   则校验失败。参数依次为：字段名、宽度、高度。
                                   若文件无法识别为图像，同样校验失败。
min_dims                是         若上传图像的最小宽度或高度未达到指定值，      ``min_dims[field_name,300,150]``
                                   则校验失败。参数依次为：字段名、宽度、高度。
                                   若文件无法识别为图像，同样校验失败。（此规则
                                   自 v4.6.0 起新增）
mime_in                 是         若文件的 MIME 类型不在参数列出的范围内，      ``mime_in[field_name,image/png,image/jpeg]``
                                   则校验失败。
ext_in                  是         若文件的扩展名不在参数列出的范围内，          ``ext_in[field_name,png,jpg,gif]``
                                   则校验失败。
is_image                是         若基于 MIME 类型无法将文件识别为图像，        ``is_image[field_name]``
                                   则校验失败。
======================= ========== ============================================= ===================================================

文件上传规则适用于单文件和多文件上传。
