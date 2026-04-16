#######
测试
#######

CodeIgniter 的设计初衷是简化框架与应用的测试流程。框架内置支持 `PHPUnit <https://phpunit.de/>`__，并提供了一系列便捷的辅助方法，确保应用的全方位测试过程轻松高效。

.. contents::
    :local:
    :depth: 3

*************
系统设置
*************

安装 PHPUnit
==================

CodeIgniter 的所有测试均基于 `PHPUnit <https://phpunit.de/>`__。在系统中安装 PHPUnit 共有两种方式。

Composer
--------

推荐使用 `Composer <https://getcomposer.org/>`__ 在项目内安装。虽然支持全局安装，但不建议这样做，以免日后与其他项目产生兼容性冲突。

请确保系统中已安装 Composer。在项目根目录（包含 application 和 system 目录的路径）下，在命令行输入以下命令：

.. code-block:: console

    composer require --dev phpunit/phpunit

此时将安装与当前 PHP 版本匹配的 PHPUnit。安装完成后，运行以下命令即可执行项目的所有测试：

.. code-block:: console

    vendor/bin/phpunit

Windows 用户请使用以下命令：

.. code-block:: console

    vendor\bin\phpunit

Phar
----

另一种选择是从 `PHPUnit <https://phpunit.de/getting-started/phpunit-9.html>`__ 官网下载 .phar 文件。这是一个独立文件，放置在项目根目录下即可。

************************
测试应用
************************

PHPUnit 配置
=====================

项目根目录下的 ``phpunit.xml.dist`` 文件用于控制单元测试。如果自行配置了 ``phpunit.xml``，则会覆盖该默认配置。

默认情况下，测试文件位于项目根目录的 **tests** 目录下。

测试类
==============

若要使用框架提供的增强工具，测试类必须继承 ``CodeIgniter\Test\CIUnitTestCase``。

测试文件的存放路径并无强制限制。建议提前制定存放规则，以便快速定位测试文件。

在本文档中，**app** 目录下的类对应的测试文件均存放在 **tests/app** 目录。例如，若要测试 **app/Libraries/Foo.php**，应在 **tests/app/Libraries/FooTest.php** 创建测试文件：

.. literalinclude:: overview/001.php

若要测试模型 **app/Models/UserModel.php**，其测试文件 **tests/app/Models/UserModelTest.php** 可能如下所示：

.. literalinclude:: overview/002.php

可根据测试风格或需求自由创建目录结构。为测试类设置命名空间时，由于 **app** 目录是 ``App`` 命名空间的根路径，所使用的类必须拥有相对于 ``App`` 的正确命名空间。

.. note:: 虽然不强制要求为测试类设置命名空间，但这有助于确保类名不发生冲突。

测试数据库结果时，必须在类中使用 :doc:`DatabaseTestTrait <database>`。

准备工作
--------

大多数测试在运行前都需要进行准备。PHPUnit 的 ``TestCase`` 提供了四个方法用于环境准备与清理::

    public static function setUpBeforeClass(): void
    public static function tearDownAfterClass(): void

    protected function setUp(): void
    protected function tearDown(): void

静态方法 ``setUpBeforeClass()`` 和 ``tearDownAfterClass()`` 在整个测试用例执行前后运行；而受保护方法 ``setUp()`` 和 ``tearDown()`` 则在每个测试方法运行间隙执行。

如果实现这些特殊函数，务必同时调用父类方法，以免影响继承类中的环境准备：

.. literalinclude:: overview/003.php

.. _testing-overview-traits:

Trait
------

常用的一种增强测试方式是使用 Trait 来整合不同测试用例的准备工作。``CIUnitTestCase`` 会自动检测类中的 Trait，并尝试运行与 Trait 同名的准备和清理方法（即 `setUp{NameOfTrait}()` 和 `tearDown{NameOfTrait}()`）。

例如，若需为部分测试用例添加身份验证，可以创建一个验证 Trait，并利用其中的 `setUp` 方法模拟用户登录：

.. literalinclude:: overview/006.php

.. literalinclude:: overview/022.php

额外断言
---------------------

``CIUnitTestCase`` 提供了以下实用的单元测试断言。

assertLogged($level, $expectedMessage)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

确保预期的日志信息确实已记录：

assertLogContains($level, $logMessage)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

确保日志记录中包含特定的消息片段。

.. literalinclude:: overview/007.php

assertEventTriggered($eventName)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

确保预期的事件确实已触发：

.. literalinclude:: overview/008.php

assertHeaderEmitted($header, $ignoreCase = false)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

确保确实发送了特定的 HTTP 标头或 Cookie：

.. literalinclude:: overview/009.php

.. note:: 使用此断言的测试用例应作为独立进程运行
    （使用 PHPUnit 中的 `@runInSeparateProcess annotation`_ 或 `RunInSeparateProcess attribute`_）。

.. _@runInSeparateProcess annotation: https://docs.phpunit.de/en/10.5/annotations.html#runinseparateprocess
.. _RunInSeparateProcess attribute: https://docs.phpunit.de/en/10.5/attributes.html#runinseparateprocess

assertHeaderNotEmitted($header, $ignoreCase = false)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

确保未发送特定的 HTTP 标头或 Cookie：

.. literalinclude:: overview/010.php

.. note:: 包含此断言的测试用例应在 PHPUnit 中作为独立进程运行
    （使用 `@runInSeparateProcess annotation`_ 或 `RunInSeparateProcess attribute`_）。

assertCloseEnough($expected, $actual, $message = '', $tolerance = 1)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

用于长时间执行的测试，验证预期时间与实际时间的绝对差值在指定误差范围内：

.. literalinclude:: overview/011.php

上述测试允许实际时间为 660 或 661 秒。

assertCloseEnoughString($expected, $actual, $message = '', $tolerance = 1)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

用于长时间执行的测试，验证格式化为字符串的时间，其预期值与实际值的绝对差值在指定误差范围内：

.. literalinclude:: overview/012.php

上述测试允许实际时间为 660 或 661 秒。

访问私有或受保护的属性
--------------------------------------

测试时，可使用以下 Getter 和 Setter 方法访问目标类中的受保护或私有成员。

getPrivateMethodInvoker($instance, $method)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

用于从类外部调用私有方法。返回一个可调用的函数。第一个参数是测试类的实例，第二个参数是待调用的方法名。

.. literalinclude:: overview/013.php

getPrivateProperty($instance, $property)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

从类实例中获取私有或受保护属性的值。第一个参数是测试类的实例，第二个参数是属性名。

.. literalinclude:: overview/014.php

setPrivateProperty($instance, $property, $value)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

为类实例中的受保护属性设置值。第一个参数是测试类的实例，第二个参数是属性名，第三个参数是待设置的值：

.. literalinclude:: overview/015.php

模拟服务
================

测试（尤其是控制器或集成测试）时，常需模拟 **app/Config/Services.php** 中定义的某个服务，以便在模拟服务响应的同时，将测试范围锁定在目标代码上。**Services** 类提供了以下简化模拟的方法。

Services::injectMock()
----------------------

用于定义 Services 类返回的具体实例。可通过此方法设置服务属性以模拟特定行为，或用模拟类替换原有服务。

.. literalinclude:: overview/016.php

第一个参数是待替换的服务名，必须与 Services 类中的函数名完全一致。第二个参数是替换后的实例。

Services::reset()
-----------------

移除所有模拟类，使 Services 类恢复初始状态。

也可使用 ``CIUnitTestCase`` 提供的 ``$this->resetServices()`` 方法。

.. note:: 此方法会重置 Services 的所有状态，导致 ``RouteCollection`` 中没有任何路由。如需加载路由，需手动调用 ``loadRoutes()`` 方法，例如 ``Services::routes()->loadRoutes()``。

Services::resetSingle(string $name)
-----------------------------------

根据名称移除单个服务的模拟实例和共享实例。

.. note:: ``Cache``、``Email`` 和 ``Session`` 服务默认会被模拟，以防止干扰测试环境。若不希望模拟这些服务，需从类属性中移除相应回调：``$setUpMethods = ['mockEmail', 'mockSession'];``。

模拟工厂实例
=========================

与服务类似，测试期间可能需要为 ``Factories`` 提供预配置的类实例。其静态方法 ``Factories::injectMock()`` 和 ``Factories::reset()`` 与 **Services** 的用法相同，但在首位多了一个组件名参数：

.. literalinclude:: overview/017.php

.. note:: 所有组件工厂在每次测试间默认都会重置。若需保留实例，请修改测试用例的 ``$setUpMethods``。

测试与时间
================

测试与时间相关的代码通常具有挑战性。但使用 :doc:`Time <../libraries/time>` 类时，可在测试期间随意固定或修改当前时间。

以下是固定当前时间的测试示例：

.. literalinclude:: overview/021.php

使用 ``Time::setTestNow()`` 方法可固定当前时间。第二个参数是可选的区域设置。

测试结束后，务必通过无参调用重置当前时间。
