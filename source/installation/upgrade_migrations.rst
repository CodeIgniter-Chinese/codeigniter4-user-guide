升级迁移
##################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.x 数据库迁移文档 <https://codeigniter.org.cn/userguide3/libraries/migration.html>`_
- :doc:`CodeIgniter 4.x 数据库迁移文档 </dbmgmt/migration>`

变更内容
=====================

- 首先，迁移的顺序命名（``001_create_users``、``002_create_posts``）不再受支持。CodeIgniter 4 仅支持时间戳方案（``20121031100537_create_users``、``20121031500638_create_posts``）。如果你使用的是顺序命名，则必须重命名每个迁移文件。
- 迁移表的定义已更改。如果从 CI3 升级到 CI4 并使用同一个数据库，
  则需要升级迁移表的定义及其数据。
- 迁移流程也已更改。现在，你可以通过一条简单的 CLI 命令迁移数据库：

.. code-block:: console

    php spark migrate

升级指南
=============

1. 如果你的 v3 项目使用的是顺序迁移名称，则必须将其改为时间戳名称。
2. 必须将所有迁移文件移动到新的文件夹 **app/Database/Migrations**。
3. 如果存在，请移除这一行：``defined('BASEPATH') OR exit('No direct script access allowed');``。
4. 在 <?php 后面紧接着添加这一行：``namespace App\Database\Migrations;``。
5. 在 ``namespace App\Database\Migrations;`` 这一行下面，添加这一行：``use CodeIgniter\Database\Migration;``
6. 将 ``extends CI_Migration`` 替换为 ``extends Migration``。
7. ``Forge`` 类中的方法名已更改为小驼峰命名规则。例如：

    - ``$this->dbforge->add_field`` 改为 ``$this->forge->addField``
    - ``$this->dbforge->add_key`` 改为 ``$this->forge->addKey``
    - ``$this->dbforge->create_table`` 改为 ``$this->forge->addTable``
    - ``$this->dbforge->drop_table`` 改为 ``$this->forge->addTable``

8. （可选）可以将数组语法从 ``array(...)`` 改为 ``[...]``
9. 如果使用同一个数据库，请升级迁移表。

    - **（开发环境）** 在开发环境中运行 CI4 迁移，或在其他带有全新数据库的环境中运行，以创建新的迁移表。
    - **（开发环境）** 导出迁移表。
    - **（生产环境）** 删除（或重命名）现有的 CI3 迁移表。
    - **（生产环境）** 导入新的迁移表及其数据。

代码示例
============

CodeIgniter 3.x 版本
------------------------

路径：**application/migrations**：

.. literalinclude:: upgrade_migrations/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

路径：**app/Database/Migrations**：

.. literalinclude:: upgrade_migrations/001.php

搜索与替换
================

可以使用下表对旧的 CI3 文件执行搜索与替换。

+------------------------------+----------------------------+
| 搜索                         | 替换                       |
+==============================+============================+
| extends CI_Migration         | extends Migration          |
+------------------------------+----------------------------+
| $this->dbforge->add_field    | $this->forge->addField     |
+------------------------------+----------------------------+
| $this->dbforge->add_key      | $this->forge->addKey       |
+------------------------------+----------------------------+
| $this->dbforge->create_table | $this->forge->createTable  |
+------------------------------+----------------------------+
| $this->dbforge->drop_table   | $this->forge->dropTable    |
+------------------------------+----------------------------+
