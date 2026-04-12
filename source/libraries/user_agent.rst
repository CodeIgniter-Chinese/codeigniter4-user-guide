################
User Agent 类
################

User Agent 类提供了一些辅助函数，用于识别访问站点的浏览器、移动设备或爬虫的相关信息。

.. contents::
    :local:
    :depth: 2

**************************
使用 User Agent 类
**************************

初始化类
======================

User Agent 类始终可直接从当前的 :doc:`IncomingRequest </incoming/incomingrequest>` 实例获取。
默认情况下，控制器中有一个 request 实例，可从中获取 User Agent 类：

.. literalinclude:: user_agent/001.php

User Agent 定义
======================

User Agent 名称定义位于以下配置文件：
**app/Config/UserAgents.php**。如有需要，可向各个 User Agent 数组中添加条目。

示例
=======

User Agent 类初始化时，会尝试判断访问站点的是网页浏览器、移动设备还是爬虫，
同时会尝试获取平台信息（如有）：

.. literalinclude:: user_agent/002.php

***************
类参考
***************

.. php:namespace:: CodeIgniter\HTTP

.. php:class:: UserAgent

    .. php:method:: isBrowser([$key = null])

        :param    string    $key: 可选的浏览器名称
        :returns:    如果 User Agent 是（指定的）浏览器则返回 true，否则返回 false
        :rtype:    bool

        判断 User Agent 是否为已知的网页浏览器，返回布尔值。

        .. literalinclude:: user_agent/003.php

        .. note:: 此示例中的字符串 "Safari" 是浏览器定义数组中的键名。
                  可在 **app/Config/UserAgents.php** 中查找此列表，以便添加新浏览器或修改对应字符串。

    .. php:method:: isMobile([$key = null])

        :param    string    $key: 可选的移动设备名称
        :returns:    如果 User Agent 是（指定的）移动设备则返回 true，否则返回 false
        :rtype:    bool

        判断 User Agent 是否为已知的移动设备，返回布尔值。

        .. literalinclude:: user_agent/004.php

    .. php:method:: isRobot([$key = null])

        :param    string    $key: 可选的爬虫名称
        :returns:    如果 User Agent 是（指定的）爬虫则返回 true，否则返回 false
        :rtype:    bool

        判断 User Agent 是否为已知的爬虫（robot），返回布尔值。

        .. note:: User Agent 库仅包含最常见的爬虫定义，并非完整的爬虫列表。
                  爬虫数量庞大，逐一搜索效率很低。如果发现访问站点的常见爬虫不在列表中，
                  可自行添加到 **app/Config/UserAgents.php** 文件。

    .. php:method:: isReferral()

        :returns:    如果 User Agent 来自外部站点引用则返回 true，否则返回 false
        :rtype:    bool

        判断 User Agent 是否从其他站点跳转而来，返回布尔值。

    .. php:method:: getBrowser()

        :returns:    检测到的浏览器名称或空字符串
        :rtype:    string

        返回访问站点的网页浏览器名称。

    .. php:method:: getVersion()

        :returns:    检测到的浏览器版本号或空字符串
        :rtype:    string

        返回访问站点的网页浏览器版本号。

    .. php:method:: getMobile()

        :returns:    检测到的移动设备品牌或空字符串
        :rtype:    string

        返回访问站点的移动设备名称。

    .. php:method:: getRobot()

        :returns:    检测到的爬虫名称或空字符串
        :rtype:    string

        返回访问站点的爬虫名称。

    .. php:method:: getPlatform()

        :returns:    检测到的操作系统或空字符串
        :rtype:    string

        返回访问站点的平台信息（Linux、Windows、OS X 等）。

    .. php:method:: getReferrer()

        :returns:    检测到的引用来源或空字符串
        :rtype:    string

        若访问请求是从其他站点跳转而来，则返回引用来源（Referrer） 。通常按以下方式测试：

        .. literalinclude:: user_agent/005.php

    .. php:method:: getAgentString()

        :returns:    完整的 User Agent 字符串或空字符串
        :rtype:    string

        返回完整的 User Agent 字符串，通常类似如下格式::

            Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.0.4) Gecko/20060613 Camino/1.0.2

    .. php:method:: parse($string)

        :param    string    $string: 自定义的 User Agent 字符串
        :rtype:    void

        解析自定义的 User Agent 字符串，与当前访问者报告的 User Agent 不同。
