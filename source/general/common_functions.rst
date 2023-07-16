##############################
全局函数和常量
##############################

CodeIgniter 提供了一些全局定义的函数和变量,在任何时候都可以使用。这些不需要加载任何额外的库或辅助程序。

.. contents::
  :local:
  :depth: 2

================
全局函数
================

服务访问器
=================

.. php:function:: cache([$key])

  :param  string $key: 要从缓存中检索的缓存名称(可选)
  :returns: 缓存对象本身,或从缓存中检索到的项目
  :rtype: mixed

  如果没有提供 $key,将返回缓存引擎实例。如果提供了 $key,将返回当前缓存中 $key 的值,如果没有找到值则返回 null。

  例子:

  .. literalinclude:: common_functions/001.php

.. php:function:: config(string $name[, bool $getShared = true])

  :param string $name: 配置类名。
  :param bool $getShared: 是否返回共享实例。
  :returns: 配置实例。
  :rtype: object|null

  从 Factories 获取配置实例的更简单方法。

  详情请见 :ref:`配置 <configuration-config>` 和
  :ref:`Factories <factories-config>`。

  ``config()`` 内部使用 ``Factories::config()``。
  关于第一个参数 ``$name`` 的详情请见 :ref:`factories-loading-class`。

.. php:function:: cookie(string $name[, string $value = ''[, array $options = []]])

  :param string $name: Cookie 名称
  :param string $value: Cookie 值
  :param array $options: Cookie 选项
  :rtype: ``Cookie``
  :returns: ``Cookie`` 实例
  :throws: ``CookieException``

  更简单地创建新的 Cookie 实例的方法。

.. php:function:: cookies([array $cookies = [][, bool $getGlobal = true]])

  :param array $cookies: 如果 ``getGlobal`` 是 ``false``,则传递给 ``CookieStore`` 的构造函数。
  :param bool $getGlobal: 如果为 ``false``,创建一个新的 ``CookieStore`` 实例。
  :rtype: ``CookieStore``
  :returns: 保存在当前 ``Response`` 中的全局 ``CookieStore`` 实例,或者一个新的 ``CookieStore`` 实例。

  获取 ``Response`` 中保存的全局 ``CookieStore`` 实例。

.. php:function:: env($key[, $default = null])

  :param string $key: 要检索的环境变量名称
  :param mixed  $default: 如果没有找到值,返回的默认值。
  :returns: 环境变量、默认值或 null。
  :rtype: mixed

  用于检索之前设置到环境中的值,如果没有找到则返回默认值。会将布尔值格式化为实际的布尔值,而不是字符串表示。

  当与 **.env** 文件一起使用时,设置特定于环境本身的值(如数据库设置、API 密钥等)特别有用。

.. php:function:: esc($data[, $context = 'html'[, $encoding]])

  :param   string|array   $data: 要转义的信息。
  :param   string   $context: 转义上下文。默认为 'html'。
  :param   string   $encoding: 字符串的字符编码。
  :returns: 转义后的数据。
  :rtype: mixed

  为了帮助防止 XSS 攻击,转义要包含在网页中的数据。
  这使用 Laminas Escaper 库来处理数据的实际过滤。

  如果 $data 是字符串,则仅转义并返回它。
  如果 $data 是数组,则循环遍历它,转义键/值对的每个“值”。

  有效的 context 值:html、js、css、url、attr、raw

.. php:function:: helper($filename)

  :param   string|array  $filename: 要加载的辅助文件名,或文件名数组

  加载辅助文件。

  完整细节请见 :doc:`helpers` 页。

.. php:function:: lang($line[, $args[, $locale]])

  :param string $line: 要检索的文本行
  :param array  $args: 用来替换占位符的数据数组。
  :param string $locale: 指定使用默认 locales 以外的其他 locales。

  根据别名字符串检索特定于语言环境的文件。

  更多信息请见 :doc:`本地化 </outgoing/localization>` 页。

.. php:function:: model($name[, $getShared = true[, &$conn = null]])

  :param string                   $name: 模型类名。
  :param boolean                  $getShared: 是否返回共享实例。
  :param ConnectionInterface|null $conn: 数据库连接。
  :returns: 模型实例
  :rtype: object

  更简单地获取模型实例的方法。

  ``model()`` 内部使用 ``Factories::models()``。
  关于第一个参数 ``$name`` 的详情请见 :ref:`factories-loading-class`。

  也可见 :ref:`使用 CodeIgniter 的模型 <accessing-models>`。

.. php:function:: old($key[, $default = null,[, $escape = 'html']])

  :param string $key: 要检查的旧表单数据的名称。
  :param mixed  $default: 如果 $key 不存在,返回的默认值。
  :param mixed  $escape: `转义 <#esc>`_ 上下文或禁用转义的 false。
  :returns: 定义键的值,或默认值。
  :rtype: mixed

  提供简单的方式来访问提交表单后的“旧输入数据”。

  例子:

  .. literalinclude:: common_functions/002.php

.. note:: 如果使用 :doc:`表单辅助程序 </helpers/form_helper>`,则此功能内置。只有在不使用表单辅助程序时,您才需要使用此函数。

.. php:function:: session([$key])

  :param string $key: 要检查的 session 项目名称。
  :returns: 如果没有 $key,则是 Session 对象实例;如果有 $key,则是在 session 中为 $key 找到的值,或者 null。
  :rtype: mixed

  提供方便的方法来访问 session 类和检索存储的值。更多信息请见 :doc:`Sessions </libraries/sessions>` 页。

.. php:function:: timer([$name])

  :param string $name: 基准点的名称。
  :returns: Timer 实例
  :rtype: CodeIgniter\Debug\Timer

  提供快速访问 Timer 类的便捷方法。您可以将基准点的名称作为唯一参数传递。这将从此点开始计时,或者如果具有此名称的计时器已经在运行,则停止计时。

  例子:

  .. literalinclude:: common_functions/003.php

.. php:function:: view($name[, $data[, $options]])

  :param   string   $name: 要加载的文件名
  :param   array    $data: 可在视图中使用的键/值对数组。
  :param   array    $options: 将传递给渲染类的选项数组。
  :returns: 来自视图的输出。
  :rtype: string

  获取当前 RendererInterface 兼容类,并告诉它渲染指定的视图。仅为在控制器、库和路由闭包中使用提供了方便的方法。

  当前,这些选项可在 ``$options`` 数组中使用:

  - ``saveData`` 指定数据在同一请求内对 ``view()`` 的多次调用之间是否持久化。如果您不希望数据被持久化,请指定 false。
  - ``cache`` 指定缓存视图的秒数。详情请见 :ref:`caching-views`。
  - ``debug`` 可以设置为 false 以禁用为 :ref:`Debug Toolbar <the-debug-toolbar>` 添加调试代码。

  ``$option`` 数组主要是为了方便与 Twig 等第三方库的集成。

  ``view()`` 内部使用 ``RendererInterface`` 兼容类的 ``render()`` 方法。

  例子:

  .. literalinclude:: common_functions/004.php

  更多细节请见 :doc:`Views </outgoing/views>` 页。

.. php:function:: view_cell($library[, $params = null[, $ttl = 0[, $cacheName = null]]])

  :param string      $library:
  :param null        $params:
  :param integer     $ttl:
  :param string|null $cacheName:
  :returns: View Cells 在视图中用于插入由其他类管理的 HTML 代码块。
  :rtype: string

  更多细节请见 :doc:`View Cells </outgoing/view_cells>` 页。

其他函数
=======================

.. php:function:: app_timezone()

  :returns: 应用程序设置显示日期的时区。
  :rtype: string

  返回应用程序设置显示日期的时区。

.. php:function:: csp_script_nonce()

  :returns: script 标签的 CSP nonce 属性。
  :rtype: string

  返回 script 标签的 nonce 属性,例如: ``nonce="Eskdikejidojdk978Ad8jf"``。
  请参阅 :ref:`内容安全策略 <content-security-policy>`。

.. php:function:: csp_style_nonce()

  :returns: style 标签的 CSP nonce 属性。
  :rtype: string

  返回 style 标签的 nonce 属性,例如: ``nonce="Eskdikejidojdk978Ad8jf"``。
  请参阅 :ref:`内容安全策略 <content-security-policy>`。

.. php:function:: csrf_token()

  :returns: 当前 CSRF token 的名称。
  :rtype: string

  返回当前 CSRF token 的名称。

.. php:function:: csrf_header()

  :returns: 当前 CSRF token 头的名称。
  :rtype: string

  当前 CSRF token 头的名称。

.. php:function:: csrf_hash()

  :returns: 当前 CSRF hash 的值。
  :rtype: string

  返回当前 CSRF hash 值。

.. php:function:: csrf_field()

  :returns: 包含所有必需 CSRF 信息的隐藏输入的字符串。
  :rtype: string

  返回包含 CSRF 信息的隐藏输入::

    <input type="hidden" name="{csrf_token}" value="{csrf_hash}">

.. php:function:: csrf_meta()

  :returns: 包含所有必需 CSRF 信息的 meta 标签的字符串。
  :rtype: string

  返回包含 CSRF 信息的 meta 标签::

    <meta name="{csrf_header}" content="{csrf_hash}">

.. php:function:: force_https($duration = 31536000[, $request = null[, $response = null]])

  :param  int   $duration: 浏览器应将此资源的链接转换为 HTTPS 的秒数。
  :param  RequestInterface $request: 当前 Request 对象的一个实例。
  :param  ResponseInterface $response: 当前 Response 对象的一个实例。

  检查页面是否正在通过 HTTPS 访问。如果是,则什么都不会发生。如果不是,则用户会被重定向回当前 URI,但通过 HTTPS。
  将设置 HTTP 严格传输安全性 (HTST) 头,指示现代浏览器自动将任何 HTTP 请求修改为 HTTPS 请求,持续时间为 ``$duration``。

  .. note:: 当您设置 ``Config\App:$forceGlobalSecureRequests`` 为 true 时,也会使用此函数。

.. php:function:: function_usable($function_name)

  :param string $function_name: 要检查的函数
  :returns: 如果函数存在且可安全调用则为 true,否则为 false。
  :rtype: bool

.. php:function:: is_cli()

  :returns: 如果脚本是从命令行执行的则为 true,否则为 false。
  :rtype: bool

.. php:function:: is_really_writable($file)

  :param string $file: 被检查的文件名。
  :returns: 如果可以写入文件则为 true,否则为 false。
  :rtype: bool

.. php:function:: is_windows([$mock = null])

  :param bool|null $mock: 如果给出且为布尔值,则将其用作返回值。
  :rtype: bool

  检测平台是否在 Windows 上运行。

  .. note:: 提供给 $mock 的布尔值将在后续调用中持久化。要重置此模拟值,用户必须向函数调用显式传递 null。这将刷新函数以使用自动检测。

  .. literalinclude:: common_functions/012.php

.. php:function:: log_message($level, $message [, $context])

  :param   string   $level: 严重级别
  :param   string   $message: 要记录的消息。
  :param   array    $context: 标签和值的关联数组,应在 $message 中替换
  :returns: 如果日志成功则返回 true,如果记录时有问题则返回 false
  :rtype: bool

  使用 **app/Config/Logger.php** 中定义的日志处理程序记录消息。

  级别可以是以下值之一:**emergency**、**alert**、**critical**、**error**、**warning**、
  **notice**、**info** 或 **debug**。

  上下文可以用于在消息字符串中替换值。完整细节请见
  :doc:`日志记录信息 <logging>` 页。

.. php:function:: redirect(string $route)

  :param  string  $route: 要重定向用户的路由名称或 Controller::method
  :rtype: RedirectResponse

  返回一个 RedirectResponse 实例,允许您轻松创建重定向。
  详情请见 :ref:`response-redirect`。

.. php:function:: remove_invisible_characters($str[, $urlEncoded = true])

  :param    string    $str: 输入字符串
  :param    bool    $urlEncoded: 是否也去除 URL 编码字符
  :returns:    过滤后的字符串
  :rtype:    string

  此函数可防止在 ASCII 字符之间插入 null 字符,像 Java\\0script。

  例子:

  .. literalinclude:: common_functions/007.php

.. php:function:: request()

  .. versionadded:: 4.3.0

  :returns:    共享的 Request 对象。
  :rtype:    IncomingRequest|CLIRequest

  该函数是 ``Services::request()`` 的包装器。

.. php:function:: response()

  .. versionadded:: 4.3.0

  :returns:    共享的 Response 对象。
  :rtype:    Response

  该函数是 ``Services::response()`` 的包装器。

.. php:function:: route_to($method[, ...$params])

  :param   string       $method: 路由名称或 Controller::method
  :param   int|string   ...$params: 将传递到路由的一个或多个参数。最后一个参数允许您设置语言环境。
  :returns: 路由路径(相对于 baseURL 的 URI 路径)
  :rtype: string

  .. note:: 此函数要求在 **app/Config/routes.php** 中为控制器/方法定义路由。

  .. important:: ``route_to()`` 返回一个*路由*路径,而不是站点的完整 URI 路径。
      如果您的 **baseURL** 包含子文件夹,返回值与要链接的 URI 不相同。
      在这种情况下,请改用 :php:func:`url_to()`。
      另请参阅 :ref:`urls-url-structure`。

  根据控制器::方法组合为您生成路由。如果提供了参数,则会将参数考虑在内。

  .. literalinclude:: common_functions/009.php

  根据路由名称为您生成路由。

  .. literalinclude:: common_functions/010.php

  从 v4.3.0 开始,当您在路由中使用 ``{locale}`` 时,可以将语言环境值作为最后一个参数可选地指定。

  .. literalinclude:: common_functions/011.php

.. php:function:: service($name[, ...$params])

  :param   string   $name: 要加载的服务名称
  :param   mixed    $params: 要传递给服务方法的参数。
  :returns: 指定服务类的一个实例。
  :rtype: mixed

  轻松访问系统中定义的任何 :doc:`服务 <../concepts/services>`。
  无论在单个请求期间调用多少次,这都总是返回该类的共享实例,因此只会创建一个类实例。

  例子:

  .. literalinclude:: common_functions/008.php

.. php:function:: single_service($name [, ...$params])

  :param   string   $name: 要加载的服务名称
  :param   mixed    $params: 要传递给服务方法的参数。
  :returns: 指定服务类的一个实例。
  :rtype: mixed

  与上述 **service()** 函数相同,区别是此函数的所有调用都将返回该类的新实例,而 **service()** 每次都返回相同的实例。

.. php:function:: slash_item ( $item )

  :param string $item: 配置项目名称
  :returns: 配置项目的值或如果项目不存在则返回 null
  :rtype:  string|null

  添加斜杠并获取配置文件项目(如果不为空)

.. php:function:: stringify_attributes($attributes [, $js])

  :param   mixed    $attributes: 字符串、键值对数组或对象
  :param   boolean  $js: 如果值不需要引号(Javascript 风格)则为 true
  :returns: 包含逗号分隔的属性键/值对的字符串
  :rtype: string

  将字符串、数组或对象的属性转换为字符串的辅助函数。

================
全局常量
================

以下常量在应用程序中的任何位置始终可用。

核心常量
==============

.. php:const:: APPPATH

  应用目录的路径。

.. php:const:: ROOTPATH

  项目根目录的路径。刚好在 ``APPPATH`` 上面。

.. php:const:: SYSTEMPATH

  系统目录的路径。

.. php:const:: FCPATH

  存放前端控制器的目录的路径。

.. php:const:: WRITEPATH

  可写目录的路径。

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
