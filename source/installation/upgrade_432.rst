##############################
从 4.3.1 升级到 4.3.2
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

base_url()
==========

:php:func:`base_url()` 的行为已修复。在以前的版本中,当你调用 ``base_url()`` **不带参数时**,它会返回不带尾部斜杠 (``/``) 的 baseURL。现在它会返回带有尾部斜杠的 baseURL。例如:

- 之前:``http://example.com``
- 之后:``http://example.com/``

如果你有调用不带参数的 ``base_url()`` 的代码,可能需要调整 URL。

.. _upgrade-432-uri-string:

uri_string()
============

:php:func:`uri_string()` 的行为已修复。在以前的版本中,当你导航到 baseURL 时,它会返回 ``/``。现在它返回一个空字符串 (``''``)。

如果你有调用 ``uri_string()`` 的代码,可能需要调整它。

.. note:: :php:func:`uri_string()` 返回相对于 baseURL 的 URI 路径。
    如果 baseURL 包含子文件夹,它不是完整的 URI 路径。
    如果要用于 HTML 链接,最好与 :php:func:`site_url()` 一起使用,
    如 ``site_url(uri_string())``。

必备文件变更
**********************

composer.json
=============

如果你手动安装了 CodeIgnter 并且正在使用或计划使用 Composer,
请删除以下行:

.. code-block:: text

    {
        ...
        "scripts": {
            "post-update-cmd": [
                "CodeIgniter\\ComposerScripts::postUpdate"  <-- 移除此行
            ],
            "test": "phpunit"
        },
        ...
    }

项目文件
*************

**项目空间** 中的一些文件(根目录、app、public、writable)已更新。由于这些文件超出 **系统** 范围,如果不进行干预,它们将不会更改。

有一些第三方 CodeIgniter 模块可以协助合并项目空间的更改:`在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容更改
===============

以下文件已作出重大更改(包括弃用或视觉调整),建议你将更新版本与应用程序合并:

- app/Config/Mimes.php
- app/Views/errors/html/error_exception.php
- composer.json
- public/.htaccess

所有更改
===========

这是 **项目空间** 中已更改的所有文件的列表;其中许多仅为注释或格式更改,不会影响运行时:

- app/Config/App.php
- app/Config/Mimes.php
- app/Views/errors/html/error_exception.php
- composer.json
- public/.htaccess
