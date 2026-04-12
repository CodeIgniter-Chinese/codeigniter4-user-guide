############
Throttler 类
############

.. contents::
    :local:
    :depth: 2

Throttler 类提供了一种非常简单的方式，用于限制在指定时间段内执行某项操作的次数。此功能最常用于 API 速率限制，或限制表单提交次数以防范暴力破解攻击。实际上，对于任何需要根据特定时间间隔限制操作频率的场景，都可以使用该类。

********
概述
********

节流器实现了简化版的 `令牌桶 <https://en.wikipedia.org/wiki/Token_bucket>`_
算法。其基本原理是将每一项需要限制的操作视为一个“桶”。调用 ``check()`` 方法时，
需指定桶的容量（即能容纳的令牌数）以及时间间隔。默认情况下，每次调用 ``check()`` 会消耗 1 个可用令牌。下面通过示例进行说明。

假设我们希望某个动作每秒执行一次。首次调用节流器时，代码如下所示。
第一个参数是桶的名称，第二个参数是桶的容量（令牌数），
第三个参数是桶重新填充所需的时间：

.. literalinclude:: throttler/001.php

这里使用了 :doc:`全局常量 </general/common_functions>` 之一来表示时间，使代码更具可读性。这表示桶允许每分钟 60 次动作，即每秒 1 次动作。

假设有第三方脚本试图反复访问某个 URL。最初，该脚本可以在不到一秒的时间内耗尽所有 60
个令牌。但此后节流器将只允许每秒执行一次动作，
从而将请求速度降低到攻击不再划算的程度。

.. note:: 要使 Throttler 类正常工作，必须将缓存库配置为使用 Dummy 以外的处理程序。
            为获得最佳性能，推荐使用 Redis 或 Memcached 等内存缓存。

*************
速率限制
*************

Throttler 类本身不会执行任何速率限制或请求节流，但它是实现这些功能的关键。
项目提供了一个示例 :doc:`过滤器 </incoming/filters>`，实现了简单的速率限制：
每个 IP 地址每秒一次请求。下面将说明其工作原理，以及如何在应用中配置和使用。

代码
========

可在 **app/Filters/Throttle.php** 创建节流器过滤器，
代码如下：

.. literalinclude:: throttler/002.php

运行此方法时，首先获取节流器实例。然后使用 IP 地址作为桶名称，
将限制设置为每秒一次请求。如果节流器拒绝检查（返回 false），
则返回状态码为 429（Too Many Attempts）的响应，脚本执行将终止，
不会到达控制器。此示例基于单个 IP 地址对所有站点请求进行节流，
而非针对每个页面。

应用过滤器
===================

并非站点的每个页面都需要节流。对于许多 Web 应用，最合理的做法是仅应用于 POST 请求，
而 API 可能需要限制用户的每个请求。要将节流应用于传入请求，
需要编辑 **app/Config/Filters.php**，首先为过滤器添加别名：

.. literalinclude:: throttler/003.php

然后将其应用到站点的所有 POST 请求：

.. literalinclude:: throttler/004.php

.. warning:: 如果使用了 ``$methods`` 过滤器，应 :ref:`禁用自动路由（传统版） <use-defined-routes-only>`
    因为 :ref:`auto-routing-legacy` 允许任何 HTTP 方法访问控制器。
    使用非预期方法访问控制器可能会绕过过滤器。

设置完成后，站点上的所有 POST 请求都将受到速率限制。

***************
类参考
***************

.. php:method:: check(string $key, int $capacity, int $seconds[, int $cost = 1])

    :param string $key: 桶的名称
    :param int $capacity: 桶可容纳的令牌数量
    :param int $seconds: 桶完全重新填充所需的秒数
    :param int $cost: 此动作消耗的令牌数量
    :returns: 动作可执行时返回 true，否则返回 false
    :rtype: bool

    检查桶内是否还有可用令牌，或在指定时间限制内是否已使用过多令牌。
    每次检查时，如果通过，可用令牌将减少 $cost 个。

.. php:method:: getTokentime()

    :returns: 下一个令牌可用前应等待的秒数。
    :rtype: integer

    在 ``check()`` 返回 false 后，可使用此方法确定
    到新令牌可用、可以再次尝试动作之前需要等待的时间。
    此时，强制的最小等待时间为 1 秒。

.. php:method:: remove(string $key) : self

    :param string $key: 桶的名称
    :returns: $this
    :rtype: self

    移除并重置桶。
    桶不存在时也不会失败。
