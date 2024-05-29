##############
URL 辅助函数
##############

URL 辅助函数文件包含帮助使用 URL 的函数。

.. contents::
    :local:
    :depth: 2

加载此辅助函数
===================

此辅助函数由框架在每个请求上自动加载。

可用函数
===================

以下函数可用:

.. php:function:: site_url([$uri = ''[, $protocol = null[, $altConfig = null]]])

    :param  array|string         $uri: URI 字符串或 URI 段数组
    :param  string        $protocol: 协议，例如 'http' 或 'https'。如果设置为空字符串 ''，则返回一个 protocol-relative 链接。
    :param  \\Config\\App $altConfig: 要使用的备用配置
    :returns: 站点 URL
    :rtype:    string

    .. note:: 从 v4.3.0 开始,如果你设置了 ``Config\App::$allowedHostnames``,
        并且当前 URL 匹配,则会返回主机名设置了的 URL。

    返回配置文件中指定的你的站点 URL。**index.php** 文件(或你在配置文件中设置为站点 ``Config\App::$indexPage`` 的任何内容)都将添加到 URL 中,就像你传递给函数的任何 URI 段一样。

    每当你需要生成本地 URL 时,都建议使用此函数,以便在 URL 改变的情况下使页面更便携。

    段可以可选地作为字符串或数组传递给函数。这是字符串示例:

    .. literalinclude:: url_helper/001.php

    上面的示例将返回类似内容:
    **http://example.com/index.php/news/local/123**

    以下是作为数组传递段的示例:

    .. literalinclude:: url_helper/002.php

    如果为不同于你自己的站点生成 URL,其中包含不同的配置首选项,则备用配置可能很有用。我们对框架本身使用它进行单元测试。

.. php:function:: base_url([$uri = ''[, $protocol = null]])

    :param  array|string   $uri: URI 字符串或 URI 段数组
    :param  string  $protocol: 协议，例如 'http' 或 'https'。如果设置为空字符串 ''，则返回一个 protocol-relative 链接。
    :returns: Base URL
    :rtype: string

    .. note:: 从 v4.3.0 开始,如果你设置了 ``Config\App::$allowedHostnames``,
        并且当前 URL 匹配,则会返回主机名设置了的 URL。

    .. note:: 在以前的版本中,如果不带参数调用,此函数返回没有尾随斜杠 (``/``) 的基本 URL。该错误已修复,
        从 v4.3.2 开始,它返回带有尾随斜杠的基本 URL。

    返回配置文件中指定的你的站点基础 URL。示例:

    .. literalinclude:: url_helper/003.php

    此函数返回与不附加 ``Config\App::$indexPage`` 的 :php:func:`site_url()` 相同的内容。

    与 :php:func:`site_url()` 类似,你可以将段作为字符串或数组提供。这是一个字符串示例:

    .. literalinclude:: url_helper/004.php

    上面的示例将返回类似内容:
    **http://example.com/blog/post/123**

    如果你传递一个空字符串 ``''`` 作为第二个参数，它会返回 protocol-relative 链接：

    这很有用,因为与 :php:func:`site_url()` 不同,你可以为文件(如图像或样式表)提供字符串。例如:

    .. literalinclude:: url_helper/005.php

    这将给你类似的内容:
    **http://example.com/images/icons/edit.png**

.. php:function:: current_url([$returnObject = false[, $request = null]])

    :param    boolean    $returnObject: 如果希望返回 URI 实例而不是字符串,则为 True。
    :param    IncomingRequest|null    $request: 用于路径检测的替代请求;用于测试。
    :returns: 当前URL
    :rtype:    string|\\CodeIgniter\\HTTP\\URI

    返回当前正在查看的页面的完整 URL。
    返回字符串时,会删除 URL 的查询和片段部分。
    返回 URI 时,会保留查询和片段部分。

    但是,出于安全原因,它基于 ``Config\App`` 设置创建,而不是旨在匹配浏览器 URL。

    从 v4.3.0 开始,如果你设置了 ``Config\App::$allowedHostnames``,并且当前 URL 匹配,则会返回主机名设置了的 URL。

    .. note:: 调用 ``current_url()`` 与这样做相同:

        .. literalinclude:: url_helper/006.php
           :lines: 2-

    .. important:: 在 v4.1.2 之前,此函数有一个错误,导致它忽略对 ``Config\App::$indexPage`` 的配置。

.. php:function:: previous_url([$returnObject = false])

    :param boolean $returnObject: 如果希望返回 URI 实例而不是字符串,则为 True。
    :returns: 用户之前所在的 URL
    :rtype: string|mixed|\\CodeIgniter\\HTTP\\URI

    返回用户之前完整的 URL(包括段)。

    .. note:: 由于盲目信任 ``HTTP_REFERER`` 系统变量存在安全问题,如果可用,CodeIgniter 会将以前访问的页面存储在会话中。这确保我们始终使用已知和可信的来源。如果尚未加载会话或否则不可用,则将使用经过清理的 ``HTTP_REFERER`` 版本。

.. php:function:: uri_string()

    :returns: URI 字符串
    :rtype:   string

    返回相对于 baseURL 的当前 URL 的路径部分。

    例如,当你的 baseURL 为 **http://some-site.com/** ,当前 URL 为::

        http://some-site.com/blog/comments/123

    函数将返回::

        blog/comments/123

    当你的 baseURL 为 **http://some-site.com/subfolder/** ,当前 URL 为::

        http://some-site.com/subfolder/blog/comments/123

    函数将返回::

        blog/comments/123

    .. note:: 以前的版本中定义了参数 ``$relative = false``。
        然而,由于一个错误,此函数总是返回相对于 baseURL 的路径。
        从 v4.3.2 开始,该参数已被删除。

    .. note:: 在以前的版本中,当你导航到 baseURL 时,此函数返回 ``/``。
        从 v4.3.2 开始,错误已修复,它返回一个空字符串(``''``)。

.. php:function:: index_page([$altConfig = null])

    :param \\Config\\App $altConfig: 要使用的备用配置
    :returns:  ``indexPage`` 值
    :rtype:    string

    返回配置文件中指定的你的站点 **indexPage**。例如:

    .. literalinclude:: url_helper/007.php

    与 :php:func:`site_url()` 一样,你可以指定备用配置。如果为不同于你自己的站点生成 URL,其中包含不同的配置首选项,则备用配置可能很有用。我们对框架本身使用它进行单元测试。

.. php:function:: anchor([$uri = ''[, $title = ''[, $attributes = ''[, $altConfig = null]]]])

    :param  mixed         $uri: URI字符串或URI段数组
    :param  string        $title: 锚点标题
    :param  mixed         $attributes: HTML属性
    :param  \\Config\\App $altConfig: 要使用的备用配置
    :returns: HTML链接(锚点标签)
    :rtype:    string

    基于你的本地站点 URL 创建标准的 HTML 锚点链接。

    第一个参数可以包含你希望附加到 URL 的任何段。与上面的 :php:func:`site_url()` 函数一样,段可以是字符串或数组。

    .. note:: 如果你正在构建应用程序内部的链接,请不要包含基本 URL (``http://...``)。这将从配置文件中指定的信息自动添加。只包含你希望附加到 URL 的 URI 段。

    第二段是你希望链接说的文本。如果留空,将使用 URL。

    第三个参数可以包含你希望添加到链接的属性列表。属性可以是简单的字符串或关联数组。

    这里有一些示例:

    .. literalinclude:: url_helper/008.php

    如上所述,你可以指定备用配置。如果为不同于你自己的站点生成链接,其中包含不同的配置首选项,则备用配置可能很有用。我们对框架本身使用它进行单元测试。

    .. note:: 传递给 anchor 函数的属性会自动转义,以防止 XSS 攻击。

.. php:function:: anchor_popup([$uri = ''[, $title = ''[, $attributes = false[, $altConfig = null]]]])

    :param  string          $uri: URI字符串
    :param  string          $title: 锚点标题
    :param  mixed           $attributes: HTML属性
    :param  \\Config\\App   $altConfig: 要使用的备用配置
    :returns: 弹出式超链接
    :rtype: string

    几乎与 :php:func:`anchor()` 函数完全相同,除了它在新窗口中打开 URL。你可以在第三个参数中指定 JavaScript 窗口属性以控制窗口的打开方式。如果未设置第三个参数,它将简单地用你自己的浏览器设置打开新窗口。

    这里是一个带有属性的示例:

    .. literalinclude:: url_helper/009.php

    如上所述,你可以指定备用配置。如果为不同于你自己的站点生成链接,其中包含不同的配置首选项,则备用配置可能很有用。我们对框架本身使用它进行单元测试。

    .. note:: 上述属性是函数默认值,所以你只需要设置与你需要的不同的那些。如果你希望函数使用所有默认值,只需在第三个参数中传递一个空数组:

        .. literalinclude:: url_helper/010.php

    .. note:: **window_name** 实际上不是一个属性,而是 `window.open() <https://www.w3schools.com/jsref/met_win_open.asp>`_ 方法接受的一个参数,它接受窗口名称或窗口目标。

    .. note:: 除上述之外的任何其他属性都将作为 HTML 锚点标记的属性进行解析。

    .. note:: 传递给 anchor_popup 函数的属性会自动转义,以防止 XSS 攻击。

.. php:function:: mailto($email[, $title = ''[, $attributes = '']])

    :param  string  $email: 电子邮件地址
    :param  string  $title: 锚点标题
    :param  mixed   $attributes: HTML属性
    :returns: “发送邮件到”超链接
    :rtype: string

    创建标准的 HTML 电子邮件链接。使用示例:

    .. literalinclude:: url_helper/011.php

    如上面的 :php:func:`anchor()` 选项卡一样,你可以使用第三个参数设置属性:

    .. literalinclude:: url_helper/012.php

    .. note:: 传递给 mailto 函数的属性会自动转义,以防止 XSS 攻击。

.. php:function:: safe_mailto($email[, $title = ''[, $attributes = '']])

    :param  string  $email: 电子邮件地址
    :param  string  $title: 锚点标题
    :param  mixed   $attributes: HTML属性
    :returns: 防垃圾邮件的“发送邮件到”超链接
    :rtype: string

    与 :php:func:`mailto()` 函数完全相同,除了它使用序数数字与 JavaScript 编写的隐写版本来帮助防止垃圾邮件机器人收集电子邮件地址。

.. php:function:: auto_link($str[, $type = 'both'[, $popup = false]])

    :param  string  $str: 输入字符串
    :param  string  $type: 链接类型('email'、'url' 或 'both')
    :param  bool    $popup: 是否创建弹出链接
    :returns: 链接化的字符串
    :rtype: string

    自动将字符串中包含的 URL 和电子邮件地址转换为链接。示例:

    .. literalinclude:: url_helper/013.php

    第二个参数确定是转换 URL 和电子邮件还是仅转换其中一个。如果未指定参数,默认行为是两者都转换。电子邮件链接编码为上面显示的 :php:func:`safe_mailto()`。

    仅转换 URL:

    .. literalinclude:: url_helper/014.php

    仅转换电子邮件地址:

    .. literalinclude:: url_helper/015.php

    第三个参数确定是否在新窗口中显示链接。值可以为 true 或 false(布尔值):

    .. literalinclude:: url_helper/016.php

    .. note:: 仅识别以 ``www.`` 或 ``://`` 开头的 URL。

.. php:function:: url_title($str[, $separator = '-'[, $lowercase = false]])

    :param  string  $str: 输入字符串
    :param  string  $separator: 单词分隔符(通常为 ``'-'`` 或 ``'_'``)
    :param  bool    $lowercase: 是否将输出字符串转换为小写
    :returns: URL 格式化的字符串
    :rtype: string

    获取一个字符串作为输入,并创建一个人性化的 URL 字符串。例如,如果你有一个博客,希望在 URL 中使用条目的标题。示例:

    .. literalinclude:: url_helper/017.php

    第二个参数确定单词分隔符。默认使用破折号。首选选项是: ``-`` (破折号)或 ``_`` (下划线)。

    示例:

    .. literalinclude:: url_helper/018.php

    第三个参数确定是否强制使用小写字符。默认不强制。选项是布尔值 true/false。

    示例:

    .. literalinclude:: url_helper/019.php

.. php:function:: mb_url_title($str[, $separator = '-'[, $lowercase = false]])

    :param  string  $str: 输入字符串
    :param  string  $separator: 单词分隔符(通常为 ``'-'`` 或 ``'_'``)
    :param  bool    $lowercase: 是否将输出字符串转换为小写
    :returns: URL 格式化的字符串
    :rtype: string

    此函数的工作方式与 :php:func:`url_title()` 相同,但它会自动转换所有重音字符。

.. php:function:: prep_url([$str = ''[, $secure = false]])

    :param  string   $str: URL字符串
    :param  boolean  $secure: true 为 ``https://``
    :returns: 带协议前缀的 URL 字符串
    :rtype: string

    如果 URL 中缺少协议前缀,此函数将添加 ``http://`` 或 ``https://``。

    如下传入 URL 字符串给函数:

    .. literalinclude:: url_helper/020.php

.. php:function:: url_to($controller[, ...$args])

    :param  string  $controller: 路由名称或 Controller::method
    :param  mixed   ...$args:    要传递给路由的一个或多个参数。最后一个参数允许你设置区域设置。
    :returns: 绝对 URL
    :rtype: string

    .. note:: 此函数要求在 **app/Config/Routes.php** 中为控制器/方法定义路由。

    在你的应用程序中构建指向控制器方法的绝对 URL。示例:

    .. literalinclude:: url_helper/021.php

    你还可以向路由添加参数。这是一个示例:

    .. literalinclude:: url_helper/022.php

    这很有用,因为即使在将链接放入视图后,你仍然可以更改路由。

    从 v4.3.0 开始,当你在路由中使用 ``{locale}`` 时,你可以可选地将区域设置值指定为最后一个参数。

    .. literalinclude:: url_helper/025.php

    有关完整详细信息,请参阅 :ref:`反向路由 <reverse-routing>` 和 :ref:`使用命名路由 <using-named-routes>`。

.. php:function:: url_is($path)

    :param string $path: 要比较当前 URI 路径的相对于 baseURL 的 URL 路径。
    :rtype: boolean

    将当前 URL 的路径与给定路径进行比较,以查看它们是否匹配。示例:

    .. literalinclude:: url_helper/023.php

    这将匹配 **http://example.com/admin**。如果你的 baseURL是 ``http://example.com/subdir/``,它将匹配 **http://example.com/subdir/admin**。

    你可以使用 ``*`` 通配符来匹配 URL 中的任何其他可应用字符:

    .. literalinclude:: url_helper/024.php

    这将匹配以下任何一个:

    - /admin
    - /admin/
    - /admin/users
    - /admin/users/schools/classmates/...
