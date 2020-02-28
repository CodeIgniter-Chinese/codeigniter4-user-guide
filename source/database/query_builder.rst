###################
查询构造器类
###################

CodeIgniter 提供了查询构造器类， 查询构造器允许你使用较少的代码来在数据库中获取、新增
或更新数据。 有时只需要一两行代码就能完成数据库操作。 CodeIgniter并不需要为每个数据表
提供一个类， 而是使用了一种更简单的接口。

除了简单， 使用查询构造器的另一个好处是可以让你创建数据库独立的应用程序， 这是因为查询语句
是由每个独立的数据库适配器生成的。另外，由于系统会自动对数据进行转义，所以它还能提供更安全
的查询。

.. contents::
    :local:
    :depth: 2

*************************
加载查询构造器
*************************

查询构造器通过 ``table()`` 数据库连接上的方法加载。 ``FROM`` 将为你设置查询部分并
返回查询构造类的新实例::

    $db      = \Config\Database::connect();
    $builder = $db->table('users');

查询构造器仅在你专门请求类时才加载到内存中，因此默认情况下不使用任何资源。

**************
查询数据
**************

下面的方法用来构建 SQL **SELECT** 语句。

**$builder->get()**

执行选择查询并返回查询结果，可以得到一个表的所有数据::

    $builder = $db->table('mytable');
    $query   = $builder->get();  // Produces: SELECT * FROM mytable

第一个和第二个参数用于设置 limit 和 offset 子句::

	$query = $builder->get(10, 20);

	// Executes: SELECT * FROM mytable LIMIT 20, 10
	// (在 MySQL 的情况。其他数据库的语法略有不同)

你应该已经注意到了， 上面的方法的结果都赋值给了一个 $query 变量， 通过这个变量， 我们
可以得到查询的结果::

	$query = $builder->get();

	foreach ($query->getResult() as $row)
	{
		echo $row->title;
	}

请访问: doc:`result functions <results>` 页面获得完整的结果关于结果生成的讨论.

**$builder->getCompiledSelect()**

该方法和 **$builder->get()** 方法一样编译选择查询并返回查询的 SQL 语句，
但是， 该方法并不执行它。 此方法只是将SQL查询作为字符串返回。

例如::

	$sql = $builder->getCompiledSelect();
	echo $sql;

	// Prints string: SELECT * FROM mytable

第一个参数使您能够设置查询生成器是否查询
将重置(默认情况下将重置，就像使用 `$builder->get()` 时一样)::

	echo $builder->limit(10,20)->getCompiledSelect(false);

	// Prints string: SELECT * FROM mytable LIMIT 20, 10
	// (在 MySQL 的情况。其他数据库的语法略有不同)

	echo $builder->select('title, content, date')->getCompiledSelect();

	// Prints string: SELECT title, content, date FROM mytable LIMIT 20, 10

上面的Executes中，最值得注意的是，第二个查询并没有用到 **$builder->from()** 方法， 
也没有为查询指定表名参数。 这是因为查询并没有使用 **$builder->get()** 方法执行， 
它会重置值或使用 **$builder->resetQuery()** 方法直接重置。

**$builder->getWhere()**

与 ``get()`` 函数相同，只是它允许您添加一个
在第一个参数中使用 "where" 子句，而不是使用 db->where()
功能::

	$query = $builder->getWhere(['id' => $id], $limit, $offset);

Please read the about the where function below for more information.

**$builder->select()**

允许您编写查询的 SELECT 部分::

	$builder->select('title, content, date');
	$query = $builder->get();

	// Executes: SELECT title, content, date FROM mytable

.. note:: 如果要从表中选择全部 (\*)， 则不需要这样做使用这个函数。 当省略时，CodeIgniter 假定您希望这样做选择所有字段并自动添加 'SELECT \*'。

``$builder->select()`` 方法的第二个参数可选，如果设置
为 FALSE，CodeIgniter 将不保护你的表名和字段名，这在当
你编写复合查询语句时很有用，不会破坏你编写的语句。

::

	$builder->select('(SELECT SUM(payments.amount) FROM payments WHERE payments.invoice_id=4) AS amount_paid', FALSE);
	$query = $builder->get();

**$builder->selectMax()**

该方法用于编写查询语句中的 ``SELECT MAX(field)`` 部分，你
可以使用第二个参数重命名结果字段。

::

	$builder->selectMax('age');
	$query = $builder->get();  // Produces: SELECT MAX(age) as age FROM mytable

	$builder->selectMax('age', 'member_age');
	$query = $builder->get(); // Produces: SELECT MAX(age) as member_age FROM mytable

**$builder->selectMin()**

该方法用于编写查询语句中的 "SELECT MIN(field)" 部分，和 
selectMax() 方法一样， 你可以使用第二个参数（可选）重命名结果字段。

::

	$builder->selectMin('age');
	$query = $builder->get(); // Produces: SELECT MIN(age) as age FROM mytable

**$builder->selectAvg()**

该方法用于编写查询语句中的 "SELECT AVG(field)" 部分，和 
selectMax() 方法一样， 你可以使用第二个参数（可选）重命名结果字段。

::

	$builder->selectAvg('age');
	$query = $builder->get(); // Produces: SELECT AVG(age) as age FROM mytable

**$builder->selectSum()**

该方法用于编写查询语句中的 "SELECT SUM(field)" 部分，和 
selectMax() 方法一样， 你可以使用第二个参数重命名结果字段。

::

	$builder->selectSum('age');
	$query = $builder->get(); // Produces: SELECT SUM(age) as age FROM mytable

**$builder->from()**

该方法用于编写查询语句中的 FROM 子句::

	$builder->select('title, content, date');
	$builder->from('mytable');
	$query = $builder->get();  // Produces: SELECT title, content, date FROM mytable

.. note:: 正如前面所说，查询中的 FROM 部分可以在方法 $db->table() 中指定。 对 from() 的其他调用将向查询的FROM部分添加更多表。

**$builder->join()**

该方法用于编写查询语句中的 JOIN 子句::

    $builder->db->table('blog');
    $builder->select('*');
    $builder->join('comments', 'comments.id = blogs.id');
    $query = $builder->get();

    // Produces:
    // SELECT * FROM blogs JOIN comments ON comments.id = blogs.id

如果你的查询中有多个连接，你可以多次调用这个方法.

你可以传入第三个参数指定连接的类型， 有这样几种选择： left， right， 
outer， inner， left outer 和 right outer 。

::

	$builder->join('comments', 'comments.id = blogs.id', 'left');
	// Produces: LEFT JOIN comments ON comments.id = blogs.id

*************************
查找特定数据
*************************

**$builder->where()**

该方法提供了4中方式让你编写查询语句中的 **WHERE** 子句:

.. note:: 所有的数据将会自动转义，生成安全的查询语句。

#. **简单的 key/value 方式:**

	::

		$builder->where('name', $name); // Produces: WHERE name = 'Joe'

	注意自动为你加上了等号。

	如果你多次调用该方法，那么多个 WHERE 条件将会使用 AND 连接起来:

	::

		$builder->where('name', $name);
		$builder->where('title', $title);
		$builder->where('status', $status);
		// WHERE name = 'Joe' AND title = 'boss' AND status = 'active'

#. **自定义 key/value 方式:**

	为了控制比较，你可以在第一个参数中包含一个比较运算符:

	::

		$builder->where('name !=', $name);
		$builder->where('id <', $id); // Produces: WHERE name != 'Joe' AND id < 45

#. **关联数组方式:**

	::

		$array = ['name' => $name, 'title' => $title, 'status' => $status];
		$builder->where($array);
		// Produces: WHERE name = 'Joe' AND title = 'boss' AND status = 'active'

	你也可以在这个方法里包含你自己的比较运算符:

	::

		$array = ['name !=' => $name, 'id <' => $id, 'date >' => $date];
		$builder->where($array);

#. **自定义字符串:**
	你可以完全手动编写子句::

		$where = "name='Joe' AND status='boss' OR status='active'";
		$builder->where($where);

``$builder->where()`` 方法有一个可选的第三个参数，如果设置为 FALSE，CodeIgniter 
将不保护你的表名和字段名。

::

	$builder->where('MATCH (field) AGAINST ("value")', NULL, FALSE);

**$builder->orWhere()**

这个方法和上面的方法一样，只是多个条件之间使用 OR 进行连接::

	$builder->where('name !=', $name);
	$builder->orWhere('id >', $id);  // Produces: WHERE name != 'Joe' OR id > 50

**$builder->whereIn()**

该方法用于生成 WHERE IN('item', 'item') 子句，多个子句之间使用 AND 连接

::

	$names = array('Frank', 'Todd', 'James');
	$builder->whereIn('username', $names);
	// Produces: WHERE username IN ('Frank', 'Todd', 'James')

**$builder->orWhereIn()**

该方法用于生成 WHERE IN('item', 'item') 子句，多个子句之间使用 OR 连接

::

	$names = array('Frank', 'Todd', 'James');
	$builder->orWhereIn('username', $names);
	// Produces: OR username IN ('Frank', 'Todd', 'James')

**$builder->whereNotIn()**

该方法用于生成 WHERE NOT IN('item', 'item') 子句，多个子句之间使用 AND 连接

::

	$names = array('Frank', 'Todd', 'James');
	$builder->whereNotIn('username', $names);
	// Produces: WHERE username NOT IN ('Frank', 'Todd', 'James')

**$builder->orWhereNotIn()**

该方法用于生成 WHERE NOT IN('item', 'item') 子句，多个子句之间使用 OR 连接

::

	$names = array('Frank', 'Todd', 'James');
	$builder->orWhereNotIn('username', $names);
	// Produces: OR username NOT IN ('Frank', 'Todd', 'James')

************************
查找相似的数据
************************

**$builder->like()**

这个方法使您能够生成类似 **LIKE** 子句，在进行搜索时非常有用。

.. note:: 所有数据将会自动被转义。

.. note:: ``like*`` 通过将第五个参数传递给方法，可以强制所有方法变体
	执行不区分大小写的搜索 ``true``。 这将使用特定于平台的功能，否则将强制值
	为小写，即 ``WHERE LOWER(column) LIKE '%search%'``。这可能需要制作
	索引 ``LOWER(column)`` 而不是 ``column`` 有效。

#. **简单 key/value 方式:**

	::

		$builder->like('title', 'match');
		// Produces: WHERE `title` LIKE '%match%' ESCAPE '!'

	如果你多次调用该方法，那么多个 WHERE 条件将会使用 AND 连接起来::

		$builder->like('title', 'match');
		$builder->like('body', 'match');
		// WHERE `title` LIKE '%match%' ESCAPE '!' AND  `body` LIKE '%match% ESCAPE '!'

	可以传入第三个可选的参数来控制 LIKE 通配符（%）的位置，可用选项有：
	'before'，'after' 和 'both' (默认为 'both')。

	::

		$builder->like('title', 'match', 'before');	// Produces: WHERE `title` LIKE '%match' ESCAPE '!'
		$builder->like('title', 'match', 'after');	// Produces: WHERE `title` LIKE 'match%' ESCAPE '!'
		$builder->like('title', 'match', 'both');	// Produces: WHERE `title` LIKE '%match%' ESCAPE '!'

#. **关联数组方式:**

	::

		$array = ['title' => $match, 'page1' => $match, 'page2' => $match];
		$builder->like($array);
		// WHERE `title` LIKE '%match%' ESCAPE '!' AND  `page1` LIKE '%match%' ESCAPE '!' AND  `page2` LIKE '%match%' ESCAPE '!'

**$builder->orLike()**

这个方法和上面的方法一样，只是多个 WHERE 条件之间使用 OR 进行连接::

	$builder->like('title', 'match'); $builder->orLike('body', $match);
	// WHERE `title` LIKE '%match%' ESCAPE '!' OR  `body` LIKE '%match%' ESCAPE '!'

**$builder->notLike()**

这个方法和 ``like()`` 方法一样，只是生成 
NOT LIKE 子句::

	$builder->notLike('title', 'match');	// WHERE `title` NOT LIKE '%match% ESCAPE '!'

**$builder->orNotLike()**

这个方法和 ``notLike()``，方法一样，只是多个条件之间使用 OR 进行连接::

	$builder->like('title', 'match');
	$builder->orNotLike('body', 'match');
	// WHERE `title` LIKE '%match% OR  `body` NOT LIKE '%match%' ESCAPE '!'

**$builder->groupBy()**

该方法用于生成 GROUP BY 子句::

	$builder->groupBy("title"); // Produces: GROUP BY title

你也可以通过一个数组传入多个值::

	$builder->groupBy(array("title", "date"));  // Produces: GROUP BY title, date

**$builder->distinct()**

该方法用于向查询中添加 "DISTINCT" 关键字

::

	$builder->distinct();
	$builder->get(); // Produces: SELECT DISTINCT * FROM mytable

**$builder->having()**

该方法用于生成 HAVING 子句， 有下面两种不同的语法. 有两个
可能的语法， 1 个或 2 个参数::

	$builder->having('user_id = 45');  // Produces: HAVING user_id = 45
	$builder->having('user_id',  45);  // Produces: HAVING user_id = 45

您还可以传递一个包含多个值的数组::

	$builder->having(['title =' => 'My Title', 'id <' => $id]);
	// Produces: HAVING title = 'My Title', id < 45

如果您正在使用 CodeIgniter 为其转义查询的数据库，那么您
是否可以通过传递可选的第三个参数来防止转义内容
设置为 FALSE .
.

::

	$builder->having('user_id',  45);  // Produces: HAVING `user_id` = 45 in some databases such as MySQL
	$builder->having('user_id',  45, FALSE);  // Produces: HAVING user_id = 45

**$builder->orHaving()**

该方法和 having() 方法一样，只是多个条件之间使用 "OR" 进行连接。

****************
排序
****************

**$builder->orderBy()**

该方法用于生成 ORDER BY 子句。

第一个参数包含需要排序的列的名称。

第一个参数为你想要排序的字段名，第二个参数用于设置排序的方向， 可选项有： **ASC**，**DESC**和**RANDOM**。

::

	$builder->orderBy('title', 'DESC');
	// Produces: ORDER BY `title` DESC

第一个参数也可以是你自己的排序字符串::

	$builder->orderBy('title DESC, name ASC');
	// Produces: ORDER BY `title` DESC, `name` ASC

如果需要根据多个字段进行排序，可以多次调用该方法。

::

	$builder->orderBy('title', 'DESC');
	$builder->orderBy('name', 'ASC');
	// Produces: ORDER BY `title` DESC, `name` ASC

如果你选择了 **RANDOM**， 第一个参数会被忽略， 但是你可以传入一个数字值， 作为随机数的种子。

::

	$builder->orderBy('title', 'RANDOM');
	// Produces: ORDER BY RAND()

	$builder->orderBy(42, 'RANDOM');
	// Produces: ORDER BY RAND(42)

.. note:: Oracle 暂时还不支持随机排序，会默认使用ASC。

****************************
分页与计数
****************************

**$builder->limit()**

该方法用于限制你的查询返回结果的数量::

	$builder->limit(10);  // Produces: LIMIT 10

第二个参数可以用来设置偏移.

::

	$builder->limit(10, 20);  // Produces: LIMIT 20, 10 (在 MySQL。 其他数据库的语法略有不同）

**$builder->countAllResults()**

该方法用于获取特定查询返回结果的数量，也可以使用查询构造器的这些方法：
``where()``, ``orWhere()``, ``like()``, ``orLike()`` 等等。例如::

	echo $builder->countAllResults('my_table');  // 生成一个整数，比如 25
	$builder->like('title', 'match');
	$builder->from('my_table');
	echo $builder->countAllResults(); // 生成一个整数，比如 17

但是， 这个方法会重置你在 ``select()``。 方法里设置的所有值，如果你希望
保留它们，可以将第二个参数设置为 FALSE::

	echo $builder->countAllResults('my_table', FALSE);

**$builder->countAll()**

该方法用于获取某个表的总行数，第一个参数为表名。例如::

	echo $builder->countAll('my_table');  // Produces an integer, like 25

**************
查询分组
**************

查询分组可以让你生成用括号括起来的一组 WHERE 条件，这能创造出非常复杂的 WHERE 子句， 支持嵌套的条件组。 
例如::

	$builder->select('*')->from('my_table')
		->groupStart()
			->where('a', 'a')
			->orGroupStart()
				->where('b', 'b')
				->where('c', 'c')
			->groupEnd()
		->groupEnd()
		->where('d', 'd')
	->get();

	// 生成:
	// SELECT * FROM (`my_table`) WHERE ( `a` = 'a' OR ( `b` = 'b' AND `c` = 'c' ) ) AND `d` = 'd'

.. note:: 条件组必须要配对，确保每个 groupStart() 方法都有一个 groupEnd() 方法与之配对。

**$builder->groupStart()**

开始一个新的条件组，为查询中的 WHERE 条件添加一个左括号。

**$builder->orGroupStart()**

开始一个新的条件组，为查询中的 WHERE 条件添加一个左括号，并在前面加上 "OR" 。

**$builder->notGroupStart()**

开始一个新的条件组，为查询中的 WHERE 条件添加一个左括号，并在前面加上 "NOT" 。

**$builder->orNotGroupStart()**

开始一个新的条件组，为查询中的 WHERE 条件添加一个左括号，并在前面加上 "OR NOT" 。

**$builder->groupEnd()**

结束当前的条件组，为查询中的 WHERE 条件添加一个右括号。

**************
插入数据
**************

**$builder->insert()**

该方法根据你提供的数据生成一条 INSERT 语句并执行，它的参数是一个**数组** 或一个**对象**，
下面是使用数组的例子::

	$data = array(
		'title' => 'My title',
		'name'  => 'My Name',
		'date'  => 'My date'
	);

	$builder->insert($data);
	// Produces: INSERT INTO mytable (title, name, date) VALUES ('My title', 'My name', 'My date')

第一个参数为要插入的数据，是个关联数组。

下面是使用对象的例子::

	/*
	class Myclass {
		public $title   = 'My Title';
		public $content = 'My Content';
		public $date    = 'My Date';
	}
	*/

	$object = new Myclass;
	$builder->insert($object);
	// Produces: INSERT INTO mytable (title, content, date) VALUES ('My Title', 'My Content', 'My Date')

第一个参数为要插入的数据，是个对象。

.. note:: 所有数据会被自动转义，生成安全的查询语句。

**$builder->getCompiledInsert()**

该方法和 $builder->insert() 方法一样编译插入查询，但是并不
执行。此方法只是将 SQL 查询作为字符串返回。

例如::

	$data = array(
		'title' => 'My title',
		'name'  => 'My Name',
		'date'  => 'My date'
	);

	$sql = $builder->set($data)->getCompiledInsert('mytable');
	echo $sql;

	// Produces string: INSERT INTO mytable (`title`, `name`, `date`) VALUES ('My title', 'My name', 'My date')

第二个参数用于设置是否重置查询（默认情况下会重置，正如 $builder->insert() 方法一样）::

	echo $builder->set('title', 'My Title')->getCompiledInsert('mytable', FALSE);

	// Produces string: INSERT INTO mytable (`title`) VALUES ('My Title')

	echo $builder->set('content', 'My Content')->getCompiledInsert();

	// Produces string: INSERT INTO mytable (`title`, `content`) VALUES ('My Title', 'My Content')

上面的例子中，最值得注意的是，第二个查询并没有用到 `$builder->from()` 方法， 也没有将表名传递给
第一个参数。 这样做的原因是因为查询尚未使用 `$builder->insert()` 执行，它使用 `$builder->insert()` 重置
值或直接重置。

.. note:: 这个方法不支持批量插入。

**$builder->insertBatch()**

该方法根据你提供的数据生成一条 INSERT 语句并执行，它的参数是一个**数组** 或一个**对象**，
下面是使用数组的例子::

	$data = array(
		array(
			'title' => 'My title',
			'name'  => 'My Name',
			'date'  => 'My date'
		),
		array(
			'title' => 'Another title',
			'name'  => 'Another Name',
			'date'  => 'Another date'
		)
	);

	$builder->insertBatch($data);
	// Produces: INSERT INTO mytable (title, name, date) VALUES ('My title', 'My name', 'My date'),  ('Another title', 'Another name', 'Another date')

第一个参数为要插入的数据，是个二维数组。

.. note:: 所有数据会被自动转义，生成安全的查询语句。

*************
更新数据
*************

**$builder->replace()**


该方法用于执行一条 REPLACE 语句， 该语句基本上是（可选）DELETE + INSERT的SQL标准，
使用 *PRIMARY* 和 *UNIQUE* 键作为决定因素。在我们的例子中，它可以使你免于需要实现与不同的
组合复杂的逻辑 ``select()``， ``update()``， ``delete()`` 和 ``insert()``。

例如::

	$data = array(
		'title' => 'My title',
		'name'  => 'My Name',
		'date'  => 'My date'
	);

	$builder->replace($data);

	// Executes: REPLACE INTO mytable (title, name, date) VALUES ('My title', 'My name', 'My date')

上面的例子中，我们假设 *title* 字段是我们的主键，那么如果我们数据库里有一行
包含 'My title'作为标题，这一行将会被删除并被我们的新数据所取代。

也可以使用 ``set()`` 方法，而且所有字段都被自动转义，正如 ``insert()`` 方法一样。

**$builder->set()**

**该方法可以取代直接传递数据数组到 insert 或 update 方法：**

**它可以用来代替直接将数据数组传递给 insert 或 update 功能:**

::

	$builder->set('name', $name);
	$builder->insert();  // Produces: INSERT INTO mytable (`name`) VALUES ('{$name}')

如果你多次调用该方法，它会正确组装出 insert 或 update 语句来::

	$builder->set('name', $name);
	$builder->set('title', $title);
	$builder->set('status', $status);
	$builder->insert();

**set()** 将方法也接受可选的第三个参数（``$escape``），如果设置为 FALSE，数据将不会自动
转义。为了说明两者之间的区别，这里有一个带转义的 ``set()`` 方法和不带转义的例子。

::

	$builder->set('field', 'field+1', FALSE);
	$builder->where('id', 2);
	$builder->update(); // gives UPDATE mytable SET field = field+1 WHERE `id` = 2

	$builder->set('field', 'field+1');
	$builder->where('id', 2);
	$builder->update(); // gives UPDATE `mytable` SET `field` = 'field+1' WHERE `id` = 2

你也可以传一个关联数组作为参数::

	$array = array(
		'name'   => $name,
		'title'  => $title,
		'status' => $status
	);

	$builder->set($array);
	$builder->insert();

或者一个对象::

	/*
	class Myclass {
		public $title   = 'My Title';
		public $content = 'My Content';
		public $date    = 'My Date';
	}
	*/

	$object = new Myclass;
	$builder->set($object);
	$builder->insert();

**$builder->update()**

该方法根据你提供的数据生成更新字符串并执行，它的参数是一个 **数组** 或一个 **对象** ，
下面是使用数组的例子::

	$data = array(
		'title' => $title,
		'name'  => $name,
		'date'  => $date
	);

	$builder->where('id', $id);
	$builder->update($data);
	// Produces:
	//
	//	UPDATE mytable
	//	SET title = '{$title}', name = '{$name}', date = '{$date}'
	//	WHERE id = $id

或者你可以使用一个对象::

	/*
	class Myclass {
		public $title   = 'My Title';
		public $content = 'My Content';
		public $date    = 'My Date';
	}
	*/

	$object = new Myclass;
	$builder->where('id', $id);
	$builder->update($object);
	// Produces:
	//
	// UPDATE `mytable`
	// SET `title` = '{$title}', `name` = '{$name}', `date` = '{$date}'
	// WHERE id = `$id`

.. note:: 所有数据会被自动转义，生成安全的查询语句。

你应该注意到 $builder->where() 方法的使用，它可以为你设置 WHERE 子句。 
你也可以直接使用字符串形式直接传递给更新函数::

	$builder->update($data, "id = 4");

或者使用一个数组::

	$builder->update($data, array('id' => $id));

当执行更新操作时，你还可以使用上面介绍的 $builder->set() 方法。

**$builder->updateBatch()**

该方法根据你提供的数据生成一条 UPDATE 语句并执行，它的参数是一个 **数组** 或一个 **对象**，下面是使用数组的例子::

	$data = array(
	   array(
	      'title' => 'My title' ,
	      'name'  => 'My Name 2' ,
	      'date'  => 'My date 2'
	   ),
	   array(
	      'title' => 'Another title' ,
	      'name'  => 'Another Name 2' ,
	      'date'  => 'Another date 2'
	   )
	);

	$builder->updateBatch($data, 'title');

	// Produces:
	// UPDATE `mytable` SET `name` = CASE
	// WHEN `title` = 'My title' THEN 'My Name 2'
	// WHEN `title` = 'Another title' THEN 'Another Name 2'
	// ELSE `name` END,
	// `date` = CASE
	// WHEN `title` = 'My title' THEN 'My date 2'
	// WHEN `title` = 'Another title' THEN 'Another date 2'
	// ELSE `date` END
	// WHERE `title` IN ('My title','Another title')

第一个参数为要更新的数据，是个二维数组，第二个参数是 where 语句的键。

.. note:: 所有数据会被自动转义，生成安全的查询语句。

.. note:: 取决于该方法的内部实现，在这个方法之后调用 ``affectedRows()`` 方法返回的结果可能会不正确。 但是你可以使用 ``updateBatch()`` 方法的返回值， 代表了受影响的行数。

**$builder->getCompiledUpdate()**

该方法和 ``$builder->getCompiledInsert()`` 方法完全一样，除了生成的 SQL 语句
是 UPDATE 而不是 INSERT。

查看 `$builder->getCompiledInsert()` 方法的文档获取更多信息。

.. note:: 该方法不支持批量更新。

*************
删除数据
*************

**$builder->delete()**

该方法生成删除SQL语句并执行。

::

	$builder->delete(array('id' => $id));  // Produces: // DELETE FROM mytable  // WHERE id = $id

第一个参数为 where 条件。你也可以不用第一个参数， 使用 where() 或者 or_where() 
函数来替代它::

	$builder->where('id', $id);
	$builder->delete();

	// Produces:
	// DELETE FROM mytable
	// WHERE id = $id

如果你想要删除一个表中的所有数据，可以使用 truncate() 或 empty_table() 方法。.

**$builder->emptyTable()**

该方法生成删除SQl语句并执行::

	  $builder->emptyTable('mytable'); // Produces: DELETE FROM mytable

**$builder->truncate()**

该方法生截断SQL语句并执行。

::

	$builder->truncate();

	// Produces:
	// TRUNCATE mytable

.. note:: 如果 TRUNCATE 语句不可用，truncate() 方法将执行 "DELETE FROM table"。

**$builder->getCompiledDelete()**

该方法和 ``$builder->getCompiledInsert()`` 方法完全一样，除了生成的 SQL 语句是 DELETE 而不是 INSERT。

查看 $builder->getCompiledInsert() 方法的文档获取更多信息。

***************
链式方法
***************

通过将多个方法连接在一起，链式方法可以大大的简化你的语法。感受一下这个例子::

	$query = $builder->select('title')
			 ->where('id', $id)
			 ->limit(10, 20)
			 ->get();

.. _ar-caching:

***********************
重置查询构造器
***********************

**$builder->resetQuery()**

该方法无需执行就能重置查询构造器中的查询，$builder->get() 或 $builder->insert() 方法也可以用于重置查询，但是必须要先执行它。

当你在使用查询构造器生成 SQL 语句（如：``$builder->getCompiledSelect()``）， 之后再执行它。这种情况下，不重置查询缓存将非常有用::

		// 注意 get_compiled_select 方法的第二个参数为 FALSE
    $sql = $builder->select(array('field1','field2'))
                   ->where('field3',5)
                   ->getCompiledSelect(false);

    // ...
    // 用 SQL 代码做一些疯狂的事情... 比如将它添加到 cron 脚本中
    // 以后执行还是什么...
    // ...

    $data = $builder->get()->getResultArray();

    // 会执行并返回以下查询的结果数组吗:
    // SELECT field1, field1 from mytable where field3 = 5;

***************
类引用
***************

.. php:class:: \CodeIgniter\Database\BaseBuilder

	.. php:method:: resetQuery()

		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		重置当前查询生成器状态。在你需要的时候有用要构建可以在特定条件下取消的查询.

	.. php:method:: countAllResults([$reset = TRUE])

		:param	bool	$reset: 是否重置SELECT的值
		:returns:	查询结果中的行数
		:rtype:	int

		生成一个特定于平台的查询字符串，查询生成器查询返回的所有记录。

	.. php:method:: get([$limit = NULL[, $offset = NULL]])

		:param	int	$limit: The LIMIT clause
		:param	int	$offset: The OFFSET clause
		:returns:	\CodeIgniter\Database\ResultInterface instance (方法链)
		:rtype:	\CodeIgniter\Database\ResultInterface

		基于已经编译并运行SELECT语句， 称为Query Builder方法。

	.. php:method:: getWhere([$where = NULL[, $limit = NULL[, $offset = NULL]]])

		:param	string	$where: The WHERE clause
		:param	int	$limit: The LIMIT clause
		:param	int	$offset: The OFFSET clause
		:returns:	\CodeIgniter\Database\ResultInterface instance (方法链)
		:rtype:	\CodeIgniter\Database\ResultInterface

		与 ``get()`` 相同，但也允许直接添加 WHERE。

	.. php:method:: select([$select = '*'[, $escape = NULL]])

		:param	string	$select: 查询的 SELECT 部分
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 SELECT 子句。

	.. php:method:: selectAvg([$select = ''[, $alias = '']])

		:param	string	$select: 用于计算平均值的字段
		:param	string	$alias: 结果值名称的别名
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 SELECT AVG(field) 子句。

	.. php:method:: selectMax([$select = ''[, $alias = '']])

		:param	string	$select: 用于计算最大值的字段
		:param	string	$alias: 结果值名称的别名
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 SELECT MAX(field) 子句。

	.. php:method:: selectMin([$select = ''[, $alias = '']])

		:param	string	$select: 用于计算最小值的字段
		:param	string	$alias: 结果值名称的别名
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 SELECT MIN(field) 子句。

	.. php:method:: selectSum([$select = ''[, $alias = '']])

		:param	string	$select: 字段来计算总和
		:param	string	$alias: 结果值名称的别名
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 SELECT SUM(field) 子句。

	.. php:method:: distinct([$val = TRUE])

		:param	bool	$val: 期望值的 "distinct" 标志
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		设置一个标志， 告诉查询构建器添加查询的 SELECT 部分的 DISTINCT 子句。

	.. php:method:: from($from)

		:param	mixed	$from: Table name(s); 字符串或数组
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		指定查询的 FROM 子句。

	.. php:method:: join($table, $cond[, $type = ''[, $escape = NULL]])

		:param	string	$table: Table name to join
		:param	string	$cond: The JOIN ON condition
		:param	string	$type: The JOIN type
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加JOIN子句。

	.. php:method:: where($key[, $value = NULL[, $escape = NULL]])

		:param	mixed	$key: 要比较的字段名称或关联数组
		:param	mixed	$value: 如果是单个键，则与此值相比
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance
		:rtype:	object

		生成查询的WHERE部分。 用 'AND' 分隔多个调用。

	.. php:method:: orWhere($key[, $value = NULL[, $escape = NULL]])

		:param	mixed	$key: 要比较的字段名称或关联数组
		:param	mixed	$value: 如果是单个键，则与此值相比
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance
		:rtype:	object

		生成查询的WHERE部分。 用'OR'分隔多个调用。

	.. php:method:: orWhereIn([$key = NULL[, $values = NULL[, $escape = NULL]]])

		:param	string	$key: 要搜索的字段
		:param	array	$values: 搜索的值
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance
		:rtype:	object

		生成一个 WHERE 字段 IN('item'，'item') SQL 查询，
		如果合适，加上 'OR' 。

	.. php:method:: orWhereNotIn([$key = NULL[, $values = NULL[, $escape = NULL]]])

		:param	string	$key: 要搜索的字段
		:param	array	$values: 搜索的值
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance
		:rtype:	object

		生成一个 WHERE 字段 NOT IN('item'，'item') SQL 查询，
		如果合适，加上 'OR' 。

	.. php:method:: whereIn([$key = NULL[, $values = NULL[, $escape = NULL]]])

		:param	string	$key: 要检查的字段的名称
		:param	array	$values: 目标值数组
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance
		:rtype:	object

		生成一个 WHERE 字段 IN('item'，'item') SQL 查询， 如果合适，加入 'AND' 。

	.. php:method:: whereNotIn([$key = NULL[, $values = NULL[, $escape = NULL]]])

		:param	string	$key: 要检查的字段的名称
		:param	array	$values: 目标值数组
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance
		:rtype:	object

		生成一个 WHERE 字段 NOT IN('item'，'item') SQL 查询，
		如果合适，加入 'AND' 。

	.. php:method:: groupStart()

		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		启动组表达式，使用 ANDs 表示其中的条件。

	.. php:method:: orGroupStart()

		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		启动组表达式，使用 ORs 表示其中的条件。

	.. php:method:: notGroupStart()

		:returns:	BaseBuilder instance (method chaining)
		:rtype:	BaseBuilder

		启动组表达式，使用 AND NOTs 表示其中的条件。

	.. php:method:: orNotGroupStart()

		:returns:	BaseBuilder instance (method chaining)
		:rtype:	BaseBuilder

		启动组表达式，使用 OR NOTs 表示其中的条件。

	.. php:method:: groupEnd()

		:returns:	BaseBuilder instance
		:rtype:	object

		Ends a group expression.

	.. php:method:: like($field[, $match = ''[, $side = 'both'[, $escape = NULL]]])

		:param	string	$field: 字段名
		:param	string	$match: 匹配的文本部分
		:param	string	$side: 将 '%' 通配符放在表达式的哪一侧
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 LIKE 子句，用 AND 分隔多个调用。

	.. php:method:: orLike($field[, $match = ''[, $side = 'both'[, $escape = NULL]]])

		:param	string	$field: 字段名
		:param	string	$match: 匹配的文本部分
		:param	string	$side: 将 '%' 通配符放在表达式的哪一侧
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 LIKE 子句，用 OR 分隔多个调用。

	.. php:method:: notLike($field[, $match = ''[, $side = 'both'[, $escape = NULL]]])

		:param	string	$field: 字段名
		:param	string	$match: 匹配的文本部分
		:param	string	$side: 将 '%' 通配符放在表达式的哪一侧
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 NOT LIKE 子句，用 AND 分隔多个调用。

	.. php:method:: orNotLike($field[, $match = ''[, $side = 'both'[, $escape = NULL]]])

		:param	string	$field: 字段名
		:param	string	$match: 匹配的文本部分
		:param	string	$side: 将 '%' 通配符放在表达式的哪一侧
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 NOT LIKE 子句，用 OR 分隔多个调用。

	.. php:method:: having($key[, $value = NULL[, $escape = NULL]])

		:param	mixed	$key: 标识符（字符串）或 field/value 对的关联数组
		:param	string	$value: 如果 $key 是标识符，则寻求值
		:param	string	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 HAVING 子句，用 AND 分隔多个调用。

	.. php:method:: orHaving($key[, $value = NULL[, $escape = NULL]])

		:param	mixed	$key: 标识符（字符串）或 field/value 对的关联数组
		:param	string	$value: 如果 $key 是标识符，则寻求值
		:param	string	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 HAVING 子句，用 OR 分隔多个调用。

	.. php:method:: groupBy($by[, $escape = NULL])

		:param	mixed	$by: 根据字段分组; 字符串或数组
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 GROUP BY 子句。

	.. php:method:: orderBy($orderby[, $direction = ''[, $escape = NULL]])

		:param	string	$orderby: 根据字段排序
		:param	string	$direction: 请求的排序 - ASC， DESC 或随机
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 ORDER BY 子句。

	.. php:method:: limit($value[, $offset = 0])

		:param	int	$value: 限制返回行数
		:param	int	$offset: 偏移行数
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 LIMIT 和 OFFSET 子句。

	.. php:method:: offset($offset)

		:param	int	$offset:  偏移行数
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 OFFSET 子句。

	.. php:method:: set($key[, $value = ''[, $escape = NULL]])

		:param	mixed	$key: 标识符（字符串）或 field/value 对的关联数组
		:param	string	$value: 字段值，如果 $key 是单个字段
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		添加要稍后传递给 ``insert()`` 的 field/value 对， ``update()`` 或 ``replace()``。

	.. php:method:: insert([$set = NULL[, $escape = NULL]])

		:param	array	$set: field/value 对的关联数组
		:param	bool	$escape: 是否转义值和标识符
		:returns:	成功时为 TRUE，失败时为 FALSE
		:rtype:	bool

		编译并执行 INSERT 语句。

	.. php:method:: insertBatch([$set = NULL[, $escape = NULL[, $batch_size = 100]]])

		:param	array	$set: 插入数据
		:param	bool	$escape: 是否转义值和标识符
		:param	int	$batch_size: 要一次插入的行数
		:returns:	插入的行数或失败时的 FALSE
		:rtype:	mixed

		编译并执行批处理 ``INSERT`` 语句。

		.. note:: 当提供超过 ``$batch_size`` 行时， 多个将执行``INSERT``
		
		查询， 每次尝试插入最多为 ``$batch_size`` 行。

	.. php:method:: setInsertBatch($key[, $value = ''[, $escape = NULL]])

		:param	mixed	$key: field/value 对应的关联数组
		:param	string	$value: 字段值，如果 $key 是单个字段
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		稍后通过 ``insertBatch()`` 添加要插入表中的 field/value 对。

	.. php:method:: update([$set = NULL[, $where = NULL[, $limit = NULL]]])

		:param	array	$set: field/value 对应的关联数组
		:param	string	$where: The WHERE clause
		:param	int	$limit: The LIMIT clause
		:returns:	TRUE 为成功, FALSE 为失败
		:rtype:	bool

		编译并执行 UPDATE 语句。

	.. php:method:: updateBatch([$set = NULL[, $value = NULL[, $batch_size = 100]]])

		:param	array	$set: 字段名， 或 field/value 对的关联数组
		:param	string	$value: 字段值，如果 $set 是单个字段
		:param	int	$batch_size: 在单个查询中分组的条件计数
		:returns:	更新的行数或失败时的 FALSE
		:rtype:	mixed

		编译并执行批处理 ``UPDATE`` 语句。

		当提供超过 ``$batch_size`` field/value 对时，
		将执行多个查询，每个处理最多 ``$batch_size`` field/value 对。

	.. php:method:: setUpdateBatch($key[, $value = ''[, $escape = NULL]])

		:param	mixed	$key: 字段名， 或 field/value 对的关联数组
		:param	string	$value: 字段值，如果 $key 是单个字段
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		稍后通过``updateBatch（）``添加要在表中更新的 field/value 对。

	.. php:method:: replace([$set = NULL])

		:param	array	$set: field/value 对应的关联数组
		:returns:	TRUE 为成功, FALSE 为失败
		:rtype:	bool

		编译并执行REPLACE语句。

	.. php:method:: delete([$where = ''[, $limit = NULL[, $reset_data = TRUE]]])

		:param	string	$where: The WHERE clause
		:param	int	$limit: The LIMIT clause
		:param	bool	$reset_data: TRUE 重置查询 "write" 子句
		:returns:	BaseBuilder instance (方法链) 或者失败时为 FALSE
		:rtype:	mixed

		编译并执行 DELETE 查询。

    .. php:method:: increment($column[, $value = 1])

        :param string $column: 要递增的列的名称
        :param int    $value:  要增加列的数量

				按指定的数量增加字段的值。 如果是这个领域不是 numeric 字段，如 VARCHAR， 它可能会被替换价值 $value。

    .. php:method:: decrement($column[, $value = 1])

        :param string $column: 要减少的列的名称
        :param int    $value:  减少列的数量

				按指定的数量减去字段的值。 如果是这个领域不是 numeric 字段，如 VARCHAR， 它可能会被替换价值 $value。

	.. php:method:: truncate()

		:returns:	TRUE 为成功, FALSE 为失败
		:rtype:	bool

		在表上执行 TRUNCATE 语句。

		.. note:: 如果使用的数据库平台不支持 TRUNCATE， 将使用DELETE语句。

	.. php:method:: emptyTable()

		:returns:	TRUE 为成功, FALSE 为失败
		:rtype:	bool

		通过 DELETE 语句删除表中的所有记录。

	.. php:method:: getCompiledSelect([$reset = TRUE])

		:param	bool	$reset: 是否重置当前 QB 值
		:returns:	已编译的 SQL 语句为字符串
		:rtype:	string

		编译 SELECT 语句并将其作为字符串返回。

	.. php:method:: getCompiledInsert([$reset = TRUE])

		:param	bool	$reset: 是否重置当前 QB 值
		:returns:	已编译的 SQL 语句为字符串
		:rtype:	string

		编译 INSERT 语句并将其作为字符串返回。

	.. php:method:: getCompiledUpdate([$reset = TRUE])

		:param	bool	$reset: 是否重置当前 QB 值
		:returns:	已编译的 SQL 语句为字符串
		:rtype:	string

		编译 UPDATE 语句并将其作为字符串返回。

	.. php:method:: getCompiledDelete([$reset = TRUE])

		:param	bool	$reset: 是否重置当前 QB 值
		:returns:	已编译的 SQL 语句为字符串
		:rtype:	string

		编译 DELETE 语句并将其作为字符串返回。
