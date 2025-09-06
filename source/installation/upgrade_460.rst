#############################
从 4.5.8 升级到 4.6.0
#############################

请根据你的安装方式参考对应的升级指南：

- :ref:`Composer 安装 App Starter 升级指南 <app-starter-upgrading>`
- :ref:`Composer 安装 将 CodeIgniter4 添加到现有项目 升级指南 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级指南 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

****************
重大变更
****************

异常类变更
=================

部分类抛出的异常类已变更，部分异常类的父类已调整。详见 :ref:`更新日志 <v460-behavior-changes-exceptions>`。

如果你的代码捕获了这些异常，请修改对应的异常类。

.. _upgrade-460-time-create-from-timestamp:

Time::createFromTimestamp() 时区变更
===========================================

当未显式传递时区参数时，:ref:`Time::createFromTimestamp() <time-createfromtimestamp>` 现在返回 **UTC** 时区的 Time 实例。在 v4.4.6 至 v4.6.0 之前的版本中，返回的是当前设置的默认时区的 Time 实例。

此行为变更是为了与 PHP 8.4 新增的 ``DateTimeInterface::createFromTimestamp()`` 方法行为保持一致。

如需保持默认时区，需显式传递时区作为第二个参数::

    use CodeIgniter\I18n\Time;

    $time = Time::createFromTimestamp(1501821586, date_default_timezone_get());

.. _upgrade-460-time-keeps-microseconds:

Time 保留微秒
=======================

在先前版本中，:doc:`Time <../libraries/time>` 在某些情况下会丢失微秒。这些问题已修复。

由于修复，``Time`` 的比较结果可能发生变化:

.. literalinclude:: upgrade_460/006.php
   :lines: 2-

在此情况下，你需要手动移除微秒:

.. literalinclude:: upgrade_460/007.php
   :lines: 2-

以下情况现在会保留微秒:

.. literalinclude:: upgrade_460/002.php
   :lines: 2-

.. literalinclude:: upgrade_460/003.php
   :lines: 2-

注意：表示当前时间的 ``Time`` 实例在此前版本中已保留微秒。

.. literalinclude:: upgrade_460/004.php
   :lines: 2-

返回 ``int`` 类型的方法仍会丢失微秒:

.. literalinclude:: upgrade_460/005.php
   :lines: 2-

.. _upgrade-460-time-set-timestamp:

Time::setTimestamp() 行为修正
=================================

在先前版本中，对非默认时区的 Time 实例调用 ``Time::setTimestamp()`` 可能返回错误日期/时间的实例。

此问题已修复，现在行为与 ``DateTimeImmutable`` 一致:

.. literalinclude:: upgrade_460/008.php
   :lines: 2-

注意：使用默认时区时行为未改变:

.. literalinclude:: upgrade_460/009.php
   :lines: 2-

.. _upgrade-460-registrars-with-dirty-hack:

注册器的脏数据修复
==========================

为防止 :ref:`registrars` 的自动发现机制重复执行，当 Registrar 类被加载或实例化时，如果实例化了 Config 类（继承自 ``CodeIgniter\Config\BaseConfig``），将会抛出 ``ConfigException``。

这是因为注册器的自动发现机制若重复执行，可能导致 Config 类属性被重复赋值。

所有 Registrar 类（所有命名空间中的 **Config/Registrar.php**）必须修改为在加载或实例化时不实例化任何 Config 类。

如果你使用的包/模块包含此类 Registrar 类，需要修复这些包/模块中的 Registrar 类。

以下是不再适用的代码示例:

.. literalinclude:: upgrade_460/001.php

.. _upgrade-460-sid-change:

Session ID (SID) 变更
=======================

现在 :doc:`../libraries/sessions` 强制使用 PHP 默认的 32 字符 SID（每字符 4 位熵）。此变更是为了匹配 PHP 9 的行为。

即始终使用以下设置:

.. code-block:: ini

    session.sid_bits_per_character = 4
    session.sid_length = 32

先前版本遵循 PHP ini 设置。因此此变更可能改变你的 SID 长度。

如无法接受此变更，请自定义 Session 类库。

接口变更
=================

部分接口已变更。实现这些接口的类应更新其 API 以反映变更。详见 :ref:`更新日志 <v460-interface-changes>`。

方法签名变更
========================

部分方法签名已变更。继承这些方法的类应更新其 API 以反映变更。详见 :ref:`更新日志 <v460-method-signature-changes>`。

移除已弃用项
========================

部分已弃用项已被移除。如仍在使用这些项或继承这些类，请更新代码。详见 :ref:`更新日志 <v460-removed-deprecated-items>`。

*********************
重大增强
*********************

.. _upgrade-460-filters-changes:

过滤器变更
===============

``Filters`` 类已变更，允许在 before 或 after 阶段多次运行相同过滤器（使用不同参数）。

如继承 ``Filters`` 类，需根据以下变更进行调整：

- 数组属性 ``$filters`` 和 ``$filtersClasses`` 的结构已变更
- 属性 ``$arguments`` 和 ``$argumentsClass`` 已停用
- ``Filters`` 已调整为不重复实例化相同过滤器类。如过滤器类在 before 和 after 阶段均使用，将复用同一实例

*************
项目文件
*************

**项目空间** （根目录、app、public、writable）中的部分文件已更新。由于这些文件位于 **system** 范围之外，需手动干预才能更新。

可通过第三方 CodeIgniter 模块辅助合并项目空间变更：`在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

内容变更
===============

以下文件有重大变更（包含弃用或视觉调整），建议将更新版本合并至你的应用：

配置
------

- app/Config/Feature.php
    - ``Config\Feature::$autoRoutesImproved`` 已变更为 ``true``
    - 新增 ``Config\Feature::$strictLocaleNegotiation``
- app/Config/Routing.php
    - ``Config\Routing::$translateUriToCamelCase`` 已变更为 ``true``
- app/Config/Kint.php
    - ``Config\Kint::$richSort`` 已被移除。Kint v6 不再使用 ``AbstractRenderer::SORT_FULL``。如果在你的代码中保留此属性，将因未定义常量而导致运行时错误。

所有变更
===========

以下是 **项目空间** 中所有发生变更的文件列表（多数为不影响运行的注释或格式调整）：

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
