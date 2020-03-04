############
Throttler 类
############

.. contents::
    :local:
    :depth: 2

Throttler 类提供了一种非常简单的方法，可以将用户要执行的活动限制为在设定的时间段内只能进行一定次数的尝试。
这最常用于对 API 进行速率限制，或限制用户针对表单进行的尝试次数，以帮助防止暴力攻击。
该类可用于你根据设置的时间来进行限制的操作。

********
总览
********

Throttler 是 `Token Bucket （令牌桶） <https://en.wikipedia.org/wiki/Token_bucket>`_
算法的简化版本。一般，会将你要执行的每个操作都视为一个存储桶。调用该 ``check()`` 方法时，你要告诉它存储桶的大小，
可以容纳多少令牌以及时间间隔。 ``check()`` 默认情况下，每个呼叫使用1个可用令牌。让我们通过一个例子来阐明这一点。
（译注：国内用户可参考 `令牌桶 <https://baike.baidu.com/item/%E4%BB%A4%E7%89%8C%E6%A1%B6%E7%AE%97%E6%B3%95>`_ ）

假设我们希望某动作每秒发生一次。对 Throttler 的第一次呼叫将如下所示。第一个参数是存储桶名称，第二个参数是存储桶持有的令牌数量，
第三个参数是存储桶重新填充所需的时间： ::

    $throttler = \Config\Services::throttler();
    $throttler->check($name, 60, MINUTE);

我们暂时使用 `全局常量 </general/common_functions>` 的其中一个，以使其更具可读性。也就是说，这个存储桶每分钟允许执行60次操作，
或者每秒允许执行1次操作。

假设某个第三方脚本试图重复访问 URL 。最初，它能够在不到一秒钟的时间内使用完所有60个令牌。但是，在那之后，
Throttler 将仅允许每秒执行一次操作，从而有可能减慢请求的速度，以至于让攻击不再有价值。

.. note:: 为了使 Throttler 类可以正常工作，必须将 Cache 库设置为使用虚拟对象以外的处理程序。为了获得最佳性能，
    建议使用像 Redis 或 Memcached 那样的内存缓存。

*************
速率限制
*************

Throttler 类不会自己做任何的速率限制或请求节流，（？不知道咋翻译？）。这里提供了一个示例 :doc:`过滤器 </incoming/filters>` ，
该过滤器以每个IP地址每秒一个请求的速率限制实现了非常简单的速率限制。我们将介绍它的工作原理，以及如何设置它并开始在应用程序中使用它。

实现代码
========

你可以在 **app/Filters/Throttle.php** 上创建自己的Throttler过滤器，大致如下： ::

    <?php namespace App\Filters;

    use CodeIgniter\Filters\FilterInterface;
    use CodeIgniter\HTTP\RequestInterface;
    use CodeIgniter\HTTP\ResponseInterface;
    use Config\Services;

    class Throttle implements FilterInterface
    {
            /**
             * 这是一个为应用程序使用 Trottler 类来实现速率限制的实例
             *
             * @param RequestInterface|\CodeIgniter\HTTP\IncomingRequest $request
             *
             * @return mixed
             */
            public function before(RequestInterface $request)
            {
                $throttler = Services::throttler();

        		// 在整个站点上将IP地址限制为每秒不超过1个请求
        		if ($throttler->check($request->getIPAddress(), 60, MINUTE) === false)
                {
                    return Services::response()->setStatusCode(429);
        		}
            }

            //--------------------------------------------------------------------

            /**
             * 暂时无事可做
             *
             * @param RequestInterface|\CodeIgniter\HTTP\IncomingRequest $request
             * @param ResponseInterface|\CodeIgniter\HTTP\Response       $response
             *
             * @return mixed
             */
            public function after(RequestInterface $request, ResponseInterface $response)
            {
            }
    }

运行时，此方法首先获取节流阀的实例。接下来，它将IP地址用作存储桶名称，并进行设置以将其限制为每秒一个请求。
如果节流阀拒绝检查，返回false，则我们返回状态代码设置为429（太多尝试的 HTTP Response），
并且脚本执行在调用控制器之前就结束了。本示例将基于对站点的所有请求（而不是每页）中的单个IP地址进行限制。

应用过滤器
===================

我们不一定需要限制网站上的每个页面。对于许多Web应用程序，最有意义的是仅将其应用于POST请求，尽管API可能希望限制用户发出的每个请求。
为了将此应用到传入请求，您需要编辑 **/app/Config/Filters.php** 并首先向过滤器添加别名： ::

	public $aliases = [
		...
		'throttle' => \App\Filters\Throttle::class
	];

接下来，我们将其分配给网站上的所有POST请求： ::

    public $methods = [
        'post' => ['throttle', 'CSRF']
    ];

这就是全部。现在，会对网站上发出的所有POST请求进行速率限制。

***************
类参考
***************

.. php:method:: check(string $key, int $capacity, int $seconds[, int $cost = 1])

    :param string $key: 储存桶的名称
    :param int $capacity: 储存桶中持有的令牌数量
    :param int $seconds: 储存桶完全填满的秒数
    :param int $cost: 此操作将会花费的令牌数量
    :returns: 如果可以执行此操作则为 TRUE，否则为 FALSE
    :rtype: bool

    检查存储桶中是否还有令牌，或者是否在分配的时间限制内使用了太多令牌。在每次检查期间，如果成功，可用令牌将减少 $cost。

.. php:method:: getTokentime()

    :returns: 直到下一次令牌可用的秒数
    :rtype: int

    在 ``check()`` 运行并返回 FALSE 之后，可以使用此方法确定直到新令牌可用并可以再次尝试操作之前的时间。
    在这种情况下，最小强制等待时间为一秒。
