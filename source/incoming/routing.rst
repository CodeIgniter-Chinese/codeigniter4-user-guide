###########
URI 路由
###########

.. contents::
    :local:
    :depth: 2

一般情况下，一个 URL 字符串和它对应的控制器中类和方法是一一对应的关系。 URL 中的每一段通常遵循下面的规则::

    example.com/class/function/id/

但是有时候，你可能想改变这种映射关系，调用一个不同的类或方法，而不是 URL 中对应的那样。

例如，假设你希望你的 URL 变成下面这样::

    example.com/product/1/
    example.com/product/2/
    example.com/product/3/
    example.com/product/4/

URL 的第二段通常表示方法的名称，但在上面的例子中，第二段是一个商品 ID ， 为了实现这一点，CodeIgniter 允许你重新定义 URL 的处理流程。

设置你自己的路由规则
==============================

路由规则定义在 **app/config/Routes.php** 文件中。你将会在其中看到，该文件创建了一个RouteCollection类的实例，这一实例允许你定义自己的路由规则。
路由中可使用通配符和正则表达式。

路由通常将URI置于左侧，而将控制器和对应的方法以及任何可能存在的，并需要传递给控制器的参数映射在右侧。控制器与其方法的列出形式就像你调用一个类的静态方法一样，
用双冒号来分隔一个充分命名空间化形式的类与其方法，例如 ``Users::list``。如果这个方法需要被传递参数，这些参数应被以正斜杠分割的形式在方法名后列出，如::

	// 调用 $Users->list()
	Users::list
	// 调用 $Users->list(1, 23)
	Users::list/1/23

通配符
============

一个典型的路由规则看上去就像这样::

    $routes->add('product/(:num)', 'App\Catalog::productLookup');

在一个路由中，第一个参数包含需要被匹配到的URI，而第二个参数包含着这个路由应被定位到的目标位置。在上述例子中，当单词"product"在URL的第一个分段中被发现，
同时在第二个分段中出现了一个数字，那么 ``App\Catalog`` 类与 ``productLookup`` 方法就会调用。

通配符是一系列简单的正则表达式类型的字符串。在路由处理过程中，通配符会被正则表达式的值所取代，故而这些通配符主要是为了可读性而设计的。

当在你的路由处理过程中，可使用如下通配符:

* **(:any)** 将会从当前位置开始到URI结束，匹配任何字符。这一通配符可能会包括多个URI分段。
* **(:segment)** 将会匹配除了斜杠(/)以外的任何字符，从而将匹配结果限制在一个单独的分段中。
* **(:num)** 将会匹配任何整数。
* **(:alpha)** 将会匹配任何英文字母字符。
* **(:alphanum)** 将会匹配任何英文字母或整数，或者是这两者的组合。
* **(:hash)** 与 **:segment** 相同，但可用于方便地查看那个路由正在使用哈希id(参照 :doc:`Model </models/model>` )。

.. note:: 因为 **{locale}** 是一个系统保留关键词，用于 :doc:`localization </outgoing/localization>` ，所以不可用于通配符或路由的其他部分。

示例
========

以下是一些路由示例::

	$routes->add('journals', 'App\Blogs');

一个第一个分段包含有单词"journals"的URL将会被映射于 ``App\Blogs`` 类，这个类的默认方法通常将会是 ``index()``::

	$routes->add('blog/joe', 'Blogs::users/34');

一个包含有 "blog/joe" 的分段的URL将会被映射于 ``\Blogs`` 类和 ``users`` 方法，而其ID参数将会被置为34::

	$routes->add('product/(:any)', 'Catalog::productLookup');

一个第一个分段为"product"，并且第二个分段是任意字符的URl，将会被映射于 ``\Catalog`` 类的 ``productLookup`` 方法::

	$routes->add('product/(:num)', 'Catalog::productLookupByID/$1';

一个第一个分段为"product"，并且第二个分段是数字的URl，将会被映射于 ``\Catalog`` 类的 ``productLookup`` 方法，并将这一数字传递为方法的一个变量参数。

.. important:: 尽管 ``add()`` 方法是相当方便的，我们还是推荐使用基于HTTP动词的路由结构，如下所述，并且这也更为安全。与此同时，这样也会带来轻微的性能提升，因为只有匹配当前请求方法的路由会被保存，从而在搜索路由时会减少搜索次数。

自定义通配符
===================

你也可以在路由文件中创建自己的通配符从而实现用户体验和可读性的定制需求。

你可以使用 ``addPlaceholder`` 方法来增加新的通配符。第一个参数是一个被用来作为通配符的字符串，第二个是该通配符应当被替换成的正则表达式。
这一方法操作需要在你增加路由之前被调用::

	$routes->addPlaceholder('uuid', '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}');
	$routes->add('users/(:uuid)', 'Users::show/$1');

正则表达式
===================

如果你更倾向于使用正则表达式的话，也可以用它来定义路由规则。允许任何有效的正则表达式，例如反向引用。

.. important:: Note:如果你使用逆向引用，你需要使用美元符号代替双斜线语法。一个典型的使用正则表达式的路由规则看起来像下面这样::

	$routes->add('products/([a-z]+)/(\d+)', 'Products::show/$1/id_$2');

上例中，一个类似于 products/shirts/123 这样的 URL 将会重定向到 ``Products`` 控制器的 ``show`` 方法。
并且将原来的第一个第二个URI分段作为参数传递给它。通过正则表达式，你也可以捕获一个带有斜杠（'/'）的分段，而通常来说
斜杠是用于多个分段时间的分隔符。

例如，当一个用户访问你的 Web 应用中的某个受密码保护的页面时，如果他没有 登陆，会先跳转到登陆页面，你希望在他们在成功登陆后重定向回刚才那个页面， 那么这个例子会很有用::

	$routes->add('login/(.+)', 'Auth::login/$1');

对于诸位虽然不熟悉正则表达式而又想了解更多关于正则表达式的，`regular-expressions.info <http://www.regular-expressions.info/>`_ 可能是一个不错的起点。

.. important:: 注意：你也可以在你的路由规则中混用通配符和正则表达式。

闭包
========

你可以使用一个匿名函数，或者闭包，作为路由的映射目标位置。这一函数将会在用户访问指定URI时执行。
以上操作在执行小功能，或只是显示一个简单的视图时，是相当方便的::

    $routes->add('feed', function()
    {
        $rss = new RSSFeeder();
        return $rss->feed('general');
    });

映射多个路由
=======================

虽然add()方法非常简单易用，但是调用 ``map()`` 方法来同时处理多个路由通常更为方便。
你可以通过定义一个路由的数组，并将其作为 ``map()`` 方法的第一个参数的批量处理的方式，来取代每次都要用 ``add()`` 方法来添加所需要路由::

	$routes = [];
	$routes['product/(:num)']      = 'Catalog::productLookupById';
	$routes['product/(:alphanum)'] = 'Catalog::productLookupByName';

	$collection->map($routes);

重定向路由
==================

任何存在了足够长时间的网站都肯定存在移动过的页面。你可以通过 ``addRedirect()`` 方法来重定向需要跳转到其他路由的路由规则。
第一个参数是原有的路由的URI规则，第二个参数是新的URI，或者是一个命名路由的名称。第三个参数是随着重定向一起发送的状态码，
默认值 ``302`` ，这也是通常情况下用的比较多的，意味着暂时的重定向::

    $routes->add('users/profile', 'Users::profile', ['as' => 'profile']);

    // 重定向至命名路由
    $routes->addRedirect('users/about', 'profile');
    // 重定向至URI
    $routes->addRedirect('users/about', 'users/profile');

当页面加载时，若匹配到重定向路由，则用户将会在加载原有控制器之前被重定向到新页面。

分组路由
===============

你可以使用 ``group()`` 将你的路由分组并设定一个通用的名字。分组名将作为URI的一个分段，用于组内所有定义的路由之前。
这一方式可以帮助你在定义一大组有相同前缀的路由时，减少额外的打字输入，例如设置一个管理分组时::

	$routes->group('admin', function($routes)
	{
		$routes->add('users', 'Admin\Users::index');
		$routes->add('blog', 'Admin\Blog::index');
	});

如上，'users'和'blog'这些URI就会加上"amdin"的前缀，从而处理例如 ``/admin/users`` 和 ``/admin/blog`` 的URI。
如果你需要的话，同样也可以嵌套分组以便管理::

	$routes->group('admin', function($routes)
	{
		$routes->group('users', function($routes)
		{
			$routes->add('list', 'Admin\Users::list');
		});

	});

这将用于处理例如 ``admin/users/list`` 的URI。

如果你需要为一个分组指定指定选项，类似 `namespace <#assigning-namespace>`_ ，请在回调前使用::

	$routes->group('api', ['namespace' => 'App\API\v1'], function($routes)
	{
		$routes->resource('users');
	});

这将能够使得如同 ``/api/users/`` 一样resource的路由映射于 ``App\API\v1\Users`` 控制器上。
你也可以对一组路由使用一个特定的 `过滤器 <filers.html>`_ 。过滤器总是会在控制器的调用前或调用后运行，这一操作在认证或api日志时格外有用::

    $routes->group('api', ['filter' => 'api-auth'], function($routes)
    {
        $routes->resource('users');
    });

控制器的值必须与定义在 ``app/Config/Filters.php`` 中的一系列别名中的至少一个所匹配。

环境约束
========================

你可以设置一组在特定环境下运行的路由。这方便了你创建一组只有开发者在本地环境中可使用，而在测试和生产环境不可见的工具。
以上操作可通过 ``environment()`` 方法来实现。第一个参数是环境名。在这个闭包中的定义的所有路由，仅在当前环境下可访问::

	$routes->environment('development', function($routes)
	{
		$routes->add('builder', 'Tools\Builder::index');
	});

反向路由
===============

反向路由允许你定义一个链接与它需要查找的当前路由所需要使用的控制器和方法以及参数。这可以不需要改变程序代码而定义路由规则。通常用于视图内部以创建链接地址。

举例来说，如果你需要一个跳转到图片相册的路由，你可以使用 ``route_to()`` 辅助函数以获取当前应该使用的路由。
第一个参数是完整的控制器类名与方法名以双英文冒号（::）区分，就像你在写一条原生的路由规则的格式一样。其他所有需要传递给这个路由的参数都将在后面被传递::

	// 该路由定义为:
	$routes->add('users/(:id)/gallery(:any)', 'App\Controllers\Galleries::showUserGallery/$1/$2');

	// 生成对应连接到用户ID1：5，图片ID：12的指定URL
	// 生成:/users/15/gallery/12
	<a href="<?= route_to('App\Controllers\Galleries::showUserGallery', 15, 12) ?>">查看相册</a>

使用命名路由
==================

你可以为路由命名，从而提高系统健壮性（鲁棒性），这一操作可通过给一个路由命名从而在后面调用来实现。
即使路由定义改变了，所有在系统中通过 ``route_to`` 创建的的连接将仍旧可用并且不需要进行任何变动。
命名一个路由，通过与路由名一起传递 ``as`` 选项来实现::

    // 路由定义为:
    $routes->add('users/(:id)/gallery(:any)', 'Galleries::showUserGallery/$1/$2', ['as' => 'user_gallery');

    // 生成对应连接到用户ID1：5，图片ID：12的指定URL
	// 生成:/users/15/gallery/12
    <a href="<?= route_to('user_gallery', 15, 12) ?>">View Gallery</a>

这同样使得视图更具有可读性。

在路由中使用 HTTP 动词
==========================

还可以在你的路由规则中使用 HTTP 动词（请求方法），当你在创建 RESTFUL 应用时特别有用。
你可以使用所有标准的 HTTP 动词（GET、PUT、POST、DELETE等），每个动词都拥有自己对应的方法供你使用::

	$routes->get('products', 'Product::feature');
	$routes->post('products', 'Product::feature');
	$routes->put('products/(:num)', 'Product::feature');
	$routes->delete('products/(:num)', 'Product::feature');

你可以指定一个路由可以匹配多个动词，将其传递 ``match()`` 方法作为一个数组::

	$routes->match(['get', 'put'], 'products', 'Product::feature');

命令行专用的路由
========================

你可以使用 ``cli()`` 方法来创建命令行专用，浏览器不可访问的路由。
这一方法中创建crojobs(定时任务)或命令行工具时相当有效。
而基于HTTP动词的路由同样对于命令行也是不可访问的，除了通过 ``any()`` 方法创建的路由之外::

	$routes->cli('migrate', 'App\Database::migrate');

全局选项
==============
所有用于创建路由的方法（例如add, get, post, `resource <restful.html>`_ 等）都可以调用一个选项数组来修改已生成的路由或限制它们的规则。而这一数组 ``$options`` 就是这些方法的最后一个参数::

	$routes->add('from', 'to', $options);
	$routes->get('from', 'to', $options);
	$routes->post('from', 'to', $options);
	$routes->put('from', 'to', $options);
	$routes->head('from', 'to', $options);
	$routes->options('from', 'to', $options);
	$routes->delete('from', 'to', $options);
	$routes->patch('from', 'to', $options);
	$routes->match(['get', 'put'], 'from', 'to', $options);
	$routes->resource('photos', $options);
	$routes->map($array, $options);
	$routes->group('name', $options, function());

应用过滤器
----------------

你可以通过指定一个过滤器在控制器调用前或调用后运行的方式来改变指定路由的行为，这一操作通常在鉴权或API记录日志时非常有用::

    $routes->add('admin',' AdminController::index', ['filter' => 'admin-auth']);

过滤器的值必须至少匹配 ``app/Config/Filters.php`` 中的一个别名。
你也可以指定过滤器的 ``before()`` 和 ``after()`` 方法的参数::

    $routes->add('users/delete/(:segment)', 'AdminController::index', ['filter' => 'admin-auth:dual,noreturn']);

浏览 `Controller filters <filters.html>`_ 来获取更多有关设置筛选过滤器的信息。

指定命名空间
-------------------

尽管默认的命名空间会在生成的控制器前自动附加（如下），你也可以通过 ``namespace`` 选项来指定一个别的命名空间在选项数组中。
选项值应该与你想指定的命名空间一致::

    // 路由指定至 \Admin\Users::index()
	$routes->add('admin/users', 'Users::index', ['namespace' => 'Admin']);

新的命名空间仅应用于创建一个单独路由的方法调用中，例如get, post等。对于创建多个路由的方法，新的命名空间将会被附在所有被这个方法锁生成的路由之前，例如在 ``group()`` 中，所有的路由都是在闭包中生成的。

限制域名
-----------------

你可以通过给选项数组的"hostname"选项传一个域名作为值的形式来限制一组路由只在你的应用的特定域名或子域名下生效::

	$collection->get('from', 'to', ['hostname' => 'accounts.example.com']);

这个例子仅允许当前访问的路由在域名为"accounts.example.com"时生效，而在其主域名"example.com"下无法生效。

限制子域名
-------------------

当 ``subdomain`` 选项开启时，系统将会限制路由仅在此子域名生效。只有在访问该子域名时系统才会匹配这组路由规则::

	// 限制子域名为media.example.com
	$routes->add('from', 'to', ['subdomain' => 'media']);

你可以通过设置该选项值为星号(*)的方式来对所有子域名生效。当你访问的URL不匹配任何子域名时，这项路由将不会被匹配到::

	// 限制所有子域名访问
	$routes->add('from', 'to', ['subdomain' => '*']);

.. important:: 系统不是完美无缺的，所以在部署生产环境前需要在特定的子域名下进行测试。大多数域名都没有问题，但在一些边缘情况下，特别是某些域名本身中就含有点号(.)，而这个点号又不是拿来区分前缀或者后缀时，就可能会出错。

Offsetting the Matched Parameters
---------------------------------

你可以向后推移在路由中匹配到的参数的位置，通过在 ``offset`` 选项中传递任何数字值，该值指名了推移匹配的URI分段的数量。

这将会为开发API带来好处，当URI第一个分段是版本号时，同样可以用于第一个参数是一个语言标识（例如en，fr等，译者注）::

	$routes->get('users/(:num)', 'users/show/$1', ['offset' => 1]);

	// 创建:
	$routes['users/(:num)'] = 'users/show/$2';

（译者注：实质就是将匹配的位置向后推移，由于第一个分段的位置可能会被其他参数占用，所以通配符的位置需要后移，
例如/en/users/(:num)，这里/en/是第一个分段，不需要作为路由使用，所以(:num)实际上通过offset后移到了$2的位置。）

路由配置选项
============================

路由集合类提供了多个可影响到所有路由的选项配置，并可被修改以符合程序要求，这些选项可在 `/app/Config/Routes/php`` 文件的顶部被更改。

默认命名空间
-----------------

当匹配到了一个需要路由的控制器，路由将会为该控制器增加一个默认的命名空间。默认设置下，这个命名空间的值为空，从而每个每个路由都需要完全对应到的带有命名空间的控制器类名::

    $routes->setDefaultNamespace('');

    // 控制器为 \Users
    $routes->add('users', 'Users::index');

    // 控制器为 \Admin\Users
    $routes->add('users', 'Admin\Users::index');

如果你的控制器不是严格遵从命名空间的话，就没有更改的必要。如果你为控制器指定了命名空间，就可以通过更改默认命名空间的值来减少打字输入::

	$routes->setDefaultNamespace('App');

	// 控制器为 \App\Users
	$routes->add('users', 'Users::index');

	// 控制器为 \App\Admin\Users
	$routes->add('users', 'Admin\Users::index');

默认控制器
------------------

当用户直接访问你的站点的根路径时（例如example.com），所调用的控制器将会由 ``setDefaultController()`` 方法所设置的参数决定，除非有一个路由是显式声明过（默认控制器）。
这一方法的默认值是 ``Home`` ，对应的控制器是 ``/app/Controllers/Home.php`` ::


	// example.com 对应的路由是app/Controllers/Welcome.php
	$routes->setDefaultController('Welcome');

默认控制器同样也在找不到对应的路由规则，URI对应到控制器的对应目录下的情况下被用到。
例如有个用户访问了 ``example.com/admin`` ，如果有个控制器被命名为 ``/app/Controllers/admin/Home.php`` ，那么就被调用到。

默认方法
--------------

与默认控制器的设置类似，用于设置设置默认方法。其应用场景是，找到了URI对应的控制器，但是URI分段对应不上控制器的方法时。默认值是 ``index`` ::

	$routes->setDefaultMethod('listAll');

在这个例子中，当用户访问example.com/products时，Products控制器存在，从而执行 ``Products::listAll()`` 方法。

连字符(-)转换
--------------------

从它的布尔值就能看出来这其实并不是一个路由，这个选项可以自动的将 URL 中的控制器和方法中的连字符（'-'）转换为下划线（'_'），当你需要这样时， 它可以让你少写很多路由规则。由于连字符不是一个有效的类名或方法名， 如果你不使用它的话，将会引起一个严重错误::

	$routes->setTranslateURIDashes(true);

仅使用定义路由
-----------------------

当指定的URI映射不到定义的路由时，系统将会将URI映射到如上所述的控制器和方法。
你可以通过设置 ``setAutoRoute()`` 选项为false的方式来关闭这一自动映射，并限制系统仅使用你定义的路由::

	$routes->setAutoRoute(false);

404 重载
------------

如果当前URI匹配不到对应的页面，系统将输出一个通用的404视图。你可以通过使用 ``set404Override()`` 方法，定义一个操作来改变以上行为。
这一方法的参数可以是一个合法的类/方法的组合，就如同你在任何路由或者闭包中定义的一样::

    // 将执行App\Errors类的show404方法
    $routes->set404Override('App\Errors::show404');

    // 将会输出一个自定义的视图
    $routes->set404Override(function()
    {
        echo view('my_errors/not_found.html');
    });
