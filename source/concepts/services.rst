########
服务
########

.. contents::
    :local:
    :depth: 2

简介
************

什么是服务？
==================

CodeIgniter 4 中的 **服务** 提供了创建和共享新类实例的功能。它通过 ``Config\Services`` 类实现。

CodeIgniter 内部的所有核心类都以“服务”形式提供。这仅仅意味着，与硬编码要加载的类名不同，需要调用的类被定义在一个非常简单的配置文件中。该文件充当一种工厂，用于创建所需类的新实例。

为什么要使用服务？
==================

一个简单的例子可能更容易理解。假设你需要引入一个 Timer 类的实例。最直接的方法就是创建该类的一个新实例：

.. literalinclude:: services/001.php

这非常有效。直到你决定要用一个不同的计时器类来替代它。也许这个类提供了一些默认计时器不具备的高级功能。为了实现这一点，你现在必须找到应用程序中所有使用了计时器类的地方。如果你为了持续记录应用程序性能而保留了这些代码，那么这种方式会非常耗时且容易出错。服务正是为了解决这个问题而设计的。

我们不再自己创建实例，而是让一个中心类来为我们创建该类的实例。这个类非常简单，它只为每个我们想作为服务使用的类包含一个方法。该方法通常返回该类的一个 **共享实例**，并将任何可能的依赖项传递给它。然后，我们将计时器创建代码替换为调用这个全局函数或 Services 类的代码：

.. literalinclude:: services/002.php

当你需要更改所使用的实现时，可以修改服务配置文件，更改会自动在整个应用程序中生效，而无需你做任何额外操作。现在你只需利用任何新功能即可。这种方式非常简单且不易出错。

.. note:: 建议仅在控制器中创建服务。其他文件，如模型和库，应通过构造函数或 setter 方法传入依赖项。

如何获取服务
********************

由于许多 CodeIgniter 类都以服务形式提供，你可以像下面这样获取它们：

.. literalinclude:: services/013.php

``$timer`` 是 Timer 类的一个实例，如果你再次调用 ``service('timer')``，你将得到完全相同的实例。

服务通常返回该类的一个 **共享实例**。以下代码在第一次调用时创建一个 ``CURLRequest`` 实例，第二次调用则返回完全相同的实例。

.. literalinclude:: services/015.php

因此，``$client2`` 的参数 ``$options2`` 不会生效，它会被忽略。

获取新实例
======================

如果你想获取 Timer 类的一个新实例，需要将参数 ``$getShared`` 设为 ``false``：

.. literalinclude:: services/014.php

便捷函数
=====================

提供了两个用于获取服务的函数，这些函数始终可用。

service()
---------

第一个是 ``service()``，它返回所请求服务的一个实例。唯一必需的参数是服务名称。这与 Services 文件中的方法相同，始终返回该类的一个 **共享实例**，因此多次调用该函数应始终返回相同的实例：

.. literalinclude:: services/003.php

.. note:: 自 v4.5.0 起，当你不向服务传递参数时，由于性能提升，推荐使用全局函数 ``service()``。

如果创建方法需要额外的参数，可以在服务名称后传递它们：

.. literalinclude:: services/004.php

single_service()
----------------

第二个函数 ``single_service()`` 的工作方式与 ``service()`` 类似，但返回一个新实例：

.. literalinclude:: services/005.php

定义服务
*****************

为了使服务正常工作，你必须能够依赖每个类都具有一个稳定的 API 或 `接口 <https://www.php.net/manual/zh/language.oop5.interfaces.php>`_。CodeIgniter 的几乎所有类都提供了一个它们遵循的接口。当你想要扩展或替换核心类时，你只需确保满足该接口的要求，就能知道这些类是兼容的。

例如，``RouteCollection`` 类实现了 ``RouteCollectionInterface``。当你想要创建一个提供不同路由创建方式的替代类时，你只需创建一个实现 ``RouteCollectionInterface`` 的新类：

.. literalinclude:: services/006.php

最后，将 ``routes()`` 方法添加到 **app/Config/Services.php** 中，以创建 ``MyRouteCollection`` 的新实例，而非 ``CodeIgniter\Router\RouteCollection``：

.. literalinclude:: services/007.php

允许传入参数
===================

在某些情况下，你可能希望在实例化类时传入一个设置。由于服务文件是一个非常简单的类，实现这一点很容易。

一个很好的例子是 ``renderer`` 服务。默认情况下，我们希望该类能在 ``APPPATH . 'views/'`` 找到视图。但我们希望开发者能够根据需要更改该路径。因此，该类接受 ``$viewPath`` 作为构造函数参数。服务方法如下所示：

.. literalinclude:: services/008.php

这在构造函数方法中设置了默认路径，但也允许轻松更改所使用的路径：

.. literalinclude:: services/009.php

共享类
==============

有时你需要确保只创建一个服务的实例。这可以通过工厂方法内部调用的 ``getSharedInstance()`` 方法轻松处理。该方法会检查该实例是否已在服务类中被创建并保存，如果没有，则创建一个新实例。所有的工厂方法都提供 ``$getShared = true`` 作为最后一个参数。你也应该遵循这种方法：

.. literalinclude:: services/010.php

服务发现
*****************

CodeIgniter 可以自动发现你在任何已定义的命名空间内创建的 **Config/Services.php** 文件。这使得可以轻松地使用任何模块的服务文件。为了使自定义服务文件被发现，它们必须满足以下要求：

- 其命名空间必须在 **app/Config/Autoload.php** 中定义
- 在命名空间内，该文件必须位于 **Config/Services.php**
- 它必须继承 ``CodeIgniter\Config\BaseService``

一个小例子可以阐明这一点。

假设你在项目根目录下创建了一个名为 **Blog** 的新目录。这将包含一个带有控制器、模型等的 **博客模块**，并且你希望将其中的一些类作为服务提供。第一步是创建一个新文件：**Blog/Config/Services.php**。该文件的骨架如下：

.. literalinclude:: services/011.php

现在你可以像上面描述的那样使用这个文件。当你想从任何控制器获取文章服务时，只需使用框架的 ``Config\Services`` 类来获取你的服务：

.. literalinclude:: services/012.php

.. note:: 如果多个服务文件具有相同的方法名，将返回找到的第一个实例。

.. _resetting-services-cache:

重置服务缓存
========================

.. versionadded:: 4.6.0

当在框架初始化过程早期首次调用 Services 类时，通过自动发现找到的服务类会被缓存在一个类属性中，并且不会被更新。

如果稍后动态加载了模块，并且这些模块中有服务，那么必须更新缓存。

这可以通过运行 ``Config\Services::resetServicesCache()`` 来实现。这将清除缓存，并在需要时强制重新进行服务发现。
