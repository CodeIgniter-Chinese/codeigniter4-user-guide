##############
Spark 命令
##############

CodeIgniter 提供了官方命令 **spark** 和内置命令。

.. contents::
    :local:
    :depth: 3

****************
运行命令
****************

通过 CLI 运行
===============

命令是从命令行中在项目根目录下运行的。
提供了一个名为 **spark** 的命令文件，用于运行任何 CLI 命令。

显示命令列表
------------------------

当不指定命令调用 **spark** 时，会显示一个简单的帮助页面，其中还提供了按类别排序的可用命令列表及其描述：

.. code-block:: console

    php spark

spark list
^^^^^^^^^^

``php spark`` 与 ``list`` 命令完全相同：

.. code-block:: console

    php spark list

您还可以使用 ``--simple`` 选项获取按字母顺序排序的所有可用命令的原始列表：

.. code-block:: console

    php spark list --simple

显示帮助
------------

您可以使用 ``help`` 命令获取有关任何 CLI 命令的帮助，如下所示：

.. code-block:: console

    php spark help db:seed

自 v4.3.0 起，您还可以使用 ``--help`` 选项代替 ``help`` 命令：

.. code-block:: console

    php spark db:seed --help

运行命令
-----------------

您应该将命令的名称作为第一个参数传递以运行该命令：

.. code-block:: console

    php spark migrate

某些命令接受附加参数，这些参数应该直接在命令之后用空格分隔提供：

.. code-block:: console

    php spark db:seed DevUserSeeder

对于 CodeIgniter 提供的所有命令，如果您没有提供所需的参数，系统将提示您提供运行所需的信息：

.. code-block:: console

    php spark make:controller

    Controller 类名：

抑制头部输出
-------------------------

运行命令时，会输出包含 CodeIgniter 版本和当前时间的头部信息：

.. code-block:: console

    php spark env

    CodeIgniter v4.3.5 Command Line Tool - Server Time: 2023-06-16 12:45:31 UTC+00:00

    Your environment is currently set as development.

您可以始终传递 ``--no-header`` 以抑制头部输出，这对于解析结果很有帮助：

.. code-block:: console

    php spark env --no-header

    Your environment is currently set as development.

调用命令
================

命令也可以从您自己的代码中运行。这通常在控制器中用于 cron 任务，但可以随时使用。您可以使用 ``command()`` 函数来实现。该函数始终可用。

.. literalinclude:: cli_commands/001.php

唯一的参数是字符串，即所调用的命令和任何参数。它的使用方式与从命令行调用完全相同。

当不从命令行运行时，所有运行的命令的输出都会被捕获。它会从命令中返回，以便您可以选择是否显示它。
