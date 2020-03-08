运行你的应用程序
###############################################################################

.. contents::
    :local:
    :depth: 1

一个CodeIgniter 4的程序能够通过以下几种方式来运行：部署在一台web服务器上，使用虚拟化，或者使用CodeIgniter的命令行工具以便测试。
本节阐述了如何使用以上技术来进行部署，以及介绍了一些高级用法与如何做出贡献。

如果CodeIgniter对你来说相当陌生，请阅读用户手册中的 :doc:`准备开始 </intro/index>` 这节来学习如何构建一个动态的PHP应用，祝你玩得开心！

初始化配置与设置
=================================================

#. 用一个文本编辑器打开 **app/Config/App.php** 文件并设置你的baseURL（网站基础URL）。如果你希望更灵活点，也可以通过编辑 ``.env`` 文件，新增或更改其中的 **app.baseURL="http://example.com"** 来更改baseURL。
#. 如果你想要使用数据库，用文本编辑器打开 **app/Config/Database.php** 文件并进行数据库设置。同样的，也可以在 ``.env`` 文件里进行如上设置。If you intend to use a database, open the

在生产环境里需要做的另一个件事就是关闭PHP的错误报告以及其他所有的只在开发环境里的功能。
在CodeIgniter中，可以通过设置 ``ENVIRONMENT`` 常量来进行。关于这一特性，在文档 :doc:环境 </general/environments>`
中进行了更为详尽的介绍。
在默认情况下，应用程序会使用"production"(生产）环境。为了更为充分地使用所提供的debug（问题定位）工具，你需要将环境设置为"develop"(开发环境）

.. note:: 如果你想要在一台web服务器上运行你的网站。你需要修改项目线下的 ``writable`` 文件夹的权限，从而使得你的web服务器的当前用户可以对它进行写入。

本地开发主机
=================================================

CodeIgniter4 中内置了一个本地开发用的主机，利用了PHP内置的web服务器并实现了CodeIgniter的路由机制。
你可以使用主目录下的如下如下命令行中的 ``serve`` 脚本来启动::

    php spark serve

这将会启动服务器，与此同时，你可以在浏览器中输入以下 http://localhost:8080 地址来浏览你的应用。

.. note:: 内置的开发服务器只应该在本地开发机器上使用。绝对不要将其用于生产服务器中

If you need to run the site on a host other than simply localhost, you'll first need to add the host
to your ``hosts`` file. The exact location of the file varies in each of the main operating systems, though
all unix-type systems (include OS X) will typically keep the file at **/etc/hosts**.

The local development server can be customized with three command line options:

- You can use the ``--host`` CLI option to specify a different host to run the application at::

    php spark serve --host=example.dev

- By default, the server runs on port 8080 but you might have more than one site running, or already have
  another application using that port. You can use the ``--port`` CLI option to specify a different one::

    php spark serve --port=8081

- You can also specify a specific version of PHP to use, with the ``--php`` CLI option, with its value
  set to the path of the PHP executable you want to use::

    php spark serve --php=/usr/bin/php7.6.5.4

Hosting with Apache
=================================================

A CodeIgniter4 webapp is normally hosted on a web server. 
Apache’s ``httpd`` is the "standard" platform, and assumed in much of our documentation.

Apache is bundled with many platforms, but can also be downloaded in a bundle 
with a database engine and PHP from [Bitnami](https://bitnami.com/stacks/infrastructure).

.htaccess
-------------------------------------------------------

The “mod_rewrite” module enables URLs without “index.php” in them, and is assumed 
in our user guide.

Make sure that the rewrite module is enabled (uncommented) in the main 
configuration file, eg. ``apache2/conf/httpd.conf``::

    LoadModule rewrite_module modules/mod_rewrite.so

Also make sure that the default document root's <Directory> element enables this too, 
in the "AllowOverride" setting::

    <Directory "/opt/lamp7.2/apache2/htdocs">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

Virtual Hosting
-------------------------------------------------------

We recommend using “virtual hosting” to run your apps. 
You can set up different aliases for each of the apps you work on,

Make sure that the virtual hosting module is enabled (uncommented) in the main 
configuration file, eg. ``apache2/conf/httpd.conf``::

    LoadModule vhost_alias_module modules/mod_vhost_alias.so

Add a host alias in your “hosts” file, typically ``/etc/hosts`` on unix-type platforms, 
or ``c:/Windows/System32/drivers/etc/hosts`` on Windows. 
Add a line to the file. This could be "myproject.local" or "myproject.test", for instance::

    127.0.0.1 myproject.local

Add a <VirtualHost> element for your webapp inside the virtual hosting configuration, 
eg. ``apache2/conf/extra/httpd-vhost.conf``::

    <VirtualHost *:80>
        DocumentRoot "/opt/lamp7.2/apache2/htdocs/myproject/public"
        ServerName myproject.local
        ErrorLog "logs/myproject-error_log"
        CustomLog "logs/myproject-access_log" common
    </VirtualHost>

If your project folder is not a subfolder of the Apache document root, then your 
<VirtualHost> element may need a nested <Directory> element to grant the web s
erver access to the files.

Testing
-------------------------------------------------------

With the above configuration, your webapp would be accessed with the URL ``http://myproject.local`` in your browser.

Apache needs to be restarted whenever you change its configuration.

Hosting with Vagrant
=================================================

Virtualization is an effective way to test your webapp in the environment you 
plan to deploy on, even if you develop on a different one. 
Even if you are using the same platform for both, virtualization provides an 
isolated environment for testing.

The codebase comes with a ``VagrantFile.dist``, that can be copied to ``VagrantFile``
and tailored for your system, for instance enabling access to specific database or caching engines.

Setting Up
-------------------------------------------------------

It assumes that you have installed `VirtualBox <https://www.virtualbox.org/wiki/Downloads>`_ and 
`Vagrant <https://www.vagrantup.com/downloads.html>`_ 
for your platform.

The Vagrant configuration file assumes you have set up a `ubuntu/bionic64 Vagrant box 
<https://app.vagrantup.com/ubuntu/boxes/bionic64>`_ on your system::

    vagrant box add ubuntu/bionic64

Testing
-------------------------------------------------------

Once set up, you can then launch your webapp inside a VM, with the command::

    vagrant up

Your webapp will be accessible at ``http://localhost:8080``, with the code coverage 
report for your build at ``http://localhost:8081`` and the user guide for 
it at ``http://localhost:8082``.
