###########################
通过 CLI 运行控制器
###########################

除了通过浏览器的 URL 调用应用程序的 :doc:`控制器 </incoming/controllers>` 外,
它们也可以通过命令行接口 (CLI) 加载。

.. note:: 建议使用 Spark 命令来编写 CLI 脚本,而不是通过 CLI 调用控制器。
    有关详细信息,请参阅 :doc:`spark_commands` 和 :doc:`cli_commands` 页面。

.. contents::
    :local:
    :depth: 2

**************************
让我们试一试:Hello World!
**************************

创建控制器
===================

让我们创建一个简单的控制器,这样你就可以看到它的实际效果。使用文本编辑器,
创建一个名为 Tools.php 的文件,并添加以下代码:

.. literalinclude:: cli_controllers/001.php

.. note:: 如果使用 :ref:`auto-routing-improved`,请将方法名更改为 ``cliMessage()``。

然后将该文件保存到 **app/Controllers/** 目录中。

定义路由
==============

如果使用自动路由,请跳过此步骤。

在 **app/Config/Routes.php** 文件中,你可以轻松创建只能通过 CLI 访问的路由,
就像创建任何其他路由一样。与使用 ``get()``、``post()``
或类似的方法不同,你将使用 ``cli()`` 方法。其他所有内容的工作原理与正常的路由定义完全相同:

.. literalinclude:: cli_controllers/002.php

有关更多信息,请参阅 :ref:`Routes <command-line-only-routes>` 页面。

.. warning:: 如果启用 :ref:`auto-routing-legacy` 并将命令文件放在 **app/Controllers** 中,
    任何人都可以在 :ref:`auto-routing-legacy` 的帮助下通过 HTTP 访问该命令。

通过 CLI 运行
=================

通常,你会使用类似于以下内容的 URL 访问站点::

    example.com/index.php/tools/message/to

相反,我们将在 Mac/Linux 上打开终端,或者在 Windows 上转到运行窗口 > “cmd”,
并导航到 CodeIgniter 项目的 web 根目录。

.. code-block:: bash

    $ cd /path/to/project/public
    $ php index.php tools message

如果你操作正确,应该会看到打印出 “Hello World!”。

.. code-block:: bash

    $ php index.php tools message “John Smith”

这里我们以参数的方式传递内容,就像 URL 参数的工作方式一样。
“John Smith” 被作为参数传递,输出是:

    Hello John Smith!

******************
这就是基础知识!
******************

简而言之,这就是有关命令行上的控制器需要了解的全部内容。
请记住,这是一个正常的控制器,因此路由和 ``_remap()`` 正常工作。

.. note:: ``_remap()`` 在 :ref:`auto-routing-improved` 中不起作用。

如果要确保通过 CLI 运行,请检查 :php:func:`is_cli()` 的返回值。

但是,CodeIgniter 提供了其他工具,可以使创建 CLI 可访问的脚本更加愉快,
包括 CLI 專用路由和一个可以帮助你使用 CLI 專用工具的库。
