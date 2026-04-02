##############################
从 4.2.12 升级到 4.3.0
##############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

Composer 版本
****************

.. important:: 如果你使用 Composer，CodeIgniter v4.3.0 要求
    Composer 2.0.14 或更高版本。

如果你正在使用较旧版本的 Composer，请升级 ``composer`` 工具，
删除 **vendor/** 目录，然后重新运行 ``composer update``。

例如，升级步骤如下：

.. code-block:: console

    composer self-update
    rm -rf vendor/
    composer update

必须修改的文件
**********************

spark
=====

以下文件发生了重大更改，
**你必须将更新后的版本合并到应用中**：

- ``spark``

.. important:: 如果不更新此文件，在运行 ``composer update`` 之后，所有 Spark 命令将完全无法使用。

    例如，升级步骤如下：

    .. code-block:: console

        composer update
        cp vendor/codeigniter4/framework/spark .

配置文件
============

app/Config/Kint.php
-------------------

- **app/Config/Kint.php** 已针对 Kint 5.0 进行了更新。
- 需要进行如下替换：

    - 将 ``Kint\Renderer\Renderer`` 替换为 ``Kint\Renderer\AbstractRenderer``
    - 将 ``Renderer::SORT_FULL`` 替换为 ``AbstractRenderer::SORT_FULL``

app/Config/Exceptions.php
-------------------------

- 如果你使用 PHP 8.2，需要新增属性 ``$logDeprecations`` 和 ``$deprecationLogLevel``。

Mock 配置类
-------------------

- 如果你在测试中使用了以下 Mock 配置类，需要同步更新 **app/Config** 中对应的 Config 文件：

    - ``MockAppConfig`` （``Config\App``）
    - ``MockCLIConfig`` （``Config\App``）
    - ``MockSecurityConfig`` （``Config\Security``）

- 为这些 Config 类中的属性添加 **类型声明**。你可能还需要修正属性值，使其符合属性类型。

composer.json
=============

如果你是手动安装 CodeIgniter，并且使用 Composer，
需要移除以下内容，然后运行 ``composer update``。

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

破坏性变更
****************

数据库异常变更
==========================

- 当发生数据库错误时，抛出的异常类可能会发生变化。如果你捕获了这些异常，
  必须确认代码仍然能够正确捕获异常。
- 现在，即使 ``CI_DEBUG`` 为 false，也会抛出部分异常。
- 在事务中，即使 ``DBDebug`` 为 true，默认情况下也不会抛出异常。
  如果你希望抛出异常，需要调用 ``transException(true)``。
  参见 :ref:`transactions-throwing-exceptions`。
- 详情请参见 :ref:`exceptions-when-database-errors-occur`。

未捕获异常的 HTTP 状态码与退出码
=====================================================

- 如果你期望 *异常代码* 作为 *HTTP 状态码*，HTTP 状态码的行为将发生变化。
  在这种情况下，需要在异常中实现 ``HTTPExceptionInterface``。
  参见 :ref:`error-specify-http-status-code`。
- 如果你期望基于 *异常代码* 的 *退出码*，退出码的行为将发生变化。
  在这种情况下，需要在异常中实现 ``HasExitCodeInterface``。
  参见 :ref:`error-specify-exit-code`。

redirect()->withInput() 与验证错误
=============================================

``redirect()->withInput()`` 与验证错误此前存在未文档化的行为。
当你使用 ``withInput()`` 重定向时，CodeIgniter 会将验证错误存储在 Session 中，
并且你可以在重定向后的页面中，在 *未运行新一轮验证之前*，
通过 Validation 对象获取错误信息::

    // 控制器中
    if (! $this->validate($rules)) {
        return redirect()->back()->withInput();
    }

    // 重定向后页面的视图中
    <?= service('Validation')->listErrors() ?>

该行为属于 Bug，并已在 v4.3.0 中修复。

如果你的代码依赖于该 Bug，需要进行修改。
请使用新的表单辅助函数
:php:func:`validation_errors()`、
:php:func:`validation_list_errors()` 和
:php:func:`validation_show_error()` 来显示验证错误，
而不是直接使用 Validation 对象。

验证相关变更
==================

- ``ValidationInterface`` 已发生变更。实现该接口的类需要相应地补充方法和参数，
  以避免破坏 LSP。详情参见 :ref:`v430-validation-changes`。
- ``Validation::loadRuleGroup()`` 的返回值在 ``$group`` 为空时，
  已从 ``null`` 改为 ``[]``。如果你的代码依赖旧行为，需要进行调整。

Time 修复
==========

- 由于 Bug 修复，:doc:`Time <../libraries/time>` 中的一些方法
  从可变行为变为不可变行为；``Time`` 现在继承自 ``DateTimeImmutable``。
  详情参见 :ref:`变更记录 <v430-time-fix>`。
- 如果你需要修改前 ``Time`` 的行为，新增了兼容类 ``TimeLegacy``。
  请将应用代码中的 ``Time`` 全部替换为 ``TimeLegacy``。
- 但 ``TimeLegacy`` 已被弃用，因此建议你更新代码以适配新的 ``Time`` 行为。

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

捕获错误流和输出流的方式已发生变化。现在不再使用::

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

而需要改为::

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

或者使用 trait ``CodeIgniter\Test\StreamFilterTrait``。
参见 :ref:`testing-cli-output`。

接口变更
=================

部分接口已修复。详情参见 :ref:`v430-interface-changes`。

外键数据
================

- ``BaseConnection::getForeignKeyData()`` 返回的数据结构已发生变化。
  任何依赖该方法的代码都需要调整以适配新的结构。

示例：``tableprefix_table_column1_column2_foreign``

返回的数据结构如下::

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

破坏性增强
*********************

多域名支持
=======================

- 如果设置了 ``Config\App::$allowedHostnames``，且当前 URL 匹配，
  :php:func:`base_url()`、:php:func:`current_url()`、:php:func:`site_url()`
  等 URL 相关函数将返回使用 ``Config\App::$allowedHostnames`` 中主机名的 URL。

数据库
========

- ``CodeIgniter\Database\Database::loadForge()`` 的返回类型已更改为 ``Forge``。
  扩展类需要相应调整类型。
- ``CodeIgniter\Database\Database::loadUtils()`` 的返回类型已更改为 ``BaseUtils``。
  扩展类需要相应调整类型。
- ``BaseBuilder::updateBatch()`` 的第二个参数 ``$index`` 已更名为 ``$constraints``，
  现在可接受 array、string 或 ``RawSql`` 类型。扩展类需要相应调整类型。
- ``BaseBuilder::insertBatch()`` 和 ``BaseBuilder::updateBatch()`` 的 ``$set`` 参数
  现在接受表示单行数据的对象。扩展类需要相应调整类型。
- ``BaseBuilder::_updateBatch()`` 的第三个参数 ``$index`` 已更名为 ``$values``，
  且参数类型已更改为 ``array``。扩展类需要相应调整类型。
- ``Model::update()`` 方法在生成不包含 WHERE 子句的 SQL 语句时，
  现在会抛出 ``DatabaseException``。
  如果需要更新表中的所有记录，请改用查询构建器，例如
  ``$model->builder()->update($data)``。

.. _upgrade-430-honeypot-and-csp:

Honeypot 与 CSP
================

当启用 CSP 时，会在 Honeypot 字段的容器标签中注入 ``id="hpc"``
以隐藏该字段。如果该 id 已在你的视图中使用，需要通过
``Config\Honeypot::$containerId`` 进行修改。
同时，你可以移除 ``Config\Honeypot::$container`` 中的
``style="display:none"``。

其他
======

- **辅助函数：** ``html_helper``、``form_helper`` 或通用函数中的
  空 HTML 元素（例如 ``<input>``）现在默认采用 HTML5 兼容方式。
  如果你需要兼容 XHTML，必须将 **app/Config/DocTypes.php** 中的
  ``$html5`` 属性设为 ``false``。
- **CLI：** 由于 Spark 命令的启动逻辑已从 ``CodeIgniter\CodeIgniter`` 中抽离，
  如果你覆盖了 ``Services::codeigniter()`` 服务，运行这些命令可能会出现问题。

项目文件
*************

**项目空间** （根目录、app、public、writable）中的部分文件已更新。
由于这些文件位于 **system** 范围之外，框架不会在没有你介入的情况下自动修改它们。
目前有一些第三方 CodeIgniter 模块可用于协助合并项目空间中的变更：
`在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容变更
===============

以下文件发生了较大的改动（包括弃用项或界面调整），建议将更新后的版本合并到你的应用中：

.. _upgrade_430_config:

配置
------

- app/Config/App.php
    - 新增属性 ``$allowedHostnames``，用于指定除 ``$baseURL`` 主机名以外的其他允许主机名。
      参见 :ref:`v430-multiple-domain-support`。
    - 属性 ``$appTimezone`` 已更改为 ``UTC``，以避免受夏令时影响。
- app/Config/Autoload.php
    - 新增属性 ``$helpers``，用于自动加载辅助函数。
- app/Config/Database.php
    - ``$default['DBDebug']`` 和 ``$test['DBDebug']`` 默认值已更改为 ``true``。
      参见 :ref:`exceptions-when-database-errors-occur`。
- app/Config/DocTypes.php
    - 新增属性 ``$html5``，用于决定是否移除空 HTML 元素
      （例如 ``<input>``）中的斜杠（``/``），
      默认设为 ``true`` 以兼容 HTML5。
- app/Config/Encryption.php
    - 新增属性 ``$rawData``、``$encryptKeyInfo`` 和 ``$authKeyInfo``，
      用于与 CI3 加密类兼容。参见 :ref:`encryption-compatible-with-ci3`。
- app/Config/Exceptions.php
    - 新增两个 public 属性：``$logDeprecations`` 和 ``$deprecationLogLevel``。
      详情参见 :ref:`logging_deprecation_warnings`。
- app/Config/Honeypot.php
    - 新增属性 ``$containerId``，用于在启用 CSP 时设置容器标签的 ID。
    - 属性 ``$template`` 中的 ``input`` 标签已更改为 HTML5 兼容形式。
- app/Config/Logger.php
    - 在非 ``production`` 环境中，属性 ``$threshold`` 已更改为 ``9``。
- app/Config/Modules.php
    - 新增属性 ``$composerPackages``，用于限制 Composer 包的自动发现，
      以提升性能。
- app/Config/Routes.php
    - 由于 Spark 命令的执行方式已改变，不再需要加载框架内部路由
      （``SYSTEMPATH . 'Config/Routes.php'``）。
- app/Config/Security.php
    - 将属性 ``$redirect`` 的值更改为 ``false``，
      以防止 CSRF 校验失败时发生重定向，
      从而更容易识别 CSRF 错误。
- app/Config/Session.php
    - 新增，用于处理 Session 配置。
- app/Config/Validation.php
    - 默认验证规则已更改为严格规则，以提升安全性。
      参见 :ref:`validation-traditional-and-strict-rules`。

视图文件
----------

以下视图文件已更改为 HTML5 兼容标签。
同时，错误消息现在定义在 **Errors** 语言文件中。

- app/Views/errors/html/error_404.php
- app/Views/errors/html/error_exception.php
- app/Views/errors/html/production.php
- app/Views/welcome_message.php

所有变更
===========

以下是 **项目空间** 中所有发生变更的文件列表；
其中许多只是简单的注释或格式调整，对运行时没有任何影响。
``Config`` 类中的所有原子类型属性均已添加类型声明：

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
