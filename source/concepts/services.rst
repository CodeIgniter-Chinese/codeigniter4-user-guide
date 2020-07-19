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

为了保证服务的正常运行，你需要能够对每个拥有常量API，或者实现了 `接口 <https://www.php.net/manual/en/language.oop5.interfaces.php>`_ 的类建立依赖。
CodeIgniter 的大部分类都提供了一个它们所应当提供的接口。当你需要扩展或者替代核心类时，你只需要确保自己符合这些接口的要求并且确定这些类的功能是完善的。

举例来说， ``RouterCollection`` 类实现了 ``RouterCollectionInterface`` 接口。当你想要替代该类，并实现不同的路由管理方法时，只需要创建一个实现了 ``RouterCollectionInterface`` 接口的类即可::

	class MyRouter implements \CodeIgniter\Router\RouteCollectionInterface
	{
		// Implement required methods here.
	}

最后，修改 **/app/Config/Services.php** 以创建 ``MyRouter`` 类的实例，来替代 ``CodeIgniter\Router\RouterCollection`` ::

	public static function routes()
	{
		return new \App\Router\MyRouter();
	}

允许使用参数
-------------------

在某些情况下，你可能想要使用某个选项来为一个类在实例化的时候传递配置信息。
由于服务文件只是简单的类文件，如上操作非常方便。

``renderer`` 服务就是一个不错的例子。默认情况下，我们需要该类能够找到 ``APPPATH.views/`` 目录下的视图文件。我们同时也想为开发者提供改变路径的选项（如果他们需要的话）。
因此该类接受 ``$viewPath`` 变量作为构造函数的参数。该服务的调用方法可能如下所示::

	public static function renderer($viewPath=APPPATH.'views/')
	{
		return new \CodeIgniter\View\View($viewPath);
	}

这一过程在构造函数方法里设置了默认路径，同时也可以轻松地改变其所使用的路径::

	$renderer = \Config\Services::renderer('/shared/views');

共享类
-----------------

某些情况下你可能只需要创建一个类的单实例。该操作可以通过工厂方法内部调用的 ``getSharedInstance()`` 方法来轻松地处理。
该方法检查了该类是否已创建了存储于内部的单个实例，如果没有的话，就会创建一个新的。所有的工厂方法都会提供一个 ``$getShared = true`` 的值作为最后的参数。你可以像这样操作该方法::

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

服务发现
-----------------

CodeIgniter可以自动发现所有你在其他命名空间里可能定义的 ``Config\Services.php`` 文件。这一功能允许了任何模块服务化文件的简单使用。
为了这些定制化的服务文件可以被自动发现，他们需要满足这些要求

- 它们的命名空间必须在 ``Config\Autoload.php`` 中已定义
- 在命名空间内部，该文件必须可以在 ``Config\Services.php`` 里被找到
- 它们必须继承 ``CodeIgniter\Config\BaseService`` 类

一个小例子可以帮助我们更好地理解。

假设你创建了一个新的目录，比如在根目录下的一个叫做 ``Blog`` 的目录。该目录中里有一个 **博客模块** ，并含有控制器，模型等文件。
如果你愿意的话也可以将某些类作为服务而使用。第一步就是创建一个新的文件: ``Blog\Config\Services.php`` ，该文件结构应当如下所示::

    <?php namespace Blog\Config;

    use CodeIgniter\Config\BaseService;

    class Services extends BaseService
    {
        public static function postManager()
        {
            ...
        }
    }

现在你可以使用如上描述的文件。每当你想要调用其他控制器的 posts 服务时，就可以简单地使用该框架的 ``Config\Services`` 类来获取你所需要的服务::

    $postManager = Config\Services::postManager();

.. note:: 如果多个服务文件拥有相同的方法名，那么第一个被发现的服务实例就会作为返回值。
