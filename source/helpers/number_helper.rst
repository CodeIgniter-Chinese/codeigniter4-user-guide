#############
数字辅助函数
#############

数字辅助函数文件包含了帮助你以与区域设置相关的方式处理数字数据的函数。

.. contents::
    :local:
    :depth: 2

加载此辅助函数
===================

使用以下代码加载此辅助函数:

.. literalinclude:: number_helper/001.php

当事情出错时
====================

如果 PHP 的国际化和本地化逻辑无法使用给定的区域设置和选项处理所提供的值,则会抛出 ``BadFunctionCallException()``。

可用函数
===================

以下函数可用:

.. php:function:: number_to_size($num[, $precision = 1[, $locale = null]])

    :param      mixed     $num: 字节数
    :param      int       $precision: 浮点精度
    :returns:   格式化的数据大小字符串,如果提供的值不是数字则返回 false
    :rtype:     string

    根据大小格式化数字,并添加适当的后缀。示例:

    .. literalinclude:: number_helper/002.php

    可选的第二个参数允许你设置结果的精度:

    .. literalinclude:: number_helper/003.php

    可选的第三个参数允许你指定在生成数字时应使用的区域设置,这可能会影响格式设置。如果未指定区域设置,则将分析请求并从标头或应用程序默认值中获取适当的区域设置:

    .. literalinclude:: number_helper/004.php

    .. note:: 此函数生成的文本位于以下语言文件中:*language/<your_lang>/Number.php*

.. php:function:: number_to_amount($num[, $precision = 1[, $locale = null])

    :param      mixed     $num: 要格式化的数字
    :param      int       $precision: 浮点精度
    :param      string    $locale: 用于格式化的区域设置
    :returns:   字符串的人类可读版本,如果提供的值不是数字则返回 false
    :rtype:     string

    将数字转换为人类可读版本,如 **123.4 万亿** 用于高达四次方的数字。示例:

    .. literalinclude:: number_helper/005.php

    可选的第二个参数允许你设置结果的精度:

    .. literalinclude:: number_helper/006.php

    可选的第三个参数允许指定区域设置:

    .. literalinclude:: number_helper/007.php

.. php:function:: number_to_currency($num, $currency[, $locale = null[, $fraction = 0]])

    :param float $num: 要格式化的数字
    :param string $currency: 货币类型,即 USD、EUR 等
    :param string|null $locale: 用于格式化的区域设置
    :param integer $fraction: 小数点后小数位数
    :returns: 适用于该区域设置的货币格式的数字
    :rtype: string

    将数字转换为常见的货币格式,如 USD、EUR、GBP 等:

    .. literalinclude:: number_helper/008.php

    如果你不指定区域设置,将使用请求区域设置。

.. php:function:: number_to_roman($num)

    :param string $num: 要转换的数字
    :returns: 从给定参数转换后的罗马数字
    :rtype: string|null

    将数字转换为罗马数字:

    .. literalinclude:: number_helper/009.php

    此函数仅处理 1 到 3999 范围内的数字。对于该范围之外的任何值,它都将返回 null。
