######################################
从 4.0.5 升级到 4.1.0 或 4.1.1
######################################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

破坏性变更
****************

传统自动加载
==================

``Autoloader::loadLegacy()`` 方法最初用于向 CodeIgniter v4 过渡。从 v4.1.0 起，
该支持已被移除。所有类都必须使用命名空间。
