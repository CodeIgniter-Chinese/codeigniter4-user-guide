#################
官方包
#################

CodeIgniter 框架无法解决开发者遇到的所有问题。
许多用户表示他们喜欢该框架的小巧和快速，因此我们不想让核心框架变得臃肿。
为了弥补这一差距，我们发布了官方包来提供并非每个网站都需要或想要的额外功能。

.. contents::
    :local:
    :depth: 2

.. _shield:

******
Shield
******

`CodeIgniter Shield <https://shield.codeigniter.com/>`_ 是 CodeIgniter 4 的认证和授权框架。
它设计为安全、灵活且易于扩展，以满足多种不同类型网站的需求。
它包含众多功能，其中包括：

* 基于 Session 的认证
* 个人访问令牌认证
* 登录/注册后"操作"的框架（如双因素认证等）
* 基于角色的访问控制，具有简单灵活的权限管理
* 每个用户的权限覆盖
* 以及更多...

.. _settings:

********
Settings
********

`CodeIgniter Settings <https://settings.codeigniter.com>`_ 是对配置文件的封装，
允许将任何配置设置保存到数据库中，当没有存储自定义值时则默认使用配置文件。
这使得应用程序可以随附默认配置值，但随着项目增长或服务器迁移而自适应，无需修改代码。

************
Tasks (BETA)
************

`CodeIgniter Tasks <https://tasks.codeigniter.com>`_ 是 CodeIgniter 4 的简单任务调度器。
它允许你安排任务在特定时间运行，或以循环方式运行。
它设计为简单易用，但足够灵活以处理大多数用例。

************
Queue (BETA)
************

`CodeIgniter Queue <https://queue.codeigniter.com>`_ 是 CodeIgniter 4 的简单队列系统。
它允许你将任务排队以便稍后运行。

*****
Cache
*****

我们提供了一个包含 `PSR-6 和 PSR-16 缓存适配器 <https://github.com/codeigniter4/cache>`_
的库，用于 CodeIgniter 4。这不是必须使用的，因为 CodeIgniter 4 自带一个功能齐全的缓存组件。
此模块仅用于集成依赖 PSR 接口规范的第三方包。

******
DevKit
******

`CodeIgniter DevKit <https://github.com/codeigniter4/devkit>`_ 提供了 CodeIgniter 使用的所有开发工具，
以帮助确保代码质量，包括我们的编码规范、静态分析工具和规则、单元测试、数据生成、文件系统模拟、
安全建议等。这可以在你的任何个人项目或库中使用，让你快速配置 17 种不同的工具。

***************
编码标准
***************

`CodeIgniter 编码标准 <https://github.com/CodeIgniter/coding-standard>`_
包含了 CodeIgniter 的官方编码规范，基于 PHP CS Fixer 并由 Nexus CS Config 提供支持。
这可以在你自己的项目中使用，以形成一致的风格规则集合，可以自动应用于你的代码。
