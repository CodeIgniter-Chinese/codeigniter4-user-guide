#############################
从 4.4.5 升级到 4.4.6
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

****************
破坏性变更
****************

Time::createFromTimestamp() 时区变更
===========================================

现在，如果你未指定时区，
:ref:`Time::createFromTimestamp() <time-createfromtimestamp>` 会返回一个使用应用时区的
Time 实例。

如果你想保持 UTC 时区，则需要调用 ``setTimezone('UTC')``::

    use CodeIgniter\I18n\Time;

    $time = Time::createFromTimestamp(1501821586)->setTimezone('UTC');

*************
项目文件
*************

**项目空间** （根目录、app、public、writable）中的部分文件已更新。
由于这些文件位于 **system** 范围之外，框架不会在没有你介入的情况下自动修改它们。

目前有一些第三方 CodeIgniter 模块可用于协助合并项目空间中的变更：
`在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

所有变更
===========

以下列出了 **项目空间** 中所有已发生变更的文件；
其中很多只是简单的注释或格式调整，不会影响运行时行为：

- app/Config/App.php
- app/Config/Routing.php
- app/Views/welcome_message.php
- composer.json
