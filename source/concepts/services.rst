########
服务
########

.. contents::
    :local:
    :depth: 2

引言
============

在CodeIgniter内部的所有类实际上都是以"服务"的形式呈现的。这意味着，所有的类都是以定义在一个简单的配置文件里，而非硬编码所需要加载的类名，来进行加载的。
该配置文件实际上扮演了一种为所需类创建新的实例的工厂的角色。

一个简单的例子可能会讲得更清楚，比如请设想你需要获得一个 Timer （计时器）类的实例，最简单的方法就是为该类创建一个新的实例::

	$timer = new \CodeIgniter\Debug\Timer();

这种方式运行得相当不错，直到你决定需要在该位置上使用另一个计时器类时。可能这个类比起默认的计时器类提供了更高级的报告方法。
为了实现这一目标，你可能会查找应用中的所有位置来定位哪些地方使用了定时器类。由于你可能在很多地方都设置了该类的实例，以获取应用日常运行的性能日志，
这种查找-替换的工作可能会变得相当的耗时并且错误频发。这就是服务的用武之地。

取代了手动创建实例的操作，我们保留了一个中央控制类来为我们新建实例。该类的结构相当简单，仅仅包含了一个方法用于调度我们需要用作服务的每个类。
该方法只是返回了指定类的一个共享实例，用于所有依赖该类的地方以服务的形式来调用。从而我们可以用以下代码来取代每次都新建一个实例的方式::

	$timer = \Config\Services::timer();

当你想要更改这一实现时，只需要更改服务的配置文件，从而在应用中就可以自动地进行变更替换，不需要任何其他操作。
现在你所需要的只是使用新的替换上来的类的特性，非常地简单且不易出错。

.. note:: 我们推荐只在控制器里创建服务。在其他文件例如模型和库，应当依赖于构造函数或者 setter 方法的传参来实例化。


便利的方法
---------------------

有两个方法被用于获取一个服务，这些方法都非常的方便。

第一个就是 ``service()`` 方法，该方法返回了指定服务的新的实例。唯一需要的参数就是服务名。
该方法与服务文件内部返回共享实例的方式是一样的，因此对该方法的多次调用总是会返回一个相同的实例::

	$logger = service('logger');

如果创建的方法需要额外的参数，那么这些参数就应该在服务名后传递::

	$renderer = service('renderer', APPPATH.'views/');

第二个方法 ``single_service()`` ，和 ``service()`` 一样调用，不过每次都会返回一个指定类的新的实例::

	$logger = single_service('logger');

定义服务
=================

To make services work well, you have to be able to rely on each class having a constant API, or
`interface <https://www.php.net/manual/en/language.oop5.interfaces.php>`_, to use. Almost all of
CodeIgniter's classes provide an interface that they adhere to. When you want to extend or replace
core classes, you only need to ensure you meet the requirements of the interface and you know that
the classes are compatible.

For example, the ``RouterCollection`` class implements the ``RouterCollectionInterface``. When you
want to create a replacement that provides a different way to create routes, you just need to
create a new class that implements the ``RouterCollectionInterface``::

	class MyRouter implements \CodeIgniter\Router\RouteCollectionInterface
	{
		// Implement required methods here.
	}

Finally, modify **/app/Config/Services.php** to create a new instance of ``MyRouter``
instead of ``CodeIgniter\Router\RouterCollection``::
	public static function routes()
	{
		return new \App\Router\MyRouter();
	}

Allowing Parameters
-------------------

In some instances, you will want the option to pass a setting to the class during instantiation.
Since the services file is a very simple class, it is easy to make this work.

A good example is the ``renderer`` service. By default, we want this class to be able
to find the views at ``APPPATH.views/``. We want the developer to have the option of
changing that path, though, if their needs require it. So the class accepts the ``$viewPath``
as a constructor parameter. The service method looks like this::

	public static function renderer($viewPath=APPPATH.'views/')
	{
		return new \CodeIgniter\View\View($viewPath);
	}

This sets the default path in the constructor method, but allows for easily changing
the path it uses::

	$renderer = \Config\Services::renderer('/shared/views');

Shared Classes
-----------------

There are occasions where you need to require that only a single instance of a service
is created. This is easily handled with the ``getSharedInstance()`` method that is called from within the
factory method. This handles checking if an instance has been created and saved
within the class, and, if not, creates a new one. All of the factory methods provide a
``$getShared = true`` value as the last parameter. You should stick to the method also::

    class Services
    {
        public static function routes($getShared = false)
        {
            if (! $getShared)
            {
                return new \CodeIgniter\Router\RouteCollection();
            }

            return static::getSharedInstance('routes');
        }
    }

Service Discovery
-----------------

CodeIgniter can automatically discover any Config\\Services.php files you may have created within any defined namespaces.
This allows simple use of any module Services files. In order for custom Services files to be discovered, they must
meet these requirements:

- Its namespace must be defined in ``Config\Autoload.php``
- Inside the namespace, the file must be found at ``Config\Services.php``
- It must extend ``CodeIgniter\Config\BaseService``

A small example should clarify this.

Imagine that you've created a new directory, ``Blog`` in your root directory. This will hold a **blog module** with controllers,
models, etc, and you'd like to make some of the classes available as a service. The first step is to create a new file:
``Blog\Config\Services.php``. The skeleton of the file should be::

    <?php namespace Blog\Config;

    use CodeIgniter\Config\BaseService;

    class Services extends BaseService
    {
        public static function postManager()
        {
            ...
        }
    }

Now you can use this file as described above. When you want to grab the posts service from any controller, you
would simply use the framework's ``Config\Services`` class to grab your service::

    $postManager = Config\Services::postManager();

.. note:: If multiple Services files have the same method name, the first one found will be the instance returned.
