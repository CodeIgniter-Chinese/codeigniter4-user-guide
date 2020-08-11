#############
数字辅助函数
#############

在本地化识别风格里数字辅助函数文件包含的函数帮助你与数字化的数据工作。

.. contents::
  :local:

.. raw:: html

  <div class="custom-index container"></div>

加载数字辅助函数
===================

数字辅助函数使用下面的代码加载::

	helper('number');

当某些事情出岔子
====================

如果 PHP 的国际化和本地化不能分给被提供的值，由于赋予了区域和选项，那么 ``BadFunctionCallException()`` 函数将会被掷出。


通用函数
===================

下面的函数是通用的:

.. php:function:: number_to_size($num[, $precision = 1[, $locale = null])

    :param	mixed	$num: 字节的数目
    :param	int	$precision: 浮点精确度
    :returns:	格式化数据大小 string, 要不然如果提供的值不是数字的则是错误的
    :rtype:	string

    像字节一样格式化数字,以大小为基础，并添加适事例当的词尾。事例::

        echo number_to_size(456); // 返回 456 Bytes
        echo number_to_size(4567); // 返回 4.5 KB
        echo number_to_size(45678); // 返回 44.6 KB
        echo number_to_size(456789); // 返回 447.8 KB
        echo number_to_size(3456789); // 返回 3.3 MB
        echo number_to_size(12345678912345); // 返回 1.8 GB
        echo number_to_size(123456789123456789); // 返回 11,228.3 TB

    第二个可选的参数允许你设置结果的精确度::

	    echo number_to_size(45678, 2); // 返回 44.61 KB

    第三个可选的参数当产生数字时应该常被使用，并能对格式化产生作用，它允许你去具体指定区域。
    如果没有区域被具体指定，请求将会被解析并且适当区域会减少头文件或者本地应用默认程序::

        // 产生 11.2 TB
        echo number_to_size(12345678912345, 1, 'en_US');
        // 产生 11,2 TB
        echo number_to_size(12345678912345, 1, 'fr_FR');

    .. note:: 由本段函数产生文本在接下来的语言文件中被找到: *language/<your_lang>/Number.php*

.. php:function:: number_to_amount($num[, $precision = 1[, $locale = null])

    :param	mixed	$num: 数字格式 
    :param	int	$precision: 浮点精确度
    :param  string $locale: 为了格式化区域使用
    :returns:	string 的可读版本， 要不然如果提供的值不是数字的为错误的
    :rtype:	string

    为了计数能达到百万的四次方，转换数字格式为人类可读版本，像 **123.4 trillion**. 事例::

        echo number_to_amount(123456); // 返回 123 thousand
        echo number_to_amount(123456789); // 返回 123 million
        echo number_to_amount(1234567890123, 2); // 返回 1.23 trillion
        echo number_to_amount('123,456,789,012', 2); // 返回 123.46 billion

    一个可选择的第二参数允许你去设置结果的精确度::

        echo number_to_amount(45678, 2); // 返回 45.68 thousand

    一个可选择的第三参数允许区域被具体指定::

        echo number_to_amount('123,456,789,012', 2, 'de_DE'); // 返回 123,46 billion

.. php:function:: number_to_currency($num, $currency[, $locale = null])

    :param mixed $num: 数字格式
    :param string $currency: 货币类型, 例如 USD, EUR, 等等
    :param string $locale: 为了格式化区域使用
    :param integer $fraction: Number of fraction digits after decimal point
    :returns: 为了本地化数字应与货币相称
    :rtype: string

    在公用的通货格式里转换数字, 例如 USD, EUR, GBP, 等等::

        echo number_to_currency(1234.56, 'USD');  // 返回 $1,234.56
        echo number_to_currency(1234.56, 'EUR');  // 返回 £1,234.56
        echo number_to_currency(1234.56, 'GBP');  // 返回 £1,234.56
        echo number_to_currency(1234.56, 'YEN');  // 返回 YEN1,234.56

.. php:function:: number_to_roman($num)

    :param string $num: 想要转换的数字
    :returns: 来自赋予参数的被转换的 roman 数字
    :rtype: string

    转换数字为 roman::

        echo number_to_roman(23);  // 返回 XXIII
        echo number_to_roman(324);  // 返回 CCCXXIV
        echo number_to_roman(2534);  // 返回 MMDXXXIV

    函数仅处理 1 到 3999 之间的数字。
    超出范围的任何值它将返回空。
