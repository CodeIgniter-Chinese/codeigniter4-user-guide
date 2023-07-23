######################################
从 4.0.5 升级到 4.1.0 或 4.1.1
######################################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

重大变更
****************

传统自动加载
==================

``Autoloader::loadLegacy()`` 方法原本是为过渡到 CodeIgniter v4 而设计的。自 v4.1.0 开始,
此支持已被移除。所有类必须采用命名空间。
