#############################
从 4.3.5 升级到 4.3.6
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

- ``AutoRouterInterface::getRoute()`` 新增了第二个参数 ``string $httpVerb``。
  如果你实现了该方法，需要添加此参数。

破坏性增强
*********************

- ``ValidationInterface::check()`` 和 ``Validation::check()`` 的方法签名已发生变更。
  如果你实现或扩展了它们，需要更新方法签名。

项目文件
*************

4.3.6 版本未修改项目文件中的任何可执行代码。

所有变更
===========

以下列出了 **项目空间** 中所有发生变更的文件；
其中多数只是注释或格式调整，不会影响运行时行为：

- composer.json
