###############
时间和日期
###############

CodeIgniter 提供了一个完全本地化的、不可变的日期/时间类,该类基于 PHP 的 DateTimeImmutable 对象构建,但使用 Intl 扩展的功能在时区之间转换时间并针对不同的语言环境正确显示输出。这个类是 ``Time`` 类,位于 ``CodeIgniter\I18n`` 命名空间中。

.. note:: 由于 Time 类扩展了 ``DateTimeImmutable``,如果这个类没有提供你需要的功能,你很可能可以在 `DateTimeImmutable <https://www.php.net/manual/en/class.datetimeimmutable.php>`_ 类本身中找到它们。

.. note:: 在 v4.3.0 之前,Time 类扩展了 ``DateTime``,并且一些继承的方法改变了当前对象状态。这个 bug 在 v4.3.0 中修复了。如果你需要旧的 Time 类用于向后兼容,你可以暂时使用已弃用的 ``TimeLegacy`` 类。

.. contents::
    :local:
    :depth: 2

*************
实例化
*************

有几种方法可以创建新的 Time 实例。第一种就是像任何其他类一样简单地创建一个新实例。当你以这种方式执行时,你可以传递一个表示所需时间的字符串。这可以是 PHP 的 strtotime 函数可以解析的任何字符串:

.. literalinclude:: time/001.php

你可以在第二个和第三个参数中分别传递表示时区和语言环境的字符串。时区可以是 PHP 的 `DateTimeZone <https://www.php.net/manual/en/timezones.php>`__ 类支持的任何时区。语言环境可以是 PHP 的 `Locale <https://www.php.net/manual/en/class.locale.php>`__ 类支持的任何语言环境。如果没有提供语言环境或时区,将使用应用程序默认值。

.. literalinclude:: time/002.php

now()
=====

Time 类有几个帮助方法来实例化该类。第一个是 ``now()`` 方法,它返回一个设置为当前时间的新实例。你可以在第二个和第三个参数中分别传递表示时区和语言环境的字符串。如果没有提供语言环境或时区,将使用应用程序默认值。

.. literalinclude:: time/003.php

parse()
=======

这个辅助方法是默认构造函数的静态版本。它以 DateTimeImmutable 构造函数可以接受的字符串作为第一个参数,时区作为第二个参数,语言环境作为第三个参数:

.. literalinclude:: time/004.php

today()
=======

返回一个新的实例,日期设置为当前日期,时间设置为午夜。它在第一个和第二个参数中接受时区和语言环境的字符串:

.. literalinclude:: time/005.php

yesterday()
===========

返回一个新的实例,日期设置为昨天的日期,时间设置为午夜。它在第一个和第二个参数中接受时区和语言环境的字符串:

.. literalinclude:: time/006.php

tomorrow()
==========

返回一个新的实例,日期设置为明天的日期,时间设置为午夜。它在第一个和第二个参数中接受时区和语言环境的字符串:

.. literalinclude:: time/007.php

createFromDate()
================

给定独立的 **year**、**month** 和 **day** 输入,将返回一个新的实例。如果这些参数中的任何一个未提供,它将使用当前值来填充它。在第四个和第五个参数中接受时区和语言环境的字符串:

.. literalinclude:: time/008.php

createFromTime()
================

类似于 ``createFromDate()``,只关心 **hours**、**minutes** 和 **seconds**。使用当前日期作为 Time 实例的日期部分。在第四个和第五个参数中接受时区和语言环境的字符串:

.. literalinclude:: time/009.php

create()
========

前两个方法的组合,以 **year**、**month**、**day**、**hour**、**minutes** 和 **seconds** 作为单独的参数。未提供的值将使用当前日期和时间来确定。在第四个和第五个参数中接受时区和语言环境的字符串:

.. literalinclude:: time/010.php

createFromFormat()
==================

这是 DateTimeImmutable 同名方法的替代方法。这允许同时设置时区,并返回一个 ``Time`` 实例,而不是 DateTimeImmutable:

.. literalinclude:: time/011.php

createFromTimestamp()
=====================

该方法获取一个 UNIX 时间戳和可选的时区和语言环境来创建一个新的 Time 实例:

.. literalinclude:: time/012.php

createFromInstance()
====================

当使用提供 DateTime 实例的其他库时,你可以使用此方法将其转换为 Time 实例,可选设置语言环境。时区将自动从传入的 DateTime 实例中确定:

.. literalinclude:: time/013.php

toDateTime()
============

虽然不是一个实例化方法,但此方法与 **instance** 方法相反,允许你将 Time 实例转换为 DateTime 实例。这会保留时区设置,但会丢失语言环境,因为 DateTime 不知道语言环境:

.. literalinclude:: time/014.php


********************
显示值
********************

由于 Time 类扩展了 DateTimeImmutable,因此你可以获得它提供的所有输出方法,包括 ``format()`` 方法。
然而,DateTimeImmutable 方法不提供本地化的结果。然而,Time 类确实提供了一些帮助方法来显示值的本地化版本。

toLocalizedString()
===================

这是 DateTimeImmutable 的 ``format()`` 方法的本地化版本。但是,与你可能熟悉的值不同,你必须使用 `IntlDateFormatter <https://www.php.net/manual/en/class.intldateformatter.php>`__ 类可以接受的值。
可以在 `这里 <https://unicode-org.github.io/icu-docs/apidoc/released/icu4c/classSimpleDateFormat.html#details>`__ 找到值的完整列表。

.. literalinclude:: time/015.php

.. _time-todatetimestring:

toDateTimeString()
==================

这是三个帮助方法中的第一个,用于处理 `IntlDateFormatter <https://www.php.net/manual/en/class.intldateformatter.php>`_ 而不必记住它们的值。
这将返回以 (Y-m-d H:i:s) 格式化的本地化字符串版本:

.. literalinclude:: time/016.php

toDateString()
==============

仅显示 Time 的本地化日期部分:

.. literalinclude:: time/017.php

toTimeString()
==============

仅显示值的本地化时间部分:

.. literalinclude:: time/018.php

humanize()
==========

此方法返回一个字符串,该字符串以人类可读的格式显示当前日期/时间与实例之间的差异,这种格式旨在易于理解。它可以创建像“3小时前”、“1个月内”等字符串:

.. literalinclude:: time/019.php

显示的确切时间如下确定:

=============================== =================================
时间差                           结果
=============================== =================================
$time > 1年 且 < 2年            1年内/1年前
$time > 1月 且 < 1年            6个月内/6个月前
$time > 7天 且 < 1月            3周内/3周前
$time > 今天 且 < 7天           4天内/4天前
$time == 明天/昨天              明天/昨天
$time > 59分钟 且 < 1天         2小时内/2小时前
$time > 现在 且 < 1小时         35分钟内/35分钟前
$time == 现在                    现在
=============================== =================================

确切使用的语言通过语言文件 **Time.php** 控制。

******************************
使用单个值
******************************

Time 对象提供了许多方法来获取和设置现有实例的各个项,如年、月、小时等。通过以下方法检索到的所有值都将完全本地化,并尊重创建 Time 实例时使用的语言环境。

以下所有 ``getX()`` 和 ``setX()`` 方法也可以当作类属性使用。所以,对像 ``getYear()`` 这样的方法调用也可以通过 ``$time->year`` 访问,以此类推。

获取器
=======

存在以下基本获取器:

.. literalinclude:: time/020.php

除此之外,还有一些方法可以提供有关日期的其他信息:

.. literalinclude:: time/021.php

getAge()
--------

根据出生日期返回 Time 实例与当前时间之间的年龄。非常适合根据生日检查某人的年龄:

.. literalinclude:: time/022.php

getDST()
--------

根据 Time 实例是否当前正在观察夏令时返回 boolean true/false:

.. literalinclude:: time/023.php

getLocal()
----------

如果 Time 实例与应用程序当前运行的时区相同,则返回 boolean true:

.. literalinclude:: time/024.php

getUtc()
--------

如果 Time 实例处于 UTC 时间,则返回 boolean true:

.. literalinclude:: time/025.php

getTimezone()
-------------

返回一个新的 `DateTimeZone <https://www.php.net/manual/en/class.datetimezone.php>`__ 对象,将时区设置为 Time 实例的时区:

.. literalinclude:: time/026.php

getTimezoneName()
-----------------

返回 Time 实例的完整 `时区字符串 <https://www.php.net/manual/en/timezones.php>`__:

.. literalinclude:: time/027.php

设置器
=======

存在以下基本设置器。如果设置的值超出范围,将抛出 ``InvalidArgumentExeption``。

.. note:: 所有设置器都将返回一个新的 Time 实例,保留原始实例不变。

.. note:: 如果值超出范围,所有设置器都会抛出 InvalidArgumentException。

.. literalinclude:: time/028.php

setTimezone()
-------------

将时间从当前时区转换到新时区:

.. literalinclude:: time/029.php

setTimestamp()
--------------

返回一个新的实例,日期设置为新时间戳:

.. literalinclude:: time/030.php

修改值
===================

以下方法允许你通过添加或减去当前 Time 的值来修改日期。这不会修改现有的 Time 实例,而是返回一个新的实例。

.. literalinclude:: time/031.php

比较两个时间
===================

以下方法允许你将一个 Time 实例与另一个进行比较。在比较之前,所有比较都会先转换为 UTC,以确保不同时区的响应正确。

equals()
--------

确定传入的日期时间是否等于当前实例。在这种情况下,相等意味着它们表示同一时间点,不需要在同一时区,因为两个时间都转换为 UTC 进行了比较:

.. literalinclude:: time/032.php

被测试的值可以是一个 Time 实例、一个 DateTime 实例,或者一个 DateTime 实例可以理解的完整日期时间的字符串。当作为第一个参数传递字符串时,可以将时区字符串传递为第二个参数。如果未给定时区,将使用系统默认值:

.. literalinclude:: time/033.php

sameAs()
--------

这个方法与 ``equals()`` 方法完全相同,只有当日期、时间和时区全部相同时才返回 true:

.. literalinclude:: time/034.php

isBefore()
----------

检查传入的时间是否在当前实例之前。比较是针对两个时间的 UTC 版本完成的:

.. literalinclude:: time/035.php

被测试的值可以是一个 Time 实例、一个 DateTime 实例,或者一个 DateTime 实例可以理解的完整日期时间的字符串。当作为第一个参数传递字符串时,可以将时区字符串传递为第二个参数。如果未给定时区,将使用系统默认值:

.. literalinclude:: time/036.php

isAfter()
---------

工作原理与 ``isBefore()`` 完全相同,只是检查时间是否在传入的时间之后:

.. literalinclude:: time/037.php

查看差异
===================

要直接比较两个 Time,你需要使用 ``difference()`` 方法,它返回一个 ``CodeIgniter\I18n\TimeDifference`` 实例。第一个参数是一个 Time 实例、一个 DateTime 实例或一个包含日期/时间的字符串。 如果在第一个参数中传递了一个字符串,第二个参数可以是一个时区字符串:

.. literalinclude:: time/038.php

一旦你有了 TimeDifference 实例,你就有几种方法可以用来查找两个时间之间的差异信息。如果它在原始时间之前,返回的值将为负数,如果在未来,则返回正数:

.. literalinclude:: time/039.php

你可以使用 ``getX()`` 方法,也可以像访问属性一样访问计算的值:

.. literalinclude:: time/040.php

humanize()
----------

与 Time 的 ``humanize()`` 方法非常相似,它返回一个字符串,以人类可读的格式显示时间之间的差异,这种格式旨在易于理解。它可以创建像 “3小时前”、“1个月内” 等字符串。处理非常近期的日期的方式存在最大区别:

.. literalinclude:: time/041.php

显示的确切时间如下确定:

=============================== =================================
时间差                           结果
=============================== =================================
$time > 1年 且 < 2年            1年内/1年前
$time > 1月 且 < 1年            6个月内/6个月前
$time > 7天 且 < 1月            3周内/3周前
$time > 今天 且 < 7天           4天内/4天前
$time > 1小时 且 < 1天          8小时内/8小时前
$time > 1分钟 且 < 1小时        35分钟内/35分钟前
$time < 1分钟                    现在
=============================== =================================

确切使用的语言通过语言文件 **Time.php** 控制。
