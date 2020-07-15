###########################
连接你的数据库
###########################

你可以在任意你需要的方法中添加以下代码来连接你的数据库，或在类的构造函数中添加这段代码让其在类里全局可用。

::

	$db = \Config\Database::connect();

如果上面的函数没有指定第一个参数，它将使用数据库配置文件中指定的默认配置组来连接数据库，对于大多数人而言，这是首选的方案。

有一个简便的、纯粹是封装上一段代码的方法，亦可以让你便捷的连接数据库::

    $db = db_connect();

可用的参数
--------------------

#. 数据库组名，一个必须与配置类的属性名匹配的字符串。默认值为 $config->defaultGroup；
#. TRUE/FALSE (boolean). 是否返回共享连接（参考下文的连接多个数据库）。

手动连接数据库
---------------------------------

这个函数的第一个参数是 **可选的** ，用来从你的配置文件中选取某个配置组（建立连接）。例如:

从配置文件中选择一个特定的配置组，你可以这样做::

	$db = \Config\Database::connect('group_name');

其中 group_name 是配置文件中配置组的名字。

用多个链接连同一个数据库
-------------------------------------

默认情况下， ``connect()``  方法每次返回数据库连接的同一实例。若你需要一个单独的连接到相同数据库，使用 ``false``  作为第二个参数::

	$db = \Config\Database::connect('group_name', false);


连接多个数据库
================================

如果你需要同时连接到多个不同的数据库，你可以这样做::

	$db1 = \Config\Database::connect('group_one');
	$db = \Config\Database::connect('group_two');

注意: 将 "group_one" 和 "group_two" 修改为你想要连接的配置组名称

.. 注解:: 如果只是在同一连接上使用不同的数据库，你不需要创建单独的数据库配置。当你需要时，可以切换到不同的数据库，例如:

	| $db->dbSelect($database2_name);

使用自定义配置连接数据库
===============================

你可以传入一个数据库配置数组参数替代配置组名称，以此获得一个自定义的数据库连接。数组的格式必须与数据库配置文件的配置组格式相同::

    $custom = [
		'DSN'      => '',
		'hostname' => 'localhost',
		'username' => '',
		'password' => '',
		'database' => '',
		'DBDriver' => 'MySQLi',
		'DBPrefix' => '',
		'pConnect' => false,
		'DBDebug'  => (ENVIRONMENT !== 'production'),
		'cacheOn'  => false,
		'cacheDir' => '',
		'charset'  => 'utf8',
		'DBCollat' => 'utf8_general_ci',
		'swapPre'  => '',
		'encrypt'  => false,
		'compress' => false,
		'strictOn' => false,
		'failover' => [],
		'port'     => 3306,
	];
    $db = \Config\Database::connect($custom);


重新连接/保持连接有效
===========================================

当你在处理一些重量级的 PHP 操作时（例如处理图像），若超过了数据库的超时值，你应该考虑在执行后续查询前先调用 reconnect() 方法向数据库发送 ping 命令，这样可以优雅的保持连接有效或重新建立连接。

.. 重要:: 若你使用 MySQLi 数据库驱动，reconnect() 方法并不能 ping 通服务器但它可以关闭连接然后再次连接。

::

	$db->reconnect();

手动关闭连接
===============================

虽然 CodeIgniter 可以智能的管理并自动关闭数据库连接，你仍可以显式关闭连接。

::

	$db->close();
