****************************
创建核心系统类
****************************


每次CodeIgniter 运行时，都有一些基础类伴随着核心框架自动的被初始化。但你也可以使用你自己的类来替代这些核心类或者扩展这些核心类。

**大多数用户一般不会有这种需求，但对于那些想较大幅度的改变 CodeIgniter 核心的人来说，我们依然提供了替换和扩展核心类的选择。**

.. note:: 变动核心系统类意味着一系列的挑战，所以，请三思后行。

系统类列表
=================

以下是系统核心文件的列表，它们在每次 CodeIgniter 启动时被调用：

* Config\Services
* CodeIgniter\Autoloader\Autoloader
* CodeIgniter\Config\DotEnv
* CodeIgniter\Controller
* CodeIgniter\Debug\Exceptions
* CodeIgniter\Debug\Timer
* CodeIgniter\Events\Events
* CodeIgniter\HTTP\CLIRequest (if launched from command line only)
* CodeIgniter\HTTP\IncomingRequest (if launched over HTTP)
* CodeIgniter\HTTP\Request
* CodeIgniter\HTTP\Response
* CodeIgniter\HTTP\Message
* CodeIgniter\Log\Logger
* CodeIgniter\Log\Handlers\BaseHandler
* CodeIgniter\Log\Handlers\FileHandler
* CodeIgniter\Router\RouteCollection
* CodeIgniter\Router\Router
* CodeIgniter\Security\Security
* CodeIgniter\View\View
* CodeIgniter\View\Escaper

替换核心类
=================

要使用你的系统类替换 CodeIgniter 默认的系统类时，首先确保 :doc:`Autoloader <../concepts/autoloader>` 能找到你的类；其次你的新类继承了正确的接口，同时修改 :doc:`Service <../concepts/services>` 以保证加载的是你自己的类。

例如，你有一个名为 `` App\Libraries\RouteCollection `` 的新类想要替换系统的核心类，你应该像这样创建你的类::

	class RouteCollection implements \CodeIgniter\Router\RouteCollectionInterface
	{

	}

然后，你应该修改路由文件来加载你自己的类::

	public static function routes($getShared = false)
	{
		if (! $getShared)
		{
			return new \App\Libraries\RouteCollection();
		}

		return self::getSharedInstance('routes');
	}

扩展核心类
=================

如果你需要往一个现有的库里添加一些功能-或许只是添加一两个方法，重写这整个库显然是没必要的。这时更好的通常是对其中的类进行扩展。对类进行扩展与替换掉类几乎相同，除了一点：

* 类的声明必须继承父类。

比如，继承 RouteCollection  这个原生类，你应该这样声明::

    class RouteCollection extends \CodeIgniter\Router\RouteCollection
    {

    }

如果你需要在类中使用构造器来确保子类继承了父类的构造器::

        class RouteCollection implements \CodeIgniter\Router\RouteCollection
        {
            public function __construct()
            {
                parent::__construct();
            }
        }

**Tip:**  在你自己的类中，所有与父类方法名相同的函数将会覆盖父类方法，此为"方法覆盖". 这样你就可以充分地改动CodeIgniter 的核心类。

你若扩展了控制器核心类，则需确保你的新类继承了应用下的控制器类的构造器::

	class Home extends App\BaseController {

	}
