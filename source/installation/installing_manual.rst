手动安装
###################

.. contents::
    :local:
    :depth: 2

`CodeIgniter 4 框架 <https://github.com/codeigniter4/framework>`_
代码仓库中包含框架的已发布版本。
该方式适用于不希望使用 Composer 的开发者。

在 **app** 文件夹中开发应用，**public** 文件夹作为对外公开的文档根目录。
**system** 文件夹中的任何内容都不要修改！

.. note:: 这是与
   `CodeIgniter 3 <https://codeigniter.com/userguide3/installation/index.html>`_
   所描述的安装方式最为接近的一种方法。

安装
============

下载 `最新版本 <https://github.com/CodeIgniter4/framework/releases/latest>`_，
并解压到项目根目录。

.. note:: 在 v4.4.0 之前，CodeIgniter 自动加载器不允许使用在某些操作系统中
    作为文件名非法的特殊字符。
    允许使用的符号仅包括 ``/``、``_``、``.``、``:``、``\`` 和空格。
    因此，如果将 CodeIgniter 安装在包含 ``(``、``)`` 等特殊字符的文件夹路径下，
    CodeIgniter 将无法正常工作。
    自 v4.4.0 起，此限制已被移除。

初始配置
=====================

安装完成后，需要进行一些初始配置。
详情请参阅 :ref:`initial-configuration`。

.. _installing-manual-upgrading:

升级
=========

下载一份新的框架副本，然后替换 **system** 文件夹。

请阅读 :doc:`升级说明 <upgrading>` 和 :doc:`变更日志 <../changelogs/index>`，
并重点检查 Breaking Changes 和 Enhancements。

优点
====

下载即可运行。

缺点
====

需要自行检查 **项目空间**
（root、app、public、tests、writable）中的文件变更，
并手动合并这些更改。

目录结构
=========

安装完成后，项目中的文件夹结构如下：

- app、public、tests、writable、system

翻译文件的安装
=========================

如果希望使用系统消息的翻译，
可以采用类似的方式将其添加到项目中。

下载 `最新版本 <https://github.com/codeigniter4/translations/releases/latest>`_。
解压下载的 zip 文件，并将其中 **Language** 文件夹的内容
复制到 **app/Languages** 文件夹中。

每次翻译文件有更新时，
都需要重复上述步骤以合并最新内容。
