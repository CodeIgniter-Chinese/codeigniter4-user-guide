############
新闻展示功能
############

在上一个章节里，我们写了一个用于展示静态页面的类文件，通过这个简单的例子我们把CI4框架里的一些基本的概念讲解了一下。
我们还简单的使用了CI4里面的路由功能，通过自定义路由规则实现了页面的链接地址净化，使页面的访问地址看起来更整洁和搜索引擎友好。
现在，我们要开始进行一些基于数据库的动态内容的开发了。

建立教程所需的数据库
---------------------

我们假设你已经安装和 :doc:`配置 <../intro/requirements>` 好了用于 CodeIgniter4 运行所需的数据库软件。
我们也假设你会使用数据库管理的客户端工具（mysql，MySQL Workbench或者phpMyAdmin等）来运行稍后教程里提供的创建数据库表和插入测试数据所需的SQL代码。

下面我们就来教你如何为本教程创建一个数据库，并且正确配置CodeIgniter来使用这个数据库。

用你安装好的数据库客户端工具打开数据库，然后运行下面的两段SQL代码（MySQL适用）来创建一个数据表和插入一些测试数据。
随着你对 CodeIgniter 的熟悉程度越来越高，这些数据库相关的操作也可以通过程序代码在CodeIgniter框架下完成，你可以阅读 :doc:`数据迁移 <../dbmgmt/migration>` 和 :doc:`数据填充 <../dbmgmt/seeds>` 这两个章节来了解相关内容，以便掌握用程序代码操作数据库的相关技能。
::

    CREATE TABLE news (
			  id int(11) NOT NULL AUTO_INCREMENT,
			  title varchar(128) NOT NULL,
			  slug varchar(128) NOT NULL,
			  body text NOT NULL,
			  PRIMARY KEY (id),
			  KEY slug (slug)
    );

**Note:**  数据表里的 **slug** 字段在基于互联网访问的网站上是个非常有用的字段。
一般在这个字段里存放简短的词语来概括性描述数据内容，这将提升用户打开网址时候的访问体验，并且这种网址也是搜索引擎友好的网址，有利于网站内容的SEO优化。

然后我们在数据表里插入如下测试数据：
::

    INSERT INTO news VALUES
    (1,'Elvis sighted','elvis-sighted','Elvis was sighted at the Podunk internet cafe. It looked like he was writing a CodeIgniter app.'),
    (2,'Say it isn\'t so!','say-it-isnt-so','Scientists conclude that some programmers have a sense of humor.'),
    (3,'Caffeination, Yes!','caffeination-yes','World\'s largest coffee shop open onsite nested coffee shop for staff only.');

连接到你的数据库
---------------------

**CodeIgniter** 安装时会自动生成一个 ``.env`` 文件，确保里面的配置信息没有被注释掉，并且和你本地的数据库实际情况相吻合：
::

    database.default.hostname = localhost
    database.default.database = ci4tutorial
    database.default.username = root
    database.default.password = root
    database.default.DBDriver = MySQLi

创建你的数据模型文件
---------------------

我们要求你将数据库的操作代码写在模型（Model）文件里面，以便以后代码重用，不要将这些代码写在控制器（Controller）里。
你的模型文件们应该成为你处理数据库相关的增、删、改、查操作的默认地方。交由模型文件来操作数据库或者其他格数的数据文件。

打开 **app/Models/** 目录，在这个目录下面创建一个名字为 **NewsModel.php** 的文件，并在文件里加入如下代码。
为了保证代码运行顺利，你需要确认一下已经正确的完成了数据库的相关配置:doc:`这里 <../database/configuration>`。
::

	<?php

	    namespace App\Models;

	    class NewsModel extends \CodeIgniter\Model
	    {
		    protected $table = 'news';
	    }

这段代码和我们上一个章节里创建的控制器里的代码类似。
我们通过继承 ``CodeIgniter\Model`` 创建了一个新的模型文件，并加载了CI4内置的数据库操作类库。
后面我们可以在代码里通过 ``$this->db`` 来调用数据库的相关操作类库。

现在我们的数据库和数据模型文件已经建立好了。
我们首先写一个方法从数据库中获取所有的新闻文章。
为实现这点，我们将使用 **CodeIgniter** 的数据库抽象层工具 :doc:`查询构建器 <../database/query_builder>`，通过它你可以编写你的查询代码，并在 :doc:`所有支持的数据库平台 <../intro/requirements>` 上运行。
数据模型文件可以方便的和 **查询构建器** 一起工作，并且提供了一些方法让你操作数据的时候更加简单。现在向你的模型中添加如下代码。
::

	public function getNews($slug = false)
	{
		if ($slug === false)
		{
			return $this->findAll();
		}

		return $this->asArray()
		             ->where(['slug' => $slug])
		             ->first();
	}

通过这段代码，你可以执行两种不同的查询，一种是获取所有的新闻条目，另一种是根据特定的 `slug` 来获取指定的新闻条目。
你可能注意到了，我们直接的进行了基于``$slug`` 变量的数据对比命令，并不需要预先执行相应字段的查询操作，因为:doc:`查询构建器 <../database/query_builder>` 自动帮我们完成了这个工作。

我们在这里用到的 ``findAll()`` 和 ``first()`` 都是 *CodeIgniter4* 的数据模型（Model）基础类里面内置的方法。
他们根据我们在数据模型文件里（本例中是 **NewsModel** 文件）声明的 ``$table`` 变量而知道该对哪个数据表进行操作。
这些方法通过 **查询构建器** 运行指令操作当前数据表，并且会以数组的形式返回数据查询结果。在这个例子里面，``findAll()`` 的返回值是包含了指定数据表中的所有数据对象的一个数组。


显示新闻
----------------

现在，查询已经在数据模型文件里写好了，接下来我们需要将数据模型绑定到视图上，向用户显示新闻条目了。
这可以在之前写的 ``Pages`` 控制器里来做，但为了更清楚的阐述，我们定义了一个新的 ``News`` 控制器，创建在 *app/controllers/News.php* 文件中。
::

	<?php namespace App\Controllers;

	use App\Models\NewsModel;

	class News extends \CodeIgniter\Controller
	{
		public function index()
		{
			$model = new NewsModel();

			$data['news'] = $model->getNews();
		}

		public function view($slug = null)
		{
			$model = new NewsModel();

			$data['news'] = $model->getNews($slug);
		}
	}

阅读上面的代码你会发现，这和之前写的代码有些相似之处。
首先，它继承了*CodeIgniter*的一个核心类，``Controller``，这个核心类提供了很多非常有用的方法，它确保你可以操作当前的 ``Request`` 和 ``Response`` 对象，也可以操作``Logger`` 类, 方便你把日志文件写到磁盘里。

其次，有两个方法用来显示新闻条目，一个显示所有的，另一个显示特定的。
你可以看到第二个方法中调用模型方法时传入了 ``$slug`` 参数，模型根据这个 *slug* 返回特定的新闻条目。

现在，通过模型，控制器已经获取到数据了，但还没有显示出来。
下一步要做的就是将数据传递给视图。
我们修改 ``index()`` 方法成下面的样子：::

	public function index()
	{
		$model = new NewsModel();

		$data = [
			'news'  => $model->getNews(),
			'title' => 'News archive',
		];

		echo view('templates/header', $data);
		echo view('news/index', $data);
		echo view('templates/footer');
	}

上面的代码从模型中获取所有的新闻条目，并赋值给一个变量（*news*）。
另外页面的标题赋值给了 ``$data['title']`` 元素，然后所有的数据被传递给视图。
现在你需要创建一个视图文件来显示新闻条目了，新建 *app/Views/news/index.php* 文件并添加如下代码。
::

	<h2><?= $title ?></h2>

	<?php if (! empty($news) && is_array($news)) : ?>

		<?php foreach ($news as $news_item): ?>

			<h3><?= $news_item['title'] ?></h3>

			<div class="main">
				<?= $news_item['text'] ?>
			</div>
			<p><a href="<?= '/news/'.$news_item['slug'] ?>">View article</a></p>

		<?php endforeach; ?>

	<?php else : ?>

		<h3>No News</h3>

		<p>Unable to find any news for you.</p>

	<?php endif ?>

这里，我们通过一个循环将所有的新闻条目显示给用户，你可以看到我们直接采用了 *HTML* 和 *PHP* 混用的写法创建了一个视图页面。
如果你希望使用一种模板语言，你可以使用 CodeIgniter 的 `视图模版解析类 <../outgoing/view_parser>` ，或其他的第三方解析器。

新闻的列表页就做好了，但是我们还缺少一个显示特定新闻条目的页面。
我们可以调用之前创建的模型里的数据来实现这个功能，你只需要向控制器中添加一些代码，然后再新建一个视图就可以了。
回到 ``News`` 控制器，使用下面的代码替换掉 ``view()`` 方法：
::

	public function view($slug = NULL)
	{
		$model = new NewsModel();

		$data['news'] = $model->getNews($slug);

		if (empty($data['news']))
		{
			throw new \CodeIgniter\PageNotFoundException('Cannot find the page: '. $slug);
		}

		$data['title'] = $data['news']['title'];

		echo view('templates/header', $data);
		echo view('news/view', $data);
		echo view('templates/footer');
	}

我们并没有直接调用 ``getNews()`` 方法，而是传入了一个 ``$slug`` 参数，所以它会返回相应的新闻条目。
最后剩下的事是创建视图文件 ``app/Views/news/view.php`` 并添加如下代码 。

	<?php
	echo '<h2>'.$news['title'].'</h2>';
	echo $news['body'];

路由
-------
由于之前我们创建了基于通配符的路由规则，所以现在需要新增一条路由以便能访问到你刚刚创建的控制器。
修改路由配置文件（**app/config/routes.php**）添加类似下面的代码。
该规则可以让地址中带*news*的请求访问 ``News`` 控制器而不是去访问之前默认的 ``Pages`` 控制器。
第一行代码可以让访问 *news/slug* 地址的 URI 重定向到 News 控制器的 view() 方法。
::

	$routes->get('news/(:segment)', 'News::view/$1');
	$routes->get('news', 'News::index');
	$routes->get('(:any)', 'Pages::view/$1');

在地址栏里输入 *localhost:8080/news* 来访问你创建好的新闻列表页面吧。
你将会看到如下图一样的一个展示新闻列表的网页，列表里的每个文章都带一个可以打开该条新闻详情页面的超级链接。

.. image:: ../images/tutorial2.png
    :align: center