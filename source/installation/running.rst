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
#. 如果你想要使用数据库，用文本编辑器打开 **app/Config/Database.php** 文件并进行数据库设置。同样的，也可以在 ``.env`` 文件里进行如上设置。

在生产环境里需要做的另一个件事就是关闭PHP的错误报告以及其他所有的只在开发环境里的功能。
在CodeIgniter中，可以通过设置 ``ENVIRONMENT`` 常量来进行。关于这一特性，在文档 :doc:环境 </general/environments>`
中进行了更为详尽的介绍。
在默认情况下，应用程序会使用"production"(生产）环境。为了更为充分地使用所提供的 debug（问题定位）工具，你需要将环境设置为 "develop" (开发环境）

.. note:: 如果你想要在一台web服务器上运行你的网站。你需要修改项目线下的 ``writable`` 文件夹的权限，从而使得你的web服务器的当前用户可以对它进行写入。

本地开发主机
=================================================

CodeIgniter4 中内置了一个本地开发用的主机，利用了PHP内置的web服务器并实现了 CodeIgniter 的路由机制。
你可以使用主目录下的如下如下命令行中的 ``serve`` 脚本来启动::

    php spark serve

这将会启动服务器，与此同时，你可以在浏览器中输入以下 http://localhost:8080 地址来浏览你的应用。

.. note:: 内置的开发服务器只应该在本地开发机器上使用。绝对不要将其用于生产服务器中

如果你想在服务器上运行一个不仅仅是localhost，而是其他站点名的网站，你需要首先将该站点加入到你的 ``hosts`` 文件中。
该文件实际所处的位置根据不同的操作系统会存在差异，不过对于所有Unix类型的系统（包括OS X），该文件都是位于 **/etc/hosts** 。

本地开发主机可以通过三个命令行选项来进行自定义化:

- 你可以使用 ``--host`` 命令行选项来指定当前应用所位于的主机名::

    php spark serve --host=example.dev

- 默认情况下，服务器在8080端口上运行；不过如果你可能会需要多个站点同时运行，或者在8080端口上已有一个应用正在部署。那么就可以通过 ``--port`` 选项来指定另一个端口::

    php spark serve --port=8081

- 你也可以指定不同的PHP版本，通过 ``--php`` 选项，同时指定你想使用的对应的PHP版本所处的路径::

    php spark serve --php=/usr/bin/php7.6.5.4

在Apache上部署主机
=================================================

CodeIgniter4 的 webapp 通常部署在一个网站主机上。在本文档中我们将 Apache 的 ``httpd`` 进程假定为标准使用的平台。

Apache 在许多平台中默认集成，不过也能够以一个安装包（其中包含数据库引擎和PHP执行文件）从 [Bitnami] 上下载(https://bitnami.com/stacks/infrastructure)

.htaccess
-------------------------------------------------------

本文档中假定你可以使用 "mod_rewrite" 模块，该模块可以在URL中移除 "index.php" 这一部分。

确保该模块（重写模块）在主配置文件中已被启用（未注释），例如 ``apache2/conf/httpd.conf``::

    LoadModule rewrite_module modules/mod_rewrite.so

与此同时，确保默认的文档根目录 <Directory> 元素中也启用了该模块，在 "AllowOverride" 设置中::

    <Directory "/opt/lamp7.2/apache2/htdocs">
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

虚拟主机
-------------------------------------------------------

我们推荐使用虚拟主机的配置来运行你的应用。
你可以为每个应用设置不同的别名。

确保虚拟主机模块在主配置文件中启用（未注释），例如 ``apache2/conf/httpd.conf``::

    LoadModule vhost_alias_module modules/mod_vhost_alias.so

在你的主机配置文件（hosts文件）里增加一个主机别名，在unix类型的平台上通常是 ``/etc/hosts`` ，而在Windows上通常是 ``c:/Windows/System32/drivers/etc/hosts`` 。
在该文件中增加一行，比如 "myproject.local" 或 "myproject.test"，举例来说::

    127.0.0.1 myproject.local

在虚拟主机配置中，为你的 webapp 增加一个 <VirtualHost> 元素，例如在 ``apache2/conf/extra/httpd-vhost.conf`` 中::

    <VirtualHost *:80>
        DocumentRoot "/opt/lamp7.2/apache2/htdocs/myproject/public"
        ServerName myproject.local
        ErrorLog "logs/myproject-error_log"
        CustomLog "logs/myproject-access_log" common
    </VirtualHost>

如果你的项目目录并不位于 Apache 的文档根目录下，你的 <VirtualHost> 元素就需要一个嵌套的 <Directory> 元素来为服务器访问这些文件提供授权。

测试
-------------------------------------------------------

上述配置完成后，你的 webapp 应该就可以通过在浏览器上输入 ``http://myproject.local`` 的 URL 来进行访问了。

每当你更改了它的配置后，Apache 都需要被重新启动

通过 Vagrant 部署主机
=================================================

虚拟化也是一个有效地测试你希望部署的环境中的 webapp 的实现情况的方式，即使你是在一个不同环境中进行部署的话。
即使你为两个环境使用了相同的平台，虚拟化也可以为测试提供独立的环境。

相关的代码位于 ``VagrantFile.dist`` 中，该文件也可以被复制到 ``VagrantFile`` 里，并根据你的系统的情况来进行增减。例如为特定的数据库或缓存引擎提供访问。

设置
-------------------------------------------------------

我们假设了你已经安装了 `VirtualBox <https://www.virtualbox.org/wiki/Downloads>`_ 和 `Vagrant <https://www.vagrantup.com/downloads.html>`_ 的指定平台版本。

我们的 Vagrant 配置文件默认你在系统中使用 `ubuntu/bionic64 Vagrant box
<https://app.vagrantup.com/ubuntu/boxes/bionic64>`_  。

Vagrant 配置文件假定你是这样进行安装的::

    vagrant box add ubuntu/bionic64

测试
-------------------------------------------------------

设置完成后，你就可以用以下命令在虚拟机中部署你的 webapp ::

    vagrant up

你的 webapp 就可以通过 ``http://localhost:8080`` 来访问，而当次构建的代码覆盖率测试报告可以通过 ``http://localhost:8081`` ，用户指南通过 ``http://localhost:8082`` 进行访问。
