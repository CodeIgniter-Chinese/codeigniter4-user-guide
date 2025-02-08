###############
时间与日期
###############

CodeIgniter 提供了一个完全本地化、不可变的日期/时间类，该类基于 PHP 的 DateTimeImmutable 类构建，但利用 Intl 扩展的功能来转换时区时间，并针对不同区域设置正确显示输出。这个类就是 ``Time`` 类，位于 ``CodeIgniter\I18n`` 命名空间。

.. note:: 由于 Time 类继承自 ``DateTimeImmutable``，如果你需要本类未提供的功能，可以在 `DateTimeImmutable`_ 类本身中找到这些功能。

.. _DateTimeImmutable: https://www.php.net/manual/zh/class.datetimeimmutable.php

.. note:: 在 v4.3.0 之前，Time 类继承自 ``DateTime``，某些继承的方法会改变当前对象状态。此问题已在 v4.3.0 中修复。如果需要向后兼容旧的 Time 类，可以暂时使用已弃用的 ``TimeLegacy`` 类。

.. contents::
    :local:
    :depth: 2

*************
实例化
*************

创建新的 Time 实例有几种方式。第一种是像普通类一样创建新实例。

这种方式下，你可以传入表示预期时间的字符串。这可以是 PHP 的 `DateTimeImmutable`_ 构造函数能解析的任何字符串。详情参见 `支持的日期和时间格式`_。

.. _支持的日期和时间格式: https://www.php.net/manual/zh/datetime.formats.php

.. literalinclude:: time/001.php

你可以在第二个和第三个参数中分别传入表示时区和区域设置的字符串。时区可以是 PHP 的 `DateTimeZone <https://www.php.net/manual/zh/timezones.php>`__ 类支持的任何时区。区域设置可以是 PHP 的 `Locale <https://www.php.net/manual/zh/class.locale.php>`__ 类支持的任何区域。如果未提供区域或时区，将使用应用默认设置。

.. literalinclude:: time/002.php

now()
=====

Time 类有几个辅助方法来实例化该类。第一个是 ``now()`` 方法，返回设置为当前时间的新实例。你可以在第二个和第三个参数中分别传入时区和区域设置的字符串。如果未提供区域或时区，将使用应用默认设置。

.. literalinclude:: time/003.php

parse()
=======

这个辅助方法是默认构造函数的静态版本。它接受 DateTimeImmutable 构造函数可接受的字符串作为第一个参数，时区作为第二个参数，区域设置作为第三个参数：

.. literalinclude:: time/004.php

today()
=======

返回日期设置为当前日期、时间设置为午夜的新实例。第一个和第二个参数接受时区和区域设置的字符串：

.. literalinclude:: time/005.php

yesterday()
===========

返回日期设置为昨天日期、时间设置为午夜的新实例。第一个和第二个参数接受时区和区域设置的字符串：

.. literalinclude:: time/006.php

tomorrow()
==========

返回日期设置为明天日期、时间设置为午夜的新实例。第一个和第二个参数接受时区和区域设置的字符串：

.. literalinclude:: time/007.php

createFromDate()
================

给定 **年**、**月**、**日** 的独立输入，将返回新实例。如果未提供任何参数，将使用当前年、月、日。第四个和第五个参数接受时区和区域设置的字符串：

.. literalinclude:: time/008.php

createFromTime()
================

类似于 ``createFromDate()``，但仅关注 **小时**、**分钟** 和 **秒**。使用当前日期作为 Time 实例的日期部分。第四个和第五个参数接受时区和区域设置的字符串：

.. literalinclude:: time/009.php

create()
========

前两个方法的组合，将 **年**、**月**、**日**、**小时**、**分钟** 和 **秒** 作为独立参数。任何未提供的值将使用当前日期和时间。第四个和第五个参数接受时区和区域设置的字符串：

.. literalinclude:: time/010.php

createFromFormat()
==================

这是 DateTimeImmutable 同名方法的替代方法。允许同时设置时区，并返回 ``Time`` 实例而非 DateTimeImmutable：

.. literalinclude:: time/011.php

.. _time-createfromtimestamp:

createFromTimestamp()
=====================

此方法接受 UNIX 时间戳，并可选择时区和区域设置来创建新的 Time 实例：

.. literalinclude:: time/012.php

如果未显式传递时区，则返回具有 **UTC** 的 Time 实例。

.. note:: 我们建议始终使用 2 个参数调用 ``createFromTimestamp()`` （即显式传递时区），除非使用 UTC 作为默认时区。

.. note:: 在 v4.4.6 到 v4.6.0 之前，当未指定时区时，此方法返回具有默认时区的 Time 实例。

createFromInstance()
====================

当处理其他提供 DateTime 实例的库时，可以使用此方法将其转换为 Time 实例，并可选择设置区域设置。时区将自动从传入的 DateTime 实例中确定：

.. literalinclude:: time/013.php

toDateTime()
============

虽然不是实例化方法，但此方法是 **instance** 方法的反向操作，允许将 Time 实例转换为 DateTime 实例。这会保留时区设置，但丢失区域设置，因为 DateTime 不感知区域：

.. literalinclude:: time/014.php


********************
显示值
********************

由于 Time 类继承自 DateTimeImmutable，你可以使用其提供的所有输出方法，包括 ``format()`` 方法。但是 DateTimeImmutable 方法不提供本地化结果。Time 类提供了许多辅助方法来显示值的本地化版本。

toLocalizedString()
===================

这是 DateTimeImmutable 的 ``format()`` 方法的本地化版本。不过，你必须使用 `IntlDateFormatter <https://www.php.net/manual/zh/class.intldateformatter.php>`__ 类可接受的值，而不是你可能熟悉的格式值。完整值列表可在此处找到。

.. literalinclude:: time/015.php

.. _time-todatetimestring:

toDateTimeString()
==================

这是三个辅助方法中的第一个，用于使用 `IntlDateFormatter <https://www.php.net/manual/zh/class.intldateformatter.php>`_ 而无需记住其值。这将返回格式为 (``Y-m-d H:i:s``) 的本地化字符串：

.. literalinclude:: time/016.php

toDateString()
==============

仅显示值的本地化日期部分：

.. literalinclude:: time/017.php

toTimeString()
==============

仅显示值的本地化时间部分：

.. literalinclude:: time/018.php

humanize()
==========

此方法返回一个字符串，以易于理解的人类可读格式显示当前日期/时间与实例之间的差异。可以生成如 "3 hours ago"、"in 1 month" 等字符串：

.. literalinclude:: time/019.php

显示的确切时间由以下方式确定：

=============================== =================================
时间差                           结果
=============================== =================================
1 年 < $time < 2 年              in 1 year / 1 year ago
1 个月 < $time < 1 年            in 6 months / 6 months ago
7 天 < $time < 1 个月            in 3 weeks / 3 weeks ago
今天 < $time < 7 天              in 4 days / 4 days ago
$time == 昨天 / 明天             Tomorrow / Yesterday
59 分钟 < $time < 1 天           in 2 hours / 2 hours ago
现在 < $time < 1 小时            in 35 minutes / 35 minutes ago
$time == 现在                    Now
=============================== =================================

结果字符串来自语言文件 **system/Language/en/Time.php**。如需覆盖，请创建 **app/Language/{locale}/Time.php**。

******************************
处理独立值
******************************

Time 对象提供多个方法用于获取和设置现有实例的独立项（如年、月、小时等）。通过以下方法获取的所有值都将完全本地化，并尊重创建 Time 实例时使用的区域设置。

所有以下 ``getX()`` 和 ``setX()`` 方法也可以像类属性一样使用。因此，像 ``getYear()`` 这样的方法调用也可以通过 ``$time->year`` 等方式访问。

Getter 方法
===========

存在以下基本 getter 方法：

.. literalinclude:: time/020.php

此外，还有一些方法可提供有关日期的额外信息：

.. literalinclude:: time/021.php

getAge()
--------

返回 Time 实例与当前时间之间的年龄（以年为单位）。非常适合根据生日检查年龄：

.. literalinclude:: time/022.php

getDST()
--------

根据 Time 实例当前是否处于夏令时返回布尔值 true/false：

.. literalinclude:: time/023.php

getLocal()
----------

如果 Time 实例与时区与应用程序当前运行时区相同，则返回布尔值 true：

.. literalinclude:: time/024.php

getUtc()
--------

如果 Time 实例处于 UTC 时间，则返回布尔值 true：

.. literalinclude:: time/025.php

getTimezone()
-------------

返回一个新的 `DateTimeZone <https://www.php.net/manual/zh/class.datetimezone.php>`__ 对象，该对象设置为 Time 实例的时区：

.. literalinclude:: time/026.php

getTimezoneName()
-----------------

返回 Time 实例的完整 `时区字符串 <https://www.php.net/manual/zh/timezones.php>`__：

.. literalinclude:: time/027.php

Setter 方法
===========

存在以下基本 setter 方法。如果设置的任何值超出范围，将抛出 ``InvalidArgumentExeption``。

.. note:: 所有 setter 方法将返回新的 Time 实例，原始实例保持不变。

.. note:: 所有 setter 方法在值超出范围时将抛出 InvalidArgumentException。

.. literalinclude:: time/028.php

setTimezone()
-------------

将时间从当前时区转换到新时区：

.. literalinclude:: time/029.php

setTimestamp()
--------------

返回日期设置为新时间戳的新实例：

.. literalinclude:: time/030.php

.. note:: 在 v4.6.0 之前，由于存在 bug，此方法可能返回不正确的日期/时间。详情参见 :ref:`升级指南 <upgrade-460-time-set-timestamp>`。

修改值
===================

以下方法允许你通过向当前 Time 添加或减去值来修改日期。这不会修改现有 Time 实例，而是返回新实例。

.. literalinclude:: time/031.php

比较两个时间
===================

以下方法允许你将一个 Time 实例与另一个进行比较。所有比较在转换到 UTC 后进行，以确保不同时区能正确响应。

equals()
--------

确定传入的日期时间是否等于当前实例。此处的"相等"意味着它们代表同一时刻，不要求处于相同时区，因为两个时间都会转换为 UTC 进行比较：

.. literalinclude:: time/032.php

被测试值可以是 Time 实例、DateTime 实例，或包含完整日期时间的字符串（需能被新 DateTime 实例理解）。当第一个参数传递字符串时，可以在第二个参数中传递时区字符串。如果未提供时区，将使用系统默认值：

.. literalinclude:: time/033.php

sameAs()
--------

此方法与 ``equals()`` 相同，但仅当日期、时间和时区都完全相同时才返回 true：

.. literalinclude:: time/034.php

isBefore()
----------

检查传入时间是否早于当前实例。比较基于两个时间的 UTC 版本：

.. literalinclude:: time/035.php

被测试值可以是 Time 实例、DateTime 实例，或包含完整日期时间的字符串（需能被新 DateTime 实例理解）。当第一个参数传递字符串时，可以在第二个参数中传递时区字符串。如果未提供时区，将使用系统默认值：

.. literalinclude:: time/036.php

isAfter()
---------

工作方式与 ``isBefore()`` 完全相同，但检查时间是否晚于传入时间：

.. literalinclude:: time/037.php

.. _time-viewing-differences:

查看差异
===================

要直接比较两个 Time 实例，可以使用 ``difference()`` 方法，该方法返回一个 ``CodeIgniter\I18n\TimeDifference`` 实例。

第一个参数可以是 Time 实例、DateTime 实例或日期/时间字符串。如果第一个参数传递字符串，第二个参数可以是时区字符串：

.. literalinclude:: time/038.php

获得 TimeDifference 实例后，可以使用多个方法获取两个时间差异的信息。如果差异时间在过去，返回值为负；如果在未来则为正：

.. literalinclude:: time/039.php

.. note:: 在 v4.4.7 之前，Time 始终在比较前将时区转换为 UTC。当包含因夏令时 (DST) 导致天数不同于 24 小时的情况时，可能导致意外结果。

    从 v4.4.7 开始，当比较处于相同时区的日期/时间时，直接进行比较而不转换为 UTC：

        .. literalinclude:: time/042.php

你可以使用 ``getX()`` 方法，或像访问属性一样访问计算值：

.. literalinclude:: time/040.php

humanize()
----------

类似于 Time 的 ``humanize()`` 方法，此方法返回一个字符串，以人类可读格式显示时间差异，便于理解。可以生成如 "3 hours ago"、"in 1 month" 等字符串。主要区别在于处理最近日期的方式：

.. literalinclude:: time/041.php

显示的确切时间由以下方式确定：

=============================== =================================
时间差                           结果
=============================== =================================
1 年 < $time < 2 年              in 1 year / 1 year ago
1 个月 < $time < 1 年            in 6 months / 6 months ago
7 天 < $time < 1 个月            in 3 weeks / 3 weeks ago
今天 < $time < 7 天              in 4 days / 4 days ago
1 小时 < $time < 1 天            in 8 hours / 8 hours ago
1 分钟 < $time < 1 小时          in 35 minutes / 35 minutes ago
$time < 1 分钟                   Now
=============================== =================================

结果字符串来自语言文件 **system/Language/en/Time.php**。如需覆盖，请创建 **app/Language/{locale}/Time.php**。
