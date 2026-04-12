#############
Typography 类
#############

Typography 类包含多种辅助方法，用于将文本格式化为符合语义规范的形式。

.. contents::
    :local:
    :depth: 2

*******************
加载类
*******************

与 CodeIgniter 的所有服务一样，Typography 类可通过 ``Config\Services`` 加载，不过通常无需手动操作：

.. literalinclude:: typography/001.php

**************************
可用静态方法
**************************

以下方法均可直接使用：

.. php:function:: autoTypography($str[, $reduceLinebreaks = false])

    :param    string    $str: 输入字符串
    :param    bool    $reduceLinebreaks: 是否将连续出现的多个双换行符缩减为两个
    :returns:    格式化后的 HTML 字符串
    :rtype: string

    将文本格式化为语义准确且排版规范的 HTML。

    使用示例：

    .. literalinclude:: typography/002.php

    .. note:: 排版格式化操作较为耗费性能，尤其在处理大量内容时。若决定使用此函数，建议考虑对页面进行 :doc:`缓存 <../general/caching>`。

.. php:function:: formatCharacters($str)

    :param    string    $str: 输入字符串
    :returns:    格式化后的字符串
    :rtype:    string

    主要用于将双引号和单引号转换为弯引号（curly entities），同时也会转换破折号（em-dashes）、双空格以及和号（ampersands）。

    使用示例：

    .. literalinclude:: typography/003.php

.. php:function:: nl2brExceptPre($str)

    :param    string    $str: 输入字符串
    :returns:    包含 HTML 换行标签的字符串
    :rtype:    string

    将换行符转换为 ``<br />`` 标签，但会忽略 ``<pre>`` 标签内的换行。此函数逻辑与 PHP 原生函数 ``nl2br()`` 基本一致，唯一的区别是排除了 ``<pre>`` 标签。

    使用示例：

    .. literalinclude:: typography/004.php
