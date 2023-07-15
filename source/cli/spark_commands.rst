##############
Spark 命令
##############

CodeIgniter 提供了官方命令 **spark** 和内置命令。

.. contents::
    :local:
    :depth: 2

****************
运行命令
****************

通过 CLI 运行
===============

这些命令是从项目根目录的命令行运行的。
提供了命令文件 **spark** 用于运行任何 CLI 命令::

    > php spark

如果不指定命令直接调用,将显示一个简单的帮助页面,其中也提供了可用命令列表。

您应该将命令名作为第一个参数传递来运行该命令::

    > php spark migrate

某些命令需要附加参数,应在命令后直接提供这些参数,使用空格分隔::

    > php spark db:seed DevUserSeeder

您始终可以传递 ``--no-header`` 来隐藏标题输出,有助于解析结果::

    > php spark cache:clear --no-header

对于 CodeIgniter 提供的所有命令,如果您没有提供所需的参数,它会提示您它需要正确运行的信息::

    > php spark make::controller

    Controller class name:

调用命令
================

命令也可以在代码中调用。这通常在控制器的 cron 任务中完成,但可以在任何时候使用。您可以使用 ``command()`` 函数来实现。该函数一直可用。

.. literalinclude:: cli_commands/001.php

唯一的参数是一个字符串,即调用的命令及任何参数。这看起来与从命令行调用完全相同。

从命令行外运行时,命令的所有输出都会被捕获。它从命令返回,以便您可以选择显示或不显示。

******************
使用帮助命令
******************

spark help
==========

您可以使用 ``help`` 命令获取有关任何 CLI 命令的帮助::

    > php spark help db:seed

从 v4.3.0 开始,您也可以使用 ``--help`` 选项代替 ``help`` 命令::

    > php spark db:seed --help

spark list
==========

使用 ``list`` 命令获取可用命令列表及其描述,这些命令已按类别排序::

    > php spark list

您也可以使用 ``--simple`` 选项获取所有可用命令的原始列表,这些命令已按字母顺序排序::

    > php spark list --simple
