#############################
从 4.2.6 升级到 4.2.7
#############################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

重大变更
****************

set_cookie()
============

由于一个错误,之前版本的 :php:func:`set_cookie()` 和 :php:meth:`CodeIgniter\\HTTP\\Response::setCookie()`
没有使用 ``Config\Cookie`` 中的 ``$secure`` 和 ``$httponly`` 值。
即使在 ``Config\Cookie`` 中设置了 ``$secure = true``,以下代码也不会发出带有安全标志的 Cookie::

    helper('cookie');

    $cookie = [
        'name'  => $name,
        'value' => $value,
    ];
    set_cookie($cookie);
    // 或者
    $this->response->setCookie($cookie);

但是现在对于未指定的选项,会使用 ``Config\Cookie`` 中的值。
如果在 ``Config\Cookie`` 中设置了 ``$secure = true``,上面的代码现在会发出带有安全标志的 Cookie。

如果你的代码依赖于此错误,请更改为显式指定必要的选项::

    $cookie = [
        'name'     => $name,
        'value'    => $value,
        'secure'   => false, // 显式设置
        'httponly' => false, // 显式设置
    ];
    set_cookie($cookie);
    // 或者
    $this->response->setCookie($cookie);

其他
======

- ``Time::__toString()`` 现在与本地设置无关。它在所有本地设置中都返回类似 '2022-09-07 12:00:00' 的与数据库兼容的字符串。大多数本地设置不受此更改的影响。 但在一些如 `ar`、`fa` 的本地设置中, ``Time::__toString()`` (或 ``(string) $time`` 或隐式转换为字符串)不再返回本地化的日期时间字符串。如果你想获取本地化的日期时间字符串,请使用 :ref:`Time::toDateTimeString() <time-todatetimestring>`。
- 当验证带星号 (``*``) 的字段时,验证规则 ``required_without`` 的逻辑已更改为单独验证每个数组项,并且规则方法的方法签名也已更改。扩展类应相应地更新参数,以免违反LSP。

项目文件
*************

4.2.7 版本没有更改项目文件中的任何可执行代码。

所有更改
===========

这是 **项目空间** 中已更改的所有文件的列表;其中许多仅为注释或格式更改,不会影响运行时:

* app/Common.php
