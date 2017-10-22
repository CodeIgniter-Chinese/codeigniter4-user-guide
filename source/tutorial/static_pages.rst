############
加载静态页
############

**Note:** 本教程假设你已经下载好 CodeIgniter，并将其 :doc:`安装 <../installation/index>` 到你的开发环境。

首先你需要新建一个 **控制器** 来处理静态页。控制器就是用来帮助你完成工作的一个简单的类，它是你整个 Web 应用程序的"粘合剂"。

例如，当访问下面这个 URL 时:
	
	http://example.com/news/latest/10

根据此 URL 我们可以推测出有一个名称为 "news" 的控制器，被调用的方法为 "latest"，"latest" 方法的作用应该是查询10条新闻条目并展示在页面上。
在MVC模式里，你会经常看到下面格式的 URL:

	http://example.com/[controller-class]/[controller-method]/[arguments]

在正式环境下 URL 的格式可能会更复杂，但现在，我们只需要知道这些就够了。

新建一个文件 *application/Controllers/Pages.php*，然后添加如下代码：

::

	<?php
	class Pages extends CodeIgniter\Controller {

		public function view($page = 'home')
		{
	    }
	}

你刚创建了一个 ``Pages`` 类，有一个方法 view 并可接受一个 $page 的参数。``Pages`` 类继承自 ``CodeIgniter\Controller`` 类，这意味着它可以访问 ``CodeIgniter\Controller`` 类 (*system/Controller.php*) 中定义的方法和变量。

控制器将是你 Web 应用程序中处理请求的核心。和其他的 PHP 类一样，可以在你的控制器中使用 ``$this`` 来访问它。

现在，你已经创建了你的第一个方法，是时候创建一些基本的页面模板了。我们将新建两个 "views" (页面模板) 分别作为我们的页头和页脚。

新建页头文件 *application/Views/Templates/Header.php* 并添加以下代码：

::

	<!doctype html>
	<html>
	<head>
		<title>CodeIgniter Tutorial</title>
	</head>
	<body>

		<h1><?= $title; ?></h1>

页头包含了一些基本的 HTML 代码，用于展示页面主视图之前的内容。同时，它还打印出了 ``$title`` 变量，这个我们之后讲控制器的时候再细说。
现在，再新建个页脚文件 *application/Views/Templates/Footer.php*，然后添加以下代码：

::

			<em>&copy; 2016</em>
		</body>
	</html>

在控制器中添加逻辑
------------------------------

你刚新建的控制器中有一个 ``view()`` 方法，这个方法可接受一个用于指定要加载页面的参数。静态页面的模板目录为：*application/Views/Pages/*。

在该目录中，新建 *Home.php* 和 *About.php* 模板文件。在每个文件中任意输入一些文本然后保存它们。如果你不知道写什么，那就写 "Hello World!" 吧。

为了加载这些界面，你需要检查下请求的页面是否存在：

::

	public function view($page = 'home')
	{
	    if ( ! file_exists(APPPATH.'/Views/Pages/'.$page.'.php'))
		{
			// Whoops, we don't have a page for that!
			throw new \CodeIgniter\PageNotFoundException($page);
		}

		$data['title'] = ucfirst($page); // Capitalize the first letter

		echo view('Templates/Header', $data);
		echo view('Pages/'.$page, $data);
		echo view('Templates/Footer', $data);
	}

当请求的页面存在时，将给用户加载并展示出一个包含页头页脚的页面。如果不存在，会显示 "404 Page not found" 的错误页面。

此事例方法中，第一行用以检查界面是否存在，``file_exists()`` 是原生的 PHP 函数，用于检查某个文件是否存在。``PageNotFoundException`` 是 CodeIgniter 的内置函数，用来展示默认的错误页面。

在页头模板文件中，``$title`` 变量代表页面的自定义标题，它是在方法中被赋值的，但并不是直接赋值给 title 变量，而是赋值给 ``$data`` 数组中的 title 元素。

最后要做的就是按顺序加载所需的视图，``view()`` 方法中的参数代表要展示的视图文件名称。``$data`` 数组中的每一个元素将被赋值给一个变量，这个变量的名字就是数组的键值。所以控制器中 ``$data['title']`` 的值，就等于视图中 ``$title`` 的值。

路由
-------

控制器已经开始工作了！在你的浏览器中输入 ``[your-site-url]index.php/pages/view`` 来查看你的页面。当你访问 ``index.php/pages/view/about`` 时你将看到包含页头和页脚的 about 页面。

使用自定义的路由规则，你可以将任意的 URL 映射到任意的控制器和方法上，从而打破默认的规则：
``http://example.com/[controller-class]/[controller-method]/[arguments]``

让我们来试试。打开路由文件 *application/Config/Routes.php* 然后添加如下两行代码，并删除掉其它对 ``$route`` 数组赋值的代码。

::

	$routes->setDefaultController('Pages/view');
	$routes->add('(:any)', 'Pages::view/$1');

CodeIgniter 读取路由的规则为从上到下，并将请求映射到第一个匹配的规则。每个规则都是一个正则表达式（左侧）映射到一个控制器和方法（右侧）。当获取到请求时，CodeIgniter 首先查找能匹配到的第一条规则，然后调用相应的可能存在参数的控制器和方法。

你可以在关于 :doc:`URL路由的文档 <../general/routing>` 中找到更多信息。

路由事例的第二条规则 ``$routes`` 数组中使用了通配符 ``(:any)`` 来匹配所有的请求，然后将参数传递给 ``Pages`` 类的 ``view()`` 方法。

为请求默认的控制器，你必须确定当前路由未被定义或重新编写过。默认的路由文件 **does** 下存在一个处理网站根目录的路由 (/) 规则.删除以下的路由来确保 Pages 控制器可以访问到我们的 home 页面：

	$routes->add('/', 'Home::index');

现在访问 ``index.php/about``。路由规则是不是正确的将你带到了控制器中的 ``view()`` 方法？太酷了！
