###################
查询构建器类
###################

CodeIgniter 为你提供了访问查询构建器类的方式。该模式允许你通过最少的脚本执行数据库的检索、插入和更新操作。在某些情况下，只需一两行代码即可执行数据库操作。CodeIgniter 不要求每个数据库表对应一个独立的类文件，而是提供了一个更为简化的接口。

除了简单性，使用查询构建器功能的一个主要优势是它允许你创建与数据库无关的应用程序，因为查询语法由每个数据库适配器生成。它还允许更安全的查询，因为系统会自动对值进行转义。

.. note:: CodeIgniter 不支持表名和列名中包含点号（``.``）。自 v4.5.0 起，支持包含点号的数据库名。

.. contents::
    :local:
    :depth: 2

************************
SQL 注入防护
************************

你可以借助查询构建器相当安全地生成 SQL 语句。 然而，它并非被设计为无论你传递什么数据都能防止 SQL 注入。

传递给查询构建器的参数可以是：
    1. **标识符**，例如字段（或表）名
    2. 它们的 **值**
    3. **SQL 字符串** 的一部分

查询构建器默认会对所有 **值** 进行转义。

默认情况下，它也会尝试正确保护 **标识符** 和 **SQL 字符串** 中的标识符。然而，该实现是为了在多数用例中良好工作，并非设计用于防御所有攻击。因此，在未经适当验证的情况下，你绝不应将用户输入传递给它们。

此外，许多方法具有 ``$escape`` 参数，可以设置为禁用转义。如果 ``$escape`` 设置为 false，查询构建器将不提供任何保护，因此在传递给查询构建器之前，你必须自行确保它们已正确转义或保护。使用指定原始 SQL 语句的 ``RawSql`` 时也是如此。

*************************
加载查询构建器
*************************

查询构建器通过数据库连接上的 ``table()`` 方法加载。这会为你设置查询的 **FROM** 部分，并返回查询构建器类的新实例：

.. literalinclude:: query_builder/001.php

只有在你明确请求该类时，查询构建器才会加载到内存中，因此默认情况下不会占用资源。

**************
选择数据
**************

以下方法允许你构建 SQL **SELECT** 语句。

Get
===

$builder->get()
---------------

运行选择查询并返回结果。可单独使用以从表中检索所有记录：

.. literalinclude:: query_builder/002.php

第一个和第二个参数允许你设置 limit 和 offset 子句：

.. literalinclude:: query_builder/003.php

你会注意到上述方法被赋值给名为 $query 的变量，该变量可用于显示结果：

.. literalinclude:: query_builder/004.php

关于结果生成的完整讨论，请访问 :ref:`getResult() <getresult>` 方法。

$builder->getCompiledSelect()
-----------------------------

像 ``$builder->get()`` 一样编译选择查询，但不会 *运行* 查询。此方法仅以字符串形式返回 SQL 查询。

示例：

.. literalinclude:: query_builder/005.php

第一个参数（false）允许你设置查询构建器是否会被重置（因为参数的默认值为 true，即 ``getCompiledSelect(bool $reset = true)``，默认情况下会像使用 ``$builder->get()`` 一样被重置）：

.. literalinclude:: query_builder/006.php

需要注意的关键点是，第二个查询未使用 ``limit(10, 20)``，但生成的 SQL 查询包含 ``LIMIT 20, 10``。造成此结果的原因是第一个查询的参数设置为 ``false``，导致 ``limit(10, 20)`` 保留在第二个查询中。

$builder->getWhere()
--------------------

与 ``get()`` 方法相同，区别在于它允许你在第一个参数中添加 "where" 子句，而无需使用 ``$builder->where()`` 方法：

.. literalinclude:: query_builder/007.php

有关 ``where()`` 方法的更多信息，请阅读下文。

.. _query-builder-select:

Select
======

$builder->select()
------------------

允许你编写查询的 **SELECT** 部分：

.. literalinclude:: query_builder/008.php

.. note:: 如果从表中选择所有（``*``），则无需使用此方法。当省略时，CodeIgniter 假定你希望选择所有字段并自动添加 ``SELECT *``。

``$builder->select()`` 接受可选的第二个参数。如果将其设置为 ``false``，CodeIgniter 将不会尝试保护你的字段或表名。这在需要复合 select 语句且自动转义字段可能破坏它们时非常有用。

.. literalinclude:: query_builder/009.php

.. _query-builder-select-rawsql:

RawSql
^^^^^^

.. versionadded:: 4.2.0

自 v4.2.0 起，``$builder->select()`` 接受表示原始 SQL 字符串的 ``CodeIgniter\Database\RawSql`` 实例。

.. literalinclude:: query_builder/099.php

.. warning:: 使用 ``RawSql`` 时，你必须手动转义值并保护标识符。否则可能导致 SQL 注入。

$builder->selectMax()
---------------------

为你的查询编写 **SELECT MAX(field)** 部分。你可以选择包含第二个参数以重命名结果字段。

.. literalinclude:: query_builder/010.php

$builder->selectMin()
---------------------

为你的查询编写 **SELECT MIN(field)** 部分。与 ``selectMax()`` 类似，你可以选择包含第二个参数以重命名结果字段。

.. literalinclude:: query_builder/011.php

$builder->selectAvg()
---------------------

为你的查询编写 **SELECT AVG(field)** 部分。与 ``selectMax()`` 类似，你可以选择包含第二个参数以重命名结果字段。

.. literalinclude:: query_builder/012.php

$builder->selectSum()
---------------------

为你的查询编写 **SELECT SUM(field)** 部分。与 ``selectMax()`` 类似，你可以选择包含第二个参数以重命名结果字段。

.. literalinclude:: query_builder/013.php

$builder->selectCount()
-----------------------

为你的查询编写 **SELECT COUNT(field)** 部分。与 ``selectMax()`` 类似，你可以选择包含第二个参数以重命名结果字段。

.. note:: 此方法在与 ``groupBy()`` 结合使用时特别有用。对于一般计数，请参见 ``countAll()`` 或 ``countAllResults()``。

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

允许你编写查询的 **FROM** 部分：

.. literalinclude:: query_builder/016.php

.. note:: 如前所示，查询的 **FROM** 部分可以在 ``$db->table()`` 方法中指定。对 ``from()`` 的额外调用将向查询的 FROM 部分添加更多表。

.. _query-builder-from-subquery:

子查询
==========

$builder->fromSubquery()
------------------------

允许你将 **FROM** 查询的一部分作为子查询编写。

这是将子查询添加到现有表的位置：

.. literalinclude:: query_builder/017.php

使用 ``$db->newQuery()`` 方法将子查询作为主表：

.. literalinclude:: query_builder/018.php

Join
====

.. _query-builder-join:

$builder->join()
----------------

允许你编写查询的 **JOIN** 部分：

.. literalinclude:: query_builder/019.php

如果在一个查询中需要多个连接，可以进行多次方法调用。

如果需要特定类型的 **JOIN**，可以通过该方法的第三个参数指定。选项包括：``left``、``right``、``outer``、``inner``、``left outer`` 和 ``right outer``。

.. literalinclude:: query_builder/020.php

.. _query-builder-join-rawsql:

RawSql
^^^^^^

.. versionadded:: 4.2.0

自 v4.2.0 起，``$builder->join()`` 接受表示原始 SQL 字符串的 ``CodeIgniter\Database\RawSql`` 实例作为 JOIN ON 条件。

.. literalinclude:: query_builder/102.php

.. warning:: 使用 ``RawSql`` 时，你必须手动转义值并保护标识符。否则可能导致 SQL 注入。

*************************
查找特定数据
*************************

Where
=====

$builder->where()
-----------------

此方法允许你使用五种方法之一设置 **WHERE** 子句：

.. note:: 传递给此方法的所有值都会自动转义，从而生成更安全的查询，除非使用自定义字符串。

.. note:: ``$builder->where()`` 接受可选的第三个参数。如果将其设置为 ``false``，CodeIgniter 将不会尝试保护你的字段或表名。

1. 简单键/值方法
^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. literalinclude:: query_builder/021.php

    注意等号已为你添加。

    如果多次调用该方法，它们将通过 **AND** 链接：

    .. literalinclude:: query_builder/022.php

2. 自定义键/值方法
^^^^^^^^^^^^^^^^^^^^^^^^^^

    你可以在第一个参数中包含运算符以控制比较：

    .. literalinclude:: query_builder/023.php

3. 关联数组方法
^^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. literalinclude:: query_builder/024.php

    你也可以使用此方法包含自己的运算符：

    .. literalinclude:: query_builder/025.php

4. 自定义字符串
^^^^^^^^^^^^^^^^

    你可以手动编写自己的子句：

    .. literalinclude:: query_builder/026.php

    .. warning:: 如果在字符串中使用用户提供的数据，你必须手动转义值并保护标识符。否则可能导致 SQL 注入。

        .. literalinclude:: query_builder/027.php

.. _query-builder-where-rawsql:

5. RawSql
^^^^^^^^^

    .. versionadded:: 4.2.0

    自 v4.2.0 起，``$builder->where()`` 接受表示原始 SQL 字符串的 ``CodeIgniter\Database\RawSql`` 实例。

    .. literalinclude:: query_builder/100.php

    .. warning:: 使用 ``RawSql`` 时，你必须手动转义值并保护标识符。否则可能导致 SQL 注入。

.. _query-builder-where-subquery:

6. 子查询
^^^^^^^^^^^^^

    .. literalinclude:: query_builder/028.php

$builder->orWhere()
-------------------

此方法与上述方法相同，区别在于多个实例通过 **OR** 连接：

.. literalinclude:: query_builder/029.php

$builder->whereIn()
-------------------

生成 **WHERE field IN ('item', 'item')** SQL 查询，并在适当时通过 **AND** 连接：

.. literalinclude:: query_builder/030.php

你可以使用子查询代替值数组：

.. literalinclude:: query_builder/031.php

$builder->orWhereIn()
---------------------

生成 **WHERE field IN ('item', 'item')** SQL 查询，并在适当时通过 **OR** 连接：

.. literalinclude:: query_builder/032.php

你可以使用子查询代替值数组：

.. literalinclude:: query_builder/033.php

$builder->whereNotIn()
----------------------

生成 **WHERE field NOT IN ('item', 'item')** SQL 查询，并在适当时通过 **AND** 连接：

.. literalinclude:: query_builder/034.php

你可以使用子查询代替值数组：

.. literalinclude:: query_builder/035.php

$builder->orWhereNotIn()
------------------------

生成 **WHERE field NOT IN ('item', 'item')** SQL 查询，并在适当时通过 **OR** 连接：

.. literalinclude:: query_builder/036.php

你可以使用子查询代替值数组：

.. literalinclude:: query_builder/037.php

************************
查找相似数据
************************

Like
====

$builder->like()
----------------

此方法允许你生成 **LIKE** 子句，适用于执行搜索。

.. note:: 传递给此方法的所有值都会自动转义。

.. note:: 所有 ``like*`` 方法变体可以通过将第五个参数设置为 ``true`` 来强制执行不区分大小写的搜索。这将使用平台特定的功能（如果可用），否则将强制将值转换为小写，即 ``WHERE LOWER(column) LIKE '%search%'``。这可能需要在 ``LOWER(column)`` 而非 ``column`` 上创建索引才能生效。

1. 简单键/值方法
^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. literalinclude:: query_builder/038.php

    如果多次调用该方法，它们将通过 **AND** 链接：

    .. literalinclude:: query_builder/039.php

    如果要控制通配符（ **%** ）的位置，可以使用可选的第三个参数。选项为 ``before``、``after`` 和 ``both`` （默认）。

    .. literalinclude:: query_builder/040.php

2. 关联数组方法
^^^^^^^^^^^^^^^^^^^^^^^^^^^

       .. literalinclude:: query_builder/041.php

.. _query-builder-like-rawsql:

3. RawSql
^^^^^^^^^

    .. versionadded:: 4.2.0

    自 v4.2.0 起，``$builder->like()`` 接受表示原始 SQL 字符串的 ``CodeIgniter\Database\RawSql`` 实例。

    .. literalinclude:: query_builder/101.php

    .. warning:: 使用 ``RawSql`` 时，你必须手动转义值并保护标识符。否则可能导致 SQL 注入。

$builder->orLike()
------------------

此方法与上述方法相同，区别在于多个实例通过 **OR** 连接：

.. literalinclude:: query_builder/042.php

$builder->notLike()
-------------------

此方法与 ``like()`` 相同，但生成 **NOT LIKE** 语句：

.. literalinclude:: query_builder/043.php

$builder->orNotLike()
---------------------

此方法与 ``notLike()`` 相同，但多个实例通过 **OR** 连接：

.. literalinclude:: query_builder/044.php

$builder->groupBy()
-------------------

允许你编写查询的 **GROUP BY** 部分：

.. literalinclude:: query_builder/045.php

你也可以传递多个值的数组：

.. literalinclude:: query_builder/046.php

$builder->distinct()
--------------------

向查询添加 **DISTINCT** 关键字：

.. literalinclude:: query_builder/047.php

$builder->having()
------------------

允许你编写查询的 **HAVING** 部分。有两种可能的语法，1 个参数或 2 个：

.. literalinclude:: query_builder/048.php

你也可以传递多个值的数组：

.. literalinclude:: query_builder/049.php

如果你使用的数据库由 CodeIgniter 转义值，可以通过传递可选的第三个参数并设置为 ``false`` 来防止转义内容。

.. literalinclude:: query_builder/050.php

$builder->orHaving()
--------------------

与 ``having()`` 相同，但多个子句通过 **OR** 分隔。

$builder->havingIn()
--------------------

生成 **HAVING field IN ('item', 'item')** SQL 查询，并在适当时通过 **AND** 连接：

.. literalinclude:: query_builder/051.php

你可以使用子查询代替值数组：

.. literalinclude:: query_builder/052.php

$builder->orHavingIn()
----------------------

生成 **HAVING field IN ('item', 'item')** SQL 查询，并在适当时通过 **OR** 连接：

.. literalinclude:: query_builder/053.php

你可以使用子查询代替值数组：

.. literalinclude:: query_builder/054.php

$builder->havingNotIn()
-----------------------

生成 **HAVING field NOT IN ('item', 'item')** SQL 查询，并在适当时通过 **AND** 连接：

.. literalinclude:: query_builder/055.php

你可以使用子查询代替值数组：

.. literalinclude:: query_builder/056.php

$builder->orHavingNotIn()
-------------------------

生成 **HAVING field NOT IN ('item', 'item')** SQL 查询，并在适当时通过 **OR** 连接：

.. literalinclude:: query_builder/057.php

你可以使用子查询代替值数组：

.. literalinclude:: query_builder/058.php

$builder->havingLike()
----------------------

此方法允许你为查询的 **HAVING** 部分生成 **LIKE** 子句，适用于执行搜索。

.. note:: 传递给此方法的所有值都会自动转义。

.. note:: 所有 ``havingLike*()`` 方法变体可以通过将第五个参数设置为 ``true`` 来强制执行不区分大小写的搜索。这将使用平台特定的功能（如果可用），否则将强制将值转换为小写，即 ``HAVING LOWER(column) LIKE '%search%'``。这可能需要在 ``LOWER(column)`` 而非 ``column`` 上创建索引才能生效。

1. 简单键/值方法
^^^^^^^^^^^^^^^^^^^^^^^^^^

    .. literalinclude:: query_builder/059.php

    如果多次调用该方法，它们将通过 **AND** 链接：

    .. literalinclude:: query_builder/060.php

    如果要控制通配符（ **%** ）的位置，可以使用可选的第三个参数。选项为 ``before``、``after`` 和 ``both`` （默认）。

    .. literalinclude:: query_builder/061.php

2. 关联数组方法
^^^^^^^^^^^^^^^^^^^^^^^^^^^

       .. literalinclude:: query_builder/062.php

$builder->orHavingLike()
------------------------

此方法与上述方法相同，区别在于多个实例通过 **OR** 连接：

.. literalinclude:: query_builder/063.php

$builder->notHavingLike()
-------------------------

此方法与 ``havingLike()`` 相同，但生成 **NOT LIKE** 语句：

.. literalinclude:: query_builder/064.php

$builder->orNotHavingLike()
---------------------------

此方法与 ``notHavingLike()`` 相同，但多个实例通过 **OR** 连接：

.. literalinclude:: query_builder/065.php

****************
排序结果
****************

OrderBy
=======

$builder->orderBy()
-------------------

允许你设置 **ORDER BY** 子句。

第一个参数包含要排序的列名。

第二个参数允许你设置结果的方向。选项为 ``ASC``、``DESC`` 和 ``RANDOM``。

.. literalinclude:: query_builder/066.php

你也可以在第一个参数中传递自己的字符串：

.. literalinclude:: query_builder/067.php

如果需要多个字段，可以进行多次方法调用。

.. literalinclude:: query_builder/068.php

如果选择 ``RANDOM`` 方向选项，除非指定数字种子值，否则将忽略第一个参数。

.. literalinclude:: query_builder/069.php

****************************
限制或计数结果
****************************

Limit
=====

$builder->limit()
-----------------

允许你限制查询返回的行数：

.. literalinclude:: query_builder/070.php

.. note:: 如果在 SQL 语句中指定了 ``LIMIT 0``，将返回 0 条记录。然而，在查询构建器中存在一个错误：如果指定 ``limit(0)``，生成的 SQL 语句将没有 ``LIMIT`` 子句，并返回所有记录。在 v4.5.0 中添加了设置以修复此错误行为。详细信息请参阅 :ref:`v450-query-builder-limit-0-behavior`。此错误行为将在未来版本中修复，因此建议你更改默认设置。

第二个参数允许你设置结果偏移量。

.. literalinclude:: query_builder/071.php

$builder->countAllResults()
---------------------------

允许你确定特定查询构建器查询中的行数。查询支持查询构建器的限制条件，如 ``where()``、``orWhere()``、``like()``、``orLike()`` 等。示例：

.. literalinclude:: query_builder/072.php

但是，此方法还会重置你可能传递给 ``select()`` 的任何字段值。如果需要保留它们，可以将第一个参数传递为 ``false``。

.. literalinclude:: query_builder/073.php

$builder->countAll()
--------------------

允许你确定特定表中的行数。示例：

.. literalinclude:: query_builder/074.php

与 ``countAllResult()`` 方法类似，此方法也会重置你可能传递给 ``select()`` 的任何字段值。如果需要保留它们，可以将第一个参数传递为 ``false``。

.. _query-builder-union:

*************
联合查询
*************

Union
=====

$builder->union()
-----------------

用于组合两个或多个 SELECT 语句的结果集。它将仅返回唯一结果。

.. literalinclude:: query_builder/103.php

.. note:: 为了与 DBMS（如 MSSQL 和 Oracle）正确配合，查询会被包装在 ``SELECT * FROM ( ... ) alias`` 中。主查询将始终具有别名 ``uwrp0``。通过 ``union()`` 添加的每个后续查询将具有别名 ``uwrpN+1``。

所有联合查询将添加在主查询之后，无论 ``union()`` 方法的调用顺序如何。也就是说，即使在调用 ``union()`` 之后调用 ``limit()`` 或 ``orderBy()`` 方法，这些方法也将相对于主查询。

在某些情况下，可能需要对查询结果进行排序或限制记录数。解决方案是使用通过 ``$db->newQuery()`` 创建的包装器。在下面的示例中，我们获取前 5 个用户 + 后 5 个用户并按 id 排序结果：

.. literalinclude:: query_builder/104.php

$builder->unionAll()
--------------------

行为与 ``union()`` 方法相同。但是，将返回所有结果，而不仅仅是唯一结果。

**************
查询分组
**************

Group
=====

查询分组允许你通过将 **WHERE** 子句括在括号中来创建分组。这将允许你创建具有复杂 **WHERE** 子句的查询。支持嵌套分组。示例：

.. literalinclude:: query_builder/075.php

.. note:: 分组需要平衡，确保每个 ``groupStart()`` 都有对应的 ``groupEnd()``。

$builder->groupStart()
----------------------

通过向查询的 **WHERE** 子句添加左括号开始新分组。

$builder->orGroupStart()
------------------------

通过向查询的 **WHERE** 子句添加左括号开始新分组，并添加前缀 **OR**。

$builder->notGroupStart()
-------------------------

通过向查询的 **WHERE** 子句添加左括号开始新分组，并添加前缀 **NOT**。

$builder->orNotGroupStart()
---------------------------

通过向查询的 **WHERE** 子句添加左括号开始新分组，并添加前缀 **OR NOT**。

$builder->groupEnd()
--------------------

通过向查询的 **WHERE** 子句添加右括号结束当前分组。

$builder->havingGroupStart()
----------------------------

通过向查询的 **HAVING** 子句添加左括号开始新分组。

$builder->orHavingGroupStart()
------------------------------

通过向查询的 **HAVING** 子句添加左括号开始新分组，并添加前缀 **OR**。

$builder->notHavingGroupStart()
-------------------------------

通过向查询的 **HAVING** 子句添加左括号开始新分组，并添加前缀 **NOT**。

$builder->orNotHavingGroupStart()
---------------------------------

通过向查询的 **HAVING** 子句添加左括号开始新分组，并添加前缀 **OR NOT**。

$builder->havingGroupEnd()
--------------------------

通过向查询的 **HAVING** 子句添加右括号结束当前分组。

**************
插入数据
**************

Insert
======

$builder->insert()
------------------

根据你提供的数据生成 insert 字符串并运行查询。你可以向该方法传递 **数组** 或 **对象**。以下是使用数组的示例：

.. literalinclude:: query_builder/076.php

第一个参数是值的关联数组。

.. note:: 除 ``RawSql`` 外，所有值都会自动转义，生成更安全的查询。

.. warning:: 使用 ``RawSql`` 时，你必须手动转义数据。否则可能导致 SQL 注入。

以下是使用对象的示例：

.. literalinclude:: query_builder/077.php

.. literalinclude:: query_builder/121.php

第一个参数是一个对象。

$builder->ignore()
------------------

根据你提供的数据生成 insert ignore 字符串并运行查询。因此，如果具有相同主键的条目已存在，则不会插入该查询。你可以选择向该方法传递 **布尔值**。也可用于 **insertBatch**、**update** 和 **delete** （在支持时）。以下是使用上述示例数组的示例：

.. literalinclude:: query_builder/078.php

$builder->getCompiledInsert()
-----------------------------

像 ``$builder->insert()`` 一样编译插入查询，但不会 *运行* 查询。此方法仅以字符串形式返回 SQL 查询。

示例：

.. literalinclude:: query_builder/079.php

第一个参数允许你设置是否重置查询构建器查询（默认情况下会重置，就像使用 ``$builder->insert()`` 一样）：

.. literalinclude:: query_builder/080.php

第二个查询起作用的原因是第一个参数设置为 ``false``。

.. note:: 此方法不适用于批量插入。

.. _insert-batch-data:

insertBatch
===========

$builder->insertBatch()
-----------------------

从数据插入
^^^^^^^^^^^^^^^^

根据你提供的数据生成 insert 字符串并运行查询。你可以向该方法传递 **数组** 或 **对象**。以下是使用数组的示例：

.. literalinclude:: query_builder/081.php

第一个参数是值的关联数组。

.. note:: 除 ``RawSql`` 外，所有值都会自动转义，生成更安全的查询。

.. warning:: 使用 ``RawSql`` 时，你必须手动转义数据。否则可能导致 SQL 注入。

从查询插入
^^^^^^^^^^^^^^^^^^^

你也可以从查询插入：

.. literalinclude:: query_builder/117.php

.. note:: 自 v4.3.0 起，可以使用 ``setQueryAsData()``。

.. note:: 必须将 select 查询的列别名与目标表的列匹配。

.. _upsert-data:

**************
更新插入数据
**************

Upsert
======

$builder->upsert()
------------------

.. versionadded:: 4.3.0

根据你提供的数据生成更新插入字符串并运行查询。你可以向该方法传递 **数组** 或 **对象**。默认情况下，将按顺序定义约束。首先选择主键，然后是唯一键。MySQL 将默认使用任何约束。以下是使用数组的示例：

.. literalinclude:: query_builder/112.php

第一个参数是值的关联数组。

以下是使用对象的示例：

.. literalinclude:: query_builder/122.php

.. literalinclude:: query_builder/113.php

第一个参数是一个对象。

.. note:: 所有值都会自动转义，生成更安全的查询。

$builder->getCompiledUpsert()
-----------------------------

.. versionadded:: 4.3.0

像 ``$builder->upsert()`` 一样编译更新插入查询，但不会 *运行* 查询。此方法仅以字符串形式返回 SQL 查询。

示例：

.. literalinclude:: query_builder/114.php

.. note:: 此方法不适用于批量更新插入。

upsertBatch
===========

$builder->upsertBatch()
-----------------------

.. versionadded:: 4.3.0

从数据更新插入
^^^^^^^^^^^^^^^^

根据你提供的数据生成更新插入字符串并运行查询。你可以向该方法传递 **数组** 或 **对象**。默认情况下，将按顺序定义约束。首先选择主键，然后是唯一键。MySQL 将默认使用任何约束。

以下是使用数组的示例：

.. literalinclude:: query_builder/108.php

第一个参数是值的关联数组。

.. note:: 所有值都会自动转义，生成更安全的查询。

从查询更新插入
^^^^^^^^^^^^^^^^^^^

你也可以从查询更新插入：

.. literalinclude:: query_builder/115.php

.. note:: 自 v4.3.0 起，可以使用 ``setQueryAsData()``、``onConstraint()`` 和 ``updateFields()`` 方法。

.. note:: 必须将 select 查询的列别名与目标表的列匹配。

$builder->onConstraint()
------------------------

.. versionadded:: 4.3.0

允许手动设置用于更新插入的约束。这不适用于 MySQL，因为 MySQL 默认检查所有约束。

.. literalinclude:: query_builder/109.php

此方法接受字符串或列数组。

$builder->updateFields()
------------------------

.. versionadded:: 4.3.0

允许手动设置执行更新插入时要更新的字段。

.. literalinclude:: query_builder/110.php

此方法接受字符串、列数组或 RawSql。你还可以指定不包含在数据集中的额外列进行更新。这可以通过将第二个参数设置为 ``true`` 来实现。

.. literalinclude:: query_builder/111.php

注意 ``updated_at`` 字段未插入，但用于更新。

*************
更新数据
*************

Update
======

$builder->replace()
-------------------

此方法执行 **REPLACE** 语句，本质上是 SQL 标准的（可选）**DELETE** + **INSERT**，使用 *PRIMARY* 和 *UNIQUE* 作为决定因素。在我们的案例中，它将使你无需通过组合不同的 ``select()``、``update()``、``delete()`` 和 ``insert()`` 调用来实现复杂逻辑。

示例：

.. literalinclude:: query_builder/082.php

在上述示例中，如果我们假设 ``title`` 字段是主键，则包含 ``My title`` 作为 ``title`` 值的行将被删除，并用我们的新行数据替换。

也允许使用 ``set()`` 方法，并且所有值都会自动转义，就像 ``insert()`` 一样。

$builder->set()
---------------

此方法允许你为插入或更新设置值。

**它可以代替直接向 insert() 或 update() 方法传递数据数组：**

.. literalinclude:: query_builder/083.php

如果多次调用该方法，它们将根据你执行的是插入还是更新正确组装：

.. literalinclude:: query_builder/084.php

``set()`` 也接受可选的第三个参数（``$escape``），如果设置为 ``false``，将防止值被转义。为了说明差异，以下是使用和不使用转义参数的 ``set()``。

.. literalinclude:: query_builder/085.php

你也可以向此方法传递关联数组：

.. literalinclude:: query_builder/086.php

或对象：

.. literalinclude:: query_builder/077.php

.. literalinclude:: query_builder/087.php

$builder->update()
------------------

根据你提供的数据生成 update 字符串并运行查询。你可以传递 **数组** 或 **对象**。以下是使用数组的示例：

.. literalinclude:: query_builder/088.php

或者你可以提供对象：

.. literalinclude:: query_builder/077.php

.. literalinclude:: query_builder/089.php

.. note:: 除 ``RawSql`` 外，所有值都会自动转义，生成更安全的查询。

.. warning:: 使用 ``RawSql`` 时，你必须手动转义数据。否则可能导致 SQL 注入。

你会注意到使用 ``$builder->where()`` 方法，允许你设置 **WHERE** 子句。你可以直接将此信息作为字符串传递到 ``update()`` 方法中：

.. literalinclude:: query_builder/090.php

或作为数组：

.. literalinclude:: query_builder/091.php

执行更新时，也可以使用上述的 ``$builder->set()`` 方法。

$builder->getCompiledUpdate()
-----------------------------

此方法与 ``$builder->getCompiledInsert()`` 的工作方式完全相同，区别在于生成的是 **UPDATE** SQL 字符串而非 **INSERT** SQL 字符串。

有关详细信息，请查看 `$builder->getCompiledInsert()`_ 的文档。

.. note:: 此方法不适用于批量更新。

.. _update-batch:

UpdateBatch
===========

$builder->updateBatch()
-----------------------

.. note:: 自 v4.3.0 起，``updateBatch()`` 的第二个参数 ``$index`` 已更改为 ``$constraints``。现在接受数组、字符串或 ``RawSql`` 类型。

从数据更新
^^^^^^^^^^^^^^^^

根据你提供的数据生成 update 字符串并运行查询。你可以向该方法传递 **数组** 或 **对象**。以下是使用数组的示例：

.. literalinclude:: query_builder/092.php

第一个参数是值的关联数组，第二个参数是 where 键。

.. note:: 自 v4.3.0 起，生成的 SQL 结构已改进。

自 v4.3.0 起，你也可以使用 ``onConstraint()`` 和 ``updateFields()`` 方法：

.. literalinclude:: query_builder/120.php

.. note:: 除 ``RawSql`` 外，所有值都会自动转义，生成更安全的查询。

.. warning:: 使用 ``RawSql`` 时，你必须手动转义数据。否则可能导致 SQL 注入。

.. note:: 因为工作原理的原因，若使用此方法则 ``affectedRows()`` 无法提供正确的结果。相反，``updateBatch()`` 返回受影响的行数。

从查询更新
^^^^^^^^^^^^^^^^^^^

自 v4.3.0 起，你也可以使用 ``setQueryAsData()`` 方法从查询更新：

.. literalinclude:: query_builder/116.php

.. note:: 必须将 select 查询的列别名与目标表的列匹配。

*************
删除数据
*************

Delete
======

$builder->delete()
------------------

生成 **DELETE** SQL 字符串并运行查询。

.. literalinclude:: query_builder/093.php

第一个参数是 where 子句。你也可以使用 ``where()`` 或 ``orWhere()`` 方法，而不是将数据传递到方法的第一个参数：

.. literalinclude:: query_builder/094.php

如果要删除表中的所有数据，可以使用 ``truncate()`` 方法或 ``emptyTable()``。

$builder->getCompiledDelete()
-----------------------------

此方法与 ``$builder->getCompiledInsert()`` 的工作方式完全相同，区别在于生成的是 **DELETE** SQL 字符串而非 **INSERT** SQL 字符串。

有关详细信息，请查看 `$builder->getCompiledInsert()`_ 的文档。

.. _delete-batch:

DeleteBatch
===========

$builder->deleteBatch()
-----------------------

.. versionadded:: 4.3.0

从数据删除
^^^^^^^^^^^^^^^^

根据一组数据生成批量 **DELETE** 语句。

.. literalinclude:: query_builder/118.php

此方法在删除具有复合主键的表中的数据时可能特别有用。

.. note:: SQLite3 不支持使用 ``where()``。

从查询删除
^^^^^^^^^^^^^^^^^^^

你也可以从查询删除：

.. literalinclude:: query_builder/119.php

$builder->emptyTable()
----------------------

生成 **DELETE** SQL 字符串并运行查询：

.. literalinclude:: query_builder/095.php

$builder->truncate()
--------------------

生成 **TRUNCATE** SQL 字符串并运行查询。

.. literalinclude:: query_builder/096.php

.. note:: 如果 TRUNCATE 命令不可用，``truncate()`` 将执行 "DELETE FROM table"。

**********************
条件语句
**********************

.. _db-builder-when:

When
====

$builder->when()
----------------

.. versionadded:: 4.3.0

这允许根据条件修改查询，而不会中断查询构建器链。第一个参数是条件，应评估为布尔值。第二个参数是在条件为 true 时运行的回调函数。

例如，你可能希望仅根据 HTTP 请求中发送的值应用给定的 WHERE 语句：

.. literalinclude:: query_builder/105.php

由于条件评估为 ``true``，将调用回调函数。条件中设置的值将作为第二个参数传递给回调函数，以便在查询中使用。

有时，你可能希望在条件评估为 false 时应用不同的语句。这可以通过提供第二个闭包实现：

.. literalinclude:: query_builder/106.php

WhenNot
=======

$builder->whenNot()
-------------------

.. versionadded:: 4.3.0

此方法与 ``$builder->when()`` 的工作方式完全相同，区别在于仅在条件评估为 ``false`` 时运行回调函数，而 ``when()`` 在 ``true`` 时运行。

.. literalinclude:: query_builder/107.php

***************
方法链
***************

方法链允许你通过连接多个方法来简化语法。考虑以下示例：

.. literalinclude:: query_builder/097.php

.. _ar-caching:

***********************
重置查询构建器
***********************

ResetQuery
==========

$builder->resetQuery()
----------------------

重置查询构建器允许你在不首先使用 ``$builder->get()`` 或 ``$builder->insert()`` 等方法执行查询的情况下重新开始查询。

这在以下情况下非常有用：你使用查询构建器生成 SQL（例如 ``$builder->getCompiledSelect()``），但随后选择运行查询：

.. literalinclude:: query_builder/098.php

***************
类参考
***************

.. php:namespace:: CodeIgniter\Database

.. php:class:: BaseBuilder

    .. php:method:: db()

        :returns:   当前使用的数据库连接
        :rtype:     ``ConnectionInterface``

        从 ``$db`` 返回当前数据库连接。用于访问不直接对查询构建器可用的 ``ConnectionInterface`` 方法，如 ``insertID()`` 或 ``errors()``。

    .. php:method:: resetQuery()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        重置当前查询构建器状态。在希望构建可在某些条件下取消的查询时非常有用。

    .. php:method:: countAllResults([$reset = true])

        :param bool $reset: 是否重置 SELECT 的值
        :returns:   查询结果中的行数
        :rtype:     int

        生成特定于平台的查询字符串，统计查询构建器查询返回的所有记录。

    .. php:method:: countAll([$reset = true])

        :param bool $reset: 是否重置 SELECT 的值
        :returns:   查询结果中的行数
        :rtype:     int

        生成特定于平台的查询字符串，统计特定表中的所有记录。

    .. php:method:: get([$limit = null[, $offset = null[, $reset = true]]]])

        :param int $limit: LIMIT 子句
        :param int $offset: OFFSET 子句
        :param bool $reset: 是否清除查询构建器的值？
        :returns: ``\CodeIgniter\Database\ResultInterface`` 实例（方法链）
        :rtype:    ``\CodeIgniter\Database\ResultInterface``

        根据已调用的查询构建器方法编译并运行 ``SELECT`` 语句。

    .. php:method:: getWhere([$where = null[, $limit = null[, $offset = null[, $reset = true]]]]])

        :param string $where: WHERE 子句
        :param int $limit: LIMIT 子句
        :param int $offset: OFFSET 子句
        :param bool $reset: 是否清除查询构建器的值？
        :returns:   ``\CodeIgniter\Database\ResultInterface`` 实例（方法链）
        :rtype:     ``\CodeIgniter\Database\ResultInterface``

        与 ``get()`` 相同，但允许直接添加 WHERE 子句。

    .. php:method:: select([$select = '*'[, $escape = null]])

        :param array|RawSql|string $select: 查询的 SELECT 部分
        :param bool $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``SELECT`` 子句。

    .. php:method:: selectAvg([$select = ''[, $alias = '']])

        :param string $select: 计算平均值的字段
        :param string $alias: 结果值名称的别名
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``SELECT AVG(field)`` 子句。

    .. php:method:: selectMax([$select = ''[, $alias = '']])

        :param string $select: 计算最大值的字段
        :param string $alias: 结果值名称的别名
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``SELECT MAX(field)`` 子句。

    .. php:method:: selectMin([$select = ''[, $alias = '']])

        :param string $select: 计算最小值的字段
        :param string $alias: 结果值名称的别名
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``SELECT MIN(field)`` 子句。

    .. php:method:: selectSum([$select = ''[, $alias = '']])

        :param string $select: 计算总和的字段
        :param string $alias: 结果值名称的别名
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``SELECT SUM(field)`` 子句。

    .. php:method:: selectCount([$select = ''[, $alias = '']])

        :param string $select: 计算计数的字段
        :param string $alias: 结果值名称的别名
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``SELECT COUNT(field)`` 子句。

    .. php:method:: selectSubquery(BaseBuilder $subquery, string $as)

        :param string $subquery: BaseBuilder 实例
        :param string $as: 结果值名称的别名
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向选择部分添加子查询。

    .. php:method:: distinct([$val = true])

        :param bool $val: "distinct" 标志的期望值
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        设置一个标志，告诉查询构建器向查询的 ``SELECT`` 部分添加 ``DISTINCT`` 子句。

    .. php:method:: from($from[, $overwrite = false])

        :param mixed $from: 表名；字符串或数组
        :param bool    $overwrite: 是否覆盖第一个现有表？
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

        :param BaseBuilder|RawSql $query: BaseBuilder 或 RawSql 实例
        :param string|null $alias: 查询的别名
        :param array|string|null $columns: 查询中的列数组或逗号分隔的字符串
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        设置查询作为 ``insertBatch()``、``updateBatch()``、``upsertBatch()`` 的数据源。如果 ``$columns`` 为 null，将运行查询以生成列名。

    .. php:method:: join($table, $cond[, $type = ''[, $escape = null]])

        :param string $table: 要连接的表名
        :param string|RawSql $cond: JOIN ON 条件
        :param string $type: JOIN 类型
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``JOIN`` 子句。自 v4.2.0 起，可以使用 ``RawSql`` 作为 JOIN ON 条件。另请参阅 :ref:`query-builder-join`。

    .. php:method:: where($key[, $value = null[, $escape = null]])

        :param array|RawSql|string $key: 要比较的字段名，或关联数组
        :param mixed $value: 如果是单个键，则与此值比较
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成查询的 ``WHERE`` 部分。多个调用之间用 ``AND`` 分隔。

    .. php:method:: orWhere($key[, $value = null[, $escape = null]])

        :param mixed $key: 要比较的字段名，或关联数组
        :param mixed $value: 如果是单个键，则与此值比较
        :param bool $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成查询的 ``WHERE`` 部分。多个调用之间用 ``OR`` 分隔。

    .. php:method:: orWhereIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要搜索的字段
        :param array|BaseBulder|Closure $values: 目标值数组，或用于子查询的匿名函数
        :param bool $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成 ``WHERE field IN('item', 'item')`` SQL 查询，并在适当时用 ``OR`` 连接。

    .. php:method:: orWhereNotIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要搜索的字段
        :param array|BaseBulder|Closure $values: 目标值数组，或用于子查询的匿名函数
        :param bool $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成 ``WHERE field NOT IN('item', 'item')`` SQL 查询，并在适当时用 ``OR`` 连接。

    .. php:method:: whereIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要检查的字段名
        :param array|BaseBulder|Closure $values: 目标值数组，或用于子查询的匿名函数
        :param bool $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成 ``WHERE field IN('item', 'item')`` SQL 查询，并在适当时用 ``AND`` 连接。

    .. php:method:: whereNotIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要检查的字段名
        :param array|BaseBulder|Closure $values: 目标值数组，或用于子查询的匿名函数
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成 ``WHERE field NOT IN('item', 'item')`` SQL 查询，并在适当时用 ``AND`` 连接。

    .. php:method:: groupStart()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        开始一个组表达式，使用 ``AND`` 连接内部条件。

    .. php:method:: orGroupStart()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        开始一个组表达式，使用 ``OR`` 连接内部条件。

    .. php:method:: notGroupStart()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        开始一个组表达式，使用 ``AND NOT`` 连接内部条件。

    .. php:method:: orNotGroupStart()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        开始一个组表达式，使用 ``OR NOT`` 连接内部条件。

    .. php:method:: groupEnd()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        结束一个组表达式。

    .. php:method:: like($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param array|RawSql|string $field: 字段名
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``LIKE`` 子句，多个调用之间用 ``AND`` 分隔。

    .. php:method:: orLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``LIKE`` 子句，多个调用之间用 ``OR`` 分隔。

    .. php:method:: notLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``NOT LIKE`` 子句，多个调用之间用 ``AND`` 分隔。

    .. php:method:: orNotLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``NOT LIKE`` 子句，多个调用之间用 ``OR`` 分隔。

    .. php:method:: having($key[, $value = null[, $escape = null]])

        :param mixed $key: 标识符（字符串）或字段/值对的关联数组
        :param string $value: 如果 $key 是标识符，则查找的值
        :param string $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``HAVING`` 子句，多个调用之间用 ``AND`` 分隔。

    .. php:method:: orHaving($key[, $value = null[, $escape = null]])

        :param mixed $key: 标识符（字符串）或字段/值对的关联数组
        :param string $value: 如果 $key 是标识符，则查找的值
        :param string $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``HAVING`` 子句，多个调用之间用 ``OR`` 分隔。

    .. php:method:: orHavingIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要搜索的字段
        :param array|BaseBulder|Closure $values: 目标值数组，或用于子查询的匿名函数
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成 ``HAVING field IN('item', 'item')`` SQL 查询，并在适当时用 ``OR`` 连接。

    .. php:method:: orHavingNotIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要搜索的字段
        :param array|BaseBulder|Closure $values: 目标值数组，或用于子查询的匿名函数
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成 ``HAVING field NOT IN('item', 'item')`` SQL 查询，并在适当时用 ``OR`` 连接。

    .. php:method:: havingIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要检查的字段名
        :param array|BaseBulder|Closure $values: 目标值数组，或用于子查询的匿名函数
        :param bool $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成 ``HAVING field IN('item', 'item')`` SQL 查询，并在适当时用 ``AND`` 连接。

    .. php:method:: havingNotIn([$key = null[, $values = null[, $escape = null]]])

        :param string $key: 要检查的字段名
        :param array|BaseBulder|Closure $values: 目标值数组，或用于子查询的匿名函数
        :param bool $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        生成 ``HAVING field NOT IN('item', 'item')`` SQL 查询，并在适当时用 ``AND`` 连接。

    .. php:method:: havingLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询的 ``HAVING`` 部分添加 ``LIKE`` 子句，多个调用之间用 ``AND`` 分隔。

    .. php:method:: orHavingLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制不区分大小写的搜索
        :returns: ``BaseBuilder`` 实例（方法链）
        :rtype:    ``BaseBuilder``

        向查询的 ``HAVING`` 部分添加 ``LIKE`` 子句，多个调用之间用 ``OR`` 分隔。

    .. php:method:: notHavingLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :param bool $insensitiveSearch: 是否强制不区分大小写的搜索
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询的 ``HAVING`` 部分添加 ``NOT LIKE`` 子句，多个调用之间用 ``AND`` 分隔。

    .. php:method:: orNotHavingLike($field[, $match = ''[, $side = 'both'[, $escape = null[, $insensitiveSearch = false]]]])

        :param string $field: 字段名
        :param string $match: 要匹配的文本部分
        :param string $side: 在表达式的哪一侧放置 '%' 通配符
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询的 ``HAVING`` 部分添加 ``NOT LIKE`` 子句，多个调用之间用 ``OR`` 分隔。

    .. php:method:: havingGroupStart()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        开始 ``HAVING`` 子句的组表达式，使用 ``AND`` 连接内部条件。

    .. php:method:: orHavingGroupStart()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        开始 ``HAVING`` 子句的组表达式，使用 ``OR`` 连接内部条件。

    .. php:method:: notHavingGroupStart()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        开始 ``HAVING`` 子句的组表达式，使用 ``AND NOT`` 连接内部条件。

    .. php:method:: orNotHavingGroupStart()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        开始 ``HAVING`` 子句的组表达式，使用 ``OR NOT`` 连接内部条件。

    .. php:method:: havingGroupEnd()

        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        结束 ``HAVING`` 子句的组表达式。

    .. php:method:: groupBy($by[, $escape = null])

        :param mixed $by: 分组的字段；字符串或数组
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``GROUP BY`` 子句。

    .. php:method:: orderBy($orderby[, $direction = ''[, $escape = null]])

        :param string $orderby: 排序字段
        :param string $direction: 排序方向 - ASC、DESC 或 random
        :param bool    $escape: 是否转义值和标识符
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``ORDER BY`` 子句。

    .. php:method:: limit($value[, $offset = 0])

        :param int $value: 限制结果的行数
        :param int $offset: 跳过的行数
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        向查询添加 ``LIMIT`` 和 ``OFFSET`` 子句。

    .. php:method:: offset($offset)

        :param int $offset: 跳过的行数
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

        添加稍后传递给 ``insert()``、``update()`` 或 ``replace()`` 的字段/值对。

    .. php:method:: insert([$set = null[, $escape = null]])

        :param array $set: 字段/值对的关联数组
        :param bool $escape: 是否转义值
        :returns:   成功时返回 ``true``，失败时返回 ``false``
        :rtype:     bool

        编译并执行 ``INSERT`` 语句。

    .. php:method:: insertBatch([$set = null[, $escape = null[, $batch_size = 100]]])

        :param array $set: 要插入的数据
        :param bool $escape: 是否转义值
        :param int $batch_size: 单次插入的行数
        :returns: 插入的行数，或在无数据执行插入操作时返回 ``false``
        :rtype:    int|false

        编译并执行批量 ``INSERT`` 语句。

        .. note:: 当提供的行数超过 ``$batch_size`` 时，将执行多个 ``INSERT`` 查询，每个查询尝试插入最多 ``$batch_size`` 行。

    .. php:method:: setInsertBatch($key[, $value = ''[, $escape = null]])

        .. deprecated:: 4.3.0
           请改用 :php:meth:`CodeIgniter\\Database\\BaseBuilder::setData()`。

        :param mixed $key: 字段名或字段/值对的数组
        :param string $value: 字段值，如果 $key 是单个字段
        :param bool $escape: 是否转义值
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        添加稍后通过 ``insertBatch()`` 插入到表中的字段/值对。

        .. important:: 此方法已弃用，将在未来版本中移除。

    .. php:method:: upsert([$set = null[, $escape = null]])

        :param array $set: 字段/值对的关联数组
        :param bool $escape: 是否转义值
        :returns:   成功时返回 ``true``，失败时返回 ``false``
        :rtype:     bool

        编译并执行 ``UPSERT`` 语句。

    .. php:method:: upsertBatch([$set = null[, $escape = null[, $batch_size = 100]]])

        :param array $set: 要更新插入的数据
        :param bool $escape: 是否转义值
        :param int $batch_size: 单次更新插入的行数
        :returns: 更新插入的行数，或在失败时返回 ``false``
        :rtype:    int|false

        编译并执行批量 ``UPSERT`` 语句。

        .. note:: MySQL 使用 ``ON DUPLICATE KEY UPDATE``，每行的受影响行数为 1（如果作为新行插入）、2（如果更新现有行）和 0（如果现有行设置为当前值）。

        .. note:: 当提供的行数超过 ``$batch_size`` 时，将执行多个 ``UPSERT`` 查询，每个查询尝试更新插入最多 ``$batch_size`` 行。

    .. php:method:: update([$set = null[, $where = null[, $limit = null]]])

        :param array $set: 字段/值对的关联数组
        :param string $where: WHERE 子句
        :param int $limit: LIMIT 子句
        :returns:   成功时返回 ``true``，失败时返回 ``false``
        :rtype:     bool

        编译并执行 ``UPDATE`` 语句。

    .. php:method:: updateBatch([$set = null[, $constraints = null[, $batchSize = 100]]])

        :param array|object|null $set: 字段名，或字段/值对的关联数组
        :param array|RawSql|string|null $constraints: 用作更新键的字段或字段集
        :param int $batchSize: 单次查询中分组条件的数量
        :returns:   更新的行数，或在失败时返回 ``false``
        :rtype:     int|false

        .. note:: 自 v4.3.0 起，参数 ``$set`` 和 ``$constraints`` 的类型已更改。

        编译并执行批量 ``UPDATE`` 语句。``$constraints`` 参数接受逗号分隔的字段字符串、数组、关联数组或 ``RawSql``。

        .. note:: 当提供的字段/值对超过 ``$batchSize`` 时，将执行多个查询，每个查询处理最多 ``$batchSize`` 字段/值对。如果我们将 ``$batchSize`` 设置为 0，则所有字段/值对将在单个查询中执行。

    .. php:method:: updateFields($set, [$addToDefault = false, [$ignore = null]])

        .. versionadded:: 4.3.0

        :param mixed $set: 行或行数组，行是数组或对象
        :param bool $addToDefault: 添加数据集中不存在的额外列
        :param bool $ignore: 要忽略的列数组
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        与 ``updateBatch()`` 和 ``upsertBatch()`` 方法一起使用。定义将更新的字段。

    .. php:method:: onConstraint($set)

        .. versionadded:: 4.3.0

        :param mixed $set: 用作键或约束的字段或字段集
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        与 ``updateBatch()`` 和 ``upsertBatch()`` 方法一起使用。接受逗号分隔的字段字符串、数组、关联数组或 RawSql。

    .. php:method:: setData($set, [$escape = null, [$alias = '']])

        .. versionadded:: 4.3.0

        :param mixed $set: 行或行数组，行是数组或对象
        :param bool $escape: 是否转义值
        :param bool $alias: 数据集的表别名
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        用于 ``*Batch()`` 方法设置插入、更新、更新插入的数据。

    .. php:method:: setUpdateBatch($key[, $value = ''[, $escape = null]])

        .. deprecated:: 4.3.0
           请改用 :php:meth:`CodeIgniter\\Database\\BaseBuilder::setData()`。

        :param mixed $key: 字段名或字段/值对的数组
        :param string $value: 字段值，如果 $key 是单个字段
        :param bool    $escape: 是否转义值
        :returns:   ``BaseBuilder`` 实例（方法链）
        :rtype:     ``BaseBuilder``

        添加稍后通过 ``updateBatch()`` 更新表中的字段/值对。

        .. important:: 此方法已弃用，将在未来版本中移除。

    .. php:method:: replace([$set = null])

        :param array $set: 字段/值对的关联数组
        :returns: 成功时返回 ``true``，失败时返回 ``false``
        :rtype:    bool

        编译并执行 ``REPLACE`` 语句。

    .. php:method:: delete([$where = ''[, $limit = null[, $reset_data = true]]])

        :param string $where: WHERE 子句
        :param int $limit: LIMIT 子句
        :param bool $reset_data: 是否重置查询的 "write" 子句
        :returns:   ``BaseBuilder`` 实例（方法链）或失败时返回 ``false``
        :rtype:     ``BaseBuilder|false``

        编译并执行 ``DELETE`` 查询。

    .. php:method:: deleteBatch([$set = null[, $constraints = null[, $batchSize = 100]]])

        :param array|object|null $set: 字段名，或字段/值对的关联数组
        :param array|RawSql|string|null $constraints: 用作删除键的字段或字段集
        :param int $batchSize: 单次查询中分组条件的数量
        :returns:   删除的行数，或在失败时返回 ``false``
        :rtype:     int|false

        编译并执行批量 ``DELETE`` 查询。

    .. php:method:: increment($column[, $value = 1])

        :param string $column: 要递增的列名
        :param int $value: 递增的量

        将字段的值递增指定量。如果字段不是数字字段（如 ``VARCHAR``），可能会被替换为 ``$value``。

    .. php:method:: decrement($column[, $value = 1])

        :param string $column: 要递减的列名
        :param int $value:  递减的量

        将字段的值递减指定量。如果字段不是数字字段（如 ``VARCHAR``），可能会被替换为 ``$value``。

    .. php:method:: truncate()

        :returns:   成功时返回 ``true``，失败时返回 ``false``，测试模式下返回字符串
        :rtype:     bool|string

        在表上执行 ``TRUNCATE`` 语句。

        .. note:: 如果使用的数据库平台不支持 ``TRUNCATE``，将改用 ``DELETE`` 语句。

    .. php:method:: emptyTable()

        :returns: 成功时返回 ``true``，失败时返回 ``false``
        :rtype:    bool

        通过 ``DELETE`` 语句删除表中的所有记录。

    .. php:method:: getCompiledSelect([$reset = true])

        :param bool $reset: 是否重置当前 QB 值
        :returns: 编译后的 SQL 语句字符串
        :rtype:    string

        编译 ``SELECT`` 语句并以字符串形式返回。

    .. php:method:: getCompiledInsert([$reset = true])

        :param bool $reset: 是否重置当前 QB 值
        :returns: 编译后的 SQL 语句字符串
        :rtype:     string

        编译 ``INSERT`` 语句并以字符串形式返回。

    .. php:method:: getCompiledUpdate([$reset = true])

        :param bool $reset: 是否重置当前 QB 值
        :returns: 编译后的 SQL 语句字符串
        :rtype:    string

        编译 ``UPDATE`` 语句并以字符串形式返回。

    .. php:method:: getCompiledDelete([$reset = true])

        :param bool $reset: 是否重置当前 QB 值
        :returns: 编译后的 SQL 语句字符串
        :rtype:    string

        编译 ``DELETE`` 语句并以字符串形式返回。
