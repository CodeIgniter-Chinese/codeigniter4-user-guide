################
数据库填充
################

数据库填充是向数据库中添加数据的一个简单方法。它在开发过程中特别有用,您需要用一些样本数据来填充数据库以进行开发,但它的用途不仅限于此。
填充器可以包含一些不想放入迁移文件的静态数据,像国家信息、地理编码表、事件或设置信息等等。

.. contents::
    :local:
    :depth: 2

****************
数据库填充器
****************

数据库填充器是简单的类,必须有一个 ``run()`` 方法,并扩展 ``CodeIgniter\Database\Seeder``。
在 ``run()`` 内,该类可以创建任何它需要的形式的数据。它可以通过 ``$this->db`` 和 ``$this->forge`` 访问数据库连接和伪造器。
填充文件必须存储在 **app/Database/Seeds** 目录中。文件名必须与类名匹配。

.. literalinclude:: seeds/001.php

***************
嵌套填充器
***************

填充器可以通过 ``call()`` 方法调用其他填充器。这使您可以轻松组织一个中心填充器,但将任务组织到单独的填充器文件中:

.. literalinclude:: seeds/002.php

在 ``call()`` 方法中,您也可以使用完全限定的类名,这使您可以将填充器保存在自动加载程序可以找到的任何地方。
这对于更模块化的代码库很有帮助:

.. literalinclude:: seeds/003.php

*************
使用填充器
*************

您可以通过数据库配置类获取主填充器的副本:

.. literalinclude:: seeds/004.php

命令行填充
====================

您也可以通过命令行作为迁移CLI工具的一部分从命令行填充数据,如果您不想创建一个专用的控制器::

    > php spark db:seed TestSeeder

*********************
创建填充器文件
*********************

使用命令行,您可以轻松生成填充器文件。

::

    > php spark make:seeder user --suffix
    // 输出:UserSeeder.php文件位于app/Database/Seeds目录中。

您可以通过提供 ``--namespace`` 选项来指定填充器文件要存储的 ``root`` 命名空间::

    For Unix:
    > php spark make:seeder MySeeder --namespace Acme\\Blog

    For Windows:
    > php spark make:seeder MySeeder --namespace Acme\Blog

如果 ``Acme\Blog`` 映射到 **app/Blog** 目录,那么此命令将在 **app/Blog/Database/Seeds** 目录中生成 **MySeeder.php**。

提供 ``--force`` 选项将覆盖目标位置中的现有文件。
