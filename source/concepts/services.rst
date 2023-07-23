########
服务
########

.. contents::
    :local:
    :depth: 2

简介
************

什么是服务?
==================

CodeIgniter 4 中的 **服务** 提供了创建和共享新类实例的功能。它由 ``Config\Services`` 类实现。

CodeIgniter 的所有核心类都以“服务”提供。这仅仅意味着,不是硬编码一个类名进行加载,而是在一个非常简单的配置文件中定义要调用的类。这个文件充当工厂的角色,用来创建所需类的新实例。

为什么使用服务?
=================

一个快速的示例可能会使事情更清楚,所以想象一下,你需要获取 Timer 类的一个实例。最简单的方法就是简单地创建该类的一个新实例:

.. literalinclude:: services/001.php

这工作得很好。直到你决定要使用另一个定时器类来替换它。也许这个定时器类具有默认定时器不提供的一些高级报告功能。为了做到这一点,你现在需要找到应用程序中使用了定时器类的所有位置。由于你可能已经将它们保留在那里以便持续运行性能日志,所以这可能是一个非常耗时且容易出错的处理方法。这就是服务派上用场的地方。

与其自己创建实例,不如让一个中心类为我们创建类的实例。这个类非常简单。它只包含每个我们希望用作服务的类的方法。该方法通常返回该类的一个共享实例,并将它可能具有的任何依赖项传递给它。然后,我们将用调用此新类的代码替换定时器创建代码:

.. literalinclude:: services/002.php

当你需要更改使用的实现时,可以修改服务配置文件,更改会自动传播到整个应用程序,而你不需要做任何事情。现在你只需要利用任何新的功能,就大功告成了。非常简单且不易出错。

.. note:: 建议只在控制器中创建服务。其他文件,如模型和库应该通过构造函数或设置器方法传入依赖项。

如何获取服务
********************

由于许多 CodeIgniter 类作为服务提供,你可以像如下获取它们:

.. literalinclude:: services/013.php

``$typography`` 是一个 Typography 类的实例,如果你再次调用 ``\Config\Services::typography()``,你将会得到完全相同的实例。

服务通常返回类的共享实例。下面的代码在首次调用时创建一个 ``CURLRequest`` 实例。第二次调用返回完全相同的实例。

.. literalinclude:: services/015.php

因此, ``$client2`` 的参数 ``$options2`` 不起作用。它被忽略了。

获取新实例
======================

如果你想获取 Typography 类的新实例,需要向参数 ``$getShared`` 传递 ``false``:

.. literalinclude:: services/014.php

便利函数
=====================

提供了两个获取服务的函数。这些函数始终可用。

service()
---------

第一个是 ``service()``,它返回所请求服务的新实例。唯一必需的参数是服务名称。这与 Services 文件中的方法名称相同,总是返回类的一个共享实例,所以多次调用函数应该始终返回相同的实例:

.. literalinclude:: services/003.php

如果创建方法需要其他参数,可以在服务名称后传入:

.. literalinclude:: services/004.php

single_service()
----------------

第二个函数 ``single_service()`` 的工作方式与 ``service()`` 相同,但返回类的新实例:

.. literalinclude:: services/005.php

定义服务
*****************

为了使服务能够良好地工作,你必须能够依赖于每个类具有一个恒定的 API 或 `接口 <https://www.php.net/manual/en/language.oop5.interfaces.php>`_ 来使用它。CodeIgniter 的几乎所有类都提供了它们要遵守的接口。当你想扩展或替换核心类时,你只需要确保满足接口的要求,你就会知道这些类是兼容的。

例如, ``RouteCollection`` 类实现了 ``RouteCollectionInterface``。当你想要创建一个提供不同路由创建方式的替代类时,你只需要创建一个实现 ``RouteCollectionInterface`` 的新类:

.. literalinclude:: services/006.php

最后,在 **app/Config/Services.php** 中添加 ``routes()`` 方法,以创建 ``MyRouteCollection`` 的新实例,而不是 ``CodeIgniter\Router\RouteCollection``:

.. literalinclude:: services/007.php

允许参数
===================

在某些情况下,你会希望在实例化时有选择地向类传递设置。由于 services 文件是一个非常简单的类,因此很容易实现这一点。

一个很好的例子是 ``renderer`` 服务。默认情况下,我们希望这个类能够在 ``APPPATH . 'views/'`` 中找到视图。我们希望开发人员有可能更改该路径,但如果他们的需求需要的话。所以该类接受 ``$viewPath`` 作为构造函数参数。服务方法如下所示:

.. literalinclude:: services/008.php

这会在构造函数中设置默认路径,但允许轻松更改它使用的路径:

.. literalinclude:: services/009.php

共享类
==============

有时候你需要要求只创建服务的单个实例。这可以通过在工厂方法中调用的 ``getSharedInstance()`` 方法轻松处理。这会处理检查实例是否已在类中创建和保存,如果没有,则创建一个新实例。所有工厂方法都提供 ``$getShared = true`` 作为最后一个参数。你也应该坚持使用该方法:

.. literalinclude:: services/010.php

服务发现
*****************

CodeIgniter 可以自动发现你可能在任何定义的命名空间中创建的任何 **Config/Services.php** 文件。这允许简单使用任何模块的 Services 文件。为了发现自定义 Services 文件,它们必须满足以下要求:

- 其命名空间必须在 **app/Config/Autoload.php** 中定义
- 在命名空间内,该文件必须位于 **Config/Services.php**
- 它必须扩展 ``CodeIgniter\Config\BaseService``

一个小例子应该澄清这一点。

假设在项目的根目录中创建了一个新目录 **Blog**。这将保存带有控制器、模型等的 **Blog 模块**,你想将其中一些类作为服务提供。第一步是创建一个新文件:**Blog/Config/Services.php**。该文件框架应该是:

.. literalinclude:: services/011.php

现在你可以像上面描述的那样使用此文件。当你想从任何控制器获取文章服务时,只需使用框架的 ``Config\Services`` 类获取你的服务:

.. literalinclude:: services/012.php

.. note:: 如果多个 Services 文件具有相同的方法名,则返回找到的第一个实例。
