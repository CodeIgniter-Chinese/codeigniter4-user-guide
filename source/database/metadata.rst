################
获取元数据
################

.. contents::
    :local:
    :depth: 2

**************
表元数据
**************

这些方法让你可以获取表信息。

列出数据库中的所有表
================================

$db->listTables()
-----------------

返回一个数组，其中包含当前连接的数据库中所有表的名称。示例：

.. literalinclude:: metadata/001.php

.. note:: 某些驱动程序包含额外的系统表，这些表不会包含在此返回结果中。

确定表是否存在
===========================

$db->tableExists()
------------------

在对某个特定表执行操作之前，知道该表是否存在会很有帮助。此方法返回布尔值 true/false。用法示例：

.. literalinclude:: metadata/002.php

.. note:: 将 *table_name* 替换为你正在查找的表名。

**************
字段元数据
**************

列出表中的所有字段
==========================

$db->getFieldNames()
--------------------

返回一个包含字段名称的数组。此查询可以通过两种方式调用：

1. 你可以提供表名，并从 ``$db`` 对象调用：

    .. literalinclude:: metadata/003.php

2. 你可以通过从查询结果对象调用该方法，来获取你运行的任何查询所关联的字段名称：

    .. literalinclude:: metadata/004.php

确定字段是否存在于表中
==========================================

$db->fieldExists()
------------------

在执行某个操作之前，知道特定字段是否存在会很有帮助。此方法返回布尔值 true/false。用法示例：

.. literalinclude:: metadata/005.php

.. note:: 将 *field_name* 和 *table_name* 分别替换为你正在查找的列名和表名。

获取字段元数据
=======================

.. _db-metadata-getfielddata:

$db->getFieldData()
-------------------

返回一个包含字段信息的对象数组。

有时收集字段名称或其他元数据（如列类型、最大长度等）会很有帮助。

.. note:: 并非所有数据库都提供元数据。

用法示例：

.. literalinclude:: metadata/006.php

如果数据库支持，此函数可返回以下数据：

- ``name`` - 字段名
- ``type`` - 字段的类型
- ``max_length`` - 字段的最大长度
- ``nullable`` - 如果字段可为空则为布尔值 ``true``，否则为布尔值 ``false``
- ``default`` - 默认值
- ``primary_key`` - 如果字段是主键则为整数 ``1`` （即使存在多个主键，也全为整数 ``1``），否则为整数 ``0`` （此字段当前仅在 ``MySQLi`` 和 ``SQLite3`` 中可用）

.. note:: 自 v4.4.0 版本起，SQLSRV 支持 ``nullable``。

$query->getFieldData()
----------------------

如果已经执行过查询，可以使用结果对象代替提供表名：

.. literalinclude:: metadata/007.php

.. note:: 返回的数据与 ``$db->getFieldData()`` 返回的数据不同。如果无法获取所需数据，请使用 ``$db->getFieldData()``。

列出表中的所有索引
===========================

.. _db-metadata-getindexdata:

$db->getIndexData()
-------------------

返回一个包含索引信息的对象数组。

用法示例：

.. literalinclude:: metadata/008.php

键的类型可能因你使用的数据库而异。例如，MySQL 会为表关联的每个键返回 primary、fulltext、spatial、index 或 unique 中的一种。

SQLite3 会返回一个名为 ``PRIMARY`` 的伪索引。但它是一个特殊索引，不能在 SQL 命令中使用。

.. _metadata-getforeignkeydata:

$db->getForeignKeyData()
------------------------

返回一个包含外键信息的对象数组。

用法示例：

.. literalinclude:: metadata/009.php

外键使用 ``tableprefix_table_column1_column2_foreign`` 命名约定。Oracle 使用略有不同的后缀 ``_fk``。
