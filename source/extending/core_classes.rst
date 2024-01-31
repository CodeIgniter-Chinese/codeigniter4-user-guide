****************************
创建核心系统类
****************************

每次 CodeIgniter 运行时,都会自动初始化几个基本类作为核心框架的一部分。但是,可以用你自己的版本替换任何核心系统类,或者只是扩展核心版本。

**大多数用户都不需要这样做,但对于那些想要显着改变 CodeIgniter 核心的人来说,替换或扩展它们的选项确实存在。**

.. important:: 与核心系统类打交道有很多影响,所以在尝试之前,请确保你知道你在做什么。

.. contents::
    :local:
    :depth: 2

系统类列表
=================

以下是每次 CodeIgniter 运行时都会调用的核心系统类列表:

*  ``CodeIgniter\Autoloader\Autoloader``
*  ``CodeIgniter\Autoloader\FileLocator``
*  ``CodeIgniter\Cache\CacheFactory``
*  ``CodeIgniter\Cache\Handlers\BaseHandler``
*  ``CodeIgniter\Cache\Handlers\FileHandler``
*  ``CodeIgniter\Cache\ResponseCache``
*  ``CodeIgniter\CodeIgniter``
*  ``CodeIgniter\Config\BaseService``
*  ``CodeIgniter\Config\DotEnv``
*  ``CodeIgniter\Config\Factories``
*  ``CodeIgniter\Config\Services``
*  ``CodeIgniter\Controller``
*  ``CodeIgniter\Cookie\Cookie``
*  ``CodeIgniter\Cookie\CookieStore``
*  ``CodeIgniter\Debug\Exceptions``
*  ``CodeIgniter\Debug\Timer``
*  ``CodeIgniter\Events\Events``
*  ``CodeIgniter\Filters\Filters``
*  ``CodeIgniter\HTTP\CLIRequest`` (如果仅从命令行启动)
*  ``CodeIgniter\HTTP\ContentSecurityPolicy``
*  ``CodeIgniter\HTTP\Header``
*  ``CodeIgniter\HTTP\IncomingRequest`` (如果通过 HTTP 启动)
*  ``CodeIgniter\HTTP\Message``
*  ``CodeIgniter\HTTP\OutgoingRequest``
*  ``CodeIgniter\HTTP\Request``
*  ``CodeIgniter\HTTP\Response``
*  ``CodeIgniter\HTTP\SiteURI``
*  ``CodeIgniter\HTTP\SiteURIFactory``
*  ``CodeIgniter\HTTP\URI``
*  ``CodeIgniter\HTTP\UserAgent`` (如果通过 HTTP 启动)
*  ``CodeIgniter\Log\Logger``
*  ``CodeIgniter\Log\Handlers\BaseHandler``
*  ``CodeIgniter\Log\Handlers\FileHandler``
*  ``CodeIgniter\Router\RouteCollection``
*  ``CodeIgniter\Router\Router``
*  ``CodeIgniter\Superglobals``
*  ``CodeIgniter\View\View``

替换核心类
======================

要使用自己的系统类代替默认类,请确保:

1. :doc:`自动加载器 <../concepts/autoloader>` 可以找到你的类,
2. 你的新类实现了适当的接口,
3. 并修改适当的 :doc:`服务 <../concepts/services>` 来加载你的类以替换核心类。

创建你的类
-------------------

例如,如果你有一个新的 ``App\Libraries\RouteCollection`` 类,想用它代替核心系统类,你会这样创建你的类:

.. literalinclude:: core_classes/001.php

添加服务
------------------

然后你需要在 **app/Config/Services.php** 中添加 ``routes`` 服务来加载你的类:

.. literalinclude:: core_classes/002.php

扩展核心类
======================

如果你只需要为现有库添加一些功能 - 可能添加一两个方法 - 那么重新创建整个库就有点过度设计。在这种情况下,最好简单地扩展该类。扩展该类与 `替换核心类`_ 几乎相同,只有一个例外:

* 类声明必须扩展父类。

例如,要扩展原生的 ``RouteCollection`` 类,你需要用以下方式声明你的类:

.. literalinclude:: core_classes/003.php

如果你的类中需要使用构造函数,请确保扩展父类构造函数:

.. literalinclude:: core_classes/004.php

**提示:** 你类中与父类方法同名的任何函数都会代替原生的方法(这被称为“方法重载”)。这允许你大幅改变 CodeIgniter 核心。
