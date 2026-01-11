####################
数据库 Forge 类
####################

数据库 Forge 类包含帮助你管理数据库的方法。

.. contents::
    :local:
    :depth: 2

****************************
初始化 Forge 类
****************************

.. important:: 为了初始化 Forge 类，数据库驱动程序必须已经在运行，因为 Forge 类依赖于它。

这样加载 Forge 类：

.. literalinclude:: forge/001.php

你也可以将另一个数据库组名传递给 DB Forge 加载器，以防要管理的数据库不是默认的：

.. literalinclude:: forge/002.php

在上面的示例中，我们将不同的数据库组名作为第一个参数传递进行连接。

*******************************
创建和删除数据库
*******************************

$forge->createDatabase('db_name')
=================================

允许你创建第一个参数中指定的数据库。根据成功或失败返回 true/false：

.. literalinclude:: forge/003.php

可选的第二个参数设置为 true 将添加 ``IF EXISTS`` 语句，或者在创建前检查数据库是否存在（取决于 DBMS）。

.. literalinclude:: forge/004.php

$forge->dropDatabase('db_name')
===============================

允许你删除第一个参数中指定的数据库。根据成功或失败返回 true/false：

.. literalinclude:: forge/005.php

在命令行中创建数据库
======================================

CodeIgniter 支持使用专用的 ``db:create`` 命令直接从你喜爱的终端创建数据库。使用此命令时假定数据库尚不存在。否则，CodeIgniter 将提示数据库创建失败。

开始只需输入命令和数据库名称（例如，``foo``）：

.. code-block:: console

    php spark db:create foo

如果一切顺利，你应该会看到 ``Database "foo" successfully created.`` 消息显示。

如果你在测试环境中或使用 SQLite3 驱动程序，可以使用 ``--ext`` 选项传入文件扩展名来指定创建数据库的文件。有效值为 ``db`` 和
``sqlite``，默认为 ``db``。记住这些值前面不应有句号。

.. code-block:: console

    php spark db:create foo --ext sqlite

上述命令将在 **WRITEPATH/foo.sqlite** 中创建数据库文件。

.. note:: 使用特殊的 SQLite3 数据库名称 ``:memory:`` 时，预期命令仍会
    产生成功消息但不会创建数据库文件。这是因为 SQLite3 只会使用
    内存数据库。

***************
创建表
***************

创建表时你可能希望做几件事。添加字段、向表添加键、修改字段。CodeIgniter 为此提供了一种机制。

.. _adding-fields:

添加字段
=============

$forge->addField()
------------------

字段通常通过关联数组创建。在数组中，必须包含与字段数据类型相关的 ``type`` 键。

例如，``INT``、``VARCHAR``、``TEXT`` 等。
许多数据类型（例如 ``VARCHAR``）还需要 ``constraint`` 键。

.. literalinclude:: forge/006.php

此外，可以使用以下键/值：

-  ``unsigned``/true : 在字段定义中生成 ``UNSIGNED``。
-  ``default``/value : 在字段定义中生成 ``DEFAULT`` 约束。
-  ``null``/true : 在字段定义中生成 ``NULL``。如果没有此项，字段将默认为 ``NOT NULL``。
-  ``auto_increment``/true : 在字段上生成 auto_increment 标志。注意，字段类型必须是支持此功能的类型，例如 ``INTEGER``。
-  ``unique``/true : 为字段定义生成唯一键。

.. literalinclude:: forge/007.php

定义字段后，可以使用
``$forge->addField($fields)`` 添加它们，然后调用
:ref:`createTable() <creating-a-table>` 方法。

数据类型说明
-------------------

浮点类型
^^^^^^^^^^^^^^^^^^^^

浮点类型如 ``FLOAT`` 和 ``DOUBLE`` 表示近似值。
因此，当需要精确值时不应使用它们。

::

    mysql> CREATE TABLE t (f FLOAT, d DOUBLE);
    mysql> INSERT INTO t VALUES(99.9, 99.9);

    mysql> SELECT * FROM t WHERE f=99.9;
    Empty set (0.00 sec)

    mysql> SELECT * FROM t WHERE f > 99.89 AND f < 99.91;
    +------+------+
    | f    | d    |
    +------+------+
    | 99.9 | 99.9 |
    +------+------+
    1 row in set (0.01 sec)

当需要保持精确精度时，例如货币数据，
应使用 ``DECIMAL`` 或 ``NUMERIC``。

TEXT
^^^^

``TEXT`` 不应在 SQLSRV 上使用。它已被弃用。
参见 `ntext, text, and image (Transact-SQL) - SQL Server | Microsoft Learn <https://learn.microsoft.com/en-us/sql/t-sql/data-types/ntext-text-and-image-transact-sql?view=sql-server-ver16>`_。

ENUM
^^^^

并非所有数据库都支持 ``ENUM``。

从 v4.5.0 开始，``SQLSRV`` Forge 将 ``ENUM`` 数据类型转换为 ``VARCHAR(n)``。
先前版本转换为 ``TEXT``。

.. _forge-addfield-default-value-rawsql:

将原始 SQL 字符串作为默认值
---------------------------------

.. versionadded:: 4.2.0

从 v4.2.0 开始，``$forge->addField()`` 接受 ``CodeIgniter\Database\RawSql`` 实例，它表示原始 SQL 字符串。

.. literalinclude:: forge/027.php

.. warning:: 使用 ``RawSql`` 时，必须手动转义数据。否则可能导致 SQL 注入。

将字符串作为字段传递
-------------------------

如果你确切知道希望如何创建字段，可以将
字符串传入字段定义中，使用 ``addField()``：

.. literalinclude:: forge/008.php

.. note:: 将原始字符串作为字段传递后，不能对这些字段调用 ``addKey()``。

.. note:: 多次调用 ``addField()`` 是累积的。

创建 id 字段
--------------------

创建 id 字段有特殊例外。类型为 id 的字段将自动被分配为 INT(9) auto_incrementing 主键。

.. literalinclude:: forge/009.php

.. _adding-keys:

添加键
===========

$forge->addKey()
----------------

一般来说，你会希望表具有键。这可以通过
``$forge->addKey('field')`` 完成。可选的第二个参数设置为 true 将使其成为主键，第三个参数设置为 true 将使其成为唯一键。你可以使用第四个参数指定名称。注意 ``addKey()`` 必须后跟对 ``createTable()`` 的调用，或者当表已存在时调用 ``processIndexes()``。

多个非主键字段必须以数组形式发送。下面的示例输出适用于 MySQL。

.. literalinclude:: forge/010.php

$forge->addPrimaryKey()
-----------------------

$forge->addUniqueKey()
----------------------

为了使代码更易读，也可以使用特定方法添加主键和唯一键：

.. literalinclude:: forge/011.php

.. note:: 添加主键时，MySQL 和 SQLite 将假定名称为 ``PRIMARY``，即使提供了名称。

.. _adding-foreign-keys:

添加外键
===================

外键有助于在表之间强制执行关系和操作。对于支持外键的表，
可以直接在 forge 中添加它们：

.. literalinclude:: forge/012.php

你可以指定约束的 "on update" 和 "on delete" 属性的所需操作以及名称：

.. literalinclude:: forge/013.php

.. note:: SQLite3 不支持外键命名。CodeIgniter 将通过 ``prefix_table_column_foreign`` 引用它们。

.. _creating-a-table:

创建表
================

声明字段和键后，可以使用以下命令创建新表

.. literalinclude:: forge/014.php

可选的第二个参数设置为 true 将仅在表尚不存在时创建表。

.. literalinclude:: forge/015.php

你也可以传递可选的表属性，例如 MySQL 的 ``ENGINE``：

.. literalinclude:: forge/016.php

.. note:: 除非指定 ``CHARACTER SET`` 和/或 ``COLLATE`` 属性，
    ``createTable()`` 将始终使用你配置的 *charset*
    和 *DBCollat* 值添加它们，只要它们不为空（仅 MySQL）。

***************
删除表
***************

删除表
================

执行 ``DROP TABLE`` 语句并可选择添加 ``IF EXISTS`` 子句。

.. literalinclude:: forge/017.php

可以传递第三个参数以添加 ``CASCADE`` 选项，某些驱动程序可能需要此选项来处理具有外键的表的删除。

.. literalinclude:: forge/018.php

****************
修改表
****************

向表中添加字段
=========================

$forge->addColumn()
-------------------

``addColumn()`` 方法用于修改现有表。它
接受与 :ref:`创建表 <adding-fields>` 相同的字段数组，并且可以
用于添加额外字段。

.. note:: 与创建表时不同，如果未指定 ``null``，列
    将为 ``NULL``，而不是 ``NOT NULL``。

.. literalinclude:: forge/022.php

如果使用 MySQL 或 CUBIRD，可以利用它们的
``AFTER`` 和 ``FIRST`` 子句来定位新字段。

示例：

.. literalinclude:: forge/023.php

从表中删除字段
============================

.. _db-forge-dropColumn:

$forge->dropColumn()
--------------------

用于从表中删除列。

.. literalinclude:: forge/024.php

用于从表中删除多个列。

.. literalinclude:: forge/025.php

修改表中的字段
============================

.. _db-forge-modifyColumn:

$forge->modifyColumn()
----------------------

此方法的用法与 ``addColumn()`` 相同，只是它
修改现有字段而不是添加新字段。为了
更改名称，可以在字段定义数组中添加 "name" 键。

.. literalinclude:: forge/026.php

.. note:: ``modifyColumn()`` 可能会意外更改 ``NULL``/``NOT NULL``。
    因此建议始终为 ``null`` 键指定值。与创建表时不同，
    如果未指定 ``null``，字段将为 ``NULL``，而不是 ``NOT NULL``。

.. note:: 由于错误，在 v4.3.4 之前，SQLite3 即使指定 ``'null' => false`` 也可能不设置 ``NOT NULL``。

.. note:: 由于错误，在 v4.3.4 之前，Postgres 和 SQLSRV 即使指定 ``'null' => true`` 也会设置 ``NOT NULL``。

.. _db-forge-adding-keys-to-a-table:

向表添加键
======================

.. versionadded:: 4.3.0

可以使用 ``addKey()``、``addPrimaryKey()``、
``addUniqueKey()`` 或 ``addForeignKey()`` 和 ``processIndexes()`` 向现有表添加键：

.. literalinclude:: forge/029.php

.. _dropping-a-primary-key:

删除主键
======================

.. versionadded:: 4.3.0

执行 DROP PRIMARY KEY。

.. literalinclude:: forge/028.php

删除键
===============

执行 DROP KEY。

.. literalinclude:: forge/020.php

删除外键
======================

执行 DROP FOREIGN KEY。

.. literalinclude:: forge/019.php

重命名表
================

执行 TABLE 重命名

.. literalinclude:: forge/021.php

***************
类参考
***************

.. php:namespace:: CodeIgniter\Database

.. php:class:: Forge

    .. php:method:: addColumn($table[, $field = []])

        :param    string    $table: 要添加字段的表名
        :param    array    $field: 列定义
        :returns:    成功时返回 true，失败时返回 false
        :rtype:    bool

        向现有表添加z字段。用法：参见 `向表中添加字段`_。

    .. php:method:: addField($field)

        :param    array    $field: 要添加的字段定义
        :returns:    ``\CodeIgniter\Database\Forge`` 实例（方法链）
        :rtype:    ``\CodeIgniter\Database\Forge``

        向将用于创建表的集合添加字段。用法：参见 `添加字段`_。

    .. php:method:: addForeignKey($fieldName, $tableName, $tableField[, $onUpdate = '', $onDelete = '', $fkName = ''])

        :param    string|string[]    $fieldName: 键字段名称或字段数组
        :param    string    $tableName: 父表名称
        :param    string|string[]    $tableField: 父表字段名称或字段数组
        :param    string    $onUpdate: "on update" 的所需操作
        :param    string    $onDelete: "on delete" 的所需操作
        :param    string    $fkName: 外键名称。这不适用于 SQLite3
        :returns:    ``\CodeIgniter\Database\Forge`` 实例（方法链）
        :rtype:    ``\CodeIgniter\Database\Forge``

        向将用于创建表的集合添加外键。用法：参见 `添加外键`_。

        .. note:: 从 v4.3.0 起可以使用 ``$fkName``。

    .. php:method:: addKey($key[, $primary = false[, $unique = false[, $keyName = '']]])

        :param    mixed    $key: 键字段名称或字段数组
        :param    bool    $primary: 如果应为主键则设置为 true，否则为常规键
        :param    bool    $unique: 如果应为唯一键则设置为 true，否则为常规键
        :param    string    $keyName: 要添加的键名称
        :returns:    ``\CodeIgniter\Database\Forge`` 实例（方法链）
        :rtype:    ``\CodeIgniter\Database\Forge``

        向将用于创建表的集合添加键。用法：参见 `添加键`_。

        .. note:: 从 v4.3.0 起可以使用 ``$keyName``。

    .. php:method:: addPrimaryKey($key[, $keyName = ''])

        :param    mixed    $key: 键字段名称或字段数组
        :param    string    $keyName: 要添加的键名称
        :returns:    ``\CodeIgniter\Database\Forge`` 实例（方法链）
        :rtype:    ``\CodeIgniter\Database\Forge``

        向将用于创建表的集合添加主键。用法：参见 `添加键`_。

        .. note:: 从 v4.3.0 起可以使用 ``$keyName``。

    .. php:method:: addUniqueKey($key[, $keyName = ''])

        :param    mixed    $key: 键字段名称或字段数组
        :param    string    $keyName: 要添加的键名称
        :returns:    ``\CodeIgniter\Database\Forge`` 实例（方法链）
        :rtype:    ``\CodeIgniter\Database\Forge``

        向将用于创建表的集合添加唯一键。用法：参见 `添加键`_。

        .. note:: 从 v4.3.0 起可以使用 ``$keyName``。

    .. php:method:: createDatabase($dbName[, $ifNotExists = false])

        :param    string    $db_name: 要创建的数据库名称
        :param    string    $ifNotExists: 设置为 true 以添加 ``IF NOT EXISTS`` 子句或检查数据库是否存在
        :returns:    成功时返回 true，失败时返回 false
        :rtype:    bool

        创建新数据库。用法：参见 `创建和删除数据库`_。

    .. php:method:: createTable($table[, $if_not_exists = false[, array $attributes = []]])

        :param    string    $table: 要创建的表名称
        :param    string    $if_not_exists: 设置为 true 以添加 ``IF NOT EXISTS`` 子句
        :param    string    $attributes: 表属性的关联数组
        :returns:  成功时返回查询对象，失败时返回 false
        :rtype:    mixed

        创建新表。用法：参见 `创建表`_。

    .. php:method:: dropColumn($table, $columnNames)

        :param    string    $table: 表名
        :param    mixed    $columnNames: 逗号分隔的字符串或列名数组
        :returns:    成功时返回 true，失败时返回 false
        :rtype:    bool

        从表中删除单个或多个列。用法：参见 `从表中删除字段`_。

    .. php:method:: dropDatabase($dbName)

        :param    string    $dbName: 要删除的数据库名称
        :returns:    成功时返回 true，失败时返回 false
        :rtype:    bool

        删除数据库。用法：参见 `创建和删除数据库`_。

    .. php:method:: dropKey($table, $keyName[, $prefixKeyName = true])

        :param    string    $table: 具有键的表名
        :param    string    $keyName: 要删除的键名称
        :param    string    $prefixKeyName: 是否应将数据库前缀添加到 ``$keyName``
        :returns:    成功时返回 true，失败时返回 false
        :rtype:    bool

        删除索引或唯一索引。

        .. note:: 从 v4.3.0 起可以使用 ``$keyName`` 和 ``$prefixKeyName``。

    .. php:method:: dropPrimaryKey($table[, $keyName = ''])

        :param    string    $table: 要删除主键的表名
        :param    string    $keyName: 要删除的主键名称
        :returns:    成功时返回 true，失败时返回 false
        :rtype:    bool

        从表中删除主键。

        .. note:: 从 v4.3.0 起可以使用 ``$keyName``。

    .. php:method:: dropTable($table_name[, $if_exists = false])

        :param    string    $table: 要删除的表名称
        :param    string    $if_exists: 设置为 true 以添加 ``IF EXISTS`` 子句
        :returns:    成功时返回 true，失败时返回 false
        :rtype:    bool

        删除表。用法：参见 `删除表`_。

    .. php:method:: processIndexes($table)

        .. versionadded:: 4.3.0

        :param    string    $table: 要添加索引的表名称
        :returns:    成功时返回 true，失败时返回 false
        :rtype:    bool

        在 ``addKey()``、``addPrimaryKey()``、``addUniqueKey()``
        和 ``addForeignKey()`` 之后使用，向现有表添加索引。
        参见 `向表添加键`_。

    .. php:method:: modifyColumn($table, $field)

        :param    string    $table: 表名
        :param    array    $field: 列定义
        :returns:    成功时返回 true，失败时返回 false
        :rtype:    bool

        修改表列。用法：参见 `修改表中的字段`_。

    .. php:method:: renameTable($tableName, $newTableName)

        :param    string    $tableName: 表的当前名称
        :param    string    $newTableName: 表的新名称
        :returns:  成功时返回查询对象，失败时返回 false
        :rtype:    mixed

        重命名表。用法：参见 `重命名表`_。
