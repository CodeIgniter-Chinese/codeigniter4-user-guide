###############################
从 4.2.10 升级到 4.2.11
###############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

破坏性变更
****************

.. _upgrade-4211-proxyips:

Config\\App::$proxyIPs
======================

配置值的格式已更改。现在，你必须将代理 IP 地址与客户端 IP 地址对应的 HTTP 标头名称成对设置为数组::

    public $proxyIPs = [
            '10.0.1.200'     => 'X-Forwarded-For',
            '192.168.5.0/24' => 'X-Forwarded-For',
    ];

如果仍使用旧格式的配置值，将抛出 ``ConfigException``。

.. _upgrade-4211-session-key:

Session 处理器 Key 变更
===========================

:ref:`sessions-databasehandler-driver`、
:ref:`sessions-memcachedhandler-driver` 和
:ref:`sessions-redishandler-driver`
的 Session 数据记录 Key 已更改。因此，如果你使用这些 Session 处理器，升级后所有现有的会话数据都会失效。

- 使用 ``DatabaseHandler`` 时，Session 表中 ``id`` 列的值现在包含 Session Cookie 名称（``Config\App::$sessionCookieName``）。
- 使用 ``MemcachedHandler`` 或 ``RedisHandler`` 时，Key 值包含 Session Cookie 名称（``Config\App::$sessionCookieName``）。

``id`` 列和 Memcached Key 都有最大长度限制（250 字节）。
如果以下值超过最大长度，Session 将无法正常工作。

- 使用 ``DatabaseHandler`` 时，Session Cookie 名称、分隔符和 Session ID（默认 32 个字符）
- 使用 ``MemcachedHandler`` 时，前缀（``ci_session``）、Session Cookie 名称、分隔符和 Session ID

项目文件
*************

4.2.11 版本没有修改项目文件中的任何可执行代码。

所有变更
===========

以下列出了 **项目空间** 中所有发生变更的文件；
其中许多只是简单的注释或格式调整，不会影响运行时：

* app/Config/App.php
* app/Config/Autoload.php
* app/Config/Logger.php
* app/Config/Toolbar.php
* app/Views/welcome_message.php
* composer.json
* phpunit.xml.dist
