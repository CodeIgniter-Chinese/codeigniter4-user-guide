###################
查询构造器类
###################

CodeIgniter 提供了查询构造器类，它允许你用较少的代码量获取数据库的信息、新增
或更新数据。有时只需要一两行代码就能完成数据库操作。CodeIgniter 不要求每个数据表
有一个类文件，它使用了一种更简单的接口。

除了简单，使用查询构造器的主要好处是可以让你创建跨数据库的应用程序，因为查询语句
是由每种数据库适配器生成的。它也允许用于更安全的查询，因为系统会自动转义传入数据。

.. contents::
    :local:
    :depth: 2

*************************
加载查询构造器
*************************

查询构造器通过数据库连接对象的 ``table()`` 方法加载，
这会设置查询语句 ``FROM`` 的部分并且返回一个查询构造器的新实例::

    $db      = \Config\Database::connect();
    $builder = $db->table('users');

查询构造器仅在你明确请求类时才加载到内存中，因此默认不使用（消耗）任何资源。

**************
选择数据
**************

下面的方法用来构建 SQL **SELECT** 语句。

**$builder->get()**

执行选择查询并返回结果，可用于获取一个表的所有记录::

    $builder = $db->table('mytable');
    $query   = $builder->get();  // 生成: SELECT * FROM mytable

第一个和第二个参数用于设置 limit 和 offset 子句::

	$query = $builder->get(10, 20);

	// 执行: SELECT * FROM mytable LIMIT 20, 10
	// (在 MySQL 里的情况，其他数据库的语法略有不同）

你应该已经注意到了，上面方法的结果赋值给了一个 $query 变量，
我们可以用它输出查询结果::

	$query = $builder->get();

	foreach ($query->getResult() as $row)
	{
		echo $row->title;
	}

请访问 :doc:`结果方法 <results>` 页面获得结果生成的完整论述。

**$builder->getCompiledSelect()**

和 **$builder->get()** 方法一样编译选择查询但是并不执行，
此方法只是将 SQL 查询语句作为字符串返回。

例如::

	$sql = $builder->getCompiledSelect();
	echo $sql;

	// 输出字符串: SELECT * FROM mytable

第一个参数使你能设置是否重置查询构造器（默认重置，
就像使用 `$builder->get()` 时一样)::

	echo $builder->limit(10,20)->getCompiledSelect(false);

	// 输出字符串: SELECT * FROM mytable LIMIT 20, 10
	// (在 MySQL 里的情况，其他数据库的语法略有不同）

	echo $builder->select('title, content, date')->getCompiledSelect();

	// 输出字符串: SELECT title, content, date FROM mytable LIMIT 20, 10

最值得注意的是，上例第二个查询并没有用到 **$builder->from()** 方法， 
也没有为查询指定表名参数。因为这个查询没有被可重置值的 **$builder->get()** 方法执行，或是使用 **$builder->resetQuery()** 方法直接重置。

**$builder->getWhere()**

与 ``get()`` 函数相同，只是它允许你用第一个参数中添加 "where" 子句，
而不是使用 db->where() 功能::

	$query = $builder->getWhere(['id' => $id], $limit, $offset);

请阅读下面 `where` 方法获得更多信息。

**$builder->select()**

允许你编写查询的 SELECT 部分::

	$builder->select('title, content, date');
	$query = $builder->get();

	// 执行: SELECT title, content, date FROM mytable

.. 注解:: 如果要从表中选择全部字段 (\*) ，不需要使用这个函数。
    当省略它时，CodeIgniter 假定你希望选择所有字段并自动添加 'SELECT \*' 。

``$builder->select()`` 方法的第二个参数可选，如果设置为 FALSE，
CodeIgniter 将不保护你的表名和字段名。当你编写复合查询语句时很有用，
它不会因为自动转义而搞坏你的语句。

::

	$builder->select('(SELECT SUM(payments.amount) FROM payments WHERE payments.invoice_id=4) AS amount_paid', FALSE);
	$query = $builder->get();

**$builder->selectMax()**

该方法用于编写查询语句中的 ``SELECT MAX(field)`` 部分，
你可以使用第二个参数重命名结果字段（可选）。

::

	$builder->selectMax('age');
	$query = $builder->get();  // 生成: SELECT MAX(age) as age FROM mytable

	$builder->selectMax('age', 'member_age');
	$query = $builder->get(); // 生成: SELECT MAX(age) as member_age FROM mytable

**$builder->selectMin()**

该方法用于编写查询语句中的 "SELECT MIN(field)" 部分，
和 selectMax() 一样，你可以使用第二个参数重命名结果字段（可选）。

::

	$builder->selectMin('age');
	$query = $builder->get(); // 生成: SELECT MIN(age) as age FROM mytable

**$builder->selectAvg()**

该方法用于编写查询语句中的 "SELECT AVG(field)" 部分，
和 selectMax() 一样，你可以使用第二个参数重命名结果字段（可选）。

::

	$builder->selectAvg('age');
	$query = $builder->get(); // 生成: SELECT AVG(age) as age FROM mytable

**$builder->selectSum()**

该方法用于编写查询语句中的 "SELECT SUM(field)" 部分，
和 selectMax() 一样，你可以使用第二个参数重命名结果字段（可选）。

::

	$builder->selectSum('age');
	$query = $builder->get(); // 生成: SELECT SUM(age) as age FROM mytable

**$builder->selectCount()**

该方法用于编写查询语句中的 "SELECT COUNT(field)" 部分，
和 selectMax() 一样，你可以使用第二个参数重命名结果字段（可选）。

.. 注解:: 该方法在使用 ``groupBy()`` 时特别有用。
        用于一般的结果计数详见 ``countAll()`` 或 ``countAllResults()`` 。

::

	$builder->selectCount('age');
	$query = $builder->get(); // 生成: SELECT COUNT(age) as age FROM mytable

**$builder->from()**

该方法用于编写查询语句中的 FROM 子句::

	$builder->select('title, content, date');
	$builder->from('mytable');
	$query = $builder->get();  // 生成: SELECT title, content, date FROM mytable

.. 注解:: 正如前面所说，查询中的 FROM 部分可以在方法 $db->table() 中指定。
    额外调用 from() 将向查询的 FROM 部分添加更多表。

**$builder->join()**

该方法用于编写查询语句中的 JOIN 子句::

    $builder->db->table('blog');
    $builder->select('*');
    $builder->join('comments', 'comments.id = blogs.id');
    $query = $builder->get();

    // 生成:
    // SELECT * FROM blogs JOIN comments ON comments.id = blogs.id

如果你的查询有多个连接，可以多次调用这个方法。

你可以传入第三个参数指定连接的类型，可选: left，right, 
outer, inner, left outer 和 right outer 。

::

	$builder->join('comments', 'comments.id = blogs.id', 'left');
	// 生成: LEFT JOIN comments ON comments.id = blogs.id

*************************
查找具体数据
*************************

**$builder->where()**

该方法提供了4中方式让你编写查询语句中的 **WHERE** 子句:

.. 注解:: 所有传入数据将会自动转义，生成安全的查询语句。

#. **简单的 key/value 方式:**

	::

		$builder->where('name', $name); // 生成: WHERE name = 'Joe'

	注意它自动为你加上了等号。

	如果你多次调用该方法，那么多个 WHERE 条件将会使用 AND 连接:

	::

		$builder->where('name', $name);
		$builder->where('title', $title);
		$builder->where('status', $status);
		// WHERE name = 'Joe' AND title = 'boss' AND status = 'active'

#. **自定义 key/value 方式:**

	你可以在第一个参数中包含一个比较运算符，用来控制比较条件:

	::

		$builder->where('name !=', $name);
		$builder->where('id <', $id); // 生成: WHERE name != 'Joe' AND id < 45

#. **关联数组方式:**

	::

		$array = ['name' => $name, 'title' => $title, 'status' => $status];
		$builder->where($array);
		// 生成: WHERE name = 'Joe' AND title = 'boss' AND status = 'active'

	你也可以在这个方法里包含你自己的运算符:

	::

		$array = ['name !=' => $name, 'id <' => $id, 'date >' => $date];
		$builder->where($array);

#. **自定义字符串:**
	你可以手动编写子句::

		$where = "name='Joe' AND status='boss' OR status='active'";
		$builder->where($where);

``$builder->where()`` 的第三个参数（可选），如果设置为 FALSE，CodeIgniter 
将不保护你的表名和字段名。

::

	$builder->where('MATCH (field) AGAINST ("value")', NULL, FALSE);

#. **子查询:**
    你可以使用匿名函数生成一个子查询。

    ::

        $builder->where('advance_amount <', function(BaseBuilder $builder) {
            return $builder->select('MAX(advance_amount)', false)->from('orders')->where('id >', 2);
        });
        // 生成: WHERE "advance_amount" < (SELECT MAX(advance_amount) FROM "orders" WHERE "id" > 2)

**$builder->orWhere()**

这个方法和上面的方法一样，只是多个条件之间使用 OR 进行连接

    ::

	$builder->where('name !=', $name);
	$builder->orWhere('id >', $id);  // 生成: WHERE name != 'Joe' OR id > 50

**$builder->whereIn()**

该方法用于生成 WHERE IN('item', 'item') 子句，多个子句之间使用 AND 连接

    ::

        $names = ['Frank', 'Todd', 'James'];
        $builder->whereIn('username', $names);
        // 生成: WHERE username IN ('Frank', 'Todd', 'James')

你可以用子查询替代数组值。

    ::

        $builder->whereIn('id', function(BaseBuilder $builder) {
            return $builder->select('job_id')->from('users_jobs')->where('user_id', 3);
        });
        // 生成: WHERE "id" IN (SELECT "job_id" FROM "users_jobs" WHERE "user_id" = 3)

**$builder->orWhereIn()**

该方法用于生成 WHERE IN('item', 'item') 子句，多个子句之间使用 OR 连接

    ::

        $names = ['Frank', 'Todd', 'James'];
        $builder->orWhereIn('username', $names);
        // 生成: OR username IN ('Frank', 'Todd', 'James')

你可以用子查询替代数组值。

    ::

        $builder->orWhereIn('id', function(BaseBuilder $builder) {
            return $builder->select('job_id')->from('users_jobs')->where('user_id', 3);
        });

        // 生成: OR "id" IN (SELECT "job_id" FROM "users_jobs" WHERE "user_id" = 3)

**$builder->whereNotIn()**

该方法用于生成 WHERE NOT IN('item', 'item') 子句，多个子句之间使用 AND 连接

    ::

        $names = ['Frank', 'Todd', 'James'];
        $builder->whereNotIn('username', $names);
        // 生成: WHERE username NOT IN ('Frank', 'Todd', 'James')

你可以用子查询替代数组值。

    ::

        $builder->whereNotIn('id', function(BaseBuilder $builder) {
            return $builder->select('job_id')->from('users_jobs')->where('user_id', 3);
        });

        // 生成: WHERE "id" NOT IN (SELECT "job_id" FROM "users_jobs" WHERE "user_id" = 3)


**$builder->orWhereNotIn()**

该方法用于生成 WHERE NOT IN('item', 'item') 子句，多个子句之间使用 OR 连接

    ::

        $names = ['Frank', 'Todd', 'James'];
        $builder->orWhereNotIn('username', $names);
        // 生成: OR username NOT IN ('Frank', 'Todd', 'James')

你可以用子查询替代数组值。

    ::

        $builder->orWhereNotIn('id', function(BaseBuilder $builder) {
            return $builder->select('job_id')->from('users_jobs')->where('user_id', 3);
        });

        // 生成: OR "id" NOT IN (SELECT "job_id" FROM "users_jobs" WHERE "user_id" = 3)

************************
查找相似的数据
************************

**$builder->like()**

这个方法使您能够生成类似 **LIKE** 子句，做搜索时非常有用。

.. 注解:: 所有传入数据将被自动转义。

.. 注解:: ``like*`` 通过传第五个参数传递值 ``true`` 可以强制在
	执行查询时不区分大小写。这项特性可用性跟平台相关，否则将强制值转为小写，
	例如 ``WHERE LOWER(column) LIKE '%search%'``，让其生效可能需要
	在制作索引时用 ``LOWER(column)`` 而不是 ``column`` 。

#. **简单 key/value 方式:**

	::

		$builder->like('title', 'match');
		// 生成: WHERE `title` LIKE '%match%' ESCAPE '!'

	如果你多次调用该方法，那么多个 WHERE 条件将会使用 AND 连接起来::

		$builder->like('title', 'match');
		$builder->like('body', 'match');
		// WHERE `title` LIKE '%match%' ESCAPE '!' AND  `body` LIKE '%match% ESCAPE '!'

	如果你想控制通配符通配符（%）的位置，可以指定第三个参数，
	可用选项：'before'，'after' 和 'both' (默认) 。

	::

		$builder->like('title', 'match', 'before');	// 生成: WHERE `title` LIKE '%match' ESCAPE '!'
		$builder->like('title', 'match', 'after');	// 生成: WHERE `title` LIKE 'match%' ESCAPE '!'
		$builder->like('title', 'match', 'both');	// 生成: WHERE `title` LIKE '%match%' ESCAPE '!'

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

这个方法和 ``like()`` 方法一样，只是生成 NOT LIKE 子句::

	$builder->notLike('title', 'match');	// WHERE `title` NOT LIKE '%match% ESCAPE '!'

**$builder->orNotLike()**

这个方法和 ``notLike()`` 方法一样，只是多个条件之间使用 OR 连接::

	$builder->like('title', 'match');
	$builder->orNotLike('body', 'match');
	// WHERE `title` LIKE '%match% OR  `body` NOT LIKE '%match%' ESCAPE '!'

**$builder->groupBy()**

该方法用于生成 GROUP BY 子句::

	$builder->groupBy("title"); // 生成: GROUP BY title

你也可以通过一个数组传入多个值::

	$builder->groupBy(["title", "date"]);  // 生成: GROUP BY title, date

**$builder->distinct()**

该方法用于向查询中添加 "DISTINCT" 关键字

::

	$builder->distinct();
	$builder->get(); // 生成: SELECT DISTINCT * FROM mytable

**$builder->having()**

该方法用于生成 HAVING 子句，有下面两种不同的语法。
有两种可用语法，单参数或双参数::

	$builder->having('user_id = 45');  // 生成: HAVING user_id = 45
	$builder->having('user_id',  45);  // 生成: HAVING user_id = 45

你还可以传递一个包含多个值的数组::

	$builder->having(['title =' => 'My Title', 'id <' => $id]);
	// 生成: HAVING title = 'My Title', id < 45

如果你正在使用 CodeIgniter 为其转义查询的数据库，
你可以传第三个可选参数来防止转义内容，设为 FALSE 。

::

	$builder->having('user_id',  45);  // 生成: HAVING `user_id` = 45 in some databases such as MySQL
	$builder->having('user_id',  45, FALSE);  // 生成: HAVING user_id = 45

**$builder->orHaving()**

该方法和 having() 方法一样，只是多个条件之间使用 "OR" 进行连接。

**$builder->havingIn()**

生成一个 HAVING 字段的 IN ('item', 'item') SQL 查询子句，
多个条件之间使用 AND 连接

    ::

        $groups = [1, 2, 3];
        $builder->havingIn('group_id', $groups);
        // 生成: HAVING group_id IN (1, 2, 3)

你可以用子查询代替数组。

    ::

        $builder->havingIn('id', function(BaseBuilder $builder) {
            return $builder->select('user_id')->from('users_jobs')->where('group_id', 3);
        });
        // 生成: HAVING "id" IN (SELECT "user_id" FROM "users_jobs" WHERE "group_id" = 3)

**$builder->orHavingIn()**

生成一个 HAVING 字段的 IN ('item', 'item') SQL 查询子句，
多个条件之间使用 OR 连接

    ::

        $groups = [1, 2, 3];
        $builder->orHavingIn('group_id', $groups);
        // 生成: OR group_id IN (1, 2, 3)

你可以用子查询代替数组。

    ::

        $builder->orHavingIn('id', function(BaseBuilder $builder) {
            return $builder->select('user_id')->from('users_jobs')->where('group_id', 3);
        });

        // 生成: OR "id" IN (SELECT "user_id" FROM "users_jobs" WHERE "group_id" = 3)

**$builder->havingNotIn()**

生成一个 HAVING 字段的 NOT IN ('item', 'item') SQL 查询子句，
多个条件之间使用 AND 连接

    ::

        $groups = [1, 2, 3];
        $builder->havingNotIn('group_id', $groups);
        // 生成: HAVING group_id NOT IN (1, 2, 3)

你可以用子查询代替数组。

    ::

        $builder->havingNotIn('id', function(BaseBuilder $builder) {
            return $builder->select('user_id')->from('users_jobs')->where('group_id', 3);
        });

        // 生成: HAVING "id" NOT IN (SELECT "user_id" FROM "users_jobs" WHERE "group_id" = 3)


**$builder->orHavingNotIn()**

生成一个 HAVING 字段的 NOT IN ('item', 'item') SQL 查询子句，
多个条件之间使用 OR 连接

    ::

        $groups = [1, 2, 3];
        $builder->havingNotIn('group_id', $groups);
        // 生成: OR group_id NOT IN (1, 2, 3)

你可以用子查询代替数组。

    ::

        $builder->orHavingNotIn('id', function(BaseBuilder $builder) {
            return $builder->select('user_id')->from('users_jobs')->where('group_id', 3);
        });

        // 生成: OR "id" NOT IN (SELECT "user_id" FROM "users_jobs" WHERE "group_id" = 3)

**$builder->havingLike()**

该方法让你能够在 HAVING 查询部分生成 **LIKE** 子句，常用于搜索。

.. 注解:: 该方法所有传入参数会被自动转义。

.. 注解:: ``havingLike*`` 通过传第五个参数传递值 ``true`` 可以强制在
	执行查询时不区分大小写。这项特性可用性跟平台相关，否则将强制值转为小写，
	例如 ``HAVING LOWER(column) LIKE '%search%'``，让其生效可能需要
	在制作索引时用 ``LOWER(column)`` 而不是 ``column`` 。

#. **简单 key/value 方式:**

	::

		$builder->havingLike('title', 'match');
		// 生成: HAVING `title` LIKE '%match%' ESCAPE '!'

	如果你多次调用该方法，那么多个 WHERE 条件将会使用 AND 连接起来::

		$builder->havingLike('title', 'match');
		$builder->havingLike('body', 'match');
		// HAVING `title` LIKE '%match%' ESCAPE '!' AND  `body` LIKE '%match% ESCAPE '!'

	如果你想控制通配符通配符（%）的位置，可以指定第三个参数，
	可用选项：'before'，'after' 和 'both' (默认) 。

	::

		$builder->havingLike('title', 'match', 'before');	// 生成: HAVING `title` LIKE '%match' ESCAPE '!'
		$builder->havingLike('title', 'match', 'after');	// 生成: HAVING `title` LIKE 'match%' ESCAPE '!'
		$builder->havingLike('title', 'match', 'both');	// 生成: HAVING `title` LIKE '%match%' ESCAPE '!'

#. **关联数组方式:**

	::

		$array = ['title' => $match, 'page1' => $match, 'page2' => $match];
		$builder->havingLike($array);
		// HAVING `title` LIKE '%match%' ESCAPE '!' AND  `page1` LIKE '%match%' ESCAPE '!' AND  `page2` LIKE '%match%' ESCAPE '!'

**$builder->orHavingLike()**

这个方法和上面的方法一样，只是多个条件之间使用 OR 进行连接::

	$builder->havingLike('title', 'match'); $builder->orHavingLike('body', $match);
	// HAVING `title` LIKE '%match%' ESCAPE '!' OR  `body` LIKE '%match%' ESCAPE '!'

**$builder->notHavingLike()**

这个方法和 ``havingLike()`` 一样，只是它生成的是 NOT LIKE 子句::

	$builder->notHavingLike('title', 'match');	// HAVING `title` NOT LIKE '%match% ESCAPE '!'

**$builder->orNotHavingLike()**

这个方法和 ``notHavingLike()`` 一样，只是多个条件之间使用 OR 进行连接::

	$builder->havingLike('title', 'match');
	$builder->orNotHavingLike('body', 'match');
	// HAVING `title` LIKE '%match% OR  `body` NOT LIKE '%match%' ESCAPE '!'

****************
结果排序
****************

**$builder->orderBy()**

该方法用于生成 ORDER BY 子句。

第一个参数包含你要排序的列名。

第二个参数用于设置排序的方向，
可选项有： **ASC** ， **DESC** 和 **RANDOM** 。

::

	$builder->orderBy('title', 'DESC');
	// 生成: ORDER BY `title` DESC

第一个参数也可以是你自己的排序字符串::

	$builder->orderBy('title DESC, name ASC');
	// 生成: ORDER BY `title` DESC, `name` ASC

如果需要根据多个字段进行排序，可以多次调用该方法。

::

	$builder->orderBy('title', 'DESC');
	$builder->orderBy('name', 'ASC');
	// 生成: ORDER BY `title` DESC, `name` ASC

如果你选择了 **RANDOM** 选项，第一个参数会被忽略，
除非你指定第一个参数作为随机数的种子。

::

	$builder->orderBy('title', 'RANDOM');
	// 生成: ORDER BY RAND()

	$builder->orderBy(42, 'RANDOM');
	// 生成: ORDER BY RAND(42)

.. 注解:: Oracle 目前还不支持随机排序，会默认使用 ASC 替代。

****************************
结果分页与计数
****************************

**$builder->limit()**

该方法可以让你限制查询结果的返回行数::

	$builder->limit(10);  // 生成: LIMIT 10

第二个参数可以用来设置偏移。

::

	$builder->limit(10, 20);  // 生成: LIMIT 20, 10 (在 MySQL 里的情况，其他数据库的语法略有不同）


**$builder->countAllResults()**

该方法用于获取指定构造器查询返回的结果数量，接受的构造器方法有
 ``where()`` , ``orWhere()`` , ``like()`` , ``orLike()`` 等，例如::

	echo $builder->countAllResults('my_table');  // 生成一个整数，比如 25
	$builder->like('title', 'match');
	$builder->from('my_table');
	echo $builder->countAllResults(); // 生成一个整数，比如 17

然而，这个方法会重置你在 ``select()`` 里设置的所有值，
如果你要保留它们，可以将第一个参数设置为 FALSE::

	echo $builder->countAllResults(false); // 生成一个整数，比如 17

**$builder->countAll()**

该方法用于获取指定表的总行数，例如::

	echo $builder->countAll();  // 生成一个整数，比如 25

与 countAllResult 方法一样，该方法也会重置你在 ``select()`` 里设置的所有值，
如果你要保留它们，可以将第一个参数设置为 FALSE。

**************
查询分组
**************

查询分组可以让你生成用括号括起来的一组 WHERE 条件，
这能创造出非常复杂的 WHERE 子句，支持嵌套的条件组。
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

.. 注解:: 条件组必须要配对，确保每个 groupStart() 方法
    都有一个 groupEnd() 方法与之配对。

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

**$builder->groupHavingStart()**

开始一个新的条件组，为查询中的 HAVING 条件添加一个左括号。

**$builder->orGroupHavingStart()**

开始一个新的条件组，为查询中的 HAVING 条件添加一个左括号，并在前面加上 "OR" 。

**$builder->notGroupHavingStart()**

开始一个新的条件组，为查询中的 HAVING 条件添加一个左括号，并在前面加上 "NOT" 。

**$builder->orNotGroupHavingStart()**

开始一个新的条件组，为查询中的 HAVING 条件添加一个左括号，并在前面加上 "OR NOT" 。

**$builder->groupHavingEnd()**

结束当前的条件组，为查询中的 HAVING 条件添加一个右括号。

**************
插入数据
**************

**$builder->insert()**

该方法根据你提供的数据生成一条 INSERT 语句并执行，
它的参数是一个 **数组** 或一个 **对象** ，
下面是使用数组的例子::

	$data = array(
		'title' => 'My title',
		'name'  => 'My Name',
		'date'  => 'My date'
	);

	$builder->insert($data);
	// 生成: INSERT INTO mytable (title, name, date) VALUES ('My title', 'My name', 'My date')

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
	// 生成: INSERT INTO mytable (title, content, date) VALUES ('My Title', 'My Content', 'My Date')

第一个参数为要插入的数据，是个对象。

.. 注解:: 所有数据会被自动转义，生成安全的查询语句。

**$builder->ignore()**

该方法根据你提供的数据生成一条 INSERT IGNORE 语句并执行，
如果已经存在相同主键，该数据不会被插入。
你可以给该方法传入一个可选参数，类型是 **boolean** 。
下面是使用数组的例子::

	$data = [
		'title' => 'My title',
		'name'  => 'My Name',
		'date'  => 'My date'
	];

	$builder->ignore(true)->insert($data);
	// 生成: INSERT OR IGNORE INTO mytable (title, name, date) VALUES ('My title', 'My name', 'My date')


**$builder->getCompiledInsert()**

该方法和 $builder->insert() 方法一样编译插入查询，但是 *并不执行* 。
此方法只是将 SQL 查询作为字符串返回。

例如::

	$data = array(
		'title' => 'My title',
		'name'  => 'My Name',
		'date'  => 'My date'
	);

	$sql = $builder->set($data)->getCompiledInsert('mytable');
	echo $sql;

	// 生成字符串: INSERT INTO mytable (`title`, `name`, `date`) VALUES ('My title', 'My name', 'My date')

第二个参数用于设置是否重置查询（默认会重置，如 $builder->insert() 方法一样）::

	echo $builder->set('title', 'My Title')->getCompiledInsert('mytable', FALSE);

	// 生成字符串: INSERT INTO mytable (`title`) VALUES ('My Title')

	echo $builder->set('content', 'My Content')->getCompiledInsert();

	// 生成字符串: INSERT INTO mytable (`title`, `content`) VALUES ('My Title', 'My Content')

最值得注意的是，上例第二个查询并没有用到 **$builder->from()** 方法， 
也没有为查询指定表名参数。因为这个查询没有被可重置值的 **$builder->insert()** 方法执行，或是使用 **$builder->resetQuery()** 方法直接重置。

.. 注解:: 这个方法不支持批量插入。

**$builder->insertBatch()**

该方法根据你提供的数据生成一条 INSERT 语句并执行，
它的参数可以是一个 **数组** 或一个 **对象** ，
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
	// 生成: INSERT INTO mytable (title, name, date) VALUES ('My title', 'My name', 'My date'),  ('Another title', 'Another name', 'Another date')

第一个参数为要插入的数据，是个二维数组。

.. 注解:: 所有数据会被自动转义，生成安全的查询语句。

*************
更新数据
*************

**$builder->replace()**

该方法用于执行一条 REPLACE 语句，基本上是（可选）DELETE + INSERT 的 SQL 标准，
使用 *PRIMARY* 和 *UNIQUE* 键作为决定因素。
在我们的例子中，它可以使你免于实现各种不同逻辑的组合：
``select()`` ， ``update()`` ， ``delete()`` 和 ``insert()`` 。

例如::

	$data = array(
		'title' => 'My title',
		'name'  => 'My Name',
		'date'  => 'My date'
	);

	$builder->replace($data);

	// Executes: REPLACE INTO mytable (title, name, date) VALUES ('My title', 'My name', 'My date')

上面的例子中，我们假设 *title* 字段是主键，那么如果我们数据库里有一行
包含 'My title' 为标题的数据，那行将被删除并被我们的新数据取代。

也可以使用 ``set()`` 方法，而且所有字段都被自动转义，正如 ``insert()`` 方法一样。

**$builder->set()**

该方法可以设置 insert 或 update 用到的数据。

**它可以用来代替直接将数据数组传递给 insert 或 update 方法:**

::

	$builder->set('name', $name);
	$builder->insert();  // 生成: INSERT INTO mytable (`name`) VALUES ('{$name}')

如果你多次调用该方法，它会正确组装出 insert 或 update 语句来::

	$builder->set('name', $name);
	$builder->set('title', $title);
	$builder->set('status', $status);
	$builder->insert();

**set()** 将方法也接受可选的第三个参数（``$escape``），
如果设置为 FALSE ，数据将不会自动转义。
为了说明区别，这里有一个带转义的 ``set()`` 方法和不带转义的例子。

::

	$builder->set('field', 'field+1', FALSE);
	$builder->where('id', 2);
	$builder->update(); // 生成 UPDATE mytable SET field = field+1 WHERE `id` = 2

	$builder->set('field', 'field+1');
	$builder->where('id', 2);
	$builder->update(); // 生成 UPDATE `mytable` SET `field` = 'field+1' WHERE `id` = 2

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

该方法根据你提供的数据生成更新字符串并执行，它的参数是一个 **数组** 
或一个 **对象** ，下面是使用数组的例子::

	$data = array(
		'title' => $title,
		'name'  => $name,
		'date'  => $date
	);

	$builder->where('id', $id);
	$builder->update($data);
	// 生成:
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
	// 生成:
	//
	// UPDATE `mytable`
	// SET `title` = '{$title}', `name` = '{$name}', `date` = '{$date}'
	// WHERE id = `$id`

.. 注解:: 所有数据会被自动转义，生成安全的查询语句。

你应该注意到用 $builder->where() 方法可以为你设置 WHERE 子句。
你可以选择性的将这些（条件）信息直接以字符串传入 update 方法::

	$builder->update($data, "id = 4");

或者使用一个数组::

	$builder->update($data, array('id' => $id));

当执行更新操作时，你还可以使用上面介绍的 $builder->set() 方法。

**$builder->updateBatch()**

该方法根据你提供的数据生成一条 UPDATE 语句并执行，它的参数是一个 **数组** 
或一个 **对象** ，下面是使用数组的例子::

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

	// 生成:
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

.. 注解:: 所有数据会被自动转义，生成安全的查询语句。

.. 注解:: 由于该方法的内部实现，在这之后调用 ``affectedRows()`` 方法的返回值可能不正确，替代办法是用 ``updateBatch()`` 的返回值，表示受影响的行数。

**$builder->getCompiledUpdate()**

该方法和 ``$builder->getCompiledInsert()`` 方法完全一样，
除了生成的 SQL 语句是 UPDATE 而不是 INSERT。

查看 `$builder->getCompiledInsert()` 方法的文档获取更多信息。

.. note:: 该方法不支持批量更新。

*************
删除数据
*************

**$builder->delete()**

该方法生成删除SQL语句并执行。

::

	$builder->delete(array('id' => $id));  // 生成: // DELETE FROM mytable  // WHERE id = $id

第一个参数为 where 子句。你也可以使用 where() 或 or_where() 方法替代第一个参数::

	$builder->where('id', $id);
	$builder->delete();

	// 生成:
	// DELETE FROM mytable
	// WHERE id = $id

如果你想删除一个表中的全部数据，可以使用 truncate() 或 emptyTable() 方法。

**$builder->emptyTable()**

该方法生成删除 SQl 语句并执行::

	  $builder->emptyTable('mytable'); // 生成: DELETE FROM mytable

**$builder->truncate()**

该方法生截断 SQL 语句并执行。

::

	$builder->truncate();

	// 生成:
	// TRUNCATE mytable

.. 注解:: 如果 TRUNCATE 命令不可用，truncate() 方法将执行 "DELETE FROM table"。

**$builder->getCompiledDelete()**

该方法和 ``$builder->getCompiledInsert()`` 方法完全一样，
除了生成的 SQL 语句是 DELETE 而不是 INSERT。

查看 $builder->getCompiledInsert() 方法的文档获取更多信息。

***************
链式方法
***************

通过将多个方法连接在一起，链式方法可以大大简化你的语法。感受一下这个例子::

	$query = $builder->select('title')
			 ->where('id', $id)
			 ->limit(10, 20)
			 ->get();

.. _ar-caching:

***********************
重置查询构造器
***********************

**$builder->resetQuery()**

该方法使你可以重置查询构造器，而无需先执行例如 $builder->get() 
或 $builder->insert() 这类方法。

当你要用查询构造器生成 SQL 语句（如： ``$builder->getCompiledSelect()`` ）， 
之后再执行它，这种情况下，不重置查询构造器很有用::

	// 注意 get_compiled_select 方法的第二个参数为 FALSE
    $sql = $builder->select(['field1','field2'])
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
类库参考
***************

.. php:class:: \CodeIgniter\Database\BaseBuilder

	.. php:method:: resetQuery()

		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		重置当前查询构造器状态。当你需要构建一个可在某些情况下取消的查询时有用。

	.. php:method:: countAllResults([$reset = TRUE])

		:param	bool	$reset: 是否重置 SELECT 的值
		:returns:	查询结果中的行数
		:rtype:	int

		生成特定于平台的查询语句，用于计数查询构造器返回的行数。

	.. php:method:: countAll([$reset = TRUE])

		:param	bool	$reset: 是否重置 SELECT 的值
		:returns:	查询结果中的行数
		:rtype:	int

		生成特定于平台的查询语句，用于计数查询构造器返回的行数。

	.. php:method:: get([$limit = NULL[, $offset = NULL]])

		:param	int	$limit: LIMIT 子句
		:param	int	$offset: OFFSET 子句
		:returns:	\CodeIgniter\Database\ResultInterface instance (方法链)
		:rtype:	\CodeIgniter\Database\ResultInterface

		基于已经调用过的查询构造器方法，编译执行 SELECT 查询。

	.. php:method:: getWhere([$where = NULL[, $limit = NULL[, $offset = NULL]]])

		:param	string	$where: WHERE 子句
		:param	int	$limit: LIMIT 子句
		:param	int	$offset: OFFSET 子句
		:returns:	\CodeIgniter\Database\ResultInterface instance (方法链)
		:rtype:	\CodeIgniter\Database\ResultInterface

		与 ``get()`` 相同，但也允许直接添加 WHERE 。

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

	.. php:method:: selectCount([$select = ''[, $alias = '']])

		:param	string	$select: 用于计算记录总和的字段
		:param	string	$alias: 结果值名称的别名
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 SELECT COUNT(field) 子句。

	.. php:method:: distinct([$val = TRUE])

		:param	bool	$val: 预期的 "distinct" 标志值
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		设置一个标志， 告诉查询构建器给 SELECT 部分添加 DISTINCT 子句。

	.. php:method:: from($from[, $overwrite = FALSE])

		:param	mixed	$from: Table name(s); 字符串或数组
		:param	bool	$overwrite: 是否移除第一个设置的表？
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		指定查询的 FROM 子句。

	.. php:method:: join($table, $cond[, $type = ''[, $escape = NULL]])

		:param	string	$table: 要 join 的表名
		:param	string	$cond: JOIN ON 条件
		:param	string	$type: JOIN 类型
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

		生成查询的 WHERE 部分，用 'AND' 分隔多个调用。

	.. php:method:: orWhere($key[, $value = NULL[, $escape = NULL]])

		:param	mixed	$key: 要比较的字段名称或关联数组
		:param	mixed	$value: 如果是单个键，则与此值相比
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance
		:rtype:	object

		生成查询的 WHERE 部分，用 'OR' 分隔多个调用。

	.. php:method:: orWhereIn([$key = NULL[, $values = NULL[, $escape = NULL]]])

		:param	string	$key: 要搜索的字段
		:param	array|Closure   $values: 目标值的数组，或子查询的匿名函数
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance
		:rtype:	object

		生成一个 WHERE 字段 IN('item', 'item') SQL 查询，多个用 'OR' 连接。

	.. php:method:: orWhereNotIn([$key = NULL[, $values = NULL[, $escape = NULL]]])

		:param	string	$key: 要搜索的字段
		:param	array|Closure   $values: 目标值的数组，或子查询的匿名函数
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance
		:rtype:	object

		生成一个 WHERE 字段 NOT IN('item', 'item') SQL 查询，多个用 'OR' 连接。

	.. php:method:: whereIn([$key = NULL[, $values = NULL[, $escape = NULL]]])

		:param	string	$key: 要检查的字段的名称
		:param	array|Closure   $values: 目标值的数组，或子查询的匿名函数
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance
		:rtype:	object

		生成一个 WHERE 字段 IN('item', 'item') SQL 查询，多个用 'AND' 连接。

	.. php:method:: whereNotIn([$key = NULL[, $values = NULL[, $escape = NULL]]])

		:param	string	$key: 要检查的字段的名称
		:param	array|Closure   $values: 目标值的数组，或子查询的匿名函数
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance
		:rtype:	object

		生成一个 WHERE 字段 NOT IN('item', 'item') SQL 查询，多个用 'AND' 连接。

	.. php:method:: groupStart()

		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		启动组表达式，使用 AND 连接其中的条件。

	.. php:method:: orGroupStart()

		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		启动组表达式，使用 OR 连接其中的条件。

	.. php:method:: notGroupStart()

		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		启动组表达式，使用 AND NOT 连接其中的条件。

	.. php:method:: orNotGroupStart()

		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		启动组表达式，使用 OR NOT 连接其中的条件。

	.. php:method:: groupEnd()

		:returns:	BaseBuilder instance
		:rtype:	object

		完成一个组表达式。

	.. php:method:: like($field[, $match = ''[, $side = 'both'[, $escape = NULL[, $insensitiveSearch = FALSE]]]])

		:param	string	$field: 字段名
		:param	string	$match: 匹配的文本部分
		:param	string	$side: 将 '%' 通配符放在表达式的哪一侧
		:param	bool	$escape: 是否转义值和标识符
		:param	bool    $insensitiveSearch: 是否强制大小写不敏感检索
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 LIKE 子句，用 AND 分隔多个调用。

	.. php:method:: orLike($field[, $match = ''[, $side = 'both'[, $escape = NULL[, $insensitiveSearch = FALSE]]]])

		:param	string	$field: 字段名
		:param	string	$match: 匹配的文本部分
		:param	string	$side: 将 '%' 通配符放在表达式的哪一侧
		:param	bool	$escape: 是否转义值和标识符
		:param	bool    $insensitiveSearch: 是否强制大小写不敏感检索
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 LIKE 子句，用 OR 分隔多个调用。

	.. php:method:: notLike($field[, $match = ''[, $side = 'both'[, $escape = NULL[, $insensitiveSearch = FALSE]]]])

		:param	string	$field: 字段名
		:param	string	$match: 匹配的文本部分
		:param	string	$side: 将 '%' 通配符放在表达式的哪一侧
		:param	bool	$escape: 是否转义值和标识符
		:param	bool    $insensitiveSearch: 是否强制大小写不敏感检索
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 NOT LIKE 子句，用 AND 分隔多个调用。

	.. php:method:: orNotLike($field[, $match = ''[, $side = 'both'[, $escape = NULL[, $insensitiveSearch = FALSE]]]])

		:param	string	$field: 字段名
		:param	string	$match: 匹配的文本部分
		:param	string	$side: 将 '%' 通配符放在表达式的哪一侧
		:param	bool	$escape: 是否转义值和标识符
		:param	bool    $insensitiveSearch: 是否强制大小写不敏感检索
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 NOT LIKE 子句，用 OR 分隔多个调用。

	.. php:method:: having($key[, $value = NULL[, $escape = NULL]])

		:param	mixed	$key: 标识符（字符串）或 field/value 对的关联数组
		:param	string	$value: 如果 $key 是标识符，则寻求此值
		:param	string	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 HAVING 子句，用 AND 分隔多个调用。

	.. php:method:: orHaving($key[, $value = NULL[, $escape = NULL]])

		:param	mixed	$key: 标识符（字符串）或 field/value 对的关联数组
		:param	string	$value: 如果 $key 是标识符，则寻求此值
		:param	string	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 HAVING 子句，用 OR 分隔多个调用。

	.. php:method:: orHavingIn([$key = NULL[, $values = NULL[, $escape = NULL]]])

		:param	string	        $key: 要检索的字段名
		:param	array|Closure   $values: 目标值的数组，或子查询的匿名函数
		:param	bool	        $escape: 是否转义值和标识符
		:returns:	BaseBuilder instance
		:rtype:	object

		向查询添加 HAVING 字段 IN('item', 'item') 子句，多个用 OR 连接。

	.. php:method:: orHavingNotIn([$key = NULL[, $values = NULL[, $escape = NULL]]])

		:param	string	        $key: 要检索的字段名
		:param	array|Closure   $values: 目标值的数组，或子查询的匿名函数
		:param	bool	        $escape: 是否转义值和标识符
		:returns:	BaseBuilder instance
		:rtype:	object

		向查询添加 HAVING 字段 NOT IN('item', 'item') 子句，多个用 OR 连接。

	.. php:method:: havingIn([$key = NULL[, $values = NULL[, $escape = NULL]]])

		:param	string	        $key: 要检索的字段名
		:param	array|Closure   $values: 目标值的数组，或子查询的匿名函数
		:param	bool	        $escape: 是否转义值和标识符
		:returns:	BaseBuilder instance
		:rtype:	object

		向查询添加 HAVING 字段 IN('item', 'item') 子句，多个用 AND 连接。

	.. php:method:: havingNotIn([$key = NULL[, $values = NULL[, $escape = NULL]]])

		:param	string	        $key: 要检索的字段名
		:param	array|Closure   $values: 目标值的数组，或子查询的匿名函数
		:param	bool	        $escape: 是否转义值和标识符
		:returns:	BaseBuilder instance
		:rtype:	object

		向查询添加 HAVING 字段 NOT IN('item', 'item') 子句，多个用 AND 连接。

	.. php:method:: havingLike($field[, $match = ''[, $side = 'both'[, $escape = NULL[, $insensitiveSearch = FALSE]]]])

		:param	string	$field: 字段名
		:param	string	$match: 匹配的文本部分
		:param	string	$side: 将 '%' 通配符放在表达式的哪一侧
		:param	bool	$escape: 是否转义值和标识符
		:param	bool    $insensitiveSearch: 是否强制大小写不敏感检索
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询的 HAVING 部分添加 LIKE 子句，用 AND 分隔多个调用。

	.. php:method:: orHavingLike($field[, $match = ''[, $side = 'both'[, $escape = NULL[, $insensitiveSearch = FALSE]]]])

		:param	string	$field: 字段名
		:param	string	$match: 匹配的文本部分
		:param	string	$side: 将 '%' 通配符放在表达式的哪一侧
		:param	bool	$escape: 是否转义值和标识符
		:param	bool    $insensitiveSearch: 是否强制大小写不敏感检索
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询的 HAVING 部分添加 LIKE 子句，用 OR 分隔多个调用。

	.. php:method:: notHavingLike($field[, $match = ''[, $side = 'both'[, $escape = NULL[, $insensitiveSearch = FALSE]]]])

		:param	string	$field: 字段名
		:param	string	$match: 匹配的文本部分
		:param	string	$side: 将 '%' 通配符放在表达式的哪一侧
		:param	bool	$escape: 是否转义值和标识符
		:param	bool    $insensitiveSearch: 是否强制大小写不敏感检索
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询的 HAVING 部分添加 NOT LIKE 子句，用 AND 分隔多个调用。

	.. php:method:: orNotHavingLike($field[, $match = ''[, $side = 'both'[, $escape = NULL[, $insensitiveSearch = FALSE]]]])

		:param	string	$field: 字段名
		:param	string	$match: 匹配的文本部分
		:param	string	$side: 将 '%' 通配符放在表达式的哪一侧
		:param	bool	$escape: 是否转义值和标识符
		:param	bool    $insensitiveSearch: 是否强制大小写不敏感检索
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询的 HAVING 部分添加 NOT LIKE 子句，用 OR 分隔多个调用。

	.. php:method:: havingGroupStart()

		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		启动 HAVING 子句的组表达式，使用 AND 连接其中的条件。

	.. php:method:: orHavingGroupStart()

		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		启动 HAVING 子句的组表达式，使用 OR 连接其中的条件。

	.. php:method:: notHavingGroupStart()

		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		启动 HAVING 子句的组表达式，使用 AND NOT 连接其中的条件。

	.. php:method:: orNotHavingGroupStart()

		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		启动 HAVING 子句的组表达式，使用 OR NOT 连接其中的条件。

	.. php:method:: havingGroupEnd()

		:returns:	BaseBuilder instance
		:rtype:	object

		完成一个 HAVING 子句的组表达式。

	.. php:method:: groupBy($by[, $escape = NULL])

		:param	mixed	$by: 根据字段分组; 字符串或数组
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		向查询添加 GROUP BY 子句。

	.. php:method:: orderBy($orderby[, $direction = ''[, $escape = NULL]])

		:param	string	$orderby: 根据字段排序
		:param	string	$direction: 要求的排序 - ASC ， DESC 或 RANDOM
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

		:param	mixed	$key: 字段名或 field/value 对的关联数组
		:param	string	$value: 字段值，如果 $key 是单个字段
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		添加 field/value 键值对，稍后用于传递给 ``insert()`` ， ``update()`` 或 ``replace()`` 。

	.. php:method:: insert([$set = NULL[, $escape = NULL]])

		:param	array	$set: field/value 对的关联数组
		:param	bool	$escape: 是否转义值和标识符
		:returns:	成功时为 TRUE，失败时为 FALSE
		:rtype:	bool

		编译并执行 INSERT 语句。

	.. php:method:: insertBatch([$set = NULL[, $escape = NULL[, $batch_size = 100]]])

		:param	array	$set: 要插入的数据
		:param	bool	$escape: 是否转义值和标识符
		:param	int	$batch_size: 要一次插入的行数
		:returns:	插入的行数或失败时的 FALSE
		:rtype:	mixed

		编译并执行批量的 ``INSERT`` 语句。

		.. 注解:: 当数据超过 ``$batch_size`` 行时，将执行多个 ``INSERT`` 查询，
		    每次尝试插入最多为 ``$batch_size`` 行。

	.. php:method:: setInsertBatch($key[, $value = ''[, $escape = NULL]])

		:param	mixed	$key: 字段名或 field/value 对应的关联数组
		:param	string	$value: 字段值，如果 $key 是单个字段
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		添加 field/value 键值对，稍后通过 ``insertBatch()`` 向一个表插入。

	.. php:method:: update([$set = NULL[, $where = NULL[, $limit = NULL]]])

		:param	array	$set: field/value 对应的关联数组
		:param	string	$where: WHERE 子句
		:param	int	$limit: LIMIT 子句
		:returns:	TRUE 为成功, FALSE 为失败
		:rtype:	bool

		编译并执行 UPDATE 语句。

	.. php:method:: updateBatch([$set = NULL[, $value = NULL[, $batch_size = 100]]])

		:param	array	$set: 字段名，或 field/value 对的关联数组
		:param	string	$value: 字段值，如果 $set 是单个字段
		:param	int	$batch_size: 在单个查询中分组的条件计数
		:returns:	更新的行数或失败时的 FALSE
		:rtype:	mixed

		编译并执行批量的 ``UPDATE`` 语句。

		.. 注解:: 当数据超过 ``$batch_size`` 行时，将执行多个 ``INSERT`` 查询，
		    每次最多处理 ``$batch_size`` 行。

	.. php:method:: setUpdateBatch($key[, $value = ''[, $escape = NULL]])

		:param	mixed	$key: 字段名，或 field/value 对的关联数组
		:param	string	$value: 字段值，如果 $key 是单个字段
		:param	bool	$escape: 是否转义值和标识符
		:returns:	BaseBuilder instance (方法链)
		:rtype:	BaseBuilder

		添加 field/value 键值对，稍后通过 ``updateBatch()`` 更新一个表。

	.. php:method:: replace([$set = NULL])

		:param	array	$set: field/value 对应的关联数组
		:returns:	TRUE 为成功, FALSE 为失败
		:rtype:	bool

		编译并执行 REPLACE 语句。

	.. php:method:: delete([$where = ''[, $limit = NULL[, $reset_data = TRUE]]])

		:param	string	$where: WHERE 子句
		:param	int	$limit: LIMIT 子句
		:param	bool	$reset_data: TRUE 会重置查询 "write" 子句
		:returns:	BaseBuilder instance (方法链) 或者失败时为 FALSE
		:rtype:	mixed

		编译并执行 DELETE 查询。

    .. php:method:: increment($column[, $value = 1])

        :param string $column: 要递增的列的名称
        :param int    $value:  要给列增加的数值

		给一个字段增加指定量的数值，如果该字段不是数字型字段，比如如 VARCHAR ，
		它可能会被新的 $value 值替换。

    .. php:method:: decrement($column[, $value = 1])

        :param string $column: 要减少的列的名称
        :param int    $value:  要给列减少的数值

		给一个字段减去指定量的数值，如果该字段不是数字型字段，比如如 VARCHAR ，
		它可能会被新的 $value 值替换。

	.. php:method:: truncate()

		:returns:	TRUE 为成功, FALSE 为失败
		:rtype:	bool

		在表上执行 TRUNCATE 语句。

		.. note:: 如果所用的数据库平台不支持 TRUNCATE ，将使用 DELETE 语句替代。

	.. php:method:: emptyTable()

		:returns:	TRUE 为成功, FALSE 为失败
		:rtype:	bool

		通过 DELETE 语句删除表中所有记录。

	.. php:method:: getCompiledSelect([$reset = TRUE])

		:param	bool	$reset: 是否重置当前查询构造器（QB）的值
		:returns:	已编译的 SQL 语句为字符串
		:rtype:	string

		编译 SELECT 语句并将其作为字符串返回。

	.. php:method:: getCompiledInsert([$reset = TRUE])

		:param	bool	$reset: 是否重置当前查询构造器（QB）的值
		:returns:	已编译的 SQL 语句为字符串
		:rtype:	string

		编译 INSERT 语句并将其作为字符串返回。

	.. php:method:: getCompiledUpdate([$reset = TRUE])

		:param	bool	$reset: 是否重置当前查询构造器（QB）的值
		:returns:	已编译的 SQL 语句为字符串
		:rtype:	string

		编译 UPDATE 语句并将其作为字符串返回。

	.. php:method:: getCompiledDelete([$reset = TRUE])

		:param	bool	$reset: 是否重置当前查询构造器（QB）的值
		:returns:	已编译的 SQL 语句为字符串
		:rtype:	string

		编译 DELETE 语句并将其作为字符串返回。
