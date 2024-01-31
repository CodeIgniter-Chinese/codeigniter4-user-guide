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

.. important:: 为了初始化 Forge 类,你的数据库驱动程序必须已经运行,因为 Forge 类依赖于它。

如下加载 Forge 类:

.. literalinclude:: forge/001.php

你也可以向 DB Forge 加载器传递另一个数据库组名称,以防要管理的数据库不是默认数据库:

.. literalinclude:: forge/002.php

在上面的示例中,我们正在作为第一个参数传递一个不同的数据库组名称进行连接。

*******************************
创建和删除数据库
*******************************

$forge->createDatabase('db_name')
=================================

允许你创建第一个参数中指定的数据库。基于成功或失败返回 true/false:

.. literalinclude:: forge/003.php

可选的第二个参数设置为 true 将添加 ``IF EXISTS`` 语句或检查数据库是否存在,然后再创建它(取决于 DBMS)。

.. literalinclude:: forge/004.php

$forge->dropDatabase('db_name')
===============================

允许你删除第一个参数中指定的数据库。基于成功或失败返回 true/false:

.. literalinclude:: forge/005.php

在命令行中创建数据库
======================================

CodeIgniter 支持直接从喜欢的终端使用专用的 ``db:create`` 命令创建数据库。通过使用此命令,假定数据库还不存在。否则,CodeIgniter 将抱怨数据库创建失败。

首先,只需键入命令和数据库名称(例如 ``foo``):

.. code-block:: console

    php spark db:create foo

如果一切顺利,你应该会看到显示的 ``Database "foo" successfully created.`` 消息。

如果你在测试环境中或正在使用 SQLite3 驱动程序,可以使用 ``--ext`` 选项
为将创建数据库的文件传递文件扩展名。有效值为 ``db`` 和 ``sqlite``,默认为 ``db``。请记住,这些前面不应有句点。
:

.. code-block:: console

    php spark db:create foo --ext sqlite

上述命令将创建名为 **WRITEPATH/foo.sqlite** 的数据库文件。

.. note:: 当使用特殊的 SQLite3 数据库名称 ``:memory:`` 时,请注意命令仍会生成成功消息,但不会创建数据库文件。这是因为 SQLite3 将只使用内存中的数据库。

***************
创建表
***************

在创建表时,你可能希望执行几件事。添加字段、向表添加键、更改列。CodeIgniter 为此提供了一种机制。

.. _adding-fields:

添加字段
=============

$forge->addField()
------------------

字段通常通过关联数组创建。在数组中,你必须包含与字段的数据类型相关的 ``type`` 键。

例如, ``INT``、``VARCHAR``、``TEXT`` 等。许多数据类型(例如 ``VARCHAR``)还需要一个 ``constraint`` 键。

.. literalinclude:: forge/006.php

另外,可以使用以下键/值:

- ``unsigned``/true : 在字段定义中生成 ``UNSIGNED``。
- ``default``/value : 在字段定义中生成 ``DEFAULT`` 约束。
- ``null``/true : 在字段定义中生成 ``null``。如果不指定,字段将默认为 ``NOT null``。
- ``auto_increment``/true : 在字段上生成 auto_increment 标志。请注意,字段类型必须是支持这一点的类型,如 ``INTEGER``。
- ``unique``/true : 为字段定义生成唯一键。

.. literalinclude:: forge/007.php

在定义了字段后,可以使用 ``$forge->addField($fields)`` 后跟对 :ref:`createTable() <creating-a-table>` 方法的调用来添加它们。

关于数据类型的注解
-------------------

浮点类型
^^^^^^^^^^^^^^^^^^^^

浮点类型，如 ``FLOAT`` 和 ``DOUBLE``，表示的是近似值。因此，当需要精确值时，不应使用它们。

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

当需要保存精确的精度时，例如在处理货币数据，应使用 ``DECIMAL`` 或 ``NUMERIC``。

TEXT
^^^^

SQLSRV 上不应使用 ``TEXT``，它已被弃用。
欲知详情，请参见 `ntext, text, 和 image (Transact-SQL) - SQL Server | Microsoft Learn <https://learn.microsoft.com/en-us/sql/t-sql/data-types/ntext-text-and-image-transact-sql?view=sql-server-ver16>`_。

.. _forge-addfield-default-value-rawsql:

作为默认值的原始 SQL 字符串
---------------------------------

.. versionadded:: 4.2.0

从 v4.2.0 开始, ``$forge->addField()`` 接受一个 ``CodeIgniter\Database\RawSql`` 实例,它表示原始 SQL 字符串。

.. literalinclude:: forge/027.php

.. warning:: 当你使用 ``RawSql`` 时,必须手动对数据进行转义。否则可能会导致 SQL 注入。

作为字段传递字符串
-------------------------

如果确切知道如何创建字段,可以将字符串传递到 ``addField()`` 中的字段定义中:

.. literalinclude:: forge/008.php

.. note:: 不能在传递原始字符串作为字段后对这些字段调用 ``addKey()``。

.. note:: 对 ``addField()`` 的多次调用是累积的。

创建 id 字段
--------------------

创建 id 字段有一个特殊的例外。类型为 id 的字段将自动被赋值为 INT(9) 自增主键。

.. literalinclude:: forge/009.php

.. _adding-keys:

添加键
===========

$forge->addKey()
----------------

通常,你会希望表具有键。这是通过 ``$forge->addKey('field')`` 完成的。可选的第二个参数设置为 true 将使其成为主键,第三个参数设置为 true 将使其成为唯一键。你可以使用第四个参数指定名称。请注意, ``addKey()`` 必须在表已存在的情况下后跟对 ``createTable()`` 或 ``processIndexes()`` 的调用。

多个非主键列必须作为数组发送。以下为 MySQL 的示例输出。

.. literalinclude:: forge/010.php

$forge->addPrimaryKey()
-----------------------

$forge->addUniqueKey()
----------------------

为了使代码更易读,也可以使用特定方法添加主键和唯一键:

.. literalinclude:: forge/011.php

.. note:: 当你添加主键时,即使提供了名称,MySQL 和 SQLite 也会假定名称为 ``PRIMARY``。

.. _adding-foreign-keys:

添加外键
===================

外键有助于在表之间强制关系和操作。对于支持外键的表,可以直接在 forge 中添加它们:

.. literalinclude:: forge/012.php

你还可以指定约束的“更新时”和“删除时”属性的所需操作以及名称:

.. literalinclude:: forge/013.php

.. note:: SQLite3 不支持命名外键。CodeIgniter 将引用它们的 ``prefix_table_column_foreign``。

.. _creating-a-table:

创建表格
================

在声明字段和键之后,可以使用以下方法创建新表格

.. literalinclude:: forge/014.php

可选的第二个参数设置为 true 将只在表不存在时创建该表。

.. literalinclude:: forge/015.php

你也可以传递可选的表属性,例如 MySQL 的 ``ENGINE``:

.. literalinclude:: forge/016.php

.. note:: 除非指定了 ``CHARACTER SET`` 和/或 ``COLLATE`` 属性,否则 ``createTable()`` 将始终使用配置的 *charset* 和 *DBCollat* 值添加它们,只要它们不为空(仅限 MySQL)。

***************
删除表
***************

删除一张表
================

执行 ``DROP TABLE`` 语句,并可选地添加 ``IF EXISTS`` 子句。

.. literalinclude:: forge/017.php

可以传递第三个参数以添加 ``CASCADE`` 选项,某些驱动程序可能需要它来处理具有外键的表的删除。

.. literalinclude:: forge/018.php

****************
修改表
****************

向表中添加字段
=========================

$forge->addColumn()
-------------------

``addColumn()`` 方法用于修改现有表。它接受与 :ref:`创建表 <adding-fields>` 相同的字段数组,可用于添加其他字段。

.. note:: 与创建表不同,如果未指定 ``null``,列将为 ``NULL``,而不是 ``NOT NULL``。

.. literalinclude:: forge/022.php

如果使用 MySQL 或 CUBIRD,则可以利用它们的 ``AFTER`` 和 ``FIRST`` 子句来定位新列。

例子:

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

此方法的使用与 ``addColumn()`` 相同,只是它更改现有列而不是添加新列。为了更改名称,可以将“name”键添加到定义字段的数组中。

.. literalinclude:: forge/026.php

.. note:: ``modifyColumn()`` 可能会意外地更改 ``NULL``/``NOT NULL``。因此,建议始终为 ``null`` 键指定值。与创建表不同,如果未指定 ``null``,列将为 ``NULL``,而不是 ``NOT NULL``。

.. note:: 由于一个错误,在 v4.3.4 之前,即使指定 ``'null' => false``,SQLite3 也可能不设置 ``NOT NULL``。

.. note:: 由于一个错误,在 v4.3.4 之前,Postgres 和 SQLSRV 即使指定 ``'null' => true`` 也会设置 ``NOT NULL``。

.. _db-forge-adding-keys-to-a-table:

向表添加键
======================

.. versionadded:: 4.3.0

你可以通过使用 ``addKey()``、``addPrimaryKey()``、``addUniqueKey()`` 或 ``addForeignKey()`` 和 ``processIndexes()`` 向现有表添加键:

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

执行 TABLE RENAME

.. literalinclude:: forge/021.php

***************
类参考
***************

.. php:namespace:: CodeIgniter\Database

.. php:class:: Forge

    .. php:method:: addColumn($table[, $field = []])

        :param    string    $table: 要向其中添加列的表名
        :param    array    $field: 列定义
        :returns:    成功则为 true,失败则为 false
        :rtype:    bool

        向现有表添加列。用法:参见 `向表中添加字段`_.

    .. php:method:: addField($field)

        :param    array    $field: 要添加的字段定义
        :returns:    ``\CodeIgniter\Database\Forge`` 实例(方法链)
        :rtype:    ``\CodeIgniter\Database\Forge``

        将用于创建表的字段添加到集合中。用法:参见 `添加字段`_。

    .. php:method:: addForeignKey($fieldName, $tableName, $tableField[, $onUpdate = '', $onDelete = '', $fkName = ''])

        :param    string|string[]    $fieldName: 键字段的名称或字段数组
        :param    string    $tableName: 父表的名称
        :param    string|string[]    $tableField: 父表字段的名称或字段数组
        :param    string    $onUpdate: “更新时”的所需操作
        :param    string    $onDelete: “删除时”的所需操作
        :param    string    $fkName: 外键的名称。这与 SQLite3 不兼容
        :returns:    ``\CodeIgniter\Database\Forge`` 实例(方法链)
        :rtype:    ``\CodeIgniter\Database\Forge``

        将用于创建表的外键添加到集合中。用法:参见 `添加外键`_。

        .. note:: 从 v4.3.0 开始可以使用 ``$fkName``。

    .. php:method:: addKey($key[, $primary = false[, $unique = false[, $keyName = '']]])

        :param    mixed    $key: 键字段的名称或字段数组
        :param    bool    $primary: 设置为 true 将其设置为主键,否则设置为常规键
        :param    bool    $unique: 设置为 true 将其设置为唯一键,否则设置为常规键
        :param    string    $keyName: 要添加的键的名称
        :returns:    ``\CodeIgniter\Database\Forge`` 实例(方法链)
        :rtype:    ``\CodeIgniter\Database\Forge``

        将用于创建表的键添加到集合中。用法:参见 `添加键`_。

        .. note:: 从 v4.3.0 开始可以使用 ``$keyName``。

    .. php:method:: addPrimaryKey($key[, $keyName = ''])

        :param    mixed    $key: 键字段的名称或字段数组
        :param    string    $keyName: 要添加的键的名称
        :returns:    ``\CodeIgniter\Database\Forge`` 实例(方法链)
        :rtype:    ``\CodeIgniter\Database\Forge``

        将用于创建表的主键添加到集合中。用法:参见 `添加键`_。

        .. note:: 从 v4.3.0 开始可以使用 ``$keyName``。

    .. php:method:: addUniqueKey($key[, $keyName = ''])

        :param    mixed    $key: 键字段的名称或字段数组
        :param    string    $keyName: 要添加的键的名称
        :returns:    ``\CodeIgniter\Database\Forge`` 实例(方法链)
        :rtype:    ``\CodeIgniter\Database\Forge``

        将用于创建表的唯一键添加到集合中。用法:参见 `添加键`_。

        .. note:: 从 v4.3.0 开始可以使用 ``$keyName``。

    .. php:method:: createDatabase($dbName[, $ifNotExists = false])

        :param    string    $db_name: 要创建的数据库名称
        :param    string    $ifNotExists: 设置为 true 将添加 ``IF NOT EXISTS`` 子句或检查数据库是否存在
        :returns:    成功则为 true,失败则为 false
        :rtype:    bool

        创建新数据库。用法:参见 `创建和删除数据库`_。

    .. php:method:: createTable($table[, $if_not_exists = false[, array $attributes = []]])

        :param    string    $table: 要创建的表的名称
        :param    string    $if_not_exists: 设置为 true 将添加 ``IF NOT EXISTS`` 子句
        :param    string    $attributes: 表属性的关联数组
        :returns:   成功则为查询对象,失败则为 false
        :rtype:    mixed

        创建新表。用法:参见 `创建表格`_。

    .. php:method:: dropColumn($table, $column_name)

        :param    string    $table: 表名
        :param    mixed    $column_names: 逗号分隔的字符串或列名称数组
        :returns:    成功则为 true,失败则为 false
        :rtype:    bool

        从表中删除单个或多个列。用法:参见 `从表中删除字段`_。

    .. php:method:: dropDatabase($dbName)

        :param    string    $dbName: 要删除的数据库名称
        :returns:    成功则为 true,失败则为 false
        :rtype:    bool

        删除数据库。用法:参见 `创建和删除数据库`_。

    .. php:method:: dropKey($table, $keyName[, $prefixKeyName = true])

        :param    string    $table: 具有键的表的名称
        :param    string    $keyName: 要删除的键的名称
        :param    string    $prefixKeyName: 是否要添加数据库前缀到 ``$keyName``
        :returns:    成功则为 true,失败则为 false
        :rtype:    bool

        删除索引或唯一索引。

        .. note:: 从 v4.3.0 开始可以使用 ``$keyName`` 和 ``$prefixKeyName``。

    .. php:method:: dropPrimaryKey($table[, $keyName = ''])

        :param    string    $table: 要删除主键的表的名称
        :param    string    $keyName: 要删除的主键的名称
        :returns:    成功则为 true,失败则为 false
        :rtype:    bool

        从表中删除主键。

        .. note:: 从 v4.3.0 开始可以使用 ``$keyName``。

    .. php:method:: dropTable($table_name[, $if_exists = false])

        :param    string    $table: 要删除的表的名称
        :param    string    $if_exists: 设置为 true 将添加 ``IF EXISTS`` 子句
        :returns:    成功则为 true,失败则为 false
        :rtype:    bool

        删除表。用法:参见 `删除一张表`_。

    .. php:method:: processIndexes($table)

        .. versionadded:: 4.3.0

        :param    string    $table: 要向其中添加索引的表的名称
        :returns:    成功则为 true,失败则为 false
        :rtype:    bool

        跟在 ``addKey()``、``addPrimaryKey()``、``addUniqueKey()`` 和 ``addForeignKey()`` 之后,
        向已有表添加索引。参见 `向表添加键`_。

    .. php:method:: modifyColumn($table, $field)

        :param    string    $table: 表名
        :param    array    $field: 列定义
        :returns:    成功则为 true,失败则为 false
        :rtype:    bool

        修改表列。用法:参见 `修改表中的字段`_。

    .. php:method:: renameTable($table_name, $new_table_name)

        :param    string    $table: 表的当前名称
        :param    string    $new_table_name: 表的新名称
        :returns:   成功则为查询对象,失败则为 false
        :rtype:    mixed

        重命名表。用法:参见 `重命名表`_。
