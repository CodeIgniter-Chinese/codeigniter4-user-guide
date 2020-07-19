##################################
数据库快速入门: 示例代码
##################################

这个页面包含的示例代码将简单介绍如何使用数据库类。更完整的信息请参考每个函数/类单独的介绍页面。

初始化数据库类
===============================

下面的代码将根据你的 :doc:`数据库配置 <configuration>` 加载并初始化数据库类::

	$db = \Config\Database::connect();

数据库类一旦载入，你就可以像下面介绍的那样使用它。

注意：如果你所有的页面都需要连接数据库，你可以让其自动加载。参见 :doc:`数据库连接 <connecting>`。

多结果标准查询（对象形式）
=====================================================

::

	$query = $db->query('SELECT name, title, email FROM my_table');
	$results = $query->getResult();

	foreach ($results as $row)
	{
		echo $row->title;
		echo $row->name;
		echo $row->email;
	}
	
	echo 'Total Results: ' . count($results);

上面的 getResult() 函数返回一个 **对象数组** 。例如：$row->title

多结果标准查询（数组形式）
====================================================

::

	$query = $db->query('SELECT name, title, email FROM my_table');
	$results = $query->getResultArray();

	foreach ($results as $row)
	{
		echo $row['title'];
		echo $row['name'];
		echo $row['email'];
	}

上面的 getResultArray() 函数返回一个 **二维数组** 。例如：$row['title']

单结果标准查询（对象形式）
=================================

::

	$query = $db->query('SELECT name FROM my_table LIMIT 1');
	$row = $query->getRow();
	echo $row->name;

上面的 getRow() 函数返回一个 **对象** 。例如：$row->name

单结果标准查询（数组形式）
=================================================

::

	$query = $db->query('SELECT name FROM my_table LIMIT 1');
	$row = $query->getRowArray();
	echo $row['name'];

上面的 getRowArray() 函数返回一个 **一维数组** 。例如：$row['name']

标准插入
===============

::

	$sql = "INSERT INTO mytable (title, name) VALUES (".$db->escape($title).", ".$db->escape($name).")";
	$db->query($sql);
	echo $db->getAffectedRows();

使用查询构造器查询数据
===========================

 :doc:`查询构造器模式 <query_builder>` 提供给我们一种简单的查询数据的途径::

	$query = $db->table('table_name')->get();
	
	foreach ($query->getResult() as $row)
	{
		echo $row->title;
	}

上面的 get() 函数从给定的表中查询出所有结果。 :doc:`查询构造器 <query_builder>`  提供了所有数据库操作的快捷函数。

使用查询构造器插入数据
============================

::

	$data = array(
		'title' => $title,
		'name' => $name,
		'date' => $date
	);
	
	$db->table('mytable')->insert($data);  // 生成: INSERT INTO mytable (title, name, date) VALUES ('{$title}', '{$name}', '{$date}')

