升级模型
##############

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.x 模型文档 <http://codeigniter.com/userguide3/general/models.html>`_
- :doc:`CodeIgniter 4.x 模型文档 </models/model>`

变更点
=====================

- CI4 模型具有更多功能,包括自动数据库连接、基本 CRUD、模型内验证和自动分页。
- 由于 CodeIgniter 4 添加了命名空间,模型必须进行更改以支持命名空间。

升级指南
=============

1. 首先，将所有模型文件移动到文件夹 **app/Models**。
2. 在 PHP 标签的开头之后添加这一行：``namespace App\Models;``。
3. 在 ``namespace App\Models;`` 行的下面添加这一行：``use CodeIgniter\Model;``。
4. 将 ``extends CI_Model`` 替换为 ``extends Model``。
5. 添加 ``protected $table`` 属性并设置表名。
6. 添加 ``protected $allowedFields`` 属性并设置允许插入/更新的字段名称数组。
7. 代替 CI3 的 ``$this->load->model('x');``，你现在应该使用 ``$this->x = new X();``，遵循组件的命名空间约定。或者，你可以使用 :php:func:`model()` 函数：``$this->x = model('X');``。

如果在模型结构中使用子目录,则必须根据情况更改命名空间。
例如:你有一个版本 3 模型位于 **application/models/users/user_contact.php**,命名空间必须是 ``namespace App\Models\Users;``,版本 4 中的模型路径应如下所示:**app/Models/Users/UserContact.php**

CI4 中的新 Model 有很多内置方法。例如 ``find($id)`` 方法。使用它可以找到主键等于 ``$id`` 的数据。
插入数据现在也比以前更简单。在 CI4 中有一个 ``insert($data)`` 方法。你可以选择使用所有这些内置方法,并将代码迁移到新方法。

可以在 :doc:`../models/model` 中找到有关这些方法的更多信息。

代码示例
============

CodeIgniter 3.x 版本
------------------------

路径:**application/models**:

.. literalinclude:: upgrade_models/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

路径:**app/Models**:

.. literalinclude:: upgrade_models/001.php

上述代码是从 CI3 到 CI4 的直接翻译。它在模型中直接使用了查询构建器。请注意，当你直接使用查询构建器时，你将无法使用 CodeIgniter 模型中的功能。

如果你想使用 CodeIgniter 模型的功能，代码将是：

.. literalinclude:: upgrade_models/002.php
