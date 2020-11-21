#################
数据库迁移
#################
迁移是一种有条理、有组织的方式更改数据库的便捷方式。你可以手动编辑SQL的片段，然后你要负责告诉其他开发人员他们也需要去运行这段SQL。你还必须跟踪下次部署时需要对生产机器运行哪些更改。

数据库表**迁移**会跟踪已经运行的迁移，因此您只需更新应用程序文件并调用$migration->current()以确定应运行哪些迁移。当前版本位于**application/Config/Migrations.php**中。

- 迁移文件名
- 创建迁移
- 使用$currentVersion
    - 数据库组
    - 命名空间
    - 用法示例
- 命令行工具
- 迁移参数
- 类参考

**************
迁移文件名
**************
每个迁移都按数字顺序向前或向后运行，具体取决于所采用的方法。有两种编号样式可供选择：

- **顺序**：每个迁移按顺序编号，从001开始。每个数字必须是三位数，并且序列中不得有任何间隙。（这是CodeIgniter 3.0之前的编号方案。）
- **时间戳**：使用创建迁移时的时间戳对每个迁移进行编号，格式为**YYYYMMDDHHIES**格式（例如**20121031100537**）。这有助于防止在团队环境中工作时出现编号冲突，并且是CodeIgniter 3.0及更高版本中的首选方案。

可以使用*application/Config/Migrations.php*文件中的$type设置选择所需的样式。默认设置为时间戳。

无论您选择使用哪种编号样式，请在迁移文件前加上迁移编号，后跟下划线和迁移的描述性名称。例如：

- 001_add_blog.php（顺序编号）
- 20121031100537_add_blog.php（时间戳编号）

**************
创建迁移
**************

这将是新博客站点的首次迁移。所有迁移都在 **application/Database/Migrations/** 目录中，并命名，如 *20121031100537_Add_blog.php*。
::

	<?php namespace App\Database\Migrations;

	use CodeIgniter\Database\Migration;

	class AddBlog extends Migration
	{

		public function up()
		{
			$this->forge->addField([
				'blog_id'          => [
					'type'           => 'INT',
					'constraint'     => 5,
					'unsigned'       => true,
					'auto_increment' => true,
				],
				'blog_title'       => [
					'type'           => 'VARCHAR',
					'constraint'     => '100',
				],
				'blog_description' => [
					'type'           => 'TEXT',
					'null'           => true,
				],
			]);
			$this->forge->addKey('blog_id', true);
			$this->forge->createTable('blog');
		}

		public function down()
		{
			$this->forge->dropTable('blog');
		}
	}

然后在 **application/Config/Migrations.php** 中设置 $currentVersion = 20121031100537;。

数据库连接和数据库Forge类都可以通过 $this->db和$this->forge分别使用。

或者，你可以使用命令行调用来生成框架迁移文件。请参阅下面的更多细节。

**********************
使用$currentVersion
**********************

$currentVersion设置允许你标记应用程序命名空间应设置的位置。这对于在生产环境中使用尤其有用。在你的应用程序中，你始终可以将迁移更新到当前版本，而不是最新版本，以确保生产和登台服务器正在运行正确的架构。在开发服务器上，你可以为尚未准备好生产的代码添加其他迁移。通过使用该latest()方法，你可以确保你的开发机器始终运行前沿架构。

**************
数据库组
**************

只能针对单个数据库组运行迁移。如果 **在application/Config/Database.php** 中定义了多个组 ，则它将针对该$defaultGroup同一配置文件中指定的组运行。有时你可能需要为不同的数据库组使用不同的模式。也许你有一个用于所有常规站点信息的数据库，而另一个数据库用于关键任务数据。通过$DBGroup在迁移上设置属性，可以确保仅针对正确的组运行迁移。此名称必须与数据库组的名称完全匹配::

    class Migration_Add_blog extends \CodeIgniter\Database\Migration
    {
      protected $DBGroup = 'alternate_db_group';

      public function up() { . . . }

      public function down() { . . . }
    }

**************
命名空间
**************

迁移库可以自动扫描你在 **application/Config/Autoload.php** 中定义的所有名称空间 及其$psr4属性以匹配目录名称。它将包括它在Database/Migrations中找到的所有迁移。

每个命名空间都有自己的版本序列，这将帮助您升级和降级每个模块（命名空间），而不会影响其他命名空间。

例如，假设我们在Autoload配置文件中定义了以下命名空间::

    $psr4 = [
            'App'       => APPPATH,
            'MyCompany' => ROOTPATH.'MyCompany'
    ];

这将查找位于**APPPATH/Database/Migrations**和**ROOTPATH/Database/Migrations**的任何迁移。这使得在可重用的模块化代码套件中包含迁移变得简单。

**************
用法示例
**************

在此示例中，一些简单的代码放在 **application/Controllers/Migrate.php** 中以更新架构::

    <?php

    class Migrate extends \CodeIgniter\Controller
    {

            public function index()
            {
                    $migrate = \Config\Services::migrations();

                    try
                    {
                    $migrate->current();
                    }
                    catch (\Exception $e)
                    {
                      // Do something with the error here...
                    }
            }

    }

**************
命令行工具
**************

CodeIgniter附带了几个:doc:`commands </cli/cli_commands>`，它们可以从命令行获得，以帮助你处理迁移。这些工具不需要使用迁移，但可能会使那些希望使用它们的人更容易。这些工具主要提供对MigrationRunner类中可用的相同方法的访问。

**migrate**

Migrates a database group with all available migrations::

    > php spark migrate

You can use (migrate) with the following options:

- ``-g`` - to chose database group, otherwise default database group will be used.
- ``-n`` - to choose namespace, otherwise (App) namespace will be used.
- ``-all`` - to migrate all namespaces to the latest migration

This example will migrate Blog namespace with any new migrations on the test database group::

    > php spark migrate -g test -n Blog

When using the ``-all`` option, it will scan through all namespaces attempting to find any migrations that have
not been run. These will all be collected and then sorted as a group by date created. This should help
to minimize any potential conflicts between the main application and any modules.

**rollback**

回滚所有迁移，将所有数据库组转为空白平板，有效迁移0::

    > php spark migrate:rollback

你可以使用（rollback）以下选项：

- （-g）选择数据库组，否则将使用默认数据库组。
- （-n）选择名称空间，否则将使用（App）名称空间。
- （all）将所有名称空间迁移到最新的迁移

**refresh**

首先回滚所有迁移，然后迁移到最新版本，刷新数据库状态::

    > php spark migrate:refresh

你可以使用（refresh）以下选项：

- （-g）选择数据库组，否则将使用默认数据库组。
- （-n）选择名称空间，否则将使用（App）名称空间。
- （all）将所有名称空间迁移到最新的迁移

**status**

显示所有迁移的列表及其运行的日期和时间，如果尚未运行，则显示'--'::

    > php spark migrate:status
    Filename               Migrated On
    First_migration.php    2016-04-25 04:44:22

你可以使用（status）以下选项：

- （-g）选择数据库组，否则将使用默认数据库组。

**make:migration**

Creates a skeleton migration file in **app/Database/Migrations**.
It automatically prepends the current timestamp. The class name it
creates is the Pascal case version of the filename.

::

  > php spark make:migration <class> [options]

You can use (make:migration) with the following options:

- ``-n`` - to choose namespace, otherwise the value of ``APP_NAMESPACE`` will be used.
- ``-force`` - If a similarly named migration file is present in destination, this will be overwritten.

**************
迁移参数
**************
以下是 **app/Config/Migrations.php** 中提供的所有迁移配置选项的表。

========================== ====================== ========================== =============================================================
参数                        默认值                  可选项                      描述
========================== ====================== ========================== =============================================================
**enabled**                true                   true / false               启用或者禁用迁移
**table**                  migrations             None                       用于存储当前版本的数据库表名
**timestampFormat**        Y-m-d-His\_                                       The format to use for timestamps when creating a migration.
========================== ====================== ========================== =============================================================

**************
类参考
**************
    .. php:class:: CodeIgniter\Database\MigrationRunner

            .. php:method:: current($group)

                    :param  mixed   $group: database group name, if null (App) namespace will be used.
                    :returns:       TRUE if no migrations are found, current version string on success, FALSE on failure
                    :rtype: mixed

                    Migrates up to the current version (whatever is set for
                    ``$currentVersion`` in *application/Config/Migrations.php*).

            .. php:method:: findMigrations()

                    :returns:       An array of migration files
                    :rtype: array

                    An array of migration filenames are returned that are found in the **path** property.

            .. php:method:: latest($namespace, $group)

                    :param  mixed   $namespace: application namespace, if null (App) namespace will be used.
                    :param  mixed   $group: database group name, if null default database group will be used.
                    :returns:       Current version string on success, FALSE on failure
                    :rtype: mixed

                    This works much the same way as ``current()`` but instead of looking for
                    the ``$currentVersion`` the Migration class will use the very
                    newest migration found in the filesystem.
            .. php:method:: latestAll($group)

                    :param  mixed   $group: database group name, if null default database group will be used.
                    :returns:       TRUE on success, FALSE on failure
                    :rtype: mixed

                    This works much the same way as ``latest()`` but instead of looking for
                    one namespace, the Migration class will use the very
                    newest migration found for all namespaces.
            .. php:method:: version($target_version, $namespace, $group)

                    :param  mixed   $namespace: application namespace, if null (App) namespace will be used.
                    :param  mixed   $group: database group name, if null default database group will be used.
                    :param  mixed   $target_version: Migration version to process
                    :returns:       TRUE if no migrations are found, current version string on success, FALSE on failure
                    :rtype: mixed

                    Version can be used to roll back changes or step forwards programmatically to
                    specific versions. It works just like ``current()`` but ignores ``$currentVersion``.
                    ::

                            $migration->version(5);

            .. php:method:: setNamespace($namespace)

              :param  string  $namespace: application namespace.
              :returns:   The current MigrationRunner instance
              :rtype:     CodeIgniter\Database\MigrationRunner

              Sets the path the library should look for migration files::

                $migration->setNamespace($path)
                          ->latest();
            .. php:method:: setGroup($group)

              :param  string  $group: database group name.
              :returns:   The current MigrationRunner instance
              :rtype:     CodeIgniter\Database\MigrationRunner

              Sets the path the library should look for migration files::

                $migration->setNamespace($path)
                          ->latest();