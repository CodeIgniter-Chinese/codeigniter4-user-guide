##########
数据库迁移
##########

迁移是一种以结构化和有序的方式修改数据库的便捷方法。你可以手工编辑 SQL 片段,但这样你就需要告知其他开发者他们需要运行这些片段。你也需要在下次部署到生产环境时跟踪哪些更改需要运行。

数据库表 **迁移** 用于跟踪已经运行的迁移，因此你只需确保你的迁移文件已经准备好，并运行 ``spark migrate`` 命令将数据库更新到最新状态。你还可以使用 ``spark migrate --all`` 命令来包括所有命名空间的迁移。

.. contents::
   :local:
   :depth: 2

********************
迁移文件命名
********************

每个迁移会按照创建时的数字顺序正向或反向运行,具体取决于采取的方法。每个迁移使用创建时的时间戳命名,格式为 **YYYY-MM-DD-HHIISS** (例如 **2012-10-31-100537**)。这有助于在团队环境下避免编号冲突。

为你的迁移文件添加迁移编号前缀,后跟下划线和对迁移的描述性名称。年、月、日可以用破折号、下划线或不加分隔符的方式分割。例如:

* 2012-10-31-100538_AlterBlogTrackViews.php
* 2012_10_31_100539_AlterBlogAddTranslations.php
* 20121031100537_AddBlog.php

******************
创建迁移
******************

这将是为一个带博客的新网站创建的第一个迁移。所有迁移都在 **app/Database/Migrations/** 目录下,文件名类似 **2022-01-31-013057_AddBlog.php**。

.. literalinclude:: migration/001.php

数据库连接和数据库 Forge 类都可以通过 ``$this->db`` 和 ``$this->forge`` 获取。

或者,你可以使用命令行调用来生成骨架迁移文件。更多细节请参阅 :ref:`command-line-tools` 中的 **make:migration**。

.. note:: 由于迁移类是一个 PHP 类,每个迁移文件中的类名必须是唯一的。

外键
============

当你的表包含外键时,迁移经常在尝试删除表和列时会遇到问题。要在运行迁移时暂时绕过外键检查,可以在数据库连接上使用 ``disableForeignKeyChecks()`` 和 ``enableForeignKeyChecks()`` 方法。

.. literalinclude:: migration/002.php

数据库组
===============

迁移只会针对单个数据库组运行。如果你在 **app/Config/Database.php** 中定义了多个组,那么它将针对那里指定的 ``$defaultGroup`` 运行。

有时你可能需要为不同的数据库组使用不同的模式。也许你有一个数据库用于所有常规站点信息,而另一个数据库用于业务关键的数据。

你可以通过在迁移上设置 ``$DBGroup`` 属性来确保迁移只针对适当的组运行。此名称必须与数据库组的名称完全匹配:

.. literalinclude:: migration/003.php

命名空间
==========

迁移库可以自动扫描你在 **app/Config/Autoload.php** 中定义的所有命名空间,或者从 Composer 等外部源加载的命名空间,使用 ``$psr4`` 属性匹配目录名称。它将包含在 **Database/Migrations** 中找到的所有迁移。

每个命名空间都有自己的版本序列,这将帮助你升级和降级每个模块(命名空间)而不影响其他命名空间。

例如,假设我们在 Autoload 配置文件中定义了以下命名空间:

.. literalinclude:: migration/004.php

这将查找 **APPPATH/Database/Migrations** 和 **ROOTPATH/MyCompany/Database/Migrations** 中的任何迁移。这使得在你的可重用、模块化代码套件中包含迁移变得很简单。

.. _command-line-tools:

*******************
命令行工具
*******************

CodeIgniter 自带了几个 :doc:`commands </cli/spark_commands>`,可通过命令行访问,以帮助你使用迁移。这些工具使得使用迁移更加方便。这些工具主要提供了 MigrationRunner 类中可用的相同方法的访问。

migrate
=======

使用所有可用的迁移迁移一个数据库组:

.. code-block:: console

    php spark migrate

你可以对 (migrate) 使用以下选项:

- ``-g`` - 用于指定数据库组。如果指定了该选项，只会运行指定数据库组的迁移。如果未指定，则会运行所有迁移。
- ``-n`` - 用于选择命名空间，否则将使用 ``App`` 命名空间。
- ``--all`` - 迁移所有命名空间到最新的迁移。

这个例子将在 test 数据库组上使用任何新的迁移迁移 ``Acme\Blog`` 命名空间:

For Unix:

.. code-block:: console

    php spark migrate -g test -n Acme\\Blog

For Windows:

.. code-block:: console

    php spark migrate -g test -n Acme\Blog

当使用 ``--all`` 选项时,它将扫描所有命名空间,尝试找到任何未运行的迁移。这些迁移将一起收集,然后按创建日期排序为一组。这应该有助于最大限度地减少主应用程序和任何模块之间的潜在冲突。

rollback
========

回滚所有迁移到空白状态,有效迁移到 0:

.. code-block:: console

  php spark migrate:rollback

你可以对 (rollback) 使用以下选项:

- ``-b`` - 选择批次:自然数指定批次。
- ``-f`` - 强制绕过确认问题,它仅在生产环境中询问。

refresh
=======

首先回滚所有迁移,然后迁移所有来刷新数据库状态:

.. code-block:: console

  php spark migrate:refresh

你可以对 (refresh) 使用以下选项:

- ``-g`` - 用于指定数据库组。如果指定了该选项，只会运行指定数据库组的迁移。如果未指定，则会运行所有迁移。
- ``-n`` - 用于选择命名空间，否则将使用 ``App`` 命名空间。
- ``--all`` - 刷新所有命名空间。
- ``-f`` - 强制绕过确认问题,它仅在生产环境中询问。

status
======

显示所有迁移的列表以及它们运行的日期和时间,如果未运行则显示 '--':

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

你可以对 (status) 使用以下选项:

- ``-g`` - 用于指定数据库组。如果指定了该选项，只会检查指定数据库组的迁移。如果未指定，则会检查所有迁移。

make:migration
==============

在 **app/Database/Migrations** 中创建一个骨架迁移文件。它会自动在文件名前加上当前时间戳。它创建的类名是文件名的大驼峰版本。

.. code-block:: console

  php spark make:migration <class> [options]

你可以对 (``make:migration``) 使用以下选项:

- ``--namespace`` - 设置根命名空间。默认: ``APP_NAMESPACE``。
- ``--suffix``    - 在类名后追加组件标题。

以下选项也可用于为数据库 Sessions 生成迁移文件:

- ``--session``   - 为数据库 sessions 生成迁移文件。
- ``--table``     - 数据库 sessions 使用的表名。默认: ``ci_sessions``。
- ``--dbgroup``   - 数据库 sessions 使用的数据库组。默认: ``default``。

*********************
迁移配置
*********************

下表列出了所有迁移的配置选项,在 **app/Config/Migrations.php** 中可用。

========================== ====================== ========================== =================================================================================
首选项                     默认值                  可选值                     描述
========================== ====================== ========================== =================================================================================
**enabled**                true                   true / false               启用或禁用迁移。
**table**                  migrations             None                       用于存储 schema 版本号的表名。该表始终在默认数据库组（``$defaultGroup``）中创建。
**timestampFormat**        Y-m-d-His\_                                       创建迁移时使用的时间戳格式。
========================== ====================== ========================== =================================================================================

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

        :param    mixed    $group: 数据库组名称,如果为 null 则使用默认数据库组。
        :returns:    成功则为 ``true``,失败则为 ``false``
        :rtype:    bool

        该方法定位命名空间(或所有命名空间)的迁移,确定哪些迁移尚未运行,并按版本顺序运行它们(命名空间交错)。

    .. php:method:: regress($targetBatch, $group)

        :param    int    $targetBatch: 要迁移到的前一批次; 1+ 指定批次,0 还原全部,负数指相对批次(例如 -3 表示“往前三批”)
        :param    ?string    $group: 数据库组名称,如果为 null 则使用默认数据库组。
        :returns:    成功则为 ``true``,失败或找不到迁移则为 ``false``
        :rtype:    bool

        回滚可用于将更改回滚到以前的状态,逐批进行。

        .. literalinclude:: migration/006.php

    .. php:method:: force($path, $namespace, $group)

        :param    mixed    $path:  有效迁移文件的路径。
        :param    mixed    $namespace: 所提供迁移的命名空间。
        :param    mixed    $group: 数据库组名称,如果为 null 则使用默认数据库组。
        :returns:    成功则为 ``true``,失败则为 ``false``
        :rtype:    bool

        该方法强制单文件迁移,不考虑顺序或批次。基于它是否已经迁移来检测 ``up()`` 或 ``down()`` 方法。

        .. note:: 该方法仅建议用于测试,可能会导致数据一致性问题。

    .. php:method:: setNamespace($namespace)

        :param  string|null  $namespace: 应用程序命名空间。``null`` 为所有命名空间。
        :returns:   当前的 MigrationRunner 实例
        :rtype:     CodeIgniter\\Database\\MigrationRunner

        设置库应查找迁移文件的命名空间:

        .. literalinclude:: migration/007.php

        .. note:: 如果设置为 ``null``,则它将查找所有命名空间中的迁移文件。

    .. php:method:: setGroup($group)

        :param  string  $group: 数据库组名称。
        :returns:   当前的 MigrationRunner 实例
        :rtype:     CodeIgniter\\Database\\MigrationRunner

        设置库应查找迁移文件的组:

        .. literalinclude:: migration/008.php
