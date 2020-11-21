###########
控制器
###########

控制器是你整个应用的核心，因为它们决定了 HTTP 请求将被如何处理。

.. contents::
    :local:
    :depth: 2


什么是控制器?
=====================

简而言之，一个控制器就是一个类文件，是以一种能够和 URI 关联在一起的方式来命名的。

考虑下面的 URI::

	example.com/index.php/blog/

上例中，CodeIgniter 将会尝试查询一个名为 Blog.php 的控制器并加载它。

**当控制器的名称和 URI 的第一段匹配上时，它将会被加载。**


让我们试试看：Hello World！
===============================


接下来你会看到如何创建一个简单的控制器，打开你的文本编辑器，新建一个文件 Blog.php ， 然后放入以下代码::

	<?php
	class Blog extends \CodeIgniter\Controller
	{
		public function index()
		{
			echo 'Hello World!';
		}
	}


然后将文件保存到 **/application/controllers/** 目录下。


.. important:: 文件名必须是大写字母开头，如：'Blog.php' 。


现在使用类似下面的 URL 来访问你的站点:：

	example.com/index.php/blog


如果一切正常，你将看到：:

	Hello World!

.. important:: 类名必须以大写字母开头。

这是有效的::

	<?php
	class Blog extends \CodeIgniter\Controller {

	}

这是 **无效** 的::

	<?php
	class blog extends \CodeIgniter\Controller {

	}


另外，一定要确保你的控制器继承了父控制器类，这样它才能使用父类的方法。


方法
=======


上例中，方法名为 ``index()`` 。"index" 方法总是在 URI 的 **第二段** 为空时被调用。 另一种显示 "Hello World" 消息的方法是::

	example.com/index.php/blog/index/


**URI 中的第二段用于决定调用控制器中的哪个方法。**

让我们试一下，向你的控制器添加一个新的方法::

	<?php
	class Blog extends \CodeIgniter\Controller {

		public function index()
		{
			echo 'Hello World!';
		}

		public function comments()
		{
			echo 'Look at this!';
		}
	}


现在，通过下面的 URL 来调用 comments 方法::

	example.com/index.php/blog/comments/

你应该能看到你的新消息了。


通过 URI 分段向你的方法传递参数
====================================

如果你的 URI 多于两个段，多余的段将作为参数传递到你的方法中。

例如，假设你的 URI 是这样::

	example.com/index.php/products/shoes/sandals/123


你的方法将会收到第三段和第四段两个参数（"sandals" 和 "123"）::

	<?php
	class Products extends \CodeIgniter\Controller {

		public function shoes($sandals, $id)
		{
			echo $sandals;
			echo $id;
		}
	}


.. important:: 如果你使用了 `URI 路由` ，传递到你的方法的参数将是路由后的参数。


定义默认控制器
=============================

CodeIgniter 可以设置一个默认的控制器，当 URI 没有分段参数时加载，例如当用户直接访问你网站的首页时。 打开 **application/config/routes.php** 文件，通过下面的参数指定一个默认的控制器::

	$routes->setDefaultController('Blog');


其中，“Blog”是你想加载的控制器类名，如果你现在通过不带任何参数的 index.php 访问你的站点，你将看到你的“Hello World”消息。

想要了解更多信息，请参阅 :doc:`./source/general/routing.rst` 部分文档。


重映射方法
======================


正如上文所说，URI 的第二段通常决定控制器的哪个方法被调用。CodeIgniter 允许你使用 ``_remap()`` 方法来重写该规则::

	public function _remap()
	{
		// Some code here...
	}


.. important:: 如果你的控制包含一个 _remap() 方法，那么无论 URI 中包含什么参数时都会调用该方法。 它允许你定义你自己的路由规则，重写默认的使用 URI 中的分段来决定调用哪个方法这种行为。


被重写的方法（通常是 URI 的第二段）将被作为参数传递到 ``_remap()`` 方法::

	public function _remap($method)
	{
		if ($method === 'some_method')
		{
			$this->$method();
		}
		else
		{
			$this->default_method();
		}
	}

方法名之后的所有其他段将作为 ``_remap()`` 方法的第二个参数，它是可选的。这个参数可以使用 PHP 的 call_user_func_array() 函数来模拟 CodeIgniter 的默认行为。

例如::

	public function _remap($method, ...$params)
	{
		$method = 'process_'.$method;
		if (method_exists($this, $method))
		{
			return $this->$method(...$params);
		}
		show_404();
	}


私有方法
===============

有时候你可能希望某些方法不能被公开访问，要实现这点，只要简单的将方法声明为 private 或 protected ， 这样这个方法就不能被 URL 访问到了。例如，如果你有一个下面这个方法::

	protected function utility()
	{
		// some code
	}


使用下面的 URL 尝试访问它，你会发现是无法访问的::

	example.com/index.php/blog/utility/


将控制器放入子目录中
================================================

如果你正在构建一个比较大的应用，那么将控制器放到子目录下进行组织可能会方便一点。CodeIgniter 也可以实现这一点。

你只需要简单的在 *application/controllers/* 目录下创建新的目录，并将控制器文件放到子目录下。

.. note:: 当使用该功能时，URI 的第一段必须指定目录，例如，假设你在如下位置有一个控制器::

		application/controllers/products/Shoes.php

	为了调用该控制器，你的 URI 应该像下面这样::

		example.com/index.php/products/shoes/show/123

每个子目录包含一个默认控制器，将在 URL 只包含子目录的时候被调用。默认控制器在 *application/Config/Routes.php* 中定义。

你也可以使用 CodeIgniter 的 :doc:`./source/general/routing.rst` 功能来重定向 URI。


构造函数
==================


如果你打算在你的控制器中使用构造函数，你 **必须** 将下面这行代码放在里面:：

	parent::__construct(...$params);

原因是你的构造函数将会覆盖父类的构造函数，所以我们要手工的调用它。

例如::

	<?php
	class Blog extends \CodeIgniter\Controller
	{
		public function __construct(...$params)
		{
			parent::__construct(...$params);

			// Your own constructor code
		}
	}

如果你需要在你的类被初始化时设置一些默认值，或者进行一些默认处理，构造函数将很有用。 构造函数没有返回值，但是可以执行一些默认操作。

包含属性
===================

你创建的每一个 controller 都应该继承 ``CodeIgniter\Controller`` 类。这个类提供了适合所有控制器的几个属性。

Request 对象
--------------
``$this->request`` 作为应用程序的主要属性 :doc:`./source/libraries/request.rst` 是可以一直被使用的类属性。


Response 对象
---------------
``$this->response`` 作为应用程序的主要属性 :doc:`./source/libraries/response.rst` 是可以一直被使用的类属性。

Logger 对象
-------------
``$this->logger`` 类实例 :doc:`./source/general/logging.rst` 是可以一直被使用的类属性。

forceHTTPS
----------
一种强制通过 HTTPS 访问方法的便捷方法，在所有控制器中都是可用的::

	if (! $this->request->isSecure())
	{
		$this->forceHTTPS();
	}

默认情况下，在支持 HTTP 严格传输安全报头的现代浏览器中，此调用应强制浏览器将非 HTTPS 调用转换为一年的 HTTPS 调用。你可以通过将持续时间（以秒为单位）作为第一个参数来修改。 ::

	if (! $this->request->isSecure())
	{
		$this->forceHTTPS(31536000);    // one year
	}


.. note:: 你可以使用更多全局变量和函数 :doc:`./source/general/common_functions.rst` ，包括 年、月等等。


辅助函数
-------------

你可以定义一个辅助文件数组作为类属性。每当控制器被加载时，
这些辅助文件将自动加载到内存中，这样就可以在控制器的任何地方使用它们的方法。::

	class MyController extends \CodeIgniter\Controller
	{
		protected $helpers = ['url', 'form'];
	}

验证 $_POST 数据
======================

控制器还提供了一个简单方便的方法来验证 $_POST 数据，将一组规则作为第一个参数进行验证，如果验证不通过，可以选择显示一组自定义错误消息。你可以通过 **$this->request** 这个用法获取 POST 数据。 :doc:`Validation Library docs <./source/libraries/validation.rst>` 是有关规则和消息数组的格式以及可用规则的详细信息。 ::

    public function updateUser(int $userID)
    {
        if (! $this->validate([
            'email' => "required|is_unique[users.email,id,{$userID}]",
            'name' => 'required|alpha_numeric_spaces'
        ]))
        {
            return view('users/update', [
                'errors' => $this->errors
            ]);
        }

        // do something here if successful...
    }

如果你觉得在配置文件中保存规则更简单，你可以通过在 ``Config\Validation.php`` 中定义代替 $rules 数组 ::

    public function updateUser(int $userID)
    {
        if (! $this->validate('userRules'))
        {
            return view('users/update', [
                'errors' => $this->errors
            ]);
        }

        // do something here if successful...
    }

.. note:: 验证也可以在模型中自动处理。你可以在任何地方处理，你会发现控制器中的一些情况比模型简单，反之亦然。

就这样了！
==========

OK，总的来说，这就是关于控制器的所有内容了。
