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

命令从项目根目录的命令行运行。
提供了一个名为 **spark** 的命令文件，用于运行任何 CLI 命令。

显示命令列表
------------------------

调用 **spark** 但不指定命令时，会显示一个简单的帮助页面，
其中还提供了可用命令及其描述的列表，按类别排序：

.. code-block:: console

    php spark

spark list
^^^^^^^^^^

``php spark`` 与 ``list`` 命令完全相同：

.. code-block:: console

    php spark list

你也可以使用 ``--simple`` 选项来获取按字母顺序排序的所有可用命令的原始列表：

.. code-block:: console

    php spark list --simple

获取帮助
------------

你可以使用 ``help`` 命令来获取任何 CLI 命令的帮助信息，如下所示：

.. code-block:: console

    php spark help db:seed

从 v4.3.0 开始，你也可以使用 ``--help`` 选项代替 ``help`` 命令：

.. code-block:: console

    php spark db:seed --help

运行命令
-----------------

你应该将命令名称作为第一个参数传递来运行该命令：

.. code-block:: console

    php spark migrate

一些命令需要额外的参数，这些参数应直接在命令后提供，以空格分隔：

.. code-block:: console

    php spark db:seed DevUserSeeder

对于 CodeIgniter 提供的所有命令，如果你没有提供所需的参数，系统会提示你输入运行命令所需的信息：

.. code-block:: console

    php spark make:controller

    Controller class name :

抑制头部输出
-------------------------

当你运行命令时，会输出包含 CodeIgniter 版本和当前时间的头部信息：

.. code-block:: console

    php spark env

    CodeIgniter v4.3.5 Command Line Tool - Server Time: 2023-06-16 12:45:31 UTC+00:00

    Your environment is currently set as development.

你始终可以传递 ``--no-header`` 来抑制头部输出，这在解析结果时很有用：

.. code-block:: console

    php spark env --no-header

    Your environment is currently set as development.

调用命令
================

你也可以在自己的代码中运行命令。这最常在控制器中用于定时任务（cronjob），
但也可以随时使用。你可以通过使用 ``command()`` 函数来实现。这个函数始终可用。

.. literalinclude:: cli_commands/001.php

唯一的参数是一个字符串，包含要调用的命令及其所有参数。其形式与你在命令行中调用时完全相同。

当命令不在命令行中运行时，命令的所有输出都会被捕获。这些输出会从命令中返回，
因此你可以选择是否显示它们。
