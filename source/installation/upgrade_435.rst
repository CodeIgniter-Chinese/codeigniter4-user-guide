##############################
从 4.3.4 升级到 4.3.5
##############################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

重大变更
****************

验证占位符
=======================

为了安全地使用 :ref:`validation-placeholders`,请记得为你将用作占位符的字段创建一个验证规则。

例如，如果你有以下代码::

    $validation->setRules([
        'email' => 'required|max_length[254]|valid_email|is_unique[users.email,id,{id}]',
    ]);

你需要为 ``{id}`` 添加规则::

    $validation->setRules([
        'id'    => 'max_length[19]|is_natural_no_zero', // Add this
        'email' => 'required|max_length[254]|valid_email|is_unique[users.email,id,{id}]',
    ]);

Session::stop()
===============

在 v4.3.5 之前,由于一个错误, ``Session::stop()`` 方法并没有销毁 session。这个方法已被修改为销毁 session,并已不建议使用,因为它与 ``Session::destroy()`` 方法完全相同。所以请使用 :ref:`Session::destroy() <session-destroy>` 方法替代。

如果你的代码依赖这个错误,请用 ``session_regenerate_id(true)`` 替换它。

参见 :ref:`Session 库 <session-stop>`。

项目文件
*************

**项目空间** 中的一些文件(根目录、app、public、writable)已更新。由于这些文件超出 **系统** 范围,如果不进行干预,它们将不会更改。

有一些第三方 CodeIgniter 模块可以协助合并项目空间的更改:`在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容更改
===============

以下文件已作出重大更改(包括弃用或视觉调整),建议你将更新版本与应用程序合并:

配置
------

- app/Config/Generators.php

所有更改
===========

这是 **项目空间** 中已更改的所有文件的列表;其中许多仅为注释或格式更改,不会影响运行时:

- app/Config/App.php
- app/Config/Generators.php
- composer.json
