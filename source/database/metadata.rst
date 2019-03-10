#################
数据库元数据
#################

.. contents::
    :local:
    :depth: 2

**************
表元数据
**************

下面这些方法用于获取表信息。

列出数据库中的所有表
================================

**$db->listTables();**

返回一个数组，其中包含当前连接到的数据库中所有表的数组。例如::

	$tables = $db->listTables();

	foreach ($tables as $table)
	{
		echo $table;
	}

检查表是否存在
===========================

**$db->tableExists();**

有时，在对其执行操作之前知道特定表是否存在是有帮助的。
返回布尔值 TRUE/FALSE. 例如::

	if ($db->tableExists('table_name'))
	{
		// some code...
	}

.. 注意:: 使用你要查找的表名替换掉 table_name


**************
字段元数据
**************

列出表中的所有列
==========================

**$db->getFieldNames()**

返回包含字段名称的数组。 有两种不同的调用方式：

1.你可以提供表名称从 $db->object 中调用它::

	$fields = $db->getFieldNames('table_name');

	foreach ($fields as $field)
	{
		echo $field;
	}

2.你可以从任何查询结果对象上调用该方法，获取查询返回的所有字段::

	$query = $db->query('SELECT * FROM some_table');

	foreach ($query->getFieldNames() as $field)
	{
		echo $field;
	}

检查表中是否存在某字段 
==========================================

**$db->fieldExists()**

有时，在执行一个操作之前先确定某个字段是否存在是很有用的。该方法返回布尔值 TRUE/FALSE。
使用示例::

	if ($db->fieldExists('field_name', 'table_name'))
	{
		// some code...
	}

.. 注意:: 将 *field_name* 替换为你要查找的字段名, 并且将 *table_name* 替换为你要查找的表的名称


获取字段的元数据
=======================

**$db->getFieldData()**

该方法返回一个包含字段信息的对象数组。

有时，收集字段名称或相关的元数据会很有用的，例如数据类型，最大长度等。

.. 注意:: 并非所有的数据库都支持元数据。

使用示例::

	$fields = $db->getFieldData('table_name');

	foreach ($fields as $field)
	{
		echo $field->name;
		echo $field->type;
		echo $field->max_length;
		echo $field->primary_key;
	}

如果你已经进行了查询，则可以使用结果对象而不是提供表格名::

	$query = $db->query("YOUR QUERY");
	$fields = $query->fieldData();

如果你的数据库支持，则可以从此函数获得以下数据:

-  name - 字段名
-  max_length - 字段的最大长度
-  primary_key - 等于1的话表示此字段是主键
-  type - 字段的数据类型

列出表格中的索引
===========================

**$db->getIndexData()**

请写下来，有人……