############
URL 辅助函数
############

URL 辅助函数文件包含了一系列辅助处理 URL 的函数。

.. contents::
    :local:
    :depth: 2

加载辅助函数
===================

框架会在每次请求时自动加载此辅助函数。

可用函数
===================

提供以下函数：

.. php:function:: site_url([$uri = ''[, $protocol = null[, $altConfig = null]]])

    :param  array|string         $uri: URI 字符串或 URI 段数组。
    :param  string        $protocol: 协议，例如 ``'http'`` 或 ``'https'``。若设为空字符串 ``''``，则返回协议相对链接。
    :param  \\Config\\App $altConfig: 使用的替代配置。
    :returns: 站点 URL
    :rtype:    string

    .. note:: 自 v4.3.0 起，若设置了 ``Config\App::$allowedHostnames`` 且当前 URL 匹配，则返回包含该主机名的 URL。

    返回配置文件中指定的站点 URL。URL 中会包含 **index.php** 文件（或配置文件中 ``Config\App::$indexPage`` 设置的内容），以及传递给函数的任何 URI 段。

    建议在生成本地 URL 时始终使用此函数，以便在 URL 发生变化时提高页面的可移植性。

    URI 段可以作为字符串或数组传递给函数。字符串示例如下：

    .. literalinclude:: url_helper/001.php

    以上示例将返回类似：
    **http://example.com/index.php/news/local/123**

    数组传递段的示例如下：

    .. literalinclude:: url_helper/002.php

    如果需要为具有不同配置偏好的其他站点生成 URL，使用替代配置会非常有用。框架自身的单元测试就使用了此功能。

.. php:function:: base_url([$uri = ''[, $protocol = null]])

    :param  array|string   $uri: URI 字符串或 URI 段数组。
    :param  string  $protocol: 协议，例如 ``'http'`` 或 ``'https'``。若设为空字符串 ``''``，则返回协议相对链接。
    :returns: 基础 URL
    :rtype: string

    .. note:: 自 v4.3.0 起，若设置了 ``Config\App::$allowedHostnames`` 且当前 URL 匹配，则返回包含该主机名的 URL。

    .. note:: 在早期版本中，不带参数调用此函数会返回不带末尾斜杠（``/``）的基础 URL。该问题已修复，自 v4.3.2 起返回带末尾斜杠的基础 URL。

    返回配置文件中指定的站点基础 URL。示例：

    .. literalinclude:: url_helper/003.php

    此函数返回与 :php:func:`site_url()` 相同的结果，但不会追加 ``Config\App::$indexPage``。

    与 :php:func:`site_url()` 类似，可以提供字符串或数组形式的 URI 段。字符串示例如下：

    .. literalinclude:: url_helper/004.php

    以上示例将返回类似：
    **http://example.com/blog/post/123**

    若第二个参数传递空字符串 ``''``，则返回协议相对链接：

    .. literalinclude:: url_helper/026.php

    此函数非常有用，因为与 :php:func:`site_url()` 不同，它可以指向文件的字符串路径，例如图片或样式表。示例：

    .. literalinclude:: url_helper/005.php

    这将生成类似：
    **http://example.com/images/icons/edit.png**

.. php:function:: current_url([$returnObject = false[, $request = null]])

    :param    boolean    $returnObject: 若设为 true，则返回 URI 实例而非字符串。
    :param    IncomingRequest|null    $request: 用于路径检测的替代请求；常用于测试。
    :returns: 当前 URL
    :rtype:    string|\\CodeIgniter\\HTTP\\URI

    返回当前正在浏览的页面的完整 URL。
    返回字符串时，URL 的 query 和 fragment 会被移除。
    返回 URI 对象时，query 和 fragment 会被保留。

    出于安全考虑，此 URL 基于 ``Config\App`` 设置生成，并非旨在与浏览器地址栏完全匹配。

    自 v4.3.0 起，若设置了 ``Config\App::$allowedHostnames`` 且当前 URL 匹配，则返回包含该主机名的 URL。

    .. note:: 调用 ``current_url()`` 等同于：

        .. literalinclude:: url_helper/006.php
           :lines: 2-

    .. important:: 在 v4.1.2 之前，此函数存在会忽略 ``Config\App::$indexPage`` 配置的缺陷。

.. php:function:: previous_url([$returnObject = false])

    :param boolean $returnObject: 若设为 true，则返回 URI 实例而非字符串。
    :returns: 用户之前访问的 URL
    :rtype: string|\\CodeIgniter\\HTTP\\URI

    返回用户之前访问页面的完整 URL（包括 URI 段）。

    .. note:: 由于盲目信任 ``HTTP_REFERER`` 系统变量存在安全隐患，如果 Session 可用，CodeIgniter 会将之前访问的页面存储在 Session 中。这确保了始终使用已知且可信的来源。若 Session 未加载或不可用，则会使用经过清理的 ``HTTP_REFERER``。

.. php:function:: uri_string()

    :returns: URI 字符串
    :rtype:   string

    返回当前 URL 相对于 baseURL 的路径部分。

    例如，当 baseURL 为 **http://some-site.com/** 且当前 URL 为::

        http://some-site.com/blog/comments/123

    此函数返回::

        blog/comments/123

    当 baseURL 为 **http://some-site.com/subfolder/** 且当前 URL 为::

        http://some-site.com/subfolder/blog/comments/123

    此函数返回::

        blog/comments/123

    .. note:: 在早期版本中定义了 ``$relative = false`` 参数。但由于 Bug，此函数始终返回相对于 baseURL 的路径。自 v4.3.2 起，该参数已被移除。

    .. note:: 在早期版本中，导航到 baseURL 时此函数返回 ``/``。自 v4.3.2 起该问题已修复，现在返回空字符串（``''``）。

.. php:function:: index_page([$altConfig = null])

    :param \\Config\\App $altConfig: 使用的替代配置
    :returns:  ``indexPage`` 的值
    :rtype:    string

    返回配置文件中指定的站点 **indexPage**。
    示例：

    .. literalinclude:: url_helper/007.php

    与 :php:func:`site_url()` 相同，可以指定替代配置。如果需要为具有不同配置偏好的其他站点生成 URL，此功能非常有用。框架自身的单元测试就使用了此功能。

.. php:function:: anchor([$uri = ''[, $title = ''[, $attributes = ''[, $altConfig = null]]]])

    :param  array|string        $uri: URI 字符串或 URI 段数组
    :param  string              $title: 锚点标题
    :param  array|object|string $attributes: HTML 属性
    :param  \\Config\\App|null  $altConfig: 使用的替代配置
    :returns: HTML 超链接（a 标签）
    :rtype:    string

    根据本地站点 URL 创建标准 HTML 链接。

    第一个参数可以包含任何希望追加到 URL 的 URI 段。与上述 :php:func:`site_url()` 函数类似，URI 段可以是字符串或数组。

    .. note:: 构建应用程序内部链接时，请勿包含基础 URL（``http://...``）。框架会自动根据配置文件中的信息添加。只需包含希望追加到 URL 的 URI 段即可。

    第二个参数是希望链接显示的文本。若留空，则直接使用 URL。

    第三个参数包含希望添加到链接的属性列表。属性可以是简单的字符串，也可以是关联数组。

    示例如下：

    .. literalinclude:: url_helper/008.php

    如上所述，可以指定替代配置。在为具有不同配置偏好的其他站点生成链接时，此功能非常有用。

    .. note:: 传入 anchor 函数的属性会自动进行转义，以防止 XSS 攻击。

.. php:function:: anchor_popup([$uri = ''[, $title = ''[, $attributes = false[, $altConfig = null]]]])

    :param  string          $uri: URI 字符串
    :param  string          $title: 锚点标题
    :param  array|false|object|string $attributes: HTML 属性
    :param  \\Config\\App   $altConfig: 使用的替代配置
    :returns: 弹出式超链接
    :rtype: string

    与 :php:func:`anchor()` 函数几乎完全相同，区别在于它会在新窗口中打开 URL。可以在第三个参数中指定 JavaScript 窗口属性，以控制窗口的打开方式。若未设置第三个参数，它将根据浏览器设置简单地打开一个新窗口。

    带属性的示例如下：

    .. literalinclude:: url_helper/009.php

    同样可以指定替代配置。

    .. note:: 以上属性是函数的默认值，因此只需设置不同的属性即可。若希望函数使用所有默认设置，只需在第三个参数传递一个空数组：

        .. literalinclude:: url_helper/010.php

    .. note:: **window_name** 并非真正的属性，而是 JavaScript `window.open() <https://www.w3schools.com/jsref/met_win_open.asp>`_ 方法的参数，该方法接受窗口名称或窗口目标。

    .. note:: 除上述列出的属性外，任何其他属性都会被解析为 a 标签的 HTML 属性。

    .. note:: 传入 anchor_popup 函数的属性会自动进行转义，以防止 XSS 攻击。

.. php:function:: mailto($email[, $title = ''[, $attributes = '']])

    :param  string  $email: 电子邮件地址
    :param  string  $title: 锚点标题
    :param  array|object|string $attributes: HTML 属性
    :returns: "mail to" 超链接
    :rtype: string

    创建标准 HTML 电子邮件链接。用法示例：

    .. literalinclude:: url_helper/011.php

    与上述 :php:func:`anchor()` 标签类似，可以使用第三个参数设置属性：

    .. literalinclude:: url_helper/012.php

    .. note:: 传入 mailto 函数的属性会自动进行转义，以防止 XSS 攻击。

.. php:function:: safe_mailto($email[, $title = ''[, $attributes = '']])

    :param  string  $email: 电子邮件地址
    :param  string  $title: 锚点标题
    :param  array|object|string $attributes: HTML 属性
    :returns: 防垃圾邮件的 "mail to" 超链接
    :rtype: string

    与 :php:func:`mailto()` 函数相同，但它会使用 JavaScript 编写混淆版的 *mailto* 标签，通过序数来防止 Email 地址被垃圾邮件机器人抓取。

.. php:function:: auto_link($str[, $type = 'both'[, $popup = false]])

    :param  string  $str: 输入字符串
    :param  string  $type: 链接类型（``'email'``、``'url'`` 或 ``'both'``）
    :param  bool    $popup: 是否创建弹出式链接
    :returns: 链接化处理后的字符串
    :rtype: string

    自动将字符串中包含的 URL 和电子邮件地址转换为链接。示例：

    .. literalinclude:: url_helper/013.php

    第二个参数决定转换 URL、Email 还是两者都转换。若未指定，默认行为是两者都转换。Email 链接按上述 :php:func:`safe_mailto()` 方式编码。

    仅转换 URL：

    .. literalinclude:: url_helper/014.php

    仅转换电子邮件地址：

    .. literalinclude:: url_helper/015.php

    第三个参数决定链接是否在新窗口中显示，取值为布尔值 true 或 false：

    .. literalinclude:: url_helper/016.php

    .. note:: 仅识别以 ``www.`` 或 ``://`` 开头的 URL。

.. php:function:: url_title($str[, $separator = '-'[, $lowercase = false]])

    :param  string  $str: 输入字符串
    :param  string  $separator: 单词分隔符（通常为 ``'-'`` 或 ``'_'``）
    :param  bool    $lowercase: 是否将输出字符串转换为全小写
    :returns: URL 格式的字符串
    :rtype: string

    接收字符串作为输入，并创建人性化的 URL 字符串。例如，在博客中希望在 URL 中使用文章标题时，此函数非常有用。示例：

    .. literalinclude:: url_helper/017.php

    第二个参数决定单词分隔符。默认使用减号。常用选项为：``-`` （减号）或 ``_`` （下划线）。

    示例：

    .. literalinclude:: url_helper/018.php

    第三个参数决定是否强制转换为小写。默认不转换。选项为布尔值 true/false。

    示例：

    .. literalinclude:: url_helper/019.php

.. php:function:: mb_url_title($str[, $separator = '-'[, $lowercase = false]])

    :param  string  $str: 输入字符串
    :param  string  $separator: 单词分隔符（通常为 ``'-'`` 或 ``'_'``）
    :param  bool    $lowercase: 是否将输出字符串转换为全小写
    :returns: URL 格式的字符串
    :rtype: string

    功能与 :php:func:`url_title()` 相同，但会自动转换所有重音字符。

.. php:function:: parse_subdomain($hostname)

    :param  string|null  $hostname: 待解析的主机名。若为 null，则使用当前请求的主机。
    :returns: 子域名，若不存在则返回空字符串。
    :rtype: string

    从给定主机名中解析子域名。

    示例如下：

    .. literalinclude:: url_helper/027.php

    可以通过将已知的两部分 TLD（顶级域名）添加到 ``Config\Hostnames::TWO_PART_TLDS`` 数组中来自定义识别列表。

.. php:function:: prep_url([$str = ''[, $secure = false]])

    :param  string   $str: URL 字符串
    :param  boolean  $secure: 设为 true 以使用 ``https://``
    :returns: 包含协议前缀的 URL 字符串
    :rtype: string

    当 URL 缺少协议前缀时，此函数会添加 ``http://`` 或 ``https://``。

    用法如下：

    .. literalinclude:: url_helper/020.php

.. php:function:: url_to($controller[, ...$args])

    :param  string  $controller: 路由名称或 Controller::method
    :param  int|string ...$args: 传递给路由的一个或多个参数。最后一个参数可用于设置语言环境。
    :returns: 绝对 URL
    :rtype: string

    .. note:: 此函数要求在 **app/Config/Routes.php** 中为控制器/方法定义路由。

    构建指向应用中控制器方法的绝对 URL。示例：

    .. literalinclude:: url_helper/021.php

    也可以为路由添加参数。
    示例如下：

    .. literalinclude:: url_helper/022.php

    即使在视图中放入链接后更改了路由配置，链接依然有效。

    自 v4.3.0 起，若在路由中使用了 ``{locale}``，可以根据需要将语言环境值作为最后一个参数传入。

    .. literalinclude:: url_helper/025.php

    有关完整详细信息，请参阅 :ref:`reverse-routing` 和 :ref:`using-named-routes`。

.. php:function:: url_is($path)

    :param string $path: 待检查的、相对于 baseURL 的 URL 路径。
    :rtype: boolean

    将当前 URL 的路径与给定路径进行比较，检查是否匹配。示例：

    .. literalinclude:: url_helper/023.php

    这会匹配 **http://example.com/admin**。如果 baseURL 为 ``http://example.com/subdir/``，则会匹配 **http://example.com/subdir/admin**。

    可以使用 ``*`` 通配符匹配 URL 中任何适用的字符：

    .. literalinclude:: url_helper/024.php

    这将匹配以下任何路径：

    - /admin
    - /admin/
    - /admin/users
    - /admin/users/schools/classmates/...
