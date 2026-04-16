#############################
从 4.2.0 升级到 4.2.1
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

必须修改的文件
**********************

app/Config/Mimes.php
====================

- **app/Config/Mimes.php** 中的文件扩展名到 MIME 类型的映射已更新，以修复一个缺陷。
  同时，``Mimes::getExtensionFromType()`` 的逻辑也已发生变化。

破坏性变更
****************

.. _upgrade-421-get_cookie:

get_cookie()
============

如果同时存在一个带前缀的 Cookie 和一个不带前缀但名称相同的 Cookie，
之前的 ``get_cookie()`` 会出现一个容易混淆的行为：返回不带前缀的 Cookie。

例如，当 ``Config\Cookie::$prefix`` 为 ``prefix_``，并且存在两个 Cookie，
``test`` 和 ``prefix_test``：

.. code-block:: php

    $_COOKIES = [
        'test'        => 'Non CI Cookie',
        'prefix_test' => 'CI Cookie',
    ];

在旧行为中，``get_cookie()`` 的返回如下：

.. code-block:: php

    get_cookie('test');        // 返回 "Non CI Cookie"
    get_cookie('prefix_test'); // 返回 "CI Cookie"

现在该问题已作为缺陷修复，行为变更如下：

.. code-block:: php

    get_cookie('test');              // 返回 "CI Cookie"
    get_cookie('prefix_test');       // 返回 null
    get_cookie('test', false, null); // 返回 "Non CI Cookie"

如果你的代码依赖之前的行为，则需要进行相应修改。

.. note:: 在上述示例中，如果只存在一个 ``prefix_test`` Cookie，
    之前的 ``get_cookie('test')`` 同样会返回 ``"CI Cookie"``。

破坏性增强
*********************

项目文件
*************

**项目空间** （根目录、app、public、writable）中的部分文件已更新。
由于这些文件位于 **system** 范围之外，框架不会在没有你介入的情况下自动修改它们。

目前有一些第三方 CodeIgniter 模块可用于协助合并项目空间中的变更：
`在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

.. note:: 除极少数用于缺陷修复的情况外，对项目空间文件所做的任何修改都不会破坏你的应用。
    此处列出的所有变更在下一个主版本发布前都是可选的，
    任何强制性变更都会在上述章节中说明。

内容变更
===============

所有变更
===========

以下是 **项目空间** 中所有发生变更的文件列表；
其中许多仅为注释或格式调整，不会影响运行时行为：

* app/Config/Mimes.php
