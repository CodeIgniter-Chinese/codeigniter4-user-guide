############
代码模块
############

CodeIgniter 支持一种代码模块化形式,以帮助你创建可重用的代码。模块通常围绕特定主题展开,可以认为是你更大的应用程序中的微型应用程序。

框架支持的任何标准文件类型都受支持,如控制器、模型、视图、配置文件、辅助函数、语言文件等。模块可以包含尽可能少或多的这些文件。

如果你想将一个模块创建为 Composer 包，请参阅 :doc:`../extending/composer_packages`。

.. contents::
    :local:
    :depth: 2

**********
命名空间
**********

模块功能的核心元素来自 CodeIgniter 使用的 :doc:`兼容 PSR-4 的自动加载 <../concepts/autoloader>`。虽然任何代码都可以使用 PSR-4 自动加载器和命名空间,但充分利用模块的主要方法是为你的代码添加命名空间并将其添加到 **app/Config/Autoload.php** 中的 ``$psr4`` 属性。

例如,假设我们想保留一个简单的博客模块,以便在应用程序之间重用。我们可以创建一个文件夹,名为 Acme,来存储所有的模块。我们将它放在主项目根目录中的 **app** 目录旁边::

    acme/        // 新模块目录
    app/
    public/
    system/
    tests/
    writable/

打开 **app/Config/Autoload.php** 并将 ``Acme\Blog`` 命名空间添加到 ``$psr4`` 数组属性:

.. literalinclude:: modules/001.php

现在设置好后,我们可以通过 ``Acme\Blog`` 命名空间访问 **acme/Blog** 文件夹中的任何文件。仅此一点就解决了模块工作所需的 80%,所以你应该确保熟悉命名空间并熟练使用它们。通过所有定义的命名空间会自动扫描几种文件类型 - 使用模块的关键组成部分。

模块中的常见目录结构将模拟主应用程序文件夹::

    acme/
        Blog/
            Config/
            Controllers/
            Database/
                Migrations/
                Seeds/
            Helpers/
            Language/
                en/
            Libraries/
            Models/
            Views/

当然,没有什么能强制你使用这个确切的结构,你应该以最适合模块的方式组织它,省略不需要的目录,为实体、接口或存储库等创建新目录。

***************************
自动加载非类文件
***************************

通常,你的模块不仅包含 PHP 类,还包含像程序函数、引导文件、模块常量文件等通常不会像加载类那样加载的文件。一种方法是在使用文件位置的开头 ``require`` 这些文件。

CodeIgniter 提供的另一种方法是像自动加载类一样自动加载这些 *非类* 文件。我们需要做的就是提供这些文件路径的列表,并将它们包含在 **app/Config/Autoload.php** 文件的 ``$files`` 属性中。

.. literalinclude:: modules/002.php

.. _auto-discovery:

**************
自动发现
**************

通常,你需要指定要包含的文件的完全命名空间,但是可以通过自动发现许多不同类型的文件来配置 CodeIgniter,从而使将模块集成到应用程序中更简单,包括:

- :doc:`Events <../extending/events>`
- :doc:`Filters <../incoming/filters>`
- :ref:`registrars`
- :doc:`Route files <../incoming/routing>`
- :doc:`Services <../concepts/services>`

这在文件 **app/Config/Modules.php** 中配置。

自动发现系统通过扫描在 **Config/Autoload.php** 和 Composer 包中定义的 psr4 命名空间下的特定目录和文件来工作。

例如,发现过程将在路径中查找可以发现的项,并应该找到 **acme/Blog/Config/Routes.php** 中的 routes 文件。

启用/禁用发现
=======================

你可以通过系统中的 ``$enabled`` 类变量打开或关闭所有自动发现。False 将禁用所有发现,优化性能,但会消除模块和 Composer 包的特殊功能。

指定要发现的项
=======================

使用 ``$aliases`` 选项,你可以指定要自动发现的项。如果不存在该项,则不会为该项执行自动发现,但数组中的其他项仍将被发现。

发现和 Composer
======================

使用 PSR-4 命名空间通过 Composer 安装的包也将默认被发现。使用 PSR-0 命名空间的包将不会被检测到。

.. _modules-specify-composer-packages:

指定 Composer 包
-------------------------

.. versionadded:: 4.3.0

为避免花时间扫描不相关的 Composer 包,你可以通过编辑 **app/Config/Modules.php** 中的 ``$composerPackages`` 变量手动指定要发现的包:

.. literalinclude:: modules/013.php

或者,你可以指定要从发现中排除的包。

.. literalinclude:: modules/014.php

禁用 Composer 包发现
----------------------------------

如果你不希望在查找文件时扫描 Composer 的所有已知目录,可以通过编辑 **app/Config/Modules.php** 中的 ``$discoverInComposer`` 变量将其关闭:

.. literalinclude:: modules/004.php

******************
使用文件
******************

本节将查看每种文件类型(控制器、视图、语言文件等)以及如何在模块中使用它们。用户指南的相关位置已对其中一些信息进行了更详细的描述,但在此重复以更容易掌握所有部分的关系。

路由
======

默认情况下,模块内会自动扫描 :doc:`路由 <../incoming/routing>`。可以在上面描述的 **Modules** 配置文件中将其关闭。

.. note:: 由于文件被包含到当前作用域中,因此 ``$routes`` 实例已为你定义。如果尝试重新定义该类,则会导致错误。

使用模块时,如果应用程序中的路由包含通配符,这可能是一个问题。在这种情况下,请参阅 :ref:`routing-priority`。

.. _modules-filters:

过滤器
=======

.. deprecated:: 4.4.2

.. note:: 此功能已被弃用。请改用 :ref:`registrars`，如下所示：

    .. literalinclude:: modules/015.php

默认情况下,模块内会自动扫描 :doc:`过滤器 <../incoming/filters>`。可以在上面描述的 **Modules** 配置文件中将其关闭。

.. note:: 由于文件被包含到当前作用域中,因此 ``$filters`` 实例已为你定义。如果尝试重新定义该类,则会导致错误。

在模块的 **Config/Filters.php** 文件中,你需要定义使用的过滤器的别名:

.. literalinclude:: modules/005.php

控制器
===========

**app/Controllers** 目录之外的控制器无法通过 URI 检测自动路由,而必须在 Routes 文件本身中指定:

.. literalinclude:: modules/006.php

为了减少这里所需的输入量, **group** 路由功能很有用:

.. literalinclude:: modules/007.php

配置文件
============

使用配置文件时不需要特殊更改。这些仍然是命名空间类,并使用 ``new`` 命令加载:

.. literalinclude:: modules/008.php

无论何时使用始终可用的 :php:func:`config()` 函数，并将一个短类名传递给它，配置文件都会被自动发现。

.. note:: 我们不建议在模块中使用相同的短类名。需要覆盖或添加 **app/Config/** 中已知配置的模块应使用 :ref:`Implicit Registrars <registrars>`。

.. note:: 在 v4.4.0 之前，即使你指定了一个完全限定的类名，如 ``config(\Acme\Blog\Config\Blog::class)``，``config()`` 仍会在 **app/Config/** 中查找文件，只要存在与短类名相同的类。在 v4.4.0 中修复了这个行为，并返回指定的实例。

迁移
==========

定义命名空间中的迁移文件将被自动发现。跨所有命名空间找到的所有迁移将在每次运行时都执行。

种子
=====

只要提供完全限定的命名空间,就可以从 CLI 和其他种子文件中调用种子文件。如果在 CLI 上调用,则需要提供双反斜杠:

For Unix:

.. code-block:: console

    php spark db:seed Acme\\Blog\\Database\\Seeds\\TestPostSeeder

For Windows:

.. code-block:: console

    php spark db:seed Acme\Blog\Database\Seeds\TestPostSeeder

辅助函数
========

在使用 :php:func:`helper()` 函数时,定义的命名空间内的辅助函数将被自动发现,只要它们在 **Helpers** 目录内:

.. literalinclude:: modules/009.php

你可以指定命名空间。详情请参阅 :ref:`helpers-loading-from-specified-namespace`。

语言文件
==============

只要文件遵循与主应用程序目录相同的目录结构,在使用 ``lang()`` 方法时就会从定义的命名空间自动定位语言文件。

库
=========

库总是通过它们的完全限定类名实例化的,所以不提供特殊访问:

.. literalinclude:: modules/010.php

模型
======

如果你通过完全限定的类名用 ``new`` 关键字实例化模型,则不提供特殊访问:

.. literalinclude:: modules/011.php

每当使用始终可用的 :php:func:`model()` 函数时,都会自动发现模型文件。

.. note:: 我们不建议在模块中使用相同的短类名。

.. note:: 当有一个相同短名称的类时,即使你指定了完全限定的类名(如 ``model(\Acme\Blog\Model\PostModel::class)``), ``model()`` 也会在 **app/Models/** 中找到该文件。这是因为 ``model()`` 是 ``Factories`` 类的包装器,默认使用 ``preferApp``。有关更多信息,请参阅 :ref:`factories-loading-class`。

视图
=====

如 :doc:`视图 </outgoing/views>` 文档中所述,可以使用类命名空间加载视图:

.. literalinclude:: modules/012.php
