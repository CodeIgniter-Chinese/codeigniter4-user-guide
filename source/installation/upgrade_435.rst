##############################
从 4.3.4 升级到 4.3.5
##############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

破坏性变更
****************

验证占位符
=======================

要安全地使用 :ref:`validation-placeholders`，请务必为将用作占位符的字段创建对应的验证规则。

例如，如果有如下代码::

    $validation->setRules([
        'email' => 'required|max_length[254]|valid_email|is_unique[users.email,id,{id}]',
    ]);

则需要为 ``{id}`` 添加规则::

    $validation->setRules([
        'id'    => 'max_length[19]|is_natural_no_zero', // Add this
        'email' => 'required|max_length[254]|valid_email|is_unique[users.email,id,{id}]',
    ]);

Session::stop()
===============

在 v4.3.5 之前，由于一个 bug，``Session::stop()`` 方法并不会销毁会话。该方法已被修改为会销毁会话，并且现在已被弃用，因为它与 ``Session::destroy()`` 方法完全相同。因此，请改用 :ref:`Session::destroy <session-destroy>` 方法。

如果现有代码依赖于该 bug 的行为，请将其替换为 ``session_regenerate_id(true)``。

另请参阅 :ref:`Session 库 <session-stop>`。

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

- app/Config/Generators.php

所有变更
===========

以下列出了 **项目空间** 中所有发生变更的文件；其中许多只是简单的注释或格式调整，对运行时没有影响：

- app/Config/App.php
- app/Config/Generators.php
- composer.json
