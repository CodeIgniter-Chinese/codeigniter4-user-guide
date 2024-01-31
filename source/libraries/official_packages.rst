#################
官方包
#################

CodeIgniter 框架无法解决开发者将遇到的所有问题。许多用户说他们喜欢框架小巧、快速的特点,所以我们不想让核心框架臃肿。为了弥合这一差距,我们正在发布官方包以提供不是每个网站都需要或想要的额外功能。

.. contents::
    :local:
    :depth: 2

.. _shield:

******
Shield
******

`CodeIgniter Shield <https://shield.codeigniter.com/>`_ 是 CodeIgniter 4 的身份验证和授权框架。它旨在安全、灵活且易于扩展以满足许多不同类型网站的需求。其中许多功能包括:

* 基于会话的身份验证
* 个人访问令牌认证
* 登录/注册后“动作”的框架(如双因素认证等)
* 基于角色的访问控制,具有简单、灵活的权限。
* 每个用户的权限覆盖
* 等等...

********
Settings
********

`CodeIgniter Settings <https://settings.codeigniter.com>`_ 是配置文件包装器,允许任何配置设置保存到数据库中,同时在没有自定义值存储时默认为配置文件。这允许应用程序与默认配置值一起发布,但随着项目的发展或服务器的迁移而不必接触代码而适应。

************
任务 (BETA)
************

`CodeIgniter 任务 <https://tasks.codeigniter.com>`_ 是 CodeIgniter 4 的一个简单任务调度器。
它允许你安排任务在特定时间运行，或者定期运行。它的设计目标是简单易用，但足够灵活以处理大多数使用场景。

************
队列 (BETA)
************

`CodeIgniter 队列 <https://queue.codeigniter.com>`_ 是 CodeIgniter 4 的一个简单队列系统。
它允许你将任务排队，以便稍后运行。

*****
Cache
*****

我们为 CodeIgniter 4 提供了带有 `PSR-6 和 PSR-16 缓存适配器 <https://github.com/codeigniter4/cache>`_ 的库。这不是必需的,因为 CodeIgniter 4 自带完全功能的缓存组件。此模块仅用于集成依赖 PSR 接口规定的第三方包。


******
DevKit
******

`CodeIgniter DevKit <https://github.com/codeigniter4/devkit>`_ 提供了 CodeIgniter 用来帮助确保高质量代码的所有开发工具,包括我们的编码标准、静态分析工具和规则、单元测试、数据生成、文件系统模拟、安全建议等等。这可以在你的任何个人项目或库中使用,以快速设置 17 种不同的工具。


***************
编码标准
***************

`CodeIgniter 编码标准 <https://github.com/CodeIgniter/coding-standard>`_ 包含了基于 PHP CS Fixer 和 Nexus CS Config 的 CodeIgniter 的官方编码标准。这可以在你自己的项目中使用,以形成一致的风格规则集合,可以自动应用于你的代码。
