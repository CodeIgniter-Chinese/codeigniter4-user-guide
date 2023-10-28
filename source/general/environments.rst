##############################
处理多个环境
##############################

开发人员通常希望根据应用程序是在开发还是生产环境中运行来实现不同的系统行为。
例如,在开发应用程序时,详细的错误输出是有用的,但在“生产环境”时可能也会带来安全问题。在开发环境中,你可能需要加载在生产环境中不需要的其他工具等等。

.. contents::
    :local:
    :depth: 3

************************
定义的环境
************************

默认情况下,CodeIgniter 定义了三个环境。

- ``production`` 用于生产
- ``development`` 用于开发
- ``testing`` 用于 PHPUnit 测试

.. important:: 环境 ``testing`` 保留用于 PHPUnit 测试。它在框架的各处内置了一些特殊条件以协助测试。你不能在开发中使用它。

如果你想要另一个环境,例如用于暂存,你可以添加自定义环境。请参阅 `添加环境`_。

.. _setting-environment:

*******************
设置环境
*******************

.. _environment-constant:

ENVIRONMENT 常量
========================

要设置环境,CodeIgniter 提供了 ``ENVIRONMENT`` 常量。
如果设置了 ``$_SERVER['CI_ENVIRONMENT']``,将使用该值,否则默认为 ``production``。

根据你的服务器设置,可以通过几种方式设置此值。

.env
----

在 :ref:`.env 文件 <dotenv-file>` 中设置该变量是最简单的方法。

.. code-block:: ini

    CI_ENVIRONMENT = development

.. note:: 你可以通过 ``spark env`` 命令更改 **.env** 文件中的 ``CI_ENVIRONMENT`` 值:

    .. code-block:: console

        php spark env production

.. _environment-apache:

Apache
------

可以在 **.htaccess** 文件或 Apache 配置中使用 `SetEnv <https://httpd.apache.org/docs/2.4/mod/mod_env.html#setenv>`_ 设置此服务器变量。

.. code-block:: apache

    SetEnv CI_ENVIRONMENT development


.. _environment-nginx:

Nginx
-----

在 Nginx 下,必须通过 ``fastcgi_params`` 传递环境变量,以便它在 ``$_SERVER`` 变量下显示。这允许它在虚拟主机级别工作,而不是使用 `env` 为整个服务器设置它,尽管这在专用服务器上也可以很好地工作。然后可以将服务器配置修改为类似以下内容:

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

Nginx 和其他服务器可用的替代方法,或者你可以完全删除此逻辑,并根据服务器的 IP 地址设置常量(例如)。

除了影响一些基本框架行为(参见下一节),你还可以在自己的开发中使用此常量来区分正在运行的环境。

*******************
添加环境
*******************

要添加自定义环境,你只需要为它们添加引导文件。

引导文件
==========

CodeIgniter 要求与环境名称匹配的 PHP 脚本位于 **APPPATH/Config/Boot** 下。这些文件可以包含你希望针对环境进行的任何自定义,无论是更新错误显示设置、加载其他开发人员工具还是其他任何内容。这些由系统自动加载。在初始安装中已经创建了以下文件:

* development.php
* production.php
* testing.php

例如,如果你想添加 ``staging`` 环境用于暂存,你只需要:

1. 将 **APPPATH/Config/Boot/production.php** 复制到 **staging.php**。
2. 如有必要,在 **staging.php** 中自定义设置。

**********************************
确认当前环境
**********************************

要确认当前环境,只需打印常量 ``ENVIRONMENT``。

你也可以通过 ``spark env`` 命令检查当前环境:

.. code-block:: console

    php spark env

*************************************
对默认框架行为的影响
*************************************

CodeIgniter 系统中有一些地方使用了 ``ENVIRONMENT`` 常量。本节描述了默认框架行为如何受到影响。

错误报告
===============

将 ``ENVIRONMENT`` 常量设置为 ``development`` 值将导致所有 PHP 错误在发生时渲染到浏览器。
相反,将常量设置为 ``production`` 将禁用所有错误输出。在生产中禁用错误报告是一项 :doc:`很好的安全实践 </concepts/security>`。
