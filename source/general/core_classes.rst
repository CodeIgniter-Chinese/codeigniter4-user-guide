****************************
生成核心系统类
****************************


每次CI运行，就有若干个基础类作为核心框架的一部分被初始化。然而，将任意一个核心系统类替换成你自己想要的类或仅仅是局部扩展这些基础类也是可以的。

**虽说绝大部分用户将没有上述的需求，但对于一些想显著改变CI核心的用户来说，这个可替换或者扩展的选项存在确有必要。**

**注意**

变动核心系统类意味着一系列的挑战，所以，请三思后行。

系统类列表
=================

以下是每次CI运行时涉及到的系统核心文件列表：

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

核心类的替换
=================

当用你自己的系统类替代CI默认的类时，确保如下，1:doc:`Autoloader <../concepts/autoloader>` 能找到你的类，2你的新类继承了正确的接口，同时修改:doc:`Service <../concepts/services>` 保证加载的是你自己的类。

比如，你有一个名为 `` App\Libraries\RouteCollection `` 的新类想要替换掉系统原来的类，你应该像这样生成之::

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

核心类的扩展
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

**Tip:**  在你自己的类中，所有与父类方法名相同的函数将会覆盖父类方法，此为"方法覆盖". 这样你就可以充分地改动CI的核心类。

你若扩展了控制器核心类，则需确保你的新类继承了应用下的控制器类的构造器::

	class Home extends App\BaseController {

	}
