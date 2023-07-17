手动安装
###################

.. contents::
    :local:
    :depth: 2

`CodeIgniter 4 框架 <https://github.com/codeigniter4/framework>`_
仓库包含框架的已发布版本。
它适用于不希望使用 Composer 的开发人员。

在 **app** 文件夹中开发您的应用程序,
**public** 文件夹将是您面向公众的文档根目录。不要更改 **system** 文件夹中的任何内容!

.. note:: 这是最接近为 `CodeIgniter 3 <https://codeigniter.com/userguide3/installation/index.html>`_
   描述的安装技术。

安装
============

下载`最新版本 <https://github.com/CodeIgniter4/framework/releases/latest>`_,
并将其提取到成为项目根目录。

.. note:: CodeIgniter 自动加载程序不允许特殊字符,这些字符在某些操作系统中的文件名中是非法的。
    可以使用的符号是 ``/``, ``_``, ``.``, ``:``, ``\`` 和空格。
    因此,如果在包含特殊字符的文件夹下安装 CodeIgniter,比如 ``(``, ``)`` 等,CodeIgniter 将无法工作。

初始配置
=====================

安装后,需要进行一些初始配置。
请参阅 :ref:`initial-configuration` 以获取详细信息。

.. _installing-manual-upgrading:

升级
=========

下载框架的新副本,然后替换 **system** 文件夹。

阅读 :doc:`升级说明 <upgrading>`,并查看已破坏的更改和增强功能。

优点
====

下载并运行。

缺点
====

您需要自行检查 **项目空间** 中的文件更改(根目录、app、public、tests、writable)并合并它们。

结构
=========

设置后项目中的文件夹:

- app、public、tests、writable、system

翻译安装
=========================

如果您想利用系统消息翻译,可以以类似的方式将它们添加到项目中。

下载`最新版本 <https://github.com/codeigniter4/translations/releases/latest>`_。
提取下载的 zip 文件,并将其中的 **Language** 文件夹内容复制到您的 **app/Languages** 文件夹中。

这需要重复执行以合并翻译的任何更新。
