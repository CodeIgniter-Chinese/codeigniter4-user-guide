##############################
处理多环境
##############################

开发者常常希望根据是生产环境还是开发环境能够区分不同的定制行为，例如，如果在开发环境的程序当中输出详细的错误信息这样做对开发者来说是非常有帮助的，但是这样做的话在生产环境中会造成一些安全问题。 In development environments, you might want additional tools loaded that you don't in production environments, etc.

环境常量
========================

CodeIgniter 默认使用 $_SERVER['CI_ENVIRONMENT'] 的值作为 ENVIRONMENT 常量，否则默认就是 'production'。这样能够根据不同服务器安装环境定制不同的环境依赖。

.env
----

最简单的方式是在你的 `.env </general/configuration>`_ 配置文件里设置。

.. code-block:: ini

    CI_ENVIRONMENT = development

Apache
------

如果要获取 $_SERVER['CI_ENVIRONMENT'] 的值可以在 .htaccess 的文件里，或者可以在Apache的配置文件里使用 `SetEnv <https://httpd.apache.org/docs/2.2/mod/mod_env.html#setenv>`_ 命令进行设置

.. code-block:: apache

    SetEnv CI_ENVIRONMENT development

nginx
-----

在 nginx 下，为了能够在 $_SERVER 里显示环境变量的值你必须通过 fastcgi_params 来传递。这样允许它在虚拟主机上工作来替代使用 env 去为整个服务器设置它，即使在专用服务器上运行良好。你可以修改该服务器的配置为:

.. code-block:: nginx

	server {
	    server_name localhost;
	    include     conf/defaults.conf;
	    root        /var/www;

	    location    ~* "\.php$" {
	        fastcgi_param CI_ENVIRONMENT "production";
	        include conf/fastcgi-php.conf;
	    }
	}

可选方法适用于 nginx 和其它服务器，或者你也可以完全移除这部分逻辑，并根据服务器的 IP 地址设置常量(实例)。

使用这个常量，除了会影响到一些基本的框架行为外(见下一章节），在开发过程中你还可以使用常量来区分当前运行的是什么环境。

引导文件
----------

CodeIgnite 要求在 **APPPATH/Config/Boot** 下放置一个与环境名称匹配的 PHP 脚本文件。这些文件包含你想为你的环境所做的符合要求的任何定制，无论是更新对错误显示的设置，还是加载附加开发工具，或者是添加其他东西。系统会自动加载这些文件。在新的版本中为你创建好了以下文件::

* development.php
* production.php
* testing.php

默认框架行为的影响
=====================================

CodeIgniter 系统中有几个地方用到了 ENVIRONMENT 常量。这一节将描述 它对框架行为有哪些影响。

错误报告
---------------

将 ENVIRONMENT 常量值设置为 'development'，这将导致所有发生的 PHP 错误在客户端请求页面时显示在浏览器上。相反，如果将常量设置为 'production' 将禁用所有错误输出。在生产环境禁用错误输出是 
`良好的安全实践 </concepts/security>`_。

配置文件
-------------------

另外，CodeIgnite 还可以根据不同的环境自动加载不同的配置文件，这在处理例如不同环境下有着不同的API Key的情况时相当有用。这在 `配置类 </general/configuration>`_ 文档中的“环境”一节有着更详细的介绍。
