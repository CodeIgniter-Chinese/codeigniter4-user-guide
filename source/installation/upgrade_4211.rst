###############################
从 4.2.10 升级到 4.2.11
###############################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

重大变更
****************

.. _upgrade-4211-proxyips:

Config\\App::$proxyIPs
======================

配置值格式已更改。现在你必须将代理 IP 地址和客户端 IP 地址的 HTTP 头名称设置为数组::

    public $proxyIPs = [
            '10.0.1.200'     => 'X-Forwarded-For',
            '192.168.5.0/24' => 'X-Forwarded-For',
    ];

旧格式的配置值会抛出 ``ConfigException``。

.. _upgrade-4211-session-key:

Session 处理程序密钥更改
===========================

:ref:`sessions-databasehandler-driver`、:ref:`sessions-memcachedhandler-driver` 和 :ref:`sessions-redishandler-driver` 的 session 数据记录的密钥已更改。因此,如果使用这些 session 处理程序,在升级后现有的 session 数据将失效。

- 使用 ``DatabaseHandler`` 时,session 表中的 ``id`` 列值现在包含 session cookie 名称 (``Config\App::$sessionCookieName``)。
- 使用 ``MemcachedHandler`` 或 ``RedisHandler`` 时,密钥值包含 session cookie 名称 (``Config\App::$sessionCookieName``)。

``id`` 列和 Memcached 密钥都有最大长度(250字节)。如果以下值超过那些最大长度,session 将无法正常工作。

- 使用 ``DatabaseHandler`` 时,session cookie 名称、分隔符和 session id(默认为32个字符)的组合
- 使用 ``MemcachedHandler`` 时,前缀 (``ci_session``)、session cookie 名称、分隔符和 session id 的组合

项目文件
*************

4.2.11 版本没有更改项目文件中的任何可执行代码。

所有更改
===========

这是 **项目空间** 中已更改的所有文件的列表;其中许多仅为注释或格式更改,不会影响运行时:

* app/Config/App.php
* app/Config/Autoload.php
* app/Config/Logger.php
* app/Config/Toolbar.php
* app/Views/welcome_message.php
* composer.json
* phpunit.xml.dist
