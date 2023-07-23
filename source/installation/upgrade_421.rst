#############################
从 4.2.0 升级到 4.2.1
#############################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

必备文件变更
**********************

app/Config/Mimes.php
====================

- **app/Config/Mimes.php** 中文件扩展名与 MIME 类型的映射已更新以修复一个错误。同时, ``Mimes::getExtensionFromType()`` 的逻辑也已改变。

重大变更
****************

.. _upgrade-421-get_cookie:

get_cookie()
============

如果存在一个带前缀的 cookie 和一个同名但不带前缀的 cookie,之前的 ``get_cookie()`` 有一种棘手的行为,它会返回不带前缀的 cookie。

例如,当 ``Config\Cookie::$prefix`` 为 ``prefix_`` 时,存在两个 cookie:``test`` 和 ``prefix_test``:

.. code-block:: php

    $_COOKIES = [
        'test'        => '非 CI Cookie',
        'prefix_test' => 'CI Cookie',
    ];

以前, ``get_cookie()`` 返回如下:

.. code-block:: php

    get_cookie('test');        // 返回 "非 CI Cookie"
    get_cookie('prefix_test'); // 返回 "CI Cookie"

现在该行为已被修复为一个错误,并进行了如下改变:

.. code-block:: php

    get_cookie('test');              // 返回 "CI Cookie"
    get_cookie('prefix_test');       // 返回 null
    get_cookie('test', false, null); // 返回 "非 CI Cookie"

如果你依赖之前的行为,则需要更改代码。

.. note:: 在上面的例子中,如果只有一个 cookie ``prefix_test``,
       之前的 ``get_cookie('test')`` 也会返回 ``"CI Cookie"``。

重大增强
*********************

项目文件
*************

**项目空间** 中的许多文件(根目录、app、public、writable)都已更新。由于这些文件超出 **系统** 范围,如果不进行干预,它们将不会更改。有一些第三方 CodeIgniter 模块可以协助合并项目空间的更改: `在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

.. note:: 除非极少数情况进行错误修复,否则对项目空间文件的任何更改都不会破坏你的应用程序。在下一个主要版本之前,这里注明的所有更改都是可选的,强制性更改将在上面部分介绍。

内容更改
===============

所有更改
===========

这是 **项目空间** 中已更改的所有文件的列表;其中许多仅为注释或格式更改,不会影响运行时:

* app/Config/Mimes.php
