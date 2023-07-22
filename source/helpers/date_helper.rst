##############
Date 辅助函数
##############

Date 辅助函数文件包含了帮助处理日期的函数。

.. contents::
    :local:
    :depth: 2

.. note:: 许多之前在 CodeIgniter 3 ``date_helper`` 中找到的函数已移到 CodeIgniter 4 的 :doc:`Time <../libraries/time>` 类中。

加载此辅助函数
===================

使用以下代码加载此辅助函数:

.. literalinclude:: date_helper/001.php

可用函数
===================

以下函数可用:

.. php:function:: now([$timezone = null])

    :param    string    $timezone: 时区
    :returns:    UNIX 时间戳
    :rtype:    int

    .. note:: 建议使用 :doc:`Time <../libraries/time>` 类。使用 ``Time::now()->getTimestamp()`` 来获取当前的 UNIX 时间戳。

    如果未提供时区,它将通过 ``time()`` 返回当前的 UNIX 时间戳。

    .. literalinclude:: date_helper/002.php

    如果提供任何 PHP 支持的时区,它将返回一个由时差偏移的时间戳。它与当前的 UNIX 时间戳不同。

    如果你不打算将主时间参考设置为任何其他 PHP 支持的时区(如果你运行一个允许每个用户设置自己的时区设置的站点,通常会这样做),那么使用这个函数不会比 PHP 的 ``time()`` 函数有更多的好处。

.. php:function:: timezone_select([$class = '', $default = '', $what = \DateTimeZone::ALL, $country = null])

    :param    string    $class: 可选的要应用于选择字段的类
    :param    string    $default: 初始选择的默认值
    :param    int    $what: DateTimeZone 类常量(参见 `listIdentifiers <https://www.php.net/manual/en/datetimezone.listidentifiers.php>`_)
    :param    string    $country: 一个与 ISO 3166-1 兼容的两字母国家代码(参见 `listIdentifiers <https://www.php.net/manual/en/datetimezone.listidentifiers.php>`_)
    :returns:    预格式化的 HTML 选择字段
    :rtype:    string

    生成可用时区的 `select` 表单字段(可选择通过 ``$what`` 和 ``$country`` 过滤)。
    你可以提供一个选项 class 以方便格式化应用于字段,以及一个默认选择值。

    .. literalinclude:: date_helper/003.php
