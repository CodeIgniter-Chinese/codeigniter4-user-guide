################
数据库填充
################

数据库填充是向数据库添加数据的简便方法。这在开发期间特别有用，可用于填充开发所需的样本数据，但不限于此。数据库填充可包含不希望放入迁移文件中的静态数据，例如国家列表、地理编码表、事件或设置信息等。

.. contents::
    :local:
    :depth: 2

****************
数据库填充类
****************

数据库填充类是必须包含 ``run()`` 方法且继承自 ``CodeIgniter\Database\Seeder`` 的简单类。在 ``run()`` 方法中，该类可以创建所需的任何形式的数据。可分别通过 ``$this->db`` 和 ``$this->forge`` 使用数据库连接和 Forge 类。填充文件必须存放在 **app/Database/Seeds** 目录下，且文件名必须与类名匹配。

.. literalinclude:: seeds/001.php

***************
嵌套填充
***************

可使用 ``call()`` 方法调用其他填充类。由此可轻松组织一个中心填充类，并将具体任务拆分到独立的填充文件中：

.. literalinclude:: seeds/002.php

``call()`` 方法也支持完全限定类名，这样就能将填充类放置在自动加载器可找到的任何位置。这对于模块化代码库非常有用：

.. literalinclude:: seeds/003.php

*************
使用填充类
*************

可通过数据库配置类获取主填充类的实例：

.. literalinclude:: seeds/004.php

使用不同的数据库组
================================

获取填充类实例时，可通过第一个参数指定不同的数据库组名称：

.. literalinclude:: seeds/005.php

使用 ``call()`` 运行子填充类时，数据库连接会自动传递。这意味着除非子填充类显式设置了自身的 ``$DBGroup`` 属性，否则将使用与父类相同的连接。

如果填充类无论父类连接如何都必须使用特定数据库组，可在类中设置 ``$DBGroup`` 属性：

.. literalinclude:: seeds/006.php

连接优先级如下：

1. 若在填充类中设置了 ``$DBGroup``，则始终使用该连接组。
2. 否则，若传递了连接（来自父类的 ``call()`` 或 ``Database::seeder()``），则使用该连接。
3. 否则，使用默认连接组。

命令行填充
====================

如果不希望创建专门的控制器，也可作为迁移 CLI 工具的一部分，通过命令行填充数据：

.. code-block:: console

    php spark db:seed TestSeeder

*********************
创建填充文件
*********************

使用命令行可轻松生成填充文件：

.. code-block:: console

    php spark make:seeder user --suffix

上述命令将在 **app/Database/Seeds** 目录下生成 **UserSeeder.php** 文件。

通过 ``--namespace`` 选项可指定存放填充文件的根命名空间：

Unix 环境：

.. code-block:: console

    php spark make:seeder MySeeder --namespace Acme\\Blog

Windows 环境：

.. code-block:: console

    php spark make:seeder MySeeder --namespace Acme\Blog

若 ``Acme\Blog`` 映射到 **app/Blog** 目录，则此命令将在 **app/Blog/Database/Seeds** 目录下生成 **MySeeder.php**。

使用 ``--force`` 选项将覆盖目标位置的现有文件。
