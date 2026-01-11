##############################
处理多环境
##############################

开发者通常希望应用程序在开发环境和生产环境中表现出不同的系统行为。
例如，详细的错误输出在应用开发过程中非常有用，但在“正式上线”后却可能带来安全隐患。
此外，开发环境可能需要加载一些生产环境不需要的额外工具，诸如此类的情况还有很多。

.. contents::
    :local:
    :depth: 3

************************
预定义的环境
************************

默认情况下，CodeIgniter 定义了三种环境。

- ``production`` - 生产环境
- ``development`` - 开发环境
- ``testing`` - PHPUnit 测试环境

.. important:: ``testing`` 环境专为 PHPUnit 测试保留。
    框架在各个位置内置了特殊条件来协助测试。你不能用它来进行开发。

如果你需要其他环境，例如预发布环境（staging），可以添加自定义环境。
参见 `添加环境`_。

.. _setting-environment:

*******************
设置环境
*******************

.. _environment-constant:

ENVIRONMENT 常量
========================

要设置环境，CodeIgniter 提供了 ``ENVIRONMENT`` 常量。
如果你设置了 ``$_SERVER['CI_ENVIRONMENT']``，将使用该值，
否则默认为 ``production``。

可以根据服务器设置以多种方式设置此变量。

.env
----

设置该变量最简单的方法是在你的 :ref:`.env 文件 <dotenv-file>` 中。

.. code-block:: ini

    CI_ENVIRONMENT = development

.. note:: 你可以使用 ``spark env`` 命令更改 **.env** 文件中的 ``CI_ENVIRONMENT`` 值：

    .. code-block:: console

        php spark env production

.. _environment-apache:

Apache
------

可以使用 `SetEnv <https://httpd.apache.org/docs/2.4/mod/mod_env.html#setenv>`_ 在你的 **.htaccess** 文件或 Apache 配置中设置此服务器变量。

.. code-block:: apache

    SetEnv CI_ENVIRONMENT development


.. _environment-nginx:

Nginx
-----

在 Nginx 下，你必须通过 ``fastcgi_params`` 传递环境变量，使其显示在 ``$_SERVER`` 变量中。
这样可以在虚拟主机级别工作，而不是使用 `env` 为整个服务器设置，尽管这在专用服务器上也能正常工作。
然后你需要将服务器配置修改为类似这样：

.. code-block:: nginx

    server {
        server_name localhost;
        include     conf/defaults.conf;
        root        /var/www;

        location    ~* \.php$ {
            fastcgi_param CI_ENVIRONMENT "production";
            include conf/fastcgi-php.conf;
        }
    }

针对 Nginx 等服务器还有其他替代方案，或者你也可以彻底删掉这部分逻辑，直接通过服务器 IP 地址等方式来设置常量。

除了影响一些基本的框架行为（参见下一节），你还可以在自己的开发中使用此常量来区分当前运行在哪个环境中。

*******************
添加环境
*******************

要添加自定义环境，只需为它们添加启动文件。

启动文件
==========

CodeIgniter 要求在 **APPPATH/Config/Boot** 目录下放置一个与环境名称相匹配的 PHP 脚本。这些文件可以包含你希望针对当前环境进行的任何自定义配置，无论是调整错误显示设置、加载额外的开发工具，还是其他任何操作。系统会自动加载这些文件。在全新安装中，已默认创建了以下文件：

* development.php
* production.php
* testing.php

例如，如果你想要添加 ``staging`` 环境用于预发布，你需要做的就是：

1. 将 **APPPATH/Config/Boot/production.php** 复制为 **staging.php**。
2. 如果需要，在 **staging.php** 中自定义设置。

**********************************
确认当前环境
**********************************

要确认当前环境，只需输出常量 ``ENVIRONMENT`` 的值。

你也可以通过 ``spark env`` 命令检查当前环境：

.. code-block:: console

    php spark env

*************************************
对默认框架行为的影响
*************************************

CodeIgniter 系统中有一些地方使用了 ``ENVIRONMENT`` 常量。
本节描述了默认框架行为如何受到影响。

错误报告
===============

将 ``ENVIRONMENT`` 常量设置为 ``development`` 值将导致所有 PHP 错误在发生时渲染到浏览器。
相反，将常量设置为 ``production`` 将禁用所有错误输出。
在生产环境中禁用错误报告是一种
:doc:`良好的安全实践 </concepts/security>`。
