#####################
测试数据库
#####################

.. contents::
    :local:
    :depth: 2

测试类
**************

为了利用 CodeIgniter 为测试提供的内置数据库工具，您的测试必须扩展 ``CIUnitTestCase`` 并使用 ``DatabaseTestTrait``:

.. literalinclude:: database/001.php

由于在 ``setUp()`` 和 ``tearDown()`` 阶段执行了特殊功能，所以如果您需要使用这些方法，必须确保调用父类的方法，否则您将失去这里描述的大部分功能：

.. literalinclude:: database/002.php

设置测试数据库
**************************

运行数据库测试时,您需要提供可在测试期间使用的数据库。框架提供了特定于 CodeIgniter 的工具,而不是使用 PHPUnit 内置的数据库功能。第一步是确保您在 **app/Config/Database.php** 中设置了 ``tests`` 数据库组。这指定了仅在运行测试时使用的数据库连接,以保持其他数据的安全。

如果团队中有多个开发人员,您可能希望将凭证保存在 **.env** 文件中。要这样做,请编辑文件以确保存在以下行并具有正确的信息::

    database.tests.hostname = localhost
    database.tests.database = ci4_test
    database.tests.username = root
    database.tests.password = root
    database.tests.DBDriver = MySQLi
    database.tests.DBPrefix =
    database.tests.port = 3306

迁移和种子
====================

运行测试时,您需要确保数据库具有正确的 schema 设置并且对每个测试处于已知状态。您可以使用迁移和种子来设置数据库,方法是在测试中添加一些类属性。

.. literalinclude:: database/003.php

迁移
----------

$migrate
^^^^^^^^

此布尔值确定是否在测试之前运行数据库迁移。默认情况下,始终将数据库迁移到 ``$namespace`` 定义的最新可用状态。如果为 ``false``,则不运行迁移。如果要禁用迁移,请设置为 ``false``。

$migrateOnce
^^^^^^^^^^^^

此布尔值确定是否只运行一次数据库迁移。如果要在首次测试之前运行一次迁移,请设置为 ``true``。如果不存在或为 ``false``,则在每次测试之前运行迁移。

$refresh
^^^^^^^^

此布尔值确定是否在测试之前完全刷新数据库。如果为 ``true``,则所有迁移都会回滚到版本 0。

$namespace
^^^^^^^^^^

默认情况下,CodeIgniter 将在 **tests/_support/Database/Migrations** 中查找在测试期间应运行的迁移。您可以在 ``$namespace`` 属性中指定新命名空间来更改此位置。这不应包括 **Database\\Migrations** 子命名空间,而只是基本命名空间。

.. important:: 如果将此属性设置为 ``null``,则像 ``php spark migrate --all`` 一样从所有可用的命名空间运行迁移。

种子
-----

$seed
^^^^^

如果存在且非空,则指定在测试运行之前用来向数据库填充测试数据的种子文件的名称。

$seedOnce
^^^^^^^^^

此布尔值确定是否只运行一次数据库种子。如果要在首次测试之前运行一次数据库种子,请设置为 ``true``。如果不存在或为 ``false``,则在每次测试之前运行数据库种子。

$basePath
^^^^^^^^^

默认情况下,CodeIgniter 将在 **tests/_support/Database/Seeds** 中查找在测试期间应运行的种子。您可以通过指定 ``$basePath`` 属性来更改此目录。这不应包括 **Seeds** 目录,而是保存子目录的单个目录的路径。

帮助方法
**************

**DatabaseTestTrait** 类提供了几个帮助方法来帮助测试数据库。

更改数据库状态
=======================

regressDatabase()
-----------------

在上述 ``$refresh`` 期间调用,如果需要手动重置数据库,此方法可用。

migrateDatabase()
-----------------

在 ``setUp()`` 期间调用,如果需要手动运行迁移,此方法可用。

seed($name)
-----------

允许您手动将 Seed 加载到数据库中。唯一的参数是要运行的种子的名称。种子必须存在于 ``$basePath`` 中指定的路径内。

hasInDatabase($table, $data)
----------------------------

将新行插入数据库中。此行在当前测试运行后被删除。``$data`` 是一个包含要插入表中的数据的关联数组。

.. literalinclude:: database/007.php

从数据库获取数据
==========================

grabFromDatabase($table, $column, $criteria)
--------------------------------------------

返回在行与 ``$criteria`` 匹配的指定表中的 ``$column`` 的值。如果找到多行,它只会返回第一行。

.. literalinclude:: database/006.php

断言
==========

dontSeeInDatabase($table, $criteria)
------------------------------------

断言与 ``$criteria`` 中的键/值对匹配的行在数据库中不存在。

.. literalinclude:: database/004.php

seeInDatabase($table, $criteria)
--------------------------------

断言与 ``$criteria`` 中的键/值对匹配的行在数据库中存在。

.. literalinclude:: database/005.php

seeNumRecords($expected, $table, $criteria)
-------------------------------------------

断言在数据库中找到的与 ``$criteria`` 匹配的行数。

.. literalinclude:: database/008.php
