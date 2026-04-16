升级模型
##############

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.x 模型文档 <https://codeigniter.org.cn/userguide3/general/models.html>`_
- :doc:`CodeIgniter 4.x 模型文档 </models/model>`

变更内容
=====================

- CI4 的模型功能丰富得多，包括自动数据库连接、基础 CRUD、模型内验证以及自动分页。
- 由于 CodeIgniter 4 引入了命名空间，模型必须相应调整以支持命名空间。

升级指南
=============

1. 首先，将所有模型文件移动到 **app/Models** 文件夹中。
2. 在 <?php 后面紧接着添加这一行：``namespace App\Models;``。
3. 在 ``namespace App\Models;`` 这一行下面，添加这一行：``use CodeIgniter\Model;``。
4. 将 ``extends CI_Model`` 替换为 ``extends Model``。
5. 添加 ``protected $table`` 属性，并设置表名。
6. 添加 ``protected $allowedFields`` 属性，并设置允许插入/更新的字段名数组。
7. 不再使用 CI3 的 ``$this->load->model('x');``，现在应改用 ``$this->x = new X();``，并遵循组件的命名空间约定。或者，也可以使用 :php:func:`model()` 函数：``$this->x = model('X');``。

如果你的模型结构中使用了子目录，则必须据此调整命名空间。
例如：如果你的 v3 模型位于 **application/models/users/user_contact.php**，则命名空间必须为 ``namespace App\Models\Users;``，而在 v4 中的模型路径应如下所示：**app/Models/Users/UserContact.php**

CI4 中新的 Model 内置了许多方法。例如 ``find($id)`` 方法，可以用它查找主键等于 ``$id`` 的数据。
插入数据也比以前更简单了。CI4 提供了 ``insert($data)`` 方法。你可以根据需要使用这些内置方法，并将代码迁移到这些新方法上。

有关这些方法的更多信息，请参见 :doc:`../models/model`。

代码示例
============

CodeIgniter 3.x 版本
------------------------

路径：**application/models**：

.. literalinclude:: upgrade_models/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

路径：**app/Models**：

.. literalinclude:: upgrade_models/001.php

以上代码是从 CI3 到 CI4 的直接翻译。它在模型中直接使用了查询构建器。
请注意，直接使用查询构建器时，将无法使用 CodeIgniter 的模型功能。

如果你想使用 CodeIgniter 的模型功能，代码应如下所示：

.. literalinclude:: upgrade_models/002.php
