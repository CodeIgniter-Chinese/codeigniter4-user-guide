##############################
从 4.3.0 升级到 4.3.1
##############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

Composer 版本
****************

.. important:: 如果你使用 Composer，CodeIgniter v4.3 需要
    Composer 2.0.14 或更高版本。

如果你正在使用较旧版本的 Composer，请升级 ``composer`` 工具，
删除 **vendor/** 目录，然后重新运行 ``composer update``。

例如，升级步骤如下：

.. code-block:: console

    composer self-update
    rm -rf vendor/
    composer update

必须修改的文件
**********************

配置文件
============

app/Config/Email.php
--------------------

- 如果你在升级到 v4.3.0 时更新过 **app/Config/Email.php**，则必须
  为 ``$fromEmail``、``$fromName``、``$recipients``、
  ``$SMTPHost``、``$SMTPUser`` 和 ``$SMTPPass`` 设置默认值，
  以便应用环境变量（**.env**）中的配置。
- 如果未设置默认值，即使设置了对应的环境变量，也不会反映到
  Config 对象中。

app/Config/Exceptions.php
-------------------------

- 如果你使用 PHP 8.2，需要新增属性 ``$logDeprecations`` 和 ``$deprecationLogLevel``。

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

- app/Config/Email.php
    - 为 ``$fromEmail``、``$fromName``、``$recipients``、
      ``$SMTPHost``、``$SMTPUser`` 和 ``$SMTPPass`` 设置默认值 ``''``，
      以便应用环境变量（**.env**）中的配置。

所有变更
===========

以下是 **项目空间** 中所有发生变更的文件列表；
其中许多只是简单的注释或格式调整，对运行时没有任何影响：

- app/Config/Email.php
- composer.json
