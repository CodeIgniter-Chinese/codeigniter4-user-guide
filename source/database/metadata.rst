#################
数据库元数据
#################

.. 目录::
    :local:
    :depth: 2

**************
表元数据
**************

下面这些方法用于获取表信息。

列出数据库中的所有表
================================

**$db->listTables();**

返回一个数组，包含当前连接数据库的全部表名称。例如::

	$tables = $db->listTables();

	foreach ($tables as $table)
	{
		echo $table;
	}

检查表是否存在
===========================

**$db->tableExists();**

有时先检查某个表是否存在再进行操作会比较有用，
返回布尔值 TRUE/FALSE. 例如::

	if ($db->tableExists('table_name'))
	{
		// some code...
	}

.. note:: 使用你要查找的表名替换掉 table_name

**************
字段元数据
**************

列出表的所有字段
==========================

**$db->getFieldNames()**

返回包含字段名称的数组，有两种不同的调用方式：

1. 你可以调用 $db->object 的方法获取表的字段::

	$fields = $db->getFieldNames('table_name');

	foreach ($fields as $field)
	{
		echo $field;
	}

2. 你可以调用任何查询结果对象的方法获取所有字段::

	$query = $db->query('SELECT * FROM some_table');

	foreach ($query->getFieldNames() as $field)
	{
		echo $field;
	}

检查表中是否存在某字段 
==========================================

**$db->fieldExists()**

有时先确定某个字段是否存在再进行操作也比较有用，
该方法返回布尔值 TRUE/FALSE。
使用示例::

	if ($db->fieldExists('field_name', 'table_name'))
	{
		// some code...
	}

.. note:: 将 *field_name* 替换为你要查找的字段名, 并且将 *table_name*  替换为你要查找的表的名称

获取字段的元数据
=======================

**$db->getFieldData()**

该方法返回一个包含字段信息的对象数组。

有时，收集字段名称或相关的元数据会很有用，例如数据类型，最大长度等。

.. note:: 并非所有的数据库都支持元数据。

使用示例::

	$fields = $db->getFieldData('table_name');

	foreach ($fields as $field)
	{
		echo $field->name;
		echo $field->type;
		echo $field->max_length;
		echo $field->primary_key;
	}

如果你已经进行了查询，则可以使用结果对象而且不用提供表名::

	$query = $db->query("YOUR QUERY");
	$fields = $query->fieldData();

如果你的数据库支持，则可以用此方法获得以下数据:

-  name - 字段名
-  max_length - 字段的最大长度
-  primary_key - 等于1的话表示此字段是主键
-  type - 字段的数据类型

获取表的索引
===========================

**$db->getIndexData()**

返回一个包含索引信息的对象数组。

使用示例::

	$keys = $db->getIndexData('table_name');

	foreach ($keys as $key)
	{
		echo $key->name;
		echo $key->type;
		echo $key->fields;  // 字段名的数组
	}

根据数据库不同 type 会有所区别。
例如，MySQL会返回 primary、fulltext、spatial、index 或 unique 其中之一，
每个（索引）关联一张表。

**$db->getForeignKeyData()**

返回一个包含外键信息的对象数组。

使用示例::

	$keys = $db->getForeignKeyData('table_name');

	foreach ($keys as $key)
	{
		echo $key->constraint_name;
		echo $key->table_name;
		echo $key->column_name;
		echo $key->foreign_table_name;
		echo $key->foreign_column_name;
	}

对象字段根据你用的数据库会有不同，例如 SQLite3 不返回 column_name 字段，但会附加 *sequence* 字段用于解释复合外键。
