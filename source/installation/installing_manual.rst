手动安装
###################

.. contents::
    :local:
    :depth: 2

`CodeIgniter 4 框架 <https://github.com/codeigniter4/framework>`_
仓库包含框架的已发布版本。
它适用于不希望使用 Composer 的开发人员。

在 **app** 文件夹中开发你的应用程序,
**public** 文件夹将是你面向公众的文档根目录。不要更改 **system** 文件夹中的任何内容!

.. note:: 这是最接近为 `CodeIgniter 3 <https://codeigniter.com/userguide3/installation/index.html>`_
   描述的安装技术。

安装
============

下载 `最新版本 <https://github.com/CodeIgniter4/framework/releases/latest>`__,
并将其提取到成为项目根目录。

.. note:: 在 v4.4.0 之前，CodeIgniter 的自动加载器不允许在某些操作系统上的文件名中使用非法的特殊字符。可以使用的符号包括 ``/``、``_``、``.``、``:``、``\`` 和空格。因此，如果你将 CodeIgniter 安装在包含特殊字符（如 ``(``、``)`` 等）的文件夹中，CodeIgniter 将无法正常工作。从 v4.4.0 开始，这个限制已经被移除。

初始配置
=====================

安装后,需要进行一些初始配置。
请参阅 :ref:`initial-configuration` 以获取详细信息。

.. _installing-manual-upgrading:

升级
=========

下载框架的新副本,然后替换 **system** 文件夹。

阅读 :doc:`升级说明 <upgrading>` 和 :doc:`变更日志 <../changelogs/index>`，并检查重大变更和增强功能。

优点
====

下载并运行。

缺点
====

你需要自行检查 **项目空间** 中的文件更改(根目录、app、public、tests、writable)并合并它们。

结构
=========

设置后项目中的文件夹:

- app、public、tests、writable、system

翻译安装
=========================

如果你想利用系统消息翻译,可以以类似的方式将它们添加到项目中。

下载 `最新版本 <https://github.com/codeigniter4/translations/releases/latest>`__。
提取下载的 zip 文件,并将其中的 **Language** 文件夹内容复制到你的 **app/Languages** 文件夹中。

这需要重复执行以合并翻译的任何更新。
