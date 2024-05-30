#######
测试
#######

CodeIgniter 从一开始就尽可能地简化了框架和应用程序的测试。对 `PHPUnit <https://phpunit.de/>`__ 的支持是内置的,框架还提供了许多方便的辅助方法,使得对应用程序的各个方面的测试变得尽可能轻松。

.. contents::
  :local:
  :depth: 3

*************
系统设置
*************

安装 PHPUnit
==================

CodeIgniter 使用 `PHPUnit <https://phpunit.de/>`__ 作为所有测试的基础。有两种在系统内安装 PHPUnit 的方法。

Composer
--------

推荐的方法是使用 `Composer <https://getcomposer.org/>`__ 在项目中安装它。尽管可以全局安装,但我们不建议这样做,因为随着时间的推移,它可能与系统上的其他项目造成兼容性问题。

确保系统中安装了 Composer。从项目根目录(包含应用程序和系统目录的目录)命令行输入以下命令:

.. code-block:: console

    composer require --dev phpunit/phpunit

这将为当前 PHP 版本安装正确的版本。完成后,可以通过输入以下命令来运行此项目的所有测试:

.. code-block:: console

    vendor/bin/phpunit

如果使用 Windows,请使用以下命令:

.. code-block:: console

    vendor\bin\phpunit

Phar
----

另一种选择是从 `PHPUnit <https://phpunit.de/getting-started/phpunit-9.html>`__ 站点下载 .phar 文件。这是一个独立的文件,应该放在项目根目录中。

************************
测试应用程序
************************

PHPUnit 配置
=====================

在你的 CodeIgniter 项目根目录中，有一个 ``phpunit.xml.dist`` 文件。这个文件控制着你的应用程序的单元测试。如果你提供了自己的 ``phpunit.xml``，它将覆盖默认文件。

默认情况下，测试文件放置在项目根目录下的 **tests** 目录中。

测试类
==============

为了利用提供的额外工具，你的测试必须继承 ``CodeIgniter\Test\CIUnitTestCase``。

对于测试文件的放置位置没有硬性规定。然而，我们建议你提前制定放置规则，以便你能快速了解测试文件的位置。

在本文档中，我们将把与 **app** 目录中的类对应的测试文件放置在 **tests/app** 目录中。要测试一个新的库 **app/Libraries/Foo.php**，你需要在 **tests/app/Libraries/FooTest.php** 创建一个新文件：

.. literalinclude:: overview/001.php

要测试你的某个模型 **app/Models/UserModel.php**，你可能会在 **tests/app/Models/UserModelTest.php** 中得到如下内容：

.. literalinclude:: overview/002.php

你可以创建任何适合测试风格或需求的目录结构。在给测试类加命名空间时,请记住 **app** 目录是 ``App`` 命名空间的根目录,因此所使用的任何类都必须与 ``App`` 具有正确的相对命名空间。

.. note:: 对测试类使用命名空间不是强制的,但它有助于确保类名不冲突。

在测试数据库结果时,必须在类中使用 :doc:`DatabaseTestTrait <database>`。

搭建环境
-----------

大多数测试都需要一些准备才能正确运行。PHPUnit 的 ``TestCase`` 提供了四个方法来帮助搭建环境和清理::

    public static function setUpBeforeClass(): void
    public static function tearDownAfterClass(): void

    protected function setUp(): void
    protected function tearDown(): void

静态方法 ``setUpBeforeClass()`` 和 ``tearDownAfterClass()`` 分别在整个测试用例之前和之后运行,而受保护的方法 ``setUp()`` 和 ``tearDown()`` 在每个测试之间运行。

如果你实现了这些特殊函数中的任何一个，请确保你也运行它们的父级函数，以免扩展的测试用例干扰到分阶段测试：

.. literalinclude:: overview/003.php

.. _testing-overview-traits:

Traits
------

通过 traits 统一不同测试用例的环境搭建是一个加强测试的常用方式。``CIUnitTestCase`` 将检测任何类 traits,并查找以 trait 本身命名的环境搭建方法(即 `setUp{TraitName}()` 和 `tearDown{TraitName}()`)。

例如,如果你需要在某些测试用例中添加认证,可以创建一个具有假登录用户设置方法的认证 trait:

.. literalinclude:: overview/006.php

.. literalinclude:: overview/022.php

其他断言
---------------------

``CIUnitTestCase`` 提供了你可能会发现有用的其他单元测试断言。

assertLogged($level, $expectedMessage)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

确保预期的内容确实已记录到日志:

assertLogContains($level, $logMessage)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

确保日志中存在包含消息片段的记录:

.. literalinclude:: overview/007.php

assertEventTriggered($eventName)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

确保预期触发的事件确实被触发了:

.. literalinclude:: overview/008.php

assertHeaderEmitted($header, $ignoreCase = false)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

确保标头或 Cookie 已实际发送:

.. literalinclude:: overview/009.php

.. note:: 带有此内容的测试用例应 `在 PHPunit 中作为单独进程运行 <https://docs.phpunit.de/en/9.6/annotations.html#runinseparateprocess>`_。

assertHeaderNotEmitted($header, $ignoreCase = false)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

确保标头或 Cookie 没有被发送:

.. literalinclude:: overview/010.php

.. note:: 带有此内容的测试用例应 `在 PHPunit 中作为单独进程运行 <https://docs.phpunit.de/en/9.6/annotations.html#runinseparateprocess>`_。

assertCloseEnough($expected, $actual, $message = '', $tolerance = 1)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

对于延长执行时间的测试,测试预期时间与实际时间之间的绝对差值是否在允许公差范围内:

.. literalinclude:: overview/011.php

上面的测试将允许实际时间为 660 或 661 秒。

assertCloseEnoughString($expected, $actual, $message = '', $tolerance = 1)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

对于延长执行时间的测试,测试格式化为字符串的预期和实际时间之间的绝对差值是否在允许公差范围内:

.. literalinclude:: overview/012.php

上面的测试将允许实际时间为 660 或 661 秒。

访问 Protected/Private 属性
--------------------------------------

在测试期间,可以使用以下 setter 和 getter 方法访问要测试类中的 protected 和 private 方法和属性。

getPrivateMethodInvoker($instance, $method)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

启用你从类外调用私有方法。它返回一个可调用的函数。第一个参数是要测试的类的实例。第二个参数是要调用的方法名称。

.. literalinclude:: overview/013.php

getPrivateProperty($instance, $property)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

从类的实例中检索私有/受保护类属性的值。第一个参数是要测试的类的实例。第二个参数是属性名称。

.. literalinclude:: overview/014.php

setPrivateProperty($instance, $property, $value)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在类实例中设置受保护的值。第一个参数是要测试的类的实例。第二个参数是要设置值的属性名称。第三个参数是要设置的值:

.. literalinclude:: overview/015.php

模拟服务
================

在测试中,你经常会发现需要模拟 **app/Config/Services.php** 中定义的服务之一,以将测试限制于仅检查相关代码,同时模拟服务的各种响应。这在测试控制器和其他集成测试中尤其如此。**Services** 类提供了以下方法来简化此操作。

Services::injectMock()
----------------------

此方法允许你定义 Services 类将返回的确切实例。你可以使用它来设置服务的属性,以使其以某种方式运行,或将服务替换为模拟类。

.. literalinclude:: overview/016.php

第一个参数是要替换的服务。名称必须与 Services 类中的函数名称完全匹配。第二个参数是要替换的实例。

Services::reset()
-----------------

从 Services 类中删除所有模拟类,将其恢复到原始状态。

你也可以使用 ``CIUnitTestCase`` 提供的 ``$this->resetServices()`` 方法。

.. note:: 此方法会重置所有服务的状态，并且 ``RouteCollection`` 将不包含任何路由。如果你想要使用加载的路由，你需要调用 ``loadRoutes()`` 方法，例如 ``Services::routes()->loadRoutes()``。

Services::resetSingle(string $name)
-----------------------------------

通过名称删除单个服务的所有模拟和共享实例。

.. note:: ``Cache``、``Email`` 和 ``Session`` 服务默认进行模拟,以防止侵入式测试行为。要阻止模拟,请从类属性中删除方法回调:``$setUpMethods = ['mockEmail', 'mockSession'];``

模拟 Factory 实例
=========================

与 Services 类似,在测试期间你可能需要提供预先配置的类实例用于 ``Factories``。像 **Services** 一样使用相同的 ``Factories::injectMock()`` 和 ``Factories::reset()`` 静态方法,但它们需要在前面附加组件名称作为额外参数:

.. literalinclude:: overview/017.php

.. note:: 所有组件工厂在每个测试之间默认重置。如果需要实例持久化,请修改测试用例的 ``$setUpMethods``。

测试和时间
================

测试依赖于时间的代码可能会很有挑战性。然而，当使用 :doc:`Time <../libraries/time>` 类时，可以在测试期间随意固定或更改当前时间。

下面是一个固定当前时间的样本测试代码：

.. literalinclude:: overview/021.php

你可以使用 ``Time::setTestNow()`` 方法来固定当前时间。可选地，你可以指定一个语言环境作为第二个参数。

不要忘记在测试后调用该方法（不带参数）来重置当前时间。
