########################
生成查询结果
########################

有几种生成查询结果的方法:

.. contents::
    :local:
    :depth: 3

*************
结果数组
*************

getResult()
===========

此方法将查询结果作为 **对象** 的数组返回,如果失败则返回 **空数组**。

获取 stdClass 的数组
----------------------------

通常你会在 foreach 循环中使用它,如下所示:

.. literalinclude:: results/001.php

上面的方法是 :php:meth:`CodeIgniter\\Database\\BaseResult::getResultObject()` 的别名。

获取数组的数组
-------------------------

如果希望以数组的数组形式获取结果,可以在第一个参数中传递 'array' 字符串:

.. literalinclude:: results/002.php

上面的用法是 `getResultArray()`_ 的别名。

获取自定义对象的数组
---------------------------------

你也可以将表示要为每个结果对象实例化的类的字符串传递给 ``getResult()``

.. literalinclude:: results/003.php

上面的方法是 `getCustomResultObject()`_ 的别名。

getResultArray()
================

此方法将查询结果作为纯数组返回,如果没有生成结果,则返回空数组。
通常你会在 foreach 循环中使用它,如下所示:

.. literalinclude:: results/004.php

***********
结果集
***********

getRow()
========

此方法返回单个结果集。如果查询有多个行,则只返回第一行。
结果作为 **对象** 返回。这里有个使用示例:

.. literalinclude:: results/005.php

如果要返回特定的行,可以在第一个参数中提交行号作为数字:

.. literalinclude:: results/006.php

你还可以添加第二个字符串参数,该参数是要使用的类的名称:

.. literalinclude:: results/007.php

getRowArray()
=============

与上面的 ``getRow()`` 方法相同,只是它返回数组。
例如:

.. literalinclude:: results/008.php

如果要返回特定的行,可以在第一个参数中提交行号作为数字:

.. literalinclude:: results/009.php

此外,你可以通过这些变体在结果中向前/向后/第一行/最后一行移动:

    | ``$row = $query->getFirstRow()``
    | ``$row = $query->getLastRow()``
    | ``$row = $query->getNextRow()``
    | ``$row = $query->getPreviousRow()``

默认情况下,除非在参数中放入 "array" 字样,否则它们返回对象:

    | ``$row = $query->getFirstRow('array')``
    | ``$row = $query->getLastRow('array')``
    | ``$row = $query->getNextRow('array')``
    | ``$row = $query->getPreviousRow('array')``

.. note:: 上面的所有方法都会将整个结果集加载到内存中(预取)。对于处理大型结果集,请使用 ``getUnbufferedRow()``。

getUnbufferedRow()
==================

此方法返回单个结果集,而不像 ``getRow()`` 那样在内存中预取全部结果。
如果查询有多个行,它会返回当前行并将内部数据指针向前移动。

.. literalinclude:: results/010.php

对于使用 MySQLi,你可以将 MySQLi 的结果模式设置为 ``MYSQLI_USE_RESULT``,以节省最大内存。
使用这种方式通常不推荐,但在某些情况下可能是有益的,例如将大型查询写入 csv。
如果更改结果模式,请注意与之相关的权衡。

.. literalinclude:: results/011.php

.. note:: 在使用 ``MYSQLI_USE_RESULT`` 时,在所有记录被提取或进行 ``freeResult()`` 调用之前,
    对同一连接的后续所有调用都将导致错误。``getNumRows()`` 方法将仅基于数据指针的当前位置返回行数。
    MyISAM 表将保持锁定,直到提取了所有记录或进行了 ``freeResult()`` 调用。

你可以选择传递 'object'(默认)或 'array' 以指定返回值的类型:

.. literalinclude:: results/012.php

*********************
自定义结果对象
*********************

你可以让结果作为 ``stdClass`` 或数组的自定义类的实例返回,正如 ``getResult()`` 和 ``getResultArray()`` 方法允许的那样。
如果类还未加载到内存中,则会自动加载。该对象将具有从数据库设置为属性的所有返回值。
如果这些已声明且非公共,则应提供 ``__set()`` 方法以允许设置它们。

例子:

.. literalinclude:: results/013.php

除了下面列出的两种方法外,以下方法也可以使用类名称将结果返回为:``getFirstRow()``、``getLastRow()``、
``getNextRow()`` 和 ``getPreviousRow()``。

getCustomResultObject()
=======================

将整个结果集作为请求类的实例数组返回。唯一的参数是要实例化的类的名称。

例子:

.. literalinclude:: results/014.php

getCustomRowObject()
====================

从查询结果中返回单行。第一个参数是结果的行号。第二个参数是要实例化的类名称。

例子:

.. literalinclude:: results/015.php

你也可以以完全相同的方式使用 ``getRow()`` 方法。

例子:

.. literalinclude:: results/016.php

*********************
结果辅助方法
*********************

getFieldCount()
===============

查询返回的字段(列)数。请确保使用查询结果对象调用该方法:

.. literalinclude:: results/017.php

getFieldNames()
===============

以数组形式返回查询返回的字段(列)的名称。
请确保使用查询结果对象调用该方法:

.. literalinclude:: results/018.php

getNumRows()
============

查询返回的记录数。请确保使用查询结果对象调用该方法:

.. literalinclude:: results/019.php

.. note:: 因为 SQLite3 缺乏有效的返回记录数的方法,
    CodeIgniter 将在内部提取和缓冲查询结果记录,并返回生成的记录数组的计数,这可能效率低下。

freeResult()
============

它释放与结果相关的内存并删除结果资源 ID。通常 PHP 会在脚本执行结束时自动释放其内存。
但是,如果在特定脚本中运行了大量查询,你可能希望在生成每个查询结果后释放结果,以减少内存消耗。

例子:

.. literalinclude:: results/020.php

dataSeek()
==========

此方法将下一个要提取的结果集的内部指针设置为。它仅与 ``getUnbufferedRow()`` 结合使用时才有用。

它接受一个正整数值,默认为 0 并在成功时返回 true,失败时返回 false。

.. literalinclude:: results/021.php

.. note:: 并非所有数据库驱动程序都支持此功能并会返回 false。
    最明显的是 - 你将无法与 PDO 一起使用它。

***************
类参考
***************

.. php:namespace:: CodeIgniter\Database

.. php:class:: BaseResult

    .. php:method:: getResult([$type = 'object'])

        :param    string    $type: 请求结果的类型 - array、object 或类名
        :returns:    包含提取行的数组
        :rtype:    array

        ``getResultArray()``、``getResultObject()`` 和 ``getCustomResultObject()`` 方法的包装器。

        用法:参见 `结果数组`_ 。

    .. php:method:: getResultArray()

        :returns:    包含提取行的数组
        :rtype:    array

        将查询结果作为行数组返回,其中每行本身是一个关联数组。

        用法:参见 `结果数组`_ 。

    .. php:method:: getResultObject()

        :returns:    包含提取行的数组
        :rtype:    array

        将查询结果作为行数组返回,其中每行是一个 ``stdClass`` 类型的对象。

        用法:参见 `获取 stdClass 的数组`_ 。

    .. php:method:: getCustomResultObject($class_name)

        :param    string    $class_name: 结果集的类名
        :returns:    包含提取行的数组
        :rtype:    array

        将查询结果作为行数组返回,其中每行是指定类的实例。

    .. php:method:: getRow([$n = 0[, $type = 'object']])

        :param    int    $n: 要返回的查询结果集的索引
        :param    string    $type: 请求结果的类型 - array、object 或类名
        :returns:    请求的行或不存在则为 null
        :rtype:    mixed

        ``getRowArray()``、``getRowObject()`` 和 ``getCustomRowObject()`` 方法的包装器。

        用法:参见 `结果集`_ 。

    .. php:method:: getUnbufferedRow([$type = 'object'])

        :param    string    $type: 请求结果的类型 - array、object 或类名
        :returns:    结果集的下一行或不存在则为 null
        :rtype:    mixed

        获取下一行结果并以请求的形式返回。

        用法:参见 `结果集`_ 。

    .. php:method:: getRowArray([$n = 0])

        :param    int    $n: 要返回的查询结果集的索引
        :returns:    请求的行或不存在则为 null
        :rtype:    array

        将请求的结果集作为关联数组返回。

        用法:参见 `结果集`_ 。

    .. php:method:: getRowObject([$n = 0])

        :param    int    $n: 要返回的查询结果集的索引
        :returns:    请求的行或不存在则为 null
        :rtype:    stdClass

        将请求的结果集作为 ``stdClass`` 类型的对象返回。

        用法:参见 `结果集`_ 。

    .. php:method:: getCustomRowObject($n, $type)

        :param    int    $n: 要返回的结果集的索引
        :param    string    $class_name: 结果集的类名
        :returns:    请求的行或不存在则为 null
        :rtype:    $type

        将请求的结果集作为请求类的实例返回。

    .. php:method:: dataSeek([$n = 0])

        :param    int    $n: 下一个要返回的结果集的索引
        :returns:    成功则为 true,失败则为 false
        :rtype:    bool

        将内部结果集指针移动到所需的偏移量。

        用法:参见 `结果辅助方法`_。

    .. php:method:: setRow($key[, $value = null])

        :param    mixed    $key: 列名称或键/值对的数组
        :param    mixed    $value: 如果 $key 是单个字段名,则分配给该列的值
        :rtype:    void

        为特定列赋值。

    .. php:method:: getNextRow([$type = 'object'])

        :param    string    $type: 请求结果的类型 - array、object 或类名
        :returns:    结果集的下一行,不存在则为 null
        :rtype:    mixed

        从结果集返回下一行。

    .. php:method:: getPreviousRow([$type = 'object'])

        :param    string    $type: 请求结果的类型 - array、object 或类名
        :returns:  结果集的上一行,不存在则为 null
        :rtype:    mixed

        从结果集返回上一行。

    .. php:method:: getFirstRow([$type = 'object'])

        :param    string    $type: 请求结果的类型 - array、object 或类名
        :returns:    结果集的第一行,不存在则为 null
        :rtype:    mixed

        从结果集返回第一行。

    .. php:method:: getLastRow([$type = 'object'])

        :param    string    $type: 请求结果的类型 - array、object 或类名
        :returns:    结果集的最后一行,不存在则为 null
        :rtype:    mixed

        从结果集返回最后一行。

    .. php:method:: getFieldCount()

        :returns:    结果集中的字段数
        :rtype:    int

        返回结果集中的字段数。

        用法:参见 `结果辅助方法`_。

    .. php:method:: getFieldNames()

        :returns:    列名称数组
        :rtype:    array

        返回结果集中包含的字段名称数组。

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

        用法:参见 `结果辅助方法`_。
