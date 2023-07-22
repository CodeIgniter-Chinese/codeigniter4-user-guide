############
表单辅助函数
############

表单辅助函数文件包含了帮助处理表单的函数。

.. contents::
    :local:
    :depth: 2

*************
配置
*************

从 v4.3.0 开始,``form_helper`` 函数中的空 HTML 元素(如 ``<input>``)默认为兼容 HTML5,如果你需要兼容 XHTML,必须在 **app/Config/DocTypes.php** 中将 ``$html5`` 属性设置为 ``false``。

*******************
加载此辅助函数
*******************

使用以下代码加载此辅助函数:

.. literalinclude:: form_helper/001.php

*********************
转义字段值
*********************

你可能需要在表单元素中使用 HTML 和诸如引号之类的字符。为了安全地做到这一点,你需要使用
:doc:`common function <../general/common_functions>`
:php:func:`esc()`。

考虑以下示例:

.. literalinclude:: form_helper/002.php

由于上面的字符串包含一组引号,它会导致表单中断。:php:func:`esc()` 函数将 HTML 特殊字符转换,以便可以安全使用::

    <input type="text" name="myfield" value="<?= esc($string) ?>">

.. note:: 如果使用此页面上列出的任何表单辅助函数,并以关联数组的形式传递值,则表单值将自动转义,因此不需要调用此函数。只有在以字符串形式创建自己的表单元素时,才需要调用它。

*******************
可用函数
*******************

以下函数可用:

.. php:function:: form_open([$action = ''[, $attributes = ''[, $hidden = []]]])

    :param    string    $action: 表单操作/目标 URI 字符串
    :param    mixed    $attributes: HTML 属性,作为数组或转义的字符串
    :param    array    $hidden: 隐藏字段定义的数组
    :returns:    一个 HTML 表单开启标签
    :rtype:    string

    使用从 **Config\App::$baseURL** 构建的站点 URL 创建一个开启的表单标签。它将可选地允许你添加表单属性和隐藏的输入字段,并将始终根据配置文件中的 charset 值添加 `accept-charset` 属性。

    与硬编码你自己的 HTML 相比,使用此标签的主要好处在于,如果你的 URL 改变,它允许你的站点更便携。

    这里是一个简单的例子:

    .. literalinclude:: form_helper/003.php

    上面的示例将创建一个指向你的站点 URL 加上 “email/send” URI 段的表单,如下::

        <form action="http://example.com/index.php/email/send" method="post" accept-charset="utf-8">

    你也可以像下面这样添加 ``{locale}`` :

    .. literalinclude:: form_helper/004.php

    上面的示例将创建一个指向你的站点 URL 加上当前请求区域设置和 “email/send” URI 段的表单,如下::

        <form action="http://example.com/index.php/en/email/send" method="post" accept-charset="utf-8">

    **添加属性**

        可以通过将关联数组作为第二个参数传递来添加属性,如下所示:

        .. literalinclude:: form_helper/005.php

        或者,你可以将第二个参数指定为字符串:

        .. literalinclude:: form_helper/006.php

        上面的示例将创建一个类似以下的表单::

            <form action="http://example.com/index.php/email/send" class="email" id="myform" method="post" accept-charset="utf-8">

        如果 :ref:`CSRF <cross-site-request-forgery>` 过滤器已打开,``form_open()`` 将在表单开头生成 CSRF 字段。你可以通过传递 csrf_id 作为 ``$attribute`` 数组的一部分来指定此字段的 ID:

        .. literalinclude:: form_helper/007.php

        将返回::

            <form action="http://example.com/index.php/u/sign-up" method="post" accept-charset="utf-8">
            <input type="hidden" id="my-id" name="csrf_field" value="964ede6e0ae8a680f7b8eab69136717d">

        .. note:: 要使用 CSRF 字段的自动生成,你需要打开表单页面的 CSRF 过滤器。在大多数情况下,它使用 ``GET`` 方法请求。

    **添加隐藏输入字段**

        可以通过将关联数组作为第三个参数传递来添加隐藏字段,如下所示:

        .. literalinclude:: form_helper/008.php

        你可以通过向它传递任何 false 值来跳过第二个参数。

        上面的示例将创建一个类似以下的表单::

            <form action="http://example.com/index.php/email/send" method="post" accept-charset="utf-8">
                <input type="hidden" name="username" value="Joe">
                <input type="hidden" name="member_id" value="234">

.. php:function:: form_open_multipart([$action = ''[, $attributes = ''[, $hidden = []]]])

    :param    string    $action: 表单操作/目标 URI 字符串
    :param    mixed    $attributes: HTML 属性,作为数组或转义的字符串
    :param    array    $hidden: 隐藏字段定义的数组
    :returns:    一个 HTML 多部分表单开启标签
    :rtype:    string

    此函数与上面的 :php:func:`form_open()` 完全相同,除了它添加了一个 *multipart* 属性,如果你想使用表单上传文件,这是必需的。

.. php:function:: form_hidden($name[, $value = ''])

    :param    string    $name: 字段名称
    :param    string    $value: 字段值
    :returns:    一个 HTML 隐藏输入字段标签
    :rtype:    string

    让你生成隐藏的输入字段。你可以提交名称/值字符串以创建一个字段:

    .. literalinclude:: form_helper/009.php

    ... 或者你可以提交一个关联数组来创建多个字段:

    .. literalinclude:: form_helper/010.php

    你也可以将关联数组传递给值字段:

    .. literalinclude:: form_helper/011.php

    如果你想要带有额外属性的隐藏输入字段:

    .. literalinclude:: form_helper/012.php

.. php:function:: form_input([$data = ''[, $value = ''[, $extra = ''[, $type = 'text']]]])

    :param    array    $data: 字段属性数据
    :param    string    $value: 字段值
    :param    mixed    $extra: 要作为数组或字符串添加到标记的额外属性
    :param    string    $type: 输入字段的类型。即,'text'、'email'、'number'等
    :returns:    一个 HTML 文本输入字段标签
    :rtype:    string

    允许你生成标准的文本输入字段。你可以至少在第一个和第二个参数中传递字段名称和值:

    .. literalinclude:: form_helper/013.php

    或者你可以传递一个包含你希望表单包含的任何数据的关联数组:

    .. literalinclude:: form_helper/014.php

    如果你想要布尔属性,请传递布尔值(``true``/``false``)。在这种情况下,布尔值无关紧要:

    .. literalinclude:: form_helper/035.php

    如果你希望你的表单包含一些额外的数据,如 JavaScript,你可以将其作为第三个参数中的字符串传递:

    .. literalinclude:: form_helper/015.php

    或者你可以传递它作为数组:

    .. literalinclude:: form_helper/016.php

    为了支持扩展的 HTML5 输入字段范围,你可以将输入类型作为第四个参数传递:

    .. literalinclude:: form_helper/017.php

.. php:function:: form_password([$data = ''[, $value = ''[, $extra = '']]])

    :param    array    $data: 字段属性数据
    :param    string    $value: 字段值
    :param    mixed    $extra: 要作为数组或字符串添加到标记的额外属性
    :returns:    一个 HTML 密码输入字段标签
    :rtype:    string

    此函数在所有方面与上面的 :php:func:`form_input()` 函数相同,只是它使用 “password” 输入类型。

.. php:function:: form_upload([$data = ''[, $value = ''[, $extra = '']]])

    :param    array    $data: 字段属性数据
    :param    string    $value: 字段值
    :param    mixed    $extra: 要作为数组或字符串添加到标记的额外属性
    :returns:    一个 HTML 文件上传输入字段标签
    :rtype:    string

    此函数在所有方面与上面的 :php:func:`form_input()` 函数相同,只是它使用 “file” 输入类型,允许它用于上传文件。

.. php:function:: form_textarea([$data = ''[, $value = ''[, $extra = '']]])

    :param    array    $data: 字段属性数据
    :param    string    $value: 字段值
    :param    mixed    $extra: 要作为数组或字符串添加到标记的额外属性
    :returns:    一个 HTML textarea 标签
    :rtype:    string

    此函数在所有方面与上面的 :php:func:`form_input()` 函数相同,只是它生成一个 “textarea” 类型。

    .. note:: 与上面的示例中的 *maxlength* 和 *size* 属性不同,你将指定 *rows* 和 *cols*。

.. php:function:: form_dropdown([$name = ''[, $options = [][, $selected = [][, $extra = '']]]])

    :param    string    $name: 字段名称
    :param    array    $options: 要列出的选项的关联数组
    :param    array    $selected: 要标记为 *selected* 属性的字段列表
    :param    mixed    $extra: 要作为数组或字符串添加到标记的额外属性
    :returns:    一个 HTML 下拉选择字段标签
    :rtype:    string

    允许你创建一个标准的下拉字段。第一个参数将包含字段的名称,第二个参数将包含选项的关联数组,第三个参数将包含你希望选中的值。你还可以通过第三个参数传递多个项的数组,辅助函数将为你创建一个多选字段。

    示例:

    .. literalinclude:: form_helper/018.php

    如果你希望打开的 <select> 包含额外的数据,如 id 属性或 JavaScript,你可以将其作为第四个参数中的字符串传递:

    .. literalinclude:: form_helper/019.php

    或者你可以传入它作为数组:

    .. literalinclude:: form_helper/020.php

    如果作为 ``$options`` 传递的数组是多维数组,那么 ``form_dropdown()`` 将使用数组键作为标签生产一个 <optgroup>。

.. php:function:: form_multiselect([$name = ''[, $options = [][, $selected = [][, $extra = '']]]])

    :param    string    $name: 字段名称
    :param    array    $options: 要列出的选项的关联数组
    :param    array    $selected: 要标记为 *selected* 属性的字段列表
    :param    mixed    $extra: 要作为数组或字符串添加到标记的额外属性
    :returns:    一个 HTML 下拉多选字段标签
    :rtype:    string

    允许你创建一个标准的多选字段。第一个参数将包含字段的名称,第二个参数将包含选项的关联数组,第三个参数将包含你希望选中的值或值。

    参数用法与使用上面的 :php:func:`form_dropdown()` 相同,当然字段名称需要使用 POST 数组语法,例如 foo[]。

.. php:function:: form_fieldset([$legend_text = ''[, $attributes = []]])

    :param    string    $legend_text: 要放入 <legend> 标签中的文本
    :param    array    $attributes: 要在 <fieldset> 标签上设置的属性
    :returns:    一个 HTML fieldset 开启标签
    :rtype:    string

    允许你生成 fieldset/legend 字段。

    示例:

    .. literalinclude:: form_helper/021.php

    与其他函数类似,如果你希望设置其他属性,可以在第二个参数中提交关联数组:

    .. literalinclude:: form_helper/022.php

.. php:function:: form_fieldset_close([$extra = ''])

    :param    string    $extra: 在关闭标签后要追加的任何内容,*原样*
    :returns:    一个 HTML fieldset 关闭标签
    :rtype:    string

    产生一个关闭的 ``</fieldset>`` 标签。使用此函数的唯一优点是它允许你向其传递将添加在标签下方的数据。例如

    .. literalinclude:: form_helper/023.php

.. php:function:: form_checkbox([$data = ''[, $value = ''[, $checked = false[, $extra = '']]]])

    :param    array    $data: 字段属性数据
    :param    string    $value: 字段值
    :param    bool    $checked: 是否将复选框标记为 *checked*
    :param    mixed    $extra: 要作为数组或字符串添加到标记的额外属性
    :returns:    一个 HTML 复选框输入标签
    :rtype:    string

    允许你生成一个复选框字段。简单示例:

    .. literalinclude:: form_helper/024.php

    第三个参数包含一个布尔值 true/false 以确定是否应选中该框。

    与此辅助函数中的其他表单函数类似,你也可以在第一个参数中传递属性的关联数组:

    .. literalinclude:: form_helper/025.php

    与其他函数一样,如果你希望标签包含其他数据,如 JavaScript,可以将其作为第四个参数中的字符串传递:

    .. literalinclude:: form_helper/026.php

    或者你可以传递它作为数组:

    .. literalinclude:: form_helper/027.php

.. php:function:: form_radio([$data = ''[, $value = ''[, $checked = false[, $extra = '']]]])

    :param    array    $data: 字段属性数据
    :param    string    $value: 字段值
    :param    bool    $checked: 是否将单选按钮标记为 *checked*
    :param    mixed    $extra: 要作为数组或字符串添加到标记的额外属性
    :returns:    一个 HTML 单选按钮输入标签
    :rtype:    string

    此函数在所有方面与上面的 :php:func:`form_checkbox()` 函数相同,只是它使用 “radio” 输入类型。

.. php:function:: form_label([$label_text = ''[, $id = ''[, $attributes = []]]])

    :param    string    $label_text: 要放入 <label> 标签中的文本
    :param    string    $id: 我们为其创建标签的表单元素的 ID
    :param    string    $attributes: HTML 属性
    :returns:    一个 HTML 字段标签
    :rtype:    string

    生成一个 <label>。简单示例:

    .. literalinclude:: form_helper/028.php

    与其他函数类似,如果你更喜欢设置其他属性,可以在第三个参数中提交关联数组。

    例子:

    .. literalinclude:: form_helper/029.php

.. php:function:: form_submit([$data = ''[, $value = ''[, $extra = '']]])

    :param    string    $data: 按钮名称
    :param    string    $value: 按钮值
    :param    mixed    $extra: 要作为数组或字符串添加到标记的额外属性
    :returns:    一个 HTML 输入提交标签
    :rtype:    string

    允许你生成一个标准的提交按钮。简单示例:

    .. literalinclude:: form_helper/030.php

    与其他函数类似,如果你更喜欢设置自己的属性,可以在第一个参数中提交关联数组。第三个参数允许你向表单添加额外数据,如 JavaScript。

.. php:function:: form_reset([$data = ''[, $value = ''[, $extra = '']]])

    :param    string    $data: 按钮名称
    :param    string    $value: 按钮值
    :param    mixed    $extra: 要作为数组或字符串添加到标记的额外属性
    :returns:    一个 HTML 输入重置按钮标签
    :rtype:    string

    允许你生成一个标准的重置按钮。用法与 :php:func:`form_submit()` 相同。

.. php:function:: form_button([$data = ''[, $content = ''[, $extra = '']]])

    :param    string    $data: 按钮名称
    :param    string    $content: 按钮标签
    :param    mixed    $extra: 要作为数组或字符串添加到标记的额外属性
    :returns:    一个 HTML 按钮标签
    :rtype:    string

    允许你生成一个标准的按钮元素。你可以至少在第一个和第二个参数中传递按钮名称和内容:

    .. literalinclude:: form_helper/031.php

    或者你可以传递一个关联数组,其中包含你希望表单包含的任何数据:

    .. literalinclude:: form_helper/032.php

    如果你希望表单包含一些额外的数据,如 JavaScript,可以将其作为第三个参数中的字符串传递:

    .. literalinclude:: form_helper/033.php

.. php:function:: form_close([$extra = ''])

    :param    string    $extra: 在关闭标签后要追加的任何内容,*原样*
    :returns:    一个 HTML 表单关闭标签
    :rtype:    string

    产生一个关闭的 ``</form>`` 标签。使用此函数的唯一优点是它允许你向其传递将添加在标签下方的数据。例如:

    .. literalinclude:: form_helper/034.php

.. php:function:: set_value($field[, $default = ''[, $html_escape = true]])

    :param    string    $field: 字段名称
    :param    string    $default: 默认值
    :param    bool    $html_escape: 是否关闭 HTML 转义值
    :returns:    字段值
    :rtype:    string

    允许你设置输入表单或文本区域的值。你必须通过函数的第一个参数提供字段名称。第二个(可选)参数允许你为表单设置默认值。第三个(可选)参数允许你关闭值的 HTML 转义,以防你需要将此函数与 :php:func:`form_input()` 结合使用以避免双重转义。

    示例::

        <input type="text" name="quantity" value="<?= set_value('quantity', '0') ?>" size="50">

    上面的表单在首次加载时将显示“0”。

.. php:function:: set_select($field[, $value = ''[, $default = false]])

    :param    string    $field: 字段名称
    :param    string    $value: 要检查的值
    :param    string    $default: 值是否也是默认值
    :returns:    'selected' 属性或空字符串
    :rtype:    string

    如果使用 <select> 菜单,此函数允许你显示所选菜单项。

    第一个参数必须包含选择菜单的名称,第二个参数必须包含每个项目的值,第三个(可选)参数允许你将某个项目设置为默认值(使用布尔值 true/false)。

    示例::

        <select name="myselect">
            <option value="one" <?= set_select('myselect', 'one', true) ?>>One</option>
            <option value="two" <?= set_select('myselect', 'two') ?>>Two</option>
            <option value="three" <?= set_select('myselect', 'three') ?>>Three</option>
        </select>

.. php:function:: set_checkbox($field[, $value = ''[, $default = false]])

    :param    string    $field: 字段名称
    :param    string    $value: 要检查的值
    :param    string    $default: 值是否也是默认值
    :returns:    'checked' 属性或空字符串
    :rtype:    string

    允许你以提交的状态显示复选框。

    第一个参数必须包含复选框的名称,第二个参数必须包含它的值,第三个(可选)参数允许你将某个项目设置为默认值(使用布尔值 true/false)。

    示例::

        <input type="checkbox" name="mycheck" value="1" <?= set_checkbox('mycheck', '1') ?>>
        <input type="checkbox" name="mycheck" value="2" <?= set_checkbox('mycheck', '2') ?>>

.. php:function:: set_radio($field[, $value = ''[, $default = false]])

    :param    string    $field: 字段名称
    :param    string    $value: 要检查的值
    :param    string    $default: 值是否也是默认值
    :returns:    'checked' 属性或空字符串
    :rtype:    string

    允许你以提交的状态显示单选按钮。这个函数在所有方面与上面的 :php:func:`set_checkbox()` 函数相同。

    示例::

        <input type="radio" name="myradio" value="1" <?= set_radio('myradio', '1', true) ?>>
        <input type="radio" name="myradio" value="2" <?= set_radio('myradio', '2') ?>>

.. php:function:: validation_errors()

    .. versionadded:: 4.3.0

    :returns:   验证错误
    :rtype:    array

    返回验证错误。首先,此函数检查存储在会话中的验证错误。要在会话中存储错误,需要与 :php:func:`redirect() <redirect>` 一起使用 ``withInput()``。

    返回的数组与 ``Validation::getErrors()`` 相同。详见 :ref:`验证 <validation-redirect-and-validation-errors>`。

    示例::

        <?php $errors = validation_errors(); ?>

.. php:function:: validation_list_errors($template = 'list')

    .. versionadded:: 4.3.0

    :param    string    $template: 验证模板名称
    :returns:    验证错误的渲染 HTML
    :rtype:    string

    返回验证错误的渲染 HTML。

    参数 ``$template`` 是一个验证模板名称。详见 :ref:`validation-customizing-error-display`。

    此函数在内部使用 :php:func:`validation_errors()`。

    示例::

        <?= validation_list_errors() ?>

.. php:function:: validation_show_error($field, $template = 'single')

    .. versionadded:: 4.3.0

    :param    string    $field: 字段名称
    :param    string    $template: 验证模板名称
    :returns:    格式化的验证错误 HTML
    :rtype:    string

    为指定字段以格式化的 HTML 返回单个错误。

    参数 ``$template`` 是一个验证模板名称。详见 :ref:`validation-customizing-error-display`。

    此函数在内部使用 :php:func:`validation_errors()`。

    示例::

        <?= validation_show_error('username') ?>
