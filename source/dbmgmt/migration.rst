###################
数据库迁移
###################

迁移是一种以结构化和有序的方式修改数据库的便捷方法。你可以手动编辑 SQL 片段，但随后你将负责通知其他开发者需要运行这些脚本。你还需要跟踪下一次部署时需要在生产机器上运行的更改。

数据库表 **migrations** 用于跟踪已运行的迁移，因此你只需确保迁移文件已准备好，然后运行 ``spark migrate`` 命令即可将数据库更新到最新状态。你也可以使用 ``spark migrate --all`` 来包含所有命名空间的迁移。

.. contents::
    :local:
    :depth: 2

********************
迁移文件名
********************

迁移文件名由时间戳前缀、下划线（``_``）和描述性名称（类名）组成。

* 2024-09-08-013653_AddBlogTable.php

每个迁移都使用创建迁移时的时间戳（**2024-09-08-013653**）进行编号，格式为 **YYYY-MM-DD-HHIISS**。

迁移的描述性名称（**AddBlogTable**）是 PHP 中的一个类名。因此你必须使用有效的类名。

前缀中的年、月、日和时间可以用连字符（``-``）、下划线（``_``）分隔，也可以不分隔。例如：

* 2012-10-31-100538_AlterBlogTrackViews.php
* 2012_10_31_100539_AlterBlogAddTranslations.php
* 20121031100537_AddBlog.php

每个迁移都按数字顺序向前或向后运行，具体取决于所采取的方法。这有助于在团队环境中防止编号冲突。

******************
创建迁移
******************

这将是一个包含博客功能的新站点的首次迁移。所有迁移都位于 **app/Database/Migrations/** 目录中，文件名如 **2022-01-31-013057_AddBlog.php**。

.. literalinclude:: migration/001.php

数据库连接和数据库 Forge 类分别通过 ``$this->db`` 和 ``$this->forge`` 提供给你。

或者，你可以使用命令行调用来生成一个骨架迁移文件。有关更多详细信息，请参阅 :ref:`command-line-tools` 中的 `make:migration`_。

.. note:: 由于迁移类是一个 PHP 类，因此类名在每个迁移文件中必须是唯一的。

外键
============

当你的表包含外键时，迁移在尝试删除表和列时经常会引发问题。要在运行迁移时临时绕过外键检查，请在数据库连接上使用 ``disableForeignKeyChecks()`` 和 ``enableForeignKeyChecks()`` 方法。

.. literalinclude:: migration/002.php

数据库组
===============

迁移仅针对单个数据库组运行。如果你在 **app/Config/Database.php** 中定义了多个组，那么默认情况下它将针对该配置文件中指定的 ``$defaultGroup`` 运行。

有时你可能需要为不同的数据库组使用不同的模式。例如，你可能有一个数据库用于存储所有常规站点信息，而另一个数据库用于存储关键任务数据。

你可以通过在迁移中设置 ``$DBGroup`` 属性来确保迁移仅在正确的组上运行。此名称必须与数据库组的名称完全匹配：

.. literalinclude:: migration/003.php

.. note:: 用于跟踪已运行迁移的 **migrations** 表将始终在默认数据库组中创建。

命名空间
==========

迁移库可以使用 ``$psr4`` 属性匹配目录名称，自动扫描你在 **app/Config/Autoload.php** 中定义或从 Composer 等外部源加载的所有命名空间。它将包含在 **Database/Migrations** 中找到的所有迁移。

每个命名空间都有自己的版本序列，这将帮助你在不影响其他命名空间的情况下升级和降级每个模块（命名空间）。

例如，假设我们的 Autoload 配置文件中定义了以下命名空间：

.. literalinclude:: migration/004.php
    :lines: 2-

这将查找位于 **APPPATH/Database/Migrations** 和 **ROOTPATH/MyCompany/Database/Migrations** 的所有迁移。这使得在可重用的模块化代码套件中包含迁移变得简单。

.. _command-line-tools:

*******************
命令行工具
*******************

CodeIgniter 提供了多个 :doc:`命令 </cli/spark_commands>`，这些命令可以从命令行使用，以帮助你处理迁移。这些工具为你提供了更便捷的操作方式。这些工具主要提供了对 MigrationRunner 类中可用方法的访问。

migrate
=======

使用所有可用的迁移来迁移一个数据库组：

.. code-block:: console

    php spark migrate

你可以将 ``migrate`` 与以下选项一起使用：

- ``-g`` - 指定数据库组。如果指定了该选项，则仅运行指定数据库组的迁移。如果未指定，则运行所有迁移。
- ``-n`` - 选择命名空间，否则将使用 ``App`` 命名空间。
- ``--all`` - 将所有命名空间迁移到最新的迁移。

此示例将在测试数据库组上，将 ``Acme\Blog`` 命名空间与任何新迁移进行迁移：

对于 Unix 系统：

.. code-block:: console

    php spark migrate -g test -n Acme\\Blog

对于 Windows 系统：

.. code-block:: console

    php spark migrate -g test -n Acme\Blog

当使用 ``--all`` 选项时，它将扫描所有命名空间，尝试找到尚未运行的迁移。这些迁移将被全部收集，然后按创建日期分组排序。这有助于最大限度地减少主应用程序和任何模块之间的潜在冲突。

migrate:rollback
================

将所有迁移回滚到空白状态，即回滚到迁移 0：

.. code-block:: console

  php spark migrate:rollback

你可以将 ``migrate:rollback`` 与以下选项一起使用：

- ``-b`` - 选择批次：自然数指定批次。
- ``-f`` - 强制跳过确认问题，该问题仅在生产环境中被询问。

migrate:refresh
===============

通过首先回滚所有迁移，然后再次执行所有迁移来刷新数据库状态：

.. code-block:: console

  php spark migrate:refresh

你可以将 ``migrate:refresh`` 与以下选项一起使用：

- ``-g`` - 指定数据库组。如果指定了该选项，则仅运行指定数据库组的迁移。如果未指定，则运行所有迁移。
- ``-n`` - 选择命名空间，否则将使用 ``App`` 命名空间。
- ``--all`` - 刷新所有命名空间。
- ``-f`` - 强制跳过确认问题，该问题仅在生产环境中被询问。

migrate:status
==============

显示所有迁移的列表以及它们运行的日期和时间，如果尚未运行则显示 '--'：

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

你可以将 ``migrate:status`` 与以下选项一起使用：

- ``-g`` - 指定数据库组。如果指定了该选项，则仅检查指定数据库组的迁移。如果未指定，则检查所有迁移。

make:migration
==============

在 **app/Database/Migrations** 中创建一个骨架迁移文件。它会自动在文件名前添加当前时间戳。它创建的类名是文件名的帕斯卡命名法（Pascal case）版本。

.. code-block:: console

  php spark make:migration <class> [options]

你可以将 ``make:migration`` 与以下选项一起使用：

- ``--namespace`` - 设置根命名空间。默认值：``APP_NAMESPACE``。
- ``--suffix``    - 将组件标题附加到类名。

以下选项也可用于为数据库会话生成迁移文件：

- ``--session``   - 为数据库会话生成迁移文件。
- ``--table``     - 用于数据库会话的表名。默认值：``ci_sessions``。
- ``--dbgroup``   - 用于数据库会话的数据库组。默认值：``default``。

*********************
迁移配置
*********************

以下是 **app/Config/Migrations.php** 中可用的迁移配置选项表。

==================== ============ ============= =============================================================
配置项               默认值        选项          说明
==================== ============ ============= =============================================================
**enabled**          true         true / false  启用或禁用迁移。
**table**            migrations   无            用于存储模式版本号的表名。此表始终在默认数据库组（``$defaultGroup``）中创建。
**timestampFormat**  Y-m-d-His\_                创建迁移时用于时间戳的格式。
==================== ============ ============= =============================================================

***************
类参考
***************

.. php:namespace:: CodeIgniter\Database

.. php:class:: MigrationRunner

    .. php:method:: findMigrations()

        :returns:    迁移文件的数组
        :rtype:    array

        返回在 ``path`` 属性中找到的迁移文件名数组。

    .. php:method:: latest($group)

        :param    mixed    $group: 数据库组名，如果为 null 则使用默认数据库组。
        :returns:    成功时返回 ``true``，失败时返回 ``false``
        :rtype:    bool

        它会定位命名空间（或所有命名空间）的迁移，确定哪些迁移尚未运行，并按版本顺序运行它们（命名空间混合在一起）。

    .. php:method:: regress($targetBatch, $group)

        :param    int    $targetBatch: 要回滚到的上一批次；1+ 指定批次，0 回滚所有，负数表示相对批次（例如，-3 表示“回滚三批”）
        :param    ?string    $group: 数据库组名，如果为 null 则使用默认数据库组。
        :returns:    成功时返回 ``true``，失败或未找到迁移时返回 ``false``
        :rtype:    bool

        regress 可用于将更改回滚到以前的状态，按批次进行。

        .. literalinclude:: migration/006.php

    .. php:method:: force($path, $namespace, $group)

        :param    mixed    $path:  有效迁移文件的路径。
        :param    mixed    $namespace: 提供的迁移的命名空间。
        :param    mixed    $group: 数据库组名，如果为 null 则使用默认数据库组。
        :returns:    成功时返回 ``true``，失败时返回 ``false``
        :rtype:    bool

        它强制单个文件进行迁移，无论顺序或批次如何。``up()`` 或 ``down()`` 方法根据是否已迁移来确定。

        .. note:: 此方法仅建议用于测试，可能会导致数据一致性问题。

    .. php:method:: setNamespace($namespace)

        :param  string|null  $namespace: 应用程序命名空间。``null`` 表示所有命名空间。
        :returns:   当前的 MigrationRunner 实例
        :rtype:     CodeIgniter\\Database\\MigrationRunner

        设置库应查找迁移文件的命名空间：

        .. literalinclude:: migration/007.php

        .. note:: 如果你设置为 ``null``，它将在所有命名空间中查找迁移文件。

    .. php:method:: setGroup($group)

        :param  string  $group: 数据库组名。
        :returns:   当前的 MigrationRunner 实例
        :rtype:     CodeIgniter\\Database\\MigrationRunner

        设置库应查找迁移文件的组：

        .. literalinclude:: migration/008.php
