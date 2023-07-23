##############################
从 4.2.12 升级到 4.3.0
##############################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

Composer 版本
****************

.. important:: 如果你使用 Composer,CodeIgniter v4.3.0 需要
    Composer 2.0.14 或更高版本。

如果你使用的是更早版本的 Composer,请升级你的 ``composer`` 工具,
删除 **vendor/** 目录,并再次运行 ``composer update``。

例如,过程如下::

    > composer self-update
    > rm -rf vendor/
    > composer update

必备文件变更
**********************

spark
=====

以下文件进行了重大更改,
**你必须将更新后的版本** 与应用程序合并:

- ``spark``

.. important:: 如果不更新此文件,在运行 ``composer update`` 后 Spark 命令将完全无法工作。

    升级过程例如如下::

        > composer update
        > cp vendor/codeigniter4/framework/spark .

配置文件
============

app/Config/Kint.php
-------------------

- **app/Config/Kint.php** 已更新为兼容 Kint 5.0。
- 你需要替换:

    - ``Kint\Renderer\Renderer`` 为 ``Kint\Renderer\AbstractRenderer``
    - ``Renderer::SORT_FULL`` 为 ``AbstractRenderer::SORT_FULL``

app/Config/Exceptions.php
-------------------------

- 如果你使用 PHP 8.2,需要添加新的属性 ``$logDeprecations`` 和 ``$deprecationLogLevel``。

模拟配置类
-------------------

- 如果你在测试中使用以下模拟配置类,需要更新 **app/Config** 中对应的配置文件:

    - ``MockAppConfig`` (``Config\App``)
    - ``MockCLIConfig`` (``Config\App``)
    - ``MockSecurityConfig`` (``Config\Security``)

- 在这些配置类中为属性添加**类型**。你可能需要调整属性值以匹配属性类型。

composer.json
=============

如果你手动安装了 CodeIgnter,并使用 Composer,
你需要删除以下行,并运行 ``composer update``。

.. code-block:: text

    {
        ...
        "require": {
            ...
            "kint-php/kint": "^4.2",  <-- 移除此行
            ...
        },
        ...
        "scripts": {
            "post-update-cmd": [
                "CodeIgniter\\ComposerScripts::postUpdate"  <-- 移除此行
            ],
            "test": "phpunit"
        },
        ...
    }

重大变更
****************

数据库异常变化
==========================

- 当发生数据库错误时,可能会改变异常类。如果你捕获了异常,必须确认你的代码可以捕获这些异常。
- 现在即使 ``CI_DEBUG`` 为 false,也会抛出一些异常。
- 在事务期间,即使 ``DBDebug`` 为 true,默认情况下也不会抛出异常。如果要抛出异常,需要调用 ``transException(true)``。
  参见 :ref:`transactions-throwing-exceptions`。
- 有关详细信息,请参阅 :ref:`exceptions-when-database-errors-occur`。

未捕获异常的 HTTP 状态码和退出码
=====================================================

- 如果你希望**异常代码**作为**HTTP状态码**,则 HTTP 状态码将会改变。
  在这种情况下,需要在异常中实现 ``HTTPExceptionInterface``。参见 :ref:`error-specify-http-status-code`。
- 如果你根据**异常代码**期望**退出码**,则退出码将会改变。
  在这种情况下,需要在异常中实现 ``HasExitCodeInterface``。参见 :ref:`error-specify-exit-code`。

redirect()->withInput() 和验证错误
=============================================

``redirect()->withInput()`` 和验证错误之前有一个未记录的行为。
如果你使用 ``withInput()`` 重定向,CodeIgniter 会将验证错误存储在会话中,
并且你可以在重定向页面的验证对象中获取错误,在执行新的验证之前::

    // 在控制器中
    if (! $this->validate($rules)) {
        return redirect()->back()->withInput();
    }

    // 在重定向页面的视图中
    <?= service('Validation')->listErrors() ?>

这种行为是一个错误,在 v4.3.0 中已修复。

如果你的代码依赖于此错误,则需要更改代码。
使用新的 Form 辅助函数,:php:func:`validation_errors()`、:php:func:`validation_list_errors()` 和 :php:func:`validation_show_error()`
来显示验证错误,而不是 Validation 对象。

验证更改
==================

- ``ValidationInterface`` 已更改。实现的类也应该添加方法和参数,以免违反LSP。有关详细信息,请参阅 :ref:`v430-validation-changes`。
- ``Validation::loadRuleGroup()`` 的返回值在 ``$group`` 为空时已从 ``null`` 改为 ``[]``。如果依赖于该行为,请更新代码。

Time 修复
==========

- 由于错误修复,:doc:`Time <../libraries/time>` 中的一些方法已从可变行为更改为不可变; ``Time`` 现在扩展 ``DateTimeImmutable``。详细信息请参阅 :ref:`ChangeLog <v430-time-fix>`。
- 如果需要修改前 ``Time`` 的行为,已添加了一个兼容的 ``TimeLegacy`` 类。请在应用程序代码中全部替换 ``Time`` 为 ``TimeLegacy``。
- 但是 ``TimeLegacy`` 已被废弃。因此我们建议你更新代码。

例如::

    // 之前
    $time = Time::now();
    // ...
    if ($time instanceof DateTime) {
        // ...
    }

    // 之后
    $time = Time::now();
    // ...
    if ($time instanceof DateTimeInterface) {
        // ...
    }

::

    // 之前
    $time1 = new Time('2022-10-31 12:00');
    $time2 = $time1->modify('+1 day');
    echo $time1; // 2022-11-01 12:00:00
    echo $time2; // 2022-11-01 12:00:00

    // 之后
    $time1 = new Time('2022-10-31 12:00');
    $time2 = $time1->modify('+1 day');
    echo $time1; // 2022-10-31 12:00:00
    echo $time2; // 2022-11-01 12:00:00

.. _upgrade-430-stream-filter:

在测试中捕获 STDERR 和 STDOUT 流
============================================

捕获错误和输出流的方式已更改。现在需要这样使用::

    use CodeIgniter\Test\Filters\CITestStreamFilter;

    protected function setUp(): void
    {
        CITestStreamFilter::registration();
        CITestStreamFilter::addOutputFilter();
        CITestStreamFilter::addErrorFilter();
    }

    protected function tearDown(): void
    {
        CITestStreamFilter::removeOutputFilter();
        CITestStreamFilter::removeErrorFilter();
    }

而不是::

    use CodeIgniter\Test\Filters\CITestStreamFilter;

    protected function setUp(): void
    {
        CITestStreamFilter::$buffer = '';
        $this->streamFilter         = stream_filter_append(STDOUT, 'CITestStreamFilter');
        $this->streamFilter         = stream_filter_append(STDERR, 'CITestStreamFilter');
    }

    protected function tearDown(): void
    {
        stream_filter_remove($this->streamFilter);
    }

或者使用 trait ``CodeIgniter\Test\StreamFilterTrait``。参见 :ref:`testing-cli-output`。

接口变化
=================

一些接口已修复。详细信息请参阅 :ref:`v430-interface-changes`。

外键数据
================

- ``BaseConnection::getForeignKeyData()`` 返回的数据结构已更改。
  你需要相应调整依赖此方法的任何代码,以使用新的结构。

示例:``tableprefix_table_column1_column2_foreign``

返回的数据具有以下结构::

    /**
     * @return array[
     *    {constraint_name} =>
     *        stdClass[
     *            'constraint_name'     => string,
     *            'table_name'          => string,
     *            'column_name'         => string[],
     *            'foreign_table_name'  => string,
     *            'foreign_column_name' => string[],
     *            'on_delete'           => string,
     *            'on_update'           => string,
     *            'match'               => string
     *        ]
     * ]
     */

重大增强
*********************

支持多个域名
=======================

- 如果设置了 ``Config\App::$allowedHostnames``,则当当前 URL 与其中一个匹配时,像 :php:func:`base_url()`、:php:func:`current_url()`、:php:func:`site_url()` 这样的与 URL 相关的函数会返回带有 ``Config\App::$allowedHostnames`` 中设置的主机名的 URL。

数据库
========

- ``CodeIgniter\Database\Database::loadForge()`` 的返回类型已更改为 ``Forge``。扩展类也应相应更改类型。
- ``CodeIgniter\Database\Database::loadUtils()`` 的返回类型已更改为 ``BaseUtils``。扩展类也应相应更改类型。
- ``BaseBuilder::updateBatch()`` 的第二个参数 ``$index`` 已更改为 ``$constraints``。它现在接受 array、string 或 ``RawSql`` 类型。扩展类也应相应更改类型。
- ``BaseBuilder::insertBatch()`` 和 ``BaseBuilder::updateBatch()`` 的 ``$set`` 参数现在接受单行数据的对象。扩展类也应相应更改类型。
- ``BaseBuilder::_updateBatch()`` 的第三个参数 ``$index`` 已更改为 ``$values``,参数类型已更改为 ``array``。扩展类也应相应更改类型。
- 如果 ``Model::update()`` 方法生成不带 WHERE 子句的 SQL 语句,现在会引发 ``DatabaseException``。如果需要更新表中的所有记录,请使用 Query Builder,例如 ``$model->builder()->update($data)``。

.. _upgrade-430-honeypot-and-csp:

Honeypot 和 CSP
================

当启用 CSP 时,会向 Honeypot 字段的容器标签中注入 id 属性 ``id="hpc"``,以隐藏该字段。如果视图中已经使用了该 id,则需要用 ``Config\Honeypot::$containerId`` 更改它。
并且可以在 ``Config\Honeypot::$container`` 中删除 ``style="display:none"``。

其它
======

- **辅助函数:** 由于 ``html_helper``、``form_helper`` 或常用函数中的空 HTML 元素(例如 ``<input>``)已默认更改为 HTML5 兼容,如果你需要与 XHTML 兼容,必须在 **app/Config/DocTypes.php** 中将 ``$html5`` 属性设置为 ``false``。
- **CLI:** 由于从 ``CodeIgniter\CodeIgniter`` 中提取了 Spark 命令的启动,如果 ``Services::codeigniter()`` 服务被覆盖,运行这些命令时可能会出现问题。

项目文件
*************

**项目空间** 中的许多文件(根目录、app、public、writable)都已更新。由于这些文件超出 **系统** 范围,如果不进行干预,它们将不会更改。有一些第三方 CodeIgniter 模块可以协助合并项目空间的更改:`在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容更改
===============

以下文件已作出重大更改(包括弃用或视觉调整),建议你将更新版本与应用程序合并:

.. _upgrade_430_config:

配置
------

- app/Config/App.php
    - 添加了新属性 ``$allowedHostnames``,用于在站点 URL 中设置主机名,
      除了 ``$baseURL`` 中的主机名之外。参见 :ref:`v430-multiple-domain-support`。
    - 属性 ``$appTimezone`` 已更改为 ``UTC``,以避免受夏令时的影响。
- app/Config/Autoload.php
    - 添加了新属性 ``$helpers`` 以自动加载辅助函数。
- app/Config/Database.php
    - ``$default['DBDebug']`` 和 ``$test['DBDebug']`` 默认更改为 ``true``。
      参见 :ref:`exceptions-when-database-errors-occur`。
- app/Config/DocTypes.php
    - 添加了属性 ``$html5`` 以确定是否移除空 HTML 元素(如 ``<input>``)中的 solidus (``/``)字符,默认为 ``true`` 以实现 HTML5 兼容性。
- app/Config/Encryption.php
    - 添加了新属性 ``$rawData``、``$encryptKeyInfo`` 和 ``$authKeyInfo`` 以实现 CI3
      加密兼容性。参见 :ref:`encryption-compatible-with-ci3`。
- app/Config/Exceptions.php
    - 添加了两个新的公共属性:``$logDeprecations`` 和 ``$deprecationLogLevel``。
      详细信息请参阅 :ref:`logging_deprecation_warnings`。
- app/Config/Honeypot.php
    - 添加了新属性 ``$containerId`` 以在启用 CSP 时设置容器标签的 id 属性值。
    - 属性 ``$template`` 中的值的 ``input`` 标签已更改为 HTML5 兼容。
- app/Config/Logger.php
    - 属性 ``$threshold`` 在非 ``production`` 环境中默认更改为 ``9``。
- app/Config/Modules.php
    - 添加了新属性 ``$composerPackages`` 以限制 Composer 包自动发现,提高性能。
- app/Config/Routes.php
    - 由于启动 Spark 命令的方式已更改,不再需要加载框架的内部路由 (``SYSTEMPATH . 'Config/Routes.php'``)。
- app/Config/Security.php
    - 将属性 ``$redirect`` 的值更改为 ``false``,以防止 CSRF 检查失败时发生重定向。这可以更轻松地识别它是 CSRF 错误。
- app/Config/Session.php
    - 添加以处理 session 配置。
- app/Config/Validation.php
    - 默认验证规则已更改为严格规则,以提高安全性。请参阅 :ref:`validation-traditional-and-strict-rules`。

视图文件
----------

以下视图文件已更改为 HTML5 兼容标签。
此外,错误消息现在在 **Errors** 语言文件中定义。

- app/Views/errors/html/error_404.php
- app/Views/errors/html/error_exception.php
- app/Views/errors/html/production.php
- app/Views/welcome_message.php

所有更改
===========

这是 **项目空间** 中已更改的所有文件的列表;其中许多仅为注释或格式更改,不会影响运行时。
``Config`` 类中的所有原子类型属性已加上类型:

*   app/Config/App.php
*   app/Config/Autoload.php
*   app/Config/CURLRequest.php
*   app/Config/Cache.php
*   app/Config/ContentSecurityPolicy.php
*   app/Config/Cookie.php
*   app/Config/Database.php
*   app/Config/DocTypes.php
*   app/Config/Email.php
*   app/Config/Encryption.php
*   app/Config/Exceptions.php
*   app/Config/Feature.php
*   app/Config/Filters.php
*   app/Config/Format.php
*   app/Config/Generators.php
*   app/Config/Honeypot.php
*   app/Config/Images.php
*   app/Config/Kint.php
*   app/Config/Logger.php
*   app/Config/Migrations.php
*   app/Config/Mimes.php
*   app/Config/Modules.php
*   app/Config/Pager.php
*   app/Config/Paths.php
*   app/Config/Routes.php
*   app/Config/Security.php
*   app/Config/Session.php
*   app/Config/Toolbar.php
*   app/Config/UserAgents.php
*   app/Config/Validation.php
*   app/Views/errors/html/error_404.php
*   app/Views/errors/html/error_exception.php
*   app/Views/errors/html/production.php
*   app/Views/welcome_message.php
*   composer.json
*   env
*   phpunit.xml.dist
*   spark
