###################
数据库迁移
###################

迁移是以结构化和组织良好的方式修改数据库的便捷途径。虽然可以手动编辑 SQL 片段，但这样就必须告知其他开发者运行这些片段，且在下次部署时，还需跟踪哪些更改需要应用到生产服务器。

**migrations** 数据库表用于记录已运行的迁移，因此只需确保迁移文件到位，并运行 ``spark migrate`` 命令即可将数据库更新至最新状态。还可使用 ``spark migrate --all`` 来包含所有命名空间下的迁移。

.. contents::
    :local:
    :depth: 2

********************
迁移文件名
********************

迁移文件名由时间戳前缀、下划线（``_``）和描述性名称（类名）组成。

* 2024-09-08-013653_AddBlogTable.php

每个迁移都以创建时的时间戳（**2024-09-08-013653**）编号，格式为 **YYYY-MM-DD-HHIISS**。

描述性名称（**AddBlogTable**）是 PHP 类名，因此必须命名为有效的类名。

前缀中的年、月、日和时间可以用连字符（``-``）、下划线（``_``）分隔，也可以不分隔。例如：

* 2012-10-31-100538_AlterBlogTrackViews.php
* 2012_10_31_100539_AlterBlogAddTranslations.php
* 20121031100537_AddBlog.php

迁移按数字顺序正向或反向运行，具体取决于所选的操作。这有助于防止团队协作时的编号冲突。

******************
创建迁移
******************

这是一个包含博客功能的新站点的首次迁移。所有迁移文件都存放于 **app/Database/Migrations/** 目录，文件名类似于 **2022-01-31-013057_AddBlog.php**。

.. literalinclude:: migration/001.php

可分别通过 ``$this->db`` 和 ``$this->forge`` 使用数据库连接和数据库 Forge 类。

此外，也可通过命令行调用来生成迁移文件骨架。详见 :ref:`command-line-tools` 中的 `make:migration`_。

.. note:: 由于迁移类是 PHP 类，因此每个迁移文件中的类名必须唯一。

外键
============

当表包含外键时，删除表或列的操作常会导致迁移失败。若要在运行迁移时临时绕过外键检查，请使用数据库连接中的 ``disableForeignKeyChecks()`` 和 ``enableForeignKeyChecks()`` 方法。

.. literalinclude:: migration/002.php

数据库组
===============

迁移仅针对单个数据库组运行。如果在 **app/Config/Database.php** 中定义了多个组，默认将针对该配置文件中指定的 ``$defaultGroup`` 运行。

有时可能需要为不同的数据库组使用不同的架构。例如，一个数据库用于存储常规站点信息，另一个用于存储核心业务数据。

通过在迁移类中设置 ``$DBGroup`` 属性，可确保迁移仅针对特定组运行。此名称必须与数据库组名称完全匹配：

.. literalinclude:: migration/003.php

.. note:: 记录已运行迁移的 **migrations** 表将始终在默认数据库组中创建。

命名空间
==========

迁移类库可利用 ``$psr4`` 属性匹配目录名，自动扫描在 **app/Config/Autoload.php** 中定义或从外部源（如 Composer）加载的所有命名空间。它将包含在 **Database/Migrations** 中找到的所有迁移。

每个命名空间都有独立的版本序列，这有助于在不影响其他命名空间的情况下对各个模块（命名空间）进行升级或回滚。

例如，假设在 Autoload 配置文件中定义了以下命名空间：

.. literalinclude:: migration/004.php
    :lines: 2-

系统将在 **APPPATH/Database/Migrations** 和 **ROOTPATH/MyCompany/Database/Migrations** 中查找迁移。这使得在可复用的模块化代码套件中包含迁移变得非常简单。

.. _command-line-tools:

*******************
命令行工具
*******************

CodeIgniter 自带了多个可从命令行使用的 :doc:`命令 </cli/spark_commands>`，以协助处理迁移任务。这些工具为开发者提供了便利，其核心是调用了 MigrationRunner 类中的相关方法。

migrate
=======

使用所有可用的迁移来迁移数据库组：

.. code-block:: console

    php spark migrate

可为 ``migrate`` 使用以下选项：

- ``-g`` - 指定数据库组。若指定，则仅运行该组的迁移；若未指定，则运行所有迁移。
- ``-n`` - 选择命名空间，否则默认使用 ``App``。
- ``--all`` - 将所有命名空间迁移至最新。

本例将在 test 数据库组中运行 ``Acme\Blog`` 命名空间下的所有新迁移：

Unix 环境：

.. code-block:: console

    php spark migrate -g test -n Acme\\Blog

Windows 环境：

.. code-block:: console

    php spark migrate -g test -n Acme\Blog

使用 ``--all`` 选项时，系统将扫描所有命名空间以查找未运行的迁移。这些迁移会被汇总，并按创建日期排序。这有助于最大限度地减少主应用与各模块之间可能存在的冲突。

migrate:rollback
================

将所有迁移回滚到初始状态（即迁移 0）：

.. code-block:: console

  php spark migrate:rollback

可为 ``migrate:rollback`` 使用以下选项：

- ``-b`` - 选择批次：使用正整数指定批次。
- ``-f`` - 强制跳过确认提示，此提示仅在生产环境中出现。

migrate:refresh
===============

通过先回滚所有迁移，再重新运行所有迁移来重置数据库状态：

.. code-block:: console

  php spark migrate:refresh

可为 ``migrate:refresh`` 使用以下选项：

- ``-g`` - 指定数据库组。若指定，则仅运行该组的迁移；若未指定，则运行所有迁移。
- ``-n`` - 选择命名空间，否则默认使用 ``App``。
- ``--all`` - 刷新所有命名空间。
- ``-f`` - 强制跳过确认提示，此提示仅在生产环境中出现。

migrate:status
==============

列出所有迁移及其运行时间；若尚未运行则显示 '--'：

.. code-block:: console

  php spark migrate:status

  ...

  +----------------------+-------------------+-----------------------+---------+---------------------+-------+
  | Namespace            | Version           | Filename              | Group   | Migrated On         | Batch |
  +----------------------+-------------------+-----------------------+---------+---------------------+-------+
  | App                  | 2022-04-06-234508 | CreateCiSessionsTable | default | 2022-04-06 18:45:14 | 2     |
  | CodeIgniter\Settings | 2021-07-04-041948 | CreateSettingsTable   | default | 2022-04-06 01:23:08 | 1     |
  | CodeIgniter\Settings | 2021-11-14-143905 | AddContextColumn      | default | 2022-04-06 01:23:08 | 1     |
  +----------------------+-------------------+-----------------------+---------+---------------------+-------+

可为 ``migrate:status`` 使用以下选项：

- ``-g`` - 指定数据库组。若指定，则仅检查该组的迁移；若未指定，则检查所有迁移。

make:migration
==============

在 **app/Database/Migrations** 中创建一个迁移文件骨架。该命令会自动添加当前时间戳。生成的类名是文件名的大驼峰（PascalCase）版本。

.. code-block:: console

  php spark make:migration <class> [options]

可为 ``make:migration`` 使用以下选项：

- ``--namespace`` - 设置根命名空间。默认值：``APP_NAMESPACE``。
- ``--suffix``    - 在类名后追加组件标题。

以下选项用于生成数据库 Session 的迁移文件：

- ``--session``   - 生成数据库 Session 的迁移文件。
- ``--table``     - 用于数据库 Session 的表名。默认值：``ci_sessions``。
- ``--dbgroup``   - 用于数据库 Session 的数据库组。默认值：``default``。

*********************
迁移配置
*********************

下表列出了 **app/Config/Migrations.php** 中所有的迁移配置选项。

==================== ============ ============= =============================================================
配置项               默认值       选项          描述
==================== ============ ============= =============================================================
**enabled**          true         true / false  启用或禁用迁移。
**table**            migrations   无            存储架构版本号的表名。
                                                此表始终在默认数据库组（``$defaultGroup``）中创建。
**timestampFormat**  Y-m-d-His\_                创建迁移时使用的时间戳格式。
**lock**             false        true / false  启用分布式锁，以防止多进程环境（如 Kubernetes）中的并发迁移。
==================== ============ ============= =============================================================

***************
类参考
***************

.. php:namespace:: CodeIgniter\Database

.. php:class:: MigrationRunner

    .. php:method:: findMigrations()

        :returns:    迁移文件数组
        :rtype:    array

        返回在 ``path`` 属性中找到的迁移文件名数组。

    .. php:method:: latest($group)

        :param    mixed    $group: 数据库组名称，若为 null 则使用默认组。
        :returns:    成功返回 ``true``，失败返回 ``false``
        :rtype:    bool

        定位命名空间（或所有命名空间）的迁移，确定尚未运行的迁移，并按版本顺序运行（各命名空间交替进行）。

    .. php:method:: regress($targetBatch, $group)

        :param    int    $targetBatch: 要回滚到的目标批次；正整数指定批次，0 表示回滚所有，负数表示相对批次（例如 -3 表示“回滚三个批次”）。
        :param    ?string    $group: 数据库组名称，若为 null 则使用默认组。
        :returns:    成功返回 ``true``，失败或未发现迁移返回 ``false``
        :rtype:    bool

        按批次将更改回滚到之前的状态。

        .. literalinclude:: migration/006.php

    .. php:method:: force($path, $namespace, $group)

        :param    mixed    $path: 有效迁移文件的路径。
        :param    mixed    $namespace: 所提供迁移的命名空间。
        :param    mixed    $group: 数据库组名称，若为 null 则使用默认组。
        :returns:    成功返回 ``true``，失败返回 ``false``
        :rtype:    bool

        强制运行单个迁移文件，不论顺序或批次。系统会根据是否已迁移来自动检测是执行 ``up()`` 还是 ``down()``。

        .. note:: 建议仅在测试时使用此方法，否则可能导致数据一致性问题。

    .. php:method:: setNamespace($namespace)

        :param  string|null  $namespace: 应用命名空间。``null`` 表示所有命名空间。
        :returns:    当前 MigrationRunner 实例
        :rtype:     CodeIgniter\\Database\\MigrationRunner

        设置类库查找迁移文件的命名空间：

        .. literalinclude:: migration/007.php

        .. note:: 如果设置为 ``null``，则会在所有命名空间中查找迁移文件。

    .. php:method:: setGroup($group)

        :param  string  $group: 数据库组名称。
        :returns:    当前 MigrationRunner 实例
        :rtype:     CodeIgniter\\Database\\MigrationRunner

        设置类库查找迁移文件的数据库组：

        .. literalinclude:: migration/008.php
