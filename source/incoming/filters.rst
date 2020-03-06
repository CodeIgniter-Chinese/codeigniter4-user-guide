##################
过滤器
##################

.. contents::
    :local:
    :depth: 2

过滤器可以是在控制器运行前或者运行后执行相应的操作，与 :doc:`events </extending/events>` 不同，你可以非常简单、方便的选择在应用程序的哪个 URI 上应用过滤器。
过滤器可以修改传入的请求，也可以对响应做出修改，从而具有很大的灵活性和功能性。我们可以使用过滤器执行一些共同的常见的任务，例如：

* 传入的请求执行 CSRF 验证
* 根据用户角色控制显示的功能
* 在某些功能或接口执行请求速率限制
* 显示 “停机维护” 页面
* 自动执行内容协商操作（例如设置 Accept-Language 值）
* 更多

*****************
创建过滤器
*****************

过滤器类必须实现 ``CodeIgniter\Filters\FilterInterface`` 接口。
过滤器类必须有 2 个方法：``before()`` 和 ``after()``，它们会在控制器运行之前和之后执行。
如果你的业务只需要其中一个方法，那另外的方法留空即可，不可以删除。
一个标准的过滤器类模板如下::

    <?php namespace App\Filters;

    use CodeIgniter\HTTP\RequestInterface;
    use CodeIgniter\HTTP\ResponseInterface;
    use CodeIgniter\Filters\FilterInterface;

    class MyFilter implements FilterInterface
    {
        public function before(RequestInterface $request)
        {
            // Do something here
        }

        //--------------------------------------------------------------------

        public function after(RequestInterface $request, ResponseInterface $response)
        {
            // Do something here
        }
    }

前置过滤器
==============

任何过滤器，你都可以返回 ``$request`` 对象并且可以对当前的请求进行更改替换，这些更改在后续的控制器执行时，仍然有效。

因为是前置过滤器，它会在控制器被执行前触发，所以你有时会希望做一些验证操作，不执行后续的控制器，例如登录验证。那么你可以通过返回不是请求对象的任何形式来做到这一点。
通常是执行重定向。
例如以下的示例::

    public function before(RequestInterface $request)
    {
        $auth = service('auth');

        if (! $auth->isLoggedIn())
        {
            return redirect('login');
        }
    }

如果返回了 ``Response`` 对象，那么 ``Response`` 对象会发送到客户端，并且程序会停止运行。这对实现 API 速率限制很有作用，详细可以参考
**app/Filters/Throttle.php** 相关示例。

后置过滤器
=============

后置过滤器与前置过滤器几乎一样，不同的是后置过滤器只返回 ``$response`` 对象。并且，你无法停止程序的运行。你只能对 ``$response`` 对象
做一些修改，比如为了确保客户端可以正常识别而设置某些安全选项，或者使用缓存输出，甚至可以使用错别字过滤器过滤最终的输出内容。

*******************
配置过滤器
*******************

创建完过滤器后，你需要在 ``app/Config/Filters.php`` 配置它的运行时机。该文件包含了 4 个属性，可以精确控制过滤器的运行时机。

$aliases
========

``$aliases`` 数组可以将一个简单的名称与一个或多个完整类的路径进行绑定关联，这些完整的类就是需要运行的过滤器::

    public $aliases = [
        'csrf' => \CodeIgniter\Filters\CSRF::class
    ];

别名是强制性的，如果你尝试使用完整的类名，系统会触发一个错误。以别名方式定义，可以很容易的切换实现类。例如当你需要替换其他过滤器时，只需
要更改别名对应的类即可。

当然，你也可以将多个过滤器绑定到一个别名中，这样可以使复杂的过滤器组变得简单::

    public $aliases = [
        'apiPrep' => [
            \App\Filters\Negotiate::class,
            \App\Filters\ApiAuth::class
        ]
    ];

可以在 ``$aliases`` 中定义多个别名，已满足系统需求。

$globals
========

这部分允许你定义应用程序中每个请求需要经过的过滤器。
请一定要注意过滤器的数量，因为所有的请求都将经过这些过滤器，过多会导致影响性能。可以在 ``before`` 和 ``after`` 中添加别名来指定
过滤器::

	public $globals = [
		'before' => [
			'csrf'
		],
		'after'  => []
	];

有时候你希望对绝大多数请求都使用过滤器处理，但个别请求需要单独处理时，这样的情况很常见。
一个常见的场景，你需要在 ``CSRF`` 过滤器中排除一些请求，例如来自第三方的请求或者特定的 URI 地址，其他请求则必须经过 ``CSRF`` 验证。
那么，我们可以通过 ``except`` 来实现，可以定义一个或多个排除的 URI 地址::

	public $globals = [
		'before' => [
			'csrf' => ['except' => 'api/*']
		],
		'after'  => []
	];

可以设置任意完整的 URI，也可以使用正则表达式，或者像本示例一样，设置 * 通配符的形式来设置。这样以 ``api/`` 开头的所有请求都将不受 CSRF
过滤器的保护。但该应用程序的其他请求不受影响。如果你需要指定多个 URI，可以使用数组的形式即可，具体可以参考示例::

	public $globals = [
		'before' => [
			'csrf' => ['except' => ['foo/*', 'bar/*']]
		],
		'after'  => []
	];

$methods
========

你可以将过滤器应用于请求的某些方法，例如 POST、GET、PUT等，在数组中使用全部小写的形式指定过滤器名称，与 ``$globals`` 或 ``$filters``
属性设置目的不同，这些过滤器全部都是前置过滤器，也就是说都在控制器运行前执行::

    public $methods = [
        'post' => ['foo', 'bar'],
        'get'  => ['baz']
    ]

除标准的 HTTP 方法外，还支持两种特殊的方法：'cli' 和 'ajax'。它们是所有的 'cli' 命令行运行的请求和 AJAX 请求。

.. note:: AJAX 请求的界定在 ``X-Requested-With`` 标志，在某些情况下，``X-Requested-With`` 不会通过 JavaScript 的 XHR 请求发送到后端，从而导致过滤器无法执行。如何避免此类问题，请参照文档的 :doc:`AJAX Requests </general/ajax>` 章节。

$filters
========

这个属性是过滤器别名数组，每个别名可以定义指定 URI 的前置或后置过滤器::

    public filters = [
        'foo' => ['before' => ['admin/*'], 'after' => ['users/*']],
        'bar' => ['before' => ['api/*', 'admin/*']]
    ];

****************
默认提供的过滤器
****************

CodeIgniter4 默认绑定了三个过滤器：Honeypot、Security 和 DebugToolbar。
