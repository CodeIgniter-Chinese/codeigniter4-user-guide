#####################
自定义函数调用
#####################

$db->callFunction();
============================

该函数可以用平台无关的形来调用CodeIgniter中没有原生包含的PHP数据库方法。
举例来说，假如你想调用 ``mysql_get_client_info``  函数，但是这一方法CodeIgniter **并没有** 原生支持。你可以这样做::


	$db->callFunction('get_client_info');

第一个参数是函数名（必填），且 **不应该** 带有 ``mysql\_`` 的前缀。
该函数会根据当前数据库自动附加前缀。这个机制可确保在不同数据库平台运行相同的函数。
当然，各数据库的函数调用并不完全一致，因此，就可移植性而言，此函数的实用性有限。

调用这个函数所需的任何参数可添加到第二、第三个参数，以此类推::

	$db->callFunction('some_function', $param1, $param2, etc..);

这里，你经常要提供数据库连接ID或是查询结果ID作为参数，当前DB连接ID可以用该方法获得::

	$db->connID;

查询结果ID可以用QUERY结果对象来获得，例如::

	$query = $db->query("SOME QUERY");

	$query->resultID;