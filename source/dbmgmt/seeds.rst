################
数据库填充
################

数据库填充是一种向数据库添加数据的简单方法。在开发过程中尤其有用，当你需要使用示例数据填充数据库以便进行开发时，但并不仅限于此。填充器可以包含不适合放在迁移中的静态数据，例如国家、地理编码表、事件或设置信息等。

.. contents::
    :local:
    :depth: 2

****************
数据库填充器
****************

数据库填充器是简单的类，必须包含一个 ``run()`` 方法，并且继承 ``CodeIgniter\Database\Seeder``。在 ``run()`` 方法中，该类可以创建任何所需的数据。它可以通过 ``$this->db`` 和 ``$this->forge`` 分别访问数据库连接和 Forge。填充文件必须存储在 **app/Database/Seeds** 目录中。文件名必须与类名匹配。

.. literalinclude:: seeds/001.php

***************
嵌套填充器
***************

填充器可以通过 ``call()`` 方法调用其他填充器。这允许你轻松地组织一个中心填充器，但将任务分散到单独的填充器文件中：

.. literalinclude:: seeds/002.php

你也可以在 ``call()`` 方法中使用完全限定的类名，允许你将填充器放在任何自动加载器可以找到的地方。这对于更模块化的项目结构非常有用：

.. literalinclude:: seeds/003.php

*************
使用填充器
*************

你可以通过数据库配置类获取主填充器的实例：

.. literalinclude:: seeds/004.php

命令行填充
====================

你也可以通过命令行进行数据填充，作为迁移命令行工具的一部分，如果你不想创建一个专用的控制器：

.. code-block:: console

    php spark db:seed TestSeeder

*********************
创建填充器文件
*********************

通过命令行，你可以轻松地生成填充文件：

.. code-block:: console

    php spark make:seeder user --suffix

上述命令将输出位于 **app/Database/Seeds** 目录下的 **UserSeeder.php** 文件。

你可以通过提供 ``--namespace`` 选项来指定填充文件将存储的 ``root`` 命名空间：

对于 Unix 系统：

.. code-block:: console

    php spark make:seeder MySeeder --namespace Acme\\Blog

对于 Windows 系统：

.. code-block:: console

    php spark make:seeder MySeeder --namespace Acme\Blog

如果 ``Acme\Blog`` 映射到 **app/Blog** 目录，那么此命令将在 **app/Blog/Database/Seeds** 目录生成 **MySeeder.php** 文件。

提供 ``--force`` 选项将覆盖目标位置的现有文件。
