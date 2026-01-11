########################
生成查询结果
########################

生成查询结果的方式有多种：

.. contents::
    :local:
    :depth: 3

*************
结果数组
*************

.. _getresult:

getResult()
===========

此方法将查询结果以 **对象数组** 形式返回，失败时则返回 **空数组**。

获取 stdClass 数组
----------------------------

通常你会在 foreach 循环中使用它，如下所示：

.. literalinclude:: results/001.php

上述方法是 :php:meth:`CodeIgniter\\Database\\BaseResult::getResultObject()` 的别名。

获取数组的数组
-------------------------

如果希望结果以数组的数组形式返回，可以传入字符串 'array'：

.. literalinclude:: results/002.php

上述用法是 `getResultArray()`_ 的别名。

获取自定义对象数组
--------------------

也可以向 ``getResult()`` 传递一个字符串，表示为每个结果对象实例化的类名

.. literalinclude:: results/003.php

上述方法是 `getCustomResultObject()`_ 的别名。

getResultArray()
================

此方法将查询结果作为纯数组返回，如果没有产生结果则返回空数组。通常你会在 foreach 循环中使用它，如下所示：

.. literalinclude:: results/004.php

***********
结果集
***********

getRow()
========

此方法返回单个结果集。如果查询有多行，它只返回第一行。结果以**对象**形式返回。用法示例：

.. literalinclude:: results/005.php

如果需要返回特定行，可以在第一个参数中提交行号（数字）：

.. literalinclude:: results/006.php

还可以添加第二个字符串参数，指定用于实例化行的类名：

.. literalinclude:: results/007.php

getRowArray()
=============

与上面的 ``row()`` 方法相同，只是它返回数组。示例：

.. literalinclude:: results/008.php

如果需要返回特定行，可以在第一个参数中提交行号（数字）：

.. literalinclude:: results/009.php

此外，可以使用以下变体在结果中前进/后退/定位到第一行/最后一行：

    | ``$row = $query->getFirstRow()``
    | ``$row = $query->getLastRow()``
    | ``$row = $query->getNextRow()``
    | ``$row = $query->getPreviousRow()``

默认情况下它们返回对象，除非在参数中放入 "array" 单词：

    | ``$row = $query->getFirstRow('array')``
    | ``$row = $query->getLastRow('array')``
    | ``$row = $query->getNextRow('array')``
    | ``$row = $query->getPreviousRow('array')``

.. note:: 上述所有方法都会将整个结果加载到内存中（预取）。处理大型结果集时使用 ``getUnbufferedRow()``。

getUnbufferedRow()
==================

此方法返回单个结果集，不像 ``row()`` 那样将整个结果预取到内存中。如果查询有多行，它会返回当前行并将内部数据指针向前移动。

.. literalinclude:: results/010.php

对于 MySQLi，可以将 MySQLi 的结果模式设置为 ``MYSQLI_USE_RESULT`` 以最大化内存节省。一般不推荐使用此设置，但在某些情况下（如将大型查询写入 CSV）可能有益。更改结果模式时请注意相关的权衡。

.. literalinclude:: results/011.php

.. note:: 使用 ``MYSQLI_USE_RESULT`` 时，在获取所有记录或调用 ``freeResult()`` 之前，对同一连接的所有后续调用都会导致错误。``getNumRows()`` 方法只会根据数据指针的当前位置返回行数。MyISAM 表将保持锁定状态，直到获取所有记录或调用 ``freeResult()``。

可以选择性地传递 'object'（默认）或 'array' 来指定返回值的类型：

.. literalinclude:: results/012.php

*********************
自定义结果对象
*********************

可以让结果返回为自定义类的实例，而不是 ``stdClass`` 或数组，就像 ``getResult()`` 和 ``getResultArray()`` 方法允许的那样。如果类尚未加载到内存中，自动加载器将尝试加载它。对象将把数据库返回的所有值设置为属性。如果这些属性已声明且是非公共的，则应提供 ``__set()`` 方法以允许设置它们。

示例：

.. literalinclude:: results/013.php

除了下面列出的两个方法外，以下方法也可以接受类名以返回结果：``getFirstRow()``、``getLastRow()``、``getNextRow()`` 和 ``getPreviousRow()``。

getCustomResultObject()
=======================

将整个结果集返回为请求的类实例的数组。唯一的参数是要实例化的类名。

示例：

.. literalinclude:: results/014.php

getCustomRowObject()
====================

从查询结果中返回单行。第一个参数是结果的行号。第二个参数是要实例化的类名。

示例：

.. literalinclude:: results/015.php

也可以以完全相同的方式使用 ``getRow()`` 方法。

示例：

.. literalinclude:: results/016.php

*********************
结果辅助方法
*********************

getFieldCount()
===============

查询返回的字段（列）数量。确保使用查询结果对象调用此方法：

.. literalinclude:: results/017.php

getFieldNames()
===============

返回包含查询返回的字段（列）名称的数组。确保使用查询结果对象调用此方法：

.. literalinclude:: results/018.php

getNumRows()
============

查询返回的记录数。确保使用查询结果对象调用此方法：

.. literalinclude:: results/019.php

.. note:: 由于 SQLite3 缺乏高效的返回记录计数的方法，CodeIgniter 会在内部获取并缓冲查询结果记录，然后返回结果记录数组的计数，这可能效率不高。

freeResult()
============

释放与结果关联的内存并删除结果资源 ID。通常 PHP 会在脚本执行结束时自动释放内存。但是，如果在特定脚本中运行大量查询，可能希望在生成每个查询结果后释放结果，以减少内存消耗。

示例：

.. literalinclude:: results/020.php

dataSeek()
==========

此方法设置下一个要获取的结果集的内部指针。它仅在与 ``getUnbufferedRow()`` 结合使用时有用。

它接受一个正整数值（默认为 0），成功时返回 true，失败时返回 false。

.. literalinclude:: results/021.php

.. note:: 并非所有数据库驱动程序都支持此功能，不支持的驱动程序将返回 false。最明显的是，无法在 PDO 中使用此功能。

***************
类参考
***************

.. php:namespace:: CodeIgniter\Database

.. php:class:: BaseResult

    .. php:method:: getResult([$type = 'object'])

        :param    string    $type: 请求的结果类型 - array、object 或类名
        :returns:    包含获取行的数组
        :rtype:    array

        ``getResultArray()``、``getResultObject()`` 和 ``getCustomResultObject()`` 方法的包装器。

        用法：参见 `结果数组`_。

    .. php:method:: getResultArray()

        :returns:    包含获取行的数组
        :rtype:    array

        将查询结果返回为行的数组，其中每行本身是一个关联数组。

        用法：参见 `结果数组`_。

    .. php:method:: getResultObject()

        :returns:    包含获取行的数组
        :rtype:    array

        将查询结果返回为行的数组，其中每行是 ``stdClass`` 类型的对象。

        用法：参见 `获取 stdClass 数组`_。

    .. php:method:: getCustomResultObject($className)

        :param    string    $className: 结果集的类名
        :returns:    包含获取行的数组
        :rtype:    array

        将查询结果返回为行的数组，其中每行是指定类的实例。

    .. php:method:: getRow([$n = 0[, $type = 'object']])

        :param    int    $n: 要返回的查询结果集索引
        :param    string    $type: 请求的结果类型 - array、object 或类名
        :returns:    请求的行，如果不存在则为 null
        :rtype:    mixed

        ``getRowArray()``、``getRowObject()`` 和 ``getCustomRowObject()`` 方法的包装器。

        用法：参见 `结果集`_。

    .. php:method:: getUnbufferedRow([$type = 'object'])

        :param    string    $type: 请求的结果类型 - array、object 或类名
        :returns:    结果集中的下一行，如果不存在则为 null
        :rtype:    mixed

        获取下一个结果集并以请求的形式返回。

        用法：参见 `结果集`_。

    .. php:method:: getRowArray([$n = 0])

        :param    int    $n: 要返回的查询结果集索引
        :returns:    请求的行，如果不存在则为 null
        :rtype:    array

        将请求的结果集返回为关联数组。

        用法：参见 `结果集`_。

    .. php:method:: getRowObject([$n = 0])

        :param    int    $n: 要返回的查询结果集索引
                :returns:    请求的行，如果不存在则为 null
        :rtype:    stdClass

        将请求的结果集返回为 ``stdClass`` 类型的对象。

        用法：参见 `结果集`_。

    .. php:method:: getCustomRowObject($n, $type)

        :param    int    $n: 要返回的结果集索引
        :param    string    $class_name: 结果集的类名
        :returns:    请求的行，如果不存在则为 null
        :rtype:    $type

        将请求的结果集返回为请求类的实例。

    .. php:method:: dataSeek([$n = 0])

        :param    int    $n: 下一个要返回的结果集索引
        :returns:    成功时为 true，失败时为 false
        :rtype:    bool

        将内部结果集指针移动到所需的偏移量。

        用法：参见 `结果辅助方法`_。

    .. php:method:: setRow($key[, $value = null])

        :param    mixed    $key: 列名或键/值对数组
        :param    mixed    $value: 分配给列的值，当 $key 是单个字段名时
        :rtype:    void

        为特定列分配值。

    .. php:method:: getNextRow([$type = 'object'])

        :param    string    $type: 请求的结果类型 - array、object 或类名
        :returns:    结果集的下一行，如果不存在则为 null
        :rtype:    mixed

        返回结果集中的下一行。

    .. php:method:: getPreviousRow([$type = 'object'])

        :param    string    $type: 请求的结果类型 - array、object 或类名
        :returns:    结果集的上一行，如果不存在则为 null
        :rtype:    mixed

        返回结果集中的上一行。

    .. php:method:: getFirstRow([$type = 'object'])

        :param    string    $type: 请求的结果类型 - array、object 或类名
        :returns:    结果集的第一行，如果不存在则为 null
        :rtype:    mixed

        返回结果集中的第一行。

    .. php:method:: getLastRow([$type = 'object'])

        :param    string    $type: 请求的结果类型 - array、object 或类名
        :returns:    结果集的最后一行，如果不存在则为 null
        :rtype:    mixed

        返回结果集中的最后一行。

    .. php:method:: getFieldCount()

        :returns:    结果集中的字段数
        :rtype:    int

        返回结果集中的字段数。

        用法：参见 `结果辅助方法`_。

    .. php:method:: getFieldNames()

        :returns:    列名数组
        :rtype:    array

        返回包含结果集中字段名的数组。

    .. php:method:: getFieldData()

        :returns:    包含字段元数据的数组
        :rtype:    array

        生成包含字段元数据的 ``stdClass`` 对象数组。

    .. php:method:: getNumRows()

        :returns:    结果集中的行数
        :rtype:    int

        返回查询返回的行数

    .. php:method:: freeResult()

        :rtype:    void

        释放结果集。

        用法：参见 `结果辅助方法`_。
