##############################
全局函数和常量
##############################

CodeIgniter 提供了一些全局定义的函数和变量，你可以在任何地方使用它们。
这些函数和变量不需要加载任何额外的库或辅助函数。

.. contents::
    :local:
    :depth: 2

================
全局函数
================

服务访问器
=================

.. php:function:: cache([$key])

    :param  string $key: 要从缓存中检索的项目的缓存名称（可选）
    :returns: 缓存对象，或从缓存中检索到的项目
    :rtype: mixed

    如果没有提供 $key，将返回缓存引擎实例。如果提供了 $key，
    将返回当前缓存中存储的 $key 的值，如果未找到值则返回 null。

    示例：

    .. literalinclude:: common_functions/001.php

.. php:function:: config(string $name[, bool $getShared = true])

    :param string $name: 配置类名。
    :param bool $getShared: 是否返回共享实例。
    :returns: 配置实例。
    :rtype: object|null

    从工厂获取配置实例的更简单方式。

    详情请参阅 :ref:`配置 <configuration-config>` 和
    :ref:`工厂 <factories-config>`。

    ``config()`` 内部使用 ``Factories::config()``。
    有关第一个参数 ``$name`` 的详细信息，请参阅 :ref:`factories-loading-class`。

.. php:function:: cookie(string $name[, string $value = ''[, array $options = []]])

    :param string $name: Cookie 名称
    :param string $value: Cookie 值
    :param array $options: Cookie 选项
    :rtype: ``Cookie``
    :returns: ``Cookie`` 实例
    :throws: ``CookieException``

    创建新 Cookie 实例的更简单方式。

.. php:function:: cookies([array $cookies = [][, bool $getGlobal = true]])

    :param array $cookies: 如果 ``getGlobal`` 为 ``false``，此参数将传递给 ``CookieStore`` 的构造函数。
    :param bool $getGlobal: 如果为 ``false``，则创建一个新的 ``CookieStore`` 实例。
    :rtype: ``CookieStore``
    :returns: 当前 ``Response`` 中保存的 ``CookieStore`` 实例，或一个新的 ``CookieStore`` 实例。

    获取 ``Response`` 保存的全局 ``CookieStore`` 实例。

.. php:function:: env($key[, $default = null])

    :param string $key: 要检索的环境变量名称
    :param mixed  $default: 如果未找到值时返回的默认值。
    :returns: 环境变量、默认值或 null。
    :rtype: mixed

    用于检索先前设置到环境中的值，
    或在未找到时返回默认值。会将布尔值格式化为实际的布尔值，
    而不是字符串表示形式。

    当与 **.env** 文件结合使用时特别有用，用于设置
    特定于环境本身的值，如数据库
    设置、API 密钥等。

.. php:function:: esc($data[, $context = 'html'[, $encoding]])

    :param   string|array   $data: 要转义的信息。
    :param   string   $context: 转义上下文。默认为 'html'。
    :param   string   $encoding: 字符串的字符编码。
    :returns: 转义后的数据。
    :rtype: mixed

    转义要包含在网页中的数据，以帮助防止 XSS 攻击。
    这使用 Laminas Escaper 库来处理实际的数据过滤。

    如果 $data 是字符串，则简单地转义并返回它。
    如果 $data 是数组，则循环遍历它，转义每个键/值对的 '值'。

    有效的上下文值：``html``、``js``、``css``、``url``、``attr``、``raw``

.. php:function:: helper($filename)

    :param   string|array  $filename: 要加载的辅助函数文件名，或名称数组。

    加载辅助函数文件。

    详情请参阅 :doc:`辅助函数` 页面。

.. php:function:: lang($line[, $args[, $locale]])

    :param string $line: 语言文件名和要检索的文本键。
    :param array  $args: 用于替换占位符的数据数组。
    :param string $locale: 指定要使用的不同区域设置，而不是当前区域设置。
    :returns: 语言文件中的文本
    :rtype: list<string>|string

    从语言文件中检索文本。

    详情请参阅 :ref:`language-localization`。

.. php:function:: model($name[, $getShared = true[, &$conn = null]])

    :param string                   $name: 模型类名。
    :param boolean                  $getShared: 是否返回共享实例。
    :param ConnectionInterface|null $conn: 数据库连接。
    :returns: 模型实例
    :rtype: object

    获取模型实例的更简单方式。

    ``model()`` 内部使用 ``Factories::models()``。
    有关第一个参数 ``$name`` 的详细信息，请参阅 :ref:`factories-loading-class`。

    另请参阅 :ref:`使用 CodeIgniter 的模型 <accessing-models>`。

.. php:function:: old($key[, $default = null,[, $escape = 'html']])

    :param string $key: 要检查的旧表单数据名称。
    :param string|null  $default: 如果 $key 不存在时返回的默认值。
    :param false|string  $escape: `转义 <#esc>`_ 上下文或 false 以禁用它。
    :returns: 定义键的值，或默认值。
    :rtype: array|string|null

    提供了一种简单的方式来访问提交表单后的“旧输入数据”。

    示例：

    .. literalinclude:: common_functions/002.php

.. note:: 如果你正在使用 :php:func:`set_value()`、:php:func:`set_select()`、
    :php:func:`set_checkbox()` 和 :php:func:`set_radio()` 函数（位于
    :doc:`表单辅助函数 </helpers/form_helper>` 中），此功能已内置。只有
    在不使用表单辅助函数时才需要使用此函数。

.. php:function:: session([$key])

    :param string $key: 要检查的会话项名称。
    :returns: 如果没有提供 $key，则返回 Session 对象实例；如果提供了 $key，则返回会话中 $key 对应的值，或 null。
    :rtype: mixed

    提供了一种便捷的方式来访问会话类并检索存储的值。详情请参阅 :doc:`会话 </libraries/sessions>` 页面。

.. php:function:: timer([$name])

    :param string $name: 基准点的名称。
    :returns: Timer 实例
    :rtype: CodeIgniter\Debug\Timer

    一种便捷方法，可快速访问 Timer 类。你可以将基准点的名称作为唯一参数传入。
    这将从此点开始计时，或者如果已存在同名计时器则停止计时。

    示例：

    .. literalinclude:: common_functions/003.php

.. php:function:: view($name[, $data[, $options]])

    :param   string   $name: 要加载的文件名
    :param   array    $data: 键/值对数组，使其在视图内可用。
    :param   array    $options: 将传递给渲染类的选项数组。
    :returns: 视图的输出。
    :rtype: string

    获取当前与 RendererInterface 兼容的类
    （默认为 :doc:`视图 <../outgoing/view_renderer>` 类）
    并告诉它渲染指定的视图。仅提供
    一种便捷方法，可在控制器、
    库和路由闭包中使用。

    目前，``$options`` 数组中可使用以下选项：

    - ``saveData`` 指定数据将在同一请求内的多次 ``view()`` 调用间保持。如果你不希望保持，请指定 false。
    - ``cache`` 指定缓存视图的秒数。详情请参阅 :ref:`caching-views`。
    - ``debug`` 可设置为 false 以禁用 :ref:`调试工具栏 <the-debug-toolbar>` 的调试代码添加。

    ``$option`` 数组主要用于促进与
    Twig 等库的第三方集成。

    示例：

    .. literalinclude:: common_functions/004.php

    详情请参阅 :doc:`视图 <../outgoing/views>` 和
    :doc:`../outgoing/view_renderer` 页面。

.. php:function:: view_cell($library[, $params = null[, $ttl = 0[, $cacheName = null]]])

    :param string      $library:
    :param null        $params:
    :param integer     $ttl:
    :param string|null $cacheName:
    :returns: 视图单元用于在视图中插入由其他类管理的 HTML 片段。
    :rtype: string

    详情请参阅 :doc:`视图单元 </outgoing/view_cells>` 页面。

其他函数
=======================

.. php:function:: app_timezone()

    :returns: 应用程序设置的显示日期的时区。
    :rtype: string

    返回应用程序设置的显示日期的时区。

.. php:function:: csp_script_nonce()

    :returns: script 标签的 CSP nonce 属性。
    :rtype: string

    返回 script 标签的 nonce 属性。例如：``nonce="Eskdikejidojdk978Ad8jf"``。
    请参阅 :ref:`内容安全策略 <csp-using-functions>`。

.. php:function:: csp_style_nonce()

    :returns: style 标签的 CSP nonce 属性。
    :rtype: string

    返回 style 标签的 nonce 属性。例如：``nonce="Eskdikejidojdk978Ad8jf"``。
    请参阅 :ref:`内容安全策略 <csp-using-functions>`。

.. php:function:: csrf_token()

    :returns: 当前 CSRF 令牌的名称。
    :rtype: string

    返回当前 CSRF 令牌的名称。

.. php:function:: csrf_header()

    :returns: 当前 CSRF 令牌的头部名称。
    :rtype: string

    当前 CSRF 令牌的头部名称。

.. php:function:: csrf_hash()

    :returns: 当前 CSRF 哈希值。
    :rtype: string

    返回当前 CSRF 哈希值。

.. php:function:: csrf_field()

    :returns: 包含所有必需 CSRF 信息的隐藏输入 HTML 字符串。
    :rtype: string

    返回一个已插入 CSRF 信息的隐藏输入::

        <input type="hidden" name="{csrf_token}" value="{csrf_hash}">

.. php:function:: csrf_meta()

    :returns: 包含所有必需 CSRF 信息的 meta 标签 HTML 字符串。
    :rtype: string

    返回一个已插入 CSRF 信息的 meta 标签::

        <meta name="{csrf_header}" content="{csrf_hash}">

.. php:function:: force_https($duration = 31536000[, $request = null[, $response = null]])

    :param  int  $duration: 浏览器应将此资源的链接转换为 HTTPS 的秒数。
    :param  RequestInterface $request: 当前 Request 对象的实例。
    :param  ResponseInterface $response: 当前 Response 对象的实例。

    检查页面当前是否通过 HTTPS 访问。如果是，则
    不会发生任何事情。如果不是，则将用户重定向回当前 URI，
    但通过 HTTPS。将设置 HTTP Strict Transport Security (HTST) 头部，指示
    现代浏览器在 ``$duration`` 期间自动将任何 HTTP 请求修改为 HTTPS 请求。

    .. note:: 此函数也在你将
        ``Config\App:$forceGlobalSecureRequests`` 设置为 true 时使用。

.. php:function:: function_usable($functionName)

    :param string $functionName: 要检查的函数
    :returns: 如果函数存在且可以安全调用则返回 true，否则返回 false。
    :rtype: bool

.. php:function:: is_cli()

    :returns: 如果脚本从命令行执行则返回 true，否则返回 false。
    :rtype: bool

.. php:function:: is_really_writable($file)

    :param string $file: 要检查的文件名。
    :returns: 如果可以写入文件则返回 true，否则返回 false。
    :rtype: bool

.. php:function:: is_windows([$mock = null])

    :param bool|null $mock: 如果给定且为布尔值，则将用作返回值。
    :rtype: bool

    检测平台是否在 Windows 上运行。

    .. note:: 提供给 $mock 的布尔值将在后续调用中保持。要重置此
        模拟值，用户必须在函数调用中显式传递 ``null``。这将
        刷新函数以使用自动检测。

    .. literalinclude:: common_functions/012.php

.. php:function:: log_message($level, $message [, $context])

    :param   string   $level: 严重级别
    :param   string   $message: 要记录的消息。
    :param   array    $context: 应在 $message 中替换的标签及其值的关联数组
    :returns: void
    :rtype: bool

    .. note:: 从 v4.5.0 开始，返回值已修复为与 PSR
        Log 兼容。在以前的版本中，如果成功记录则返回 ``true``，
        如果记录时出现问题则返回 ``false``。

    使用 **app/Config/Logger.php** 中定义的日志处理器记录消息。

    级别可以是以下值之一：``emergency``、``alert``、``critical``、``error``、``warning``、
    ``notice``、``info`` 或 ``debug``。

    上下文可用于替换消息字符串中的值。详情请参阅
    :doc:`日志记录信息 <logging>` 页面。

.. php:function:: redirect(string $route)

    :param  string  $route: 要重定向用户的路由名称或 Controller::method。
    :rtype: RedirectResponse

    返回 RedirectResponse 实例，允许你轻松创建重定向。
    详情请参阅 :ref:`response-redirect`。

.. php:function:: remove_invisible_characters($str[, $urlEncoded = true])

    :param    string    $str: 输入字符串
    :param    bool    $urlEncoded: 是否同时移除 URL 编码的字符
    :returns:    清理后的字符串
    :rtype:    string

    此函数防止在 ASCII 字符之间插入空字符，
    如 Java\\0script。

    示例：

    .. literalinclude:: common_functions/007.php

.. php:function:: request()

    .. versionadded:: 4.3.0

    :returns:    共享的 Request 对象。
    :rtype:    IncomingRequest|CLIRequest

    此函数是 ``Services::request()`` 和 ``service('request')`` 的包装器。

.. php:function:: response()

    .. versionadded:: 4.3.0

    :returns:    共享的 Response 对象。
    :rtype:    Response

    此函数是 ``Services::response()`` 和 ``service('response')`` 的包装器。

.. php:function:: route_to($method[, ...$params])

    :param   string       $method: 路由名称或 Controller::method
    :param   int|string   ...$params: 要传递给路由的一个或多个参数。最后一个参数允许你设置区域设置。
    :returns: 路由路径（相对于 baseURL 的 URI 路径）
    :rtype: string

    .. note:: 此函数要求 controller/method 在 **app/Config/Routes.php** 中定义了路由。

    .. important:: ``route_to()`` 返回的是 *路由* 路径，而不是你网站的完整 URI 路径。
        如果你的 **baseURL** 包含子目录，则返回值与链接的 URI 不同。
        在这种情况下，请改用 :php:func:`url_to()`。
        另请参阅 :ref:`urls-url-structure`。

    根据控制器::方法组合为你生成路由。如果提供参数，将考虑参数的影响。

    .. literalinclude:: common_functions/009.php

    根据路由名称为你生成路由。

    .. literalinclude:: common_functions/010.php

    从 v4.3.0 开始，当你在路由中使用 ``{locale}`` 时，可以选择将区域设置值作为最后一个参数指定。

    .. literalinclude:: common_functions/011.php

.. php:function:: service($name[, ...$params])

    :param   string   $name: 要加载的服务名称
    :param   mixed    $params: 要传递给服务方法的一个或多个参数。
    :returns: 指定的服务类实例。
    :rtype: mixed

    提供对系统中定义的任何 :doc:`服务 <../concepts/services>` 的便捷访问。
    这将始终返回类的共享实例，因此无论在单个请求期间调用多少次，
    都只会创建一个类实例。

    示例：

    .. literalinclude:: common_functions/008.php

.. php:function:: single_service($name [, ...$params])

    :param   string   $name: 要加载的服务名称
    :param   mixed    $params: 要传递给服务方法的一个或多个参数。
    :returns: 指定的服务类实例。
    :rtype: mixed

    与上面描述的 **service()** 函数相同，只是对此函数的
    所有调用都将返回类的新实例，而 **service** 每次都返回相同的
    实例。

.. php:function:: slash_item ( $item )

    :param string $item: 配置项名称
    :returns: 配置项，如果项不存在则返回 null
    :rtype:  string|null

    获取配置文件项并在末尾添加斜杠（如果不为空）

.. php:function:: stringify_attributes($attributes [, $js])

    :param   mixed    $attributes: 字符串、键值对数组或对象
    :param   boolean  $js: 如果值不需要引号（JavaScript 风格）则为 true
    :returns: 包含属性键/值对的字符串，以逗号分隔
    :rtype: string

    辅助函数，用于将字符串、数组或对象的属性转换为字符串。

================
全局常量
================

以下常量在应用程序中的任何位置始终可用。

核心常量
==============

.. php:const:: APPPATH

    **app** 目录的路径。

.. php:const:: ROOTPATH

    项目根目录的路径。就在 ``APPPATH`` 上方。

.. php:const:: SYSTEMPATH

    **system** 目录的路径。

.. php:const:: FCPATH

    包含前端控制器的目录路径。

.. php:const:: WRITEPATH

    **writable** 目录的路径。

时间常量
==============

.. php:const:: SECOND

    等于 1。

.. php:const:: MINUTE

    等于 60。

.. php:const:: HOUR

    等于 3600。

.. php:const:: DAY

    等于 86400。

.. php:const:: WEEK

    等于 604800。

.. php:const:: MONTH

    等于 2592000。

.. php:const:: YEAR

    等于 31536000。

.. php:const:: DECADE

    等于 315360000。
