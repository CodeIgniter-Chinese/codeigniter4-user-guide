################
User Agent 类
################

User Agent 类提供了一些有助于识别访问你网站的浏览器、移动设备或机器人的信息的函数。

.. contents::
    :local:
    :depth: 2

**************************
使用 User Agent 类
**************************

初始化类
======================

User Agent 类总是可以直接从当前的 :doc:`IncomingRequest </incoming/incomingrequest>` 实例获取。
默认情况下,在你的控制器中会有一个请求实例,你可以从中获取 User Agent 类:

.. literalinclude:: user_agent/001.php

User Agent 定义
======================

User Agent 名称定义位于以下配置文件中:**app/Config/UserAgents.php**。
如果需要的话你可以在各种 User Agent 数组中添加项。

示例
=======

当 User Agent 类被初始化时,它会试图确定是否正在浏览你的网站的 User Agent 是网页浏览器、移动设备还是机器人。
如果可用的话,它也会收集平台信息:

.. literalinclude:: user_agent/002.php

***************
类参考
***************

.. php:namespace:: CodeIgniter\HTTP

.. php:class:: UserAgent

    .. php:method:: isBrowser([$key = null])

        :param    string    $key: 可选的浏览器名称
        :returns:    如果 User Agent 是(指定的)浏览器则为 true,否则为 false
        :rtype:    bool

        如果 User Agent 是已知的网页浏览器,则返回 true/false(布尔值)。

        .. literalinclude:: user_agent/003.php

        .. note:: 这个示例中的“Safari”字符串是浏览器定义列表中的一个数组键。
            如果你想添加新浏览器或更改字符串,可以在 **app/Config/UserAgents.php** 文件中找到这个列表。

    .. php:method:: isMobile([$key = null])

        :param    string    $key: 可选的移动设备名称
        :returns:    如果 User Agent 是(指定的)移动设备则为 true,否则为 false
        :rtype:    bool

        如果 User Agent 是已知的移动设备,则返回 true/false(布尔值)。

        .. literalinclude:: user_agent/004.php

    .. php:method:: isRobot([$key = null])

        :param    string    $key: 可选的机器人名称
        :returns:    如果 User Agent 是(指定的)机器人则为 true,否则为 false
        :rtype:    bool

        如果 User Agent 是已知的机器人,则返回 true/false(布尔值)。

        .. note:: User Agent 库只包含最常见的机器人定义。这不是一个完整的机器人列表。
            有成百上千个,逐个搜索每一个效率不高。如果你发现一些常访问你网站但列表中缺失的机器人,
            可以添加到你的 **app/Config/UserAgents.php** 文件中。

    .. php:method:: isReferral()

        :returns:    如果 User Agent 来自其他网站的推荐则为 true,否则为 false
        :rtype:    bool

        如果 User Agent 来自其他网站的推荐,则返回 true/false(布尔值)。

    .. php:method:: getBrowser()

        :returns:    检测到的浏览器或空字符串
        :rtype:    string

        返回查看你网站的网页浏览器的名称字符串。

    .. php:method:: getVersion()

        :returns:    检测到的浏览器版本或空字符串
        :rtype:    string

        返回查看你网站的网页浏览器的版本号字符串。

    .. php:method:: getMobile()

        :returns:    检测到的移动设备品牌或空字符串
        :rtype:    string

        返回查看你网站的移动设备的名称字符串。

    .. php:method:: getRobot()

        :returns:    检测到的机器人名称或空字符串
        :rtype:    string

        返回查看你网站的机器人的名称字符串。

    .. php:method:: getPlatform()

        :returns:    检测到的操作系统或空字符串
        :rtype:    string

        返回查看你网站的平台(Linux、Windows、OS X等)的字符串。

    .. php:method:: getReferrer()

        :returns:    检测到的引用网站或空字符串
        :rtype:    string

        如果 User Agent 来自其他网站的推荐,返回推荐网站。通常会像这样测试:

        .. literalinclude:: user_agent/005.php

    .. php:method:: getAgentString()

        :returns:    完整的 User Agent 字符串或空字符串
        :rtype:    string

        返回包含完整 User Agent 字符串的字符串。通常看起来像这样::

            Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.0.4) Gecko/20060613 Camino/1.0.2

    .. php:method:: parse($string)

        :param    string    $string: 自定义 User Agent 字符串
        :rtype:    void

        解析自定义 User Agent 字符串,不同于当前访问者报告的字符串。
