#############################
从 4.5.3 升级到 4.5.4
#############################

请参考与你的安装方法相对应的升级说明。

- :ref:`Composer 安装 App Starter 升级 <app-starter-upgrading>`
- :ref:`Composer 安装 将 CodeIgniter4 添加到现有项目 升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装 升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

*************
项目文件
*************

**项目空间** （root、app、public、writable）中的一些文件收到了更新。由于这些文件位于 **system** 范围之外，因此不会在没有你干预的情况下更改。

.. note:: 有一些第三方的 CodeIgniter 模块可以帮助合并项目空间的更改：
    `在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

所有更改
===========

这是 **项目空间** 中所有收到更改的文件列表；许多只是简单的注释或格式调整，对运行时没有影响：

- app/Config/Events.php
- composer.json
