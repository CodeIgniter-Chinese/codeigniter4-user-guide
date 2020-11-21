####################
数据库工厂类
####################

数据库工厂类（Database Forge）包含了帮助你管理你的数据库的一些相关方法。

.. contents::
    :local:
    :depth: 2

****************************
初始化 Forge 类
****************************

.. important:: 为了初始化forge类，你的数据库驱动程序必须已经在运行，因为forge类是依赖它运行的。

加载 Forge 类的代码如下::

	$forge = \Config\Database::forge();

你可以将另外一个数据可组名传递给 DB Forge加载程序，以防要管理的数据库不是默认数据库::

	$this->myforge = $this->load->dbforge('other_db');

在上面的示例中，我们传递的是另一个数据库的名称作为第一个参数来连接。

*******************************
创建和删除数据库
*******************************

**$forge->createDatabase('db_name')**

用于创建指定数据库，根据成败返回 TRUE 或 FALSE::

	if ($forge->createDatabase('my_db'))
	{
		echo 'Database created!';
	}

**$forge->dropDatabase('db_name')**

用于删除指定数据库，根据成败返回 TRUE 或 FALSE::

	if ($forge->dropDatabase('my_db'))
	{
		echo 'Database deleted!';
	}

****************************
创建和删除数据表
****************************

在创建表时，你可能希望做一些事情。如添加字段，向表中添加键，更改列。CodeIgniter 为此提供了一种机制。

添加字段
=============

字段是通过关联数组创建的。在数组中，必须包括与字段的数据类型相关的'type'键。例如，int、varchar、text等。许多数据类型（例如varchar）还需要“约束”键。

::

	$fields = array(
		'users' => array(
			'type'       => 'VARCHAR',
			'constraint' => '100',
		),
	);
	// 添加字段时将转换为"users VARCHAR(100)"。

此外，可以使用以下键/值:

-  unsigned/true : 在字段定义中生成 "UNSIGNED" 。
-  default/value : 在字段定义中生成默认值。
-  null/true : 在字段定义中生成"NULL"。如果没有这个，该字段将默认为"NOT NULL"。
-  auto_increment/true : 在字段上生成auto_increment标志。请注意，字段类型必须是支持此类型的类型，例如整数。
-  unique/true : 为字段定义生成唯一键。

::

	$fields = array(
		'blog_id'          => array(
			'type'           => 'INT',
			'constraint'     => 5,
			'unsigned'       => TRUE,
			'auto_increment' => TRUE
		),
		'blog_title'       => array(
			'type'           => 'VARCHAR',
			'constraint'     => '100',
			'unique'         => TRUE,
		),
		'blog_author'      => array(
			'type'           =>'VARCHAR',
			'constraint'     => '100',
			'default'        => 'King of Town',
		),
		'blog_description' => array(
			'type'           => 'TEXT',
			'null'           => TRUE,
		),
	);

定义字段后，可以使用 ``$forge->addField($fields);`` 然后调用 ``createTable()`` 方法。

**$forge->addField()**

add fields方法将接受上述数组。

将字符串作为字段传递
-------------------------

如果你确切知道要如何创建字段，可以使用addField()方法将字符串传递给字段定义

::

	$forge->addField("label varchar(100) NOT NULL DEFAULT 'default label'");

.. note:: 将原始字符串作为字段传递后，不能用 ``add_key()`` 对这些字段进行调用。

.. note:: 对 add_field() 的多次调用是累积的。

创建一个id字段
--------------------

创建id字段有一个特殊例外。具有类型id的字段将自动分配为 INT(9) auto_incrementing 主键。

::

	$forge->addField('id');
	// 提出 id INT(9) NOT NULL AUTO_INCREMENT

添加键
===========

通常来说，表都会有键。这可以使用 $forge->addKey('field')方法来实现。第二个参数设置是可选的，设置为 TRUE 将使其成为主键，
第三个参数设置为 TRUE 将使其成为唯一键。注意 addKey()方法必须紧跟在createTable()方法后面。

包含多列的非主键必须使用数组来添加，下面是 MySQL 的例子。

::

	$forge->addKey('blog_id', TRUE);
	// gives PRIMARY KEY `blog_id` (`blog_id`)

	$forge->addKey('blog_id', TRUE);
	$forge->addKey('site_id', TRUE);
	// gives PRIMARY KEY `blog_id_site_id` (`blog_id`, `site_id`)

	$forge->addKey('blog_name');
	// gives KEY `blog_name` (`blog_name`)

	$forge->addKey(array('blog_name', 'blog_label'));
	// gives KEY `blog_name_blog_label` (`blog_name`, `blog_label`)

	$forge->addKey(array('blog_id', 'uri'), FALSE, TRUE);
	// gives UNIQUE KEY `blog_id_uri` (`blog_id`, `uri`)

为了使代码读取更加客观，还可以使用特定的方法添加主键和唯一键。::

	$forge->addPrimaryKey('blog_id');
	// gives PRIMARY KEY `blog_id` (`blog_id`)

外键有助于跨表强制执行关系和操作。对于支持外键的表，可以直接在forge中添加它们。::

	$forge->addUniqueKey(array('blog_id', 'uri'));
	// gives UNIQUE KEY `blog_id_uri` (`blog_id`, `uri`)


添加外键
===================

::

        $forge->addForeignKey('users_id','users','id');
        // gives CONSTRAINT `TABLENAME_users_foreign` FOREIGN KEY(`users_id`) REFERENCES `users`(`id`)

你可以为约束的 "on delete" 和 "on update" 属性指定所需的操作::

        $forge->addForeignKey('users_id','users','id','CASCADE','CASCADE');
        // gives CONSTRAINT `TABLENAME_users_foreign` FOREIGN KEY(`users_id`) REFERENCES `users`(`id`) ON DELETE CASCADE ON UPDATE CASCADE

创建表格
================

声明字段和键后，你可以根据如下代码创建一张新表

::

	$forge->createTable('table_name');
	// gives CREATE TABLE table_name

可选的第二个参数设置为TRUE时会在定义中添加"IF NOT EXISTS"子句

::

	$forge->createTable('table_name', TRUE);
	// gives CREATE TABLE IF NOT EXISTS table_name

你还可以传递可选的表属性，例如MySQL的 ``ENGINE``::

	$attributes = array('ENGINE' => 'InnoDB');
	$forge->createTable('table_name', FALSE, $attributes);
	// produces: CREATE TABLE `table_name` (...) ENGINE = InnoDB DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci

.. note:: 除非你指定 ``CHARACTER SET`` 和/或 ``COLLATE`` 属性,
	``createTable()`` 否则将始终使用你配置的 *charset*
	和 *DBCollat* 值, 只要它们不为空 (仅限MySQL).

删除表
================

执行DROP TABLE语句时，可以选择添加一个IF EXISTS子句。

::

	// Produces: DROP TABLE table_name
	$forge->dropTable('table_name');

	// Produces: DROP TABLE IF EXISTS table_name
	$forge->dropTable('table_name',TRUE);

删除外键
======================

执行一个删除外键语句。

::

	// Produces: ALTER TABLE 'tablename' DROP FOREIGN KEY 'users_foreign'
	$forge->dropForeignKey('tablename','users_foreign');

.. note:: SQLite数据库驱动程序不支持删除外键。

重命名表
================

执行表重命名

::

	$forge->renameTable('old_table_name', 'new_table_name');
	// gives ALTER TABLE old_table_name RENAME TO new_table_name

****************
修改表
****************

向表中添加列
==========================

**$forge->addColumn()**

使用 ``addColumn()`` 方法用于对现有数据表进行修改，它的参数和上面介绍的字段数组一样，并且可以用于无限数量的附加字段。

::

	$fields = array(
		'preferences' => array('type' => 'TEXT')
	);
	$forge->addColumn('table_name', $fields);
	// Executes: ALTER TABLE table_name ADD preferences TEXT

如果你使用 MySQL 或 CUBIRD ，你可以使用 AFTER 和 FIRST 语句来为新添加的列指定位置。

例如::

	// Will place the new column after the `another_field` column:
	$fields = array(
		'preferences' => array('type' => 'TEXT', 'after' => 'another_field')
	);

	// Will place the new column at the start of the table definition:
	$fields = array(
		'preferences' => array('type' => 'TEXT', 'first' => TRUE)
	);

从表中删除列
==============================

**$forge->dropColumn()**

该语句用于从表中删除列。

::

	$forge->dropColumn('table_name', 'column_to_drop');

从表中的修改列
=============================

**$forge->modifyColumn()**

此方法的用法与 ``add_column()`` 相同，只是它是更改现有列，而不是添加新列。为了更改名称，可以将“名称”键添加到字段定义数组中。

::

	$fields = array(
		'old_name' => array(
			'name' => 'new_name',
			'type' => 'TEXT',
		),
	);
	$forge->modifyColumn('table_name', $fields);
	// gives ALTER TABLE table_name CHANGE old_name new_name TEXT

***************
类引用
***************

.. php:class:: \CodeIgniter\Database\Forge

	.. php:method:: addColumn($table[, $field = array()])

		:param	string	$table: Table name to add the column to
		:param	array	$field: Column definition(s)
		:returns:	TRUE on success, FALSE on failure
		:rtype:	bool

		Adds a column to a table. Usage:  See `Adding a Column to a Table`_.

	.. php:method:: addField($field)

		:param	array	$field: Field definition to add
		:returns:	\CodeIgniter\Database\Forge instance (method chaining)
		:rtype:	\CodeIgniter\Database\Forge

                Adds a field to the set that will be used to create a table. Usage:  See `Adding fields`_.

	.. php:method:: addKey($key[, $primary = FALSE[, $unique = FALSE]])

		:param	mixed	$key: Name of a key field or an array of fields
		:param	bool	$primary: Set to TRUE if it should be a primary key or a regular one
		:param	bool	$unique: Set to TRUE if it should be a unique key or a regular one
		:returns:	\CodeIgniter\Database\Forge instance (method chaining)
		:rtype:	\CodeIgniter\Database\Forge

		Adds a key to the set that will be used to create a table. Usage:  See `Adding Keys`_.

	.. php:method:: addPrimaryKey($key)

		:param	mixed	$key: Name of a key field or an array of fields
		:returns:	\CodeIgniter\Database\Forge instance (method chaining)
		:rtype:	\CodeIgniter\Database\Forge

		Adds a primary key to the set that will be used to create a table. Usage:  See `Adding Keys`_.

	.. php:method:: addUniqueKey($key)

		:param	mixed	$key: Name of a key field or an array of fields
		:returns:	\CodeIgniter\Database\Forge instance (method chaining)
		:rtype:	\CodeIgniter\Database\Forge

		Adds an unique key to the set that will be used to create a table. Usage:  See `Adding Keys`_.

	.. php:method:: createDatabase($db_name)

		:param	string	$db_name: Name of the database to create
		:returns:	TRUE on success, FALSE on failure
		:rtype:	bool

		Creates a new database. Usage:  See `Creating and Dropping Databases`_.

	.. php:method:: createTable($table[, $if_not_exists = FALSE[, array $attributes = array()]])

		:param	string	$table: Name of the table to create
		:param	string	$if_not_exists: Set to TRUE to add an 'IF NOT EXISTS' clause
		:param	string	$attributes: An associative array of table attributes
		:returns:  TRUE on success, FALSE on failure
		:rtype:	bool

		Creates a new table. Usage:  See `Creating a table`_.

	.. php:method:: dropColumn($table, $column_name)

		:param	string	$table: Table name
		:param	array	$column_name: The column name to drop
		:returns:	TRUE on success, FALSE on failure
		:rtype:	bool

		Drops a column from a table. Usage:  See `Dropping a Column From a Table`_.

	.. php:method:: dropDatabase($db_name)

		:param	string	$db_name: Name of the database to drop
		:returns:	TRUE on success, FALSE on failure
		:rtype:	bool

		Drops a database. Usage:  See `Creating and Dropping Databases`_.

	.. php:method:: dropTable($table_name[, $if_exists = FALSE])

		:param	string	$table: Name of the table to drop
		:param	string	$if_exists: Set to TRUE to add an 'IF EXISTS' clause
		:returns:	TRUE on success, FALSE on failure
		:rtype:	bool

		Drops a table. Usage:  See `Dropping a table`_.

	.. php:method:: modifyColumn($table, $field)

		:param	string	$table: Table name
		:param	array	$field: Column definition(s)
		:returns:	TRUE on success, FALSE on failure
		:rtype:	bool

		Modifies a table column. Usage:  See `Modifying a Column in a Table`_.

	.. php:method:: renameTable($table_name, $new_table_name)

		:param	string	$table: Current of the table
		:param	string	$new_table_name: New name of the table
		:returns:	TRUE on success, FALSE on failure
		:rtype:	bool

		Renames a table. Usage:  See `Renaming a table`_.
