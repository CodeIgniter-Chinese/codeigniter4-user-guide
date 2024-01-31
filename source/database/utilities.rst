######################
数据库实用工具类
######################

数据库实用工具类包含了帮助你管理数据库的方法。

.. contents::
    :local:
    :depth: 2

******************************
初始化实用工具类
******************************

按照以下方式加载实用工具类：

.. literalinclude:: utilities/002.php
    :lines: 2-

你也可以将另一数据库组传递给 DB Utility 加载器，以防你要管理的数据库不是默认的：

.. literalinclude:: utilities/003.php
    :lines: 2-

在上述示例中，我们将数据库组名称作为第一参数传递了进去。

****************************
使用数据库实用工具
****************************

检索数据库名称列表
===============================

返回一个包含数据库名称的数组：

.. literalinclude:: utilities/004.php
    :lines: 2-

判断数据库是否存在
==================

有时候，我们需要知道特定的数据库是否存在。
返回一个布尔值 ``true``/``false``。使用示例：

.. literalinclude:: utilities/005.php
    :lines: 2-

.. note:: 将 ``database_name`` 替换为你正在查找的数据库名称。此方法区分大小写。

优化数据表
==========

允许你使用第一参数中特定的表名来优化一个表。根据成功或失败返回 ``true``/``false``：

.. literalinclude:: utilities/006.php
    :lines: 2-

.. note:: 并非所有的数据库平台都支持表优化。它主要用于 MySQL。

优化数据库
===========

允许你优化 DB 类当前连接的数据库。成功返回包含数据库状态消息的数组，失败返回 ``false``：

.. literalinclude:: utilities/008.php
    :lines: 2-

.. note:: 并非所有的数据库平台都支持数据库优化。它主要用于 MySQL。

将查询结果导出为 CSV 文件
==========================

允许你生成一个来自查询结果的 CSV 文件。方法的第一参数必须包含你的查询结果对象。示例：

.. literalinclude:: utilities/009.php
    :lines: 2-

第二、第三和第四参数分别允许你设置分隔符、换行和封闭字符。默认的分隔符是逗号，``"\n"`` 用作新行，双引号用作封闭符。示例：

.. literalinclude:: utilities/010.php
    :lines: 2-

.. important:: 这个方法不会为你写入 CSV 文件。它仅创建 CSV 布局。如果你需要写入文件，使用 :php:func:`write_file()` 辅助函数。

将查询结果导出为 XML 文档
==========================

通过此方法，你可以生成一个来自查询结果的 XML 文件。第一参数需要是一个查询结果对象，第二参数可能包含一个可选的配置参数数组。示例：

.. literalinclude:: utilities/001.php

当 ``mytable`` 有 ``id`` 和 ``name`` 列时，将得到以下 xml 结果::

    <root>
        <element>
            <id>1</id>
            <name>bar</name>
        </element>
    </root>

.. important:: 这个方法不会为你写入 XML 文件。它仅仅创建 XML 布局。如果你需要写入文件，使用 :php:func:`write_file()` 辅助函数。
