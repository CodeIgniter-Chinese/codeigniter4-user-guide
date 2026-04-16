#######################
创建 Spark 命令
#######################

虽然通过 CLI 使用控制器（就像使用其他任何路由一样）很方便，但你可能会遇到需要一些不同功能的情况。这时 Spark 命令就派上用场了。它们是简单的类，不需要定义路由，非常适合构建开发者可用的工具，让工作更轻松，无论是处理迁移或数据库填充、检查 cronjob 状态，还是为你公司构建自定义代码生成器。

.. contents::
    :local:
    :depth: 2

*********************
创建新命令
*********************

你可以非常轻松地创建新命令用于自己的开发。每个类必须位于自己的文件中，并且必须继承 ``CodeIgniter\CLI\BaseCommand``，并实现 ``run()`` 方法。

应使用以下属性，以便在 CLI 命令列表中显示你的命令并为其添加帮助功能：

* ``$group``：一个字符串，用于描述命令在列出时所属的组。例如：``Database``
* ``$name``：一个字符串，用于描述命令的名称。例如：``make:controller``
* ``$description``：一个字符串，用于描述命令。例如：``Generates a new controller file.``
* ``$usage``：一个字符串，用于描述命令的用法。例如：``make:controller <name> [options]``
* ``$arguments``：一个字符串数组，用于描述每个命令参数。例如：``'name' => 'The controller class name.'``
* ``$options``：一个字符串数组，用于描述每个命令选项。例如：``'--force' => 'Force overwrite existing file.'``

**帮助描述将根据上述参数自动生成。**

文件位置
=============

命令必须存储在名为 **Commands** 的目录中。但是，该目录必须位于 PSR-4 命名空间中，以便 :doc:`自动加载器 </concepts/autoloader>` 能够找到它。这可以是 **app/Commands**，或者你为所有项目开发保存命令的目录，例如 **Acme/Commands**。

.. note:: 执行命令时，完整的 CodeIgniter CLI 环境已经加载，因此可以获取环境信息、路径信息，并使用创建控制器时会用到的任何工具。

示例命令
==================

让我们通过一个示例命令来逐步了解，该命令的唯一功能是报告应用程序本身的基本信息，仅用于演示目的。首先在 **app/Commands/AppInfo.php** 创建一个新文件。它应包含以下代码：

.. literalinclude:: cli_commands/002.php

如果运行 **list** 命令，你将看到新命令列在它自己的 ``Demo`` 组下。仔细观察，你应该很容易理解它是如何工作的。``$group`` 属性只是告诉它如何将此命令与所有其他存在的命令组织在一起，告诉它在哪个标题下列出。

``$name`` 属性是此命令的调用名称。唯一的要求是它不能包含空格，且所有字符在命令行本身上必须是有效的。不过按照惯例，命令是小写的，通过在命令名称本身使用冒号来进行进一步的命令分组。这有助于避免多个命令出现命名冲突。

最后一个属性 ``$description`` 是一个短字符串，在 **list** 命令中显示，应描述命令的功能。

run()
-----

``run()`` 方法是执行命令时调用的方法。``$params`` 数组是你可用的命令名称之后的任何 CLI 参数列表。如果 CLI 字符串是：

.. code-block:: console

    php spark foo bar baz

那么 **foo** 是命令名称，``$params`` 数组将是：

.. literalinclude:: cli_commands/003.php

这也可以通过 :doc:`CLI </cli/cli_library>` 库访问，但它已经从字符串中移除了你的命令。这些参数可用于自定义脚本的行为方式。

我们的演示命令的 ``run()`` 方法可能类似于：

.. literalinclude:: cli_commands/004.php

有关详细信息，请参阅 :doc:`CLI 库 </cli/cli_library>` 页面。

命令终止
-------------------

默认情况下，命令以成功代码 ``0`` 退出。如果在执行命令时遇到错误，可以在 ``run()`` 方法中使用 ``return`` 语言结构并附带退出代码来终止命令。

例如，``return EXIT_ERROR;``

如果命令（例如通过 crontab 运行）在系统级别进行调试，这种方法会很有帮助。

你可以使用在 **app/Config/Constants.php** 文件中定义的 ``EXIT_*`` 退出代码常量。

***********
BaseCommand
***********

所有命令必须继承的 ``BaseCommand`` 类有几个在创建自己命令时应熟悉的有用工具方法。它还在 ``$this->logger`` 处提供了一个 :doc:`Logger </general/logging>`。

.. php:namespace:: CodeIgniter\CLI

.. php:class:: BaseCommand

    .. php:method:: call(string $command[, array $params = []])

        :param string $command: 要调用的另一个命令的名称。
        :param array $params: 提供给该命令的额外 CLI 参数。

        此方法允许你在当前命令执行期间运行其他命令：

        .. literalinclude:: cli_commands/005.php

    .. php:method:: showError(Throwable $e)

        :param Throwable $e: 用于错误报告的异常。

        一种便捷方法，用于在 CLI 中保持一致且清晰的错误输出：

        .. literalinclude:: cli_commands/006.php

    .. php:method:: showHelp()

        一种显示命令帮助的方法：（用法、参数、描述、选项）

    .. php:method:: setPad(string $item, int $max, int $extra = 2, int $indent = 0): string

        :param string   $item: 字符串项。
        :param integer  $max: 最大尺寸。
        :param integer  $extra: 在末尾添加的额外空格数。
        :param integer  $indent: 缩进空格数。

        填充字符串，使所有标题长度相同，以便整齐地对齐描述：

        .. literalinclude:: cli_commands/007.php
            :lines: 2-

    .. php:method:: getPad($array, $pad)

        .. deprecated:: 4.0.5
            改用 :php:meth:`CodeIgniter\\CLI\\BaseCommand::setPad()`。

        :param array    $array: $key => $value 数组。
        :param integer  $pad: 填充空格数。

        一种计算 ``$key => $value`` 数组输出填充的方法。填充可用于在 CLI 中输出格式良好的表格。
