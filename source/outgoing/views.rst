#####
视图
#####

.. contents::
    :local:
    :depth: 2

视图只是一个网页或页面片段，例如页眉，页脚，侧边栏等。实际上，视图可以灵活地嵌入其他视图中（在其他视图内部）。

视图不会被直接调用，它必须通过控制器加载。请记住，在 MVC 框架中，控制器充当交通警察的作用，因此它专门负责读取特定的视图。
如果你还没有阅读过 :doc:`控制器 </incoming/controllers>` 页面，建议你应该先看下这个。

使用在控制器这一章里我们所创建的样例控制器，让我们为它创建一个视图。

创建视图
===============

使用你的文本编辑器，创建一个 ``BlogView.php`` 文件，代码如下::

	<html>
        <head>
            <title>My Blog</title>
        </head>
        <body>
            <h1>Welcome to my Blog!</h1>
        </body>
	</html>

将文件保存到 **app/Views** 文件夹。

显示视图
=================

要加载并且显示指定的视图文件，你需要用到下面的方法::

	echo view('name');

*name* 是视图文件的名称。

.. important:: 如果你省略了文件的扩展名，那么框架会默认该文件以 .php 扩展名结尾。

现在，打开你之前创建的 ``Blog.php`` 这个控制器文件，并将 echo 语句替换为 view 方法，以完成显示视图的功能::

	<?php namespace App\Controllers;

	class Blog extends \CodeIgniter\Controller
	{
		public function index()
		{
			echo view('BlogView');
		}
	}

如果你使用之前访问网站的 URL 来重新访问站点，你应该会看到新的视图。这个 URL 类似以下的内容::

	example.com/index.php/blog/

.. note:: 尽管所有示例都是直接显示视图内容，但是你也可以让视图内容的结果返回给控制器；并将其添加到所有已捕获的输出内容中。（译者注：即不是直接输出而是返回一个字符串用作后续使用）

加载多个视图
======================

CodeIgniter 可以智能的处理在控制器中多次调用 ``view()`` 方法。如果出现了多次调用，它们将被合并到一起。例如，你可能希望有一个
页头视图、 一个菜单视图，一个内容视图 以及 一个页脚视图。代码看起来应该这样::

	<?php namespace App\Controllers;

	class Page extends \CodeIgniter\Controller
	{
		public function index()
		{
			$data = [
				'page_title' => 'Your title'
			];

			echo view('header');
			echo view('menu');
			echo view('content', $data);
			echo view('footer');
		}
	}

在上面的例子中，我们使用了 "添加动态数据" ，我们会在后面讲到。

在子目录中存储视图
====================================

如果你喜欢这样的组织形式，则视图文件可以保存到子目录中。当你这样做时，加载视图时需要包含子目录的名字，例如::

	echo view('directory_name/file_name');

命名空间视图
================

您可以将视图存储在已命名空间的 **View** 目录下，并像加载加载命名空间一样加载视图。虽然 PHP 不支持在命名空间下加载非类文件，但是
CodeIgniter 提供了此功能，使你可以将它们以类似于模块的方式打包在一起，以便于重用或分发。

如果您在 :doc:`自动加载 </concepts/autoloader>` 文件 PSR-4 数组中设置 ``Blog`` 目录在 ``Example\Blog`` 命名空间下，则可
以像使用命名空间一样找到视图文件。下面的示例就是通过在名称空间前添加视图名称来从 **/blog/views** 目录下加载  **BlogView**
文件::

    echo view('Example\Blog\Views\BlogView');

.. note:: **译者注** 这段有点难懂，需要和 :doc:`模块 </general/modules>` 章节一起看会比较容易懂。我的理解：框架中视图文件默认在 **app/Views** 目录下，当然这个也是可以通过 **app/Config/Paths.php** 类的 ``$viewDirectory`` 属性进行更改的。那么如果我们使用了 modules 功能把 Blog 模块独立出来，视图文件也是可以正常加载的，那么就需要在 **app/Config/Autoload.php** 文件中设定好映射目录，然后就可以通过命名空间的形式来加载视图文件了。

缓存视图
=============

你可以通过 ``view`` 方法的第三个参数 ``cache`` 选项来实现视图缓存功能，缓存的实际单位是秒::

    // 视图会缓存 60 秒
    echo view('file_name', $data, ['cache' => 60]);

默认情况下，缓存视图的文件名与视图文件名相同。不过，你可以通过传递 ``cache_name`` 参数对缓存文件名进行自定义::

    // 视图会缓存 60 秒
    echo view('file_name', $data, ['cache' => 60, 'cache_name' => 'my_cached_view']);

视图中显示动态数据
===============================

数据通过视图方法的第二个参数从控制器传递到视图，这是一个例子::

	$data = [
		'title'   => 'My title',
		'heading' => 'My Heading',
		'message' => 'My Message'
	];

	echo view('blogview', $data);

让我们打开你的控制器文件，并添加一下代码::

	<?php namespace App\Controllers;

	class Blog extends \CodeIgniter\Controller
	{
		public function index()
		{
			$data['title']   = "My Real Title";
			$data['heading'] = "My Real Heading";

			echo view('blogview', $data);
		}
	}

现在打开视图文件，并将文本更改为与数据中的数组键对应的变量::

	<html>
        <head>
            <title><?= $title ?></title>
        </head>
        <body>
            <h1><?= $heading ?></h1>
        </body>
	</html>

现在重新刷新页面，你应该会看到变量已经替换成数据中的值。

默认情况下，传递的数据只在当前调用 `view` 中可用。如果在一次请求中多次调用该方法，则必须将所需的数据传递给每个视图。这样可以防止
数据显示/覆盖到其他视图中的数据而导致出现问题。如果你想保留数据，则可以将 `saveData` 选项传递到第三个参数的 `$option` 数组中::

	$data = [
		'title'   => 'My title',
		'heading' => 'My Heading',
		'message' => 'My Message'
	];

	echo view('blogview', $data, ['saveData' => true]);

另外，如果您希望 view 方法的默认功能是在调用之间保存数据，则可以在 **app/Config/Views.php** 中将 ``$saveData`` 设置为 **true**。

创建循环
==============

传入视图文件的数据不仅仅限制为普通的变量，你还可以传入多维数组，这样你就可以在视图中生成多行了。例如，如果你从数据库中获取数据， 一般情况下数据都是一个多维数组。

这里是个简单的例子，将它添加到你的控制器中::

	<?php namespace App\Controllers;

	class Blog extends \CodeIgniter\Controller
	{
		public function index()
		{
			$data = [
				'todo_list' => ['Clean House', 'Call Mom', 'Run Errands'],
				'title'     => "My Real Title",
				'heading'   => "My Real Heading"
			];

			echo view('blogview', $data);
		}
	}

现在打开视图文件并创建一个循环::

	<html>
	<head>
		<title><?= $title ?></title>
	</head>
	<body>
		<h1><?= $heading ?></h1>

		<h3>My Todo List</h3>

		<ul>
		<?php foreach ($todo_list as $item):?>

			<li><?= $item ?></li>

		<?php endforeach;?>
		</ul>

	</body>
	</html>
