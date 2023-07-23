#############################
从 4.2.7 升级到 4.2.8
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

以下文件对代码或行为进行了改变,建议在项目中更新:

* app/Views/errors/html/error_exception.php

所有更改
===========

这是 **项目空间** 中已更改的所有文件的列表;其中许多仅为注释或格式更改,不会影响运行时:

* app/Config/Logger.php
* app/Views/errors/html/error_exception.php
