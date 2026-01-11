############
表单辅助函数
############

表单辅助函数文件包含有助于处理表单的函数。

.. contents::
    :local:
    :depth: 2

*************
配置
*************

自 v4.3.0 起，``form_helper`` 函数中的空 HTML 元素（如 ``<input>``）默认已更改为 HTML5 兼容模式。如果需要与 XHTML 兼容，必须将 **app/Config/DocTypes.php** 中的 ``$html5`` 属性设置为 ``false``。

*******************
加载此辅助函数
*******************

使用以下代码加载此辅助函数：

.. literalinclude:: form_helper/001.php

*********************
转义字段值
*********************

可能需要在表单元素中使用 HTML 和引号等字符。为了安全地执行此操作，需要使用
:doc:`通用函数 <../general/common_functions>`
:php:func:`esc()`。

考虑以下示例：

.. literalinclude:: form_helper/002.php

由于上述字符串包含一组引号，会导致表单损坏。
:php:func:`esc()` 函数转换 HTML 特殊字符，使其可以安全使用::

    <input type="text" name="myfield" value="<?= esc($string) ?>">

.. note:: 如果使用本页列出的任何表单辅助函数，并以关联数组形式传递值，
    表单值将自动转义，因此无需调用此函数。
    仅在创建自己的表单元素（以字符串形式传递）时才需要使用它。

*******************
可用函数
*******************

提供以下函数：

.. php:function:: form_open([$action = ''[, $attributes = ''[, $hidden = []]]])

    :param    string    $action: 表单 action/目标 URI 字符串
    :param    mixed    $attributes: HTML 属性，作为数组或已转义的字符串
    :param    array    $hidden: 隐藏字段的定义数组
    :returns:    HTML 表单起始标签
    :rtype:    string

    创建一个带有 URL 的表单起始标签，该 URL 基于 ``Config\App::$baseURL`` 构建。
    可以选择添加表单属性和隐藏输入字段，并且会始终根据
    **app/Config/App.php** 配置文件中的 ``$charset`` 属性添加 `accept-charset` 属性。

    使用此标签而不是硬编码 HTML 的主要好处是，它允许你的网站在 URL 更改时具有更好的可移植性。

    简单示例：

    .. literalinclude:: form_helper/003.php

    以上示例将创建一个指向你的站点 URL 加上 "email/send" URI 段的表单，如下所示::

        <form action="http://example.com/index.php/email/send" method="post" accept-charset="utf-8">

    也可以添加 ``{locale}``，如下所示：

    .. literalinclude:: form_helper/004.php

    以上示例将创建一个指向你的站点 URL 加上当前请求语言环境和 "email/send" URI 段的表单，如下所示::

        <form action="http://example.com/index.php/en/email/send" method="post" accept-charset="utf-8">

    **添加属性**

        可以通过向第二个参数传递关联数组来添加属性，如下所示：

        .. literalinclude:: form_helper/005.php

        或者，可以将第二个参数指定为字符串：

        .. literalinclude:: form_helper/006.php

        以上示例将创建一个类似如下的表单::

            <form action="http://example.com/index.php/email/send" class="email" id="myform" method="post" accept-charset="utf-8">

        如果启用 :ref:`CSRF <cross-site-request-forgery>` 过滤器，``form_open()`` 将在表单开头生成 CSRF 字段。
        可以通过将 **csrf_id** 作为 ``$attributes`` 数组的元素来指定此字段的 ID：

        .. literalinclude:: form_helper/007.php

        将返回::

            <form action="http://example.com/index.php/u/sign-up" method="post" accept-charset="utf-8">
            <input type="hidden" id="my-id" name="csrf_test_name" value="964ede6e0ae8a680f7b8eab69136717d">

        .. note:: 要使用 CSRF 字段的自动生成功能，需要在 **app/Config/Filters.php** 文件中启用 :ref:`CSRF 过滤器 <enable-csrf-protection>`。
            在大多数情况下，表单页面使用 GET 方法请求。通常，POST/PUT/DELETE/PATCH 请求需要 CSRF 保护，
            但即使对于 GET 请求，显示表单的页面也必须启用 CSRF 过滤器。

            如果通过 :ref:`filters-globals` 启用 CSRF 过滤器，它将对所有请求类型有效。
            但如果使用 ``public array $methods = ['POST' => ['csrf']];`` 启用 CSRF 过滤器，则不会在 GET 请求中添加隐藏的 CSRF 字段。

    **添加隐藏输入字段**

        可以通过向第三个参数传递关联数组来添加隐藏字段，如下所示：

        .. literalinclude:: form_helper/008.php

        可以通过向第二个参数传递任何 false 值来跳过它。

        以上示例将创建一个类似如下的表单::

            <form action="http://example.com/index.php/email/send" method="post" accept-charset="utf-8">
                <input type="hidden" name="username" value="Joe">
                <input type="hidden" name="member_id" value="234">

.. php:function:: form_open_multipart([$action = ''[, $attributes = ''[, $hidden = []]]])

    :param    string    $action: 表单 action/目标 URI 字符串
    :param    mixed    $attributes: HTML 属性，作为数组或已转义的字符串
    :param    array    $hidden: 隐藏字段的定义数组
    :returns:    HTML multipart 表单起始标签
    :rtype:    string

    此函数与上面的 :php:func:`form_open()` 完全相同，
    只是它添加了 *multipart* 属性，如果你想使用表单上传文件，这是必需的。

.. php:function:: form_hidden($name[, $value = ''])

    :param    string    $name: 字段名称
    :param    string    $value: 字段值
    :returns:    HTML 隐藏输入元素
    :rtype:    string

    生成隐藏输入字段。可以提交名称/值字符串来创建一个字段：

    .. literalinclude:: form_helper/009.php

    ... 或者可以提交关联数组来创建多个字段：

    .. literalinclude:: form_helper/010.php

    也可以向值字段传递关联数组：

    .. literalinclude:: form_helper/011.php

    如果要创建带有额外属性的隐藏输入字段：

    .. literalinclude:: form_helper/012.php

.. php:function:: form_input([$data = ''[, $value = ''[, $extra = ''[, $type = 'text']]]])

    :param    array    $data: 字段属性数据
    :param    string    $value: 字段值
    :param    mixed    $extra: 要添加到标签的额外属性，作为数组或字面字符串
    :param  string  $type: 输入字段的类型。例如，'text'、'email'、'number' 等
    :returns:    HTML 文本输入元素
    :rtype:    string

    生成标准文本输入字段。可以最少在第一个和第二个参数中传递字段名称和值：

    .. literalinclude:: form_helper/013.php

    或者可以传递包含希望表单包含的任何数据的关联数组：

    .. literalinclude:: form_helper/014.php

    如果需要布尔属性，传递布尔值（``true``/``false``）。在这种情况下，布尔值无关紧要：

    .. literalinclude:: form_helper/035.php

    如果希望表单包含一些额外数据，如 JavaScript，可以在第三个参数中将其作为字符串传递：

    .. literalinclude:: form_helper/015.php

    或者可以将其作为数组传递：

    .. literalinclude:: form_helper/016.php

    为了支持扩展范围的 HTML5 输入字段，可以在第四个参数中传递输入类型：

    .. literalinclude:: form_helper/017.php

.. php:function:: form_password([$data = ''[, $value = ''[, $extra = '']]])

    :param    array    $data: 字段属性数据
    :param    string    $value: 字段值
    :param    mixed    $extra: 要添加到标签的额外属性（可以是一个数组或一个字符串）
    :returns:    HTML 密码输入元素
    :rtype:    string

    此函数在所有方面都与上面的 :php:func:`form_input()` 函数相同，
    只是它使用 "password" 输入类型。

.. php:function:: form_upload([$data = ''[, $value = ''[, $extra = '']]])

    :param    array    $data: 字段属性数据
    :param    string    $value: 字段值
    :param    mixed    $extra: 要添加到标签的额外属性（可以是一个数组或一个字符串）
    :returns:    HTML 文件上传输入元素
    :rtype:    string

    此函数在所有方面都与上面的 :php:func:`form_input()` 函数相同，
    只是它使用 "file" 输入类型，允许它用于上传文件。

.. php:function:: form_textarea([$data = ''[, $value = ''[, $extra = '']]])

    :param    array    $data: 字段属性数据
    :param    string    $value: 字段值
    :param    mixed    $extra: 要添加到标签的额外属性（可以是一个数组或一个字符串）
    :returns:    HTML textarea 元素
    :rtype:    string

    此函数在所有方面都与上面的 :php:func:`form_input()` 函数相同，
    只是它生成 "textarea" 类型。

    .. note:: 在上面的示例中，需要指定 *rows* 和 *cols* 属性，而不是 *maxlength* 和 *size* 属性。

.. php:function:: form_dropdown([$name = ''[, $options = [][, $selected = [][, $extra = '']]]])

    :param    string    $name: 字段名称
    :param    array    $options: 要列出的选项的关联数组
    :param    array    $selected: 用 *selected* 属性标记的字段列表
    :param    mixed    $extra: 要添加到标签的额外属性（可以是一个数组或一个字符串）
    :returns:    HTML select（下拉框）元素
    :rtype:    string

    创建标准下拉框字段。第一个参数将包含字段名称，第二个参数将包含选项的关联数组，
    第三个参数将包含希望选择的值。也可以通过第三个参数传递多个项目的数组，
    辅助函数将为你创建多选。

    示例：

    .. literalinclude:: form_helper/018.php

    如果希望起始 <select> 标签包含额外数据，如 id 属性或 JavaScript，
    可以在第四个参数中将其作为字符串传递：

    .. literalinclude:: form_helper/019.php

    或者可以将其作为数组传递：

    .. literalinclude:: form_helper/020.php

    如果作为 ``$options`` 传递的数组是多维数组，那么
    ``form_dropdown()`` 将生成一个 <optgroup>，以数组键作为标签。

.. php:function:: form_multiselect([$name = ''[, $options = [][, $selected = [][, $extra = '']]]])

    :param    string    $name: 字段名称
    :param    array    $options: 要列出的选项的关联数组
    :param    array    $selected: 用 *selected* 属性标记的字段列表
    :param    mixed    $extra: 要添加到标签的额外属性（可以是一个数组或一个字符串）
    :returns:    带有 multiple 属性的 HTML select 元素
    :rtype:    string

    创建标准多选字段。第一个参数将包含字段名称，第二个参数将包含选项的关联数组，
    第三个参数将包含希望选择的值。

    参数使用与上面的 :php:func:`form_dropdown()` 相同，
    当然，字段名称需要使用 POST 数组语法，例如 foo[]。

.. php:function:: form_fieldset([$legend_text = ''[, $attributes = []]])

    :param    string    $legend_text: 要放在 <legend> 标签中的文本
    :param    array    $attributes: 要设置在 <fieldset> 标签上的属性
    :returns:    HTML fieldset 开始标签
    :rtype:    string

    生成 fieldset/legend 字段。

    示例：

    .. literalinclude:: form_helper/021.php

    与其他函数类似，如果希望设置额外属性，可以在第二个参数中提交关联数组：

    .. literalinclude:: form_helper/022.php

.. php:function:: form_fieldset_close([$extra = ''])

    :param    string    $extra: 在闭合标签之后追加的任何内容（*按原样输出*）
    :returns:    HTML fieldset 闭合标签
    :rtype:    string

    生成闭合 ``</fieldset>`` 标签。使用此函数的唯一好处是，它可以传递数据，
    这些数据将被添加到标签下方。例如

    .. literalinclude:: form_helper/023.php

.. php:function:: form_checkbox([$data = ''[, $value = ''[, $checked = false[, $extra = '']]]])

    :param    array    $data: 字段属性数据
    :param    string    $value: 字段值
    :param    bool    $checked: 是否将复选框标记为 *checked*
    :param    mixed    $extra: 要添加到标签的额外属性（可以是一个数组或一个字符串）
    :returns:    HTML 复选框输入元素
    :rtype:    string

    生成复选框字段。简单示例：

    .. literalinclude:: form_helper/024.php

    第三个参数包含布尔值 true/false，以确定是否应该选中复选框。

    与此辅助函数中的其他表单函数类似，也可以向函数传递属性数组：

    .. literalinclude:: form_helper/025.php

    与其他函数一样，如果希望标签包含如 JavaScript 等额外数据，
    可以在第四个参数中将其作为字符串传递：

    .. literalinclude:: form_helper/026.php

    或者可以将其作为数组传递：

    .. literalinclude:: form_helper/027.php

.. php:function:: form_radio([$data = ''[, $value = ''[, $checked = false[, $extra = '']]]])

    :param    array    $data: 字段属性数据
    :param    string    $value: 字段值
    :param    bool    $checked: 是否将单选按钮标记为 *checked*
    :param    mixed    $extra: 要添加到标签的额外属性（可以是一个数组或一个字符串）
    :returns:    HTML 单选输入元素
    :rtype:    string

    此函数在所有方面都与上面的 :php:func:`form_checkbox()` 函数相同，
    只是它使用 "radio" 输入类型。

.. php:function:: form_label([$label_text = ''[, $id = ''[, $attributes = []]]])

    :param    string    $label_text: 要放在 <label> 标签中的文本
    :param    string    $id: 正在为其创建标签的表单元素的 ID
    :param    string    $attributes: HTML 属性
    :returns:    HTML label 元素
    :rtype:    string

    生成 <label>。简单示例：

    .. literalinclude:: form_helper/028.php

    与其他函数类似，如果希望设置额外属性，可以在第三个参数中提交关联数组。

    示例：

    .. literalinclude:: form_helper/029.php

.. php:function:: form_submit([$data = ''[, $value = ''[, $extra = '']]])

    :param    string    $data: 按钮名称
    :param    string    $value: 按钮值
    :param    mixed    $extra: 要添加到标签的额外属性（可以是一个数组或一个字符串）
    :returns:    HTML input submit 元素
    :rtype:    string

    生成标准提交按钮。简单示例：

    .. literalinclude:: form_helper/030.php

    与其他函数类似，如果希望设置自己的属性，可以在第一个参数中提交关联数组。
    第三个参数允许向表单添加额外数据，如 JavaScript。

.. php:function:: form_reset([$data = ''[, $value = ''[, $extra = '']]])

    :param    string    $data: 按钮名称
    :param    string    $value: 按钮值
    :param    mixed    $extra: 要添加到标签的额外属性（可以是一个数组或一个字符串）
    :returns:    HTML input reset 元素
    :rtype:    string

    生成标准重置按钮。使用方式与 :func:`form_submit()` 相同。

.. php:function:: form_button([$data = ''[, $content = ''[, $extra = '']]])

    :param    string    $data: 按钮名称
    :param    string    $content: 按钮标签
    :param    mixed    $extra: 要添加到标签的额外属性（可以是一个数组或一个字符串）
    :returns:    HTML button 元素
    :rtype:    string

    生成标准按钮元素。可以最少在第一个和第二个参数中传递按钮名称和内容：

    .. literalinclude:: form_helper/031.php

    或者，你可以传入一个关联数组，其中包含你希望表单中包含的任何数据：

    .. literalinclude:: form_helper/032.php

    如果希望表单包含一些额外数据，如 JavaScript，可以在第三个参数中将其作为字符串传递：

    .. literalinclude:: form_helper/033.php

.. php:function:: form_close([$extra = ''])

    :param    string    $extra: 在闭合标签之后追加的任何内容（*按原样输出*）
    :returns:    HTML 表单闭合标签
    :rtype:    string

    生成闭合 ``</form>`` 标签。使用此函数的唯一好处是，它可以传递数据，
    这些数据将被添加到标签下方。例如：

    .. literalinclude:: form_helper/034.php

.. php:function:: set_value($field[, $default = ''[, $html_escape = true]])

    :param    string    $field: 字段名称
    :param    string    $default: 默认值
    :param  bool    $html_escape: 是否对该值禁用 HTML 转义
    :returns:    字段值
    :rtype:    string

    允许设置 input 或 textarea 元素的值。必须通过函数的第一个参数提供字段名称。
    第二个（可选）参数允许为字段值设置默认值。第三个（可选）参数允许禁用 HTML 转义，
    以防你需要将此函数与 :php:func:`form_input()` 等函数结合使用，从而避免双重转义。

    示例::

        <input type="text" name="quantity" value="<?= set_value('quantity', '0') ?>" size="50">

    以上表单在首次加载时将显示 "0"。

.. php:function:: set_select($field[, $value = ''[, $default = false]])

    :param    string    $field: 字段名称
    :param    string    $value: 要检查的值
    :param    string    $default: 该值是否也是默认值
    :returns:    'selected' 属性或空字符串
    :rtype:    string

    如果使用 <select> 菜单，此函数允许显示已选择的菜单项。

    第一个参数必须包含选择菜单的名称，第二个参数必须包含每个项目的值，
    第三个（可选）参数允许将项目设置为默认值（使用布尔值 true/false）。

    示例::

        <select name="myselect">
            <option value="one" <?= set_select('myselect', 'one', true) ?>>One</option>
            <option value="two" <?= set_select('myselect', 'two') ?>>Two</option>
            <option value="three" <?= set_select('myselect', 'three') ?>>Three</option>
        </select>

.. php:function:: set_checkbox($field[, $value = ''[, $default = false]])

    :param    string    $field: 字段名称
    :param    string    $value: 要检查的值
    :param    string    $default: 该值是否也是默认值
    :returns:    'checked' 属性或空字符串
    :rtype:    string

    允许显示复选框在提交时的状态。

    第一个参数必须包含复选框的名称，第二个参数必须包含其值，
    第三个（可选）参数允许将项目设置为默认值（使用布尔值 true/false）。

    示例::

        <input type="checkbox" name="mycheck[]" value="1" <?= set_checkbox('mycheck', '1') ?>>
        <input type="checkbox" name="mycheck[]" value="2" <?= set_checkbox('mycheck', '2') ?>>

.. php:function:: set_radio($field[, $value = ''[, $default = false]])

    :param    string    $field: 字段名称
    :param    string    $value: 要检查的值
    :param    string    $default: 该值是否也是默认值
    :returns:    'checked' 属性或空字符串
    :rtype:    string

    允许显示单选按钮在提交时的状态。此函数与上面的 :php:func:`set_checkbox()` 函数相同。

    示例::

        <input type="radio" name="myradio" value="1" <?= set_radio('myradio', '1', true) ?>>
        <input type="radio" name="myradio" value="2" <?= set_radio('myradio', '2') ?>>

.. php:function:: validation_errors()

    .. versionadded:: 4.3.0

    :returns:   验证错误
    :rtype:    array

    返回验证错误。首先，此函数检查存储在 Session 中的验证错误。
    要将错误存储在 Session 中，需要将 ``withInput()`` 与 :php:func:`redirect() <redirect>` 一起使用。

    返回的数组与 ``Validation::getErrors()`` 相同。
    详细信息请参见 :ref:`验证 <validation-redirect-and-validation-errors>`。

    .. note:: 此函数不适用于 :ref:`in-model-validation`。
        如果要获取模型验证中的验证错误，请参见
        :ref:`model-getting-validation-errors`。

    示例::

        <?php $errors = validation_errors(); ?>

.. php:function:: validation_list_errors($template = 'list')

    .. versionadded:: 4.3.0

    :param    string    $template: 验证模板名称
    :returns:    验证错误的渲染 HTML
    :rtype:    string

    返回验证错误渲染后的 HTML。

    参数 ``$template`` 是验证模板名称。
    详细信息请参见 :ref:`validation-customizing-error-display`。

    此函数内部使用 :php:func:`validation_errors()`。

    .. note:: 此函数不适用于 :ref:`in-model-validation`。
        如果要获取模型验证中的验证错误，请参见
        :ref:`model-getting-validation-errors`。

    示例::

        <?= validation_list_errors() ?>

.. php:function:: validation_show_error($field, $template = 'single')

    .. versionadded:: 4.3.0

    :param    string    $field: 字段名称
    :param    string    $template: 验证模板名称
    :returns:    验证错误渲染后的 HTML
    :rtype:    string

    以格式化的 HTML 形式返回指定字段的单个错误。

    参数 ``$template`` 是验证模板名称。
    详细信息请参见 :ref:`validation-customizing-error-display`。

    此函数内部使用 :php:func:`validation_errors()`。

    .. note:: 此函数不适用于 :ref:`in-model-validation`。
        如果要获取模型验证中的验证错误，请参见
        :ref:`model-getting-validation-errors`。

    示例::

        <?= validation_show_error('username') ?>
