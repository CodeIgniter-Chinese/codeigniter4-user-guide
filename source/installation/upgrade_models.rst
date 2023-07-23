升级模型
##############

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.X 模型文档 <http://codeigniter.com/userguide3/general/models.html>`_
- :doc:`CodeIgniter 4.X 模型文档 </models/model>`

变更点
=====================

- CI4 模型具有更多功能,包括自动数据库连接、基本 CRUD、模型内验证和自动分页。
- 由于 CodeIgniter 4 添加了命名空间,模型必须进行更改以支持命名空间。

升级指南
=============

1. 首先,将所有模型文件移到 **app/Models** 文件夹中。
2. 在打开的 php 标记之后添加此行:``namespace App\Models;``。
3. 在 ``namespace App\Models;`` 行的下面添加此行:``use CodeIgniter\Model;``。
4. 将 ``extends CI_Model`` 替换为 ``extends Model``。
5. 与 CI3 的 ``$this->load->model('x');`` 不同,你现在会使用 ``$this->x = new X();``,遵循组件的命名空间约定。或者,你可以使用 :php:func:`model()` 函数:``$this->x = model('X');``。

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

要插入数据,可以直接调用 ``$model->insert()``,因为这个方法在 CI4 中是内置的。
