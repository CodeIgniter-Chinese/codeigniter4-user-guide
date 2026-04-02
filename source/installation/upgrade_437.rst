#############################
从 4.3.6 升级到 4.3.7
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

.. _upgrade-437-feature-testing:

功能测试请求体
============================

如果调用了：

1. :ref:`withBody() <feature-setting-the-body>`
2. 以及 :ref:`withBodyFormat() <feature-formatting-the-request>`
3. 并将 ``$params`` 传递给 :ref:`call() <feature-requesting-a-page>` （或其简写方法）

那么请求体的优先级已发生变化。如果测试代码受到影响（这种情况较少见），需要进行修改。

例如，现在使用 ``$params`` 来构建请求体，而不会使用 ``$body``::

    $this->withBody($body)->withBodyFormat('json')->call('post', $params)

在此前版本中，请求体使用的是 ``$body``。

Validation::loadRuleGroup() 的返回值
===========================================

``Validation::loadRuleGroup()`` 的返回值已从“**rules 数组**”变更为“包含 **rules 数组** 和 **customErrors 数组** 的 **数组**”
（``[rules, customErrors]``）。

如果使用了该方法，需要这样更新代码::

    $rules = $this->validation->loadRuleGroup($rules);
        ↓
    [$rules, $customErrors] = $this->validation->loadRuleGroup($rules);

项目文件
*************

**项目空间** （根目录、app、public、writable）中的部分文件已更新。
由于这些文件位于 **system** 范围之外，框架不会在没有你介入的情况下自动修改它们。

目前有一些第三方 CodeIgniter 模块可用于协助合并项目空间中的变更：
`在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容变更
===============

以下文件发生了较大的改动（包括弃用项或界面调整），建议将更新后的版本合并到你的应用中：

配置
------

- app/Config/Kint.php

所有变更
===========

以下列出了 **项目空间** 中所有发生变更的文件；
其中多数只是注释或格式调整，不会影响运行时行为：

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
