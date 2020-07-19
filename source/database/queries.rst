#########
执行查询
#########

.. contents::
    :local:
    :depth: 2

************
基础查询
************

执行常规查询
===============

使用 **query** 方法提交一个查询::

	$db->query('YOUR QUERY HERE');

执行 "读取" 类型查询时，query() 方法返回一个数据库查询结果 **对象** ，
如何使用参考 :doc:`显示查询结果 <results>` ；执行 "写入" 类查询时，
只返回 TRUE 或 FALSE ，表示执行成功或失败。检索数据时，你通常需要自行
编写查询语句，例如::

	$query = $db->query('YOUR QUERY HERE');

执行简单查询
==================

**simpleQuery** 方法是 $db->query() 的简化版本。它不会返回查询结果，
不记录查询耗时，不会绑定变量，也不保存查询语句（用于调试）。它只是简单的
让你执行一个查询语句，可能大多数用户鲜有使用。

它只返回 "execute" 方法执行的返回值，无关数据库类型。
典型的返回值是 TRUE/FALSE ，当执行类型是写入型时，它表示写操作的成功或失败（
插入、删除或修改，实际就如此使用）；执行读取类型时，表示能否成功获取查询结果资源/对象。

::

	if ($db->simpleQuery('YOUR QUERY'))
	{
		echo "Success!";
	}
	else
	{
		echo "Query failed!";
	}

.. note:: PostgreSQL的 ``pg_exec()`` 方法 (举例) 执行成功时
	总是返回一个资源值，即使执行写入型查询也是如此。
	所以当你判断布尔值时要切记此点。

***************************************
手动指定数据表前缀
***************************************

当你配置了数据库的表前缀，执行原生SQL查询等类似操作，应当给数据表增加前缀，
你可以使用如下操作::

	$db->prefixTable('tablename'); // 输出 prefix_tablename

出于某些原因，你想以编程的方式修改表前缀，且不想创建新数据库连接时，可以这样做::

	$db->setPrefix('newprefix');
	$db->prefixTable('tablename'); // 输出 newprefix_tablename

你可以用此方法随时随地获取当前的表前缀::
	
	$DBPrefix = $db->getPrefix();

**********************
保护标识符
**********************

许多数据库建议保护表名和字段名 - 比如 MySQL 使用反引号。
**查询构造器会自动保护它们**, 但如果你需要手动保护标识符时，可以这么做::

	$db->protectIdentifiers('table_name');

.. important:: 尽管查询构造器会尽可能且适当的引用你所需的字段名和表名，
	但请注意它不适用于恶意用户输入，勿将其用于未处理的用户数据。

当你在数据库配置文件里配有表前缀，这个方法还能给表加上前缀，
开启这个功能请在第二个参数填写 TRUE（布尔值）::

	$db->protectIdentifiers('table_name', TRUE);

****************
查询转义
****************

执行数据库查询前做数据转义是又好又安全的实践，CodeIgniter 有三种方法帮到你:

#. **$db->escape()** 这个方法会判断数据类型，对字符串数据做转义，
   它也会自动给数据加单引号，你无需额外处理:
   ::

	$sql = "INSERT INTO table (title) VALUES(".$db->escape($title).")";

#. **$db->escapeString()** 这个方法对传入数据做强制转义，且无关类型，
   多数时候你会用上面的方法而非这个。此方法使用举例:
   ::

	$sql = "INSERT INTO table (title) VALUES('".$db->escapeString($title)."')";

#. **$db->escapeLikeString()** 这个方法用于 LIKE 条件字符串转义，
    以确保 LIKE 的通配符 ('%', '\_') 也能正确的转义。

::

        $search = '20% raise';
        $sql = "SELECT id FROM table WHERE column LIKE '%" .
        $db->escapeLikeString($search)."%' ESCAPE '!'";

.. important::  ``escapeLikeString()`` 方法使用 '!' (感叹号)
	转义 *LIKE* 条件中的特殊字符，因为这个方法只转义引号里的字符串，
	它不能自动添加 ``ESCAPE '!'`` 条件，因此你必须手动添加。

**************
查询绑定
**************

绑定可以让你用简单的查询语法，让系统将查询语句合在一起，考虑下这个例子::

	$sql = "SELECT * FROM some_table WHERE id = ? AND status = ? AND author = ?";
	$db->query($sql, [3, 'live', 'Rick']);

查询语句的问号会被方法第二个参数的数组顺次替换。

使用IN条件时，绑定用多维数组搞定集合::

	$sql = "SELECT * FROM some_table WHERE id IN ? AND status = ? AND author = ?";
	$db->query($sql, [[3, 6], 'live', 'Rick']);

转化后的语句是::

	SELECT * FROM some_table WHERE id IN (3,6) AND status = 'live' AND author = 'Rick'

使用绑定的第二个好处是，它会自动转义输入值，生成安全的查询语句。
你无需记住要手动转义数据这件事 - 引擎会自动帮你完成。

命名绑定
==============

你可以用命名绑定，而不用问号标记绑定值的位置，从而允许在查询中使用键名匹配占位符::

        $sql = "SELECT * FROM some_table WHERE id = :id: AND status = :status: AND author = :name:";
        $db->query($sql, [
                'id'     => 3,
                'status' => 'live',
                'name'   => 'Rick'
        ]);

.. note:: 查询语句中的每个键名前后【必须】加英文冒号。

***************
错误处理
***************

**$db->error();**

如果你需要获取最近一次发生的数据库报错，error() 方法会返回一个数组，
包含错误号和错误信息，来看下用例::

	if ( ! $db->simpleQuery('SELECT `example_field` FROM `example_table`'))
	{
		$error = $db->error(); // Has keys 'code' and 'message'
	}

****************
预编译查询
****************

大部分数据库引擎支持某种形式的预编译语句，使你仅做一次预编译，然后在新数据集上多次查询。它消除了 SQL 注入的可能性，因为数据是以另一种形式传给数据库而非查询语句。
当你需要多次执行相同查询时，它也相当快速。然而，若你想应用于所有查询，这会极大影响性能，因为它通常要访问数据库两次。
由于查询构造器和数据库连接已经处理了转义数据，所以，安全方面已经为你解决了，但有时候，你也需要通过预编译语句或预编译查询来优化查询。

编译查询语句
===================

使用 ``prepare()`` 方法可轻松完成编译，它有一个参数，是函数闭包，返回一个查询对象。
查询对象由任一 "最终" 类型的查询自动生成，包括 **insert** , **update** , **delete** ,  **replace** 和 **get** 。使用查询构造器执行查询可以最轻松地处理此问题。
查询实际没有执行，传入的值不重要也不会被处理，仅做占位使用。
这样会返回一个预编译查询对象::

    $pQuery = $db->prepare(function($db)
    {
        return $db->table('user')
                   ->insert([
                        'name'    => 'x',
                        'email'   => 'y',
                        'country' => 'US'
                   ]);
    });

如果你不想使用查询构造器，你可以手动创建查询对象，用问号做占位符::

    use CodeIgniter\Database\Query;

    $pQuery = $db->prepare(function($db)
    {
        $sql = "INSERT INTO user (name, email, country) VALUES (?, ?, ?)";

        return (new Query($db))->setQuery($sql);
    });

如果数据库要求在预编译阶段提供选项数组，可以将数组放到第二个参数::

    use CodeIgniter\Database\Query;

    $pQuery = $db->prepare(function($db)
    {
        $sql = "INSERT INTO user (name, email, country) VALUES (?, ?, ?)";

        return (new Query($db))->setQuery($sql);
    }, $options);

执行预编译查询
===================

一旦你有了一个预编译查询，你可以使用 ``execute()`` 方法真正的执行查询。
你可以传递多个你需要的查询参数，参数的个数必须与占位符个数相同，参数的顺序也要与原始占位符保持一致::

    // 编译查询语句
    $pQuery = $db->prepare(function($db)
    {
        return $db->table('user')
                   ->insert([
                        'name'    => 'x',
                        'email'   => 'y',
                        'country' => 'US'
                   ]);
    });

    // 准备数据
    $name    = 'John Doe';
    $email   = 'j.doe@example.com';
    $country = 'US';

    // 执行查询
    $results = $pQuery->execute($name, $email, $country);

这会返回标准的 :doc:`结果集 </database/results>`.

其他方法
=============

除了上述两个主要方法，预编译查询还有以下方法可用:

**close()**

虽然 PHP 在（自动）关闭所有打开的查询资源时做的非常好，但手动关闭执行完的预编译查询同样也是好的主意::

    $pQuery->close();

**getQueryString()**

返回预编译查询的字符串。

**hasError()**

返回布尔值 true/false ，表示调用最近一次是否有执行错误。

**getErrorCode()**
**getErrorMessage()**

如果有报错，可以用这两个方法获取错误号和错误信息。

**************************
使用查询对象
**************************

在内部，所有查询的处理和存储都在 \CodeIgniter\Database\Query 的实例中进行。
这个类负责绑定参数、也做预编译查询、还能保存查询时的性能数据。

**getLastQuery()**

当你需要获取最近一次的查询对象，请使用 getLastQuery() 方法::

	$query = $db->getLastQuery();
	echo (string)$query;

查询类
===============

每个查询对象都保存了此次查询的一些信息，它有部分被时间线功能使用，
但你也可以使用（译者注：此处时间线指数据库执行SQL过程，记录它们方便调试和优化性能）。

**getQuery()**

返回各种编译构造之后的最终查询语句，也就是发送到数据库执行的语句::

	$sql = $query->getQuery();

将查询对象做字符串转换也能获得相同的值::

	$sql = (string)$query;

**getOriginalQuery()**

返回初始传入对象里的 SQL 语句，没有任何绑定或前缀修饰等等::

	$sql = $query->getOriginalQuery();

**hasError()**

如果执行时有任何错误，这个方法将返回 true::

	if ($query->hasError())
	{
		echo 'Code: '. $query->getErrorCode();
		echo 'Error: '. $query->getErrorMessage();
	}

**isWriteType()**

如果当前查询是写入型 (例如 INSERT, UPDATE, DELETE, 等)，此方法返回 true::

	if ($query->isWriteType())
	{
		... do something
	}

**swapPrefix()**

替换最终执行的 SQL 里的表前缀，第一个参数是原始你想替换的前缀，
第二个参数是替换之后你想要的前缀::

	$sql = $query->swapPrefix('ci3_', 'ci4_');

**getStartTime()**

获取查询执行时间，以秒为单位，精确到毫秒级::

	$microtime = $query->getStartTime();

**getDuration()**

返回执行查询的时长（秒），浮点数，精确到毫秒::

	$microtime = $query->getDuration();
