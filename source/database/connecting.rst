###########################
连接数据库
###########################

.. contents::
    :local:
    :depth: 2

连接数据库
========================

连接默认组
-------------------------------

你可以通过在任何需要的函数中添加此代码行来连接数据库,或者在类构造函数中添加此行以在该类中全局提供数据库。

.. literalinclude:: connecting/001.php
    :lines: 2-

如果上述函数的第一个参数不包含任何信息,则它将连接数据库配置文件中指定的默认组。对于大多数人来说,这是首选的使用方法。

为方便起见,还提供了一个纯包装器方法,代码如下:

.. literalinclude:: connecting/002.php
    :lines: 2-

可用参数
--------------------

**\\Config\\Database::connect($group = null, bool $getShared = true): BaseConnection**

#. ``$group``:数据库组名称,必须与配置类属性名称匹配的字符串。默认值为 ``Config\Database::$defaultGroup``。
#. ``$getShared``: true/false(布尔值)。是否返回共享连接(参见下面的连接多个数据库)。

连接特定组
----------------------------

此函数的第一个参数可以用来指定配置文件中的特定数据库组。示例:

要从配置文件中选择一个特定的组,可以这样做:

.. literalinclude:: connecting/003.php
    :lines: 2-

其中 ``group_name`` 是配置文件中连接组的名称。

连接到同一数据库的多个连接
-------------------------------------

默认情况下, ``connect()`` 方法每次都会返回数据库连接的同一实例。如果你需要与同一数据库建立一个单独的连接,请将 ``false`` 作为第二个参数发送:

.. literalinclude:: connecting/004.php
    :lines: 2-

连接多个数据库
================================

如果你需要同时连接多个数据库,可以这样做:

.. literalinclude:: connecting/005.php
    :lines: 2-

注意:请将 “group_one” 和 “group_two” 更改为你正在连接的特定组名称。

.. note:: 如果你只需要在同一连接上使用不同的数据库,则不需要创建单独的数据库配置。当需要时,你可以切换到不同的数据库,像这样:
    ``$db->setDatabase($database2_name);``

使用自定义设置连接
===============================

你可以传递一个数据库设置数组而不是组名称来获取使用自定义设置的连接。传递的数组必须与配置文件中定义组的格式相同:

.. literalinclude:: connecting/006.php
    :lines: 2-

重新连接/保持连接活动
===========================================

如果在执行一些繁重的 PHP 操作(处理图像等)时超过数据库服务器的空闲超时,则在发送进一步查询之前,应考虑通过使用 ``reconnect()`` 方法向服务器发出 ping,这可以优雅地保持连接活动或重新建立连接。

.. important:: 如果使用 MySQLi 数据库驱动程序, ``reconnect()`` 方法不会向服务器发出 ping,而是关闭连接然后再次连接。

.. literalinclude:: connecting/007.php
    :lines: 2-

手动关闭连接
===============================

虽然 CodeIgniter 会智能地关闭数据库连接,但你可以显式关闭连接。

.. literalinclude:: connecting/008.php
    :lines: 2-
