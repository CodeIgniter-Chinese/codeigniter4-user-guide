############
代码模块
############

CodeIgniter 支持一种代码模块化形式，帮助你创建可重用的代码。模块通常围绕特定主题展开，可以看作是大型应用程序中的小型应用程序。

支持框架内的任何标准文件类型，如控制器、模型、视图、配置文件、辅助函数、语言文件等。模块可以包含你想要的任意数量或任意少的这些文件。

如果要创建 Composer 包形式的模块，请参阅 :doc:`../extending/composer_packages`。

.. contents::
    :local:
    :depth: 2

**********
命名空间
**********

模块功能的核心元素来自 CodeIgniter 使用的 :doc:`PSR-4 兼容的自动加载 <../concepts/autoloader>`。
虽然任何代码都可以使用 PSR-4 自动加载和命名空间，但要充分利用模块，主要方法是为代码添加命名空间，
并将其添加到 **app/Config/Autoload.php** 的 ``$psr4`` 属性中。

例如，假设我们想要创建一个可以在应用程序之间重用的简单博客模块。我们可以创建一个以公司名称 Acme 命名的文件夹来存储所有模块。
我们将其直接放在主项目根目录的 **app** 目录旁边::

    acme/        // 新模块目录
    app/
    public/
    system/
    tests/
    writable/

打开 **app/Config/Autoload.php**，将 ``Acme\Blog`` 命名空间添加到 ``$psr4`` 数组属性中：

.. literalinclude:: modules/001.php

现在设置完成，可以通过 ``Acme\Blog`` 命名空间访问 **acme/Blog** 文件夹内的任何文件。仅此一项就满足了模块正常工作所需的 80% 功能，
因此你需要熟悉命名空间并习惯使用它们。多种文件类型将通过所有已定义的命名空间自动扫描 - 这是使用模块的关键要素。

模块内的常见目录结构将模仿主应用程序文件夹::

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

当然，并没有强制要求你必须完全照搬这种结构，你应该以最适合模块的方式组织它，
比如省略不需要的目录，为实体（Entities）、接口（Interfaces）或仓库（Repositories）等创建新目录。

***************************
自动加载非类文件
***************************

你的模块通常不仅包含 PHP 类，还会包含过程式函数、引导文件、模块常量文件等，这些文件通常不像类那样被（自动）加载。处理这种情况的一种方法是，在需要使用这些文件的文件开头，直接使用 ``require`` 引入它们。

CodeIgniter 提供的另一种方法是自动加载这些 *非类* 文件，就像自动加载类一样。我们只需要提供这些文件的路径列表，并将它们包含在 **app/Config/Autoload.php** 文件的 ``$files`` 属性中即可。

.. literalinclude:: modules/002.php

.. _auto-discovery:

**************
自动发现
**************

很多时候，你需要为要包含的文件指定完整的命名空间，但 CodeIgniter 可以配置为通过自动发现多种不同的文件类型，
使模块集成到应用程序中更简单，包括：

- :doc:`事件 <../extending/events>`
- :doc:`过滤器 <../incoming/filters>`
- :ref:`registrars`
- :doc:`路由文件 <../incoming/routing>`
- :doc:`服务 <../concepts/services>`

这是在 **app/Config/Modules.php** 文件中配置的。

自动发现系统通过扫描在 **Config/Autoload.php** 和 Composer 包中定义的 psr4 命名空间中的特定目录和文件来工作。

发现过程将在该路径上查找可发现的项目，例如，应该找到位于 **acme/Blog/Config/Routes.php** 的路由文件。

启用/禁用发现
=======================

可以使用 ``$enabled`` 类变量开启或关闭系统中的所有自动发现。False 将禁用所有发现，
优化性能，但会失去模块和 Composer 包的特殊功能。

指定发现项目
=======================

使用 ``$aliases`` 选项，可以指定哪些项目被自动发现。如果项目不存在，
则不会对该项目进行自动发现，但数组中的其他项目仍将被发现。

发现与 Composer
======================

通过 Composer 使用 PSR-4 命名空间安装的包默认也会被发现。
PSR-0 命名空间的包将不会被检测到。

.. _modules-specify-composer-packages:

指定 Composer 包
-------------------------

.. versionadded:: 4.3.0

为避免浪费时间扫描不相关的 Composer 包，可以通过编辑 **app/Config/Modules.php** 中的 ``$composerPackages`` 变量手动指定要发现的包：

.. literalinclude:: modules/013.php

或者，可以指定要从发现中排除的包。

.. literalinclude:: modules/014.php

禁用 Composer 包发现
----------------------------------

如果在定位文件时不希望扫描 Composer 的所有已知目录，可以通过编辑 **app/Config/Modules.php** 中的 ``$discoverInComposer`` 变量将其关闭：

.. literalinclude:: modules/004.php

******************
文件操作
******************

本节将介绍各种文件类型（如控制器、视图、语言文件等）及其在模块中的使用方法。尽管其中部分内容在用户指南的相关章节中有更详细的说明，但我们仍在此处进行了重述，以便你能更轻松地理解所有组件是如何协同工作的。

路由
======

默认情况下，模块内的 :doc:`路由 <../incoming/routing>` 会被自动扫描。可以在上述 **Modules** 配置文件中关闭此功能。

.. note:: 由于文件被包含到当前作用域中，``$routes`` 实例已经为你定义。
    如果尝试重新定义该类，将导致错误。

使用模块时，如果应用程序中的路由包含通配符可能会出现问题。
在这种情况下，请参阅 :ref:`routing-priority`。

.. _modules-filters:

过滤器
=======

.. deprecated:: 4.4.2

.. note:: 此功能已弃用。请改用 :ref:`registrars`，如下所示：

    .. literalinclude:: modules/015.php

默认情况下，模块内的 :doc:`过滤器 <../incoming/filters>` 会被自动扫描。
可以在上述 **Modules** 配置文件中关闭此功能。

.. note:: 由于文件被包含到当前作用域中，``$filters`` 实例已经为你定义。
    如果尝试重新定义该类，将导致错误。

在模块的 **Config/Filters.php** 文件中，需要定义所使用过滤器的别名：

.. literalinclude:: modules/005.php

控制器
===========

主 **app/Controllers** 目录外的控制器无法通过 URI 检测自动路由，
但必须在 Routes 文件本身中指定：

.. literalinclude:: modules/006.php

为减少此处所需的输入量，**group** 路由功能很有帮助：

.. literalinclude:: modules/007.php

配置文件
============

使用配置文件时不需要特殊更改。这些仍然是带命名空间的类，使用 ``new`` 命令加载：

.. literalinclude:: modules/008.php

在使用始终可用的 :php:func:`config()` 函数并向其传递短类名时，配置文件会被自动发现。

.. note:: 我们不建议你在模块中使用相同的短类名。
    需要覆盖或添加到 **app/Config/** 中已知配置的模块应使用 :ref:`registrars`。

.. note:: 在 v4.4.0 之前，当存在相同短名称的类时，
    即使指定像 ``config(\Acme\Blog\Config\Blog::class)`` 这样的完全限定类名，
    ``config()`` 也会在 **app/Config/** 中查找文件。
    此行为已在 v4.4.0 中修复，并返回指定的实例。

迁移
==========

迁移文件将在定义的命名空间内自动发现。每次运行时都会执行在所有命名空间中找到的所有迁移。

数据填充
========

只要提供完整的命名空间，填充文件就可以从 CLI 使用，也可以从其他填充文件中调用。
如果在 CLI 上调用，需要提供双反斜杠：


对于 Unix：

.. code-block:: console

    php spark db:seed Acme\\Blog\\Database\\Seeds\\TestPostSeeder

对于 Windows：

.. code-block:: console

    php spark db:seed Acme\\Blog\\Database\\Seeds\\TestPostSeeder

辅助函数
========

使用 :php:func:`helper()` 函数时，只要位于命名空间的 **Helpers** 目录内，
辅助函数将在定义的命名空间内自动发现：

.. literalinclude:: modules/009.php

可以指定命名空间。详情请参阅 :ref:`helpers-loading-from-specified-namespace`。

语言文件
==============

使用 :php:func:`lang()` 函数时，只要文件遵循与主应用程序目录相同的目录结构，
语言文件就会从定义的命名空间中自动定位。

库
=========

库总是通过其完全限定的类名实例化，因此不提供特殊访问：

.. literalinclude:: modules/010.php

模型
======

如果通过完全限定的类名使用 ``new`` 关键字实例化模型，不提供特殊访问：

.. literalinclude:: modules/011.php

使用始终可用的 :php:func:`model()` 函数时，模型文件会被自动发现。

.. note:: 我们不建议你在模块中使用相同的短类名。

.. note:: 在 v4.4.0 之前，当存在相同短名称的类时，
    即使指定像 ``model(\Acme\Blog\Model\PostModel::class)`` 这样的完全限定类名，
    ``model()`` 也会在 **app/Models/** 中查找文件。
    有关更多信息，请参阅 :ref:`factories-passing-fully-qualified-classname` 中的说明。

视图
=====

可以使用类命名空间加载视图，如 :ref:`namespaced-views` 文档中所述：

.. literalinclude:: modules/012.php
