##############################
从 4.3.1 升级到 4.3.2
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

base_url()
==========

:php:func:`base_url()` 的行为已被修复。此前版本中，当 **不带参数** 调用 ``base_url()`` 时，
返回的 baseURL 末尾不包含斜杠（``/``）。现在将返回带有末尾斜杠的 baseURL。例如：

- 之前：``http://example.com``
- 现在：``http://example.com/``

如果你的代码中存在不带参数调用 ``base_url()`` 的情况，可能需要调整相关 URL。

.. _upgrade-432-uri-string:

uri_string()
============

:php:func:`uri_string()` 的行为已被修复。此前版本中，当你访问 baseURL 时，
它会返回 ``/``。现在将返回空字符串（``''``）。

如果你的代码中调用了 ``uri_string()``，可能需要进行相应调整。

.. note:: :php:func:`uri_string()` 返回的是相对于 baseURL 的 URI 路径。
    如果 baseURL 包含子文件夹，则它不是完整的 URI 路径。
    如果将其用于 HTML 链接，建议与 :php:func:`site_url()` 结合使用，
    例如 ``site_url(uri_string())``。

必须修改的文件
**********************

composer.json
=============

如果你是手动安装 CodeIgnter，并且正在使用或计划使用 Composer，
请移除以下这一行：

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

**项目空间** （根目录、app、public、writable）中的部分文件已更新。
由于这些文件位于 **system** 范围之外，框架不会在没有你介入的情况下自动修改它们。

目前有一些第三方 CodeIgniter 模块可用于协助合并项目空间中的变更：
`在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容变更
===============

以下文件发生了较大的改动（包括弃用项或界面调整），建议将更新后的版本合并到你的应用中：

- app/Config/Mimes.php
- app/Views/errors/html/error_exception.php
- composer.json
- public/.htaccess

所有变更
===========

以下是 **项目空间** 中所有发生变更的文件列表；
其中许多只是简单的注释或格式调整，对运行时没有影响：

- app/Config/App.php
- app/Config/Mimes.php
- app/Views/errors/html/error_exception.php
- composer.json
- public/.htaccess
