#############################
从 4.3.6 升级到 4.3.7
#############################

请参考与你的安装方法相对应的升级说明。

- :ref:`使用 Composer 安装的应用程序启动器升级 <app-starter-upgrading>`
- :ref:`使用 Composer 安装的将 CodeIgniter4 添加到现有项目中升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

重大变更
****************

.. _upgrade-437-feature-testing:

功能测试请求体
============================

如果你调用了以下方法：

1. :ref:`withBody() <feature-setting-the-body>`
2. 并且 :ref:`withBodyFormat() <feature-formatting-the-request>`
3. 并将 ``$params`` 传递给 :ref:`call() <feature-requesting-a-page>` (或简写方法)

则请求体的优先级已更改。如果你的测试代码受到此更改的影响，请进行修改。

例如，现在使用 ``$params`` 来构建请求体，而不使用 ``$body``::

    $this->withBody($body)->withBodyFormat('json')->call('post', $params)

以前，``$body`` 用于请求体。

Validation::loadRuleGroup() 的返回值
===========================================

``Validation::loadRuleGroup()`` 的返回值已从 "**rules 数组**" 更改为 "**rules 数组** 和 **customErrors 数组**" 的 "**数组**"（``[rules, customErrors]``）。

如果你使用了该方法，请将代码更新如下::

    $rules = $this->validation->loadRuleGroup($rules);
        ↓
    [$rules, $customErrors] = $this->validation->loadRuleGroup($rules);

项目文件
*************

**项目空间**（根目录、app、public、writable）中的一些文件已经更新。由于这些文件位于 **系统** 范围之外，因此不会在没有你干预的情况下进行更改。

有一些第三方 CodeIgniter 模块可用于帮助合并对项目空间的更改：`在 Packagist 上查看 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容更改
===============

以下文件已经进行了重大更改（包括弃用或视觉调整），建议你将更新后的版本与你的应用程序合并：

配置
------

- app/Config/Kint.php

所有更改
===========

这是 **项目空间** 中所有已更改的文件的列表；其中许多只是注释或格式变化，对运行时没有影响：

- app/Config/App.php
- app/Config/Autoload.php
- app/Config/Cache.php
- app/Config/ContentSecurityPolicy.php
- app/Config/Filters.php
- app/Config/Kint.php
- app/Config/Logger.php
- app/Config/Migrations.php
- app/Config/Modules.php
- app/Config/Paths.php
- app/Controllers/BaseController.php
- app/Controllers/Home.php
- composer.json
