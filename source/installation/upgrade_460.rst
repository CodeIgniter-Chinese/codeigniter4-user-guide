#############################
从 4.5.8 升级到 4.6.0
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

****************
破坏性变更
****************

异常类变更
=================

部分类抛出的异常类已经变更。某些异常类的父类也已变更。
详情请参见 :ref:`变更记录 <v460-behavior-changes-exceptions>`。

如果你的代码会捕获这些异常，请修改对应的异常类。

.. _upgrade-460-time-create-from-timestamp:

Time::createFromTimestamp() 时区变更
===========================================

现在，如果你没有显式传入时区，
:ref:`Time::createFromTimestamp() <time-createfromtimestamp>` 会返回一个使用 **UTC** 的 Time
实例。在 v4.4.6 到 v4.6.0 之前的版本中，返回的是使用当前默认时区的 Time 实例。

此行为变更是为了与 PHP 8.4 的变更保持一致。PHP 8.4 新增了
``DateTimeInterface::createFromTimestamp()`` 方法。

如果你想继续使用默认时区，则需要将时区作为第二个参数传入::

    use CodeIgniter\I18n\Time;

    $time = Time::createFromTimestamp(1501821586, date_default_timezone_get());

.. _upgrade-460-time-keeps-microseconds:

Time 保留微秒
=======================

在之前的版本中，:doc:`Time <../libraries/time>` 在某些情况下会丢失微秒。
现在这些 bug 已被修复。

由于这些修复，``Time`` 比较的结果可能会不同：

.. literalinclude:: upgrade_460/006.php
   :lines: 2-

在这种情况下，你需要移除微秒：

.. literalinclude:: upgrade_460/007.php
   :lines: 2-

以下情况现在也会保留微秒：

.. literalinclude:: upgrade_460/002.php
   :lines: 2-

.. literalinclude:: upgrade_460/003.php
   :lines: 2-

请注意，表示当前时间的 ``Time`` 在此前版本中已保留微秒。

.. literalinclude:: upgrade_460/004.php
   :lines: 2-

另外，返回 ``int`` 的方法仍然会丢失微秒。

.. literalinclude:: upgrade_460/005.php
   :lines: 2-

.. _upgrade-460-time-set-timestamp:

Time::setTimestamp() 行为修复
=================================

在之前的版本中，如果对一个使用非默认时区的 Time 实例调用 ``Time::setTimestamp()``，
可能会返回日期/时间错误的 Time 实例。

该 bug 已修复，现在它的行为与 ``DateTimeImmutable`` 相同：

.. literalinclude:: upgrade_460/008.php
   :lines: 2-

请注意，如果你使用的是默认时区，则行为没有变化：

.. literalinclude:: upgrade_460/009.php
   :lines: 2-

.. _upgrade-460-registrars-with-dirty-hack:

注册器的脏数据修复
==========================

为了防止 :ref:`registrars` 的自动发现执行两次，现在当 Registrar 类被加载或实例化时，
如果它实例化了一个 Config 类（该类继承自 ``CodeIgniter\Config\BaseConfig``），
就会抛出 ``ConfigException``。

这是因为如果注册器的自动发现执行两次，可能会向 Config 类的属性中添加重复的值。

所有 Registrar 类（所有命名空间中的 **Config/Registrar.php**）都必须修改，
确保它们在被加载或实例化时不会实例化任何 Config 类。

如果你使用的包/模块提供了这样的 Registrar 类，则这些包/模块中的 Registrar 类也需要修复。

下面是一个不再有效的代码示例：

.. literalinclude:: upgrade_460/001.php

.. _upgrade-460-sid-change:

Session ID（SID）变更
=======================

现在，:doc:`../libraries/sessions` 会强制使用 PHP 默认的 32 个字符 SID，
并且每个字符有 4 位熵。此变更是为了与 PHP 9 的行为保持一致。

换句话说，现在始终使用以下设置：

.. code-block:: ini

    session.sid_bits_per_character = 4
    session.sid_length = 32

在之前的版本中，会遵循 PHP ini 设置。因此，此变更可能会改变你的 SID 长度。

如果你不能接受此变更，请自定义 Session 类。

接口变更
=================

部分接口已发生变更。实现这些接口的类应更新其 API 以反映这些变更。
详情请参见 :ref:`变更记录 <v460-interface-changes>`。

方法签名变更
========================

部分方法签名已发生变更。扩展这些类的类应更新其 API 以反映这些变更。
详情请参见 :ref:`变更记录 <v460-method-signature-changes>`。

移除已弃用项
========================

部分已弃用项已被移除。如果你仍在使用这些项，或者正在扩展这些类，请升级你的代码。
详情请参见 :ref:`变更记录 <v460-removed-deprecated-items>`。

*********************
破坏性增强
*********************

.. _upgrade-460-filters-changes:

过滤器变更
===============

``Filters`` 类已变更，现在允许同一个过滤器在 before 或 after 中以不同参数执行多次。

如果你扩展了 ``Filters``，则需要对其进行修改，以符合以下变更：

- 数组属性 ``$filters`` 和 ``$filtersClasses`` 的结构已变更。
- 属性 ``$arguments`` 和 ``$argumentsClass`` 不再使用。
- ``Filters`` 已调整为同一个过滤器类不会被实例化多次。如果某个过滤器类同时用于 before 和 after，则会使用同一个实例。

*************
项目文件
*************

**项目空间** （根目录、app、public、writable）中的部分文件已更新。
由于这些文件位于 **system** 范围之外，框架不会在没有你介入的情况下自动修改它们。

目前有一些第三方 CodeIgniter 模块可用于协助合并项目空间中的变更：
`在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容变更
===============

以下文件有较大改动（包括弃用项或界面调整），建议将更新后的版本与你的应用程序进行合并：

配置
------

- app/Config/Feature.php
    - ``Config\Feature::$autoRoutesImproved`` 已变更为 ``true``。
    - 新增了 ``Config\Feature::$strictLocaleNegotiation``。
- app/Config/Routing.php
    - ``Config\Routing::$translateUriToCamelCase`` 已变更为 ``true``。
- app/Config/Kint.php
    - 已移除 ``Config\Kint::$richSort``。v6 中的 Kint 不再使用 ``AbstractRenderer::SORT_FULL``。如果你的代码中保留此属性，会因为常量未定义而导致运行时错误。

所有变更
===========

以下列出了 **项目空间** 中所有已变更的文件；
其中很多只是注释或格式调整，不会影响运行时行为：

- app/Config/Cache.php
- app/Config/Constants.php
- app/Config/Database.php
- app/Config/Feature.php
- app/Config/Format.php
- app/Config/Kint.php
- app/Config/Routing.php
- app/Config/Security.php
- app/Views/errors/html/debug.css
- app/Views/errors/html/error_400.php
- preload.php
- public/index.php
- spark
