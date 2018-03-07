#######
测试
#######


CodeIgniter 的构建是为了尽可能简单地测试框架和应用程序。
 ``PHPUnit`` 的支持是内置的，而且是 ``PHPUnit.xml`` 已经为您的应用程序设置好了。
它还提供了许多方便的助手方法来测试应用程序的各个方面。
尽可能简单。

.. contents::
    :local:
    :depth: 2

========================
测试你的应用
========================

Test 类
==============

为了利用提供的额外工具，你的 Test 类必须继承 ``\CIUnitTestCase``::

    class MyTests extends \CIUnitTestCase
    {
        . . .
    }

.. 注意:: 更多计划的特性, 暂时没有实现。 请继续关注。

Services 模拟
================

你经常会发现你需要模拟一个 **application/Config/Services.php**  限制你的测试相关问题的代码，同时模拟来自 services 的各种响应。 这特别在测试控制器和其他集成测试时是否正确。
 CodeIgniter 使这变得简单。

在测试模式下，系统在 **Service** 类上加载一个包装器，它提供了两个新方法， ``injectMock()`` 和 ``reset()`` 。

**injectMock()**

该方法允许您定义将由服务类返回的确切实例。 你可以用这个设置 Services 的属性，以便它以某种方式表现，或者用一个模拟的类替换服务。
::

    public function testSomething()
    {
        $curlrequest = $this->getMockBuilder('CodeIgniter\HTTP\CURLRequest')
                            ->setMethods(['request'])
                            ->getMock();
        Services::injectMock('curlrequest', $curlrequest);

        // Do normal testing here....
    }

第一个参数是要替换的 service 。 名称必须与 Services 中的函数名相匹配。
类完全。 第二个参数是替换它的实例。

**reset()**

删除 Services 类中的所有被模拟的类，并将其恢复到原来的状态。

=====================
测试数据库
=====================

测试类
==============

为了利用 CodeIgniter 为测试提供的内置数据库工具，你的测试必须继承 ``\ CIDatabaseTestCase`` ::

    class MyTests extends \CIDatabaseTestCase
    {
        . . .
    }

因为在 ``setUp()`` 和 ``tearDown()`` 阶段中运行特殊的功能，所以必须确保存在。
如果你需要使用这些方法，你可以调用父方法，否则你将缺少很多这里描述的功能。
::

    class MyTests extends \CIDatabaseTestCase
    {
        public function setUp()
        {
            parent::setUp();

            // Do something here....
        }


        public function tearDown()
        {
            parent::tearDown();

            // Do something here....
        }
    }

测试数据库设置
===================

在运行数据库测试时，您需要提供一个可以在测试期间使用的数据库。 而不是
使用 PHPUnit 内置的数据库特性，框架提供了特定于 CodeIgniter 的工具。 第一个
一步是确保你有一个 ``tests`` 数据库组设置在 **application/Config/Database.php** 。
 它指定只在运行测试时使用的数据库连接，以保证其他数据的安全。

如果您的团队中有多个开发人员，那么您可能希望保留您的凭证存储 **.env** 。 为了做到这一点，编辑文件以确保下面的行是存在的，并拥有正确的信息::

    database.tests.dbdriver = 'MySQLi';
    database.tests.username = 'root';
    database.tests.password = '';
    database.tests.database = '';

Migrations 和 Seeds
--------------------

在运行测试时，您需要确保数据库具有正确的模式设置。
每个测试都处于一个已知的状态。您可以使用 migrations 和 seeds 来设置数据库，
通过在测试中添加几个类属性。
::

    class MyTests extends \CIDatabaseTestCase
    {
        protected $refresh = true;
        protected $seed    = 'TestSeeder';
        protected $basePath = 'path/to/database/files';
    }

**$refresh**

boolean 决定在每次测试之前数据库是否完全刷新。 如果正确,
全部迁移回滚到版本 0 , 然后将数据库迁移到最新的可用迁移。

**$seed**

如果存在且不为空， 则根据指定要使用的 Seed 文件的名称， 在每次测试运行之前测试数据。

**$basePath**

默认情况下, CodeIgniter 会定位在 **tests/_support/database/migrations** 和 **tests/_support_database/seeds** 测试期间应该运行的 migrations 和 seeds。
 你可以通过指定 ``$basePath`` 路径来更改此目录。 这不应该包括 **migrations** 或 **seeds** 目录, 应该指向包含两个子目录的单个目录的路径。

辅助方法
==============

**CIDatabaseTestCase** 类提供了一些辅助方法,以帮助您测试您的数据库。

**seed($name)**

允许您手动将 Seed 加载到数据库中。 唯一的参数是要运行的 seed 的名称。 seed
必须在 ``$basePath`` 中指定的路径中存在pe。

**dontSeeInDatabase($table, $criteria)**

Asserts 在数据库中不存在匹配 ``$criteria`` 中 key/value 对的标准的行。
::

    $criteria = [
        'email' => 'joe@example.com',
        'active' => 1
    ];
    $this->dontSeeInDatabase('users', $criteria);

**seeInDatabase($table, $criteria)**

Asserts 在数据库中存在匹配 ``$criteria`` 中 key/value 对的标准的行。
::

    $criteria = [
        'email' => 'joe@example.com',
        'active' => 1
    ];
    $this->seeInDatabase('users', $criteria);

**grabFromDatabase($table, $column, $criteria)**

从列匹配 ``$criteria`` 的指定表中返回 ``$column`` 的值。如果不止一行被发现，它只会测试第一个。
::

    $username = $this->grabFromDatabase('users', 'username', ['email' => 'joe@example.com']);

**hasInDatabase($table, $data)**

将新的一行数据插入到数据库中。 此行在当前测试运行后删除。 ``$ data`` 是一个关联
将数据数组插入到表中。
::

    $data = [
        'email' => 'joe@example.com',
        'name'  => 'Joe Cool'
    ];
    $this->hasInDatabase('users', $data);

**seeNumRecords($expected, $table, $criteria)**

Asserts 在数据库中找到匹配 ``$criteria`` 的匹配行数。
::

    $criteria = [
        'deleted' => 1
    ];
    $this->seeNumRecords(2, 'users', $criteria);
