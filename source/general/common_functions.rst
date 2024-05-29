##############################
全局函数和常量
##############################

CodeIgniter 提供了一些全局定义的函数和变量,在任何时候都可以使用。这些不需要加载任何额外的库或辅助函数。

.. contents::
    :local:
    :depth: 2

================
全局函数
================

服务访问器
=================

.. php:function:: cache([$key])

    :param  string $key: 要从缓存中检索的缓存项名称(可选)
    :returns: 缓存对象实例,或从缓存中检索的项目
    :rtype: mixed

    如果没有提供 $key,将返回缓存引擎实例。如果提供了 $key,将返回当前缓存中 $key 的值,如果找不到值则返回 null。

    例子:

    .. literalinclude:: common_functions/001.php

.. php:function:: config(string $name[, bool $getShared = true])

    :param string $name: 配置类名。
    :param bool $getShared: 是否返回共享实例。
    :returns: 配置实例。
    :rtype: object|null

    从工厂获取配置实例的更简单方式。

    有关详细信息，请参阅 :ref:`Configuration <configuration-config>` 和
    :ref:`Factories <factories-config>`。

    ``config()`` 在内部使用 ``Factories::config()``。
    有关第一个参数 ``$name`` 的详细信息，请参阅 :ref:`factories-loading-class`。

.. php:function:: cookie(string $name[, string $value = ''[, array $options = []]])

    :param string $name: Cookie 名称
    :param string $value: Cookie 值
    :param array $options: Cookie 选项
    :rtype: ``Cookie``
    :returns: ``Cookie`` 实例
    :throws: ``CookieException``

    创建新的 Cookie 实例的更简单方法。

.. php:function:: cookies([array $cookies = [][, bool $getGlobal = true]])

    :param array $cookies: 如果 ``getGlobal`` 为 ``false``,则传入 ``CookieStore`` 构造函数
    :param bool $getGlobal: 如果为 ``false``,创建 ``CookieStore`` 的新实例
    :rtype: ``CookieStore``
    :returns: 保存在当前 ``Response`` 中的 ``CookieStore`` 实例,或新的 ``CookieStore`` 实例

    获取 ``Response`` 中保存的全局 ``CookieStore`` 实例。

.. php:function:: env($key[, $default = null])

    :param string $key: 要检索的环境变量名称
    :param mixed  $default: 如果找不到值,返回的默认值
    :returns: 环境变量、默认值或 null
    :rtype: mixed

    用于检索之前设置到环境中的值,如果找不到则返回默认值。会将布尔值格式化为实际的布尔值,而不是字符串表示。

    结合 **.env** 文件使用时特别有用,可设置特定于环境本身的值,如数据库设置、API 密钥等。

.. php:function:: esc($data[, $context = 'html'[, $encoding]])

    :param   string|array   $data: 要转义的信息
    :param   string   $context: 转义上下文。默认为 'html'
    :param   string   $encoding: 字符串的字符编码
    :returns: 转义后的数据
    :rtype: mixed

    为了帮助防止 XSS 攻击,对要包含在网页中的数据进行转义。这使用 Laminas Escaper 库来实际过滤数据。

    如果 $data 是字符串,则简单转义并返回它。如果 $data 是数组,则遍历它,转义每个键/值对的 'value'。

    有效的 context 值: ``html``, ``js``, ``css``, ``url``, ``attr``, ``raw``

.. php:function:: helper($filename)

    :param   string|array  $filename: 要加载的辅助器文件名,或文件名数组

    加载辅助器文件。

    有关完整详细信息,请参阅 :doc:`辅助器 <helpers>` 页面。

.. php:function:: lang($line[, $args[, $locale]])

    :param string $line: 要检索的文本行
    :param array  $args: 要替换占位符的数据数组
    :param string $locale: 指定使用的区域设置,而不是默认区域设置
    :returns: 基于别名字符串的特定区域设置的文件

    根据别名字符串检索特定区域设置的文件。

    有关更多信息,请参阅 :doc:`本地化 </outgoing/localization>` 页面。

.. php:function:: model($name[, $getShared = true[, &$conn = null]])

    :param string                   $name: 模型类名
    :param boolean                  $getShared: 是否返回共享实例
    :param ConnectionInterface|null $conn: 数据库连接
    :returns: 模型实例
    :rtype: object

    获取模型实例的更简单方法。

    ``model()`` 在内部使用 ``Factories::models()``。有关第一个参数 ``$name`` 的详细信息,请参阅 :ref:`factories-loading-class`。

    另请参阅 :ref:`使用 CodeIgniter 的模型 <accessing-models>`。

.. php:function:: old($key[, $default = null,[, $escape = 'html']])

    :param string $key: 要检查的旧表单数据的名称
    :param string|null  $default: 如果 $key 不存在,返回的默认值
    :param false|string  $escape: `转义 <#esc>`_ 上下文或设置 false 禁用它
    :returns: 定义键的值或默认值
    :rtype: array|string|null

    提供了一种简单的方式来访问提交表单后的“旧输入数据”。

    例子:

    .. literalinclude:: common_functions/002.php

.. note:: 如果你在 :doc:`表单辅助函数 </helpers/form_helper>` 中使用了 :php:func:`set_value()`、:php:func:`set_select()`、:php:func:`set_checkbox()` 和 :php:func:`set_radio()` 函数，这个功能已经内置了。只有在不使用表单辅助函数时才需要使用此函数。

.. php:function:: session([$key])

    :param string $key: 要检查的会话项目名称
    :returns: 如果没有 $key,则是 Session 对象的实例;如果有 $key,则是会话中为 $key 找到的值,如果找不到则为 null
    :rtype: mixed

    提供了方便访问 session 类和检索存储值的方法。有关更多信息,请参阅 :doc:`会话 </libraries/sessions>` 页面。

.. php:function:: timer([$name])

    :param string $name: 基准点的名称
    :returns: Timer 实例
    :rtype: CodeIgniter\Debug\Timer

    方便地快速访问 Timer 类的方法。你可以将基准点的名称作为唯一参数传递。这将从此点开始计时,或如果已运行具有此名称的计时器,则停止计时。

    例子:

    .. literalinclude:: common_functions/003.php

.. php:function:: view($name[, $data[, $options]])

    :param   string   $name: 要加载的文件的名称
    :param   array    $data: 要在视图中可用的键/值对数组
    :param   array    $options: 将传递给渲染类的选项数组
    :returns: 来自视图的输出
    :rtype: string

    获取当前与 RendererInterface 兼容的类,并告诉它渲染指定的视图。只是在控制器、库和路由闭包中使用的方便方法。

    当前,这些选项可用于 ``$options`` 数组中:

    - ``saveData`` 指定数据在同一请求内对 ``view()`` 的多次调用之间持久化。如果不想持久化数据,请指定 false。
    - ``cache`` 指定缓存视图的秒数。有关详细信息,请参阅 :ref:`caching-views`。
    - ``debug`` 可以设置为 false 以禁用为 :ref:`Debug 工具栏 <the-debug-toolbar>` 添加调试代码。

    ``$option`` 数组主要是为了方便与 Twig 等库的第三方集成。

    例子:

    .. literalinclude:: common_functions/004.php

    有关更多详细信息,请参阅 :doc:`视图 <../outgoing/views>` 和 :doc:`../outgoing/view_renderer` 页面。

.. php:function:: view_cell($library[, $params = null[, $ttl = 0[, $cacheName = null]]])

    :param string      $library:
    :param null        $params:
    :param integer     $ttl:
    :param string|null $cacheName:
    :returns: 视图单元用于在视图中插入由其他类管理的 HTML 块。
    :rtype: string

    更多详情请参考 :doc:`视图单元 </outgoing/view_cells>` 页面。

杂项函数
=======================

.. php:function:: app_timezone()

    :returns: 应用程序设置要显示日期的时区
    :rtype: string

    返回应用程序设置要显示日期的时区。

.. php:function:: csp_script_nonce()

    :returns: 脚本标签的 CSP 随机数属性
    :rtype: string

    返回脚本标签的随机数属性。例如:``nonce="Eskdikejidojdk978Ad8jf"``。请参阅 :ref:`內容安全策略 <csp-using-functions>`。

.. php:function:: csp_style_nonce()

    :returns: 样式标签的 CSP 随机数属性
    :rtype: string

    返回样式标签的随机数属性。例如:``nonce="Eskdikejidojdk978Ad8jf"``。请参阅 :ref:`內容安全策略 <csp-using-functions>`。

.. php:function:: csrf_token()

    :returns: 当前 CSRF 令牌的名称
    :rtype: string

    返回当前 CSRF 令牌的名称。

.. php:function:: csrf_header()

    :returns: 当前 CSRF 令牌的标头名称
    :rtype: string

    当前 CSRF 令牌的标头名称。

.. php:function:: csrf_hash()

    :returns: 当前 CSRF 哈希值
    :rtype: string

    返回当前 CSRF 哈希值。

.. php:function:: csrf_field()

    :returns: 包含所有必需 CSRF 信息的隐藏输入的 HTML 字符串
    :rtype: string

    返回包含所有必需 CSRF 信息的隐藏输入::

        <input type="hidden" name="{csrf_token}" value="{csrf_hash}">

.. php:function:: csrf_meta()

    :returns: 包含所有必需 CSRF 信息的 meta 标签的 HTML 字符串
    :rtype: string

    返回包含所有必需 CSRF 信息的 meta 标签::

        <meta name="{csrf_header}" content="{csrf_hash}">

.. php:function:: force_https($duration = 31536000[, $request = null[, $response = null]])

    :param  int  $duration: 浏览器应将此资源的链接转换为 HTTPS 的秒数
    :param  RequestInterface $request: 当前 Request 对象的实例
    :param  ResponseInterface $response: 当前 Response 对象的实例

    检查当前页面是否通过 HTTPS 访问。如果是，则不执行任何操作。如果不是，则将用户重定向回当前 URI，但通过 HTTPS 进行访问。将设置 HTTP 严格传输安全（HTST）头，指示现代浏览器将任何 HTTP 请求自动修改为 HTTPS 请求，持续时间为 ``$duration``。

    .. note:: 当你将 ``Config\App:$forceGlobalSecureRequests`` 设置为 true 时，也会使用此函数。

.. php:function:: function_usable($function_name)

    :param string $function_name: 要检查的函数
    :returns: 如果函数存在且可安全调用则为 true,否则为 false
    :rtype: bool

.. php:function:: is_cli()

    :returns: 如果脚本是从命令行执行的则为 true,否则为 false
    :rtype: bool

.. php:function:: is_really_writable($file)

    :param string $file: 被检查的文件名
    :returns: 如果可以写入文件则为 true,否则为 false
    :rtype: bool

.. php:function:: is_windows([$mock = null])

    :param bool|null $mock: 如果给出且为布尔值,则将其用作返回值
    :rtype: bool

    检测平台是否在 Windows 下运行。

    .. note:: 提供给 $mock 的布尔值将在后续调用中持久化。要重置此模拟值,用户必须为函数调用显式传递 ``null``。这将刷新函数以使用自动检测。

    .. literalinclude:: common_functions/012.php

.. php:function:: log_message($level, $message [, $context])

    :param   string   $level: 严重级别
    :param   string   $message: 要记录的消息
    :param   array    $context: 应在 $message 中替换的标签及其值的关联数组
    :returns: void
    :rtype: bool

    .. note:: 自 v4.5.0 起，返回值被固定为兼容 PSR Log。在以前的版本中，如果日志记录成功则返回 ``true``，如果有问题则返回 ``false``。

    使用 **app/Config/Logger.php** 中定义的日志处理程序记录消息。

    日志级别可以是以下值之一：``emergency``、``alert``、``critical``、``error``、``warning``、``notice``、``info`` 或 ``debug``。

    上下文可以用来在消息字符串中替换值。有关完整详细信息,请参阅 :doc:`日志记录信息 <logging>` 页面。

.. php:function:: redirect(string $route)

    :param  string  $route: 要重定向用户的路由名称或 Controller::method
    :rtype: RedirectResponse

    返回 RedirectResponse 实例,可轻松创建重定向。详情请参阅 :ref:`response-redirect`。

.. php:function:: remove_invisible_characters($str[, $urlEncoded = true])

    :param    string    $str: 输入字符串
    :param    bool    $urlEncoded: 是否也删除 URL 编码字符
    :returns: 经过清理的字符串
    :rtype:    string

    此函数可防止在 ASCII 字符(如 Java\\0script)之间插入空字符。

    例子:

    .. literalinclude:: common_functions/007.php

.. php:function:: request()

    .. versionadded:: 4.3.0

    :returns: 共享的 Request 对象
    :rtype: IncomingRequest|CLIRequest

    此函数是 ``Services::request()`` 的包装器。

.. php:function:: response()

    .. versionadded:: 4.3.0

    :returns: 共享的 Response 对象
    :rtype: Response

    此函数是 ``Services::response()`` 的包装器。

.. php:function:: route_to($method[, ...$params])

    :param   string       $method: 路由名称或 Controller::method
    :param   int|string   ...$params: 要传递给路由的一个或多个参数。最后一个参数允许你设置区域设置。
    :returns: 路由路径(基于 baseURL 的 URI 相对路径)
    :rtype: string

    .. note:: 此函数要求控制器/方法必须在 **app/Config/Routes.php** 中定义路由。

    .. important:: ``route_to()`` 返回一个 *路由* 路径,而不是站点的完整 URI 路径。如果你的 **baseURL** 包含子文件夹,返回值与链接的 URI 并不相同。在这种情况下,请改用 :php:func:`url_to()`。另请参阅 :ref:`urls-url-structure`。

    根据 controller::method 组合为你生成路由。将根据提供的参数生成路由。

    .. literalinclude:: common_functions/009.php

    根据路由名称为你生成路由。

    .. literalinclude:: common_functions/010.php

    从 v4.3.0 开始,当你在路由中使用 ``{locale}`` 时,可以可选地将区域设置值作为最后一个参数指定。

    .. literalinclude:: common_functions/011.php

.. php:function:: service($name[, ...$params])

    :param   string   $name: 要加载的服务名称
    :param   mixed    $params: 要传递给服务方法的一个或多个参数
    :returns: 指定的服务类的实例
    :rtype: mixed

    提供对系统中定义的任何 :doc:`服务 <../concepts/services>` 的简单访问。这将始终返回该类的共享实例,因此无论在单次请求期间调用多少次,都只会创建一个类实例。

    例子:

    .. literalinclude:: common_functions/008.php

.. php:function:: single_service($name [, ...$params])

    :param   string   $name: 要加载的服务名称
    :param   mixed    $params: 要传递给服务方法的一个或多个参数
    :returns: 指定的服务类的实例
    :rtype: mixed

    与上面描述的 **service()** 函数相同,但此函数的所有调用都将返回一个新的类实例,而 **service** 每次都返回相同的实例。

.. php:function:: slash_item ( $item )

    :param string $item: 配置项目名称
    :returns: 配置项目或如果项目不存在则为 null
    :rtype:  string|null

    获取附加斜杠的配置文件项目(如果不为空)

.. php:function:: stringify_attributes($attributes [, $js])

    :param   mixed    $attributes: 字符串、键值对数组或对象
    :param   boolean  $js: 如果值不需要引号(Javascript 风格)则为 true
    :returns: 逗号分隔的包含属性键/值对的字符串
    :rtype: string

    将字符串、数组或属性对象转换为字符串的辅助函数。

================
全局常量
================

以下常量在应用程序中的任何位置始终可用。

核心常量
==============

.. php:const:: APPPATH

    **app** 目录的路径。

.. php:const:: ROOTPATH

    项目根目录的路径。刚好在 ``APPPATH`` 之上。

.. php:const:: SYSTEMPATH

    **system** 目录的路径。

.. php:const:: FCPATH

    保存前端控制器的目录的路径。

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
