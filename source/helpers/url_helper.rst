############
URL 辅助函数
############

URL 辅助函数文件包含协助处理 URL 的函数。

.. contents::
    :local:
    :depth: 2

加载此辅助函数
===================

此辅助函数由框架在每个请求时自动加载。

可用函数
===================

提供以下函数：

.. php:function:: site_url([$uri = ''[, $protocol = null[, $altConfig = null]]])

    :param  array|string         $uri: URI 字符串或 URI 段数组。
    :param  string        $protocol: 协议，例如 ``'http'`` 或 ``'https'``。如果设置为空字符串 ``''``，则返回协议相对链接。
    :param  \\Config\\App $altConfig: 要使用的备用配置。
    :returns: 站点 URL
    :rtype:    string

    .. note:: 自 v4.3.0 起，如果设置了 ``Config\App::$allowedHostnames``,
        且当前 URL 匹配，则返回设置了主机名的 URL。

    返回配置文件中指定的站点 URL。**index.php**
    文件（或在配置文件中设置的站点 ``Config\App::$indexPage``）将添加到 URL 中，
    传递给函数的任何 URI 段也会添加到 URL 中。

    建议在需要生成本地 URL 时使用此函数，以便在 URL 发生变化时，
    页面具有更好的可移植性。

    段可以作为字符串或数组选择性地传递给函数。以下是一个字符串示例：

    .. literalinclude:: url_helper/001.php

    上面的示例会返回类似这样的内容：
    **http://example.com/index.php/news/local/123**

    以下是作为数组传递段的示例：

    .. literalinclude:: url_helper/002.php

    为不同配置偏好的站点生成 URL 时，备用配置会很有用。
    我们使用它来对框架本身进行单元测试。

.. php:function:: base_url([$uri = ''[, $protocol = null]])

    :param  array|string   $uri: URI 字符串或 URI 段数组。
    :param  string  $protocol: 协议，例如 ``'http'`` 或 ``'https'``。如果设置为空字符串 ``''``，则返回协议相对链接。
    :returns: 基础 URL
    :rtype: string

    .. note:: 自 v4.3.0 起，如果设置了 ``Config\App::$allowedHostnames``,
        且当前 URL 匹配，则返回设置了主机名的 URL。

    .. note:: 在之前的版本中，此函数在无参数调用时返回不带尾部
        斜杠 (``/``) 的基础 URL。该错误已修复，
        自 v4.3.2 起返回带尾部斜杠的基础 URL。

    返回配置文件中指定的站点基础 URL。示例：

    .. literalinclude:: url_helper/003.php

    此函数返回与 :php:func:`site_url()` 相同的内容，
    但不附加 ``Config\App::$indexPage``。

    与 :php:func:`site_url()` 类似，你可以以字符串或数组的形式提供段。
    以下是一个字符串示例：

    .. literalinclude:: url_helper/004.php

    上面的示例会返回类似这样的内容：
    **http://example.com/blog/post/123**

    如果你传递空字符串 ``''`` 作为第二个参数，它会返回
    协议相对链接：

    .. literalinclude:: url_helper/026.php

    这很有用，因为与 :php:func:`site_url()` 不同，你可以提供
    文件的字符串，例如图像或样式表。例如：

    .. literalinclude:: url_helper/005.php

    这会给你类似这样的内容：
    **http://example.com/images/icons/edit.png**

.. php:function:: current_url([$returnObject = false[, $request = null]])

    :param    boolean    $returnObject: 如果你希望返回 URI 实例而不是字符串，则为 true。
    :param    IncomingRequest|null    $request: 用于路径检测的备用请求；对测试很有用。
    :returns: 当前 URL
    :rtype:    string|\\CodeIgniter\\HTTP\\URI

    返回当前正在浏览页面的完整 URL。
    返回字符串时，会移除 URL 的查询和片段部分。
    返回 URI 时，会保留查询和片段部分。

    然而，出于安全原因，它是基于 ``Config\App`` 设置创建的，
    并不打算与浏览器 URL 匹配。

    自 v4.3.0 起，如果设置了 ``Config\App::$allowedHostnames``,
    且当前 URL 匹配，则返回设置了主机名的 URL。

    .. note:: 调用 ``current_url()`` 相当于执行以下操作：

        .. literalinclude:: url_helper/006.php
           :lines: 2-

    .. important:: 在 v4.1.2 之前，此函数存在一个错误，导致它忽略 ``Config\App::$indexPage`` 配置项。

.. php:function:: previous_url([$returnObject = false])

    :param boolean $returnObject: 如果你希望返回 URI 实例而不是字符串，则为 true。
    :returns: 用户之前访问的 URL
    :rtype: string|\\CodeIgniter\\HTTP\\URI

    返回用户之前访问页面的完整 URL（包括段）。

    .. note:: 由于盲目信任 ``HTTP_REFERER`` 系统变量存在安全问题，
        CodeIgniter 会在 Session 可用时将之前访问的页面存储在其中。
        这确保我们始终使用已知和可信的来源。
        如果 Session 尚未加载或不可用，则会使用过滤后的 ``HTTP_REFERER``。

.. php:function:: uri_string()

    :returns: URI 字符串
    :rtype:   string

    返回相对于 baseURL 的当前 URL 的路径部分。

    例如，当你的 baseURL 是 **http://some-site.com/** 而当前 URL 是::

        http://some-site.com/blog/comments/123

    函数会返回::

        blog/comments/123

    当你的 baseURL 是 **http://some-site.com/subfolder/** 而当前 URL 是::

        http://some-site.com/subfolder/blog/comments/123

    函数会返回::

        blog/comments/123

    .. note:: 在之前的版本中，定义了参数 ``$relative = false``。
        然而，由于一个错误，此函数始终返回相对于 baseURL 的路径。
        自 v4.3.2 起，该参数已被移除。

    .. note:: 在之前的版本中，当你导航到 baseURL 时，此函数
        返回 ``/``。自 v4.3.2 起，该错误已修复，它返回
        空字符串 (``''``)。

.. php:function:: index_page([$altConfig = null])

    :param \\Config\\App $altConfig: 要使用的备用配置
    :returns:  ``indexPage`` 值
    :rtype:    string

    返回配置文件中指定的站点 **indexPage**。
    示例：

    .. literalinclude:: url_helper/007.php

    与 :php:func:`site_url()` 类似，你可以指定备用配置。
    为不同配置偏好的站点生成 URL 时，备用配置会很有用。
    我们使用它来对框架本身进行单元测试。

.. php:function:: anchor([$uri = ''[, $title = ''[, $attributes = ''[, $altConfig = null]]]])

    :param  array|string        $uri: URI 字符串或 URI 段数组
    :param  string              $title: 锚点标题
    :param  array|object|string $attributes: HTML 属性
    :param  \\Config\\App|null  $altConfig: 要使用的备用配置
    :returns: HTML 超链接（锚点标签）
    :rtype:    string

    基于你的本地站点 URL 创建标准 HTML 锚点链接。

    第一个参数可以包含你希望附加到 URL 的任何段。
    与上面的 :php:func:`site_url()` 函数类似，段可以是字符串或数组。

    .. note:: 如果你正在构建应用程序内部的链接，
        不要包含基础 URL (``http://...``)。这将根据配置文件中指定的信息
        自动添加。只包含你希望附加到 URL 的 URI 段。

    第二个段是你希望链接显示的文本。如果留空，将使用 URL。

    第三个参数可以包含你希望添加到链接的属性列表。
    属性可以是简单的字符串或关联数组。

    以下是一些示例：

    .. literalinclude:: url_helper/008.php

    与上面类似，你可以指定备用配置。
    在为与你的站点不同的、包含不同配置偏好的站点生成链接时，
    你可能会发现备用配置很有用。我们使用它来对框架本身进行单元测试。

    .. note:: 传递给 anchor 函数的属性会自动转义以防止 XSS 攻击。

.. php:function:: anchor_popup([$uri = ''[, $title = ''[, $attributes = false[, $altConfig = null]]]])

    :param  string          $uri: URI 字符串
    :param  string          $title: 锚点标题
    :param  array|false|object|string $attributes: HTML 属性
    :param  \\Config\\App   $altConfig: 要使用的备用配置
    :returns: 弹出式超链接
    :rtype: string

    与 :php:func:`anchor()` 函数几乎相同，不同之处在于它
    在新窗口中打开 URL。你可以在第三个参数中指定 JavaScript 窗口
    属性来控制窗口的打开方式。
    如果未设置第三个参数，它将只使用你自己的浏览器设置打开新窗口。

    以下是带属性的示例：

    .. literalinclude:: url_helper/009.php

    与上面类似，你可以指定备用配置。
    在为与你的站点不同的、包含不同配置偏好的站点生成链接时，
    你可能会发现备用配置很有用。我们使用它来对框架本身进行单元测试。

    .. note:: 上述属性是函数的默认值，所以你只需要
        设置与你需求不同的属性。如果你希望
        函数使用其所有默认值，只需在第三个参数中传递一个空数组：

        .. literalinclude:: url_helper/010.php

    .. note:: **window_name** 不是真正的属性，而是 JavaScript `window.open() <https://www.w3schools.com/jsref/met_win_open.asp>`_
        方法的参数，该方法接受窗口名称或窗口目标。

    .. note:: 除上面列出的属性外的任何其他属性将被解析为
        锚点标签的 HTML 属性。

    .. note:: 传递给 anchor_popup 函数的属性会自动转义以防止 XSS 攻击。

.. php:function:: mailto($email[, $title = ''[, $attributes = '']])

    :param  string  $email: 电子邮件地址
    :param  string  $title: 锚点标题
    :param  array|object|string $attributes: HTML 属性
    :returns: "mailto" 超链接
    :rtype: string

    创建标准 HTML 电子邮件链接。使用示例：

    .. literalinclude:: url_helper/011.php

    与上面的 :php:func:`anchor()` 类似，你可以使用第三个参数设置属性：

    .. literalinclude:: url_helper/012.php

    .. note:: 传递给 mailto 函数的属性会自动转义以防止 XSS 攻击。

.. php:function:: safe_mailto($email[, $title = ''[, $attributes = '']])

    :param  string  $email: 电子邮件地址
    :param  string  $title: 锚点标题
    :param  array|object|string $attributes: HTML 属性
    :returns: 防垃圾邮件的 "mailto" 超链接
    :rtype: string

    与 :php:func:`mailto()` 函数相同，但它使用 JavaScript 编写的数字
    写入混淆版本的 *mailto* 标签，以帮助防止电子邮件地址被垃圾邮件爬虫收集。

.. php:function:: auto_link($str[, $type = 'both'[, $popup = false]])

    :param  string  $str: 输入字符串
    :param  string  $type: 链接类型 (``'email'``、``'url'`` 或 ``'both'``)
    :param  bool    $popup: 是否创建弹出链接
    :returns: 链接化的字符串
    :rtype: string

    自动将字符串中包含的 URL 和电子邮件地址转换为链接。示例：

    .. literalinclude:: url_helper/013.php

    第二个参数确定是转换 URL 和电子邮件还是仅转换其中一个。
    如果未指定参数，默认行为是两者都转换。
    电子邮件链接被编码为 :php:func:`safe_mailto()`，如上所示。

    仅转换 URL：

    .. literalinclude:: url_helper/014.php

    仅转换电子邮件地址：

    .. literalinclude:: url_helper/015.php

    第三个参数确定链接是否在新窗口中显示。
    值可以是 true 或 false（布尔值）：

    .. literalinclude:: url_helper/016.php

    .. note:: 只有以 ``www.`` 或 ``://`` 开头的 URL 才会被识别。

.. php:function:: url_title($str[, $separator = '-'[, $lowercase = false]])

    :param  string  $str: 输入字符串
    :param  string  $separator: 单词分隔符（通常是 ``'-'`` 或 ``'_'``）
    :param  bool    $lowercase: 是否将输出字符串转换为小写
    :returns: URL 格式的字符串
    :rtype: string

    接受字符串作为输入并创建人类友好的 URL 字符串。
    这很有用，例如，如果你有一个博客，希望在 URL 中使用条目的标题。
    示例：

    .. literalinclude:: url_helper/017.php

    第二个参数确定单词分隔符。默认使用减号。
    首选选项是：``-``（减号）或 ``_``（下划线）。

    示例：

    .. literalinclude:: url_helper/018.php

    第三个参数确定是否强制使用小写字符。
    默认情况下不强制。选项是布尔值 true/false。

    示例：

    .. literalinclude:: url_helper/019.php

.. php:function:: mb_url_title($str[, $separator = '-'[, $lowercase = false]])

    :param  string  $str: 输入字符串
    :param  string  $separator: 单词分隔符（通常是 ``'-'`` 或 ``'_'``）
    :param  bool    $lowercase: 是否将输出字符串转换为小写
    :returns: URL 格式的字符串
    :rtype: string

    此函数与 :php:func:`url_title()` 的工作方式相同，但它会自动转换所有重音字符。

.. php:function:: prep_url([$str = ''[, $secure = false]])

    :param  string   $str: URL 字符串
    :param  boolean  $secure: true 表示使用 ``https://``
    :returns: 带协议前缀的 URL 字符串
    :rtype: string

    如果 URL 缺少协议前缀，此函数将添加 ``http://`` 或 ``https://``。

    像这样将 URL 字符串传递给函数：

    .. literalinclude:: url_helper/020.php

.. php:function:: url_to($controller[, ...$args])

    :param  string  $controller: 路由名称或 Controller::method
    :param  int|string ...$args:    要传递给路由的一个或多个参数。最后一个参数允许你设置区域设置。
    :returns: 绝对 URL
    :rtype: string

    .. note:: 此函数要求控制器/方法在 **app/Config/Routes.php** 中定义了路由。

    构建到应用程序中控制器方法的绝对 URL。示例：

    .. literalinclude:: url_helper/021.php

    你还可以向路由添加参数。
    这是一个示例：

    .. literalinclude:: url_helper/022.php

    这很有用，因为将链接放入视图后，你仍然可以更改路由。

    自 v4.3.0 起，当你在路由中使用 ``{locale}`` 时，你可以选择性地将区域值指定为最后一个参数。

    .. literalinclude:: url_helper/025.php

    有关详细信息，请参阅 :ref:`reverse-routing` 和 :ref:`using-named-routes`。

.. php:function:: url_is($path)

    :param string $path: 用于检查当前 URI 路径的、相对于 baseURL 的 URL 路径。
    :rtype: boolean

    将当前 URL 的路径与给定路径进行比较，看它们是否匹配。示例：

    .. literalinclude:: url_helper/023.php

    这会匹配 **http://example.com/admin**。如果你的 baseURL 是 ``http://example.com/subdir/``，
    它也会匹配 **http://example.com/subdir/admin**。

    你可以使用 ``*`` 通配符来匹配
    URL 中的任何其他适用字符：

    .. literalinclude:: url_helper/024.php

    这会匹配以下任何一项：

    - /admin
    - /admin/
    - /admin/users
    - /admin/users/schools/classmates/...
