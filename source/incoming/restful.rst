处理RESTful请求资源
#######################################################

.. contents::
    :local:
    :depth: 2

表现层状态转移(REST)是一种对于分布式应用的架构风格，最初由Roy Fielding在他的2000年博士论文 `Architectural Styles and
the Design of Network-based Software Architectures
<https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm>`_ 所提出。
上文可能读起来有些枯燥，你也可以参照Martin Fowler的 `Richardson Maturity Model <https://martinfowler.com/articles/richardsonMaturityModel.html>`_ 以获得更方便的教程。

对于REST的架构方式，比起大多数软件架构体系，大家理解和误解得会更多。
或者可以这样说，当你将Roy Fielding的原则越多得使用在一个架构中，你的应用就会变得越"RESTful"。

CodeIgniter实现了一种简易的方式来创建RESTful API从而访问你的资源，通过其自带的资源路由和 `ResourceController` （资源控制器）。

资源路由
============================================================

对单个资源，你可以通过 ``resource()`` 方法来创建一个方便的RESTful路由。这种方式可以创建五种对于操作资源的CRUD方式，最为常见的比如：
创建一个资源，更新一个已存在的资源，列出所有这类资源，获取一个单独资源以及删除一个单独的资源。第一个参数就是这个资源的名字::

    $routes->resource('photos');

    // 与以下方式等同:
    $routes->get('photos/new',             'Photos::new');
    $routes->post('photos',                'Photos::create');
    $routes->get('photos',                 'Photos::index');
    $routes->get('photos/(:segment)',      'Photos::show/$1');
    $routes->get('photos/(:segment)/edit', 'Photos::edit/$1');
    $routes->put('photos/(:segment)',      'Photos::update/$1');
    $routes->patch('photos/(:segment)',    'Photos::update/$1');
    $routes->delete('photos/(:segment)',   'Photos::delete/$1');

.. note:: 上述的排序方式是为了排版清晰起见，而实际上这些路由在RouteCollection中的创建顺序已经确保了路由可以被正确地解析。

.. important:: 路由是由它们所定义的顺序而进行匹配的，因此如果像上面一样，如果你有一个GET资源图片请求，类似 "photos/poll" 一样，那么show的请求路由会比get请求优先被匹配。为了解决这个问题，将get请求这行移到资源行的顶部，从而它可以被首先匹配。

第二个参数接受的是一个包含着用于修改生成路由方式的选项数组。尽管这些路由通过API调用的，且这里支持更多的请求类型，你还是可以通过传递“websafe”选项来生成update和delete请求类型来处理HTML表单::

    $routes->resource('photos', ['websafe' => 1]);

    // 将会创建以下的同等效应的路由:
    $routes->post('photos/(:segment)/delete', 'Photos::delete/$1');
    $routes->post('photos/(:segment)',        'Photos::update/$1');

更改所使用的控制器
--------------------------

你可以通过指定所使用的控制器，通过为 ``controller`` 选项传值::

	$routes->resource('photos', ['controller' =>'App\Gallery']);

	// 将会创建如下路由
	$routes->get('photos', 'App\Gallery::index');

更改使用的通配符
---------------------------

默认情况下，在需要资源ID时，我们需要使用 ``segment`` 占位符。你可以通过为 ``placeholder`` 选项传值一个新的字符串来实现这一操作::

	$routes->resource('photos', ['placeholder' => '(:id)']);

	// 将会创建如下路由:
	$routes->get('photos/(:id)', 'Photos::show/$1');

限制生成的路由
---------------------

你可以通过 ``only`` 选项来限制所生成的路由。这个选项的传值可以是一个数组或者是一个由逗号分隔的列表，其中包含着需要创建的类型名。而剩余的将会被忽略::

	$routes->resource('photos', ['only' => ['index', 'show']]);

反过来你也可以通过 ``except`` 选项来移除那些不使用的路由。该选项就在 ``only`` 后运行::

	$routes->resource('photos', ['except' => 'new,edit']);

合理的请求类型为: index, show, create, update, new, edit and delete.

资源控制器
============================================================

`ResourceController` 为开始你的RESTful API的构建提供了一个非常便利的起点，实现了上述列举的资源路由的请求类型。

继承或重载 `modelName` 和 `format` 属性，并实现你想要处理的请求类型::

	<?php namespace App\Controllers;

	use CodeIgniter\RESTful\ResourceController;

	class Photos extends ResourceController
	{

		protected $modelName = 'App\Models\Photos';
		protected $format    = 'json';

		public function index()
		{
			return $this->respond($this->model->findAll());
		}

                // ...
	}

上述路由结构如下::

    $routes->resource('photos');

表现层路由
============================================================

你可以使用 ``presenter()`` 方法来创建一个表现层路由，并分配给对应的资源控制器。
这将会为那些给你的资源返回视图的的控制器方法创建路由，或者处理从这些控制器所创建的视图里发送的表单请求。

由于表现层惯例是由一个通用控制器来处理，这个功能不是必需的。它的用法与一个资源路由类似::

    $routes->presenter('photos');

    // 与如下等同:
    $routes->get('photos/new',                'Photos::new');
    $routes->post('photos/create',            'Photos::create');
    $routes->post('photos',                   'Photos::create');   // alias
    $routes->get('photos',                    'Photos::index');
    $routes->get('photos/show/(:segment)',    'Photos::show/$1');
    $routes->get('photos/(:segment)',         'Photos::show/$1');  // alias
    $routes->get('photos/edit/(:segment)',    'Photos::edit/$1');
    $routes->post('photos/update/(:segment)', 'Photos::update/$1');
    $routes->get('photos/remove/(:segment)',  'Photos::remove/$1');
    $routes->post('photos/delete/(:segment)', 'Photos::update/$1');

.. note:: The ordering above is for clarity, whereas the actual order the routes are created in, in RouteCollection, ensures proper route resolution

You would not have routes for `photos` for both a resource and a presenter
controller. You need to distinguish them, for instance::

    $routes->resource('api/photo');
    $routes->presenter('admin/photos');


The second parameter accepts an array of options that can be used to modify the routes that are generated. 

Change the Controller Used
--------------------------

You can specify the controller that should be used by passing in the ``controller`` option with the name of
the controller that should be used::

	$routes->presenter('photos', ['controller' =>'App\Gallery']);

	// Would create routes like:
	$routes->get('photos', 'App\Gallery::index');

Change the Placeholder Used
---------------------------

By default, the ``segment`` placeholder is used when a resource ID is needed. You can change this by passing
in the ``placeholder`` option with the new string to use::

	$routes->presenter('photos', ['placeholder' => '(:id)']);

	// Generates routes like:
	$routes->get('photos/(:id)', 'Photos::show/$1');

Limit the Routes Made
---------------------

You can restrict the routes generated with the ``only`` option. This should be an array or comma separated list of method names that should
be created. Only routes that match one of these methods will be created. The rest will be ignored::

	$routes->presenter('photos', ['only' => ['index', 'show']]);

Otherwise you can remove unused routes with the ``except`` option. This option run after ``only``::

	$routes->presenter('photos', ['except' => 'new,edit']);

Valid methods are: index, show, new, create, edit, update, remove and delete.

ResourcePresenter
============================================================

The `ResourcePresenter` provides a convenient starting point for presenting views
of your resource, and processing data from forms in those views,
with methods that align to the resource routes above.

Extend it, over-riding the `modelName` property, and then
implement those methods that you want handled.::

	<?php namespace App\Controllers;

	use CodeIgniter\RESTful\ResourcePresenter;

	class Photos extends ResourcePresenter
	{

		protected $modelName = 'App\Models\Photos';

		public function index()
		{
			return view('templates/list',$this->model->findAll());
		}

                // ...
	}

The routing for this would be::

    $routes->presenter('photos');

Presenter/Controller Comparison
=============================================================

This table presents a comparison of the default routes created by `resource()`
and `presenter()` with their corresponding Controller functions.

================ ========= ====================== ======================== ====================== ======================
Operation        Method    Controller Route       Presenter Route          Controller Function    Presenter Function
================ ========= ====================== ======================== ====================== ======================
**New**          GET       photos/new             photos/new               ``new()``              ``new()``
**Create**       POST      photos                 photos                   ``create()``           ``create()``
Create (alias)   POST                             photos/create                                   ``create()``
**List**         GET       photos                 photos                   ``index()``            ``index()``
**Show**         GET       photos/(:segment)      photos/(:segment)        ``show($id = null)``   ``show($id = null)``
Show (alias)     GET                              photos/show/(:segment)                          ``show($id = null)``
**Edit**         GET       photos/(:segment)/edit photos/edit/(:segment)   ``edit($id = null)``   ``edit($id = null)``
**Update**       PUT/PATCH photos/(:segment)                               ``update($id = null)`` 
Update (websafe) POST      photos/(:segment)      photos/update/(:segment) ``update($id = null)`` ``update($id = null)``
**Remove**       GET                              photos/remove/(:segment)                        ``remove($id = null)``
**Delete**       DELETE    photos/(:segment)                               ``delete($id = null)`` 
Delete (websafe) POST                             photos/delete/(:segment) ``delete($id = null)`` ``delete($id = null)``
================ ========= ====================== ======================== ====================== ======================
