####################
查询辅助方法
####################

.. contents::
    :local:
    :depth: 2

执行查询的信息
**********************************

$db->insertID()
===============

执行数据库插入时的插入 ID 号。

.. note:: 如果使用 PDO 驱动程序与 PostgreSQL 一起使用,或者使用 Interbase
    驱动程序,此函数需要一个 $name 参数,该参数指定要检查插入 ID 的适当序列。

$db->affectedRows()
===================

显示受影响的行数,当执行“写入”类型的查询时(插入、更新等)。

.. note:: 在 MySQL 中,"DELETE FROM TABLE" 返回 0 受影响的行。数据库
    类对此进行了一个小 Hack,允许它返回正确的受影响行数。默认情况下,此 Hack 已启用,但可以在数据库驱动程序文件中将其关闭。

$db->getLastQuery()
===================

返回代表最后执行的查询的 Query 对象(查询字符串,而不是结果)。

有关数据库的信息
*******************************

$db->countAll()
===============

允许你确定特定表中的行数。在第一个参数中提交表名。这是查询构建器的一部分。

.. literalinclude:: helpers/001.php

$db->countAllResults()
======================

允许你确定特定结果集中的行数。在第一个参数中提交表名。这是查询构建器的一部分。

.. literalinclude:: helpers/002.php

$db->getPlatform()
==================

输出你正在运行的数据库平台(DBDriver)(MySQLi、SQLSRV、Postgre等):

.. literalinclude:: helpers/003.php

$db->getVersion()
=================

输出你正在运行的数据库版本:

.. literalinclude:: helpers/004.php
