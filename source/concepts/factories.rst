#########
工厂
#########

.. contents::
    :local:
    :depth: 2

简介
************

什么是工厂?
===================

与 :doc:`./services` 一样, **工厂** 是自动加载的扩展,可以帮助保持代码简洁且高效,而不需要在类之间传递对象实例。

工厂在以下几点上类似于 CodeIgniter 3 的 ``$this->load``:

- 加载一个类
- 共享加载的类实例

简单来说,工厂提供了一种常见的方式来创建类实例并从任何地方访问它。这是一种很好的方法来重用对象状态并减少在整个应用程序中保留多个实例加载的内存负载。

任何类都可以通过工厂加载,但最好的例子是那些用于处理或传输公共数据的类。框架本身在内部使用工厂,例如,使用 ``Config`` 类时确保加载正确的配置。

与服务的区别
=========================

工厂需要一个具体的类名来实例化,并且没有创建实例的代码。

因此,工厂不适合创建一个需要许多依赖项的复杂实例,并且你无法更改要返回的实例的类。

另一方面,服务具有创建实例的代码,所以它可以创建一个需要其他服务或类实例的复杂实例。获取服务时,服务需要一个服务名称,而不是一个类名,所以可以在不更改客户端代码的情况下更改返回的实例。

.. _factories-loading-class:

加载类
***************

加载一个类
===============

以 **模型** 为例。你可以通过使用 Factories 类的魔术静态方法 ``Factories::models()`` 访问特定于模型的工厂。

静态方法名称称为 *component*。

.. _factories-passing-classname-without-namespace:

不带命名空间的类名
-----------------------------------

如果您传递一个不带命名空间的类名，Factories 首先会在 ``App`` 命名空间中搜索与魔术静态方法名对应的路径。``Factories::models()`` 会搜索 **app/Models** 目录。

传递短类名
^^^^^^^^^^^^^^^^^^^^^^^

在下面的代码中，如果您有 ``App\Models\UserModel``，将返回该实例：

.. literalinclude:: factories/001.php

如果没有 ``App\Models\UserModel``，它会在所有命名空间中搜索 ``Models\UserModel``。

下次您在代码中的任何地方请求相同的类时，Factories 将确保您获得之前的实例：

.. literalinclude:: factories/003.php

传递带有子目录的短类名
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果要加载子目录中的类，可以使用 ``/`` 作为分隔符。如果存在，以下代码将加载 **app/Libraries/Sub/SubLib.php**：

.. literalinclude:: factories/013.php
   :lines: 2-

传递完全限定类名
--------------------------------

您还可以请求一个完全限定的类名：

.. literalinclude:: factories/002.php
   :lines: 2-

如果存在，它将返回 ``Blog\Models\UserModel`` 的实例。

.. note:: 在 v4.4.0 之前，当您请求一个完全限定的类名时，如果只有 ``Blog\Models\UserModel``，将返回该实例。但是，如果同时存在 ``App\Models\UserModel`` 和 ``Blog\Models\UserModel``，将返回 ``App\Models\UserModel`` 的实例。

    如果您想获取 ``Blog\Models\UserModel``，您需要禁用选项 ``preferApp``：

    .. literalinclude:: factories/010.php
       :lines: 2-

便利函数
*********************

为工厂提供了两个快捷函数。这些函数始终可用。

.. _factories-config:

config()
========

第一个是 :php:func:`config()`,它返回一个新的 Config 类实例。唯一必需的参数是类名称:

.. literalinclude:: factories/008.php

model()
=======

第二个函数 :php:func:`model()` 返回一个新的模型类实例。唯一必需的参数是类名称:

.. literalinclude:: factories/009.php

.. _factories-defining-classname-to-be-loaded:

定义要加载的类名
*******************************

.. versionadded:: 4.4.0

您可以使用 ``Factories::define()`` 方法定义在加载类之前要加载的类名：

.. literalinclude:: factories/014.php
   :lines: 2-

第一个参数是组件。第二个参数是类别名（Factories 魔术静态方法的第一个参数），第三个参数是要加载的真实完全限定类名。

之后，如果使用 Factories 加载 ``Myth\Auth\Models\UserModel``，将返回 ``App\Models\UserModel`` 的实例：

.. literalinclude:: factories/015.php
   :lines: 2-

工厂参数
******************

``工厂`` 的第二个参数是一个选项值数组(如下所述)。
这些指令将覆盖为每个组件配置的默认选项。

同时传递的任何更多参数将转发到类构造函数,使你可以即时配置类实例。例如,假设你的应用使用单独的数据库进行身份验证,并且你希望确保尝试访问用户记录的任何尝试都通过该连接:

.. literalinclude:: factories/004.php

现在从 ``工厂`` 加载的 ``UserModel`` 每次实际上都会返回使用备用数据库连接的类实例。

.. _factories-options:

工厂选项
*****************

默认行为可能不适用于每个组件。例如,假设你的组件名称及其路径不匹配,或者你需要将实例限制为某种类型的类。
每个组件都接受一组选项来指导发现和实例化。

========== ============== ======================================================================= ===================================================
键         类型           描述                                                                    默认值
========== ============== ======================================================================= ===================================================
component  string 或 null 组件名称(如果与静态方法不同)。这可以用于将一个组件别名到另一个。        ``null`` (默认为组件名称)
path       string 或 null 命名空间/文件夹内要查找类的相对路径。                                   ``null`` (默认为组件名称,但将首字母大写)
instanceOf string 或 null 要匹配返回实例上的必需类名称。                                          ``null`` (无过滤)
getShared  boolean        是否返回类的共享实例或者加载一个新实例。                                ``true``
preferApp  boolean        是否优先使用 App 命名空间中具有相同基本名称的类而不是其他明确的类请求。 ``true``
========== ============== ======================================================================= ===================================================

.. note:: 自 v4.4.0 起，``preferApp`` 仅在您请求 :ref:`不带命名空间的类名 <factories-passing-classname-without-namespace>` 时起作用。

工厂行为
******************

可以通过三种方式(按优先级降序排列)应用选项:

* 配置类 ``Config\Factory``,其中包含与组件名称匹配的属性。
* 静态方法 ``Factories::setOptions()``。
* 在调用时直接传递参数。

配置
==============

要设置默认组件选项,请在 **app/Config/Factory.php** 中创建一个新的 Config 文件,
以数组属性的形式提供与组件名称匹配的选项。

示例:过滤器工厂
--------------------------

例如,如果你要通过工厂创建 **过滤器**,组件名称将是 ``filters``。
如果你想确保每个过滤器都是实现了 CodeIgniter 的 ``FilterInterface`` 的类的实例,
你的 **app/Config/Factory.php** 文件可能如下所示:

.. literalinclude:: factories/005.php

现在你可以用类似 ``Factories::filters('SomeFilter')`` 的代码创建过滤器,
并且返回的实例一定是 CodeIgniter 的过滤器。

这将防止第三方模块意外地在其命名空间中具有不相关的 ``Filters`` 路径而发生冲突。

示例:库工厂
--------------------------

如果你想用 ``Factories::library('SomeLib')`` 在 **app/Libraries** 目录中加载库类,
路径 `Libraries` 与默认路径 `Library` 不同。

在这种情况下,你的 **app/Config/Factory.php** 文件如下所示:

.. literalinclude:: factories/011.php

现在你可以使用 ``Factories::library()`` 方法加载你的库:

.. literalinclude:: factories/012.php
   :lines: 2-

setOptions 方法
=================

``Factories`` 类有一个静态方法允许运行时选项配置:只需使用 ``setOptions()`` 方法提供所需的选项数组,它们将与默认值合并并存储以备下次调用:

.. literalinclude:: factories/006.php

参数选项
=================

``Factories`` 的魔术静态调用以选项值数组作为第二个参数。这些指令将覆盖为每个组件配置的存储选项,并可在调用时用于获得你所需的内容。输入应为以每个覆盖值为键的选项名称数组。

例如,默认情况下 ``Factories`` 假设你希望定位组件的共享实例。通过向魔术静态调用添加第二个参数,你可以控制该单个调用是否返回新实例还是共享实例:

.. literalinclude:: factories/007.php
   :lines: 2-

.. _factories-config-caching:

配置缓存
**************

.. versionadded:: 4.4.0

为了提高性能，实现了配置缓存。

先决条件
============

.. important:: 当不满足先决条件时使用此功能将阻止 CodeIgniter 正常运行。在这种情况下不要使用此功能。

- 要使用此功能，Factories 中实例化的所有 Config 对象的属性在实例化后不能被修改。换句话说，Config 类必须是不可变或只读的类。
- 默认情况下，每个被缓存的 Config 类必须实现 ``__set_state()`` 方法。

工作原理
============

- 如果 Factories 中的 Config 实例的状态发生变化，则在关闭之前将所有 Config 实例保存到缓存文件中。
- 如果有缓存可用，则在 CodeIgniter 初始化之前恢复缓存的 Config 实例。

简而言之，Factories 持有的所有 Config 实例在关闭之前都会被缓存，并且缓存的实例将永久使用。

如何更新配置值
===========================

一旦存储，缓存的版本将永不过期。更改现有的 Config 文件（或更改其环境变量）不会更新缓存或 Config 值。

因此，如果要更新 Config 值，请更新 Config 文件或其环境变量，并且必须手动删除缓存文件。

您可以使用 ``spark cache:clear`` 命令：

.. code-block:: console

    php spark cache:clear

或者直接删除 **writable/cache/FactoriesCache_config** 文件。

如何启用配置缓存
============================

取消 **public/index.php** 中以下代码的注释::

    --- a/public/index.php
    +++ b/public/index.php
    @@ -49,8 +49,8 @@ if (! defined('ENVIRONMENT')) {
     }

     // Load Config Cache
    -// $factoriesCache = new \CodeIgniter\Cache\FactoriesCache();
    -// $factoriesCache->load('config');
    +$factoriesCache = new \CodeIgniter\Cache\FactoriesCache();
    +$factoriesCache->load('config');
     // ^^^ Uncomment these lines if you want to use Config Caching.

     /*
    @@ -79,7 +79,7 @@ $app->setContext($context);
     $app->run();

     // Save Config Cache
    -// $factoriesCache->save('config');
    +$factoriesCache->save('config');
     // ^^^ Uncomment this line if you want to use Config Caching.

     // Exits the application, setting the exit code for CLI-based applications
