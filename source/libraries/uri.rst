*****************
使用 URI 类
*****************

CodeIngiter 为你在应用中使用 URI 类提供了一个面向对象的解决方案。使用这种方式可以轻易地确保结构始终准确，无论 URI 的复杂程度如何，也能将相对 URI 添加到现有应用中，并保证其可以被安全、准确地解析。

.. contents:: Page Contents


======================
创建 URI 实例
======================

就像创建一个普通类实例一样去创建一个 URI 实例::

	$uri = new \CodeIgniter\HTTP\URI();

或者，你可以使用 ``service()`` 方法来返回一个 URI 实例::

	$uri = service('uri');

当创建新实例的时候，你可以将完整或部分 URL 传递给构造函数，其将会被解析为相应的分段::

	$uri = new \CodeIgniter\HTTP\URI('http://www.example.com/some/path');
	$uri = service('uri', 'http://www.example.com/some/path');

当前 URI
---------------

很多时候，你真正想要的是一个表示着当前请求 URL 的对象。可以有两种不同的方式来获取。第一，直接从当前请求对象中提取。假设你所在的控制器已继承自 ``CodeIgniter\Controller``，可以这样做::

	$uri = $this->request->uri;

第二，你可以使用 **url_helper** 中的一个可用函数来获取::

	helper('url');
	$uri = current_url(true);

你必须在第一个参数中传递 ``true``,否则该函数将仅返回表示当前 URL 的字符串。

===========
URI 字符串
===========

很多时候，你真正想要的是得到一个表示 URI 的字符串。那直接将 URI 对象转换为字符串就可以了::

	$uri = current_url(true);
	echo (string)$uri;  // http://example.com

如果你知道 URI 的各个部分，同时还想确保其格式准确无误，你可以通过使用 URI 类的静态方法 ``createURIString()`` 来生成字符串::

	$uriString = URI::createURIString($scheme, $authority, $path, $query, $fragment);

	// Creates: http://exmample.com/some/path?foo=bar#first-heading
	echo URI::createURIString('http', 'example.com', 'some/path', 'foo=bar', 'first-heading');

=============
URI 的组成
=============

一旦你得到了一个 URI 实例，你就可以设置或检索这个 URI 的任意部分。本节将详细介绍这些部分的内容及如何使用它们。

Scheme
------

最常见的传输协议是 'http' 或 'https'，同时也支持如 'file', 'mailto' 等其他协议。
::

    $uri = new \CodeIgniter\HTTP\URI('http://www.example.com/some/path');

    echo $uri->getScheme(); // 'http'
    $uri->setScheme('https');

Authority
---------

许多 URI 内装载着被统称为 'authority' 的数个元素，包括用户信息，主机地址和端口号。你可以通过 ``getAuthority()`` 方法来获取一个包含了所有相关元素的字符串，也可以对独立的元素进行操作。
::

	$uri = new \CodeIgniter\HTTP\URI('ftp://user:password@example.com:21/some/path');

	echo $uri->getAuthority();  // user@example.com:21
	
默认情况下，因为你不希望向别人展示密码，所以它不会被显示出来。如你想展示密码，可以使用 ``showPassword()`` 方法。URI 实例会在你再次关掉显示之前一直保持密码部分地展示，所以你应在使用完成后立刻关闭它::

	echo $uri->getAuthority();  // user@example.com:21
	echo $uri->showPassword()->getAuthority();   // user:password@example.com:21

	// Turn password display off again.
	$uri->showPassword(false);

如果你不想显示端口，可以传递唯一参数 ``true``::

	echo $uri->getAuthority(true);  // user@example.com
	
.. Note:: 如果当前端口值是传输协议的默认端口值，那它将永远不会被显示。

Userinfo
--------

用户信息部分是在使用 FTP URI 时你看到的用户名和密码。当你能在 Authority 中得到它时，你也可以通过方法直接获取它::

	echo $uri->getUserInfo();   // user

默认情况下，它将不会展示密码，但是你可以通过 ``showPassword()`` 方法来重写它::

	echo $uri->showPassword()->getUserInfo();   // user:password
	$uri->showPassword(false);

Host
----

URI 的主机部分通常是 URL 的域名。可以通过 ``getHost()`` 和 ``setHost()`` 方法很容易地设置和获取::

	$uri = new \CodeIgniter\HTTP\URI('http://www.example.com/some/path');

	echo $uri->getHost();   // www.example.com
	echo $uri->setHost('anotherexample.com')->getHost();    // anotherexample.com

Port
----

端口值是一个在 0 到 65535 之间的整数。每个协议都会有一个与之关联的默认端口值。
::

	$uri = new \CodeIgniter\HTTP\URI('ftp://user:password@example.com:21/some/path');

	echo $uri->getPort();   // 21
	echo $uri->setPort(2201)->getPort(); // 2201

当使用 ``setPort()`` 方法时，端口值会在通过可用范围值检查后被设置。

Path
----

路径是站点自身的所有分段。如你所料，可以使用 ``getPath()`` 和 ``setPath()`` 方法来操作它::

	$uri = new \CodeIgniter\HTTP\URI('http://www.example.com/some/path');

	echo $uri->getPath();   // 'some/path'
	echo $uri->setPath('another/path')->getPath();  // 'another/path'

.. Note:: 以这种方式或类允许的其他方式设置 path 的时候，将会对危险字符进行编码，并移除点分段来确保安全。

Query
-----

查询变量可以通过类使用简单的字符串来调整。Query 的值通常只能设定为一个字符串。
::

	$uri = new \CodeIgniter\HTTP\URI('http://www.example.com?foo=bar');

	echo $uri->getQuery();  // 'foo=bar'
	$uri->setQuery('foo=bar&bar=baz');

.. Note:: Query 值不能包含片段，否则会抛出一个 InvalidArgumentException 异常。

你可以使用一个数组来设置查询值::

    $uri->setQueryArray(['foo' => 'bar', 'bar' => 'baz']);

``setQuery()`` 和 ``setQueryArray()`` 方法会重写已经存在的查询变量。你可以使用 ``addQuery()`` 方法在不销毁已存在查询变量的前提下追加值。第一个参数是变量名，第二个参数是值::

    $uri->addQuery('foo', 'bar');

**过滤查询值**

你可以对 ``getQuery()`` 方法传递一个选项数组来过滤查询返回值，使用关键字  *only* 或 *except*::

    $uri = new \CodeIgniter\HTTP\URI('http://www.example.com?foo=bar&bar=baz&baz=foz');

    // Returns 'foo=bar'
    echo $uri->getQuery(['only' => ['foo']);

    // Returns 'foo=bar&baz=foz'
    echo $uri->getQuery(['except' => ['bar']]);

这样只是对调用方法后的返回值进行更改。如果你需要对 URI 对象的查询值进行永久地更改，可以使用 ``stripQuery()`` 和 ``keepQuery()`` 方法来更改真实对象的查询变量::

    $uri = new \CodeIgniter\HTTP\URI('http://www.example.com?foo=bar&bar=baz&baz=foz');

    // Leaves just the 'baz' variable
    $uri->stripQuery('foo', 'bar');

    // Leaves just the 'foo' variable
    $uri->keepQuery('foo');

Fragment
--------

片段是 URL 的结尾部分，前面是英镑符号 (#)。在 HTML 中，它们是指向页面锚点的链接。媒体 URI 可以用其他各种方法来使用它们。
::

	$uri = new \CodeIgniter\HTTP\URI('http://www.example.com/some/path#first-heading');

	echo $uri->getFragment();   // 'first-heading'
	echo $uri->setFragment('second-heading')->getFragment();    // 'second-heading'

============
URI 分段
============

路径中，斜杠之间的每一节都是一个单独的分段。URI 类提供一个简单的方式去界定段值。路径最左侧的段为起始段 1。
::

	// URI = http://example.com/users/15/profile

	// Prints '15'
	if ($request->uri->getSegment(1) == 'users')
	{
		echo $request->uri->getSegment(2);
	}

你能得到总分段数量::

	$total = $request->uri->getTotalSegments(); // 3

最后，你能获取到一个包含着所有分段的数组::

	$segments = $request->uri->getSegments();

	// $segments =
	[
		0 => 'users',
		1 => '15',
		2 => 'profile'
	]
