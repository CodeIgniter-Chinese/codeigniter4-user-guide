升级控制器
###################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.x 控制器文档 <https://codeigniter.org.cn/userguide3/general/controllers.html>`_
- :doc:`CodeIgniter 4.x 控制器文档 </incoming/controllers>`

变更内容
=====================

- 由于 CodeIgniter 4 添加了命名空间，控制器必须修改以支持命名空间。
- CI4 控制器的构造函数不会自动将核心类加载到属性中。
- CI4 的控制器有一个特殊构造函数 :ref:`initController() <controller-constructor>`。
- CI4 提供了 :doc:`Request </incoming/incomingrequest>` 和 :doc:`Responses </outgoing/response>` 对象供使用，比 CI3 的方式更强大。
- 如果你需要一个基础控制器（CI3 中的 ``MY_Controller``），请使用 **app/Controllers/BaseController.php**。
- 在控制器中调用 ``echo`` （如 CI3 中）仍然支持，但建议从控制器返回字符串或 Response 对象。

升级指南
=============

1. 首先，将所有控制器文件移动到 **app/Controllers** 文件夹。
2. 在 php 开始标签之后添加这一行：``namespace App\Controllers;``
3. 将 ``extends CI_Controller`` 替换为 ``extends BaseController``。
4. 如果存在，删除这一行：``defined('BASEPATH') OR exit('No direct script access allowed');``。

| 如果你的控制器结构中使用了子目录，需要根据目录修改命名空间。
| 例如，版本 3 的控制器位于 **application/controllers/users/auth/Register.php**，
    命名空间应为 ``namespace App\Controllers\Users\Auth;``，版本 4 的控制器路径应为 **app/Controllers/Users/Auth/Register.php**。确保子目录首字母大写。
| 此后，需要在命名空间定义下插入 ``use`` 语句以继承 ``BaseController``：
    ``use App\Controllers\BaseController;``

代码示例
============

CodeIgniter 3.x 版本
------------------------

路径：**application/controllers**：

.. literalinclude:: upgrade_controllers/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

路径：**app/Controllers**：

.. literalinclude:: upgrade_controllers/001.php
