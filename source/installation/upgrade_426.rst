#############################
从 4.2.5 升级到 4.2.6
#############################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

项目文件
*************

**项目空间** 中的一些文件(根目录、app、public、writable)收到了视觉优化的更新。
你完全不需要碰这些文件。有一些第三方 CodeIgniter 模块可以帮助合并项目空间的更改:
`在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

所有更改
===========

这是 **项目空间** 中已更改的所有文件的列表;其中许多仅为注释或格式更改,不会影响运行时:

* app/Config/App.php
* app/Config/ContentSecurityPolicy.php
* app/Config/Routes.php
* app/Config/Validation.php
