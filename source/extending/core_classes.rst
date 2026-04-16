****************************
创建核心系统类
****************************

每次 CodeIgniter 运行时，都会自动加载作为核心框架一部分的基础类。你可以用自己的类替换这些核心类，也可以继承并扩展它们。

**大多数情况下，用户无需进行此类操作。但如果你需要深度定制框架行为，CodeIgniter 也支持对核心类的替换或扩展。**

.. important:: 操作核心系统类会产生很多影响，因此在尝试之前，请确保你清楚自己在做什么。

.. contents::
    :local:
    :depth: 2

系统类列表
=================

以下是每次 CodeIgniter 运行时都会调用的核心系统类列表：

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
*  ``CodeIgniter\HTTP\CLIRequest`` (仅在命令行中启动时)
*  ``CodeIgniter\HTTP\ContentSecurityPolicy``
*  ``CodeIgniter\HTTP\Header``
*  ``CodeIgniter\HTTP\IncomingRequest`` (仅在通过 HTTP 启动时)
*  ``CodeIgniter\HTTP\Message``
*  ``CodeIgniter\HTTP\OutgoingRequest``
*  ``CodeIgniter\HTTP\Request``
*  ``CodeIgniter\HTTP\Response``
*  ``CodeIgniter\HTTP\SiteURI``
*  ``CodeIgniter\HTTP\SiteURIFactory``
*  ``CodeIgniter\HTTP\URI``
*  ``CodeIgniter\HTTP\UserAgent`` (仅在通过 HTTP 启动时)
*  ``CodeIgniter\Log\Logger``
*  ``CodeIgniter\Log\Handlers\BaseHandler``
*  ``CodeIgniter\Log\Handlers\FileHandler``
*  ``CodeIgniter\Router\RouteCollection``
*  ``CodeIgniter\Router\Router``
*  ``CodeIgniter\Superglobals``
*  ``CodeIgniter\View\View``

替换核心类
======================

要使用你自己的系统类而不是默认类，请确保：

    1. :doc:`自动加载器 <../concepts/autoloader>` 可以找到你的类，
    2. 你的新类实现了适当的接口，
    3. 并修改相应的 :doc:`服务 <../concepts/services>` 以加载你的类来替代核心类。

创建你的类
-------------------

例如，如果你有一个新的 ``App\Libraries\RouteCollection`` 类，想用它来替代核心系统类，你可以这样创建你的类：

.. literalinclude:: core_classes/001.php

添加服务
------------------

然后在 **app/Config/Services.php** 中添加 ``routes`` 服务来加载你的类：

.. literalinclude:: core_classes/002.php

扩展核心类
======================

如果只需要向现有库添加一些功能——比如增加一两个方法——那么完全重新创建整个库就过于复杂了。在这种情况下，最好只是简单地扩展该类。扩展类与 `替换核心类`_ 几乎完全相同，只有一个例外：

* 类声明必须扩展父类。

例如，要扩展原生的 ``RouteCollection`` 类，你可以这样声明你的类：

.. literalinclude:: core_classes/003.php

如果你需要在类中使用构造函数，请确保扩展父类构造函数：

.. literalinclude:: core_classes/004.php

**提示：** 在子类中定义与父类同名的方法会覆盖父类方法，这一机制称为“方法重写”，可用于自定义 CodeIgniter 核心类的行为。
