=====================
测试你的数据库
=====================

.. contents::
    :local:
    :depth: 2


测试类
==============

为了让测试方便的利用 CodeIgniter 提供的嵌入式数据库工具，你的测试必须扩展至 ``CIDatabaseTestCase``::


    <?php namespace App\Database;

    use CodeIgniter\Test\CIDatabaseTestCase;

    class MyTests extends CIDatabaseTestCase
    {
        . . .
    }

因为在 ``setUp()`` 和 ``tearDown()`` 阶段专门的功能已完成，如果你要使用这些方法你必须确保你调用了父类方法，否则你会丢失许多下面描述的功能::


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

当运行数据库测试时，在测试期间你要提供一个能使用的数据库。框架对 CodeIgniter 提供明确的工具，代替使用 PHPUnit（PHP单元）嵌入的数据库特征。第一步要确保你在 **app/Config/Database.php** 文件下已经建立了一个 ``tests`` 数据库组。当运行测试的时候具体指定一个仅在测试时使用的数据库连接，用来保持你的其他数据安全。
如果你的团队有多名开发者，你将很可能要保持你的凭据保存在 **.env** 文件里。倘若这样做，编辑文件确保以下各行存在并具有正确的信息::


    database.tests.dbdriver = 'MySQLi';
    database.tests.username = 'root';
    database.tests.password = '';
    database.tests.database = '';


迁移与植入
--------------------

当运行测试时，你要确保你的数据库已经纠正了创建概要并且每个测试是已知的状态。通过对你的测试添加一对类属性，你能使用迁移与植入去创建你的数据库。
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

这样地 boolean（布尔）值决定在每一次测试之前是否数据库已经完整地更新了。如果为真，所有的迁移被回滚到版本 0，然后数据库被迁移到最新的可用迁移。

**$seed**

如果当前状态并不是空的，这样地具体指定的植入文件的名字对每一次测试运行是常被用作带优先的数据测试的填充数据库。

**$basePath**

默认情况下， CodeIgniter 将会在 **tests/_support/Database/Seeds** 查找定位的植入并且它应该在测试时间内运行。通过具体指定的 ``$basePath`` 属性你能改变同样的路径。类似这样的基本路径应该不包括 ``$basePath`` 目录，但是该路径对单独的目录来说支持子目录。


**$namespace**

默认情况下，CodeIgniter 将会在 **tests/_support/DatabaseTestMigrations/Database/Migrations**
查找定位迁移并且它应该在测试时间内运行。在 ``$namespace`` 属性里你能由具体指定的新的命名空间改变定位。类似这样的改变不包括 **Database/Migrations** 路径，仅是基础命名空间。



辅助方法
==============
在你的测试数据库里 **CIDatabaseTestCase** 类提供几个辅助方法去援助。

**seed($name)**

允许你手动加载一个植入到数据库里。最佳的参数值是要运行植入的名字。在 ``$basePath``里， 在具体指定的路径内植入必须是当前的。


**dontSeeInDatabase($table, $criteria)**

在数据库里，在 ``$criteria`` 里声明行标准匹配的 key/value(键/值)配对不存在。
::

    $criteria = [
        'email'  => 'joe@example.com',
        'active' => 1
    ];
    $this->dontSeeInDatabase('users', $criteria);

**seeInDatabase($table, $criteria)**

在数据库里，在 ``$criteria`` 里坚持行标准相配的 key/value(键/值)配对存在。
::

    $criteria = [
        'email'  => 'joe@example.com',
        'active' => 1
    ];
    $this->seeInDatabase('users', $criteria);

**grabFromDatabase($table, $column, $criteria)**

返回来自于特别指定表格的 ``$column`` 值，该表格的行与 ``$criteria`` 匹配。如果不止一行被找到，该方法只将紧靠第一个测试。

::

    $username = $this->grabFromDatabase('users', 'username', ['email' => 'joe@example.com']);

**hasInDatabase($table, $data)**

插入新行到数据库。在最近的测试运行后该行被移除。 ``$data`` 是插入到表格里带数据的联合数组。

::

    $data = [
        'email' => 'joe@example.com',
        'name'  => 'Joe Cool'
    ];
    $this->hasInDatabase('users', $data);

**seeNumRecords($expected, $table, $criteria)**

在数据库里，声明被找到的匹配行的数目与 ``$criteria`` 相匹配。

::

    $criteria = [
        'active' => 1
    ];
    $this->seeNumRecords(2, 'users', $criteria);

