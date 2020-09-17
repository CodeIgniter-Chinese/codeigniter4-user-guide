=====================
测试你的数据库
=====================

.. contents::
    :local:
    :depth: 2


测试类
==============

为了测试以便利用 CodeIgniter 提供的嵌入的数据库工具，你的测试必须扩展至 ``CIDatabaseTestCase``::


    <?php namespace App\Database;

    use CodeIgniter\Test\CIDatabaseTestCase;

    class MyTests extends CIDatabaseTestCase
    {
        . . .
    }

在 ``setUp()`` 和 ``tearDown()`` 阶段因为特殊功能已执行，如果你需要使用这些方法你必须保证你调用了父类的方法，否则你将丢失许多这里描述的功能::


    <?php namespace App\Database;

    use CodeIgniter\Test\CIDatabaseTestCase;

    class MyTests extends CIDatabaseTestCase
    {
        public function setUp()
        {
            parent::setUp();

            // 做点什么....
        }

        public function tearDown()
        {
            parent::tearDown();

            // 做点什么....
        }
    }


设置测试数据库
==========================

当运行数据库测试时，在测试期间你需要提供一个能使用的数据库。框架对 CodeIgniter 提供特殊的工具，代替使用 PHPUnit（PHP单元）嵌入的数据库特征。第一步要确保你在 **app/Config/Database.php** 文件下已经建立了一个 ``tests`` 数据库组。当运行测试的时候具体指定一个经常仅被使用的数据库连接，用来保持你的其他的数据安全。
如果在你的小组里你有符合的开发者，你将很可能要保持你的凭据保存在 **.env** 文件里。倘若这样做，编辑文件确保下面各行是父类并且确保信息是正确的::


    database.tests.dbdriver = 'MySQLi';
    database.tests.username = 'root';
    database.tests.password = '';
    database.tests.database = '';


迁移与植入
--------------------

当运行测试时，你需要确保你的数据库已经纠正了概要设置并且对每个测试是众所周知的状态。通过对你的测试添加一对类属性，你能使用迁移与植入去创建你的数据库。
::

    <?php namespace App\Database;

    use CodeIgniter\Test\CIDatabaseTestCase;

    class MyTests extends\CIDatabaseTestCase
    {
        protected $refresh  = true;
        protected $seed     = 'TestSeeder';
        protected $basePath = 'path/to/database/files';
    }

**$refresh**

这样地 boolean（布尔）值决定在每一次测试之前是否数据库已经完整地被刷新了。如果是真的，所有的迁移被回滚到版本 0，然后数据库被迁移到最新的可用迁移。

**$seed**

如果父类并不是空的，这样地具体指定的植入文件的名字对每一次测试运转是常被用作带优先的数据测试的填充数据库。

**$basePath**

默认情况下， CodeIgniter 将会在 **tests/_support/Database/Seeds** 查找定位的植入并且它应该在测试时间内运转。由具体指定的 ``$basePath`` 属性而言你能改变这样地路径。类似这样的属性应该不包括 ``$basePath`` 目录，但是这些路径对单独的目录来说支持子目录。


**$namespace**

默认情况下，CodeIgniter 将会在 **tests/_support/DatabaseTestMigrations/Database/Migrations**
查找定位迁移并且它应该在测试时间内运转。在 ``$namespace`` 属性里你能由具体指定的一个新的命名空间改变定位。类似这样的改变不包括 **Database/Migrations** 路径，仅是基础命名空间。



辅助方法
==============
在你的测试数据库里 **CIDatabaseTestCase** 类提供几个辅助方法去援助。

**seed($name)**

允许你手动加载一个植入到数据库里。最佳的参数值是操作植入的名字。在 ``$basePath`` 植入必须是在具体指定的路径内的父类。


**dontSeeInDatabase($table, $criteria)**

在 ``$criteria`` 里坚持行标准相配的 key/value(键/值)配对。在数据库里是不存在的。
::

    $criteria = [
        'email'  => 'joe@example.com',
        'active' => 1
    ];
    $this->dontSeeInDatabase('users', $criteria);

**seeInDatabase($table, $criteria)**

在 ``$criteria`` 里坚持行标准相配的 key/value(键/值)配对。在数据库里是存在的。
::

    $criteria = [
        'email'  => 'joe@example.com',
        'active' => 1
    ];
    $this->seeInDatabase('users', $criteria);

**grabFromDatabase($table, $column, $criteria)**

返回来自于特别指定表格的 ``$column`` 的值，该表格的行与 ``$criteria`` 相配。如果更多的行被找到，它将只能逆着第一个测试。

::

    $username = $this->grabFromDatabase('users', 'username', ['email' => 'joe@example.com']);

**hasInDatabase($table, $data)**

插入一个到数据库的新行。在最近的测试后该行被移除。 ``$data`` 是插入到表格里带数据的联合数组。

::

    $data = [
        'email' => 'joe@example.com',
        'name'  => 'Joe Cool'
    ];
    $this->hasInDatabase('users', $data);

**seeNumRecords($expected, $table, $criteria)**

在数据库里显示相配的数目列会被找到，数据库与 ``$criteria`` 相匹配。

::

    $criteria = [
        'active' => 1
    ];
    $this->seeNumRecords(2, 'users', $criteria);

