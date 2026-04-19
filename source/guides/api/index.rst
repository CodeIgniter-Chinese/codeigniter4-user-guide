.. _ci47-rest-part1:

REST API 入门
##############################

.. contents::
    :local:
    :depth: 2

本教程将介绍如何在 CodeIgniter 4 中构建一个简单的图书管理 RESTful API。内容涵盖项目搭建、数据库配置、API 接口创建，以及 RESTful API 的基本特征。

本教程主要关注：

- 自动路由（改进版）
- 创建 JSON API 接口
- 使用 API ResponseTrait 实现一致的响应
- 使用模型进行基础数据库操作

.. tip::

    虽然本教程会涉及 CodeIgniter 的基础知识，但建议先完成 :doc:`第一个应用程序教程 <../first-app/index>`。

.. toctree::
    :hidden:
    :titlesonly:

    first-endpoint
    database-setup
    controller
    conclusion

准备就绪
**********************

安装 CodeIgniter
======================

.. code-block:: console

    composer create-project codeigniter4/appstarter books-api
    cd books-api
    php spark serve

在浏览器中访问 ``http://localhost:8080`` 即可看到 CodeIgniter 欢迎页面。

.. note::

    请在终端保持服务器运行。如需停止，可随时按下 :kbd:`Ctrl+C`，之后使用 ``php spark serve`` 重新启动。

设置开发模式
========================

复制环境配置文件并启用开发设置：

.. code-block:: console

    cp env .env

打开 **.env** 并确保**取消注释**以下行：

.. code-block:: ini

    CI_ENVIRONMENT = development

也可以使用 spark ``env`` 命令来设置环境：

.. code-block:: console

    php spark env development

配置 SQLite
================

本教程使用 **writable/** 目录下的单文件 SQLite 数据库，无需进行额外配置。

打开 **.env**，**取消注释** 数据库部分并进行如下设置：

.. code-block:: ini

    database.default.DBDriver = SQLite3
    database.default.database = database.db
    database.default.DBPrefix =
    database.default.username =
    database.default.password =
    database.default.hostname =
    database.default.port     =

如果该文件不存在，CodeIgniter 会自动创建 SQLite 数据库文件，但需确保 Web 服务器对 **writable/** 目录拥有写入权限。

.. warning::

    在某些系统上，可能需要调整用户组/所有者，或在开发期间临时使用 ``chmod 666``。切勿在生产环境中使用全局可写权限。


至此，已完成配置了 SQLite 的 CodeIgniter4 项目。

- 应用通过 ``php spark serve`` 启动
- **.env** 中的 ``CI_ENVIRONMENT`` 已设置为 ``development``
- **writable/database.db** 已存在且可写

下一步
===========

下一部分将启用自动路由并创建一个简单的 JSON 接口（``/api/pings``），以此了解 CodeIgniter 中 HTTP 方法与控制器方法的映射关系。
