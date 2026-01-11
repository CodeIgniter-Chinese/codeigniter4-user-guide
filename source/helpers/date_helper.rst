############
日期辅助函数
############

日期辅助函数文件包含协助处理日期的函数。

.. contents::
    :local:
    :depth: 2

.. note:: 许多之前在 CodeIgniter 3 ``date_helper`` 中的函数已经移动到 CodeIgniter 4 的 :doc:`Time <../libraries/time>` 类中。

加载此辅助函数
===================

使用以下代码加载此辅助函数：

.. literalinclude:: date_helper/001.php

可用函数
===================

提供以下函数：

.. php:function:: now([$timezone = null])

    :param    string    $timezone: 时区
    :returns:    UNIX 时间戳
    :rtype:    int

    .. note:: 推荐改为使用 :doc:`Time <../libraries/time>` 类。使用 ``Time::now()->getTimestamp()`` 获取当前 UNIX 时间戳。

    如果没有提供时区，将通过 ``time()`` 返回当前 UNIX 时间戳。

    .. literalinclude:: date_helper/002.php

    如果提供了任何 PHP 支持的时区，它将返回一个根据时差偏移后的时间戳。这与当前的（标准）UNIX 时间戳不同。

    如果你不打算将主时间基准设置为其他 PHP 支持的时区（通常只有在运行允许用户自定义时区的网站时才会这样做），那么使用此函数相比 PHP 原生的 ``time()`` 函数并没有任何优势。

.. php:function:: timezone_select([$class = '', $default = '', $what = \DateTimeZone::ALL, $country = null])

    :param    string    $class: 应用于选择字段的可选类
    :param    string    $default: 初始选择的默认值
    :param    int    $what: DateTimeZone 类常量（参见 `listIdentifiers <https://www.php.net/manual/zh/datetimezone.listidentifiers.php>`_）
    :param    string    $country: 两位字母的 ISO 3166-1 兼容的国家代码（参见 `listIdentifiers <https://www.php.net/manual/zh/datetimezone.listidentifiers.php>`_）
    :returns:    预格式化的 HTML 选择字段
    :rtype:    string

    生成一个包含可用时区的 `select` 表单字段（即下拉菜单，可根据 ``$what`` 和 ``$country`` 参数进行筛选）。
    你可以提供一个 CSS 类应用到该字段以简化样式设置，同时也可以指定一个默认选中值。

    .. literalinclude:: date_helper/003.php
