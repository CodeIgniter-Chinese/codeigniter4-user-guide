############
日期与时间类
############

CodeIgniter 提供了一个完全本地化的，不变的日期与时间类，这个类建立在 PHP 原生的 DateTime 类之上，但使用了 Intl 扩展程序的功能
来进行跨时区转换时间并正确显示不同语言环境的输出。 这个类就是 **Time** 类，位于 **CodeIgniter\\I18n** 命名空间中。

.. note:: 由于 Time 类是 DateTime 类的拓展，因此如果您需要此类不提供的功能，可以在 DateTime 类中找到它们。

.. contents::
    :local:
    :depth: 1

======
实例化
======

有多种创建 Time 类实例的方法。 首先是像其他类一样简单地创建一个新实例。 当您以这种方式进行操作时，您可以传递一
个表示所需时间的字符串。 它可以是 PHP 的 strtotime() 函数可以解析的任何字符串： ::

    use CodeIgniter\I18n\Time;

    $myTime = new Time('+3 week');
    $myTime = new Time('now');

你可以在参数中分别传递表示时区和语言环境的字符串。时区可以是 PHP 的 `DateTimeZone <http://php.net/manual/en/timezones.php>`__ 类
可以支持所有时区。 语言环境可以是 PHP 的 `Locale <http://php.net/manual/en/class.locale.php>`__ 类支持的任何语言环境。
如果未提供语言环境或时区，则将使用应用程序配置中的默认值。

::

    $myTime = new Time('now', 'America/Chicago', 'en_US');

now()
-----

Time 类有几个有用的 helper 方法来实例化这个类，首先是 **now()** 方法，该方法返回设置为当前时间的新实例。 您可以在参数中
提供表示时区和语言环境的字符串。 如果未提供语言环境或时区，则将使用应用程序配置中的默认值。

::

    $myTime = Time::now('America/Chicago', 'en_US');

parse()
-------

这个 helper 程序方法是默认的构造函数的 static 版本。它以 DateTime 类构造函数可接受的任何表示时间的字符串为第一个参数，
将表示时区的字符串作为第二个参数，将表示语言环境的字符串作为第三个参数： ::

    $myTime = Time::parse('next Tuesday', 'America/Chicago', 'en_US');

today()
-------

返回一个新实例，该实例的日期设置为当前日期，时间设置为午夜。它在第一个和第二个参数中分别接受表示时区和语言环境
的字符串： ::

    $myTime = Time::today('America/Chicago', 'en_US');

yesterday()
-----------

返回一个新实例，该实例的日期设置为昨天的日期，时间设置为午夜。它在第一个和第二个参数中分别接受表示时区和语言环境
的字符串： ::

    $myTime = Time::yesterday('America/Chicago', 'en_US');

tomorrow()
-----------

返回一个新实例，该实例的日期设置为明天的日期，时间设置为午夜。它在第一个和第二个参数中分别接受表示时区和语言环境
的字符串： ::

    $myTime = Time::tomorrow('America/Chicago', 'en_US');

createFromDate()
----------------

给定 **年** 、 **月** 、 **日** 的单独输入，将返回一个新实例。如果未提供它们三个中的任何一个，它将使用当前时间的该值进行填充。在第四
和第五个参数中接受时区和语言环境的字符串： ::

    $today       = Time::createFromDate();      // 将使用现在时间的年、月、日
    $anniversary = Time::createFromDate(2018);  // 将使用现在时间的月、日
    $date        = Time::createFromDate(2018, 3, 15, 'America/Chicago', 'en_US');

createFromTime()
----------------

与 **createFromDate()** 相似，只不过它只和 **小时** 、 **分钟** 和 **秒** 有关。 使用当前时间的日期作为 Time 实例的日期
部分。 在第四个和第五个参数中接受时区和语言环境的字符串： ::

    $lunch  = Time::createFromTime(11, 30)       // 11:30 am today
    $lunch  = Time::createFromTime(11, 30)      // 今天的 11:30
    $dinner = Time::createFromTime(18, 00, 00)  // 6:00 pm today
    $dinner = Time::createFromTime(18, 00, 00)  // 今天的 18:00
    $time   = Time::createFromTime($hour, $minutes, $seconds, $timezone, $locale);

create()
--------

前面两种方法的组合，将 **年** 、 **月** 、 **日** 、 **小时** 、 **分钟** 和 **秒** 作为单独的参数。
任何未提供的值将使用当前的日期和时间来确定。 在第四个和第五个参数中接受时区和语言环境的字符串： ::

    $time = Time::create($year, $month, $day, $hour, $minutes, $seconds, $timezone, $locale);

createFromFormat()
------------------

它是替代 DateTime 构造函数的方法。它允许同时设置时区，并返回一个 **Time** 实例，而不是 DateTime 实例： ::

    $time = Time::createFromFormat('j-M-Y', '15-Feb-2009', 'America/Chicago');

createFromTimestamp()
---------------------

该方法使用 UNIX 时间戳以及时区和语言环境（可选）来创建新的 Time 实例： ::

    $time = Time::createFromTimestamp(1501821586, 'America/Chicago', 'en_US');

instance()
----------

与提供 DateTime 实例的其他 library 一起使用时，可以使用此方法将其转换为 Time 实例，可以选择设置语言环境。
时区将根据传入的 DateTime 实例自动确定： ::

    $dt   = new DateTime('now');
    $time = Time::instance($dt, 'en_US');

toDateTime()
------------

它不是用来实例化的，此方法与 **实例化** 方法相反，它允许您将 Time 实例转换为 DateTime 实例。这样会保留时区设置，
但会丢失语言环境，因为 DateTime 并不了解语言环境： ::

    $datetime = Time::toDateTime();

==========
显示时间值
==========

由于 Time 是 DateTime 类的拓展，因此您将获得提供的所有输出方法，包括 format() 方法。 但是，DateTime 方法不提供本地化结果。 不过，
Time 类提供了许多 helper 方法来显示值的本地化版本。

toLocalizedString()
-------------------

这是 DateTime 的 format() 方法的本地化版本。但是，必须使用 `IntlDateFormatter <http://php.net/manual/en/class.intldateformatter.php>`__ 类可以接受的值，
而不能使用你熟悉的值。完整的值列表可以在 `这里 <http://www.icu-project.org/apiref/icu4c/classSimpleDateFormat.html#details>`__ 找到。

::

    $time = Time::parse('March 9, 2016 12:00:00', 'America/Chicago');
    echo $time->toLocalizedString('MMM d, yyyy');   // March 9, 2016

toDateTimeString()
------------------

这是与 IntlDateFormatter 一起使用的三种辅助方法中的第一种，无需记住它们的值。这将返回一个格式化的字符串，
该字符串的格式与数据库中日期时间列的常用格式相同（Y-m-d H:i:s）： ::

    $time = Time::parse('March 9, 2016 12:00:00', 'America/Chicago');
    echo $time->toDateTimeString();     // 2016-03-09 12:00:00

toDateString()
--------------

仅返回时间与日期的日期部分： ::

    $time = Time::parse('March 9, 2016 12:00:00', 'America/Chicago');
    echo $time->toDateTimeString();     // 2016-03-09

toTimeString()
--------------

仅返回时间与日期的时间部分： ::

    $time = Time::parse('March 9, 2016 12:00:00', 'America/Chicago');
    echo $time->toTimeString();     // 12:00:00

humanize()
----------

此方法返回一个字符串，该字符串以易于理解的人类可读格式显示当前日期或时间与实例之间的差异。它会返回“ 3 小时前”、“ 1 个月内”
等字符串： ::

    // 假设现在的时间是：March 10, 2017 (America/Chicago)
    $time = Time::parse('March 9, 2016 12:00:00', 'America/Chicago');

    echo $time->humanize();     // 1 year ago

通过以下方式确定显示的确切时间：

=============================== =================================
时间差异                         结果
=============================== =================================
$time > 1 year && < 2 years      in 1 year / 1 year ago
$time > 1 month && < 1 year      in 6 months / 6 months ago
$time > 7 days && < 1 month      in 3 weeks / 3 weeks ago
$time > today && < 7 days        in 4 days / 4 days ago
$time == tomorrow / yesterday    Tomorrow / Yesterday
$time > 59 minutes && < 1 day    1:37pm
$time > now && < 1 hour          in 35 minutes / 35 minutes ago
$time == now                     Now
=============================== =================================

返回的结果的语言被语言文件 Time.php 所控制。

================
处理各个时间的值
================

Time 对象提供了许多方法来获取和设置现有实例的各个项目，例如年、月、时等。通过以下方法检索到的的所有值都会被完全本地化，
并遵守创建 Time 实例所使用的语言环境。

以下所有 `getX` 和 `setX` 方法也可以当作类属性使用。因此，对像 `getYear` 这样调用的方法也可以通过 `$time->year`
进行调用，依此类推。

获取器
-------

有以下几种基本的获取器： ::

    $time = Time::parse('August 12, 2016 4:15:23pm');

    echo $time->getYear();      // 2016
    echo $time->getMonth();     // 8
    echo $time->getDay();       // 12
    echo $time->getHour();      // 16
    echo $time->getMinute();    // 15
    echo $time->getSecond();    // 23

    echo $time->year;           // 2016
    echo $time->month;          // 8
    echo $time->day;            // 12
    echo $time->hour;           // 16
    echo $time->minute;         // 15
    echo $time->second;         // 23

除这些之外，还有许多方法可以获取有关日期的其他信息： ::

    $time = Time::parse('August 12, 2016 4:15:23pm');

    echo $time->getDayOfWeek();     // 6 - 但可能会因地区的一个星期的第一天而有所不同
    echo $time->getDayOfYear();     // 225
    echo $time->getWeekOfMonth();   // 2
    echo $time->getWeekOfYear();    // 33
    echo $time->getTimestamp();     // 1471018523 - UNIX 时间戳
    echo $time->getQuarter();       // 3

    echo $time->dayOfWeek;          // 6
    echo $time->dayOfYear;          // 225
    echo $time->weekOfMonth;        // 2
    echo $time->weekOfYear;         // 33
    echo $time->timestamp;          // 1471018523
    echo $time->quarter;            // 3

getAge()
--------

返回 Time 实例与当前时间之间的差值（以年为单位）。主要是用于根据某人的生日检查其年龄： ::

    $time = Time::parse('5 years ago');

    echo $time->getAge();   // 5
    echo $time->age;        // 5

getDST()
--------

根据 Time 实例是否正在遵守夏令时，返回布尔值 true 或 false： ::

    echo Time::createFromDate(2012, 1, 1)->getDst();     // false
    echo Time::createFromDate(2012, 9, 1)->dst;     // true

getLocal()
----------

如果 Time 实例的时区与 web 应用程序当前所在的时区位于同一时区，则返回布尔值 true： ::

    echo Time::now()->getLocal();                   // true
    echo Time::now('Europe/London')->getLocal();    // false

getUtc()
--------

如果 Time 实例使用 UTC 时间，则返回 true： ::

    echo Time::now('America/Chicago')->getUtc();    // false
    echo Time::now('UTC')->utc;                     // true

getTimezone()
-------------

返回一个新的 `DateTimeZone <http://php.net/manual/en/class.datetimezone.php>`__ 实例，该实例是 Time 实例的时区： ::

    $tz = Time::now()->getTimezone();
    $tz = Time::now()->timezone;

    echo $tz->getName();
    echo $tz->getOffset();

getTimezoneName()
-----------------

返回 Time 实例的 `完整时区字符串 <http://php.net/manual/en/timezones.php>`__ ： ::

    echo Time::now('America/Chicago')->getTimezoneName();   // America/Chicago
    echo Time::now('Europe/London')->timezoneName;          // Europe/London

设置器
=======

存在以下的基本设置器。如果设置的任何值超出允许范围，则会抛出 ``InvalidArgumentExeption`` 。

.. note:: 所有设置器都将返回一个新的 Time 实例，而原始实例保持不变。

.. note:: 如果值超出范围，则设置器将抛出 InvalidArgumentException。

::

    $time = $time->setYear(2017);
    $time = $time->setMonthNumber(4);           // April
    $time = $time->setMonthLongName('April');
    $time = $time->setMonthShortName('Feb');    // February
    $time = $time->setDay(25);
    $time = $time->setHour(14);                 // 2:00 pm
    $time = $time->setMinute(30);
    $time = $time->setSecond(54);

setTimezone()
-------------

将时间从当前时区转换为新时区： ::

    $time  = Time::parse('May 10, 2017', 'America/Chicago');
    $time2 = $time->setTimezone('Europe/London');           // 将时间从当前时区转换为新时区

    echo $time->timezoneName;   // American/Chicago
    echo $time2->timezoneName;  // Europe/London

setTimestamp()
--------------

返回日期设置为新时间戳的新实例： ::

    $time = Time::parse('May 10, 2017', 'America/Chicago');
    $time2 = $time->setTimestamp(strtotime('April 1, 2017'));

    echo $time->toDateTimeString();     // 2017-05-10 00:00:00
    echo $time2->toDateTimeString();     // 2017-04-01 00:00:00

Modifying the Value
===================

通过以下方法，您可以通过在当前时间上增加或减少值来修改日期。这不会修改现有的 Time 实例，只会返回一个新实例。

::

    $time = $time->addSeconds(23);
    $time = $time->addMinutes(15);
    $time = $time->addHours(12);
    $time = $time->addDays(21);
    $time = $time->addMonths(14);
    $time = $time->addYears(5);

    $time = $time->subSeconds(23);
    $time = $time->subMinutes(15);
    $time = $time->subHours(12);
    $time = $time->subDays(21);
    $time = $time->subMonths(14);
    $time = $time->subYears(5);

比较两个 Time
===================

以下方法使您可以将一个 Time 实例与另一个 Time 实例进行比较。在进行比较之前，首先将所有比较转换为 UTC，以确保不同时区都正确响应。

equals()
--------

确定传入的日期时间是否等于当前实例。在这种情况下，相等意味着它们表示同一时间，并且不需要位于同一时区，因为两个时间都转换为 UTC 并以这种方式进行比较： ::

    $time1 = Time::parse('January 10, 2017 21:50:00', 'America/Chicago');
    $time2 = Time::parse('January 11, 2017 03:50:00', 'Europe/London');

    $time1->equals($time2);    // true

要作比较的值可以是 Time 实例，DateTime 实例或 DateTime 类可以理解的任何表示时间的字符串。当将字符串作为第一个参数传递时，
可以将时区字符串作为第二个参数传递。 如果没有给出时区，将使用配置的默认值： ::

    $time1->equals('January 11, 2017 03:50:00', 'Europe/London');  // true

sameAs()
--------

除了只有在日期，时间和时区都相同时才返回 true，这与 **equals** 方法相同： ::

    $time1 = Time::parse('January 10, 2017 21:50:00', 'America/Chicago');
    $time2 = Time::parse('January 11, 2017 03:50:00', 'Europe/London');

    $time1->sameAs($time2);    // false
    $time2->sameAs('January 10, 2017 21:50:00', 'America/Chicago');    // true

isBefore()
----------

检查传入的时间是否在当前实例之前。两种情况下都针对 UTC 版本进行了比较： ::

    $time1 = Time::parse('January 10, 2017 21:50:00', 'America/Chicago');
    $time2 = Time::parse('January 11, 2017 03:50:00', 'America/Chicago');

    $time1->isBefore($time2);  // true
    $time2->isBefore($time1);  // false

要作比较的值可以是 Time 实例，DateTime 实例或 DateTime 类可以理解的任何表示时间的字符串。当将字符串作为第一个参数传递时，
可以将时区字符串作为第二个参数传递。 如果没有给出时区，将使用配置的默认值： ::

    $time1->isBefore('March 15, 2013', 'America/Chicago');  // false

isAfter()
---------

除了检查时间是否在传入的时间之后，其他的与 **isBefore()** 完全相同： ::

    $time1 = Time::parse('January 10, 2017 21:50:00', 'America/Chicago');
    $time2 = Time::parse('January 11, 2017 03:50:00', 'America/Chicago');

    $time1->isAfter($time2);  // false
    $time2->isAfter($time1);  // true

查看差异
========

要直接比较两个 Times，可以使用 **difference()** 方法，该方法返回 **CodeIgniter\\I18n\\TimeDifference** 实例。第一个参数可以是 Time 实例、
DateTime 实例或带有日期或时间的字符串。 如果在第一个参数中传递了表示时间字符串，则第二个参数可以是时区字符串： ::

    $time = Time::parse('March 10, 2017', 'America/Chicago');

    $diff = $time->difference(Time::now());
    $diff = $time->difference(new DateTime('July 4, 1975', 'America/Chicago');
    $diff = $time->difference('July 4, 1975 13:32:05', 'America/Chicago');

有了 TimeDifference 实例后，您可以使用多种方法来查找有关两个 Time 间的信息。如果比较时间在待比较时间之前，则返回值为负数；反之，
如果比较时间在带比较时间之后，则返回的值为正数： ::

    $current = Time::parse('March 10, 2017', 'America/Chicago');
    $test    = Time::parse('March 10, 2010', 'America/Chicago');

    $diff = $current->difference($test);

    echo $diff->getYears();     // -7
    echo $diff->getMonths();    // -84
    echo $diff->getWeeks();     // -365
    echo $diff->getDays();      // -2557
    echo $diff->getHours();     // -61368
    echo $diff->getMinutes();   // -3682080
    echo $diff->getSeconds();   // -220924800

你可以用 **getX()** 方法，也可以像使用属性一样访问计算值： ::

    echo $diff->years;     // -7
    echo $diff->months;    // -84
    echo $diff->weeks;     // -365
    echo $diff->days;      // -2557
    echo $diff->hours;     // -61368
    echo $diff->minutes;   // -3682080
    echo $diff->seconds;   // -220924800

humanize()
----------

与 Time 的 humanize() 方法非常相似，此方法返回一个字符串，该字符串以易于理解的格式显示时间之间的时差。
它可以创建像“3 小时前”、“1 个月内”这样的的字符串。它们之间最大的区别在于最近日期的处理方式： ::

    // Assume current time is: March 10, 2017 (America/Chicago)
    // 假设现在时间是： March 10, 2017 (America/Chicago)
    $time = Time::parse('March 9, 2016 12:00:00', 'America/Chicago');

    echo $time->humanize();     // 1 year ago

通过以下方式确定显示的确切时间：

=============================== =================================
时间差异                         结果
=============================== =================================
$time > 1 year && < 2 years      in 1 year / 1 year ago
$time > 1 month && < 1 year      in 6 months / 6 months ago
$time > 7 days && < 1 month      in 3 weeks / 3 weeks ago
$time > today && < 7 days        in 4 days / 4 days ago
$time > 1 hour && < 1 day        in 8 hours / 8 hours ago
$time > 1 minute && < 1 hour     in 35 minutes / 35 minutes ago
$time < 1 minute                 Now
=============================== =================================

返回的结果的语言被语言文件 Time.php 所控制。
