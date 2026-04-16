##############################
从 4.3.2 升级到 4.3.3
##############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

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

- app/Config/Encryption.php
    - 为兼容 CI3 的加密类，新增了缺失的属性 ``$cipher``。
      参见 :ref:`encryption-compatible-with-ci3`。

所有变更
===========

以下是 **项目空间** 中所有发生变更的文件列表；
其中许多只是简单的注释或格式调整，对运行时没有影响：

- app/Common.php
- app/Config/Encryption.php
- composer.json
