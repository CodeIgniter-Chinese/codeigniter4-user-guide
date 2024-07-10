#############################
从 4.5.1 升级到 4.5.2
#############################

请参考与你的安装方式对应的升级说明。

- :ref:`Composer 安装 App Starter 升级 <app-starter-upgrading>`
- :ref:`Composer 安装 将 CodeIgniter4 添加到一个现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

*************
项目文件
*************

**项目空间** （root, app, public, writable）中的一些文件收到了更新。由于这些文件位于 **system** 范围之外，没有你的干预它们不会被更改。

.. note:: 有一些第三方的 CodeIgniter 模块可以帮助合并项目空间的变化：
    `在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

所有更改
===========

以下是 **项目空间** 中所有收到更改的文件列表；许多更改将是简单的注释或格式调整，不会影响运行时：

- app/Config/DocTypes.php
- app/Config/Exceptions.php
- preload.php
- spark
- writable/.htaccess
- writable/cache/index.html
- writable/debugbar/index.html
- writable/index.html
- writable/logs/index.html
- writable/session/index.html
