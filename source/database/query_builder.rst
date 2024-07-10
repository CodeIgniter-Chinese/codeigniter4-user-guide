###################
查询构建器类
###################

CodeIgniter 为你提供了查询构建器类的访问。这种模式允许你使用最小的脚本就可以在数据库中检索、插入和更新信息。在某些情况下,只需要一行或两行代码就可以执行数据库操作。
CodeIgniter 不要求每个数据库表都有自己的类文件。它提供了一个更简化的接口。

除了简单性之外,使用查询构建器功能的一个主要好处是,它允许你创建数据库独立的应用程序,因为查询语法是由每个数据库适配器生成的。它也允许进行更安全的查询,因为系统会自动对值进行转义。

.. note:: CodeIgniter 不支持在表名和列名中使用点（``.``）。自 v4.5.0 起，支持带点的数据库名称。

.. contents::
    :local:
    :depth: 2

************************
SQL 注入保护
************************

你可以使用查询构建器相当安全地生成 SQL 语句。但是,它不旨在防止无论你传递什么数据都防止 SQL 注入。

传递给查询构建器的参数可以是:
    1. **标识符**,如字段(或表)名称
    2. 它们的 **值**
    3. **SQL 字符串** 的一部分

查询构建器默认会转义所有 **值**。

它还将尝试通过默认正确保护 **标识符** 和 **SQL 字符串** 中的标识符。
但是,它的实现是为了在许多使用案例中工作良好,而不是旨在防止所有攻击。
因此,在没有适当验证的情况下,永远不要向它们馈送用户输入。

此外,许多方法都有 ``$escape`` 参数,可以设置为禁用转义。
如果将 ``$escape`` 设置为 false,查询构建器不提供任何保护,
所以你必须确保在将其传递给查询构建器之前已经适当地对它们进行了转义或保护。
使用 ``RawSql`` 指定原始 SQL 语句时也是如此。

*************************
加载查询构建器
*************************

可以通过数据库连接上的 ``table()`` 方法加载查询构建器。这会为你设置查询的 **FROM** 部分,并返回查询构建器类的新实例:

.. literalinclude:: query_builder/001.php

只有在明确请求类时,才会将查询构建器加载到内存中,因此默认情况下不使用任何资源。

**************
选择数据
**************

以下方法允许你构建 SQL **SELECT** 语句。

Get
===

$builder->get()
---------------

运行选择查询并返回结果。可以自己使用以从表中检索所有记录:

.. literalinclude:: query_builder/002.php

第一个和第二个参数使你可以设置 limit 和 offset 子句:

.. literalinclude:: query_builder/003.php

你会注意到上面的方法被赋值给一个名为 $query 的变量,可用于显示结果:

.. literalinclude:: query_builder/004.php

有关结果生成的完整讨论,请访问 :ref:`getResult() <getresult>` 方法页面。

请访问 :ref:`getResult() <getresult>` 方法，以了解关于结果生成的完整讨论。

$builder->getCompiledSelect()
-----------------------------

编译选择查询,就像 ``$builder->get()`` 一样,但不运行查询。此方法简单地将 SQL 查询作为字符串返回。

例如:

.. literalinclude:: query_builder/005.php

下面第一个查询中的参数 (false) 允许你设置查询构建器是否会被重置（因为该参数的默认值为 true，即默认情况下 ``getCompiledSelect(bool $reset = true)`` 会像使用 ``$builder->get()`` 一样被重置）：

.. literalinclude:: query_builder/006.php

在上述示例中需要注意的关键点是，第二个查询并没有使用 ``limit(10, 20)``，但生成的 SQL 查询却包含 ``LIMIT 20, 10``。这种结果的原因是因为第一个查询中的参数被设置为 ``false``，因此 ``limit(10, 20)`` 在第二个查询中仍然有效。

$builder->getWhere()
--------------------

与 ``get()`` 方法相同,只是它允许你在第一个参数中添加 “where” 子句,而不是使用 ``$builder->where()`` 方法:

.. literalinclude:: query_builder/007.php

请阅读下面关于 ``where()`` 方法的更多信息。

.. _query-builder-select:

Select
======

$builder->select()
------------------

允许你编写查询的 **SELECT** 部分:

.. literalinclude:: query_builder/008.php

.. note:: 如果从表中选择所有 (``*``),则不需要使用此方法。如果省略,CodeIgniter 会假定你希望选择所有字段并自动添加 ``SELECT *``。

``$builder->select()`` 接受一个可选的第二个参数。如果将其设置为 ``false``,CodeIgniter 将不会尝试保护你的字段或表名。这在需要复合 select 语句的情况下很有用,其中自动转义字段可能会破坏它们。

.. literalinclude:: query_builder/009.php

.. _query-builder-select-rawsql:

RawSql
^^^^^^

.. versionadded:: 4.2.0

从 v4.2.0 开始, ``$builder->select()`` 接受一个 ``CodeIgniter\Database\RawSql`` 实例,它表示原始 SQL 字符串。

.. literalinclude:: query_builder/099.php

.. warning:: 当你使用 ``RawSql`` 时,必须手动对值和标识符进行转义。否则可能会导致 SQL 注入。

$builder->selectMax()
---------------------

为查询编写一个 **SELECT MAX(field)** 部分。你可以选择包括第二个参数以重命名结果字段。

.. literalinclude:: query_builder/010.php

$builder->selectMin()
---------------------

为查询编写一个 **SELECT MIN(field)** 部分。与 ``selectMax()`` 一样,你可以选择包括第二个参数以重命名结果字段。

.. literalinclude:: query_builder/011.php

$builder->selectAvg()
---------------------

为查询编写一个 **SELECT AVG(field)** 部分。与 ``selectMax()`` 一样,你可以选择包括第二个参数以重命名结果字段。

.. literalinclude:: query_builder/012.php

$builder->selectSum()
---------------------

为查询编写一个 **SELECT SUM(field)** 部分。与 ``selectMax()`` 一样,你可以选择包括第二个参数以重命名结果字段。

.. literalinclude:: query_builder/013.php

$builder->selectCount()
-----------------------

为查询编写一个 **SELECT COUNT(field)** 部分。与 ``selectMax()`` 一样,你可以选择包括第二个参数以重命名结果字段。

.. note:: 此方法与 ``groupBy()`` 一起使用时特别有用。有关计数结果的更多信息,请参阅 ``countAll()`` 或 ``countAllResults()``。

.. literalinclude:: query_builder/014.php

$builder->selectSubquery()
--------------------------

在 SELECT 部分添加子查询。

.. literalinclude:: query_builder/015.php
   :lines: 2-

From
====

$builder->from()
----------------

允许你编写查询的 **FROM** 部分:

.. literalinclude:: query_builder/016.php

.. note:: 如前所示,可以在 ``$db->table()`` 方法中指定 **FROM** 部分。对 from() 的额外调用将向 FROM 部分添加更多表。

.. _query-builder-from-subquery:

子查询
==========

$builder->fromSubquery()
------------------------

允许你将 **FROM** 查询的一部分编写为子查询。

这是我们将子查询添加到现有表的地方:

.. literalinclude:: query_builder/017.php

使用 ``$db->newQuery()`` 方法将子查询设置为主表:

.. literalinclude:: query_builder/018.php

Join
====

$builder->join()
----------------

允许你编写查询的 **JOIN** 部分:

.. literalinclude:: query_builder/019.php

如果需要在一个查询中进行多个连接,可以进行多次方法调用。

如果需要特定类型的 **JOIN**,可以通过方法的第三个参数指定。选项是:``left``、``right``、``outer``、``inner``、``left outer`` 和 ``right outer``。

.. literalinclude:: query_builder/020.php

.. _query-builder-join-rawsql:

RawSql
^^^^^^

.. versionadded:: 4.2.0

从 v4.2.0 开始, ``$builder->join()`` 接受一个 ``CodeIgniter\Database\RawSql`` 实例,它表示原始 SQL 字符串。

.. literalinclude:: query_builder/102.php

.. warning:: 当你使用 ``RawSql`` 时,必须手动对值和标识符进行转义。否则可能会导致 SQL 注入。

*************************
查找特定数据
*************************

Where
=====

$builder->where()
-----------------

此方法使用五种方法之一启用设置 **WHERE** 子句:

.. note:: 除了使用自定义字符串外,传递给此方法的所有值都会自动转义,生成更安全的查询。

.. note:: ``$builder->where()`` 接受一个可选的第三个参数。如果将其设置为 ``false``,CodeIgniter 将不会尝试保护你的字段或表名。

1. 简单的键/值方法
^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. literalinclude:: query_builder/021.php

    请注意等号是自动添加的。

    如果使用多个方法调用,它们将在它们之间用 **AND** 链在一起:

    .. literalinclude:: query_builder/022.php

2. 自定义键/值方法
^^^^^^^^^^^^^^^^^^^^^^^^^^

    你可以在第一个参数中包含一个运算符来控制比较:

    .. literalinclude:: query_builder/023.php

3. 关联数组方法
^^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. literalinclude:: query_builder/024.php

    使用此方法也可以包含自己的运算符:

    .. literalinclude:: query_builder/025.php

4. 自定义字符串
^^^^^^^^^^^^^^^^

    你可以手动编写自己的子句:

    .. literalinclude:: query_builder/026.php

    .. warning:: 如果在字符串中使用用户提供的数据,则必须手动对值和标识符进行转义。否则可能会导致 SQL 注入。

        .. literalinclude:: query_builder/027.php

.. _query-builder-where-rawsql:

5. RawSql
^^^^^^^^^

    .. versionadded:: 4.2.0

    从 v4.2.0 开始, ``$builder->where()`` 接受一个 ``CodeIgniter\Database\RawSql`` 实例,它表示原始 SQL 字符串。

    .. literalinclude:: query_builder/100.php

    .. warning:: 当你使用 ``RawSql`` 时,必须手动对值和标识符进行转义。否则可能会导致 SQL 注入。

.. _query-builder-where-subquery:

6. 子查询
^^^^^^^^^^^^^

    .. literalinclude:: query_builder/028.php

$builder->orWhere()
-------------------

此方法与上面的方法相同,只是多个实例由 **OR** 连接:

.. literalinclude:: query_builder/029.php

$builder->whereIn()
-------------------

生成一个与 **AND** 连接的 **WHERE field IN ('item', 'item')** SQL 查询(如果适用):

.. literalinclude:: query_builder/030.php

你可以使用子查询而不是值数组:

.. literalinclude:: query_builder/031.php

$builder->orWhereIn()
---------------------

生成一个与 **OR** 连接的 **WHERE field IN ('item', 'item')** SQL 查询(如果适用):

.. literalinclude:: query_builder/032.php

你可以使用子查询而不是值数组:

.. literalinclude:: query_builder/033.php

$builder->whereNotIn()
----------------------

生成一个与 **AND** 连接的 **WHERE field NOT IN ('item', 'item')** SQL 查询(如果适用):

.. literalinclude:: query_builder/034.php

你可以使用子查询而不是值数组:

.. literalinclude:: query_builder/035.php

$builder->orWhereNotIn()
------------------------

生成一个与 **OR** 连接的 **WHERE field NOT IN ('item', 'item')** SQL 查询(如果适用):

.. literalinclude:: query_builder/036.php

你可以使用子查询而不是值数组:

.. literalinclude:: query_builder/037.php

************************
查找类似数据
************************

Like
====

$builder->like()
----------------

此方法使你可以生成 **LIKE** 子句,用于执行搜索。

.. note:: 传递给此方法的所有值都会自动转义。

.. note:: 可以通过向方法传递第五个参数 ``true`` 来强制所有 ``like*`` 方法变体执行不区分大小写的搜索。这将在可用的情况下使用特定于平台的功能,否则,它将强制值变为小写,即 ``WHERE LOWER(column) LIKE '%search%'``。这可能需要为 ``LOWER(column)`` 而不是 ``column`` 创建索引才能有效。

1. 简单的键/值方法
^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. literalinclude:: query_builder/038.php

    如果使用多个方法调用,它们将在它们之间用 **AND** 链在一起:

    .. literalinclude:: query_builder/039.php

    如果要控制通配符 (**%**) 的放置位置,可以使用可选的第三个参数。你的选项是 ``before``、``after`` 和 ``both`` (默认)。

    .. literalinclude:: query_builder/040.php

2. 关联数组方法
^^^^^^^^^^^^^^^^^^^^^^^^^^^

       .. literalinclude:: query_builder/041.php

.. _query-builder-like-rawsql:

3. RawSql
^^^^^^^^^

    .. versionadded:: 4.2.0

    从 v4.2.0 开始, ``$builder->like()`` 接受一个 ``CodeIgniter\Database\RawSql`` 实例,它表示原始 SQL 字符串。

    .. literalinclude:: query_builder/101.php

    .. warning:: 当你使用 ``RawSql`` 时,必须手动对值和标识符进行转义。否则可能会导致 SQL 注入。

$builder->orLike()
------------------

此方法与上面相同,只是多个实例由 **OR** 连接:

.. literalinclude:: query_builder/042.php

$builder->notLike()
-------------------

此方法与 ``like()`` 相同,只是它生成 **NOT LIKE** 语句:

.. literalinclude:: query_builder/043.php

$builder->orNotLike()
---------------------

此方法与 ``notLike()`` 相同,只是多个实例由 **OR** 连接:

.. literalinclude:: query_builder/044.php

$builder->groupBy()
-------------------

允许你编写查询的 **GROUP BY** 部分:

.. literalinclude:: query_builder/045.php

你也可以传递多个值的数组:

.. literalinclude:: query_builder/046.php

$builder->distinct()
--------------------

向查询添加 **DISTINCT** 关键字

.. literalinclude:: query_builder/047.php

$builder->having()
------------------

允许你编写查询的 **HAVING** 部分。有 2 种可能的语法,1 个参数或 2 个:

.. literalinclude:: query_builder/048.php

你也可以传递多个值的数组:

.. literalinclude:: query_builder/049.php

如果你使用转义值的数据库,可以通过传递可选的第三个参数并将其设置为 ``false`` 来防止转义内容。

.. literalinclude:: query_builder/050.php

$builder->orHaving()
--------------------

与 ``having()`` 相同,只是使用 **OR** 分隔多个子句。

$builder->havingIn()
--------------------

生成一个与 **AND** 相连的 **HAVING 字段 IN ('item', 'item')** SQL查询(如果适用):

.. literalinclude:: query_builder/051.php

你可以使用子查询而不是值数组:

.. literalinclude:: query_builder/052.php

$builder->orHavingIn()
----------------------

生成一个与 **OR** 相连的 **HAVING 字段 IN ('item', 'item')** SQL查询(如果适用):

.. literalinclude:: query_builder/053.php

你可以使用子查询而不是值数组:

.. literalinclude:: query_builder/054.php

$builder->havingNotIn()
-----------------------

生成一个与 **AND** 相连的 **HAVING 字段 NOT IN ('item', 'item')** SQL查询(如果适用):

.. literalinclude:: query_builder/055.php

你可以使用子查询而不是值数组:

.. literalinclude:: query_builder/056.php

$builder->orHavingNotIn()
-------------------------

生成一个与 **OR** 相连的 **HAVING 字段 NOT IN ('item', 'item')** SQL查询(如果适用):

.. literalinclude:: query_builder/057.php

你可以使用子查询而不是值数组:

.. literalinclude:: query_builder/058.php

$builder->havingLike()
----------------------

此方法使你可以为 **HAVING** 部分生成 **LIKE** 子句,用于执行搜索。

.. warning:: 传递给此方法的所有值都会自动转义。

.. warning:: 可以通过向方法传递第五个参数 ``true`` 来强制所有 ``havingLike*()`` 方法变体执行不区分大小写的搜索。这将在可用的情况下使用特定于平台的功能,否则,它将强制值变为小写,即 ``HAVING LOWER(column) LIKE '%search%'``。这可能需要为 ``LOWER(column)`` 而不是 ``column`` 创建索引才能有效。

1. 简单的键/值方法
^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. literalinclude:: query_builder/059.php

    如果使用多个方法调用,它们将在它们之间用 **AND** 链在一起:

    .. literalinclude:: query_builder/060.php

    如果要控制通配符 (**%**) 的放置位置,可以使用可选的第三个参数。你的选项是 ``before``、``after`` 和 ``both`` (默认)。

    .. literalinclude:: query_builder/061.php

2. 关联数组方法
^^^^^^^^^^^^^^^^^^^^^^^^^^^

       .. literalinclude:: query_builder/062.php

$builder->orHavingLike()
------------------------

此方法与上面相同,只是多个实例由 **OR** 连接:

.. literalinclude:: query_builder/063.php

$builder->notHavingLike()
-------------------------

此方法与 ``havingLike()`` 相同,只是它生成 **NOT LIKE** 语句:

.. literalinclude:: query_builder/064.php

$builder->orNotHavingLike()
---------------------------

此方法与 ``notHavingLike()`` 相同,只是多个实例由 **OR** 连接:

.. literalinclude:: query_builder/065.php

****************
排序结果
****************

OrderBy
=======

$builder->orderBy()
-------------------

允许你设置 **ORDER BY** 子句。

第一个参数包含要排序的列的名称。

第二个参数让你设置所请求的排序方向 - ASC、DESC 或 random。

.. literalinclude:: query_builder/066.php

你也可以在第一个参数中传递自己的字符串:

.. literalinclude:: query_builder/067.php

或者如果需要对多个字段进行排序,可以进行多次方法调用。

.. literalinclude:: query_builder/068.php

如果选择 ``RANDOM`` 排序方向,则首参数将被忽略,除非指定数值种子。

.. literalinclude:: query_builder/069.php

****************************
限制或计数结果
****************************

Limit
=====

$builder->limit()
-----------------

允许你限制返回的行数:

.. literalinclude:: query_builder/070.php

第二个参数允许你设置结果偏移量。

.. literalinclude:: query_builder/071.php

$builder->countAllResults()
---------------------------

允许你确定特定 Query Builder 查询中的行数。查询将接受 Query Builder 限制器,如 ``where()``、``orWhere()``、``like()``、``orLike()`` 等。例如:

.. literalinclude:: query_builder/072.php

但是,此方法也会重置你可能传递给 ``select()`` 的任何字段值。如果需要保留它们,可以将第一个参数设置为 ``false``。

.. literalinclude:: query_builder/073.php

$builder->countAll()
--------------------

允许你确定特定表中的行数。例如:

.. literalinclude:: query_builder/074.php

与 ``countAllResult()`` 方法一样,此方法也会重置你可能传递给 ``select()`` 的任何字段值。如果需要保留它们,可以将第一个参数设置为 ``false``。

.. _query-builder-union:

*************
联合查询
*************

Union
=====

$builder->union()
-----------------

用于合并两个或多个 SELECT 语句的结果。它将只返回唯一的结果。

.. literalinclude:: query_builder/103.php

.. warning:: 对于正确使用某些 DBMS(如 MSSQL 和 Oracle),查询将被包装在 ``SELECT * FROM ( ... ) alias`` 中。
    主查询总是具有 ``uwrp0`` 的别名。每个后续通过 ``union()`` 添加的查询都具有 ``uwrpN+1`` 的别名。

所有联合查询都将在主查询之后添加,而不考虑调用 ``union()`` 方法的顺序。也就是说, ``limit()`` 或 ``orderBy()`` 方法将针对主查询,即使在 ``union()`` 之后调用。

在某些情况下,可能需要对查询结果进行排序或限制记录数。解决方案是使用通过 ``$db->newQuery()`` 创建的 wrapper。在下面的示例中,我们获取前 5 个用户 + 最后 5 个用户并按 id 排序:

.. literalinclude:: query_builder/104.php

$builder->unionAll()
--------------------

行为与 ``union()`` 方法相同。但是,将返回所有结果,而不仅仅是唯一的结果。

**************
分组查询
**************

Group
=====

查询分组允许你通过用括号将它们分组来创建复杂的 **WHERE** 子句。这将允许你创建具有复杂 **WHERE** 子句的查询。支持嵌套分组。例如:

.. literalinclude:: query_builder/075.php

.. warning:: 分组需要平衡,请确保每个 ``groupStart()`` 都与 ``groupEnd()`` 匹配。

$builder->groupStart()
----------------------

通过向查询的 **WHERE** 子句添加开括号来启动新的分组。

$builder->orGroupStart()
------------------------

通过向查询的 **WHERE** 子句添加开括号并添加 **OR** 前缀来启动新的分组。

$builder->notGroupStart()
-------------------------

通过向查询的 **WHERE** 子句添加开括号并添加 **NOT** 前缀来启动新的分组。

$builder->orNotGroupStart()
---------------------------

通过向查询的 **WHERE** 子句添加开括号并添加 **OR NOT** 前缀来启动新的分组。

$builder->groupEnd()
--------------------

通过向查询的 **WHERE** 子句添加闭括号来结束当前分组。

$builder->havingGroupStart()
----------------------------

通过向查询的 **HAVING** 子句添加开括号来启动新的分组。

$builder->orHavingGroupStart()
------------------------------

通过向查询的 **HAVING** 子句添加开括号并添加 **OR** 前缀来启动新的分组。

$builder->notHavingGroupStart()
-------------------------------

通过向查询的 **HAVING** 子句添加开括号并添加 **NOT** 前缀来启动新的分组。

$builder->orNotHavingGroupStart()
---------------------------------

通过向查询的 **HAVING** 子句添加开括号并添加 **OR NOT** 前缀来启动新的分组。

$builder->havingGroupEnd()
--------------------------

通过向查询的 **HAVING** 子句添加闭括号来结束当前分组。

**************
插入数据
**************

Insert
======

$builder->insert()
------------------

根据你提供的数据生成 insert 字符串并运行查询。你可以将一个 **数组** 或 **对象** 传递给该方法。下面是一个使用数组的示例:

.. literalinclude:: query_builder/076.php

第一个参数是一个关联数组。

.. note:: 除 ``RawSql`` 外,所有值都会自动转义,生成更安全的查询。

.. warning:: 当你使用 ``RawSql`` 时,必须手动对数据进行转义。否则可能会导致 SQL 注入。

这是一个使用对象的示例:

.. literalinclude:: query_builder/077.php

.. literalinclude:: query_builder/121.php

第一个参数是一个对象。

$builder->ignore()
------------------

根据你提供的数据生成 insert ignore 字符串并运行查询。所以如果具有相同主键的条目已经存在,则不会插入查询。
你可以选择向方法传递一个 **布尔值**。也可用于 **insertBatch**、**update** 和 **delete** (若支持)。
下面是一个使用上述数组的示例:

.. literalinclude:: query_builder/078.php

$builder->getCompiledInsert()
-----------------------------

编译插入查询,就像 ``$builder->insert()`` 一样,但不运行查询。此方法简单地将 SQL 查询作为字符串返回。

例如:

.. literalinclude:: query_builder/079.php

第一个参数使你可以设置查询构建器查询是否将重置(默认情况下,它将重置,就像 ``$builder->insert()`` 一样):

.. literalinclude:: query_builder/080.php

之所以第二个查询有效,是因为第一个参数设置为 ``false``。

.. note:: 此方法不适用于批量插入。

.. _insert-batch-data:

insertBatch
===========

$builder->insertBatch()
-----------------------

通过数据插入
^^^^^^^^^^^^^^^^

根据你提供的数据生成 insert 字符串,并运行查询。你可以将一个 **数组** 或 **对象** 传递给该方法。下面是一个使用数组的示例:

.. literalinclude:: query_builder/081.php

第一个参数是一个关联数组。

.. note:: 除 ``RawSql`` 外,所有值都会自动转义,生成更安全的查询。

.. warning:: 当你使用 ``RawSql`` 时,必须手动对数据进行转义。否则可能会导致 SQL 注入。

通过查询插入
^^^^^^^^^^^^^^^^^^^

你也可以从查询中插入:

.. literalinclude:: query_builder/117.php

.. note:: ``setQueryAsData()`` 可从 v4.3.0 开始使用。

.. note:: 必须将选择查询的列别名为目标表的列名。

.. _upsert-data:

**************
插入更新数据
**************

Upsert
======

$builder->upsert()
------------------

.. versionadded:: 4.3.0

根据你提供的数据生成插入更新字符串,并运行查询。你可以将一个 **数组** 或 **对象** 传递给该方法。默认情况下,约束将按顺序定义。首先选择主键,然后是唯一键。MySQL 将默认使用任何约束。下面是一个使用数组的示例:

.. literalinclude:: query_builder/112.php

第一个参数是一个关联数组。

这是一个使用对象的示例:

.. literalinclude:: query_builder/122.php

.. literalinclude:: query_builder/113.php

第一个参数是一个对象。

.. note:: 所有值都会自动转义,生成更安全的查询。

$builder->getCompiledUpsert()
-----------------------------

.. versionadded:: 4.3.0

编译插入更新查询,就像 ``$builder->upsert()`` 一样,但不运行查询。此方法简单地将 SQL 查询作为字符串返回。

例如:

.. literalinclude:: query_builder/114.php

.. note:: 此方法不适用于批量插入更新。

upsertBatch
===========

$builder->upsertBatch()
-----------------------

.. versionadded:: 4.3.0

通过数据插入更新
^^^^^^^^^^^^^^^^

根据你提供的数据生成插入更新字符串,并运行查询。你可以将一个 **数组** 或 **对象** 传递给该方法。默认情况下,约束将按顺序定义。首先选择主键,然后是唯一键。MySQL 将默认使用任何约束。

下面是一个使用数组的示例:

.. literalinclude:: query_builder/108.php

第一个参数是一个关联数组。

.. note:: 所有值都会自动转义,生成更安全的查询。

通过查询插入更新
^^^^^^^^^^^^^^^^^^^

你也可以从查询中插入更新:

.. literalinclude:: query_builder/115.php

.. note:: ``setQueryAsData()``、``onConstraint()`` 和 ``updateFields()`` 方法可从 v4.3.0 开始使用。

.. note:: 必须将选择查询的列别名为目标表的列名。

$builder->onConstraint()
------------------------

.. versionadded:: 4.3.0

允许手动设置要用于插入更新的约束。这与 MySQL 不兼容,因为 MySQL 默认检查所有约束。

.. literalinclude:: query_builder/109.php

此方法接受字符串或列数组。

$builder->updateFields()
------------------------

.. versionadded:: 4.3.0

允许手动设置执行插入更新时要更新的字段。

.. literalinclude:: query_builder/110.php

此方法接受字符串、列数组或 RawSql。你还可以指定要更新的额外列,该列不包括在数据集中。这可以通过将第二个参数设置为 ``true`` 来完成。

.. literalinclude:: query_builder/111.php

请注意, ``updated_at`` 字段未插入但用于更新。

*************
更新数据
*************

Update
======

$builder->replace()
-------------------

这将执行一个 **REPLACE** 语句,基本上是可选的 **DELETE** + **INSERT** 的 SQL标准,使用 *PRIMARY* 和 *UNIQUE* 键作为确定因素。
在我们的例子中,它将省去你需要实现 select()、update()、delete() 和 insert() 调用的不同组合的复杂逻辑的需要。

例如:

.. literalinclude:: query_builder/082.php

在上面的示例中,如果我们假设 ``title`` 字段是我们的主键,则如果一行包含 ``My title`` 作为 ``title`` 值,则会删除该行,并用我们的新行数据替换它。

也允许使用 ``set()`` 方法,所有值都会自动转义,就像 ``insert()`` 一样。

$builder->set()
---------------

此方法使你可以为以后通过 ``insert()`` 或 ``update()`` 方法传入的插入或更新设置值。

**它可以代替直接将数据数组传递给 insert() 或 update() 方法:**

.. literalinclude:: query_builder/083.php

如果使用多个方法调用,它们将根据你执行插入还是更新来正确组装:

.. literalinclude:: query_builder/084.php

``set()`` 也将接受一个可选的第三个参数(``$escape``),如果设置为 ``false`` 将阻止对值进行转义。为了说明差异,这里 ``set()`` 同时使用和不使用 escape 参数的示例。

.. literalinclude:: query_builder/085.php

你也可以向此方法传递关联数组:

.. literalinclude:: query_builder/086.php

或者一个对象:

.. literalinclude:: query_builder/077.php

.. literalinclude:: query_builder/087.php

$builder->update()
------------------

根据你提供的数据生成 update 字符串并运行查询。你可以将一个 **数组** 或 **对象** 传递给该方法。下面是一个使用数组的示例:

.. literalinclude:: query_builder/088.php

或者你可以提供一个对象:

.. literalinclude:: query_builder/077.php

.. literalinclude:: query_builder/089.php

.. note:: 除 ``RawSql`` 外,所有值都会自动转义,生成更安全的查询。

.. warning:: 当你使用 ``RawSql`` 时,必须手动对数据进行转义。否则可能会导致 SQL 注入。

你会注意到使用了 ``$builder->where()`` 方法,使你可以设置 **WHERE** 子句。
你可以选择直接将此信息作为字符串传递给 ``update()`` 方法:

.. literalinclude:: query_builder/090.php

或者作为数组:

.. literalinclude:: query_builder/091.php

你也可以在执行更新时使用上面描述的 ``$builder->set()`` 方法。

$builder->getCompiledUpdate()
-----------------------------

此方法的工作方式与 ``$builder->getCompiledInsert()`` 完全相同，只是它生成的是 **UPDATE** SQL 字符串，而不是 **INSERT** SQL 字符串。

要获取更多信息，请查看 `$builder->getCompiledInsert()`_ 的文档。

.. note:: 这个方法不适用于批量更新。

.. _update-batch:

UpdateBatch
===========

$builder->updateBatch()
-----------------------

.. note:: 从 v4.3.0 开始, ``updateBatch()`` 的第二个参数 ``$index`` 改为 ``$constraints``。它现在接受数组、字符串或 ``RawSql`` 类型。

通过数据更新
^^^^^^^^^^^^^^^^

根据你提供的数据生成 update 字符串,并运行查询。你可以将一个 **数组** 或 **对象** 传递给该方法。下面是一个使用数组的示例:

.. literalinclude:: query_builder/092.php

第一个参数是一个关联数组,第二个参数是 where 键。

.. note:: 从 v4.3.0 开始,生成的 SQL 结构得到了改进。

从 v4.3.0 开始,你也可以使用 ``onConstraint()`` 和 ``updateFields()`` 方法:

.. literalinclude:: query_builder/120.php

.. note:: 除 ``RawSql`` 外,所有值都会自动转义,生成更安全的查询。

.. warning:: 当你使用 ``RawSql`` 时,必须手动对数据进行转义。否则可能会导致 SQL 注入。

.. note:: 由于这项工作的性质,此方法无法为 ``affectedRows()`` 提供适当的结果。
    相反, ``updateBatch()`` 返回受影响的行数。

通过查询更新
^^^^^^^^^^^^^^^^^^^

从 v4.3.0 开始，你也可以使用 ``setQueryAsData()`` 方法从查询中进行更新：

.. literalinclude:: query_builder/116.php

.. note:: 必须将选择查询的列别名为目标表的列名。

*************
删除数据
*************

Delete
======

$builder->delete()
------------------

生成 **DELETE** SQL 字符串并运行查询。

.. literalinclude:: query_builder/093.php

第一个参数是 where 子句。
你也可以使用 ``where()`` 或 ``orWhere()`` 方法,而不是将数据传递给方法的第一个参数:

.. literalinclude:: query_builder/094.php

如果要从表中删除所有数据,可以使用 ``truncate()`` 方法或 ``emptyTable()``。

$builder->getCompiledDelete()
-----------------------------

此方法的工作方式与 ``$builder->getCompiledInsert()`` 完全相同,只是它生成 **DELETE** SQL 字符串而不是 **INSERT** SQL 字符串。

有关更多信息,请查看 `$builder->getCompiledInsert()`_ 的文档。

.. _delete-batch:

DeleteBatch
===========

$builder->deleteBatch()
-----------------------

.. versionadded:: 4.3.0

通过数据删除
^^^^^^^^^^^^^^^^

根据一组数据生成批量 **DELETE** 语句。

.. literalinclude:: query_builder/118.php

当在具有复合主键的表中删除数据时,此方法特别有用。

.. note:: SQLite3 不支持使用 ``where()``。

通过查询删除
^^^^^^^^^^^^^^^^^^^

你也可以从查询中删除:

.. literalinclude:: query_builder/119.php

$builder->emptyTable()
----------------------

生成 **DELETE** SQL 字符串并运行查询:

.. literalinclude:: query_builder/095.php

$builder->truncate()
--------------------

生成 **TRUNCATE** SQL 字符串并运行查询。

.. literalinclude:: query_builder/096.php

.. note:: 如果不可用 TRUNCATE 命令, ``truncate()`` 将使用 ``DELETE FROM table``。

**********************
条件语句
**********************

.. _db-builder-when:

When
====

$builder->when()
----------------

.. versionadded:: 4.3.0

这允许基于条件修改查询,而不会打破查询构建器链。第一个参数是条件,它应该评估为布尔值。第二个参数是可调用的,它将在条件为 true 时运行。

例如,你可能只想应用给定的 WHERE 语句基于 HTTP 请求中发送的值:

.. literalinclude:: query_builder/105.php

由于条件评估为 ``true``,所以可调用的将被调用。条件中设置的值将作为第二个参数传递给可调用的,以便可以在查询中使用它。

有时你可能希望在条件评估为 false 时应用不同的语句。这可以通过提供第二个闭包来实现:

.. literalinclude:: query_builder/106.php

WhenNot
=======

$builder->whenNot()
-------------------

.. versionadded:: 4.3.0

这与 ``$builder->when()`` 的工作方式完全相同,只是它只有在条件评估为 ``false`` 时才会运行可调用的,而不是像 ``when()`` 中的 ``true``。

.. literalinclude:: query_builder/107.php

***************
方法链
***************

方法链允许你通过连接多个方法来简化语法。考虑这个例子:

.. literalinclude:: query_builder/097.php

.. _ar-caching:

***********************
重置查询构建器
***********************

ResetQuery
==========

$builder->resetQuery()
----------------------

重置查询构建器允许你在不先使用 ``$builder->get()`` 或 ``$builder->insert()`` 等方法执行查询的情况下重新开始查询。

当你使用查询构建器生成 SQL(例如 ``$builder->getCompiledSelect()``),然后选择运行查询时,这很有用:

.. literalinclude:: query_builder/098.php

***************
类参考
***************

.. php:namespace:: CodeIgniter\Database

.. php:class:: BaseBuilder

    .. php:method:: db()

        :returns:   正在使用的数据库连接
        :rtype:     ``ConnectionInterface``

        从 ``$db`` 返回当前数据库连接。用于访问查询构建器无法直接使用的 ``ConnectionInterface`` 方法,如 ``insertID()`` 或 ``errors()``。

    .. php:method:: resetQuery()

        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        重置当前的查询构建器状态。当你想要构建可在某些条件下取消的查询时很有用。

    .. php:method:: countAllResults([$reset = true])

        :param bool $reset: 是否重置 SELECT 的值
        :returns:   查询结果中的行数
        :rtype:     int

        生成平台特定的查询字符串,用于统计查询构建器查询返回的所有记录。

    .. php:method:: countAll([$reset = true])

        :param bool $reset: 是否重置 SELECT 的值
        :returns:   查询结果中的行数
        :rtype:     int

        生成平台特定的查询字符串,用于统计特定表中的所有记录。

    .. php:method:: get([$limit = null[, $offset = null[, $reset = true]]]])

        :param int $limit: LIMIT 子句
        :param int $offset: OFFSET 子句
        :param bool $reset: 是否要清除查询构建器的值?
        :returns: ``\CodeIgniter\Database\ResultInterface`` 实例(方法链)
        :rtype:    ``\CodeIgniter\Database\ResultInterface``

        编译并运行基于已经调用的查询构建器方法的 ``SELECT`` 语句。

    .. php:method:: getWhere([$where = null[, $limit = null[, $offset = null[, $reset = true]]]]])

        :param string $where: WHERE 子句
        :param int $limit: LIMIT 子句
        :param int $offset: OFFSET 子句
        :param bool $reset: 是否要清除查询构建器的值?
        :returns:   ``\CodeIgniter\Database\ResultInterface`` 实例(方法链)
        :rtype:     ``\CodeIgniter\Database\ResultInterface``

        与 ``get()`` 相同,但也允许直接添加 WHERE。

    .. php:method:: select([$select = '*'[, $escape = null]])

        :param array|RawSql|string $select: 查询的 SELECT 部分
        :param bool $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向查询添加 ``SELECT`` 子句。

    .. php:method:: selectAvg([$select = ''[, $alias = '']])

        :param string $select: 要计算平均值的字段
        :param string $alias: 结果值名称的别名
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向查询添加 ``SELECT AVG(field)`` 子句。

    .. php:method:: selectMax([$select = ''[, $alias = '']])

        :param string $select: 要计算最大值的字段
        :param string $alias: 结果值名称的别名
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向查询添加 ``SELECT MAX(field)`` 子句。

    .. php:method:: selectMin([$select = ''[, $alias = '']])

        :param string $select: 要计算最小值的字段
        :param string $alias: 结果值名称的别名
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向查询添加 ``SELECT MIN(field)`` 子句。

    .. php:method:: selectSum([$select = ''[, $alias = '']])

        :param string $select: 要计算总和的字段
        :param string $alias: 结果值名称的别名
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向查询添加 ``SELECT SUM(field)`` 子句。

    .. php:method:: selectCount([$select = ''[, $alias = '']])

        :param string $select: 要计算平均值的字段
        :param string $alias: 结果值名称的别名
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向查询添加 ``SELECT COUNT(field)`` 子句。

    .. php:method:: selectSubquery(BaseBuilder $subquery, string $as)

        :param string $subquery: BaseBuilder 的实例
        :param string $as: 结果值名称的别名
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向选择添加子查询

    .. php:method:: distinct([$val = true])

        :param bool $val: “distinct” 标志的期望值
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        设置一个标志,告诉查询构建器向查询的 ``SELECT`` 部分添加 ``DISTINCT`` 子句。

    .. php:method:: from($from[, $overwrite = false])

        :param mixed $from: 表名(字符串或数组)
        :param bool    $overwrite: 是否删除第一个已存在的表?
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        指定查询的 ``FROM`` 子句。

    .. php:method:: fromSubquery($from, $alias)

        :param BaseBuilder $from: BaseBuilder 类的实例
        :param string      $alias: 子查询的别名
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        使用子查询指定查询的 ``FROM`` 子句。

    .. php:method:: setQueryAsData($query[, $alias[, $columns = null]])

        .. versionadded:: 4.3.0

        :param BaseBuilder|RawSql $query: BaseBuilder 或 RawSql 的实例
        :param string|null $alias: 查询的别名
        :param array|string|null $columns: 查询中的列,以数组或逗号分隔的字符串表示
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        为 ``insertBatch()``、``updateBatch()``、``upsertBatch()`` 设置查询作为数据源。
        如果 ``$columns`` 为 null,则会运行查询来生成列名。

    .. php:method:: join($table, $cond[, $type = ''[, $escape = null]])

        :param string $table: 要连接的表名
        :param string $cond: JOIN ON 条件
        :param string $type: JOIN 类型
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向查询添加 ``JOIN`` 子句。

    .. php:method:: where($key[, $value = null[, $escape = null]])

        :param array|RawSql|string $key: 要比较的字段名称,或关联数组
        :param mixed $value: 如果是单个键,则与此值进行比较
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        生成查询的 ``WHERE`` 部分。使用 ``AND`` 分隔多个调用。

    .. php:method:: orWhere($key[, $value = null[, $escape = null]])

        :param mixed $key: 要比较的字段名称,或关联数组
        :param mixed $value: 如果是单个键,则与此值进行比较
        :param bool $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        生成查询的 ``WHERE`` 部分。使用 ``OR`` 分隔多个调用。

    .. php:method:: orWhereIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要搜索的字段
        :param array|BaseBulder|Closure $values: 目标值的数组,或子查询的匿名函数
        :param bool $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        生成 ``WHERE`` 字段 ``IN('item', 'item')`` SQL 查询,如果适用的话,使用 ``OR`` 连接。

    .. php:method:: orWhereNotIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要搜索的字段
        :param array|BaseBulder|Closure $values: 目标值的数组,或子查询的匿名函数
        :param bool $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        生成 ``WHERE`` 字段 ``NOT IN('item', 'item')`` SQL 查询,如果适用的话,使用 ``OR`` 连接。

    .. php:method:: whereIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要检查的字段名称
        :param array|BaseBulder|Closure $values: 目标值的数组,或子查询的匿名函数
        :param bool $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        生成 ``WHERE`` 字段 ``IN('item', 'item')`` SQL 查询,如果适用的话,使用 ``AND`` 连接。

    .. php:method:: whereNotIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要检查的字段名称
        :param array|BaseBulder|Closure $values: 目标值的数组,或子查询的匿名函数
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        生成 ``WHERE`` 字段 ``NOT IN('item', 'item')`` SQL 查询,如果适用的话,使用 ``AND`` 连接。

    .. php:method:: groupStart()

        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        启动一个组表达式,对表达式内的条件使用 ``AND`` 连接。

    .. php:method:: orGroupStart()

        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        启动一个组表达式,对表达式内的条件使用 ``OR`` 连接。

    .. php:method:: notGroupStart()

        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        启动一个组表达式,对表达式内的条件使用 ``AND NOT`` 连接。

    .. php:method:: orNotGroupStart()

        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        启动一个组表达式,对表达式内的条件使用 ``OR NOT`` 连接。

    .. php:method:: groupEnd()

        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        结束一个组表达式。

    .. php:method:: like($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param array|RawSql|string $field: 字段名称
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制执行不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向查询添加 ``LIKE`` 子句,使用 ``AND`` 分隔多个调用。

    .. php:method:: orLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名称
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制执行不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向查询添加 ``LIKE`` 子句,使用 ``OR`` 分隔多个调用。

    .. php:method:: notLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名称
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制执行不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向查询添加 ``NOT LIKE`` 子句,使用 ``AND`` 分隔多个调用。

    .. php:method:: orNotLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名称
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制执行不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向查询添加 ``NOT LIKE`` 子句,使用 ``OR`` 分隔多个调用。

    .. php:method:: having($key[, $value = null[, $escape = null]])

        :param mixed $key: 标识符(字符串)或字段/值对的关联数组
        :param string $value: 如果 $key 是标识符,则查找此值
        :param string $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向查询添加 ``HAVING`` 子句,使用 ``AND`` 分隔多个调用。

    .. php:method:: orHaving($key[, $value = null[, $escape = null]])

        :param mixed $key: 标识符(字符串)或字段/值对的关联数组
        :param string $value: 如果 $key 是标识符,则查找此值
        :param string $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向查询添加 ``HAVING`` 子句,使用 ``OR`` 分隔多个调用。

    .. php:method:: orHavingIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要搜索的字段
        :param array|BaseBulder|Closure $values: 目标值的数组或子查询的匿名函数
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        生成 ``HAVING`` 字段 ``IN('item', 'item')`` SQL查询,如果适用的话,使用 ``OR`` 连接。

    .. php:method:: orHavingNotIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要搜索的字段
        :param array|BaseBulder|Closure $values: 目标值的数组或子查询的匿名函数
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        生成 ``HAVING`` 字段 ``NOT IN('item', 'item')`` SQL查询,如果适用的话,使用 ``OR`` 连接。

    .. php:method:: havingIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要检查的字段名称
        :param array|BaseBulder|Closure $values: 目标值的数组或子查询的匿名函数
        :param bool $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        生成 ``HAVING`` 字段 ``IN('item', 'item')`` SQL查询,如果适用的话,使用 ``AND`` 连接。

    .. php:method:: havingNotIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要检查的字段名称
        :param array|BaseBulder|Closure $values: 目标值的数组或子查询的匿名函数
        :param bool $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制执行不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        生成 ``HAVING`` 字段 ``NOT IN('item', 'item')`` SQL查询,如果适用的话,使用 ``AND`` 连接。

    .. php:method:: havingLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名称
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制执行不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向 ``HAVING`` 部分添加 ``LIKE`` 子句,使用 ``AND`` 分隔多个调用。

    .. php:method:: orHavingLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名称
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制执行不区分大小写的搜索
        :returns: ``BaseBuilder`` 实例(方法链)
        :rtype:    ``BaseBuilder``

        向 ``HAVING`` 部分添加 ``LIKE`` 子句,使用 ``OR`` 分隔多个调用。

    .. php:method:: notHavingLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名称
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制执行不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向 ``HAVING`` 部分添加 ``NOT LIKE`` 子句,使用 ``AND`` 分隔多个调用。

    .. php:method:: orNotHavingLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名称
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向 ``HAVING`` 部分添加 ``NOT LIKE`` 子句,使用 ``OR`` 分隔多个调用。

    .. php:method:: havingGroupStart()

        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        启动 ``HAVING`` 子句的一个组表达式,对表达式内的条件使用 ``AND`` 连接。

    .. php:method:: orHavingGroupStart()

        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        启动 ``HAVING`` 子句的一个组表达式,对表达式内的条件使用 ``OR`` 连接。

    .. php:method:: notHavingGroupStart()

        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        启动 ``HAVING`` 子句的一个组表达式,对表达式内的条件使用 ``AND NOT`` 连接。

    .. php:method:: orNotHavingGroupStart()

        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        启动 ``HAVING`` 子句的一个组表达式,对表达式内的条件使用 ``OR NOT`` 连接。

    .. php:method:: havingGroupEnd()

        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        结束 ``HAVING`` 子句的一个组表达式。

    .. php:method:: groupBy($by[, $escape = null])

        :param mixed $by: 要分组的字段;字符串或数组
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向查询添加 ``GROUP BY`` 子句。

    .. php:method:: orderBy($orderby[, $direction = ''[, $escape = null]])

        :param string $orderby: 要排序的字段
        :param string $direction: 请求的排序方向 - ASC、DESC 或 random
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向查询添加 ``ORDER BY`` 子句。

    .. php:method:: limit($value[, $offset = 0])

        :param int $value: 要限制结果的行数
        :param int $offset: 要跳过的行数
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向查询添加 ``LIMIT`` 和 ``OFFSET`` 子句。

    .. php:method:: offset($offset)

        :param int $offset: 要跳过的行数
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        向查询添加 ``OFFSET`` 子句。

    .. php:method:: union($union)

        :param BaseBulder|Closure $union: 联合查询
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        添加 ``UNION`` 子句。

    .. php:method:: unionAll($union)

        :param BaseBulder|Closure $union: 联合查询
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        添加 ``UNION ALL`` 子句。

    .. php:method:: set($key[, $value = ''[, $escape = null]])

        :param mixed $key: 字段名称,或字段/值对的数组
        :param mixed $value: 如果 $key 是单个字段,则为字段值
        :param bool    $escape: 是否转义值
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        添加通过 ``insert()``、``update()`` 或 ``replace()`` 稍后传入的字段/值对。

    .. php:method:: insert([$set = null[, $escape = null]])

        :param array $set: 字段/值对的关联数组
        :param bool $escape: 是否转义值
        :returns:   成功则为 ``true``,失败则为 ``false``
        :rtype:     bool

        编译并执行 ``INSERT`` 语句。

    .. php:method:: insertBatch([$set = null[, $escape = null[, $batch_size = 100]]])

        :param array $set: 要插入的数据
        :param bool $escape: 是否转义值
        :param int $batch_size: 一次插入的行数
        :returns: 插入的行数,失败则为 ``false``
        :rtype:    int|false

        编译并执行批量 ``INSERT`` 语句。

        .. note:: 当提供多于 ``$batch_size`` 行时,会执行多个
            ``INSERT`` 查询,每个试图插入最多 ``$batch_size`` 行。

    .. php:method:: setInsertBatch($key[, $value = ''[, $escape = null]])

        .. deprecated:: 4.3.0
           请使用 :php:meth:`CodeIgniter\\Database\\BaseBuilder::setData()` 替代。

        :param mixed $key: 字段名称或字段/值对数组
        :param string $value: 如果 $key 是单个字段,则为字段值
        :param bool $escape: 是否转义值
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        添加后面通过 ``insertBatch()`` 批量插入到表中的字段/值对。

        .. important:: 此方法不建议使用。将在未来版本中删除。

    .. php:method:: upsert([$set = null[, $escape = null]])

        :param array $set: 字段/值对的关联数组
        :param bool $escape: 是否转义值
        :returns:   成功则为 ``true``,失败则为 ``false``
        :rtype:     bool

        编译并执行 ``UPSERT`` 语句。

    .. php:method:: upsertBatch([$set = null[, $escape = null[, $batch_size = 100]]])

        :param array $set: 要插入更新的数据
        :param bool $escape: 是否转义值
        :param int $batch_size: 一次插入更新的行数
        :returns: 插入更新的行数,失败则为 ``false``
        :rtype:    int|false

        编译并执行批量 ``UPSERT`` 语句。

        .. note:: MySQL 使用 ``ON DUPLICATE KEY UPDATE``,每行的 affected-rows 值
            如果行作为新行插入,则为 1;如果更新了现有行,则为 2;如果现有行设置为其当前值,则为 0。

        .. note:: 当提供多于 ``$batch_size`` 行时,会执行多个
            ``UPSERT`` 查询,每个试图插入更新最多 ``$batch_size`` 行。

    .. php:method:: update([$set = null[, $where = null[, $limit = null]]])

        :param array $set: 字段/值对的关联数组
        :param string $where: WHERE 子句
        :param int $limit: LIMIT 子句
        :returns:   成功则为 ``true``,失败则为 ``false``
        :rtype:     bool

        编译并执行 ``UPDATE`` 语句。

    .. php:method:: updateBatch([$set = null[, $constraints = null[, $batchSize = 100]]])

        :param array|object|null $set: 字段名称,或字段/值对的关联数组
        :param array|RawSql|string|null $constraints: 用作更新键的字段或字段集。
        :param int $batchSize: 每个查询分组的条件数
        :returns:   更新的行数,失败则为 ``false``
        :rtype:     int|false

        .. note:: 从 v4.3.0 开始,参数 ``$set`` 和 ``$constraints`` 的类型发生了变化。

        编译并执行批量 ``UPDATE`` 语句。
        ``$constraints`` 参数接受逗号分隔的列字符串,数组,关联数组或 ``RawSql``。

        .. note:: 当提供超过 ``$batchSize`` 个字段/值对时,将执行多个查询,
             每个处理最多 ``$batchSize`` 个字段/值对。 如果我们将 ``$batchSize`` 设置为 0,
             则所有字段/值对将在一个查询中执行。

    .. php:method:: updateFields($set, [$addToDefault = false, [$ignore = null]])

        .. versionadded:: 4.3.0

        :param mixed $set: 列的行或行数组,行是一个数组或对象
        :param bool $addToDefault: 额外添加不在数据集中的列
        :param bool $ignore: 忽略 $set 中的列数组
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        与 ``updateBatch()`` 和 ``upsertBatch()`` 方法一起使用。 这定义了要更新的字段。

    .. php:method:: onConstraint($set)

        .. versionadded:: 4.3.0

        :param mixed $set: 用作键或约束的字段集或字段
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        与 ``updateBatch()`` 和 ``upsertBatch()`` 方法一起使用。 这接受逗号分隔的列字符串,数组,关联数组或 RawSql。

    .. php:method:: setData($set, [$escape = null, [$alias = '']])

        .. versionadded:: 4.3.0

        :param mixed $set: 列的行或行数组,行是一个数组或对象
        :param bool $escape: 是否转义值
        :param bool $alias: 数据集的表别名
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        用于 ``*Batch()`` 方法为插入、更新、插入更新设置数据。

    .. php:method:: setUpdateBatch($key[, $value = ''[, $escape = null]])

        .. deprecated:: 4.3.0
           请使用 :php:meth:`CodeIgniter\\Database\\BaseBuilder::setData()` 替代。

        :param mixed $key: 字段名称或字段/值对数组
        :param string $value: 如果 $key 是单个字段,则为字段值
        :param bool    $escape: 是否转义值
        :returns:   ``BaseBuilder`` 实例(方法链)
        :rtype:     ``BaseBuilder``

        添加后面通过 ``updateBatch()`` 批量更新到表中的字段/值对。

        .. important:: 此方法不建议使用。将在未来版本中删除。

    .. php:method:: replace([$set = null])

        :param array $set: 字段/值对的关联数组
        :returns: 成功则为 ``true``,失败则为 ``false``
        :rtype:    bool

        编译并执行 ``REPLACE`` 语句。

    .. php:method:: delete([$where = ''[, $limit = null[, $reset_data = true]]])

        :param string $where: WHERE 子句
        :param int $limit: LIMIT 子句
        :param bool $reset_data: 是否重置查询的“写入”子句
        :returns:   ``BaseBuilder`` 实例(方法链),失败则为 ``false``
        :rtype:     ``BaseBuilder|false``

        编译并执行 ``DELETE`` 查询。

    .. php:method:: deleteBatch([$set = null[, $constraints = null[, $batchSize = 100]]])

        :param array|object|null $set: 字段名称,或字段/值对的关联数组
        :param array|RawSql|string|null $constraints: 用作删除键的字段或字段集合
        :param int $batchSize: 每个查询要分组的条件数
        :returns:   删除的行数,失败则为 ``false``
        :rtype:     int|false

        编译并执行批量 ``DELETE`` 查询。

    .. php:method:: increment($column[, $value = 1])

        :param string $column: 要递增的列的名称
        :param int $value:  要在列中递增的值

        将字段的值递增指定的量。如果字段不是数值字段,比如 ``VARCHAR``,它可能会被 ``$value`` 替换。

    .. php:method:: decrement($column[, $value = 1])

        :param string $column: 要递减的列的名称
        :param int $value:  要在列中递减的值

        将字段的值递减指定的量。如果字段不是数值字段,比如 ``VARCHAR``,它可能会被 ``$value`` 替换。

    .. php:method:: truncate()

        :returns:   成功则为 ``true``,失败则为 ``false``,测试模式下返回字符串
        :rtype:     bool|string

        对表执行 ``TRUNCATE`` 语句。

        .. note:: 如果使用的数据库平台不支持 ``TRUNCATE``,
            将使用 ``DELETE FROM table`` 代替。

    .. php:method:: emptyTable()

        :returns: 成功则为 ``true``,失败则为 ``false``
        :rtype:    bool

        通过 ``DELETE`` 语句从表中删除所有记录。

    .. php:method:: getCompiledSelect([$reset = true])

        :param bool $reset: 是否重置当前的 QB 值
        :returns: 编译后的 SQL 语句字符串
        :rtype:    string

        编译 ``SELECT`` 语句并将其作为字符串返回。

    .. php:method:: getCompiledInsert([$reset = true])

        :param bool $reset: 是否重置当前的 QB 值
        :returns: 编译后的 SQL 语句字符串
        :rtype:     string

        编译 ``INSERT`` 语句并将其作为字符串返回。

    .. php:method:: getCompiledUpdate([$reset = true])

        :param bool $reset: 是否重置当前的 QB 值
        :returns: 编译后的 SQL 语句字符串
        :rtype:    string

        编译 ``UPDATE`` 语句并将其作为字符串返回。

    .. php:method:: getCompiledDelete([$reset = true])

        :param bool $reset: 是否重置当前的 QB 值
        :returns: 编译后的 SQL 语句字符串
        :rtype:    string

        编译 ``DELETE`` 语句并将其作为字符串返回。
