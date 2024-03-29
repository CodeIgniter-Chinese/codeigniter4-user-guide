#############################
从 4.3.5 升级到 4.3.6
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

- ``AutoRouterInterface::getRoute()`` 新增了第二个参数 ``string $httpVerb``。
  如果你实现了它,请添加该参数。

重大增强
*********************

- ``ValidationInterface::check()`` 和 ``Validation::check()`` 的方法签名已更改。
  如果你扩展或实现了它们,请更新签名。

项目文件
*************

4.3.6 版本没有更改项目文件中的任何可执行代码。

所有更改
===========

这是 **项目空间** 中已更改的所有文件的列表;其中许多仅为注释或格式更改,不会影响运行时:

- composer.json
