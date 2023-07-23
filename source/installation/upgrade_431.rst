##############################
从 4.3.0 升级到 4.3.1
##############################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

Composer 版本
****************

.. important:: 如果你使用 Composer,CodeIgniter v4.3 需要
    Composer 2.0.14 或更高版本。

如果你使用的是更早版本的 Composer,请升级你的 ``composer`` 工具,
删除 **vendor/** 目录,并再次运行 ``composer update``。

例如,过程如下::

    > composer self-update
    > rm -rf vendor/
    > composer update

必备文件变更
**********************

配置文件
============

app/Config/Email.php
--------------------

- 如果你在升级到 v4.3.0 时更新了 **app/Config/Email.php**,你必须
  为 ``$fromEmail``、``$fromName``、``$recipients``、``$SMTPHost``、``$SMTPUser`` 和 ``$SMTPPass``
  设置默认值,以应用环境变量 (**.env**) 值。
- 如果没有设置默认值,设置这些环境变量将不会反映在配置对象中。

app/Config/Exceptions.php
-------------------------

- 如果你使用 PHP 8.2,需要添加新的属性 ``$logDeprecations`` 和 ``$deprecationLogLevel``。

项目文件
*************

**项目空间** 中的一些文件(根目录、app、public、writable)已更新。由于这些文件超出 **系统** 范围,如果不进行干预,它们将不会更改。

有一些第三方 CodeIgniter 模块可以协助合并项目空间的更改:`在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容更改
===============

以下文件已作出重大更改(包括弃用或视觉调整),建议你将更新版本与应用程序合并:

配置
------

- app/Config/Email.php
    - 为 ``$fromEmail``、``$fromName``、``$recipients``、``$SMTPHost``、``$SMTPUser`` 和 ``$SMTPPass``
      设置默认值为 ``''``,以应用环境变量 (**.env**) 值。

所有更改
===========

这是 **项目空间** 中已更改的所有文件的列表;其中许多仅为注释或格式更改,不会影响运行时:

- app/Config/Email.php
- composer.json
