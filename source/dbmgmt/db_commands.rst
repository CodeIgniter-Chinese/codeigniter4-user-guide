#################
数据库命令
#################

CodeIgniter 提供了一些简单的数据库管理命令。

.. contents::
    :local:
    :depth: 2

*************************
显示表信息
*************************

列出数据库中的表
================================

db:table --show
---------------

要在喜欢的终端中直接列出数据库中的所有表，
可以使用 ``db:table --show`` 命令：

.. code-block:: console

    php spark db:table --show

使用此命令时假定数据库中存在表。
否则，CodeIgniter 会提示数据库中没有表。

.. _db-command-specify-the-dbgroup:

指定数据库组
==========================

db:table --dbgroup
------------------

.. versionadded:: 4.5.0

可以使用 ``--dbgroup`` 选项指定要使用的数据库组：

.. code-block:: console

    php spark db:table --show --dbgroup tests

检索一些记录
=====================

db:table
--------

当有一个名为 ``my_table`` 的表时，可以查看表的字段名和记录：

.. code-block:: console

    php spark db:table my_table

如果数据库中不存在 ``my_table`` 表，CodeIgniter 会显示可用表列表供选择。

也可以不使用表名而使用以下命令：

.. code-block:: console

    php spark db:table

在这种情况下，会要求输入表名。

还可以传递一些选项：

.. code-block:: console

    php spark db:table my_table --limit-rows 50 --limit-field-value 20 --desc

选项 ``--limit-rows 50`` 将行数限制为 50 行。

选项 ``--limit-field-value 20`` 将字段值的长度限制为 20 个字符，以防止终端中的表输出混乱。

选项 ``--desc`` 将排序方式设置为 "DESC"。

检索字段元数据
=======================

db:table --metadata
-------------------

当有一个名为 ``my_table`` 的表时，可以使用 ``--metadata`` 选项查看列类型、表的最大长度等元数据：

.. code-block:: console

    php spark db:table my_table --metadata

使用此命令时假定表存在。
否则，CodeIgniter 会显示表列表供选择。
也可以将此命令用作 ``db:table --metadata``。
