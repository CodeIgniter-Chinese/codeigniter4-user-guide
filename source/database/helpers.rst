####################
查询辅助方法
####################

.. contents::
    :local:
    :depth: 2

执行查询后的信息
**********************************

$db->insertID()
===============

执行数据库插入操作时，返回插入记录的 ID 号。

.. note:: 如果使用 PDO 驱动连接 PostgreSQL，或使用 Interbase 驱动，此函数需要一个 $name 参数，用于指定检查插入 ID 的相应序列。

$db->affectedRows()
===================

执行“写”类型查询（如 insert、update 等）时，显示受影响的行数。

.. note:: 在 MySQL 中，执行 "DELETE FROM TABLE" 会返回 0 个受影响的行。数据库类有一个小的 hack 可以让它返回正确的受影响行数。默认情况下此 hack 是启用的，但可以在数据库驱动文件中将其关闭。

$db->getLastQuery()
===================

返回一个代表最后执行的查询的 Query 对象（即查询语句本身，而非查询结果）。

关于数据库的信息
*******************************

$db->countAll()
===============

用于确定特定表中的行数。将表名作为第一个参数传入。这是查询构建器的一部分。

.. literalinclude:: helpers/001.php

$db->countAllResults()
======================

用于确定特定结果集中的行数。将表名作为第一个参数传入。这是查询构建器的一部分。

.. literalinclude:: helpers/002.php

$db->getPlatform()
==================

输出你正在运行的数据库平台（DBDriver），如 MySQLi、SQLSRV、Postgre 等：

.. literalinclude:: helpers/003.php

$db->getVersion()
=================

输出你正在运行的数据库版本：

.. literalinclude:: helpers/004.php
