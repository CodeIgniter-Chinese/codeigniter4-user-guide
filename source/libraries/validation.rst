###########
验证
###########

CodeIgniter提供了一个全面的数据验证类,可以帮助最小化您编写的代码量。

.. contents::
   :local:
   :depth: 2

********
概览
********

在解释CodeIgniter的验证方法之前,让我们描述一下理想的场景:

#. 显示一个表单。
#. 您填写并提交它。
#. 如果您提交了无效的数据,或者可能遗漏了必填项,则会重新显示包含您的数据以及描述问题的错误消息的表单。
#. 这个过程将一直持续,直到您提交了一个有效的表单。

在接收端,脚本必须:

#. 检查必填数据。
#. 验证数据的类型和标准是否正确。例如,如果提交了一个用户名,则必须验证它只包含允许的字符。它必须有一个最小长度,并且不能超过最大长度。用户名不能是其他人已经存在的用户名,也可能不能是保留字等。
#. 对数据进行安全处理。
#. 必要时预格式化数据。
#. 准备好数据,将其插入数据库。

尽管上述过程没有非常复杂,但通常需要大量的代码,且为了显示错误消息,各种控制结构通常被放入表单HTML中。 表单验证虽简单,但实施通常非常混乱且麻烦。

************************
表单验证教程
************************

下面是一个关于实现CodeIgniter表单验证的“动手”教程。

为了实现表单验证,您需要三样东西:

#. 包含表单的 :doc:`视图 </outgoing/views>` 文件。
#. 包含“成功”消息的视图文件,在成功提交后显示。
#. :doc:`控制器 </incoming/controllers>` 方法来接收和处理已提交的数据。

让我们为会员注册表单创建这三个部分作为示例。

表单
=======

使用文本编辑器,创建一个名为 **signup.php** 的表单。在其中放置此代码并将其保存到您的 **app/Views/** 文件夹中::

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

            <h5>电子邮件地址</h5>
            <input type="text" name="email" value="<?= set_value('email') ?>" size="50">

            <div><input type="submit" value="提交"></div>

        <?= form_close() ?>

    </body>
    </html>

成功页面
================

使用文本编辑器,创建一个名为 **success.php** 的表单。在其中放置此代码并将其保存到您的 **app/Views/** 文件夹中::

    <html>
    <head>
        <title>我的表单</title>
    </head>
    <body>

        <h3>您的表单已成功提交!</h3>

        <p><?= anchor('form', '再试一次!') ?></p>

    </body>
    </html>

控制器
==============

使用文本编辑器,创建一个名为 **Form.php** 的控制器。在其中放置此代码并将其保存到您的 **app/Controllers/** 文件夹中:

.. literalinclude:: validation/001.php

.. note:: 从v4.3.0开始,可以使用 :ref:`$this->request->is() <incomingrequest-is>` 方法。
    在之前的版本中,您需要使用 ``if (strtolower($this->request->getMethod()) !== 'post')``。

路由
==========

然后在 **app/Config/Routes.php** 中为控制器添加路由:

.. literalinclude:: validation/039.php
   :lines: 2-

试一试!
=======

要测试您的表单,请使用类似以下的URL访问您的站点::

    example.com/index.php/form/

如果您提交表单,应该只是看到表单重新加载。 这是因为您还没有在 ``$this->validate()`` 中设置任何验证规则。

``validate()`` 方法是控制器中的一个方法。 它使用 **Validation类**。 参见 :ref:`controllers-validating-data`。

.. note:: 由于您还没有告诉 ``validate()`` 方法验证任何内容,它默认返回 **false**(布尔值false)。
    ``validate()`` 方法仅在成功应用规则而没有任何失败时才返回 true。

解释
===========

您会注意到上述页面的几件事。

signup.php
----------

表单(**signup.php**)是一个标准的网页表单,只有一些例外:

#. 它使用 :doc:`表单辅助函数 </helpers/form_helper>` 来创建表单的打开和关闭。 从技术上讲,这不是必需的。 您可以使用标准HTML来创建表单。
   但是,使用辅助函数的好处是它根据配置文件中的URL生成操作URL。 这使您的应用程序在URL更改的情况下更便于移植。
#. 在表单顶部,您会注意到以下函数调用:
   ::

    <?= validation_list_errors() ?>

   此函数将返回验证器发送回的任何错误消息。 如果没有消息,它会返回一个空字符串。

Form.php
--------

控制器(**Form.php**)有一个属性:``$helpers``。
它加载视图文件中使用的表单辅助函数。

控制器有一个方法:``index()``。 当收到非POST请求时,此方法会返回 **signup** 视图以显示表单。 否则,它会使用Controller提供的 ``validate()`` 方法。 它也运行验证例程。
根据验证是否成功,它要么显示表单,要么显示成功页面。

添加验证规则
====================

然后在控制器(**Form.php**)中添加验证规则:

.. literalinclude:: validation/002.php
   :lines: 2-

如果提交表单,您应该会看到成功页面或带有错误消息的表单。

*********************
验证配置
*********************

.. _validation-traditional-and-strict-rules:

传统规则和严格规则
============================

CodeIgniter 4 有两类验证规则类。
传统规则类 (**传统规则**) 的命名空间为 ``CodeIgniter\Validation``,
新类 (**严格规则**) 的命名空间为 ``CodeIgniter\Validation\StrictRules``,它们提供更严格的验证。

.. note:: 从 v4.3.0 开始,**严格规则** 默认用于更好的安全性。

传统规则
-----------------

.. warning:: 在包含非字符串值(如 JSON 数据)的数据验证中,建议使用 **严格规则**。

**传统规则** 隐式地假设正在验证字符串值,
被验证的值可能会隐式转换为字符串值。
这适用于大多数基本情况,如验证 POST 数据。

但是,例如,如果使用 JSON 输入数据,它可能是 bool/null/array 类型。
当使用传统规则类验证布尔值 ``true`` 时,它会被转换为字符串 ``'1'``。
如果使用 ``integer`` 规则对其进行验证,``'1'`` 可以通过验证。

严格规则
-----------------

.. versionadded:: 4.2.0

**严格规则** 不使用隐式类型转换。

使用传统规则
-----------------------

如果要使用传统规则,您需要在 **app/Config/Validation.php** 中更改规则类:

.. literalinclude:: validation/003.php

*******************
加载库
*******************

该库以名为 **validation** 的服务加载:

.. literalinclude:: validation/004.php

这会自动加载包含多个 Ruleset 和可轻松重用的规则集合的 ``Config\Validation`` 文件。

.. note:: 您可能永远不需要使用此方法,因为 :doc:`控制器 </incoming/controllers>` 和
    :doc:`模型 </models/model>` 都提供了使验证更容易的方法。

************************
设置验证规则
************************

CodeIgniter 允许您根据需要为给定字段设置尽可能多的验证规则,级联排列。 要设置验证规则,
您将使用 ``setRule()``、``setRules()`` 或 ``withRequest()``
方法。

设置单个规则
=====================

setRule()
---------

此方法设置单个规则。 它具有以下方法签名::

    setRule(string $field, ?string $label, array|string $rules[, array $errors = []])

``$rules`` 可以接受管道分隔的规则列表或规则数组集合:

.. literalinclude:: validation/005.php

传递给 ``$field`` 的值必须与传入的数据数组的键匹配。 如果
数据直接来自 ``$_POST``,那么它必须与表单输入名称完全匹配。

.. warning:: 在 v4.2.0 之前,此方法的第三个参数 ``$rules`` 的类型提示为 ``string``。 在 v4.2.0 及以后,类型提示已删除以允许数组。 为了避免在覆盖此方法的扩展类中破坏 LSP,子类的方法也应修改为删除类型提示。

设置多个规则
======================

setRules()
----------

与 ``setRule()`` 类似,但接受字段名称及其规则的数组:

.. literalinclude:: validation/006.php

要给出带标签的错误消息,可以设置如下:

.. literalinclude:: validation/007.php

.. _validation-withrequest:

设置数组数据的规则
============================

如果您的数据在嵌套的关联数组中,您可以使用“点数组语法”来轻松验证您的数据:

.. literalinclude:: validation/009.php

您可以使用通配符符号 ``*`` 匹配数组的任意一级:

.. literalinclude:: validation/010.php

“点数组语法”在您有单维数组数据时也很有用。
例如,下拉多选返回的数据:

.. literalinclude:: validation/011.php

withRequest()
=============

使用验证库最常见的时机之一是在验证从 HTTP 请求输入的数据。 如果需要,您可以传入当前请求对象的实例,它将获取所有输入数据并将其设置为要验证的数据:

.. literalinclude:: validation/008.php

.. note:: 此方法从
    :ref:`$request->getJSON() <incomingrequest-getting-json-data>` 获取 JSON 数据
    当请求是 JSON 请求(``Content-Type: application/json``)时,
    或者从
    :ref:`$request->getRawInput() <incomingrequest-retrieving-raw-data>` 获取原始数据
    当请求是 PUT、PATCH、DELETE 请求且
    不是 HTML 表单 POST (``Content-Type: multipart/form-data``) 时,
    或者从 :ref:`$request->getVar() <incomingrequest-getting-data>` 获取数据。

***********************
使用验证
***********************

运行验证
==================

``run()`` 方法运行验证。 它具有以下方法签名::

    run(?array $data = null, ?string $group = null, ?string $dbGroup = null): bool

``$data`` 是要验证的数据数组。 可选的第二个参数
``$group`` 是要应用的 :ref:`预定义规则组 <validation-array>`。
可选的第三个参数 ``$dbGroup`` 是要使用的数据库组。

如果验证成功,此方法将返回 true。

.. literalinclude:: validation/043.php

运行多次验证
============================

.. note:: ``run()`` 方法不会重置错误状态。 如果先前的运行失败,
   ``run()`` 将总是返回 false,``getErrors()`` 将返回
   所有先前的错误,直到显式重置。

如果您打算连续运行多次验证,例如对不同的数据集或使用不同的
规则,您可能需要在每次运行之前调用 ``$validation->reset()`` 来清除
先前运行的错误。 请注意,``reset()`` 会使任何先前设置的数据、规则或自定义错误无效,
所以像 ``setRules()``、``setRuleGroup()`` 等需要重复设置:

.. literalinclude:: validation/019.php

验证1个值
==================

针对规则验证单个值:

.. literalinclude:: validation/012.php

将验证规则集保存到配置文件
==================================================

Validation类的一个很好的特性是它允许您将整个应用程序的所有
验证规则存储在配置文件中。 您可以将规则组织到“组”中。 每次运行
验证时,您都可以指定不同的组。

.. _validation-array:

如何保存规则
----------------------

要存储验证规则,只需在 ``Config\Validation``
类中创建一个新的公共属性,使用组的名称作为名称。 此元素将保存带有验证
规则的数组。 如前所示,验证数组的原型如下:

.. literalinclude:: validation/013.php

如何指定规则组
-------------------------

当您调用 ``run()`` 方法时,可以指定要使用的组:

.. literalinclude:: validation/014.php

如何保存错误消息
--------------------------

您还可以通过使用属性名称并附加 ``_errors`` 将自定义错误消息存储在此配置文件中。 当使用此组时,这些将自动
用于任何错误:

.. literalinclude:: validation/015.php

或者以数组形式传递所有设置:

.. literalinclude:: validation/016.php

请参阅 :ref:`validation-custom-errors` 以了解数组格式的详细信息。

获取和设置规则组
-----------------------------

**获取规则组**

此方法从验证配置中获取规则组:

.. literalinclude:: validation/017.php

**设置规则组**

此方法将验证配置中的规则组设置到验证服务中:

.. literalinclude:: validation/018.php

.. _validation-placeholders:

验证占位符
=======================

Validation类提供了一个简单的方法来根据传入的数据替换规则的部分。
这听起来相当隐晦,但在 ``is_unique`` 验证规则时特别方便。 占位符只是
被 ``$data`` 作为``$field`` 传入的值周围的大括号。 它将被
匹配的传入字段的**值**替换。 下面的示例应该能澄清这一点:

.. literalinclude:: validation/020.php

.. note:: 从 v4.3.5 开始,您必须为占位符字段设置验证规则
    (``id``)。

在这组规则中,它指出电子邮件地址在数据库中应该是唯一的,除了与占位符的值匹配的行。 假设表单 POST 数据如下:

.. literalinclude:: validation/021.php

那么 ``{id}`` 占位符将被替换为数字 **4**,给出这条修订后的规则:

.. literalinclude:: validation/022.php

因此,在验证电子邮件地址是否唯一时,它会忽略数据库中 ``id=4`` 的行。

.. note:: 从 v4.3.5 开始,如果占位符 (``id``) 值未通过
    验证,占位符将不会被替换。

这也可以用于在运行时创建更动态的规则,只要您注意任何传入的动态
键不与表单数据冲突即可。

*******************
使用错误
*******************

Validation库提供了几种方法来帮助您设置错误消息、提供
自定义错误消息以及检索一个或多个错误以显示。

默认情况下,错误消息来自 **system/Language/en/Validation.php** 中的语言字符串,
其中每个规则都有一个条目。

.. _validation-custom-errors:

设置自定义错误消息
=============================

``setRule()`` 和 ``setRules()`` 方法的最后一个参数都可以接受自定义
消息数组,这些消息将作为针对每个字段的特定错误消息,这为用户提供了非常愉快的体验,因为错误消息是针对每个实例定制的。 如果未提供自定义错误消息,则使用默认值。

有两种提供自定义错误消息的方法。

作为最后一个参数:

.. literalinclude:: validation/023.php

或以标记样式:

.. literalinclude:: validation/024.php

如果您想包括字段的“人类”名称,或某些规则允许的可选参数(如 max_length),或者被验证的值,您可以分别向消息中添加 ``{field}``、``{param}`` 和 ``{value}`` 标签。例如::

    'min_length' => '提供的({value})供{field}的值必须至少有{param}个字符。'

在一个字段的人类名称为用户名且规则为 ``min_length[6]`` 且值为“Pizza”的情况下,错误消息将显示:“提供的值(Pizza)用户名必须至少有 6 个字符。”

.. warning:: 如果使用 ``getErrors()`` 或 ``getError()`` 获取错误消息,则消息未转义 HTML。如果使用像 ``({value})`` 这样的用户输入数据来制作错误消息,则它可能包含 HTML 标签。如果在显示它们之前不转义消息,则可能存在 XSS 攻击。

.. note:: 当使用标记样式的错误消息时,如果向 ``setRules()`` 的第二个参数传递参数,则它将被第一个参数的值覆盖。

翻译消息和验证标签
=============================================

要使用语言文件中的翻译字符串,我们可以简单地使用点表示法。
假设我们有一个位于这里的翻译文件:**app/Languages/en/Rules.php**。
我们可以简单地使用该文件中定义的语言行,如下所示:

.. literalinclude:: validation/025.php

.. _validation-getting-all-errors:

获取所有错误
==================

如果您需要检索失败字段的所有错误消息,可以使用 ``getErrors()`` 方法:

.. literalinclude:: validation/026.php

如果不存在错误,将返回一个空数组。

当使用通配符时,错误将指向特定的字段,用适当的键/键替换通配符::

    // for data
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

    // rule
    'contacts.*.name' => 'required'

    // error will be
    'contacts.friends.1.name' => 'The contacts.*.name field is required.'

获取单个错误
======================

您可以使用 ``getError()`` 方法检索单个字段的错误。 唯一的参数是字段
名称:

.. literalinclude:: validation/027.php

如果不存在错误,将返回一个空字符串。

.. note:: 当使用通配符时,所有匹配掩码的找到的错误将合并到一行中,以 EOL 字符分隔。

检查错误是否存在
=====================

您可以使用 ``hasError()`` 方法检查是否存在错误。 唯一的参数是字段名称:

.. literalinclude:: validation/028.php

指定通配符字段时,将检查所有匹配掩码的错误:

.. literalinclude:: validation/029.php

.. _validation-redirect-and-validation-errors:

重定向和验证错误
==============================

PHP 在请求之间不共享任何内容。 因此,如果验证失败然后重定向,
重定向请求中将没有验证错误,因为验证是在前一个请求中运行的。

在这种情况下,您需要使用 Form 辅助函数 :php:func:`validation_errors()`,
:php:func:`validation_list_errors()` 和 :php:func:`validation_show_error()`。
这些函数检查存储在会话中的验证错误。

要在会话中存储验证错误,您需要将 ``withInput()``
与 :php:func:`redirect() <redirect>` 一起使用:

.. literalinclude:: validation/042.php
   :lines: 2-

.. _validation-customizing-error-display:

*************************
自定义错误显示
*************************

当您调用 ``$validation->listErrors()`` 或 ``$validation->showError()`` 时,它在后台加载一个视图文件,该文件确定如何显示错误。 默认情况下,它们显示在 class 为 ``errors`` 的 div 容器中。
您可以轻松地创建新视图并在整个应用程序中使用它们。

创建视图
==================

第一步是创建自定义视图。 这些可以放在 ``view()`` 方法可以找到的任何位置,
这意味着标准视图目录或任何命名空间视图文件夹都可以使用。 例如,您可以在
**app/Views/_errors_list.php** 中创建一个新视图:

.. literalinclude:: validation/030.php

在视图内可以使用名为 ``$errors`` 的数组,其中包含错误列表,键是
有错误的字段名称,值是错误消息,如下所示:

.. literalinclude:: validation/031.php

实际上有两种类型的视图可以创建。 第一种具有所有错误的数组,我们刚刚看到了。
另一种更简单,只包含一个变量 ``$error``,其中包含错误消息。
这与 ``showError()`` 方法一起使用,其中必须指定一个字段,错误应属于该字段::

    <span class="help-block"><?= esc($error) ?></span>

配置
=============

一旦创建了自定义视图,就需要让 Validation 库知道它们。 打开 **app/Config/Validation.php**。
在里面,您会找到 ``$templates`` 属性,其中您可以列出尽可能多的自定义视图,并提供一个
它们可以通过的短别名。 如果我们要添加上面的示例文件,它会如下所示:

.. literalinclude:: validation/032.php

指定模板
=======================

您可以通过在 ``listErrors()`` 中作为第一个参数传递其别名来指定要使用的模板::

    <?= $validation->listErrors('my_list') ?>

显示特定字段的错误时,您可以将别名作为第二个参数传递给 ``showError()`` 方法,
紧跟着错误应属于的字段名称::

    <?= $validation->showError('username', 'my_single') ?>

*********************
创建自定义规则
*********************

.. _validation-using-rule-classes:

使用规则类
==================

规则存储在简单的带命名空间的类中。 它们可以存储在您想要的任何位置,只要
自动加载程序可以找到它即可。 这些文件称为 RuleSets。

添加 RuleSet
----------------

要添加新的 RuleSet,请编辑 **app/Config/Validation.php** 并
将新文件添加到 ``$ruleSets`` 数组中:

.. literalinclude:: validation/033.php

您可以将其添加为带有完全限定类名的简单字符串,或如
上所示使用 ``::class`` 后缀。 在更高级的 IDE 中,主要好处
在于它提供了一些额外的导航功能。

创建规则类
---------------------

在文件本身中,每个方法都是一条规则,必须接受要验证的值作为第一个参数,并且必须返回
一个布尔值 true 或 false,表示通过或失败测试。

.. literalinclude:: validation/034.php

默认情况下,系统将在 **system/Language/en/Validation.php** 中查找错误消息中使用的语言字符串。 在自定义规则中,您可以通过引用第二个参数 ``&$error`` 来提供错误消息:

.. literalinclude:: validation/035.php

使用自定义规则
-------------------

您的新自定义规则现在可以像任何其他规则一样使用:

.. literalinclude:: validation/036.php

允许参数
-------------------

如果您的方法需要使用参数,函数将需要至少三个参数:

1. 要验证的值 (``$value``)
2. 参数字符串 (``$params``)
3. 提交表单的所有数据的数组 (``$data``)
4. (可选)自定义错误字符串 (``&$error``),如上所述。

.. warning:: ``$data`` 中的字段值是未验证的(或可能无效的)。
    使用未验证的输入数据是漏洞的源泉。 在自定义规则中,在使用
    ``$data`` 中的数据之前,您必须执行必要的验证。

``$data`` 数组特别适用于根据其他提交字段的值来确定结果的规则,如 ``required_with``::

.. literalinclude:: validation/037.php

.. _validation-using-closure-rule:

使用闭包规则
==================

.. versionadded:: 4.3.0

如果您的应用程序中只需要自定义规则的功能一次,
则可以使用闭包而不是规则类。

您需要为验证规则使用数组:

.. literalinclude:: validation/040.php

您必须为闭包规则设置错误消息。
设置错误消息时,请为闭包规则设置数组键。
在上面的代码中,``required`` 规则的键为 ``0``,闭包的键为 ``1``。

或者可以使用以下参数:

.. literalinclude:: validation/041.php

***************
可用规则
***************

.. note:: 规则是一个字符串;参数之间不能有**空格**,尤其是 ``is_unique`` 规则。
    ``ignore_value`` 前后不能有空格。

.. literalinclude:: validation/038.php

常规使用的规则
=====================

以下是可用的所有原生规则列表:

======================= ========== ============================================= ===================================================
规则                    参数       描述                                         示例
======================= ========== ============================================= ===================================================
alpha                   无         如果字段包含字母表之外的字符,则失败。
alpha_space             无         如果字段包含字母和空格之外的字符,则失败。
alpha_dash              无         如果字段包含字母数字、下划线和破折号之外的字符,则失败。
alpha_numeric           无         如果字段包含字母数字之外的字符,则失败。
alpha_numeric_space     无         如果字段包含字母数字和空格之外的字符,则失败。
alpha_numeric_punct     无         如果字段包含字母数字、空格和以下限定标点集之外的字符,则失败: ``~`` (波浪符)、
                                   ``!`` (感叹号)、``#`` (数字符号)、
                                   ``$`` (美元符号)、``%`` (百分比)、``&`` (和符)、
                                   ``*`` (星号)、``-`` (破折号)、``_`` (下划线)、``+`` (加号)、
                                   ``=`` (等号)、``|`` (竖线)、``:`` (冒号)、``.`` (句点)。
decimal                 无         如果字段包含十进制数字之外的字符则失败。还接受 ``+`` 或
                                   ``-`` 号表示数字的正负。
differs                 是         如果字段的值与参数中的字段的值相同,则失败。  ``differs[field_name]``
exact_length            是         如果字段的长度不等于参数值则失败。一个或多个用逗号分隔的值。 ``exact_length[5]`` 或 ``exact_length[5,8,12]``
greater_than            是         如果字段小于或等于参数值或不是数字,则失败。 ``greater_than[8]``
greater_than_equal_to   是         如果字段小于参数值或不是数字,则失败。    ``greater_than_equal_to[5]``
hex                     无         如果字段包含十六进制字符之外的字符,则失败。
if_exist                无         如果存在此规则,则验证将仅在要验证的数据中存在字段键时检查该字段。
in_list                 是         如果字段不在预定列表中,则失败。           ``in_list[red,blue,green]``
integer                 无         如果字段包含整数之外的字符,则失败。
is_natural              无         如果字段包含自然数(0、1、2、3等)之外的字符,则失败。
is_natural_no_zero      无         如果字段包含零之外的自然数(1、2、3等)之外的字符,则失败。
is_not_unique           是         检查数据库中是否存在给定的值。可以通过字段/值过滤来忽略记录(当前只接受一个过滤器)。 ``is_not_unique[table.field,where_field,where_value]``
is_unique               是         检查此字段值是否存在于数据库中。 可选择设置要忽略的列和值,在更新记录时很有用,可忽略自身。 ``is_unique[table.field,ignore_field,ignore_value]``
less_than               是         如果字段大于或等于参数值或不是数字,则失败。 ``less_than[8]``
less_than_equal_to      是         如果字段大于参数值或不是数字,则失败。     ``less_than_equal_to[8]``
matches                 是         值必须与参数中字段的值匹配。                ``matches[field]``
max_length              是         如果字段长度超过参数值,则失败。            ``max_length[8]``
min_length              是         如果字段长度短于参数值,则失败。            ``min_length[3]``
not_in_list             是         如果字段在预定列表中,则失败。              ``not_in_list[red,blue,green]``
numeric                 无         如果字段包含非数字字符,则失败。
regex_match             是         如果字段不匹配正则表达式,则失败。          ``regex_match[/regex/]``
permit_empty            无         允许字段接收空数组、空字符串、null或false。
required                无         如果字段是一个空数组、空字符串、null或false,则失败。
required_with           是         当任何其他字段不是空的时,需要此字段。     ``required_with[field1,field2]``
required_without        是         当任何其他字段为空时,需要此字段。         ``required_without[field1,field2]``
string                  无         一个通用的 alpha* 规则的替代,确认元素是一个字符串
timezone                无         如果字段与 `timezone_identifiers_list()`_ 不匹配则失败
valid_base64            无         如果字段包含无效的Base64字符,则失败。
valid_json              无         如果字段不包含有效的JSON字符串,则失败。
valid_email             无         如果字段不包含有效的电子邮件地址,则失败。
valid_emails            无         如果以逗号分隔提供的任何值无效,则失败。
valid_ip                是         如果提供的IP无效则失败。可选择 ``ipv4`` 或 ``ipv6`` 参数指定IP格式。 ``valid_ip[ipv6]``
valid_url               无         如果字段不包含(宽松的)URL,则失败。包括可能是主机名的简单字符串,如“codeigniter”。
                                   **通常,应使用 ``valid_url_strict``。**
valid_url_strict        是         如果字段不包含有效的 URL,则失败。您可以可选地指定有效方案的列表。如果未指定,``http,https``
                                   有效。此规则使用 PHP 的 ``FILTER_VALIDATE_URL``。 ``valid_url_strict[https]``
valid_date              是         如果字段不包含有效日期,则失败。任何 `strtotime()`_ 接受的字符串如果不指定可选的参数匹配日期格式都是有效的。
                                   **所以通常有必要指定参数。**
valid_cc_number         Yes        验证信用卡号是否与指定提供商使用的格式匹配。 当前支持的提供商有:
                                   American Express (``amex``)、
                                   China Unionpay (``unionpay``)、
                                   Diners Club CarteBlance (``carteblanche``)、
                                   Diners Club (``dinersclub``)、
                                   Discover Card (``discover``)、
                                   Interpayment (``interpayment``)、
                                   JCB (``jcb``)、Maestro (``maestro``)、
                                   Dankort (``dankort``)、NSPK MIR (``mir``)、
                                   Troy (``troy``)、MasterCard (``mastercard``)、
                                   Visa (``visa``)

针对文件上传的规则
======================

这些验证规则使您可以执行上传文件是否符合业务需求的基本检查。
由于文件上传 HTML 字段的值不存在,并存储在 ``$_FILES`` 全局中,所以需要两次使用输入字段的名称。一次是作为任何其他规则的字段名称,一次是所有
与文件上传相关规则的第一个参数::

    // 在 HTML 中
    <input type="file" name="avatar">

    // 在控制器中
    $this->validate([
        'avatar' => 'uploaded[avatar]|max_size[avatar,1024]',
    ]);

======================= ========== ============================================= ===================================================
规则                    参数       描述                                         示例
======================= ========== ============================================= ===================================================
uploaded                是         如果参数的名称与任何上传文件的名称不匹配,则失败。 ``uploaded[field_name]``
max_size                是         如果名为参数的上传文件大于第二个参数(单位 kb)的大小,则失败。 或者如果文件大于 php.ini 配置文件中声明的
                                   最大大小 - ``upload_max_filesize`` 指令。
max_dims                是         如果上传图片的最大宽度和高度超过值,则失败。第一个参数是字段名称。第二个是宽度,第三个是高度。如果
                                   无法确定文件是图像,也会失败。
mime_in                 是         如果文件的 mime 类型不在参数中列出,则失败。 ``mime_in[field_name,image/png,image/jpeg]``
ext_in                  是         如果文件扩展名不在参数中列出,则失败。     ``ext_in[field_name,png,jpg,gif]``
is_image                是         如果根据 mime 类型无法确定文件是图像,则失败。 ``is_image[field_name]``
======================= ========== ============================================= ===================================================

文件验证规则适用于单文件和多文件上传。
