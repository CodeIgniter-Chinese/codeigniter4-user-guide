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

与 :doc:`./services` 类似，**工厂** 是自动加载的扩展，旨在保持代码简洁高效，同时无需在类之间传递对象实例。

工厂在以下几点上与 CodeIgniter 3 的 ``$this->load`` 相似：

- 加载类
- 共享已加载的类实例

最简单的情况下，工厂提供了一种创建类实例并从任何地方访问的通用方式。这是复用对象状态并减少因在应用中加载多个实例而产生内存负载的绝佳方法。

任何类都可以通过工厂加载，但最典型的例子是处理或传输公共数据的类。框架本身也在内部使用工厂，例如在使用 ``Config`` 类时确保加载正确的配置。

与服务的区别
=========================

工厂需要具体的类名进行实例化，且不包含创建实例的专门代码。

因此，工厂不适合创建需要许多依赖项的复杂实例，并且无法更改返回实例的类。

相比之下，服务拥有创建实例的代码，因此可以创建需要其他服务或类实例的复杂实例。获取服务时，服务需要的是服务名而非类名，因此可以在不更改客户端代码的情况下更改返回的实例。

.. _factories-loading-class:

加载类
***************

加载一个类
===============

以 **模型** 为例。可以通过调用工厂类类的魔术静态方法 ``Factories::models()`` 来访问专属于模型的工厂。

该静态方法名被称为 *组件*。

.. _factories-passing-classname-without-namespace:

传递不带命名空间的类名
-----------------------------------

如果传递不带命名空间的类名，工厂会首先在 ``App`` 命名空间中搜索与魔术静态方法名相对应的路径。
例如 ``Factories::models()`` 会搜索 **app/Models** 目录。

传递短类名
^^^^^^^^^^^^^^^^^^^^^^^

在以下代码中，如果存在 ``App\Models\UserModel``，则会返回其实例：

.. literalinclude:: factories/001.php

如果不存在 ``App\Models\UserModel``，则会在所有命名空间中搜索 ``Models\UserModel``。

下次在代码中任何位置请求同一个类时，工厂将确保获取与之前相同的实例：

.. literalinclude:: factories/003.php

在子目录中传递短类名
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果想加载子目录中的类，请使用 ``/`` 作为分隔符。
如果 **app/Libraries/Sub/SubLib.php** 存在，以下代码将加载该文件：

.. literalinclude:: factories/013.php
   :lines: 2-

.. _factories-passing-fully-qualified-classname:

传递完全限定类名
---------------------------------

也可以请求完全限定类名：

.. literalinclude:: factories/002.php
   :lines: 2-

如果存在 ``Blog\Models\UserModel``，则返回其实例。

.. note:: 在 v4.4.0 之前，请求完全限定类名时，如果仅存在 ``Blog\Models\UserModel``，则返回该实例。但如果同时存在 ``App\Models\UserModel`` 和 ``Blog\Models\UserModel``，则会返回 ``App\Models\UserModel`` 的实例。

    如果希望获取 ``Blog\Models\UserModel``，则需要禁用 ``preferApp`` 选项：

    .. literalinclude:: factories/010.php
       :lines: 2-

便捷函数
*********************

工厂提供了两个快捷函数。这些函数始终可用。

.. _factories-config:

config()
========

第一个是 :php:func:`config()`，返回 Config 类的新实例。唯一必需的参数是类名：

.. literalinclude:: factories/008.php

model()
=======

第二个函数 :php:func:`model()` 返回模型类的新实例。唯一必需的参数是类名：

.. literalinclude:: factories/009.php

.. _factories-defining-classname-to-be-loaded:

定义要加载的类名
*******************************

.. versionadded:: 4.4.0

可以在加载类之前使用 ``Factories::define()`` 方法定义要加载的类名：

.. literalinclude:: factories/014.php
   :lines: 2-

第一个参数是组件。第二个参数是类别名（工厂魔术静态方法的第一个参数），第三个参数是要加载的真实完全限定类名。

之后，如果使用工厂加载 ``Myth\Auth\Models\UserModel``，将返回 ``App\Models\UserModel`` 实例：

.. literalinclude:: factories/015.php
   :lines: 2-

工厂参数
******************

``Factories`` 接受一个选项值数组作为第二个参数（详见下文）。这些指令将覆盖为每个组件配置的默认选项。

同时传递的其他参数将转发给类的构造函数，从而可以轻松地动态配置类实例。例如，假设应用为身份验证使用独立的数据库，并希望确保所有访问用户记录的尝试始终通过该连接：

.. literalinclude:: factories/004.php

现在，每当从 ``Factories`` 加载 ``UserModel`` 时，实际上都会返回一个使用备用数据库连接的类实例。

.. _factories-options:

工厂选项
*****************

默认行为可能并不适用于所有组件。例如，组件名与其路径不一致，或者需要将实例限制为某种特定类型的类。每个组件都接受一组选项来指导发现和实例化。

========== ============== ============================================================ ===================================================
键名       类型           描述                                                         默认值
========== ============== ============================================================ ===================================================
component  string 或 null 组件名称（如果与静态方法名不同）。                           ``null`` （默认为组件名）
                          可用于将一个组件别名化为另一个。
path       string 或 null 在命名空间/文件夹内寻找类的相对路径。                        ``null`` （默认为组件名，但首字母大写）
instanceOf string 或 null 返回实例必须匹配的类名。                                     ``null`` （不进行过滤）
getShared  boolean        是返回类的共享实例还是加载新实例。                           ``true``
preferApp  boolean        App 命名空间中具有相同基名的类是否覆盖其他显式类请求。       ``true``
========== ============== ============================================================ ===================================================

.. note:: 自 v4.4.0 起，``preferApp`` 仅在请求 :ref:`不带命名空间的类名 <factories-passing-classname-without-namespace>` 时有效。

工厂行为
******************

可以通过以下三种方式之一应用选项（按优先级升序排列）：

* 一个配置类 ``Config\Factory``，其属性名与组件名匹配。
* 静态方法 ``Factories::setOptions()``。
* 调用时直接通过参数传递选项。

配置
==============

要设置默认组件选项，请在 **app/Config/Factory.php** 创建新的配置文件，并提供一个与组件名匹配的数组属性作为选项。

示例：过滤器工厂
--------------------------

例如，如果想通过工厂创建 **过滤器**，组件名称将为 ``filters``。如果想确保每个过滤器都是实现 CodeIgniter ``FilterInterface`` 的类实例，**app/Config/Factory.php** 文件可能如下所示：

.. literalinclude:: factories/005.php

现在可以使用 ``Factories::filters('SomeFilter')`` 这样的代码创建过滤器，返回的实例必定是 CodeIgniter 过滤器。

这可以防止与某些第三方模块发生冲突，因为这些模块的命名空间中可能恰好存在无关的 ``Filters`` 路径。

示例：类库工厂
--------------------------

如果想使用 ``Factories::library('SomeLib')`` 加载 **app/Libraries** 目录中的类，路径 `Libraries` 与默认路径 `Library` 不同。

在这种情况下，**app/Config/Factory.php** 文件将如下所示：

.. literalinclude:: factories/011.php

现在可以通过 ``Factories::library()`` 方法加载类：

.. literalinclude:: factories/012.php
   :lines: 2-

setOptions 方法
=================

``Factories`` 类有一个静态方法允许运行时配置选项：只需使用 ``setOptions()`` 方法提供所需的选项数组，它们将与默认值合并存储供下次调用：

.. literalinclude:: factories/006.php

参数选项
=================

``Factories`` 的魔术静态调用接受选项值数组作为第二个参数。这些指令将覆盖为每个组件配置的存储选项，并可在调用时精准获取所需内容。输入应为一个以选项名为键、覆盖值为值的数组。

例如，默认情况下 ``Factories`` 假设需要定位组件的共享实例。通过在魔术静态调用中添加第二个参数，可以控制该次调用返回新实例还是共享实例：

.. literalinclude:: factories/007.php
   :lines: 2-

.. _factories-config-caching:

配置缓存
**************

.. versionadded:: 4.4.0

.. important:: 除非仔细阅读本节并了解其工作原理，否则请勿使用此功能。否则，应用程序将无法正常运行。

为了提高性能，框架实现了配置缓存。

先决条件
============

.. important:: 在不满足先决条件的情况下使用此功能将导致 CodeIgniter 无法正常运行。在此类情况下请勿使用。

- 要使用此功能，工厂中实例化的所有 Config 对象属性在实例化后不得更改。换言之，Config 类必须是不可变或只读类。
- 默认情况下，每个被缓存的 Config 类都必须实现 ``__set_state()`` 方法。

工作原理
============

.. important:: 一旦缓存，配置值在删除缓存前绝不会更改，即使修改了配置文件或 **.env** 也是如此。

- 如果工厂中的 Config 实例状态发生变化，在框架执行结束前将工厂中的所有 Config 实例保存到缓存文件中。
- 如果缓存可用，在 CodeIgniter 初始化前恢复缓存的 Config 实例。

简而言之，工厂持有的所有 Config 实例都会在框架执行结束前立即缓存，并永久使用缓存实例。

如何更新配置值
===========================

存储后，缓存版本永不过期。修改现有的配置文件（或更改其环境变量）不会更新缓存或配置值。

因此，如果想更新配置值，在更新配置文件或环境变量后，必须手动删除缓存文件。

可以使用 ``spark cache:clear`` 命令：

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

或者可以使用 ``spark optimize`` 命令启用。

.. note::
    此属性无法通过 :ref:`环境变量 <configuration-classes-and-environment-variables>` 覆盖。

.. warning:: 在 :doc:`Worker 模式 </installation/worker_mode>` 下运行应用时，请勿使用此选项。
