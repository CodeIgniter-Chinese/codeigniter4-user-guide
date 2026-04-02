#############################
从 4.1.5 升级到 4.1.6
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

破坏性变更
****************

验证结果变更
=========================

由于修复了一个缺陷，当你验证数组项时，验证结果现在可能会发生变化（参见 :ref:`变更记录 <changelog-v416-validation-changes>`）。
因此，请检查所有对数组进行验证的代码中的验证结果。像 ``contacts.*.name`` 这样验证多个字段的用法不受影响。

如果你有如下表单::

    <input type='text' name='invoice_rule[1]'>
    <input type='text' name='invoice_rule[2]'>

并且验证规则如下::

    'invoice_rule' => ['rules' => 'numeric', 'errors' => ['numeric' => 'Not numeric']]

请将规则键名改为 ``invoice_rule.*``，验证即可正常工作。

破坏性增强
*********************

无。

项目文件
*************

**项目空间** （根目录、app、public、writable）中的部分文件已更新。
由于这些文件位于 **system** 范围之外，框架不会在没有你介入的情况下自动修改它们。

目前有一些第三方 CodeIgniter 模块可用于协助合并项目空间中的变更：
`在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

.. note:: 除极少数用于缺陷修复的情况外，对项目空间文件所做的任何修改都不会破坏你的应用。
    此处列出的所有变更在下一个主版本发布前都是可选的，
    任何强制性变更都会在上述章节中说明。

内容变更
===============

以下文件发生了较大的改动（包括弃用项或界面调整），建议将更新后的版本合并到你的应用中：

* ``app/Config/Filters.php``
* ``app/Config/Mimes.php``
* ``app/Config/Security.php``
* ``app/Config/Toolbar.php``

所有变更
===========

以下是 **项目空间** 中所有发生变更的文件列表；
其中许多仅为注释或格式调整，不会影响运行时行为：

* ``app/Config/Filters.php``
* ``app/Config/Mimes.php``
* ``app/Config/Security.php``
* ``app/Config/Toolbar.php``
* ``app/Views/errors/html/error_exception.php``
