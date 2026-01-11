#############
数字辅助函数
#############

数字辅助辅助函数文件包含了一些函数，用于根据区域设置来处理数值数据。

.. contents::
    :local:
    :depth: 2

加载此辅助函数
===================

使用以下代码加载此辅助函数：

.. literalinclude:: number_helper/001.php

出现错误时
====================

如果在指定的区域设置和选项下，PHP 的国际化与本地化逻辑无法处理传入的值，则会抛出 ``BadFunctionCallException()`` 异常。

可用函数
===================

提供以下函数：

.. php:function:: number_to_size($num[, $precision = 1[, $locale = null]])

    :param      mixed     $num: 字节数
    :param      int       $precision: 浮点精度
    :returns:   格式化后的数据大小字符串，如果提供的值不是数字则返回 false
    :rtype:     string

    根据大小将数字格式化为字节，并添加适当的后缀。示例：

    .. literalinclude:: number_helper/002.php

    可选的第二个参数允许你设置结果的精度：

    .. literalinclude:: number_helper/003.php

    可选的第三个参数允许你指定生成数字时应使用的区域设置，这可能影响格式化。如果未指定区域设置，将分析请求并从头部获取适当的区域设置，或使用应用程序默认值：

    .. literalinclude:: number_helper/004.php

    .. note:: 此函数生成的文本可在以下语言文件中找到：*language/<your_lang>/Number.php*

.. php:function:: number_to_amount($num[, $precision = 1[, $locale = null])

    :param      mixed     $num: 要格式化的数字
    :param      int       $precision: 浮点精度
    :param      string    $locale: 用于格式化的区域设置
    :returns:   人类可读的字符串版本，如果提供的值不是数字则返回 false
    :rtype:     string

    将数字转换为人类可读的版本，如对于高达千万亿级的数字显示为 **123.4 万亿**（最大支持千万亿级数字）。示例：

    .. literalinclude:: number_helper/005.php

    可选的第二个参数允许你设置结果的精度：

    .. literalinclude:: number_helper/006.php

    可选的第三个参数允许指定区域设置：

    .. literalinclude:: number_helper/007.php

.. php:function:: number_to_currency($num, $currency[, $locale = null[, $fraction = 0]])

    :param float $num: 要格式化的数字
    :param string $currency: 货币类型，如 USD、EUR 等
    :param string|null $locale: 用于格式化的区域设置
    :param integer $fraction: 小数点后的分数位数
    :returns: 适合该区域设置的货币格式的数字
    :rtype: string

    将数字转换为通用货币格式，如 USD、EUR、GBP 等：

    .. literalinclude:: number_helper/008.php

    如果不指定区域设置，将使用请求的区域设置。

.. php:function:: number_to_roman($num)

    :param int|string $num: 要转换的数字
    :returns: 从给定参数转换的罗马数字
    :rtype: string|null

    将数字转换为罗马数字：

    .. literalinclude:: number_helper/009.php

    此函数仅处理 1 到 3999 范围内的数字。
    对于超出该范围的任何值，它将返回 ``null``。
