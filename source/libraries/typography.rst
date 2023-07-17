##########
排版
##########

排版库包含了一些帮助你以语义化方式格式化文本的方法。

.. contents::
    :local:
    :depth: 2

*******************
加载库
*******************

和 CodeIgniter 中的其他服务一样,可以通过 ``Config\Services`` 来加载,不过通常你不需要手动加载:

.. literalinclude:: typography/001.php

**************************
可用的静态方法
**************************

以下方法可用:

.. php:function:: autoTypography($str[, $reduce_linebreaks = false])

    :param    string    $str: 输入字符串
    :param    bool    $reduce_linebreaks: 是否把多个连续的空行减少到两个
    :returns:    HTML 格式的适合排版的字符串
    :rtype: string

    格式化文本,使其在语义和排版上是正确的 HTML。

    使用示例:

    .. literalinclude:: typography/002.php

    .. note:: 排版格式化可能需要大量处理,特别是你有很多需要格式化的内容。如果你选择使用这个方法,你可能需要考虑 :doc:`caching <../general/caching>` 你的页面。

.. php:function:: formatCharacters($str)

    :param    string    $str: 输入字符串
    :returns:    格式化后的字符串
    :rtype:    string

    这个方法主要将双引号和单引号转换为花括号实体,也会转换破折号、双空格和和号。

    使用示例:

    .. literalinclude:: typography/003.php

.. php:function:: nl2brExceptPre($str)

    :param    string    $str: 输入字符串
    :returns:    包含 HTML 格式换行的字符串
    :rtype:    string

    在 ``<pre>`` 标签外把换行转换为 ``<br />`` 标签。这个方法和原生 PHP 的 ``nl2br()`` 函数相同,只是忽略了 ``<pre>`` 标签。

    使用示例:

    .. literalinclude:: typography/004.php
