#############################
从 4.7.0 升级到 4.7.1
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

**********************
强制文件变更
**********************

Worker 模式
===========

如果正在使用 Worker 模式，升级后必须更新 **public/frankenphp-worker.php**。最简便的方法是重新运行安装命令：

.. code-block:: console

    php spark worker:install --force

*********************
破坏性增强
*********************

数据库连接属性类型转换
======================================

``BaseConnection`` 现在会对来自 ``.env`` 覆盖的字符串值进行类型转换，使其与每个连接属性声明的类型相匹配。这会影响配置数组中原为 ``null`` 但通过 ``.env`` 设置的属性（例如 SQLite3 的 ``synchronous`` 或 ``busyTimeout``），这些属性此前以字符串形式传入，且未进行转换即存储。

如果扩展了 SQLite3 处理程序，请检查自定义类型属性并在必要时进行更新。

*************
项目文件
*************

**项目空间** （根目录、app、public、writable）中的部分文件已更新。
由于这些文件位于 **system** 范围之外，框架不会在没有你介入的情况下自动修改它们。

.. note:: 目前有一些第三方 CodeIgniter 模块可用于协助合并项目空间中的变更：
    `在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容变更
===============

以下文件发生了较大变更（包括弃用或视觉调整），建议将更新后的版本与应用进行合并：

配置
------

- app/Config/WorkerMode.php
    - 添加了 ``Config\WorkerMode::$resetEventListeners``，默认值设为 ``[]``。详情请参阅 :ref:`worker-mode-reset-event-listeners`。

所有变更
===========

以下列出了 **项目空间** 中所有已变更的文件；
其中很多只是注释或格式调整，不会影响运行时行为：

- app/Config/Database.php
- app/Config/WorkerMode.php
