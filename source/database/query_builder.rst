###################
查询构建器类
###################

CodeIgniter 提供了查询构建器类。这种模式允许使用最少的脚本从数据库中检索、插入和更新信息。在某些情况下，只需一两行代码就能执行数据库操作。
CodeIgniter 不要求每个数据库表都有自己的类文件，而是提供了一个更简化的接口。

除了简单之外，使用查询构建器功能的一个主要好处是，它允许创建数据库无关的应用程序，因为查询语法是由每个数据库适配器生成的。它还允许更安全的查询，因为值由系统自动转义。

.. note:: CodeIgniter 不支持表名和字段名中的点（``.``）。
    从 v4.5.0 开始，支持带点的数据库名称。

.. contents::
    :local:
    :depth: 2

************************
SQL 注入保护
************************

使用查询构建器生成 SQL 语句是相当安全的。然而，它并非被设计为，无论你传递什么数据都能防止 SQL 注入。

传递给查询构建器的参数可以是：
    1. **标识符**，如字段名或表名
    2. 它们的 **值**
    3. **SQL 字符串** 的一部分

查询构建器默认会转义所有 **值**。

它还会默认尝试正确保护 **标识符** 和 **SQL 字符串** 中的标识符。
然而，它是为了在许多用例中良好工作而实现的，并不是设计用来防止所有攻击的。
因此，绝不应该在没有适当验证的情况下将用户输入传入其中。

此外，许多方法都有 ``$escape`` 参数，可以设置为禁用转义。
如果 ``$escape`` 设置为 false，查询构建器将不会提供任何保护，
因此你必须自己确保在将其传递给查询构建器之前，
它们已经被正确转义或保护。
使用 ``RawSql`` 时也是如此，它指定了一个原始 SQL 语句。

*************************
加载查询构建器
*************************

查询构建器通过数据库连接上的 ``table()`` 方法加载。这会为你设置查询的 **FROM** 部分，
并返回查询构建器类的新实例：

.. literalinclude:: query_builder/001.php

查询构建器仅在你明确请求该类时才加载到内存中，因此默认情况下不使用任何资源。

**************
选择数据
**************

以下方法允许构建 SQL **SELECT** 语句。

Get
===

$builder->get()
---------------

运行选择查询并返回结果。可以单独使用检索表中的所有记录：

.. literalinclude:: query_builder/002.php

第一个和第二个参数允许设置 limit 和 offset 子句：

.. literalinclude:: query_builder/003.php

你会注意到上述方法被赋值给一个名为 $query 的变量，该变量可以用来显示结果：

.. literalinclude:: query_builder/004.php

请访问 :ref:`getResult() <getresult>` 方法，获取关于结果生成的完整讨论。

$builder->getCompiledSelect()
-----------------------------

编译选择查询，就像 ``$builder->get()`` 一样，但不 *运行* 查询。此方法只是将 SQL 查询作为字符串返回。

示例：

.. literalinclude:: query_builder/005.php

下面第一个查询中的参数（false）允许设置是否重置查询构建器
（因为参数的默认值是 true，``getCompiledSelect(bool $reset = true)``，默认情况下它会像使用 ``$builder->get()`` 时一样被重置）：

.. literalinclude:: query_builder/006.php

上述示例的关键点是，第二个查询没有
使用 ``limit(10, 20)``，但生成的 SQL 查询却有 ``LIMIT 20, 10``。
出现这种结果的原因是第一个查询中的参数设置为 ``false``，``limit(10, 20)`` 保留在第二个查询中。

$builder->getWhere()
--------------------

与 ``get()`` 方法相同，只是它允许你在第一个参数中添加
"where" 子句，而不是使用 ``$builder->where()`` 方法：

.. literalinclude:: query_builder/007.php

请阅读下面的 ``where()`` 方法获取更多信息。

.. _query-builder-select:

Select
======

$builder->select()
------------------

允许编写查询的 **SELECT** 部分：

.. literalinclude:: query_builder/008.php

.. note:: 如果从表中选择所有（``*``）字段，则不需要使用此方法。当省略时，CodeIgniter 假定你希望选择所有字段，并自动添加 ``SELECT *``。

``$builder->select()`` 接受一个可选的第二个参数。如果将其设置为 ``false``，CodeIgniter 将不会尝试保护字段或表名。这在需要复合 select 语句且自动转义字段可能破坏它们时非常有用。

.. literalinclude:: query_builder/009.php

.. _query-builder-select-rawsql:

RawSql
^^^^^^

.. versionadded:: 4.2.0

从 v4.2.0 开始，``$builder->select()`` 接受一个 ``CodeIgniter\Database\RawSql`` 实例，它表示原始 SQL 字符串。

.. literalinclude:: query_builder/099.php

.. warning:: 使用 ``RawSql`` 时，必须手动转义值并保护标识符。否则可能导致 SQL 注入。

$builder->selectMax()
---------------------

为查询编写 **SELECT MAX(field)** 部分。可以选择包含第二个参数来重命名结果字段。

.. literalinclude:: query_builder/010.php

$builder->selectMin()
---------------------

为查询编写 **SELECT MIN(field)** 部分。与 ``selectMax()`` 一样，可以选择包含第二个参数来重命名结果字段。

.. literalinclude:: query_builder/011.php

$builder->selectAvg()
---------------------

为查询编写 **SELECT AVG(field)** 部分。与 ``selectMax()`` 一样，可以选择包含第二个参数来重命名结果字段。

.. literalinclude:: query_builder/012.php

$builder->selectSum()
---------------------

为查询编写 **SELECT SUM(field)** 部分。与 ``selectMax()`` 一样，可以选择包含第二个参数来重命名结果字段。

.. literalinclude:: query_builder/013.php

$builder->selectCount()
-----------------------

为查询编写 **SELECT COUNT(field)** 部分。与 ``selectMax()`` 一样，可以选择包含第二个参数来重命名结果字段。

.. note:: 此方法在与 ``groupBy()`` 一起使用时特别有用。对于一般性的结果计数，请参阅 ``countAll()`` 或 ``countAllResults()``。

.. literalinclude:: query_builder/014.php

$builder->selectSubquery()
--------------------------

向 SELECT 部分添加子查询。

.. literalinclude:: query_builder/015.php
   :lines: 2-

From
====

$builder->from()
----------------

允许编写查询的 **FROM** 部分：

.. literalinclude:: query_builder/016.php

.. note:: 如前所示，查询的 **FROM** 部分可以在 ``$db->table()`` 方法中指定。对 ``from()`` 的额外调用将向查询的 FROM 部分添加更多表。

.. _query-builder-from-subquery:

子查询
==========

$builder->fromSubquery()
------------------------

允许将 **FROM** 查询的一部分编写为子查询。

以下示例向现有表添加子查询：

.. literalinclude:: query_builder/017.php

使用 ``$db->newQuery()`` 方法使子查询成为主表：

.. literalinclude:: query_builder/018.php

Join
====

.. _query-builder-join:

$builder->join()
----------------

允许编写查询的 **JOIN** 部分：

.. literalinclude:: query_builder/019.php

如果在一个查询中需要多个连接，可以进行多次方法调用。

如果需要特定类型的 **JOIN**，可以通过方法的第三个参数指定。选项有：``left``、``right``、``outer``、``inner``、``left outer`` 和 ``right outer``。

.. literalinclude:: query_builder/020.php

.. _query-builder-join-rawsql:

RawSql
^^^^^^

.. versionadded:: 4.2.0

从 v4.2.0 开始，``$builder->join()`` 接受一个 ``CodeIgniter\Database\RawSql`` 实例作为 JOIN ON 条件，它表示原始 SQL 字符串。

.. literalinclude:: query_builder/102.php

.. warning:: 使用 ``RawSql`` 时，必须手动转义值并保护标识符。否则可能导致 SQL 注入。

*************************
查找特定数据
*************************

Where
=====

$builder->where()
-----------------

此方法允许使用五种方式设置 **WHERE** 子句：

.. note:: 传递给此方法的所有值都会自动转义，
    产生更安全的查询，除非使用自定义字符串。

.. note:: ``$builder->where()`` 接受一个可选的第三个参数。如果将其设置为
    ``false``，CodeIgniter 将不会尝试保护字段或表名。

1. 简单键/值方式
^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. literalinclude:: query_builder/021.php

    注意，等号会为你自动添加。

    如果使用多个方法调用，它们将用 **AND** 连接在一起：

    .. literalinclude:: query_builder/022.php

2. 自定义键/值方式
^^^^^^^^^^^^^^^^^^^^^^^^^^

    可以在第一个参数中包含运算符以控制比较：

    .. literalinclude:: query_builder/023.php

3. 关联数组方式
^^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. literalinclude:: query_builder/024.php

    也可以使用此方法包含自己的运算符：

    .. literalinclude:: query_builder/025.php

4. 自定义字符串
^^^^^^^^^^^^^^^^

    可以手动编写自己的子句：

    .. literalinclude:: query_builder/026.php

    .. warning:: 如果在字符串中使用用户提供的数据，必须手动转义值并保护标识符。否则可能导致 SQL 注入。

        .. literalinclude:: query_builder/027.php

.. _query-builder-where-rawsql:

5. RawSql
^^^^^^^^^

    .. versionadded:: 4.2.0

    从 v4.2.0 开始，``$builder->where()`` 接受一个 ``CodeIgniter\Database\RawSql`` 实例，它表示原始 SQL 字符串。

    .. literalinclude:: query_builder/100.php

    .. warning:: 使用 ``RawSql`` 时，必须手动转义值并保护标识符。否则可能导致 SQL 注入。

.. _query-builder-where-subquery:

6. 子查询
^^^^^^^^^^^^^

    .. literalinclude:: query_builder/028.php

$builder->orWhere()
-------------------

此方法与上述方法相同，只是多个实例通过 **OR** 连接：

.. literalinclude:: query_builder/029.php

$builder->whereIn()
-------------------

生成一个 **WHERE field IN ('item', 'item')** SQL 查询，在适当时用 **AND** 连接：

.. literalinclude:: query_builder/030.php

可以使用子查询代替值数组：

.. literalinclude:: query_builder/031.php

$builder->orWhereIn()
---------------------

生成一个 **WHERE field IN ('item', 'item')** SQL 查询，在适当时用 **OR** 连接：

.. literalinclude:: query_builder/032.php

可以使用子查询代替值数组：

.. literalinclude:: query_builder/033.php

$builder->whereNotIn()
----------------------

生成一个 **WHERE field NOT IN ('item', 'item')** SQL 查询，在适当时用 **AND** 连接：

.. literalinclude:: query_builder/034.php

可以使用子查询代替值数组：

.. literalinclude:: query_builder/035.php

$builder->orWhereNotIn()
------------------------

生成一个 **WHERE field NOT IN ('item', 'item')** SQL 查询，在适当时用 **OR** 连接：

.. literalinclude:: query_builder/036.php

可以使用子查询代替值数组：

.. literalinclude:: query_builder/037.php

************************
查找相似数据
************************

Like
====

$builder->like()
----------------

此方法允许生成 **LIKE** 子句，用于执行搜索。

.. note:: 传递给此方法的所有值都会自动转义。

.. note:: 所有 ``like*`` 方法变体可以通过向方法传递第五个参数 ``true`` 来强制执行不区分大小写的搜索。这将使用平台特定的功能（如果可用），否则将强制值为小写，即 ``WHERE LOWER(column) LIKE '%search%'``。这可能需要为 ``LOWER(column)`` 而不是 ``column`` 创建索引才能有效。

1. 简单键/值方方式
^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. literalinclude:: query_builder/038.php

    如果使用多个方法调用，它们将用 **AND** 连接在一起：

    .. literalinclude:: query_builder/039.php

    如果想控制通配符（**%**）放置的位置，可以使用可选的第三个参数。选项有 ``before``、``after`` 和 ``both`` （默认）。

    .. literalinclude:: query_builder/040.php

2. 关联数组方式
^^^^^^^^^^^^^^^^^^^^^^^^^^^

       .. literalinclude:: query_builder/041.php

.. _query-builder-like-rawsql:

3. RawSql
^^^^^^^^^

    .. versionadded:: 4.2.0

    从 v4.2.0 开始，``$builder->like()`` 接受一个 ``CodeIgniter\Database\RawSql`` 实例，它表示原始 SQL 字符串。

    .. literalinclude:: query_builder/101.php

    .. warning:: 使用 ``RawSql`` 时，必须手动转义值并保护标识符。否则可能导致 SQL 注入。

$builder->orLike()
------------------

此方法与上述方法相同，只是多个实例通过 **OR** 连接：

.. literalinclude:: query_builder/042.php

$builder->notLike()
-------------------

此方法与 ``like()`` 相同，只是它生成 **NOT LIKE** 语句：

.. literalinclude:: query_builder/043.php

$builder->orNotLike()
---------------------

此方法与 ``notLike()`` 相同，只是多个实例通过 **OR** 连接：

.. literalinclude:: query_builder/044.php

$builder->groupBy()
-------------------

允许编写查询的 **GROUP BY** 部分：

.. literalinclude:: query_builder/045.php

也可以传递多个值的数组：

.. literalinclude:: query_builder/046.php

$builder->distinct()
--------------------

向查询添加 **DISTINCT** 关键字：

.. literalinclude:: query_builder/047.php

$builder->having()
------------------

允许编写查询的 **HAVING** 部分。有 2 种可能的语法，1 个参数或 2 个参数：

.. literalinclude:: query_builder/048.php

也可以传递多个值的数组：

.. literalinclude:: query_builder/049.php

如果使用的数据库由 CodeIgniter 负责转义值，可以通过传递可选的第三个参数并将其设置为 ``false`` 来防止内容被转义。

.. literalinclude:: query_builder/050.php

$builder->orHaving()
--------------------

与 ``having()`` 相同，只是用 **OR** 分隔多个子句。

$builder->havingIn()
--------------------

生成一个 **HAVING field IN ('item', 'item')** SQL 查询，在适当时用 **AND** 连接：

.. literalinclude:: query_builder/051.php

可以使用子查询代替值数组：

.. literalinclude:: query_builder/052.php

$builder->orHavingIn()
----------------------

生成一个 **HAVING field IN ('item', 'item')** SQL 查询，在适当时用 **OR** 连接：

.. literalinclude:: query_builder/053.php

可以使用子查询代替值数组：

.. literalinclude:: query_builder/054.php

$builder->havingNotIn()
-----------------------

生成一个 **HAVING field NOT IN ('item', 'item')** SQL 查询，在适当时用 **AND** 连接：

.. literalinclude:: query_builder/055.php

可以使用子查询代替值数组：

.. literalinclude:: query_builder/056.php

$builder->orHavingNotIn()
-------------------------

生成一个 **HAVING field NOT IN ('item', 'item')** SQL 查询，在适当时用 **OR** 连接：

.. literalinclude:: query_builder/057.php

可以使用子查询代替值数组：

.. literalinclude:: query_builder/058.php

$builder->havingLike()
----------------------

此方法允许为查询的 **HAVING** 部分生成 **LIKE** 子句，用于执行搜索。

.. note:: 传递给此方法的所有值都会自动转义。

.. note:: 所有 ``havingLike*()`` 方法变体可以通过向方法传递第五个参数 ``true`` 来强制执行不区分大小写的搜索。这将使用平台特定的功能（如果可用），否则将强制值为小写，即 ``HAVING LOWER(column) LIKE '%search%'``。这可能需要为 ``LOWER(column)`` 而不是 ``column`` 创建索引才能有效。

1. 简单键/值方式
^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. literalinclude:: query_builder/059.php

    如果使用多个方法调用，它们将用 **AND** 连接在一起：

    .. literalinclude:: query_builder/060.php

    如果想控制通配符（**%**）放置的位置，可以使用可选的第三个参数。选项有 ``before``、``after`` 和 ``both`` （默认）。

    .. literalinclude:: query_builder/061.php

2. 关联数组方式
^^^^^^^^^^^^^^^^^^^^^^^^^^^

       .. literalinclude:: query_builder/062.php

$builder->orHavingLike()
------------------------

此方法与上述方法相同，只是多个实例通过 **OR** 连接：

.. literalinclude:: query_builder/063.php

$builder->notHavingLike()
-------------------------

此方法与 ``havingLike()`` 相同，只是它生成 **NOT LIKE** 语句：

.. literalinclude:: query_builder/064.php

$builder->orNotHavingLike()
---------------------------

此方法与 ``notHavingLike()`` 相同，只是多个实例通过 **OR** 连接：

.. literalinclude:: query_builder/065.php

****************
排序结果
****************

OrderBy
=======

$builder->orderBy()
-------------------

允许设置 **ORDER BY** 子句。

第一个参数包含要排序的字段名。

第二个参数允许设置结果的排序方式。
选项有 ``ASC``、``DESC`` 和 ``RANDOM``。

.. literalinclude:: query_builder/066.php

也可以在第一个参数中传递自己的字符串：

.. literalinclude:: query_builder/067.php

如果需要多个字段，可以进行多次方法调用。

.. literalinclude:: query_builder/068.php

如果选择 ``RANDOM`` 方向选项，则将忽略第一个参数，除非指定数字种子值。

.. literalinclude:: query_builder/069.php

****************************
限制或计数结果
****************************

Limit
=====

$builder->limit()
-----------------

允许限制查询返回的行数：

.. literalinclude:: query_builder/070.php

.. note:: 如果在 SQL 语句中指定 ``LIMIT 0``，将返回 0 条记录。
  然而，查询构建器中有一个错误，如果指定 ``limit(0)``，
  生成的 SQL 语句将没有 ``LIMIT`` 子句，所有记录都将被返回。为了修复此错误行为，在 v4.5.0 中添加了一个设置。参见
  :ref:`v450-query-builder-limit-0-behavior` 了解详细信息。此错误行为将在未来版本中修复，因此建议更改默认设置。

第二个参数允许设置结果偏移量。

.. literalinclude:: query_builder/071.php

$builder->countAllResults()
---------------------------

允许确定特定查询构建器查询中的行数。支持查询构建器的限制条件，如 ``where()``、``orWhere()``、``like()``、``orLike()`` 等。示例：

.. literalinclude:: query_builder/072.php

然而，此方法还会重置你可能已传递给 ``select()`` 的任何字段值。如果需要保留它们，可以将 ``false`` 作为第一个参数传递。

.. literalinclude:: query_builder/073.php

$builder->countAll()
--------------------

允许确定特定表中的行数。示例：

.. literalinclude:: query_builder/074.php

与 ``countAllResult()`` 方法一样，此方法也会重置你可能已传递给 ``select()`` 的字段值。如果需要保留它们，可以将 ``false`` 作为第一个参数传递。

.. _query-builder-union:

*************
联合查询
*************

Union
=====

$builder->union()
-----------------

用于组合两个或多个 SELECT 语句的结果集。它将只返回唯一的结果。

.. literalinclude:: query_builder/103.php

.. note:: 为了与 DBMS（如 MSSQL 和 Oracle）正常工作，查询被包装在 ``SELECT * FROM ( ... ) alias`` 中。
    主查询将始终具有别名 ``uwrp0``。通过 ``union()`` 添加的每个后续查询将具有别名 ``uwrpN+1``。

所有联合查询都将在主查询之后添加，无论 ``union()`` 方法的调用顺序如何。
也就是说，``limit()`` 或 ``orderBy()`` 方法将相对于主查询，即使在 ``union()`` 之后调用也是如此。

在某些情况下，可能需要对查询结果进行排序或限制记录数。
解决方案是使用通过 ``$db->newQuery()`` 创建的包装器。
在下面的示例中，我们获取前 5 个用户 + 最后 5 个用户，并按 id 对结果进行排序：

.. literalinclude:: query_builder/104.php

$builder->unionAll()
--------------------

行为与 ``union()`` 方法相同。然而，将返回所有结果，而不仅仅是唯一的结果。

**************
查询分组
**************

Group
=====

查询分组允许通过将 **WHERE** 子句括在括号中来创建 **WHERE** 子句组。这样就可以创建具有复杂 **WHERE** 子句的查询。支持嵌套分组。示例：

.. literalinclude:: query_builder/075.php

.. note:: 分组需要平衡，确保每个 ``groupStart()`` 都有对应的 ``groupEnd()``。

$builder->groupStart()
----------------------

通过向查询的 **WHERE** 子句添加左括号来开始新组。

$builder->orGroupStart()
------------------------

通过向查询的 **WHERE** 子句添加左括号来开始新分组，前缀为 **OR**。

$builder->notGroupStart()
-------------------------

通过向查询的 **WHERE** 子句添加左括号来开始新分组，前缀为 **NOT**。

$builder->orNotGroupStart()
---------------------------

通过向查询的 **WHERE** 子句添加左括号来开始新分组，前缀为 **OR NOT**。

$builder->groupEnd()
--------------------

通过向查询的 **WHERE** 子句添加右括号来结束当前组。

$builder->havingGroupStart()
----------------------------

通过向查询的 **HAVING** 子句添加左括号来开始新组。

$builder->orHavingGroupStart()
------------------------------

通过向查询的 **HAVING** 子句添加左括号来开始新分组，前缀为 **OR**。

$builder->notHavingGroupStart()
-------------------------------

通过向查询的 **HAVING** 子句添加左括号来开始新分组，前缀为 **NOT**。

$builder->orNotHavingGroupStart()
---------------------------------

通过向查询的 **HAVING** 子句添加左括号来开始新分组，前缀为 **OR NOT**。

$builder->havingGroupEnd()
--------------------------

通过向查询的 **HAVING** 子句添加右括号来结束当前分组。

**************
插入数据
**************

插入
======

$builder->insert()
------------------

根据提供的数据生成插入字符串并运行查询。可以向方法传递 **数组** 或 **对象**。以下是使用数组的示例：

.. literalinclude:: query_builder/076.php

第一个参数是值的关联数组。

.. note:: 除 ``RawSql`` 外的所有值都会自动转义，生成更安全的查询。

.. warning:: 使用 ``RawSql`` 时，必须手动转义数据。否则可能导致 SQL 注入。

以下是使用对象的示例：

.. literalinclude:: query_builder/077.php

.. literalinclude:: query_builder/121.php

第一个参数是对象。

$builder->ignore()
------------------

根据提供的数据生成插入忽略字符串并运行查询。如果已存在具有相同主键的条目，则不会插入该查询。
可以选择向方法传递 **布尔值**。也可以用于 **insertBatch**、**update** 和 **delete** （在支持时）。
以下是使用上述示例数组的示例：

.. literalinclude:: query_builder/078.php

$builder->getCompiledInsert()
-----------------------------

像 ``$builder->insert()`` 一样编译插入查询，但不 *运行* 查询。此方法只是将 SQL 查询作为字符串返回。

示例：

.. literalinclude:: query_builder/079.php

第一个参数允许设置是否重置查询构建器查询
（默认情况下它会像 ``$builder->insert()`` 一样被重置）：

.. literalinclude:: query_builder/080.php

第二个查询有效的原因是第一个参数设置为 ``false``。

.. note:: 此方法不适用于批量插入。

.. _insert-batch-data:

insertBatch
===========

$builder->insertBatch()
-----------------------

从数据插入
^^^^^^^^^^^^^^^^

根据提供的数据生成插入字符串并运行查询。可以向方法传递 **数组** 或 **对象**。以下是使用数组的示例：

.. literalinclude:: query_builder/081.php

第一个参数是值的关联数组。

.. note:: 除 ``RawSql`` 外的所有值都会自动转义，生成更安全的查询。

.. warning:: 使用 ``RawSql`` 时，必须手动转义数据。否则可能导致 SQL 注入。

从查询插入
^^^^^^^^^^^^^^^^^^^

也可以从查询插入：

.. literalinclude:: query_builder/117.php

.. note:: 从 v4.3.0 开始可以使用 ``setQueryAsData()``。

.. note:: 需要为选择查询的字段设置别名以匹配目标表的字段。

.. _upsert-data:

**************
Upsert 数据
**************

Upsert
======

$builder->upsert()
------------------

.. versionadded:: 4.3.0

根据提供的数据生成 upsert 字符串并运行查询。可以向方法传递 **数组** 或 **对象**。默认情况下，约束将按顺序定义。将首先选择主键，然后选择唯一键。MySQL 默认将使用任何约束。以下是使用数组的示例：

.. literalinclude:: query_builder/112.php

.. note:: 对于 MySQL 之外的数据库，如果表有多个键（主键或唯一键），
    在处理约束时默认将优先考虑主键。如果希望
    使用不同的唯一键而不是主键，请使用 ``onConstraint()`` 方法。

第一个参数是值的关联数组。

以下是使用对象的示例：

.. literalinclude:: query_builder/122.php

.. literalinclude:: query_builder/113.php

第一个参数是对象。

.. note:: 所有值都会自动转义，生成更安全的查询。

$builder->getCompiledUpsert()
-----------------------------

.. versionadded:: 4.3.0

像 ``$builder->upsert()`` 一样编译 upsert 查询，但不 *运行* 查询。此方法只是将 SQL 查询作为字符串返回。

示例：

.. literalinclude:: query_builder/114.php

.. note:: 此方法不适用于批量 upsert。

upsertBatch
===========

$builder->upsertBatch()
-----------------------

.. versionadded:: 4.3.0

从数据 Upsert
^^^^^^^^^^^^^^^^

根据提供的数据生成 upsert 字符串并运行查询。可以向方法传递 **数组** 或 **对象**。默认情况下，约束将按顺序定义。将首先选择主键，然后选择唯一键。MySQL 默认将使用任何约束。

以下是使用数组的示例：

.. literalinclude:: query_builder/108.php

第一个参数是值的关联数组。

.. note:: 所有值都会自动转义，生成更安全的查询。

从查询 Upsert
^^^^^^^^^^^^^^^^^^^

也可以从查询进行 upsert：

.. literalinclude:: query_builder/115.php

.. note:: 从 v4.3.0 开始可以使用 ``setQueryAsData()``、``onConstraint()`` 和 ``updateFields()``
    方法。

.. note:: 需要为选择查询的字段设置别名以匹配目标表的字段。

$builder->onConstraint()
------------------------

.. versionadded:: 4.3.0

允许手动设置用于 upsert 的约束。这不适用于 MySQL，因为 MySQL 默认检查所有约束。

.. literalinclude:: query_builder/109.php

此方法接受字符串或字段数组。

$builder->updateFields()
------------------------

.. versionadded:: 4.3.0

允许手动设置执行 upsert 时要更新的字段。

.. literalinclude:: query_builder/110.php

此方法接受字符串、字段数组或 RawSql。还可以指定要更新的额外字段，该字段不包含在数据集中。
可以通过将第二个参数设置为 ``true`` 来完成此操作。

.. literalinclude:: query_builder/111.php

注意，``updated_at`` 字段未插入，但在更新时使用。

*************
更新数据
*************

更新
======

$builder->replace()
-------------------

此方法执行 **REPLACE** 语句，这基本上是 SQL
标准中的（可选） **DELETE** + **INSERT**，使用 *主键* 和 *唯一键*
作为决定条件。
在我们的情况下，它将使你无需实现复杂的
逻辑，无需使用 ``select()``、``update()``、
``delete()`` 和 ``insert()`` 调用的各种组合。

示例：

.. literalinclude:: query_builder/082.php

在上述示例中，如果我们假设 ``title`` 字段是主键，
那么如果一行包含 ``My title`` 作为 ``title`` 值，该行将被删除，
我们的新行数据将替换它。

也允许使用 ``set()`` 方法，所有值都会自动转义，就像使用 ``insert()`` 一样。

$builder->set()
---------------

此方法允许为插入或更新设置值。

**它可以用来代替直接向 insert() 或 update() 方法传递数据数组：**

.. literalinclude:: query_builder/083.php

如果使用多个方法调用，它们将根据你是执行插入还是更新来正确组装：

.. literalinclude:: query_builder/084.php

``set()`` 还将接受可选的第三个参数（``$escape``），如果设置为 ``false``，将防止值被转义。为了说明区别，以下是使用和不使用转义参数的 ``set()``。

.. literalinclude:: query_builder/085.php

也可以向此方法传递关联数组：

.. literalinclude:: query_builder/086.php

或对象：

.. literalinclude:: query_builder/077.php

.. literalinclude:: query_builder/087.php

$builder->update()
------------------

生成 update 字符串并根据提供的数据运行查询。可以向方法传递 **数组** 或 **对象**。以下是使用数组的示例：

.. literalinclude:: query_builder/088.php

或可以提供对象：

.. literalinclude:: query_builder/077.php

.. literalinclude:: query_builder/089.php

.. note:: 除 ``RawSql`` 外的所有值都会自动转义，生成更安全的查询。

.. warning:: 使用 ``RawSql`` 时，必须手动转义数据。否则可能导致 SQL 注入。

你会注意到使用了 ``$builder->where()`` 方法，允许设置 **WHERE** 子句。可以选择将此信息直接作为字符串传递到 ``update()`` 方法中：

.. literalinclude:: query_builder/090.php

或作为数组：

.. literalinclude:: query_builder/091.php

执行更新时也可以使用上述的 ``$builder->set()`` 方法。

$builder->getCompiledUpdate()
-----------------------------

这与 ``$builder->getCompiledInsert()`` 的工作方式完全相同，只是它生成 **UPDATE** SQL 字符串而不是 **INSERT** SQL 字符串。

有关更多信息，请查看 `$builder->getCompiledInsert()`_ 的文档。

.. note:: 此方法不适用于批量更新。

.. _update-batch:

UpdateBatch
===========

$builder->updateBatch()
-----------------------

.. note:: 从 v4.3.0 开始，``updateBatch()`` 的第二个参数 ``$index`` 已
    更改为 ``$constraints``。它现在接受数组、字符串或 ``RawSql`` 类型。

从数据更新
^^^^^^^^^^^^^^^^

根据提供的数据生成 update 字符串并运行查询。可以向方法传递 **数组** 或 **对象**。以下是使用数组的示例：

.. literalinclude:: query_builder/092.php

第一个参数是值的关联数组，第二个参数是 where 键。

.. note:: 从 v4.3.0 开始，生成的 SQL 结构已得到改进。

从 v4.3.0 开始，还可以使用 ``onConstraint()`` 和 ``updateFields()`` 方法：

.. literalinclude:: query_builder/120.php

.. note:: 除 ``RawSql`` 外的所有值都会自动转义，生成更安全的查询。

.. warning:: 使用 ``RawSql`` 时，必须手动转义数据。否则可能导致 SQL 注入。

.. note:: 因为工作原理的原因，若使用此方法则 ``affectedRows()`` 无法提供正确的结果。相反，``updateBatch()`` 返回受影响的行数。

从查询更新
^^^^^^^^^^^^^^^^^^^

从 v4.3.0 开始，还可以使用 ``setQueryAsData()`` 方法从查询更新：

.. literalinclude:: query_builder/116.php

.. note:: 需要为 select 查询的字段设置别名以匹配目标表的字段。

*************
删除数据
*************

删除
======

$builder->delete()
------------------

生成 **DELETE** SQL 字符串并运行查询。

.. literalinclude:: query_builder/093.php

第一个参数是 where 子句。
也可以使用 ``where()`` 或 ``orWhere()`` 方法，而不是将数据传递给方法的第一个参数：

.. literalinclude:: query_builder/094.php

如果要删除表中的所有数据，可以使用 ``truncate()`` 方法或 ``emptyTable()``。

$builder->getCompiledDelete()
-----------------------------

这与 ``$builder->getCompiledInsert()`` 的工作方式完全相同，只是它生成 **DELETE** SQL 字符串而不是 **INSERT** SQL 字符串。

有关更多信息，请查看 `$builder->getCompiledInsert()`_ 的文档。

.. _delete-batch:

DeleteBatch
===========

$builder->deleteBatch()
-----------------------

.. versionadded:: 4.3.0

从数据删除
^^^^^^^^^^^^^^^^

基于一组数据生成批量 **DELETE** 语句。

.. literalinclude:: query_builder/118.php

此方法在删除具有复合主键的表中的数据时可能特别有用。

.. note:: SQLite3 不支持使用 ``where()``。

从查询删除
^^^^^^^^^^^^^^^^^^^

也可以从查询删除：

.. literalinclude:: query_builder/119.php

$builder->emptyTable()
----------------------

生成 **DELETE** SQL 字符串并运行查询：

.. literalinclude:: query_builder/095.php

$builder->truncate()
--------------------

生成 **TRUNCATE** SQL 字符串并运行查询。

.. literalinclude:: query_builder/096.php

.. note:: 如果 TRUNCATE 命令不可用，``truncate()`` 将执行为 "DELETE FROM table"。

**********************
条件语句
**********************

.. _db-builder-when:

When
====

$builder->when()
----------------

.. versionadded:: 4.3.0

这允许基于条件修改查询，而无需中断查询构建器链。第一个参数是条件，它使用 PHP 的原生布尔逻辑进行评估——这意味着像 ``false``、``null``、
``0``、``'0'``、``0.0``、空字符串 ``''`` 和空数组 ``[]`` 这样的值将被视为 false。
第二个参数是在条件为 true 时将运行的回调函数。

例如，你可能只希望根据 HTTP 请求中发送的值应用给定的 WHERE 语句：

.. literalinclude:: query_builder/105.php

由于条件被评估为 ``true``，将调用回调函数。条件中设置的值将作为第二个参数传递给回调函数，以便在查询中使用。

有时你可能希望在条件评估为 false 时应用不同的语句。
这可以通过提供第二个闭包来实现：

.. literalinclude:: query_builder/106.php

WhenNot
=======

$builder->whenNot()
-------------------

.. versionadded:: 4.3.0

这与 ``$builder->when()`` 的工作方式完全相同，只是它只会在条件评估为 ``false`` 时运行回调函数，而不是像 ``when()`` 那样在 ``true`` 时运行。

.. literalinclude:: query_builder/107.php

***************
方法链
***************

方法链允许通过连接多个方法来简化语法。考虑此示例：

.. literalinclude:: query_builder/097.php

.. _ar-caching:

***********************
重置查询构建器
***********************

ResetQuery
==========

$builder->resetQuery()
----------------------

重置查询构建器允许在不先使用 ``$builder->get()`` 或 ``$builder->insert()`` 等方法执行查询的情况下重新开始。

这在以下情况下很有用：使用查询构建器生成 SQL
（例如，``$builder->getCompiledSelect()``），但之后选择运行查询：

.. literalinclude:: query_builder/098.php

***************
类参考
***************

.. php:namespace:: CodeIgniter\Database

.. php:class:: BaseBuilder

    .. php:method:: db()

        :returns:   正在使用的数据库连接
        :rtype:     ``ConnectionInterface``

        从 ``$db`` 返回当前数据库连接。用于访问查询构建器无法直接使用的
        ``ConnectionInterface`` 方法，如 ``insertID()`` 或 ``errors()``。

    .. php:method:: resetQuery()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        重置当前查询构建器状态。当你想构建一个在某些条件下可以取消的查询时很有用。

    .. php:method:: countAllResults([$reset = true])

        :param bool $reset: 是否重置 SELECT 的值
        :returns:   查询结果中的行数
        :rtype:     int

        生成特定于平台的查询字符串，用于计算查询构建器查询返回的所有记录数。

    .. php:method:: countAll([$reset = true])

        :param bool $reset: 是否重置 SELECT 的值
        :returns:   查询结果中的行数
        :rtype:     int

        生成特定于平台的查询字符串，用于计算特定表中的所有记录数。

    .. php:method:: get([$limit = null[, $offset = null[, $reset = true]]]])

        :param int $limit: LIMIT 子句
        :param int $offset: OFFSET 子句
        :param bool $reset: 是否要清除查询构建器的值？
        :returns: ``\CodeIgniter\Database\ResultInterface`` 实例（方法链）
        :rtype:    ``\CodeIgniter\Database\ResultInterface``

        根据已调用的查询构建器方法编译并运行 ``SELECT`` 语句。

    .. php:method:: getWhere([$where = null[, $limit = null[, $offset = null[, $reset = true]]]]])

        :param string $where: WHERE 子句
        :param int $limit: LIMIT 子句
        :param int $offset: OFFSET 子句
        :param bool $reset: 是否要清除查询构建器的值？
        :returns:   ``\CodeIgniter\Database\ResultInterface`` 实例（方法链）
        :rtype:     ``\CodeIgniter\Database\ResultInterface``

        与 ``get()`` 相同，但还允许直接添加 WHERE 子句。

    .. php:method:: select([$select = '*'[, $escape = null]])

        :param array|RawSql|string $select: 查询的 SELECT 部分
        :param bool $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``SELECT`` 子句。

    .. php:method:: selectAvg([$select = ''[, $alias = '']])

        :param string $select: 要计算平均值的字段
        :param string $alias: 结果值名称的别名
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``SELECT AVG(field)`` 子句。

    .. php:method:: selectMax([$select = ''[, $alias = '']])

        :param string $select: 要计算最大值的字段
        :param string $alias: 结果值名称的别名
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``SELECT MAX(field)`` 子句。

    .. php:method:: selectMin([$select = ''[, $alias = '']])

        :param string $select: 要计算最小值的字段
        :param string $alias: 结果值名称的别名
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``SELECT MIN(field)`` 子句。

    .. php:method:: selectSum([$select = ''[, $alias = '']])

        :param string $select: 要计算总和的字段
        :param string $alias: 结果值名称的别名
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``SELECT SUM(field)`` 子句。

    .. php:method:: selectCount([$select = ''[, $alias = '']])

        :param string $select: 要计算平均值的字段
        :param string $alias: 结果值名称的别名
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``SELECT COUNT(field)`` 子句。

    .. php:method:: selectSubquery(BaseBuilder $subquery, string $as)

        :param string $subquery: BaseBuilder 实例
        :param string $as: 结果值名称的别名
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向选择中添加子查询。

    .. php:method:: distinct([$val = true])

        :param bool $val: "distinct" 标志的期望值
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        设置一个标志，告诉查询构建器向查询的 ``SELECT`` 部分添加
        ``DISTINCT`` 子句。

    .. php:method:: from($from[, $overwrite = false])

        :param mixed $from: 表名；字符串或数组
        :param bool    $overwrite: 是否移除现有的第一个表？
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        指定查询的 ``FROM`` 子句。

    .. php:method:: fromSubquery($from, $alias)

        :param BaseBuilder $from: BaseBuilder 类的实例
        :param string      $alias: 子查询别名
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        使用子查询指定查询的 ``FROM`` 子句。

    .. php:method:: setQueryAsData($query[, $alias[, $columns = null]])

        .. versionadded:: 4.3.0

        :param BaseBuilder|RawSql $query: BaseBuilder 或 RawSql 的实例
        :param string|null $alias: 查询的别名
        :param array|string|null $columns: 查询中字段的数组或逗号分隔的字符串
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        将查询设置为 ``insertBatch()``、``updateBatch()``、``upsertBatch()`` 的数据源。
        如果 ``$columns`` 为 null，则将运行查询以生成字段名。

    .. php:method:: join($table, $cond[, $type = ''[, $escape = null]])

        :param string $table: 要连接的表名
        :param string|RawSql $cond: JOIN ON 条件
        :param string $type: JOIN 类型
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``JOIN`` 子句。从 v4.2.0 开始，``RawSql`` 可以用作
        JOIN ON 条件。另请参见 :ref:`query-builder-join`。

    .. php:method:: where($key[, $value = null[, $escape = null]])

        :param array|RawSql|string $key: 要比较的字段名，或关联数组
        :param mixed $value: 如果是单个键，则与此值比较
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成查询的 ``WHERE`` 部分。用 ``AND`` 分隔多个调用。

    .. php:method:: orWhere($key[, $value = null[, $escape = null]])

        :param mixed $key: 要比较的字段名，或关联数组
        :param mixed $value: 如果是单个键，则与此值比较
        :param bool $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成查询的 ``WHERE`` 部分。用 ``OR`` 分隔多个调用。

    .. php:method:: orWhereIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要搜索的字段
        :param array|BaseBulder|Closure $values: 目标值数组，或用于子查询的匿名函数
        :param bool $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成 ``WHERE`` 字段 ``IN('item', 'item')`` SQL 查询，在适当时用 ``OR`` 连接。

    .. php:method:: orWhereNotIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要搜索的字段
        :param array|BaseBulder|Closure $values: 目标值数组，或用于子查询的匿名函数
        :param bool $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成 ``WHERE`` 字段 ``NOT IN('item', 'item')`` SQL 查询，在适当时用 ``OR`` 连接。

    .. php:method:: whereIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要检查的字段名
        :param array|BaseBulder|Closure $values: 目标值数组，或用于子查询的匿名函数
        :param bool $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成 ``WHERE`` 字段 ``IN('item', 'item')`` SQL 查询，在适当时用 ``AND`` 连接。

    .. php:method:: whereNotIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要检查的字段名
        :param array|BaseBulder|Closure $values: 目标值数组，或用于子查询的匿名函数
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成 ``WHERE`` 字段 ``NOT IN('item', 'item')`` SQL 查询，在适当时用 ``AND`` 连接。

    .. php:method:: groupStart()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        开始一个组表达式，对其内部的条件使用 ``AND``。

    .. php:method:: orGroupStart()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        开始一个组表达式，对其内部的条件使用 ``OR``。

    .. php:method:: notGroupStart()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        开始一个组表达式，对其内部的条件使用 ``AND NOT``。

    .. php:method:: orNotGroupStart()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        开始一个组表达式，对其内部的条件使用 ``OR NOT``。

    .. php:method:: groupEnd()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        结束一个组表达式。

    .. php:method:: like($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param array|RawSql|string $field: 字段名
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制执行不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``LIKE`` 子句，用 ``AND`` 分隔多个调用。

    .. php:method:: orLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制执行不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``LIKE`` 子句，用 ``OR`` 分隔多个调用。

    .. php:method:: notLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制执行不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``NOT LIKE`` 子句，用 ``AND`` 分隔多个调用。

    .. php:method:: orNotLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制执行不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``NOT LIKE`` 子句，用 ``OR`` 分隔多个调用。

    .. php:method:: having($key[, $value = null[, $escape = null]])

        :param mixed $key: 标识符（字符串）或字段/值对的关联数组
        :param string $value: 如果 $key 是标识符，则为要查找的值
        :param string $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``HAVING`` 子句，用 ``AND`` 分隔多个调用。

    .. php:method:: orHaving($key[, $value = null[, $escape = null]])

        :param mixed $key: 标识符（字符串）或字段/值对的关联数组
        :param string $value: 如果 $key 是标识符，则为要查找的值
        :param string $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``HAVING`` 子句，用 ``OR`` 分隔多个调用。

    .. php:method:: orHavingIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要搜索的字段
        :param array|BaseBulder|Closure $values: 目标值数组，或用于子查询的匿名函数
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成 ``HAVING`` 字段 IN('item', 'item') SQL 查询，在适当时用 ``OR`` 连接。

    .. php:method:: orHavingNotIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要搜索的字段
        :param array|BaseBulder|Closure $values: 目标值数组，或用于子查询的匿名函数
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成 ``HAVING`` 字段 ``NOT IN('item', 'item')`` SQL 查询，在适当时用 ``OR`` 连接。

    .. php:method:: havingIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要检查的字段名
        :param array|BaseBulder|Closure $values: 目标值数组，或用于子查询的匿名函数
        :param bool $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成 ``HAVING`` 字段 ``IN('item', 'item')`` SQL 查询，在适当时用 ``AND`` 连接。

    .. php:method:: havingNotIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要检查的字段名
        :param array|BaseBulder|Closure $values: 目标值数组，或用于子查询的匿名函数
        :param bool $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制执行不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成 ``HAVING`` 字段 ``NOT IN('item', 'item')`` SQL 查询，在适当时用 ``AND`` 连接。

    .. php:method:: havingLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制执行不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询的 ``HAVING`` 部分添加 ``LIKE`` 子句，用 ``AND`` 分隔多个调用。

    .. php:method:: orHavingLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制执行不区分大小写的搜索
        :returns: ``BaseBuilder`` 实例（方法链）
        :rtype:    ``BaseBuilder``

        向查询的 ``HAVING`` 部分添加 ``LIKE`` 子句，用 ``OR`` 分隔多个调用。

    .. php:method:: notHavingLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制执行不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询的 ``HAVING`` 部分添加 ``NOT LIKE`` 子句，用 ``AND`` 分隔多个调用。

    .. php:method:: orNotHavingLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询的 ``HAVING`` 部分添加 ``NOT LIKE`` 子句，用 ``OR`` 分隔多个调用。

    .. php:method:: havingGroupStart()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        开始 ``HAVING`` 子句的组表达式，对其内部的条件使用 ``AND``。

    .. php:method:: orHavingGroupStart()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        开始 ``HAVING`` 子句的组表达式，对其内部的条件使用 ``OR``。

    .. php:method:: notHavingGroupStart()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        开始 ``HAVING`` 子句的组表达式，对其内部的条件使用 ``AND NOT``。

    .. php:method:: orNotHavingGroupStart()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        开始 ``HAVING`` 子句的组表达式，对其内部的条件使用 ``OR NOT``。

    .. php:method:: havingGroupEnd()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        结束 ``HAVING`` 子句的组表达式。

    .. php:method:: groupBy($by[, $escape = null])

        :param mixed $by: 要分组的字段；字符串或数组
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``GROUP BY`` 子句。

    .. php:method:: orderBy($orderby[, $direction = ''[, $escape = null]])

        :param string $orderby: 要排序的字段
        :param string $direction: 请求的排序顺序 - ASC、DESC 或 random
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``ORDER BY`` 子句。

    .. php:method:: limit($value[, $offset = 0])

        :param int $value: 要限制结果的行数
        :param int $offset: 要跳过的行数
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``LIMIT`` 和 ``OFFSET`` 子句。

    .. php:method:: offset($offset)

        :param int $offset: 要跳过的行数
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``OFFSET`` 子句。

    .. php:method:: union($union)

        :param BaseBulder|Closure $union: 联合查询
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        添加 ``UNION`` 子句。

    .. php:method:: unionAll($union)

        :param BaseBulder|Closure $union: 联合查询
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        添加 ``UNION ALL`` 子句。

    .. php:method:: set($key[, $value = ''[, $escape = null]])

        :param mixed $key: 字段名，或字段/值对的数组
        :param mixed $value: 字段值，如果 $key 是单个字段
        :param bool    $escape: 是否转义值
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        添加字段/值对，稍后传递给 ``insert()``、``update()`` 或 ``replace()``。

    .. php:method:: insert([$set = null[, $escape = null]])

        :param array $set: 字段/值对的关联数组
        :param bool $escape: 是否转义值
        :returns:   成功时返回 ``true``，失败时返回 ``false``
        :rtype:     bool

        编译并执行 ``INSERT`` 语句。

    .. php:method:: insertBatch([$set = null[, $escape = null[, $batch_size = 100]]])

        :param array $set: 要插入的数据
        :param bool $escape: 是否转义值
        :param int $batch_size: 一次插入的行数
        :returns: 插入的行数，如果没有数据执行插入操作则返回 ``false``
        :rtype:    int|false

        编译并执行批量 ``INSERT`` 语句。

        .. note:: 当提供超过 ``$batch_size`` 行时，将执行多个
            ``INSERT`` 查询，每个查询尝试插入
            最多 ``$batch_size`` 行。

    .. php:method:: setInsertBatch($key[, $value = ''[, $escape = null]])

        .. deprecated:: 4.3.0
           使用 :php:meth:`CodeIgniter\\Database\\BaseBuilder::setData()` 代替。

        :param mixed $key: 字段名或字段/值对的数组
        :param string $value: 字段值，如果 $key 是单个字段
        :param bool $escape: 是否转义值
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        添加字段/值对，稍后通过 ``insertBatch()`` 插入到表中。

        .. important:: 此方法已弃用。将在未来版本中删除。

    .. php:method:: upsert([$set = null[, $escape = null]])

        :param array $set: 字段/值对的关联数组
        :param bool $escape: 是否转义值
        :returns:   成功时返回 ``true``，失败时返回 ``false``
        :rtype:     bool

        编译并执行 ``UPSERT`` 语句。

    .. php:method:: upsertBatch([$set = null[, $escape = null[, $batch_size = 100]]])

        :param array $set: 要 upsert 的数据
        :param bool $escape: 是否转义值
        :param int $batch_size: 一次 upsert 的行数
        :returns: upsert 的行数，失败时返回 ``false``
        :rtype:    int|false

        编译并执行批量 ``UPSERT`` 语句。

        .. note:: MySQL 使用 ``ON DUPLICATE KEY UPDATE``，每行的受影响行数值
            如果行作为新行插入则为 1，如果现有行被更新则为 2，
            如果现有行被设置为其当前值则为 0。

        .. note:: 当提供超过 ``$batch_size`` 行时，将执行多个
            ``UPSERT`` 查询，每个查询尝试 upsert
            最多 ``$batch_size`` 行。

    .. php:method:: update([$set = null[, $where = null[, $limit = null]]])

        :param array $set: 字段/值对的关联数组
        :param string $where: WHERE 子句
        :param int $limit: LIMIT 子句
        :returns:   成功时返回 ``true``，失败时返回 ``false``
        :rtype:     bool

        编译并执行 ``UPDATE`` 语句。

    .. php:method:: updateBatch([$set = null[, $constraints = null[, $batchSize = 100]]])

        :param array|object|null $set: 字段名，或字段/值对的关联数组
        :param array|RawSql|string|null $constraints: 用作更新键的字段或字段
        :param int $batchSize: 在单个查询中分组的条件数
        :returns:   更新的行数，失败时返回 ``false``
        :rtype:     int|false

        .. note:: 从 v4.3.0 开始，参数 ``$set`` 和 ``$constraints`` 的类型已更改。

        编译并执行批量 ``UPDATE`` 语句。
        ``$constraints`` 参数接受逗号分隔的字段字符串、数组、关联数组或 ``RawSql``。

        .. note:: 当提供超过 ``$batchSize`` 个字段/值对时，
             将执行多个查询，每个查询处理最多 ``$batchSize``
             个字段/值对。如果我们将 ``$batchSize`` 设置为 0，
             则所有字段/值对将在一个查询中执行。

    .. php:method:: updateFields($set, [$addToDefault = false, [$ignore = null]])

        .. versionadded:: 4.3.0

        :param mixed $set: 行或行数组，行是数组或对象
        :param bool $addToDefault: 添加比数据集中更多的字段
        :param bool $ignore: 从 $set 中忽略的字段数组
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        与 ``updateBatch()`` 和 ``upsertBatch()`` 方法一起使用。这定义了将被更新的字段。

    .. php:method:: onConstraint($set)

        .. versionadded:: 4.3.0

        :param mixed $set: 用作键或约束的字段或字段集
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        与 ``updateBatch()`` 和 ``upsertBatch()`` 方法一起使用。这接受逗号分隔的字段字符串、数组、关联数组或 RawSql。

    .. php:method:: setData($set, [$escape = null, [$alias = '']])

        .. versionadded:: 4.3.0

        :param mixed $set: 行或行数组，行是数组或对象
        :param bool $escape: 是否转义值
        :param bool $alias: 数据集的表别名
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        用于 ``*Batch()`` 方法设置插入、更新、upsert 的数据。

    .. php:method:: setUpdateBatch($key[, $value = ''[, $escape = null]])

        .. deprecated:: 4.3.0
           使用 :php:meth:`CodeIgniter\\Database\\BaseBuilder::setData()` 代替。

        :param mixed $key: 字段名或字段/值对的数组
        :param string $value: 字段值，如果 $key 是单个字段
        :param bool    $escape: 是否转义值
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        添加字段/值对，稍后通过 ``updateBatch()`` 更新表中的数据。

        .. important:: 此方法已弃用。将在未来版本中删除。

    .. php:method:: replace([$set = null])

        :param array $set: 字段/值对的关联数组
        :returns: 成功时返回 ``true``，失败时返回 ``false``
        :rtype:    bool

        编译并执行 ``REPLACE`` 语句。

    .. php:method:: delete([$where = ''[, $limit = null[, $reset_data = true]]])

        :param string $where: WHERE 子句
        :param int $limit: LIMIT 子句
        :param bool $reset_data: 是否重置查询的"写入"子句
        :returns:   ``BaseBuilder`` 实例（方法链）或失败时返回 ``false``
        :rtype:     ``BaseBuilder|false``

        编译并执行 ``DELETE`` 查询。

    .. php:method:: deleteBatch([$set = null[, $constraints = null[, $batchSize = 100]]])

        :param array|object|null $set: 字段名，或字段/值对的关联数组
        :param array|RawSql|string|null $constraints: 用作删除键的字段或字段
        :param int $batchSize: 在单个查询中分组的条件数
        :returns:   删除的行数，失败时返回 ``false``
        :rtype:     int|false

        编译并执行批量 ``DELETE`` 查询。

    .. php:method:: increment($column[, $value = 1])

        :param string $column: 要递增的字段名
        :param int $value: 字段中递增的数量

        将字段的值按指定数量递增。如果字段
        不是数字字段，如 ``VARCHAR``，它可能会被替换
        为 ``$value``。

    .. php:method:: decrement($column[, $value = 1])

        :param string $column: 要递减的字段名
        :param int $value:  递减的数量

        将字段的值按指定数量递减。如果字段
        不是数字字段，如 ``VARCHAR``，它可能会被替换
        为 ``$value``。

    .. php:method:: truncate()

        :returns:   成功时返回 ``true``，失败时返回 ``false``，测试模式下返回字符串
        :rtype:     bool|string

        在表上执行 ``TRUNCATE`` 语句。

        .. note:: 如果使用的数据库平台不支持 ``TRUNCATE``，
            将使用 ``DELETE`` 语句代替。

    .. php:method:: emptyTable()

        :returns: 成功时返回 ``true``，失败时返回 ``false``
        :rtype:    bool

        通过 ``DELETE`` 语句从表中删除所有记录。

    .. php:method:: getCompiledSelect([$reset = true])

        :param bool $reset: 是否重置当前 QB 值
        :returns: 编译后的 SQL 语句字符串
        :rtype:    string

        编译 ``SELECT`` 语句并将其作为字符串返回。

    .. php:method:: getCompiledInsert([$reset = true])

        :param bool $reset: 是否重置当前 QB 值
        :returns: 编译后的 SQL 语句字符串
        :rtype:     string

        编译 ``INSERT`` 语句并将其作为字符串返回。

    .. php:method:: getCompiledUpdate([$reset = true])

        :param bool $reset: 是否重置当前 QB 值
        :returns: 编译后的 SQL 语句字符串
        :rtype:    string

        编译 ``UPDATE`` 语句并将其作为字符串返回。

    .. php:method:: getCompiledDelete([$reset = true])

        :param bool $reset: 是否重置当前 QB 值
        :returns: 编译后的 SQL 语句字符串
        :rtype:    string

        编译 ``DELETE`` 语句并将其作为字符串返回。
