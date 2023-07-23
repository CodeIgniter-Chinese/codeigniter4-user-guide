#############################
从 4.1.1 升级到 4.1.2
#############################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

重大变更
****************

current_url() 和 indexPage
===========================

由于 `一个 bug <https://github.com/codeigniter4/CodeIgniter4/issues/4116>`_ 导致 ``current_url()`` 的结果可能与项目配置不匹配,最重要的是:``indexPage``
*不会* 被包含。使用 ``App::$indexPage`` 的项目应该期望 ``current_url()`` 及所有依赖它的内容(包括响应测试、分页器、表单辅助函数、分页器和视图解析器)的值发生改变。请相应更新你的项目。

缓存键
==========

缓存处理程序在键的兼容性方面差异很大。更新的缓存驱动现在会通过验证传递所有键,大致匹配 PSR-6 的建议:

    一个至少由一个字符组成的字符串, uniquely identifies a cached item.实现库 MUST 支持由字符 A-Z、a-z、0-9、_ 和 . 组成的键,可以任意顺序,使用 UTF-8 编码,长度上限为 64 个字符。实现库 MAY 支持额外的字符和编码或者更长的长度,但必须至少支持那个最小要求。库自己负责根据需要对键字符串进行转义,但必须能够返回原始未修改的键字符串。以下保留字符是为未来扩展而预留的,实现库 MUST NOT 支持: ``{}()/\@:``

请更新项目以删除任何无效的缓存键。

BaseConnection::query() 的返回值
=====================================

之前版本中的 ``BaseConnection::query()`` 方法错误地总是返回 BaseResult 对象,即使查询失败。该方法现在对失败的查询会返回 ``false`` (如果 ``DBDebug`` 为 ``true`` 则会抛出异常),对写类型的查询会返回布尔值。请检查 ``query()`` 方法的任何使用,评估返回值是否可能是布尔类型而不是 Result 对象。要更好地了解什么查询是写类型的查询,请查看 ``BaseConnection::isWriteType()`` 和相关 Connection 类中任何特定于 DBMS 的 ``isWriteType()`` 覆盖。

重大增强
*********************

添加了 ConnectionInterface::isWriteType() 声明
====================================================

如果你编写了任何实现 ConnectionInterface 的类,现在必须实现 ``isWriteType()`` 方法,声明为 ``public function isWriteType($sql): bool``。如果你的类扩展了 BaseConnection,那么该类将提供一个基本的 ``isWriteType()`` 方法,你可能想覆盖它。

测试 Traits
===========

``CodeIgniter\Test`` 命名空间进行了大量改进,以帮助开发人员自己的测试用例。最显著的是测试扩展移至 Traits 以使它们更易于在各种测试用例需求之间进行选择。 ``CIDatabaseTestCase`` 和 ``FeatureTestCase`` 类已被废弃,它们的方法分别移至 ``DatabaseTestTrait`` 和 ``FeatureTestTrait``。请更新测试用例以扩展主要测试用例并使用任何所需的 traits。例如:

.. literalinclude:: upgrade_412/001.php

... 变为:

.. literalinclude:: upgrade_412/002.php

最后, ``ControllerTester`` 已被 ``ControllerTestTrait`` 取代,以统一方法并利用更新的响应测试(见下文)。

测试响应
==============

用于测试响应的工具已经进行了合并和改进。新的 ``TestResponse`` 替换了 ``ControllerResponse`` 和 ``FeatureResponse``,提供了两个类的完整方法和属性集。在大多数情况下,这些更改将由 ``ControllerTestTrait`` 和 ``FeatureTestCase`` “幕后”处理,但要注意两点:

* ``TestResponse`` 的 ``$request`` 和 ``$response`` 属性是受保护的,只能通过它们的 getter 方法 ``request()`` 和 ``response()`` 访问
* ``TestResponse`` 没有 ``getBody()`` 和 ``setBody()`` 方法,而是直接使用 Response 方法,例如:``$body = $result->response()->getBody();``

项目文件
*************

项目空间(root、app、public、writable)中的许多文件都已更新。由于这些文件超出系统范围,如果不进行干预,它们将不会更改。有一些第三方 CodeIgniter 模块可用于帮助合并项目空间中的更改: `在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

.. note:: 除了极少数的错误修复情况外,对项目空间文件的任何更改都不会破坏你的应用程序。直到下一个主版本之前,这里注明的所有更改都是可选的,任何强制性更改都将在上面的部分中介绍。

内容更改
===============

以下文件收到了显着更改(包括不推荐使用或视觉调整),建议你将更新版本与应用程序合并:

* ``app/Config/App.php``
* ``app/Config/Autoload.php``
* ``app/Config/Cookie.php``
* ``app/Config/Events.php``
* ``app/Config/Exceptions.php``
* ``app/Config/Security.php``
* ``app/Views/errors/html/*``
* ``env``
* ``spark``

所有更改
===========

这是项目空间中收到更改的所有文件的列表;其中许多只是注释或格式更改,不会对运行时产生影响:

* ``app/Config/App.php``
* ``app/Config/Autoload.php``
* ``app/Config/ContentSecurityPolicy.php``
* ``app/Config/Cookie.php``
* ``app/Config/Events.php``
* ``app/Config/Exceptions.php``
* ``app/Config/Logger.php``
* ``app/Config/Mimes.php``
* ``app/Config/Modules.php``
* ``app/Config/Security.php``
* ``app/Controllers/BaseController.php``
* ``app/Views/errors/html/debug.css``
* ``app/Views/errors/html/error_404.php``
* ``app/Views/errors/html/error_exception.php``
* ``app/Views/welcome_message.php``
* ``composer.json``
* ``contributing/guidelines.rst``
* ``env``
* ``phpstan.neon.dist``
* ``phpunit.xml.dist``
* ``public/.htaccess``
* ``public/index.php``
* ``rector.php``
* ``spark``
