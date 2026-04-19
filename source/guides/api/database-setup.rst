.. _ci47-rest-part3:

创建数据库与模型
###############################

.. contents::
    :local:
    :depth: 2

本节将通过为 ``books`` 资源创建 SQLite 数据库表、填充示例数据并定义访问模型来构建数据层。完成后，将获得一个包含示例数据的 ``books`` 表。

创建迁移
=====================

迁移通过定义应用与回滚逻辑，实现对数据库架构的版本控制。下面为简单的 ``authors`` 和 ``books`` 表创建迁移。

运行 Spark 命令：

.. code-block:: console

    php spark make:migration CreateAuthorsTable
    php spark make:migration CreateBooksTable

这将在 **app/Database/Migrations/** 目录下创建新文件。

将 **app/Database/Migrations/CreateAuthorsTable.php** 修改为：

.. literalinclude:: code/004.php

在本示例中，作者仅需姓名。已将姓名设为唯一键以防止重复。

现在，将 **app/Database/Migrations/CreateBooksTable.php** 修改为：

.. literalinclude:: code/005.php

其中包含指向 ``authors`` 表的外键引用。由此可将每本书与作者关联，并统一管理作者姓名。

运行迁移：

.. code-block:: console

    php spark migrate

此时，数据库已具备存储图书与作者记录所需的结构。

创建数据填充
===============

数据填充用于在开发阶段加载示例数据，以便立即开展工作。此处将添加一些示例图书及其作者。

运行：

.. code-block:: console

    php spark make:seeder BookSeeder

修改 **app/Database/Seeds/BookSeeder.php** 文件：

.. literalinclude:: code/006.php

该填充器先向 ``authors`` 表插入作者信息并获取其 ID，随后使用这些 ID 向 ``books`` 表插入图书数据。

然后运行数据填充：

.. code-block:: console

    php spark db:seed BookSeeder

此时应看到记录已插入的确认信息。

创建 Book 模型
=====================

模型为数据表提供了面向对象接口与流畅的查询 API，使数据库访问变得简单且易于复用。接下来为 ``authors`` 和 ``books`` 表创建模型。

生成模型：

.. code-block:: console

   php spark make:model AuthorModel
   php spark make:model BookModel

这两个模型都将简单地继承 CodeIgniter 的基础模型类。

修改 **app/Models/AuthorModel.php**：

.. literalinclude:: code/007.php

修改 **app/Models/BookModel.php**：

.. literalinclude:: code/008.php

这会告知 CodeIgniter 使用哪张表，以及哪些字段允许批量赋值。

下一节将使用这些新模型来构建 RESTful API 控制器。届时将构建 ``/api/books`` 接口，并了解 CodeIgniter 的 ``Api\ResponseTrait`` 如何简化 CRUD 操作。
