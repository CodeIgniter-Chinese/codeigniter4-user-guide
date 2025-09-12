###########################
通过 CLI 运行控制器
###########################

除了通过浏览器中的 URL 调用应用程序的 :doc:`控制器 </incoming/controllers>` 外，还可以通过命令行接口 (CLI) 来加载它们。

.. note:: 建议为 CLI 脚本使用 Spark 命令，而不是通过 CLI 调用控制器。
    有关详细信息，请参阅 :doc:`spark_commands` 和 :doc:`cli_commands` 页面。

.. contents::
    :local:
    :depth: 2

**************************
动手试试：Hello World!
**************************

创建控制器
===================

让我们创建一个简单的控制器，以便你直观地看到它的运行效果。使用你的文本编辑器，创建一个名为 Tools.php 的文件，并将以下代码放入其中：

.. literalinclude:: cli_controllers/001.php

.. note:: 如果你使用 :ref:`auto-routing-improved`，请将方法名改为 ``cliMessage()``。

然后将文件保存到你的 **app/Controllers/** 目录中。

定义路由
==============

如果使用自动路由，则可以跳过此步骤。

在你的 **app/Config/Routes.php** 文件中，可以像创建其他任何路由一样轻松地创建仅可通过 CLI 访问的路由。你不需要使用 ``get()``、``post()`` 或类似的方法，而是使用 ``cli()`` 方法。其他所有内容的工作方式都与普通路由定义完全相同：

.. literalinclude:: cli_controllers/002.php

有关更多信息，请参阅 :ref:`路由 <command-line-only-routes>` 页面。

.. warning:: 如果你启用了 :ref:`auto-routing-legacy` 并将命令文件放在 **app/Controllers** 目录中，
    任何人都可以通过 HTTP 并借助 :ref:`auto-routing-legacy` 访问该命令。

通过 CLI 运行
=============

通常，你会使用类似这样的 URL 访问你的网站::

    example.com/index.php/tools/message/to

相反，我们将在 Mac/Linux 上打开终端，或在 Windows 上打开“运行” > “cmd”，
在 Windows 中导航到你的 CodeIgniter 项目的 Web 根目录。

.. code-block:: bash

    $ cd /path/to/project/public
    $ php index.php tools message

如果操作正确，你应该会看到打印出的 "Hello World!"。

.. code-block:: bash

    $ php index.php tools message "John Smith"

这里我们以与 URL 参数相同的方式传递了一个参数。"John Smith" 作为参数被传递，输出结果为::

    Hello John Smith!

******************
基础知识就这些！
******************

总而言之，关于命令行上的控制器，你需要了解的就这些。请记住，这只是一个普通的控制器，因此路由和 ``_remap()`` 方法都能正常工作。

.. note:: ``_remap()`` 与 :ref:`auto-routing-improved` 不兼容。

如果要确认是否通过 CLI 运行，可以检查 :php:func:`is_cli()` 的返回值。

然而，CodeIgniter 提供了额外的工具，使创建可通过 CLI 访问的脚本变得更加便捷，包括仅限 CLI 的路由，以及一个帮助你处理仅限 CLI 工具的库。
