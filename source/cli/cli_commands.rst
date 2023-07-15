#######################
创建 Spark 命令
#######################

虽然能够像其它路由一样通过 CLI 使用控制器很方便,但您可能会发现有时需要一些不同的东西。这就是 Spark 命令的用武之地。它们是简单的类,不需要为它们定义路由,使其成为构建可以帮助开发人员简化工作的工具的完美选择,无论是通过处理迁移或数据库填充,检查任务状态,甚至为您的公司构建定制代码生成器。

.. contents::
    :local:
    :depth: 2

*********************
创建新命令
*********************

您可以非常轻松地创建新的命令供自己开发使用。每个类必须在其自己的文件中,并且必须扩展 ``CodeIgniter\CLI\BaseCommand``,并实现 ``run()`` 方法。

应使用以下属性将命令列入 CLI 命令并添加帮助功能:

* ``$group``:描述命令分组的字符串。例如:``数据库``
* ``$name``:描述命令名称的字符串。例如:``make:controller``
* ``$description``:描述命令的字符串。例如:``生成一个新的控制器文件。``
* ``$usage``:描述命令用法的字符串。例如:``make:controller <name> [options]``
* ``$arguments``:描述每个命令参数的字符串数组。例如:``'name' => '控制器类名。'``
* ``$options``:描述每个命令选项的字符串数组。例如:``'--force' => '强制覆盖现有文件。'``

**帮助描述将根据上述参数自动生成。**

文件位置
=============

命令必须存储在名为 **Commands** 的目录中。但是,该目录必须位于 PSR-4 命名空间中,以便 :doc:`自动加载程序 </concepts/autoloader>` 可以定位它。这可能在 **app/Commands** 中,或者是一个用于所有项目开发的命令目录,像 **Acme/Commands**。

.. note:: 当执行命令时,会加载完整的 CodeIgniter CLI 环境,使您可以获取环境信息、路径信息,并使用控制器中会使用的任何工具。

一个示例命令
==================

让我们逐步创建一个示例命令,其唯一的功能是报告有关应用程序本身的一些基本信息,以演示用途。首先在 **app/Commands/AppInfo.php** 中创建一个新文件。它
应该包含以下代码:

.. literalinclude:: cli_commands/002.php

如果运行 **list** 命令,您将在自己的 ``Demo`` 组下看到新命令被列出。如果仔细看,应该可以相当容易地理解它的工作方式。``$group`` 属性简单地告诉它如何组织此命令与所有其他存在的命令,告诉它在哪个标题下列出它。

``$name`` 属性是可以调用此命令的名称。唯一的要求是它不得包含空格,并且所有字符在命令行本身必须有效。不过,按照惯例,命令应该是小写的,并且通过在命令名称本身使用冒号进一步对命令进行分组,以帮助防止多个命令发生命名冲突。

最后一个属性 ``$description`` 是一个简短的字符串,在 **list** 命令中显示,并应描述命令的作用。

run()
-----

``run()`` 方法是在运行命令时调用的方法。``$params`` 数组是命令名称后面的任何 CLI 参数列表,供您使用。如果 CLI 字符串是:

    > php spark foo bar baz

那么 **foo** 是命令名称,``$params`` 数组将是:

.. literalinclude:: cli_commands/003.php

这也可以通过 :doc:`CLI </cli/cli_library>` 库访问,但这里已经从字符串中删除了您的命令。这些参数可以用于自定义脚本的行为方式。

我们的演示命令可能有一个 ``run()`` 方法,如下所示:

.. literalinclude:: cli_commands/004.php

请参阅 :doc:`CLI 库 </cli/cli_library>` 页面了解详细信息。

命令终止
-------------------

默认情况下,命令以成功代码 ``0`` 退出。如果在执行命令时遇到错误,您可以通过在 ``run()`` 方法中使用 ``return`` 语句和退出代码来终止命令。

例如,``return EXIT_ERROR;``

这种方法可以帮助系统级调试,如果命令例如通过 crontab 运行。

您可以使用 **app/Config/Constants.php** 文件中定义的 ``EXIT_*`` 退出代码常量。

***********
BaseCommand
***********

所有命令必须扩展的 ``BaseCommand`` 类有一些您应该熟悉的有用实用方法,当创建自己的命令时。它还具有可以通过 ``$this->logger`` 访问的 :doc:`日志 </general/logging>`。

.. php:namespace:: CodeIgniter\CLI

.. php:class:: BaseCommand

    .. php:method:: call(string $command[, array $params = []])

        :param string $command: 要调用的另一个命令的名称。
        :param array $params: 要传递给该命令的其他 CLI 参数。

        此方法允许您在当前命令执行期间运行其他命令:

        .. literalinclude:: cli_commands/005.php

    .. php:method:: showError(Throwable $e)

        :param Throwable $e: 用于报告错误的异常。

        一种保持 CLI 错误输出一致且清晰的便捷方法:

        .. literalinclude:: cli_commands/006.php

    .. php:method:: showHelp()

        显示命令帮助的方法:(用法、参数、描述、选项)

    .. php:method:: setPad(string $item, int $max, int $extra = 2, int $indent = 0): string

        :param string   $item: 字符串项目。
        :param integer  $max: 最大长度。
        :param integer  $extra: 在末尾添加的额外空格数。
        :param integer  $indent: 缩进空格数。

        填充我们的字符串,以便所有标题的长度相同,以美观地排列描述:

        .. literalinclude:: cli_commands/007.php
            :lines: 2-

   .. php:method:: getPad($array, $pad)

        .. deprecated:: 4.0.5
            请使用 :php:meth:`CodeIgniter\\CLI\\BaseCommand::setPad()`。

        :param array    $array: ``$key => $value`` 数组。
        :param integer  $pad: 填充的空格数。

        计算用于 ``$key => $value`` 数组输出的填充的方法。该填充可用于在 CLI 中输出格式良好的表格。
