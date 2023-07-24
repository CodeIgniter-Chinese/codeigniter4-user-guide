#############################
从 4.1.5 升级到 4.1.6
#############################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

重大变更
****************

验证结果变化
=========================

由于一个错误修复,现在验证数组项时,验证可能会改变验证结果(参见 :ref:`更新日志 <changelog-v416-validation-changes>`)。所以请检查所有验证数组的验证结果代码。像 ``contacts.*.name`` 这样验证多个字段不受影响。

如果你有以下表单::

    <input type='text' name='invoice_rule[1]'>
    <input type='text' name='invoice_rule[2]'>

并且你有以下验证规则::

    'invoice_rule' => ['rules' => 'numeric', 'errors' => ['numeric' => 'Not numeric']]

将规则键改为 ``invoice_rule.*`` 这样验证就可以工作了。

重大增强
*********************

无。

项目文件
*************

**项目空间** 中的许多文件(根目录、app、public、writable)都已更新。由于这些文件超出 **系统** 范围,如果不进行干预,它们将不会更改。有一些第三方 CodeIgniter 模块可以协助合并项目空间的更改: `在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

.. note:: 除非极少数情况进行错误修复,否则对项目空间文件的任何更改都不会破坏你的应用程序。在下一个主要版本之前,这里注明的所有更改都是可选的,强制性更改将在上面部分介绍。

内容更改
===============

以下文件已作出重大更改(包括弃用或视觉调整),建议你将更新版本与应用程序合并:

* ``app/Config/Filters.php``
* ``app/Config/Mimes.php``
* ``app/Config/Security.php``
* ``app/Config/Toolbar.php``

所有更改
===========

这是 **项目空间** 中已更改的所有文件的列表;其中许多仅为注释或格式更改,不会影响运行时:

* ``app/Config/Filters.php``
* ``app/Config/Mimes.php``
* ``app/Config/Security.php``
* ``app/Config/Toolbar.php``
* ``app/Views/errors/html/error_exception.php``
