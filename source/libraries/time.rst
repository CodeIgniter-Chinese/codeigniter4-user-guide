###############
时间与日期
###############

CodeIgniter 提供一个完全本地化、不可变的日期/时间类，该类基于 PHP 的 DateTimeImmutable 类构建，但利用 Intl
扩展的功能实现时区转换，并以不同区域设置正确显示输出。此类为 ``Time`` 类，位于 ``CodeIgniter\I18n`` 命名空间中。

.. note:: 自 4.3.0 起，Time 类继承 ``DateTimeImmutable``，若需要此类未提供的功能，
    可直接在 `DateTimeImmutable`_ 类中查找。

.. _DateTimeImmutable: https://www.php.net/manual/zh/class.datetimeimmutable.php

.. note:: 4.3.0 之前，Time 类继承 ``DateTime``，部分继承方法会更改
    当前对象状态。该问题已在 4.3.0 中修复。如需向后兼容，
    可暂时使用已弃用的 ``TimeLegacy`` 类。

.. contents::
    :local:
    :depth: 2

*************
实例化
*************

创建 Time 实例有多种方式。最简单的方式是直接像普通类一样实例化。

实例化时可传入表示所需时间的字符串。该字符串可为 PHP `DateTimeImmutable`_ 构造函数能解析的任意格式。详见
`支持的日期和时间格式`_。

.. _支持的日期和时间格式: https://www.php.net/manual/zh/datetime.formats.php

.. literalinclude:: time/001.php

第二和第三个参数可分别传入时区和区域设置字符串。时区
可为 PHP `DateTimeZone <https://www.php.net/manual/zh/timezones.php>`__ 类支持的所有值。区域设置可为
PHP `Locale <https://www.php.net/manual/zh/class.locale.php>`__ 类支持的所有值。如未提供区域设置或时区，
将使用应用默认值。

.. literalinclude:: time/002.php

now()
=====

Time 类提供多个辅助方法来实例化。首先是 ``now()`` 方法，
返回一个当前时间的新实例。第二和第三个参数可分别传入时区和区域设置字符串。如未提供时区或区域设置，
将使用应用默认值。

.. literalinclude:: time/003.php

parse()
=======

此辅助方法为默认构造方法的静态版本。第一个参数为 DateTimeImmutable 构造函数可接受的字符串，第二个参数为时区，第三个参数为区域设置：

.. literalinclude:: time/004.php

today()
=======

返回新实例，日期设为当前日期，时间设为午夜。第一和第二个参数可接受时区和区域设置字符串：

.. literalinclude:: time/005.php

yesterday()
===========

返回新实例，日期设为昨天的日期，时间设为午夜。第一和第二个参数可接受时区和区域设置字符串：

.. literalinclude:: time/006.php

tomorrow()
==========

返回新实例，日期设为明天的日期，时间设为午夜。第一和第二个参数可接受时区和区域设置字符串：

.. literalinclude:: time/007.php

createFromDate()
================

分别传入 **年**、**月**、**日**，返回新实例。如省略任一参数，
将使用当前的年、月和日。第四和第五个参数可接受时区和区域设置字符串：

.. literalinclude:: time/008.php

createFromTime()
================

与 ``createFromDate()`` 类似，仅处理 **时**、**分**、**秒**。日期部分使用
当前日期。第四和第五个参数可接受时区和区域设置字符串：

.. literalinclude:: time/009.php

create()
========

结合上述两个方法，分别接受 **年**、**月**、**日**、**时**、**分**、**秒**
作为独立参数。任何未提供的值将使用当前日期和时间。第七和第八个参数可接受时区和区域设置字符串：

.. literalinclude:: time/010.php

createFromFormat()
==================

此方法为 DateTimeImmutable 同名方法的替代版本。可同时设置时区，
并返回 ``Time`` 实例而非 DateTimeImmutable：

.. literalinclude:: time/011.php

.. _time-createfromtimestamp:

createFromTimestamp()
=====================

此方法接受 UNIX 时间戳，以及可选的时区和区域设置，
创建新 Time 实例：

.. literalinclude:: time/012.php

如未显式传入时区，返回 **UTC** 时区的 Time 实例。

.. note:: 建议始终传入两个参数调用 ``createFromTimestamp()``
    （即显式传入时区），除非默认使用 UTC 时区。

.. note:: 4.4.6 至 4.6.0 之前的版本中，如未指定时区，此方法返回
    默认时区的 Time 实例。

createFromInstance()
====================

使用其他库提供的 DateTime 实例时，可使用方法将 DateTime 实例
转换为 Time 实例，并可选设置区域设置。时区将从传入的 DateTime
实例自动推断：

.. literalinclude:: time/013.php

toDateTime()
============

此方法非实例化方法，而是与 **instance** 方法相反，将 Time
实例转换为 DateTime 实例。转换保留时区设置，但丢失区域设置，因为 DateTime
不支持区域设置：

.. literalinclude:: time/014.php


********************
显示值
********************

Time 类继承自 DateTimeImmutable，因此可直接使用该类提供的所有输出方法，包括 ``format()`` 方法。
但 DateTimeImmutable 的方法不提供本地化输出。Time 类提供多个辅助方法
用于显示本地化值。

toLocalizedString()
===================

此方法为 DateTimeImmutable ``format()`` 方法的本地化版本。不同于熟悉的格式化字符，
必须使用 `IntlDateFormatter <https://www.php.net/manual/zh/class.intldateformatter.php>`__ 类可接受的值。
完整值列表见 `此处 <https://unicode-org.github.io/icu-docs/apidoc/released/icu4c/classSimpleDateFormat.html#details>`__。

.. literalinclude:: time/015.php

.. _time-todatetimestring:

toDateTimeString()
==================

此为三个辅助方法中的第一个，无需记忆 `IntlDateFormatter <https://www.php.net/manual/zh/class.intldateformatter.php>`_ 的格式化值。
返回格式化为 ``Y-m-d H:i:s`` 的本地化字符串：

.. literalinclude:: time/016.php

toDateString()
==============

仅显示 Time 的本地化日期部分：

.. literalinclude:: time/017.php

toTimeString()
==============

仅显示值的本地化时间部分：

.. literalinclude:: time/018.php

humanize()
==========

此方法返回一个字符串，以人类可读格式显示当前日期/时间与实例之间的差异，
便于快速理解。可生成类似"3 小时前"、"1 个月后"等字符串：

.. literalinclude:: time/019.php

显示时间的具体规则如下：

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

结果字符串来自语言文件 **system/Language/en/Time.php**。
如需覆盖，创建 **app/Language/{locale}/Time.php**。

******************************
处理单个值
******************************

Time 对象提供多种方法，用于获取和设置现有实例的单个值，如年、月、小时等。
通过以下方法获取的所有值都会完全本地化，并遵守
创建 Time 实例时指定的区域设置。

以下所有 ``getX()`` 和 ``setX()`` 方法均可像类属性一样使用。例如，``getYear()`` 可通过 ``$time->year`` 访问，以此类推。

Getter 方法
===========

以下为基础 getter 方法：

.. literalinclude:: time/020.php

此外，还提供多个方法获取关于日期的额外信息：

.. literalinclude:: time/021.php

getAge()
--------

返回 Time 实例与当前时间之间的年龄（以年为单位）。适用于根据生日
计算年龄的场景：

.. literalinclude:: time/022.php

getDST()
--------

返回布尔值，表示 Time 实例当前是否处于夏令时：

.. literalinclude:: time/023.php

getLocal()
----------

返回布尔值，表示 Time 实例是否与应用当前运行的时区相同：

.. literalinclude:: time/024.php

getUtc()
--------

返回布尔值，表示 Time 实例是否处于 UTC 时间：

.. literalinclude:: time/025.php

getTimezone()
-------------

返回新 `DateTimeZone <https://www.php.net/manual/zh/class.datetimezone.php>`__ 对象，时区设为 Time 实例的时区：

.. literalinclude:: time/026.php

getTimezoneName()
-----------------

返回 Time 实例的完整 `时区字符串 <https://www.php.net/manual/zh/timezones.php>`__：

.. literalinclude:: time/027.php

Setter 方法
===========

以下为基础 setter 方法。如设置的值超出范围，将抛出 ``InvalidArgumentExeption``。

.. note:: 所有 setter 均返回新的 Time 实例，原始实例保持不变。

.. note:: 如值超出范围，所有 setter 均会抛出 InvalidArgumentException。

.. literalinclude:: time/028.php

setTimezone()
-------------

将时间从当前时区转换为新时区：

.. literalinclude:: time/029.php

setTimestamp()
--------------

返回新实例，日期设为新时间戳：

.. literalinclude:: time/030.php

.. note:: 4.6.0 之前的版本中，由于 bug，此方法可能返回错误的
    日期/时间。详见 :ref:`升级指南 <upgrade-460-time-set-timestamp>`。

修改值
===================

以下方法支持通过增加或减少值来修改当前 Time 的日期。不会
修改现有 Time 实例，而是返回新实例。

.. literalinclude:: time/031.php

addCalendarMonths() / subCalendarMonths()
-----------------------------------------

通过增加或减少完整的日历月份来修改当前 Time。若需确保重复发生的日期不跳过任何日历月份，这些方法将非常有用。下表对比了初始日期为 ``2025-01-31`` 时，``addMonths()`` 与 ``addCalendarMonths()`` 的差异。

======= =========== ===================
$months addMonths() addCalendarMonths()
======= =========== ===================
1       2025-03-03  2025-02-28
2       2025-03-31  2025-03-31
3       2025-05-01  2025-04-30
4       2025-05-31  2025-05-31
5       2025-07-01  2025-06-30
6       2025-07-31  2025-07-31
======= =========== ===================

比较两个时间
===================

以下方法允许比较两个 Time 实例。所有比较均先转换为 UTC
后进行，以确保不同时区能正确响应。

equals()
--------

判断传入的日期/时间是否等于当前实例。此处的"等于"表示两者表示同一
时刻，不要求处于相同时区，因为两个时间均转换为 UTC 后
进行比较：

.. literalinclude:: time/032.php

被测试的值可为 Time 实例、DateTime 实例或完整的日期时间
字符串（格式需能被新 DateTime 实例解析）。第一个参数传入字符串时，可传入
时区字符串作为第二个参数。如未提供时区，将使用系统默认值：

.. literalinclude:: time/033.php

sameAs()
--------

此方法与 ``equals()`` 类似，但仅当日期、时间与时区
全部相同时才返回 true：

.. literalinclude:: time/034.php

isBefore()
----------

检查传入的时间是否在当前实例之前。比较基于
两个时间的 UTC 版本进行：

.. literalinclude:: time/035.php

被测试的值可为 Time 实例、DateTime 实例或完整的日期时间
字符串（格式需能被新 DateTime 实例解析）。第一个参数传入字符串时，可传入
时区字符串作为第二个参数。如未提供时区，将使用系统默认值：

.. literalinclude:: time/036.php

isAfter()
---------

与 ``isBefore()`` 工作方式相同，检查时间是否在传入时间之后：

.. literalinclude:: time/037.php

.. _time-comparing-two-times-isPast:

isPast()
--------

.. versionadded:: 4.7.0

用于判断当前实例的时间相对于“现在”是否为过去。
返回布尔值 true/false::

.. literalinclude:: time/043.php

.. _time-comparing-two-times-isFuture:

isFuture()
----------

.. versionadded:: 4.7.0

用于判断当前实例的时间相对于“现在”是否为未来。
返回布尔值 true/false::

.. literalinclude:: time/044.php

.. _time-viewing-differences:

查看差异
===================

直接比较两个 Time，应使用 ``difference()`` 方法，返回 ``CodeIgniter\I18n\TimeDifference``
实例。

第一个参数可为 Time 实例、DateTime 实例或日期/时间字符串。如
第一个参数传入字符串，第二个参数可为时区字符串：

.. literalinclude:: time/038.php

获取 TimeDifference 实例后，可使用多种方法获取两个时间
之间的差异信息。如果相对于原始时间为过去则返回负值，为未来则返回正值：

.. literalinclude:: time/039.php

.. note:: 4.4.7 之前的版本中，Time 类在比较前总是先将时区转换为 UTC。
    如果日期因夏令时（DST）导致时长并非 24 小时，
    此类转换可能会导致非预期结果。

    4.4.7 起，比较相同时区的日期/时间时，
    直接进行比较，不转换为 UTC。

        .. literalinclude:: time/042.php

可使用 ``getX()`` 方法，或像访问属性一样访问计算值：

.. literalinclude:: time/040.php

humanize()
----------

与 Time 的 ``humanize()`` 方法类似，返回人类可读格式的字符串，
显示两个时间之间的差异，便于快速理解。可生成类似"3 小时前"、
"1 个月后"等字符串。最大区别在于处理非常近的日期时：

.. literalinclude:: time/041.php

显示时间的具体规则如下：

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

结果字符串来自语言文件 **system/Language/en/Time.php**。
如需覆盖，创建 **app/Language/{locale}/Time.php**。
