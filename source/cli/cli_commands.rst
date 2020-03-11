###################
自定义 CLI 命令
###################

尽管使用 cli 命令和路由一样方便，但是你可能会发现需要一些不同之处的时候。这就是 CLI 命令的来源。它们是简单的类，不需要为之定义路由，因此非常适合构建工具，开发人员可以使用这些工具来简化工作，无论是通过处理迁移或数据库种子，检查 cronjob 状态还是甚至为你的公司构建自定义代码生成器。

.. contents::
    :local:
    :depth: 2

****************
运行命令
****************

命令是从命令行在根目录中运行的。包含 **/app** 和 **/system** 目录的同一目录，提供了一个自定义脚本 **spark** 用于运行任何 cli 命令： ::

    > php spark

在未指定命令的情况下调用时，将显示一个简单的帮助页面，该页面还提供了可用命令的列表。你应该将命令名称作为运行该命令的第一个参数传递： ::

    > php spark migrate

一些命令带有附加参数，应在命令后直接提供，并用空格分隔： ::

    > php spark db:seed DevUserSeeder

对于 CodeIgniter 提供的命令，如果不提供必需的参数，则将提示你输入正确运行所需的信息： ::

    > php spark migrate:version
    > Version?

******************
使用帮助命令
******************

你可以使用 help 命令获得有关任何 CLI 命令的帮助，如下所示： ::

    > php spark help db:seed

*********************
创建新的命令
*********************

你可以非常轻松地创建新命令以在自己的开发中使用。每个类都必须位于其自己的文件中，并且必须 extend ``CodeIgniter\CLI\BaseCommand `` 并 implement ``run()`` 方法。

应该使用以下属性，以便在 CLI 命令中列出并向命令添加帮助功能：

* ($group): 一个字符串，用于描述列出命令时命令所属的组。例如（数据库）
* ($name): 表示命令名称的字符串。例如 ( migrate:create )
* ($description): 描述命令的字符串。例如 ( 创建一个新的迁移文件 )
* ($usage): 描述命令用法的字符串。例如 ( migrate:create [migration_name] [选项] )
* ($arguments): 描述每个命令参数的字符串数组。例如 ( 'migration_name' => '迁移文件名'' )
* ($options): 描述每个命令选项的字符串数组。例如 ( '-n'=>'设置迁移命名空间' )

**帮助描述将根据以上参数自动生成。**

文件位置
=============

命令必须存储在名为 **Commands** 的目录中。但是，该目录可以位于 :doc:`自动加载器 </concepts/autoloader>` 可以找到的任何位置。该目录可以在 **/app/Commands**中，也可以在其中保存命令以在所有项目开发中使用的目录中，例如 **Acme/Commands** 。

.. note:: 执行命令时，将加载完整的 CodeIgniter cli 环境，从而可以获取环境信息，路径信息以及使用制作控制器时将使用的任何工具。

实例命令
==================

让我们看一个示例命令，该命令的唯一功能是为演示目的报告有关应用程序本身的基本信息。首先从 **/app/Commands/AppInfo.php** 创建一个新文件。它应包含以下代码： ::

    <?php namespace App\Commands;

    use CodeIgniter\CLI\BaseCommand;
    use CodeIgniter\CLI\CLI;

    class AppInfo extends BaseCommand
    {
        protected $group       = 'demo';
        protected $name        = 'app:info';
        protected $description = '显示基本应用信息';

        public function run(array $params)
        {

        }
    }

如果运行 **list** 命令，你将在其自己的 ``demo`` 组下看到新命令。如果你仔细看一看，应该会看到它的工作原理。该 ``$group`` 属性只是告诉它如何与所有其他现有命令一起组织此命令，并告诉其列出该标题的标题。

``$name`` 属性是可以调用此命令的名称。唯一的要求是，它不能包含空格，并且所有字符在命令行本身上都必须有效。但是，按照惯例，命令是小写的，通过使用带有命令名称本身的冒号来完成命令的进一步分组。这有助于防止多个命令发生命名冲突。

最后一个属性 ``$description`` 是在 **list** 命令中显示的一条短字符串，应描述命令的作用。

run()
-----

``run()`` 方法是在运行命令时调用的方法。``$params`` 数组是你使用的命令名称后的所有 cli 参数的列表。如果 cli 字符串是： ::

    > php spark foo bar baz

则 **foo** 是命令名称， ``$params`` 数组将是： ::

    $params = ['bar', 'baz'];

This can also be accessed through the :doc:`CLI </cli/cli_library>` library, but this already has your command removed
from the string. These parameters can be used to customize how your scripts behave.

这也可以通过 :doc:`CLI </cli/cli_library>` 库进行获取，但是已经从字符串中删除了你的命令。这些参数可用于自定义脚本的行为。

我们的 demo 命令可能具有 run 类似以下方法： ::

    public function run(array $params)
    {
        CLI::write('PHP Version: '. CLI::color(phpversion(), 'yellow'));
        CLI::write('CI Version: '. CLI::color(CodeIgniter::CI_VERSION, 'yellow'));
        CLI::write('APPPATH: '. CLI::color(APPPATH, 'yellow'));
        CLI::write('SYSTEMPATH: '. CLI::color(SYSTEMPATH, 'yellow'));
        CLI::write('ROOTPATH: '. CLI::color(ROOTPATH, 'yellow'));
        CLI::write('Included files: '. CLI::color(count(get_included_files()), 'yellow'));
    }

***********
BaseCommand
***********

所有命令必须扩展的 ``BaseCommand`` 类具有几个有用的实用程序方法，在创建自己的命令时应熟悉这些方法。在 **$this->logger** 上也有一个 :doc:`Logger </general/logging>` 。

.. php:class:: CodeIgniter\\CLI\\BaseCommand

    .. php:method:: call(string $command[, array $params=[] ])

        :param string $command: 要调用的另一个命令的名称。
        :param array $params: 使该命令可用的附加 cli 参数。

        此方法使你可以在当前命令执行期间运行其他命令： ::

        $this->call('command_one');
        $this->call('command_two', $params);

    .. php:method:: showError(\Exception $e)

        :param Exception $e: 用于错误报告的 Exception。

        一种方便的方法，用于向 cli 保持一致且清晰的错误输出： ::

            try
            {
                . . .
            }
            catch (\Exception $e)
            {
                $this->showError($e);
            }

    .. php:method:: showHelp()

        显示命令帮助的方法：（用法，参数，描述，选项）

    .. php:method:: getPad($array, $pad)

        :param array    $array: 一个关联数组
        :param integer  $pad: 填充空格数

        一个为关联数组输出计算填充的方法。填充可用于在 CLI 中输出格式化的表格： ::

            $pad = $this->getPad($this->options, 6);
            foreach ($this->options as $option => $description)
            {
                    CLI::write($tab . CLI::color(str_pad($option, $pad), 'green') . $description, 'yellow');
            }

            // 输出应该会像这样
            -n                  设置迁移命名空间
            -r                  覆盖文件
