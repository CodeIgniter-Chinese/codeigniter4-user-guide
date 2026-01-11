************************
扩展控制器
************************

不应修改 CodeIgniter 的核心控制器，但框架为你提供了一个默认的类扩展，位于 **app/Controllers/BaseController.php**。你创建的任何新控制器都应继承 ``BaseController``，以利用预加载的组件和你提供的任何附加功能：

.. literalinclude:: basecontroller/001.php

.. contents::
    :local:
    :depth: 2

预加载组件
=====================

基础控制器是加载项目每次运行所需使用的任何辅助函数、模型、库、服务等内容的理想位置。辅助函数应添加到预定义的 ``$helpers`` 数组中。例如，如果你希望 HTML 和文本辅助函数在所有地方都可用：

.. literalinclude:: basecontroller/002.php

任何其他需要加载的组件或需要处理的数据都应添加到构造函数 ``initController()`` 中。例如，如果你的项目大量使用 Session 库，你可能希望在这里初始化它：

.. literalinclude:: basecontroller/003.php

附加方法
==================

基础控制器本身不可路由。作为额外的安全措施，你创建的所有新方法都应声明为 ``protected`` 或 ``private``，并且只能通过你创建的继承自 ``BaseController`` 的控制器来访问。

其他选项
=============

你可能会发现需要不止一个基础控制器。你可以创建新的基础控制器，只要你创建的其他控制器都继承了正确的基类即可。例如，如果你的项目有一个复杂的公共接口和一个简单的管理门户，你可能希望将 ``BaseController`` 用于公共控制器，并为管理控制器创建一个 ``AdminController``。

如果你不想使用基础控制器，可以通过让你的控制器继承系统控制器来绕过它：

.. literalinclude:: basecontroller/004.php
