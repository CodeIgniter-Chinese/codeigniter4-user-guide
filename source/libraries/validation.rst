.. _validation:

##########
验证
##########

CodeIgniter 提供了一个全面的数据验证类,可以帮助 minimizing 你编写的代码量。

.. contents::
    :local:
    :depth: 2

********
概览
********

在解释 CodeIgniter 的数据验证方法之前,让我们描述一下理想的场景:

#. 显示一个表单。
#. 你填写表单并提交。
#. 如果你提交了无效的或缺少必需项的数据,表单会重新显示,并包含你的数据和描述问题的错误信息。
#. 这个过程会继续,直到你提交了一个有效的表单。

接收端必须:

#. 检查必需的数据。
#. 验证数据类型正确,并满足正确的标准。例如,如果提交了用户名,必须验证它只包含允许的字符。它必须有最小长度,并且不超过最大长度。用户名不能是其他人已存在的用户名,或者可能是保留字等。
#. 为安全起见对数据进行 sanitize。
#. 如果需要的话预格式化数据。
#. 准备数据以便插入数据库。

尽管上述过程没有非常复杂的地方,但通常需要大量的代码,为了显示错误信息,各种控制结构通常放在表单 HTML 中。表单验证虽简单但一般实现起来既混乱又乏味。

*************************
表单验证教程
*************************

以下是实现 CodeIgniter 表单验证的“动手”教程。

为了实现表单验证,你需要三件事:

#. 包含表单的 :doc:`视图 </outgoing/views>` 文件。
#. 包含成功提交的“成功”消息的视图文件。
#. :doc:`控制器 </incoming/controllers>` 方法来接收和处理提交的数据。

让我们创建这三件事,以会员注册表单为例。

表单
========

使用文本编辑器,创建一个名为 **signup.php** 的表单。在其中放入以下代码并保存到你的 **app/Views/** 文件夹::

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

使用文本编辑器,创建一个名为 **success.php** 的页面。在其中放入以下代码,并保存到你的 **app/Views/** 文件夹::

    <html>
    <head>
        <title>我的表单</title>
    </head>
    <body>

        <h3>你的表单已成功提交!</h3>

        <p><?= anchor('form', '再试一次!') ?></p>

    </body>
    </html>

控制器
==============

使用文本编辑器,创建一个名为 **Form.php** 的控制器。在其中放入以下代码,并保存到你的 **app/Controllers/** 文件夹:

.. literalinclude:: validation/001.php

.. note:: 从 v4.3.0 开始,可以使用 :ref:`$this->request->is() <incomingrequest-is>` 方法。
    在早期版本中,需要使用 ``if (strtolower($this->request->getMethod()) !== 'post')``。

.. note:: 自 v4.4.0 起，可以使用 :ref:`$this->validator->getValidated() <validation-getting-validated-data>` 方法。

路由
==========

然后在 **app/Config/Routes.php** 中为控制器添加路由:

.. literalinclude:: validation/039.php
   :lines: 2-

试一试!
=======

要测试你的表单,使用类似这样的 URL 访问你的网站::

    example.com/index.php/form/

如果提交表单,你应该只是简单地看到表单重新加载。这是因为你还没有在 :ref:`controller-validatedata` 中设置任何验证规则。

``validateData()`` 方法是控制器中的一个方法。它使用内部的 **验证类**。参见 :ref:`controller-validatedata`。

.. note:: 由于你还没有告诉 ``validateData()`` 方法要验证任何内容,它 **默认返回 false** (布尔值 false)。只有在成功应用你的规则且没有失败时, ``validateData()`` 方法才会返回 true。

解释
===========

你会注意到上面的页面有几件事。

signup.php
----------

表单(**signup.php**)是一个标准的网页表单,有一些例外:

#. 它使用 :doc:`表单辅助函数 </helpers/form_helper>` 来创建表单的开标签和闭标签。从技术上讲,这不是必需的。你可以使用标准 HTML 来创建表单。
   但是,使用辅助函数的好处是它会根据你的配置文件中的 URL 为你生成 action URL。这使得在 URL 变更的情况下你的应用更具可移植性。
#. 在表单顶部,你会注意到以下函数调用:
   ::

    <?= validation_list_errors() ?>

   这个函数将返回验证器发送回的任何错误消息。如果没有消息,它会返回一个空字符串。

Form.php
--------

控制器(**Form.php**)有一个属性:``$helpers``。
它加载了视图文件使用的表单辅助函数。

控制器有一个方法:``index()``。这个方法在收到非 POST 请求时返回 **signup** 视图以显示表单。否则,它使用控制器提供的 :ref:`controller-validatedata` 方法。它还运行验证例程。
根据验证是否成功,它要么显示表单,要么显示成功页面。

添加验证规则
====================

然后在控制器中添加验证规则(**Form.php**):

.. literalinclude:: validation/002.php
   :lines: 2-

如果提交表单,你应该看到成功页面或带错误消息的表单。

*********************
验证配置
*********************

.. _validation-traditional-and-strict-rules:

传统规则和严格规则
============================

CodeIgniter 4 有两种验证规则类。
传统规则类(**传统规则**)命名空间为 ``CodeIgniter\Validation``,
新的类(**严格规则**)命名空间为 ``CodeIgniter\Validation\StrictRules``,提供严格验证。

.. note:: 从 v4.3.0 开始,默认使用 **严格规则** 以获得更好的安全性。

传统规则
-----------------

.. important:: 传统规则只存在于向后兼容性。在新项目中不要使用它们。即使你已经在使用它们，我们也建议切换到严格规则。

.. warning:: 在验证包含非字符串值的数据时,比如 JSON 数据,推荐使用 **严格规则**。

**传统规则** 隐式地假设正在验证字符串值,输入值可能会隐式转换为字符串值。
它适用于大多数基本情况,如验证 POST 数据。

但是,例如,如果你使用 JSON 输入数据,它可能是 bool/null/array 类型。
当你使用传统规则类验证布尔值 ``true`` 时,它会被转换为字符串 ``'1'``。
如果使用 ``integer`` 规则对其进行验证, ``'1'`` 可以通过验证。

严格规则
------------

.. versionadded:: 4.2.0

**严格规则** 不使用隐式类型转换。

使用传统规则
-----------------------

如果你想使用传统规则,需要在 **app/Config/Validation.php** 中更改规则类:

.. literalinclude:: validation/003.php

*******************
加载库
*******************

该库以名为 **validation** 的服务加载:

.. literalinclude:: validation/004.php
   :lines: 2-

这会自动加载 ``Config\Validation`` 文件,其中包含用于包含多个 Rulesets 的设置,以及可以轻松重用的规则集合。

.. note:: 你可能永远不需要使用这个方法,因为 :doc:`控制器 </incoming/controllers>` 和
    :doc:`模型 </models/model>` 都提供了使验证更容易的方法。

************************
设置验证规则
************************

CodeIgniter 允许你根据需要为一个字段设置尽可能多的验证规则,级联地指定它们。要设置验证规则,
你将使用 ``setRule()``、``setRules()`` 或 ``withRequest()`` 方法。

设置单个规则
=====================

setRule()
---------

这个方法设置一个规则。它具有如下方法签名::

    setRule(string $field, ?string $label, array|string $rules[, array $errors = []])

``$rules`` 可以接收管道分隔的规则列表,或者规则数组:

.. literalinclude:: validation/005.php
   :lines: 2-

你传递给 ``$field`` 的值必须匹配传入数据数组的键。如果数据直接来自 ``$_POST``,那么它必须与表单输入名称完全匹配。

.. warning:: 在 v4.2.0 之前,这个方法的第三个参数 ``$rules`` 的类型提示是接收 ``string``。在 v4.2.0 及以后,类型提示被删除以允许数组。为避免在扩展类中覆盖此方法时违反 LSP,子类的方法也应修改为删除类型提示。

设置多个规则
======================

setRules()
----------

像 ``setRule()`` 一样,但接受字段名称及其规则的数组:

.. literalinclude:: validation/006.php
   :lines: 2-

要给出带标签的错误消息,可以设置如下:

.. literalinclude:: validation/007.php
   :lines: 2-

.. note:: ``setRules()`` 会覆盖先前设置的任何规则。要向现有规则集添加多个规则，请多次使用 ``setRule()``。

.. _validation-dot-array-syntax:

为数组数据设置规则
============================

如果你的数据在嵌套的关联数组中,你可以使用“点数组语法”来轻松验证数据:

.. literalinclude:: validation/009.php
   :lines: 2-

你可以使用通配符 ``*`` 符号匹配任意一层数组:

.. literalinclude:: validation/010.php
   :lines: 2-

.. note:: 在 v4.4.4 之前，由于一个错误，通配符 ``*`` 在错误的下标上验证了数据。详情请参见 :ref:`升级 <upgrade-444-validation-with-dot-array-syntax>`。

当你有单维数组数据时,"点数组语法"也很有用。
例如,下拉多选返回的数据:

.. literalinclude:: validation/011.php
   :lines: 2-

.. _validation-withrequest:

withRequest()
=============

.. important:: 该方法只存在于向后兼容性。在新项目中不要使用它。即使你已经在使用它，我们也建议你使用另一个更适合的方法。

.. warning:: 如果你只想验证 POST 数据，不要使用 ``withRequest()``。
    此方法使用 :ref:`$request->getVar() <incomingrequest-getting-data>`
    它按照该顺序返回 ``$_GET``, ``$_POST`` 或 ``$_COOKIE`` 数据
    （取决于 php.ini `request-order <https://www.php.net/manual/en/ini.core.php#ini.request-order>`_）。
    新的值会覆盖旧的值。如果它们具有相同的名称，POST 值可能会被
    Cookie 覆盖。

当验证从 HTTP 请求输入的数据时,你会最常使用验证库。如果需要的话,你可以传入当前请求对象的实例,它会获取所有输入数据并将其设置为要验证的数据:

.. literalinclude:: validation/008.php
   :lines: 2-

.. warning:: 当你使用此方法时，应使用 :ref:`getValidated() <validation-getting-validated-data>` 方法获取经过验证的数据。因为该方法从 :ref:`$request->getJSON() <incomingrequest-getting-json-data>` 获取 JSON 数据（当请求是 JSON 请求时，``Content-Type: application/json``），或者从 :ref:`$request->getRawInput() <incomingrequest-retrieving-raw-data>` 获取原始数据（当请求是 PUT、PATCH、DELETE 请求且不是 HTML 表单提交时，``Content-Type: multipart/form-data``），或者从 :ref:`$request->getVar() <incomingrequest-getting-data>` 获取数据，并且攻击者可以更改要验证的数据。

.. note:: 自 v4.4.0 起，可以使用 :ref:`getValidated() <validation-getting-validated-data>` 方法。

***********************
使用验证
***********************

运行验证
==================

``run()`` 方法运行验证。它有如下方法签名::

    run(?array $data = null, ?string $group = null, ?string $dbGroup = null): bool

``$data`` 是要验证的数据数组。可选的第二个参数
``$group`` 是要应用的 :ref:`预定义规则组 <validation-array>`。
可选的第三个参数 ``$dbGroup`` 是要使用的数据库组。

如果验证成功,该方法返回 true。

.. literalinclude:: validation/043.php
   :lines: 2-

运行多个验证
============================

.. note:: ``run()`` 方法不会重置错误状态。如果前一次运行失败, ``run()`` 将总是返回 false, ``getErrors()`` 将返回所有先前的错误,直到明确重置。

如果你打算运行多个验证,例如对不同的数据集或之后的规则,你可能需要在每次运行之前调用 ``$validation->reset()`` 来清除之前运行的错误。要注意 ``reset()`` 会使任何数据、规则或自定义错误无效,所以 ``setRules()``、``setRuleGroup()`` 等需要重复:

.. literalinclude:: validation/019.php
   :lines: 2-

验证单个值
==================

``check()`` 方法根据规则验证一个值。
第一个参数 ``$value`` 是要验证的值。第二个参数 ``$rule`` 是验证规则。
可选的第三个参数 ``$errors`` 是自定义错误消息。

.. literalinclude:: validation/012.php
   :lines: 2-

.. note:: 在 v4.4.0 之前，此方法的第二个参数 ``$rule`` 的类型提示为 ``string``。在 v4.4.0 及之后的版本中，类型提示被移除，允许接受数组。

.. note:: 此方法调用 ``setRule()`` 方法在内部设置规则。

.. _validation-getting-validated-data:

获取经过验证的数据
======================

.. versionadded:: 4.4.0

可以使用 ``getValidated()`` 方法获取实际经过验证的数据。
该方法返回一个仅包含已通过验证规则的元素的数组。

.. literalinclude:: validation/044.php
   :lines: 2-

.. literalinclude:: validation/045.php
   :lines: 2-

将一组验证规则保存到配置文件
==================================================

验证类的一个很好的特性是它允许你将所有验证规则存储在配置文件中。你可以按“组”组织规则。每次运行验证时,你都可以指定不同的组。

.. _validation-array:

如何保存规则
----------------------

要存储验证规则,只需在 ``Config\Validation`` 类中创建一个新的公共属性,名称为你的组名。这个元素将持有一个包含你的验证规则的数组。如前所示,验证数组的原型如下:

.. literalinclude:: validation/013.php

如何指定规则组
-------------------------

当调用 ``run()`` 方法时,你可以在第一个参数中指定要使用的组:

.. literalinclude:: validation/014.php
   :lines: 2-

如何保存错误消息
--------------------------

你也可以在此配置文件中存储自定义错误消息,方法是命名与组相同的属性,并追加 ``_errors``。这些将在使用该组时自动用于任何错误:

.. literalinclude:: validation/015.php

或者以数组形式传入所有设置:

.. literalinclude:: validation/016.php

参见 :ref:`validation-custom-errors` 了解数组格式的细节。

获取和设置规则组
-----------------------------

获取规则组
^^^^^^^^^^^^^^

此方法从验证配置中获取规则组:

.. literalinclude:: validation/017.php
   :lines: 2-

设置规则组
^^^^^^^^^^^^^^

此方法将验证配置中的规则组设置到验证服务中:

.. literalinclude:: validation/018.php
   :lines: 2-

.. _validation-placeholders:

验证占位符
=======================

验证类提供了一种简单的方法,基于传入的数据替换规则的一部分。这听起来比较模糊,但在使用 ``is_unique`` 验证规则时特别有用。占位符简单地是以花括号括起来的字段名(或数组键),该字段名作为 ``$data`` 传入。它将被传入字段的 **值** 所替换。以下示例将阐明这一点:

.. literalinclude:: validation/020.php
   :lines: 2-

.. note:: 从 v4.3.5 开始，出于安全考虑，你必须为占位符字段（上面示例代码中的 ``id`` 字段）设置验证规则。

在这组规则中,它说明电子邮件地址在数据库中应该是唯一的,除了具有与占位符的值匹配的 id 的行。假设表单 POST 数据如下:

.. literalinclude:: validation/021.php
   :lines: 2-

然后 ``{id}`` 占位符会被替换为数字 **4**,得到这条修改后的规则:

.. literalinclude:: validation/022.php
   :lines: 2-

所以在验证电子邮件唯一性时,它会忽略数据库中 ``id=4`` 的行。

.. note:: 从 v4.3.5 开始,如果占位符(``id``)的值未通过验证,占位符不会被替换。

只要传入的动态键不与表单数据冲突,这也可以在运行时用于创建更动态的规则。

*******************
处理错误
*******************

验证库提供了几种方法来帮助你设置错误消息、提供自定义错误消息以及检索一个或多个错误以显示。

默认情况下，错误消息来源于 **system/Language/en/Validation.php** 中的语言字符串，其中每个规则都有一个条目。如果你想要更改消息默认值，创建一个文件 **app/Language/en/Validation.php** （使用本地化对应的文件夹，替代 ``en``）
并在其中放置那些不同于默认值的错误消息的 Key 和值。

.. _validation-custom-errors:

设置自定义错误消息
=============================

``setRule()`` 和 ``setRules()`` 方法的最后一个参数都可以接受自定义消息数组,它将用于每个字段的特定错误。这允许对用户来说是非常愉快的体验,因为错误是针对每个实例定制的。如果没有提供自定义错误消息,将使用默认值。

有两种方式可以提供自定义错误消息。

作为最后一个参数:

.. literalinclude:: validation/023.php
   :lines: 2-

或者以标签样式:

.. literalinclude:: validation/024.php
   :lines: 2-

如果你想要包含字段的“人类”名称,或某些规则允许的可选参数(如 max_length),或者被验证的值,你可以分别在消息中添加 ``{field}``、``{param}`` 和 ``{value}`` 标签::

    'min_length' => '提供的 {field} 值 ({value}) 必须至少有 {param} 个字符。'

对一个人类名称为 Username、规则为 ``min_length[6]``、值为 "Pizza" 的字段,错误会显示:"提供的 Username 值 (Pizza) 必须至少有 6 个字符。"

.. warning:: 如果使用 ``getErrors()`` 或 ``getError()`` 获取错误消息,消息不会被 HTML 转义。如果使用像 ``({value})`` 这样的用户输入数据来制作错误消息,它可能包含 HTML 标签。如果你在显示之前不转义消息,可能存在 XSS 攻击。

.. note:: 当使用标签样式的错误消息时,如果你向 ``setRules()`` 传递第二个参数,它将被第一个参数的值覆盖。

翻译消息和验证标签
============================================

要使用语言文件中的翻译字符串,我们可以简单地使用点语法。
假设我们有一个位于这里的翻译文件:**app/Languages/en/Rules.php**。
我们可以简单地使用这个文件中定义的语言行,像这样:

.. literalinclude:: validation/025.php
   :lines: 2-

.. _validation-getting-all-errors:

获取所有错误
==================

如果你需要检索所有失败字段的错误消息,可以使用 ``getErrors()`` 方法:

.. literalinclude:: validation/026.php
   :lines: 2-

如果没有错误,将返回一个空数组。

当使用通配符 (``*``) 时,错误将指向特定的字段,用适当的键替换通配符::

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
    'contacts.friends.1.name' => 'contacts.friends.*.name 字段是必需的。'

获取单个错误
======================

你可以使用 ``getError()`` 方法检索单个字段的错误。唯一的参数是字段名称:

.. literalinclude:: validation/027.php
   :lines: 2-

如果没有错误,将返回一个空字符串。

.. note:: 当使用通配符时,所有匹配通配符的找到的错误将组合成一行,以 EOL 字符分隔。

检查错误是否存在
=====================

你可以使用 ``hasError()`` 方法检查是否存在错误。唯一的参数是字段名称:

.. literalinclude:: validation/028.php
   :lines: 2-

当指定使用通配符的字段时,将检查匹配通配符的所有错误:

.. literalinclude:: validation/029.php
   :lines: 2-

.. _validation-redirect-and-validation-errors:

重定向和验证错误
==============================

PHP 请求之间不共享任何内容。所以在验证失败时重定向,重定向的请求中将没有验证错误,因为验证是在前一个请求中运行的。

在这种情况下,你需要使用表单辅助函数 :php:func:`validation_errors()`、:php:func:`validation_list_errors()` 和 :php:func:`validation_show_error()`。
这些函数检查存储在会话中的验证错误。

要在会话中存储验证错误,你需要在 :php:func:`redirect()` 中使用 ``withInput()``:

.. literalinclude:: validation/042.php
   :lines: 2-

.. _validation-customizing-error-display:

*************************
自定义错误显示
*************************

当你调用 ``$validation->listErrors()`` 或 ``$validation->showError()`` 时,它会在后台加载一个视图文件,该文件确定如何显示错误。默认情况下,它们显示在一个 class 为 ``errors`` 的 div 中。你可以轻松地创建新视图并在整个应用中使用它们。

创建视图
==================

第一步是创建自定义视图。可以将这些视图放在 ``view()`` 方法可以找到的任何位置,这意味着标准的视图目录或任何命名空间视图文件夹都可以工作。例如,你可以在 **app/Views/_errors_list.php** 创建一个新视图:

.. literalinclude:: validation/030.php

在视图内可以使用名为 ``$errors`` 的数组,它包含错误列表,其中键是有错误的字段名称,值是错误消息,像这样:

.. literalinclude:: validation/031.php
   :lines: 2-

实际上有两种类型的视图你可以创建。第一种具有所有错误的数组,这就是我们刚才看到的。另一种更简单,只包含一个名为 ``$error`` 的变量,其中包含错误消息。这在使用 ``showError()`` 方法时使用,该方法必须指定错误属于的字段::

    <span class="help-block"><?= esc($error) ?></span>

配置
=============

一旦你创建了视图,就需要让 Validation 库知道它们。打开 **app/Config/Validation.php**。
在里面,你会找到 ``$templates`` 属性,你可以在其中列出尽可能多的自定义视图,并提供一个它们可以通过的简短别名。如果我们要添加上面例子中的文件,它会是这样:

.. literalinclude:: validation/032.php

指定模板
=======================

你可以通过在 ``listErrors()`` 中作为第一个参数传递其别名来指定要使用的模板::

    <?= $validation->listErrors('my_list') ?>

当显示特定字段的错误时,可以将别名作为 ``showError()`` 方法的第二个参数传递,紧跟着错误所属字段的名称::

    <?= $validation->showError('username', 'my_single') ?>

*********************
创建自定义规则
*********************

.. _validation-using-rule-classes:

使用规则类
==================

规则存储在简单的命名空间类中。可以将它们存储在自动加载程序可以找到的任何位置。这些文件称为规则集。

添加规则集
----------------

要添加新的规则集,请编辑 **app/Config/Validation.php** 并将新文件添加到 ``$ruleSets`` 数组中:

.. literalinclude:: validation/033.php

你可以像上面显示的那样添加完整限定的类名的简单字符串,或使用 ``::class`` 后缀。这里的主要好处是在更高级的 IDE 中提供了一些额外的导航功能。

创建规则类
---------------------

在文件本身中,每个方法都是一条规则,必须接受要验证的值作为第一个参数,并返回一个布尔真或假值,表示如果通过测试则为真,否则为假:

.. literalinclude:: validation/034.php

默认情况下，系统会在 **system/Language/en/Validation.php** 中查找错误中使用的语言字符串。为了为你的自定义规则提供默认的错误消息，你可以将它们放在 **app/Language/en/Validation.php** 中（使用本地化对应的文件夹，替代 ``en``）。另外，如果你想使用其他语言字符串文件替代默认的 **Validation.php**，你可以通过接受一个 ``&$error`` 变量（作为第二个参数，或者，如果你的规则需要处理参数，如下所述 - 第四个参数）来提供错误消息：

.. literalinclude:: validation/035.php

使用自定义规则
-------------------

你的新自定义规则现在可以像任何其他规则一样使用了:

.. literalinclude:: validation/036.php
   :lines: 2-

允许参数
-------------------

如果你的方法需要使用参数,函数需要至少三个参数:

1. 要验证的值(``$value``)
2. 参数字符串(``$params``)
3. 提交表单的所有数据的数组(``$data``)
4. (可选)自定义错误字符串(``&$error``),如上所述

.. warning:: ``$data`` 中的值是未验证的(或可能无效的)。使用未验证的输入数据是漏洞的源头。你必须在自定义规则内对 ``$data`` 中的数据执行必要的验证,然后再使用它。

``$data`` 数组对需要检查提交的其他字段的值来确定结果的规则特别有用,比如 ``required_with`` :

.. literalinclude:: validation/037.php

.. _validation-using-closure-rule:

使用闭包规则
==================

.. versionadded:: 4.3.0

如果你的应用中只需要自定义规则的功能一次,你可以使用闭包 instead of 规则类。

你需要为验证规则使用数组:

.. literalinclude:: validation/040.php
   :lines: 2-

你必须为闭包规则设置错误消息。
设置错误消息时,请为闭包规则设置数组键。
在上面的代码中, ``required`` 规则的键为 ``0``,闭包的键为 ``1``。

或者可以使用以下参数:

.. literalinclude:: validation/041.php
   :lines: 2-

***************
可用规则
***************

.. note:: 规则是一个字符串;参数之间绝不能有 **空格**,特别是 ``is_unique`` 规则。
    ``ignore_value`` 前后不能有空格。

.. literalinclude:: validation/038.php
   :lines: 2-

常规规则
=====================

以下是可用的所有原生规则列表:

======================= ========== ================================================================= ===================================================
规则                    参数       描述                                                              示例
======================= ========== ================================================================= ===================================================
alpha                   无         如果字段包含除 ASCII 字母字符之外的任何内容,则失败。
alpha_space             无         如果字段包含 ASCII 空格和字母字符之外的任何内容,则失败。
alpha_dash              无         如果字段包含除 ASCII 字母数字字符、下划线或破折号之外的任何内容,
                                   则失败。
alpha_numeric           无         如果字段包含除 ASCII 字母数字字符之外的任何内容,则失败。
alpha_numeric_space     无         如果字段包含除 ASCII 字母数字和空格字符之外的任何内容,则失败。
alpha_numeric_punct     无         如果字段包含除字母数字、空格和这组有限标点之外的任何内容,
                                   则失败:``~`` (波浪号)、
                                   ``!`` (感叹号)、``#`` (数字)、
                                   ``$`` (美元符号), ``%`` (百分号), ``&`` (和号),
                                   ``*`` (星号), ``-`` (破折号),
                                   ``_`` (下划线), ``+`` (加号),
                                   ``=`` (等号), ``|`` (竖线),
                                   ``:`` (冒号), ``.`` (句点)。
decimal                 无         如果字段包含除十进制数字外的任何内容,则失败。
                                   也接受数字前的 ``+`` 或 ``-`` 号。
differs                 是         如果字段与参数中字段的值不不同,则失败。                           ``differs[field_name]``
exact_length            是         如果字段的长度不完全等于参数值,则失败。                           ``exact_length[5]`` 或 ``exact_length[5,8,12]``
greater_than            是         如果字段小于或等于参数值,或不是数字,则失败。                      ``greater_than[8]``
greater_than_equal_to   是         如果字段小于参数值,或不是数字,则失败。                            ``greater_than_equal_to[5]``
hex                     无         如果字段包含除十六进制字符之外的任何内容,则失败。
if_exist                无         如果存在此规则,验证将仅在要验证的数据中存在字段键时检查该字段。
in_list                 是         如果字段不在预定列表中,则失败。                                   ``in_list[red,blue,green]``
integer                 无         如果字段包含除整数之外的任何内容,则失败。
is_natural              无         如果字段包含除自然数之外的任何内容,则失败:0, 1, 2, 3等。
is_natural_no_zero      无         如果字段包含除自然数和零之外的任何内容,则失败:1, 2, 3等。
is_not_unique           是         检查数据库中是否存在给定的值。
                                   可以通过字段/值过滤器忽略记录(当前只接受一个过滤器)。
is_unique               是         检查字段值是否存在于数据库中。可以可选地设置要忽略的列和值,
                                   在更新记录时很有用,忽略它本身。
less_than               是         如果字段大于或等于参数值,或不是数字,则失败。                      ``less_than[8]``
less_than_equal_to      是         如果字段大于参数值,或不是数字,则失败。                            ``less_than_equal_to[8]``
matches                 是         值必须匹配参数中字段的值。                                        ``matches[field]``
max_length              是         如果字段长于参数值,则失败。                                       ``max_length[8]``
min_length              是         如果字段短于参数值,则失败。                                       ``min_length[3]``
not_in_list             是         如果字段在预定列表中,则失败。                                     ``not_in_list[red,blue,green]``
numeric                 无         如果字段包含除数字外的任何内容,则失败。
regex_match             是         如果字段不匹配正则表达式,则失败。                                 ``regex_match[/regex/]``
permit_empty            无         允许字段接收空数组、空字符串、null 或 false。
required                无         如果字段为空数组、空字符串、null 或 false,则失败。
required_with           是         当数据中任何其他字段不为空时,该字段是必需的。                     ``required_with[field1,field2]``
required_without        是         当数据中任何其他字段为空时,该字段是必需的。                       ``required_without[field1,field2]``
string                  无         alpha* 规则的通用替代,确认元素是一个字符串。
timezone                无         如果字段不匹配 `timezone_identifiers_list()`_ 中的时区,则失败。
valid_base64            无         如果字段包含除有效的 Base64 字符之外的任何内容,则失败。
valid_json              无         如果字段不包含有效的 JSON 字符串,则失败。
valid_email             无         如果字段不包含有效的电子邮件地址,则失败。
valid_emails            无         如果任何以逗号分隔提供的值不是有效的电子邮件,则失败。
valid_ip                是         如果提供的 IP 无效,则失败。
                                   可选参数为 ``ipv4`` 或 ``valid_ip[ipv6]``
                                   ``ipv6`` 以指定 IP 格式。
valid_url               无         如果字段不包含(宽松的)URL,则失败。
                                   包括可能是主机名的简单字符串,
                                   如“codeigniter”。**通常,应使用** ``valid_url_strict``。
valid_url_strict        是         如果字段不包含有效的 URL,则失败。你可以可选地指定                 ``valid_url_strict[https]``
                                   有效 schema 的列表。如果未指定, ``http,https``
                                   有效。此规则使用 PHP 的 ``FILTER_VALIDATE_URL``。
valid_date              是         如果字段不包含有效日期,则失败。任何 `strtotime()`_                ``valid_date[d/m/Y]``
                                   接受的字符串如果不指定可选参数以匹配日期格式都是
                                   有效的。**所以通常有必要指定参数。**
valid_cc_number         是         验证信用卡号是否与指定提供程序使用的格式匹配。                    ``valid_cc_number[amex]``
                                   当前支持的提供程序有:
                                   美国运通 (``amex``)、
                                   中国银联 (``unionpay``)、
                                   Diners Club CarteBlance (``carteblanche``)、
                                   Diners Club (``dinersclub``)、
                                   Discover Card (``discover``)、
                                   Interpayment (``interpayment``)、
                                   JCB (``jcb``)、 Maestro (``maestro``)、
                                   丹麦银行的 Dankort (``dankort``)、 NSPK MIR (``mir``)、
                                   Troy (``troy``)、 MasterCard (``mastercard``)、
                                   Visa (``visa``)、 UATP (``uatp``)、
                                   Verve (``verve``)、
                                   CIBC 便利卡 (``cibc``)、
                                   罗伊银行客户卡 (``rbc``)、
                                   TD Canada Trust 访问卡 (``tdtrust``)、
                                   Scotiabank 圣哥伦布卡 (``scotia``)、
                                   BMO 自动柜员机卡 (``bmoabm``)、
                                   HSBC 加拿大卡 (``hsbc``)
======================= ========== ================================================================= ===================================================

.. note:: 你也可以使用任何返回布尔值且至少接受一个要验证的数据的参数的原生 PHP 函数。
    验证库 **从不改变** 要验证的数据。

.. _timezone_identifiers_list(): https://www.php.net/manual/en/function.timezone-identifiers-list.php
.. _strtotime(): https://www.php.net/manual/en/function.strtotime.php
.. _empty(): https://www.php.net/manual/en/function.empty.php

.. _rules-for-file-uploads:

文件上传规则
======================

当你验证上传的文件时，必须使用专门为文件验证创建的规则。

.. important:: 只有下表中列出的规则可以用于验证文件。因此，如果在文件验证规则数组或字符串中添加任何通用规则，如 ``permit_empty``，文件验证将无法正确工作。

由于文件上传 HTML 字段的值不存在,而是存储在 ``$_FILES`` 全局变量中,所以需要两次使用输入字段的名称。一次是像其他规则一样指定字段名称,另一次是作为所有与文件上传相关规则的第一个参数::

    // 在 HTML 中
    <input type="file" name="avatar">

    // 在控制器中
    $this->validate([
        'avatar' => 'uploaded[avatar]|max_size[avatar,1024]',
    ]);

======================= ========== ============================================================ ===================================================
规则                    参数       描述                                                         示例
======================= ========== ============================================================ ===================================================
uploaded                是         如果参数的名称与任何上传文件的名称不匹配，则会失败。         ``uploaded[field_name]``
                                   如果你希望文件上传是可选的（不是必需的），则不要定义此规则。
max_size                是         如果名为参数的上传文件大于第二个参数的千字节(kb),则失败。
                                   或者如果文件大于 php.ini 配置文件中声明的
                                   最大大小 - ``upload_max_filesize`` 指令。
max_dims                是         如果上传图像的最大宽度和高度超过值,则失败。
                                   第一个参数是字段名称。
                                   第二个是宽度,第三个是高度。如果无法确定文件是图像,也会失败。
mime_in                 是         如果文件的 mime 类型不在参数中列出,则失败。                  ``mime_in[field_name,image/png,image/jpeg]``
ext_in                  是         如果文件扩展名不在参数中列出,则失败。                        ``ext_in[field_name,png,jpg,gif]``
is_image                是         如果根据 mime 类型无法确定文件是图像,则失败。                ``is_image[field_name]``
======================= ========== ============================================================ ===================================================

文件验证规则适用于单个和多个文件上传。
