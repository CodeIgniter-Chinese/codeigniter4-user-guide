#####################
测试数据库
#####################

.. contents::
    :local:
    :depth: 2

测试类
**************

若要利用 CodeIgniter 提供的内置数据库测试工具，测试类须继承 ``CIUnitTestCase`` 并引入 ``DatabaseTestTrait``：

.. literalinclude:: database/001.php

由于 ``setUp()`` 和 ``tearDown()`` 阶段会执行特殊功能，如需使用这些方法，务必调用父类方法，否则会丢失此处描述的大部分功能：

.. literalinclude:: database/002.php

设置测试数据库
**************************

运行数据库测试时，需准备测试专用数据库。本框架并未采用 PHPUnit 内置的数据库功能，而是提供了一套 CodeIgniter 专属工具。首先，应确保在 **app/Config/Database.php** 中已配置 ``tests`` 数据库组。该配置用于指定仅在运行测试时使用的数据库连接，从而保障其他数据的安全。

团队多人协作时，建议将凭据存放在 **.env** 文件中。请编辑该文件，确保包含以下配置且信息准确::

    database.tests.hostname = localhost
    database.tests.database = ci4_test
    database.tests.username = root
    database.tests.password = root
    database.tests.DBDriver = MySQLi
    database.tests.DBPrefix =
    database.tests.port = 3306

迁移与数据填充
====================

运行测试时，需确保数据库 Schema 正确，且每个测试用例均处于已知状态。只需在测试类中定义几个属性，即可利用迁移和数据填充来初始化数据库。

.. literalinclude:: database/003.php

迁移
----------

$migrate
^^^^^^^^

此布尔值用于控制是否在测试前运行数据库迁移。默认情况下，系统会根据 ``$namespace`` 的定义，将数据库迁移至最新状态。若设为 ``false``，则不运行迁移；如需禁用迁移，将其设为 ``false`` 即可。

$migrateOnce
^^^^^^^^^^^^

此布尔值用于控制数据库迁移是否仅运行一次。如需在执行首个测试前仅运行一次迁移，请设为 ``true``；若未配置或设为 ``false``，则每次测试前均会运行迁移。

$refresh
^^^^^^^^

此布尔值用于控制是否在测试前彻底重置数据库。若设为 ``true``，所有迁移都将回滚至版本 0。

$namespace
^^^^^^^^^^

默认情况下，CodeIgniter 会从 **tests/_support/Database/Migrations** 路径下查找并运行测试所需的迁移文件。通过在 ``$namespace`` 属性中指定新命名空间，可更改查找位置。注意此处只需提供基础命名空间，无需包含 **Database\\Migrations** 子命名空间。

.. important:: 若将此属性设为 ``null``，则会运行所有可用命名空间下的迁移，效果等同于执行 ``php spark migrate --all``。

数据填充
--------

$seed
^^^^^

若设置了此属性且不为空，则指定在测试运行前用于填充数据库的 Seed 文件名称。

$seedOnce
^^^^^^^^^

此布尔值用于控制数据库填充是否仅运行一次。若需在首个测试前仅执行一次填充，请设为 ``true``；若未定义或设为 ``false``，则每次测试前都会执行填充。

$basePath
^^^^^^^^^

默认情况下，CodeIgniter 会从 **tests/_support/Database/Seeds** 路径下查找测试所需的填充文件。可通过 ``$basePath`` 属性更改该目录。注意路径中不应包含 **Seeds** 目录，而是指向包含该子目录的父级目录。

辅助方法
**************

**DatabaseTestTrait** 类提供了多个辅助方法，以便进行数据库测试。

修改数据库状态
=======================

regressDatabase()
-----------------

在上述 ``$refresh`` 期间调用。如需手动重置数据库，可使用此方法。

migrateDatabase()
-----------------

在 ``setUp()`` 期间调用。如需手动运行迁移，可使用此方法。

seed($name)
-----------

用于手动向数据库加载 Seed。唯一参数是待运行的 Seed 名称。该 Seed 必须位于 ``$basePath`` 指定的路径内。

hasInDatabase($table, $data)
----------------------------

向数据库插入新记录。该记录会在当前测试结束后自动移除。``$data`` 为包含待插入数据的关联数组。

.. literalinclude:: database/007.php

从数据库获取数据
==========================

grabFromDatabase($table, $column, $criteria)
--------------------------------------------

返回指定表中符合 ``$criteria`` 条件的 ``$column`` 字段的值。若匹配到多条记录，则仅返回第一条记录。

.. literalinclude:: database/006.php

断言
==========

dontSeeInDatabase($table, $criteria)
------------------------------------

断言数据库中不存在符合 ``$criteria`` 键值对条件的记录。

.. literalinclude:: database/004.php

seeInDatabase($table, $criteria)
--------------------------------

断言数据库中存在符合 ``$criteria`` 键值对条件的记录。

.. literalinclude:: database/005.php

seeNumRecords($expected, $table, $criteria)
-------------------------------------------

断言数据库中符合 ``$criteria`` 条件的记录总数与预期值 ``$expected`` 相符。

.. literalinclude:: database/008.php
