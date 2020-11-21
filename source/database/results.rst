########################
生成查询结果
########################

有几种方式生成查询结果:

.. contents::
    :local:
    :depth: 2

*************
结果数组
*************

**getResult()**

这个方法返回 **对象数组** 类型的查询结果，或在失败时返回 **一个空数组** 。
典型的用法是使用 foreach 循环，像这样::

    $query = $db->query("YOUR QUERY");

    foreach ($query->getResult() as $row)
    {
        echo $row->title;
        echo $row->name;
        echo $row->body;
    }

上面的方法是 ``getResultObject()`` 的别名。

如果你想返回一个二维数组，可以给第一个参数传字符串 'array' ::

    $query = $db->query("YOUR QUERY");

    foreach ($query->getResult('array') as $row)
    {
        echo $row['title'];
        echo $row['name'];
        echo $row['body'];
    }

上面的方法是 ``getResultArray()`` 的别名。

你也可以传字符串参数到 ``getResult()`` 方法，表示要为每个结果对象实例化的类

::

    $query = $db->query("SELECT * FROM users;");

    foreach ($query->getResult('User') as $user)
    {
        echo $user->name; // 获取属性
        echo $user->reverseName(); // 或访问 'User' 类定义的方法
    }

上面的方法是 ``getCustomResultObject()`` 的别名。

**getResultArray()**

这个方法返回一个纯数组的查询结果，查无结果时为空数组。
典型的用法是使用 foreach 循环，像这样::

    $query = $db->query("YOUR QUERY");

    foreach ($query->getResultArray() as $row)
    {
        echo $row['title'];
        echo $row['name'];
        echo $row['body'];
    }

***********
单行结果
***********

**getRow()**

这个方法返回一个单行结果，如果你的查询有多行结果，它仅返回第一条。
返回结果是一个 **对象** 。使用示例::

    $query = $db->query("YOUR QUERY");

    $row = $query->getRow();

    if (isset($row))
    {
        echo $row->title;
        echo $row->name;
        echo $row->body;
    }

如果你想返回指定行的结果，可以在第一个参数里提供这个数字::

	$row = $query->getRow(5);

你也可以传一个字符串到第二个参数，表示该结果实例化的对象类::

	$query = $db->query("SELECT * FROM users LIMIT 1;");
	$row = $query->getRow(0, 'User');

	echo $row->name; // 获取属性
	echo $row->reverse_name(); // 或访问 'User' 类定义的方法

**getRowArray()**

这个与上面的 ``row()`` 方法基本相同，区别是它返回的是一个数组。
示例::

    $query = $db->query("YOUR QUERY");

    $row = $query->getRowArray();

    if (isset($row))
    {
        echo $row['title'];
        echo $row['name'];
        echo $row['body'];
    }

如果你想返回指定行的结果，可以在第一个参数里提供这个数字::

	$row = $query->getRowArray(5);

另外，你可以用这些方法在结果集里做 前进/后退/首行/尾行 的游标操作:

	| **$row = $query->getFirstRow()**
	| **$row = $query->getLastRow()**
	| **$row = $query->getNextRow()**
	| **$row = $query->getPreviousRow()**

默认他们返回一个对象，除非第一个参数是字符串 "array" 才会返回数组:

	| **$row = $query->getFirstRow('array')**
	| **$row = $query->getLastRow('array')**
	| **$row = $query->getNextRow('array')**
	| **$row = $query->getPreviousRow('array')**

.. 注解:: 以上所有方法都会把整个查询结果载入内存（预加载）。
	请使用 ``getUnbufferedRow()`` 方法处理大型结果集。

**getUnbufferedRow()**

这个方法返回单个结果，不会像 ``row()`` 把整个结果预加载到内存里。
如果你的查询结果多于一个，它返回当前行并将内部数据指针向前移动。

::

    $query = $db->query("YOUR QUERY");

    while ($row = $query->getUnbufferedRow())
    {
        echo $row->title;
        echo $row->name;
        echo $row->body;
    }

你可以选择性的传参 'object' (默认) 或 'array' 来指定返回数据的类型::

	$query->getUnbufferedRow();         // 对象
	$query->getUnbufferedRow('object'); // 对象
	$query->getUnbufferedRow('array');  // 关联数组

*********************
自定义结果对象
*********************

你可以用一个自定义的类实例作为返回结果，代替原来的 ``stdClass`` 对象或数组，
``getResult()`` 和 ``getResultArray()`` 允许如此操作。
如果该类（文件）尚未加载到内存，自动加载器会尝试载入它。
对象的属性值会设置为数据库的返回数据，如果是非公开属性，
你需要提供一个 ``__set()`` 方法以允许他们被赋予值。

示例::

	class User
	{
		public $id;
		public $email;
		public $username;

		protected $last_login;

		public function lastLogin($format)
		{
			return $this->lastLogin->format($format);
		}

		public function __set($name, $value)
		{
			if ($name === 'lastLogin')
			{
				$this->lastLogin = DateTime::createFromFormat('U', $value);
			}
		}

		public function __get($name)
		{
			if (isset($this->$name))
			{
				return $this->$name;
			}
		}
	}

除了下面列出的两个方法之外，这些方法也可以指定类名
返回类实例的结果集: ``getFirstRow()``, ``getLastRow()``,
``getNextRow()`` 和 ``getPreviousRow()`` 。

**getCustomResultObject()**

以要求的类实例数组的形式返回整个结果集。
唯一的参数是要实例化的类的名称。

示例::

	$query = $db->query("YOUR QUERY");

	$rows = $query->getCustomResultObject('User');

	foreach ($rows as $row)
	{
		echo $row->id;
		echo $row->email;
		echo $row->last_login('Y-m-d');
	}

**getCustomRowObject()**

以要求的类实例形式返回单个结果，第一个参数是它在结果集里的序号，
第二个参数是要实例化的类的名称。

示例::

	$query = $db->query("YOUR QUERY");

	$row = $query->getCustomRowObject(0, 'User');

	if (isset($row))
	{
		echo $row->email;                 // 获取属性
		echo $row->last_login('Y-m-d');   // 或访问 'User' 类定义的方法
	}

你也可以用 ``getRow()`` 方法达到相同效果。

示例::

	$row = $query->getCustomRowObject(0, 'User');

*********************
结果处理辅助方法
*********************

**getFieldCount()**

返回查询结果的字段个数（列数），确保你是使用查询结果对象调用此方法::

	$query = $db->query('SELECT * FROM my_table');

	echo $query->getFieldCount();

**getFieldNames()**

返回查询结果的字段名（列名）的数组，确保你是使用查询结果对象调用此方法::

    $query = $db->query('SELECT * FROM my_table');

	echo $query->getFieldNames();

**freeResult()**

它会释放查询结果占用的内存并删除资源ID。通常 PHP 会在脚本结束时自动释放内存，
然而，如果你在某个脚本里执行了很多查询，你也许想处理完每个查询后即刻释放内存，
以此减少内存消耗。

举例::

	$query = $thisdb->query('SELECT title FROM my_table');

	foreach ($query->getResult() as $row)
	{
		echo $row->title;
	}

	$query->freeResult();  // $query 的结果对象不再可用

	$query2 = $db->query('SELECT name FROM some_table');

	$row = $query2->getRow();
	echo $row->name;
	$query2->freeResult(); // $query2 的结果对象不再可用

**dataSeek()**

该方法设置一个内部指针，用来获取下一个结果行，它仅和 ``getUnbufferedRow()`` 一起使用才有作用。

它接受一个正整数值，默认是0，返回 TRUE 表示成功，FALSE 表示失败。

::

	$query = $db->query('SELECT `field_name` FROM `table_name`');
	$query->dataSeek(5); // Skip the first 5 rows
	$row = $query->getUnbufferedRow();

.. 注解:: 不是所有数据库驱动支持这个特性，（不支持的）会返回 FALSE。
	最值得注意的是 - 你无法在 PDO 中使用它。

***************
类库参考
***************

.. php:class:: CodeIgniter\\Database\\BaseResult

	.. php:method:: getResult([$type = 'object'])

		:param	string	$type: 要求的结果类型 - array, object, 或 类名
		:returns:	包含查询到的行的数组
		:rtype:	array

		它是这几种方法的包装： ``getResultArray()``, ``getResultObject()``
		和 ``getCustomResultObject()`` 。

		用法: 详见 `结果数组`_.

	.. php:method:: getResultArray()

		:returns:	包含查询到的行的数组
		:rtype:	array

		返回查询结果行的数组，每行都是关联数组。

		用法: 详见 `结果数组`_.

	.. php:method:: getResultObject()

		:returns:	包含查询到的行的数组
		:rtype:	array

		返回查询结果行的数组，每行都是 ``stdClass`` 类的实例。

		用法: 详见 `结果数组`_.

	.. php:method:: getCustomResultObject($class_name)

		:param	string	$class_name: 结果行的类实例名
		:returns:	包含查询到的行的数组
		:rtype:	array

		返回查询结果行的数组，每行都是指定类的实例。

	.. php:method:: getRow([$n = 0[, $type = 'object']])

		:param	int	$n: 想要返回的结果行的序号
		:param	string	$type: 要求的结果类型 - array, object, 或 类名
		:returns:	要求的行数据，不存在时返回 NULL
		:rtype:	mixed

		它是这几种方法的包装： ``getRowArray()``, ``getRowObject()`` 和
		``getCustomRowObject()`` 。

		用法: 详见 `单行结果`_.

	.. php:method:: getUnbufferedRow([$type = 'object'])

		:param	string	$type: 要求的结果类型 - array, object, 或 类名
		:returns:	结果集的下一行，不存在时返回 NULL
		:rtype:	mixed

		按要求的格式返回结果集的下一行。

		用法: 详见 `单行结果`_.

	.. php:method:: getRowArray([$n = 0])

		:param	int	$n: 想要返回的结果行的序号
		:returns:	要求的行数据，不存在时返回 NULL
		:rtype:	array

		返回结果行，格式为关联数组。

		用法: 详见 `单行结果`_.

	.. php:method:: getRowObject([$n = 0])

		:param	int	$n: 想要返回的结果行的序号
                :returns:	要求的行数据，不存在时返回 NULL
		:rtype:	stdClass

		返回结果行，格式为 ``stdClass`` 的类实例。

		用法: 详见 `单行结果`_.

	.. php:method:: getCustomRowObject($n, $type)

		:param	int	$n: 想要返回的结果行的序号
		:param	string	$class_name: 结果行的类实例名
		:returns:	要求的行数据，不存在时返回 NULL
		:rtype:	$type

		返回结果行，格式为要求的的类实例。

	.. php:method:: dataSeek([$n = 0])

		:param	int	$n: 即将返回的结果行的序号
		:returns:	TRUE 表示成功，FALSE 表示失败
		:rtype:	bool

		移动结果集的内部指针到指定位置。

		用法: 详见 `结果处理辅助方法`_.

	.. php:method:: setRow($key[, $value = NULL])

		:param	mixed	$key: 列名或键值数组
		:param	mixed	$value: 分配给列的值，$key 是单个字段名
		:rtype:	void

		为特定列分配值。

	.. php:method:: getNextRow([$type = 'object'])

		:param	string	$type: 要求的结果类型 - array, object, 或 类名
		:returns:	结果集的下一行，不存在时返回 NULL
		:rtype:	mixed

		返回结果集的下一行。

	.. php:method:: getPreviousRow([$type = 'object'])

		:param	string	$type: 要求的结果类型 - array, object, 或 类名
		:returns:	结果集的上一行，不存在时返回 NULL
		:rtype:	mixed

		返回结果集的上一行。

	.. php:method:: getFirstRow([$type = 'object'])

		:param	string	$type: 要求的结果类型 - array, object, 或 类名
		:returns:	结果集的第一行，不存在时返回 NULL
		:rtype:	mixed

		返回结果集的第一行。

	.. php:method:: getLastRow([$type = 'object'])

		:param	string	$type: 要求的结果类型 - array, object, 或 类名
		:returns:	结果集的最后一行，不存在时返回 NULL
		:rtype:	mixed

		返回结果集的最后一行。

	.. php:method:: getFieldCount()

		:returns:	结果集中字段的个数
		:rtype:	int

		返回结果集中字段的个数。

		用法: 详见 `结果处理辅助函数`_.

    .. php:method:: getFieldNames()

		:returns:	列名称的数组
		:rtype:	array

		返回一个包含结果集中字段名的数组。

	.. php:method:: getFieldData()

		:returns:	包含字段元数据的数组
		:rtype:	array

		生成一个包含字段元数据的 ``stdClass`` 对象的数组。

	.. php:method:: freeResult()

		:rtype:	void

		释放一个结果集。

		用法: 详见 `结果处理辅助函数`_.
