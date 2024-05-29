#################
数据库元数据
#################

.. contents::
    :local:
    :depth: 2

**************
表格元数据
**************

这些函数让你获取表格信息。

列出数据库中的表格
================================

$db->listTables()
-----------------

返回一个数组,其中包含当前连接数据库中的所有表格名称。例如:

.. literalinclude:: metadata/001.php

.. note:: 一些驱动程序有其他系统表被排除在此返回之外。

确定表格是否存在
===========================

$db->tableExists()
------------------

在对表运行操作之前,知道特定表格是否存在有时很有帮助。返回布尔值 true/false。用法示例:

.. literalinclude:: metadata/002.php

.. note:: 用你要查找的表格名称替换 *table_name*。

**************
字段元数据
**************

列出表中的字段
==========================

$db->getFieldNames()
--------------------

返回包含字段名称的数组。可以通过两种方式调用此查询:

1. 你可以提供表格名称并从 ``$db`` 对象调用它:

    .. literalinclude:: metadata/003.php

2. 你可以通过从查询结果对象调用函数来收集与任何查询关联的字段名称:

    .. literalinclude:: metadata/004.php

确定表中是否存在字段
==========================================

$db->fieldExists()
------------------

在执行操作之前,有时知道某个特定字段是否存在很有帮助。返回布尔值 true/false。用法示例:

.. literalinclude:: metadata/005.php

.. note:: 用你要查找的字段名称替换 *field_name*,并用你要查找的表格名称替换 *table_name*。

检索字段元数据
=======================

.. _db-metadata-getfielddata:

$db->getFieldData()
-------------------

返回包含字段信息的对象数组。

有时收集字段名称或其他元数据(如列类型、最大长度等)很有帮助。

.. note:: 并非所有数据库都提供元数据。

用法示例:

.. literalinclude:: metadata/006.php

如果你的数据库支持，下列数据可以通过此函数获取：

- ``name`` - 列名称
- ``type`` - 列的类型
- ``max_length`` - 列的最大长度
- ``nullable`` - 如果列允许为空，则为布尔值 ``true`` ，否则为布尔值 ``false``
- ``default`` - 默认值
- ``primary_key`` - 如果列是主键，则为整数 ``1``（即使有多个主键，所有主键值都是整数 ``1``），否则为整数 ``0``（此字段目前仅对 ``MySQLi`` 和 ``SQLite3`` 可用）

.. note:: 自 v4.4.0 起，SQLSRV 支持 ``nullable``。

$query->getFieldData()
----------------------

如果你已经运行了一个查询，可以使用结果对象而不是提供表名：

.. literalinclude:: metadata/007.php

.. note:: 返回的数据与 ``$db->getFieldData()`` 返回的数据不同。如果你无法获取所需的数据，请使用 ``$db->getFieldData()``。

列出表中的索引
===========================

.. _db-metadata-getindexdata:

$db->getIndexData()
-------------------

返回包含索引信息的对象数组。

用法示例:

.. literalinclude:: metadata/008.php

关键字类型可能是你使用的数据库所独有的。
例如,MySQL 将为与表关联的每个键返回 primary、fulltext、spatial、index 或 unique 中的一个。

SQLite3 返回一个名为 ``PRIMARY`` 的伪索引。但它是一个特殊的索引,你不能在 SQL 命令中使用它。

.. _metadata-getforeignkeydata:

$db->getForeignKeyData()
------------------------

返回包含外键信息的对象数组。

用法示例:

.. literalinclude:: metadata/009.php

外键使用命名约定 ``tableprefix_table_column1_column2_foreign``。Oracle 使用稍微不同的后缀 ``_fk``。
