#########
工厂
#########

.. contents::
    :local:
    :depth: 3

简介
************

什么是工厂？
===================

与 :doc:`./services` 类似，**工厂** 是自动加载功能的扩展，它能帮助你的代码保持简洁高效，而无需在类之间传递对象实例。

工厂在以下方面与 CodeIgniter 3 的 ``$this->load`` 类似：

- 加载一个类
- 共享已加载的类实例

简单来说，工厂提供了一种通用的方式来创建类实例，并能从任何地方访问它。这是一种重用对象状态，减少应用程序中多个实例加载所造成的内存开销的好方法。

任何类都可以通过工厂加载，但最佳实践是那些用于处理或传输公共数据的类。框架本身也在内部使用工厂，例如，在使用 ``Config`` 类时确保加载正确的配置。

与服务的区别
=========================

工厂需要一个具体的类名来实例化，并且没有创建实例的代码。

因此，工厂不适合创建需要许多依赖项的复杂实例，并且你无法更改要返回的实例的类。

另一方面，服务有创建实例的代码，因此它可以创建需要其他服务或类实例的复杂实例。当你获取一个服务时，服务需要的是服务名称，而不是类名，因此返回的实例可以在不更改客户端代码的情况下进行更改。

.. _factories-loading-class:

加载类
***************

加载一个类
===============

以 **模型** 为例。你可以通过使用 Factories 类的魔术静态方法 ``Factories::models()`` 来访问特定于模型的工厂。

静态方法名称被称为 *组件*。

.. _factories-passing-classname-without-namespace:

不带命名空间传递类名
-----------------------------------

如果你传递一个不带命名空间的类名，工厂会首先在 ``App`` 命名空间中搜索与魔术静态方法名称对应的路径。``Factories::models()`` 会搜索 **app/Models** 目录。

传递短类名
^^^^^^^^^^^^^^^^^^^^^^^

在以下代码中，如果你有 ``App\Models\UserModel``，实例将被返回：

.. literalinclude:: factories/001.php

如果你没有 ``App\Models\UserModel``，它会在所有命名空间中搜索 ``Models\UserModel``。

下次你在代码的任何地方请求同一个类时，工厂都会确保你得到与之前相同的实例：

.. literalinclude:: factories/003.php

传递带子目录的短类名
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果你想加载子目录中的类，可以使用 ``/`` 作为分隔符。如果存在，以下代码将加载 **app/Libraries/Sub/SubLib.php**：

.. literalinclude:: factories/013.php
   :lines: 2-

.. _factories-passing-fully-qualified-classname:

传递完全限定类名
---------------------------------

你也可以请求一个完全限定的类名：

.. literalinclude:: factories/002.php
   :lines: 2-

如果存在，它将返回 ``Blog\Models\UserModel`` 的实例。

.. note:: 在 v4.4.0 之前，当你请求一个完全限定的类名时，
    如果你只有 ``Blog\Models\UserModel``，实例将被返回。
    但如果你同时有 ``App\Models\UserModel`` 和 ``Blog\Models\UserModel``，
    则会返回 ``App\Models\UserModel`` 的实例。

    如果你想获取 ``Blog\Models\UserModel``，需要禁用选项 ``preferApp``：

    .. literalinclude:: factories/010.php
       :lines: 2-

便捷函数
*********************

为工厂提供了两个快捷函数。这些函数始终可用。

.. _factories-config:

config()
========

第一个是 :php:func:`config()`，它返回一个 Config 类的新实例。唯一需要的参数是类名：

.. literalinclude:: factories/008.php

model()
=======

第二个函数 :php:func:`model()` 返回一个 Model 类的新实例。唯一需要的参数是类名：

.. literalinclude:: factories/009.php

.. _factories-defining-classname-to-be-loaded:

定义要加载的类名
*******************************

.. versionadded:: 4.4.0

你可以使用 ``Factories::define()`` 方法在加载类之前定义要加载的类名：

.. literalinclude:: factories/014.php
   :lines: 2-

第一个参数是组件。第二个参数是类别名（工厂魔术静态方法的第一个参数），第三个参数是将要加载的真实完全限定类名。

之后，如果你用工厂加载 ``Myth\Auth\Models\UserModel``，将返回 ``App\Models\UserModel`` 的实例：

.. literalinclude:: factories/015.php
   :lines: 2-

工厂参数
******************

``Factories`` 将一个选项值数组（如下所述）作为第二个参数。这些指令将覆盖为每个组件配置的默认选项。

同时传递的任何其他参数都将被转发到类构造函数，从而可以轻松地动态配置你的类实例。例如，假设你的应用使用单独的数据库进行身份验证，并且你希望确保任何访问用户记录的尝试都通过该连接进行：

.. literalinclude:: factories/004.php

现在，每次从 ``Factories`` 加载 ``UserModel`` 时，实际上返回的都是使用备用数据库连接的类实例。

.. _factories-options:

工厂选项
*****************

默认行为可能并不适用于每个组件。例如，如果你的组件名称与其路径不匹配，或者你需要将实例限制为某种特定类。每个组件都有一组选项来指导发现和实例化过程。

========== ============== ==================================================================== ===========================================
Key        类型           描述                                                                 默认值
========== ============== ==================================================================== ===========================================
component  string 或 null 组件的名称（如果与静态方法不同）。可用于将一个组件别名为另一个组件。  ``null`` (默认为组件名称)
path       string 或 null 在命名空间/文件夹内用于查找类的相对路径。                            ``null`` (默认为组件名称，但首字母大写)
instanceOf string 或 null 匹配返回实例的类名。                                                 ``null`` (无过滤)
getShared  boolean        是否返回类的共享实例或加载一个新实例。                               ``true``
preferApp  boolean        App 命名空间中具有相同 basename 的类是否覆盖其他显式类请求。         ``true``
========== ============== ==================================================================== ===========================================

.. note:: 自 v4.4.0 起，``preferApp`` 仅在你请求
    :ref:`不带命名空间的类名 <factories-passing-classname-without-namespace>` 时才有效。

工厂行为
******************

选项可以通过以下三种方式之一应用（按优先级升序列出）：

* 一个配置类 ``Config\Factory``，其属性名与组件名称匹配。
* 静态方法 ``Factories::setOptions()``。
* 在调用时直接通过参数传递选项。

配置
==============

要设置默认组件选项，请在 **app/Config/Factory.php** 创建一个新的配置文件，该文件将选项作为与组件名称匹配的数组属性提供。

示例：过滤器工厂
--------------------------

例如，如果你想通过工厂创建 **过滤器**，组件名称将是 ``filters``。如果你希望确保每个过滤器都是实现了 CodeIgniter 的 ``FilterInterface`` 的类的实例，你的 **app/Config/Factory.php** 文件可能如下所示：

.. literalinclude:: factories/005.php

现在你可以使用 ``Factories::filters('SomeFilter')`` 这样的代码来创建一个过滤器，返回的实例必定是 CodeIgniter 的过滤器。

这可以防止与恰好在其命名空间中有无关 ``Filters`` 路径的第三方模块发生冲突。

示例：库工厂
--------------------------

如果你想使用 ``Factories::library('SomeLib')`` 在 **app/Libraries** 目录中加载你的库类，路径 `Libraries` 与默认路径 `Library` 不同。

在这种情况下，你的 **app/Config/Factory.php** 文件将如下所示：

.. literalinclude:: factories/011.php

现在你可以使用 ``Factories::library()`` 方法来加载你的库：

.. literalinclude:: factories/012.php
   :lines: 2-

setOptions 方法
=================

``Factories`` 类有一个静态方法允许运行时配置选项：只需使用 ``setOptions()`` 方法提供所需的选项数组，它们将与默认值合并并存储以供下一次调用使用：

.. literalinclude:: factories/006.php

参数选项
=================

``Factories`` 的魔术静态调用将一个选项值数组作为第二个参数。这些指令将覆盖为每个组件配置的存储选项，可以在调用时使用以获取你确切需要的内容。输入应该是一个数组，其选项名称作为键，每个覆盖值作为值。

例如，默认情况下 ``Factories`` 假定你想要定位组件的共享实例。通过向魔术静态调用添加第二个参数，你可以控制该单次调用是返回新实例还是共享实例：

.. literalinclude:: factories/007.php
   :lines: 2-

.. _factories-config-caching:

配置缓存
**************

.. versionadded:: 4.4.0

.. important:: 除非你已仔细阅读本节并理解此功能的工作原理，否则不要使用此功能。否则，你的应用程序将无法正常运行。

为了提高性能，已实现配置缓存。

前提条件
============

.. important:: 在不满足前提条件的情况下使用此功能将阻止 CodeIgniter 正常运行。在这种情况下不要使用此功能。

- 要使用此功能，工厂中实例化的所有 Config 对象的属性在实例化后不得被修改。换句话说，Config 类必须是不可变的或只读的类。
- 默认情况下，每个被缓存的 Config 类必须实现 ``__set_state()`` 方法。

工作原理
============

.. important:: 一旦缓存，配置值将永远不会改变，直到缓存被删除，即使配置文件或 **.env** 文件被更改也是如此。

- 在关闭前，如果工厂中的 Config 实例状态发生变化，则将所有 Config 实例保存到缓存文件中。
- 如果存在缓存，则在 CodeIgniter 初始化前恢复缓存的 Config 实例。

简而言之，工厂持有的所有 Config 实例在关闭前立即被缓存，且缓存的实例将永久使用。

如何更新配置值
===========================

一旦存储，缓存的版本永远不会过期。更改现有的 Config 文件（或为其更改环境变量）不会更新缓存或配置值。

因此，如果你想更新配置值，请更新 Config 文件或环境变量，并且必须手动删除缓存文件。

你可以使用 ``spark cache:clear`` 命令：

.. code-block:: console

    php spark cache:clear

或者直接删除 **writable/cache/FactoriesCache_config** 文件。

.. note::
    自 v4.5.0 起，``spark optimize`` 命令会清除缓存。

如何启用配置缓存
============================

.. versionadded:: 4.5.0

在 **app/Config/Optimize.php** 中将以下属性设置为 ``true``::

    public bool $configCacheEnabled = true;

或者你可以使用 ``spark optimize`` 命令启用它。

.. note::
    此属性不能被
    :ref:`环境变量 <configuration-classes-and-environment-variables>` 覆盖。

.. note::
    在 v4.4.x 中，取消注释 **public/index.php** 中的以下代码::

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
