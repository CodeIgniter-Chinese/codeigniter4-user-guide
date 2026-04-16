#############################
从 4.1.1 升级到 4.1.2
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

破坏性变更
****************

current_url() 与 indexPage
===========================

由于 ``current_url()`` 中存在 `一个 bug <https://github.com/codeigniter4/CodeIgniter4/issues/4116>`_，
生成的 URI 可能与项目配置不一致，尤其是：不会包含 ``indexPage``。
使用 ``App::$indexPage`` 的项目，应预期 ``current_url()`` 及其所有依赖项
（包括响应测试、分页器、表单辅助函数和视图解析器）
返回的值会发生变化。请相应更新项目代码。

缓存键
==========

各个缓存处理器对缓存键的兼容性差异较大。更新后的缓存驱动现在会对所有键进行校验，
其规则大致与 PSR-6 的建议一致：

    至少包含一个字符、用于唯一标识缓存项的字符串。
    实现库必须支持由 A-Z、a-z、0-9、_ 和 . 组成的键，
    采用 UTF-8 编码，长度不超过 64 个字符。
    实现库可以支持额外的字符、编码或更长的长度，
    但至少必须支持上述最小集合。
    各库需自行对键字符串进行必要的转义，
    但必须能返回原始未修改的键字符串。
    以下字符为未来扩展保留，
    实现库不得支持：``{}()/\@:``

请更新项目，移除所有无效的缓存键。

BaseConnection::query() 返回值
=====================================

在此前版本中，``BaseConnection::query()`` 方法在查询失败时，
仍会错误地返回 BaseResult 对象。
现在，该方法在查询失败时将返回 ``false``
（或在 ``DBDebug`` 为 ``true`` 时抛出异常），
而对于写类型查询则返回布尔值。
请检查所有 ``query()`` 的使用场景，
评估其返回值是否可能为布尔值而非 Result 对象。
关于哪些查询属于写类型，
请参考 ``BaseConnection::isWriteType()``
以及各数据库连接类中针对 ``isWriteType()`` 的实现或重写。

破坏性增强
*********************

新增 ConnectionInterface::isWriteType() 声明
====================================================

如果你编写了任何实现 ConnectionInterface 的类，
现在必须实现 ``isWriteType()`` 方法，
其声明为 ``public function isWriteType($sql): bool``。
如果你的类继承自 BaseConnection，
该基类已经提供了一个基础的 ``isWriteType()``
实现，你可以根据需要进行重写。

测试 Trait
===========

``CodeIgniter\Test`` 命名空间进行了大量改进，
以更好地支持开发者编写测试用例。
最重要的变化是：测试扩展被迁移为 Trait，
以便根据不同测试需求灵活组合使用。
``CIDatabaseTestCase`` 和 ``FeatureTestCase``
已被弃用，其方法分别迁移到
``DatabaseTestTrait`` 和 ``FeatureTestTrait`` 中。
请更新测试用例，使其继承主测试基类，
并按需引入所需的 Trait。例如：

.. literalinclude:: upgrade_412/001.php

... 变为：

.. literalinclude:: upgrade_412/002.php

最后，``ControllerTester`` 已被 ``ControllerTestTrait`` 取代，
以统一测试方式，并充分利用下文所述的
响应测试改进。

测试响应
==============

用于测试响应的工具已被整合并增强。
新的 ``TestResponse`` 取代了
``ControllerResponse`` 和 ``FeatureResponse``，
并提供了二者所需的完整方法与属性集合。
在大多数情况下，这些变更会通过
``ControllerTestTrait`` 和 ``FeatureTestCase``
在后台处理，但仍有两点需要注意：

* ``TestResponse`` 的 ``$request`` 和 ``$response`` 属性为 protected，
  只能通过其 getter 方法 ``request()`` 和 ``response()`` 访问
* ``TestResponse`` 不再提供 ``getBody()`` 和 ``setBody()`` 方法，
  而是直接使用 Response 的方法，例如：
  ``$body = $result->response()->getBody();``

项目文件
*************

项目空间中的大量文件（根目录、app、public、writable）已获得更新。
由于这些文件不属于 system 范畴，
框架不会在未征得你同意的情况下自动修改它们。
有一些第三方 CodeIgniter 模块可用于协助合并
项目空间中的变更：
`在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

.. note:: 除极少数用于修复 bug 的情况外，
    对项目空间文件所做的更改不会破坏你的应用。
    此处列出的所有更改在下一个主版本发布之前都是可选的，
    任何强制性的更改都会在上文相关章节中说明。

内容变更
===============

以下文件发生了较大的改动（包括弃用项或界面调整），建议将更新后的版本合并到你的应用中：

* ``app/Config/App.php``
* ``app/Config/Autoload.php``
* ``app/Config/Cookie.php``
* ``app/Config/Events.php``
* ``app/Config/Exceptions.php``
* ``app/Config/Security.php``
* ``app/Views/errors/html/*``
* ``env``
* ``spark``

所有变更
===========

以下是项目空间中所有发生变更的文件列表；
其中许多只是简单的注释或格式调整，
对运行时没有影响：

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
