************************
扩展控制器
************************

CodeIgniter 的核心控制器不应该改变,但是在
**app/Controllers/BaseController.php** 提供了一个默认的类扩展。你创建的任何新控制器都应该扩展 ``BaseController`` 来利用预加载的组件和你提供的任何其他功能:

.. literalinclude:: basecontroller/001.php

.. contents::
    :local:
    :depth: 2

预加载组件
=====================

基础控制器是一个很好的地方,可以加载你打算在项目每次运行时使用的任何辅助函数、模型、类库、服务等。辅助函数应该添加到预定义的 ``$helpers`` 数组中。例如,如果你需要 HTML 和 Text 辅助函数在所有地方可用:

.. literalinclude:: basecontroller/002.php

需要加载的任何其他组件或要处理的数据应该添加到构造函数 ``initController()`` 中。例如,如果你的项目大量使用 Session 库,你可以在这里初始化它:

.. literalinclude:: basecontroller/003.php

其他方法
==================

基础控制器是不可路由的。作为一个额外的安全措施, **所有** 你创建的新方法都应该声明为 ``protected`` 或 ``private``,并且只能通过扩展 ``BaseController`` 的控制器访问它们。

其他选择
=============

你可能会发现需要多个基础控制器。只要其他控制器扩展正确的基础控制器,就可以创建多个基础控制器。例如,如果你的项目有复杂的公共接口和简单的管理门户,可以考虑让公共控制器扩展 ``BaseController``,为任何管理控制器创建 ``AdminController``。

如果你不想使用基础控制器,可以通过让控制器扩展系统的 Controller 来绕过它:

.. literalinclude:: basecontroller/004.php
