升级控制器
###################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.X 控制器文档 <http://codeigniter.com/userguide3/general/controllers.html>`_
- :doc:`CodeIgniter 4.X 控制器文档 </incoming/controllers>`

变更点
=====================

- 由于 CodeIgniter 4 添加了命名空间,必须对控制器进行更改以支持命名空间。
- CI4 控制器的构造函数不会自动将核心类加载到属性中。
- CI4 的控制器有一个特殊的构造函数 :ref:`initController() <controller-constructor>`。
- CI4 为你提供了 :doc:`Request </incoming/incomingrequest>` 和 :doc:`Responses </outgoing/response>`
  对象来使用 - 比 CI3 的方式更强大。
- 如果你需要一个基类控制器(CI3 中的 ``MY_Controller``),请使用 **app/Controllers/BaseController.php**。

升级指南
=============

1. 首先,将所有控制器文件移动到 **app/Controllers** 文件夹中。
2. 在打开的 php 标签之后添加此行:``namespace App\Controllers;``
3. 将 ``extends CI_Controller`` 替换为 ``extends BaseController``。
4. 如果存在,请删除 ``defined('BASEPATH') OR exit('No direct script access allowed');`` 这一行。

| 如果你在控制器结构中使用子目录,则必须根据情况更改命名空间。
  例如,你有一个版本 3 控制器位于 **application/controllers/users/auth/Register.php**,
  则命名空间必须是 ``namespace App\Controllers\Users\Auth;``,
  版本 4 中的控制器路径应如下所示:**app/Controllers/Users/Auth/Register.php**。
  请确保子目录的首字母大写。
| 之后,你必须在命名空间定义下面插入一个 ``use`` 语句,以扩展 ``BaseController``::
    ``use App\Controllers\BaseController;``

代码示例
============

CodeIgniter 3.x 版本
------------------------

路径:**application/controllers**:

.. literalinclude:: upgrade_controllers/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

路径:**app/Controllers**:

.. literalinclude:: upgrade_controllers/001.php
