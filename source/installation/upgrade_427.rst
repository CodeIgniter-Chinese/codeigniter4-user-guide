#############################
从 4.2.6 升级到 4.2.7
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

破坏性变更
****************

set_cookie()
============

由于一个 Bug，之前版本中的 :php:func:`set_cookie()` 和
:php:meth:`CodeIgniter\\HTTP\\Response::setCookie()`
并未使用 ``Config\Cookie`` 中的 ``$secure`` 和 ``$httponly`` 值。
即使在 ``Config\Cookie`` 中将 ``$secure = true``，下面的代码也不会发送带有 secure 标志的 Cookie::

    helper('cookie');

    $cookie = [
        'name'  => $name,
        'value' => $value,
    ];
    set_cookie($cookie);
    // 或者
    $this->response->setCookie($cookie);

现在，对于未明确指定的选项，将会使用 ``Config\Cookie`` 中的值。
如果在 ``Config\Cookie`` 中将 ``$secure = true``，上述代码现在会发送带有 secure 标志的 Cookie。

如果你的代码依赖于这个 Bug，请修改代码，显式指定所需的选项::

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

- ``Time::__toString()`` 现在与区域设置无关。无论使用何种区域设置，它都会返回与数据库兼容的字符串，例如 '2022-09-07 12:00:00'。大多数区域设置不受此更改影响，但在少数区域设置（如 `ar`、`fa`）中，``Time::__toString()`` （或 ``(string) $time``，或隐式转换为字符串）将不再返回本地化的日期时间字符串。如果需要获取本地化的日期时间字符串，请改用 :ref:`Time::toDateTimeString() <time-todatetimestring>`。
- 验证规则 ``required_without`` 的逻辑已更改：在使用通配符（``*``）验证字段时，现在会对数组中的每一项分别进行验证，同时该规则方法的方法签名也已发生变化。扩展该规则的类同样需要更新其参数，以避免破坏 LSP。

项目文件
*************

4.2.7 版本未对项目文件中的任何可执行代码进行更改。

所有变更
===========

以下是 **项目空间** 中所有发生变更的文件列表；
其中许多只是简单的注释或格式调整，对运行时没有任何影响：

* app/Common.php
