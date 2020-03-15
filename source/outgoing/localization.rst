############
本地化
############

.. contents::
    :local:
    :depth: 2

********************
处理不同地域
********************

CodeIgniter 提供了一系列帮助你处理多语言环境下将应用本土化的工具。尽管一个应用完全地本土化是一个复杂的问题，在你的应用中将一些字符串根据不同的语言进行替换，是相当简单的。

语言字符串存储于 **app/Language** 目录下，其下的每个子目录都代表着一种所支持的语言::

    /app
        /Language
            /en
                app.php
            /fr
                app.php

.. important:: 地区的识别仅对于使用了 IncomingRequest 类的基于 web 的请求起效，命令行请求无法使用这些功能。

配置地区
======================

每个站点都拥有默认的语言/地区属性，可以通过 **Config/App.php** 进行设置::

    public $defaultLocale = 'en';

该变量的值，可以是任何字符串值，用于你的应用程序处理文本字符串和其他格式用。
我们推荐使用 `BCP 47 <http://www.rfc-editor.org/rfc/bcp/bcp47.txt>`_ 类型的语言代号。该说明中，语言编码是例如用于美国英语的 en-US 或者是用于法国法语的 fr-FR 的格式。
或者也可以参照 `W3C's site <https://www.w3.org/International/articles/language-tags/>`_ 以获取可读性更高的说明。

如果不能找到绝对匹配的语言代码时，该系统将足够灵活地使用更为泛化的语言代码。
如果地区代码被设为 **en-US** ，而只有 **en** 语言的语言文件，那么因为没有更为精确地匹配 **en-US** 的语言，我们就会使用这些语言文件。
但是如果有一个语言文件目录 **app/Language/en-US** 存在的话，该目录里的语言文件就会被首先使用。

地区识别
================

我们有两种方式用于在请求中识别正确的地区。第一种方式是"设后即忘"的方式，并会自动执行 :doc:`内容协商 </incoming/content_negotiation>` 以决定使用正确的地区。
第二种方式使得你可以在路由中给定一个特定的分段并用于设置地区。

内容协商
-------------------

你可以通过在 ``Config/App`` 中设置两个额外的参数来自动开启内容协商。
第一个参数用于告诉 ``Request`` 类我们需要开启内容协商，因此只要将其设为 true 即可::

    public $negotiateLocale = true;

当该参数启用时，系统会自动根据你在 ``$suppoertLocales`` 中定义的语言数组来协商使用正确的语言。
如果在你提供的语言和所请求的语言中中匹配不到的话，该数组的第一个成员就会被使用。在下例中，在不匹配时， **en** 地区就会被使用::

    public $supportedLocales = ['en', 'es', 'fr-FR'];

在路由中
---------

The second method uses a custom placeholder to detect the desired locale and set it on the Request. The
placeholder ``{locale}`` can be placed as a segment in your route. If present, the contents of the matching
segment will be your locale::

    $routes->get('{locale}/books', 'App\Books::index');

In this example, if the user tried to visit ``http://example.com/fr/books``, then the locale would be
set to ``fr``, assuming it was configured as a valid locale.

.. note:: If the value doesn't match a valid locale as defined in the App configuration file, the default
    locale will be used in it's place.

获取当前地区
=============================

The current locale can always be retrieved from the IncomingRequest object, through the ``getLocale()`` method.
If your controller is extending ``CodeIgniter\Controller``, this will be available through ``$this->request``::

    <?php namespace App\Controllers;

    class UserController extends \CodeIgniter\Controller
    {
        public function index()
        {
            $locale = $this->request->getLocale();
        }
    }

Alternatively, you can use the :doc:`Services class </concepts/services>` to retrieve the current request::

    $locale = service('request')->getLocale();

*********************
Language Localization
*********************

创建语言文件
=======================

Languages do not have any specific naming convention that are required. The file should be named logically to
describe the type of content it holds. For example, let's say you want to create a file containing error messages.
You might name it simply: **Errors.php**.

Within the file, you would return an array, where each element in the array has a language key and the string to return::

        'language_key' => 'The actual message to be shown.'

.. note:: It's good practice to use a common prefix for all messages in a given file to avoid collisions with
    similarly named items in other files. For example, if you are creating error messages you might prefix them
    with error\_

::

    return [
        'errorEmailMissing'    => 'You must submit an email address',
        'errorURLMissing'      => 'You must submit a URL',
        'errorUsernameMissing' => 'You must submit a username',
    ];

基本用途
===========

You can use the ``lang()`` helper function to retrieve text from any of the language files, by passing the
filename and the language key as the first parameter, separated by a period (.). For example, to load the
``errorEmailMissing`` string from the ``Errors`` language file, you would do the following::

    echo lang('Errors.errorEmailMissing');

If the requested language key doesn't exist in the file for the current locale, the string will be passed
back, unchanged. In this example, it would return 'Errors.errorEmailMissing' if it didn't exist.

参数替换
--------------------

.. note:: The following functions all require the `intl <https://www.php.net/manual/en/book.intl.php>`_ extension to
    be loaded on your system in order to work. If the extension is not loaded, no replacement will be attempted.
    A great overview can be found over at `Sitepoint <https://www.sitepoint.com/localization-demystified-understanding-php-intl/>`_.

You can pass an array of values to replace placeholders in the language string as the second parameter to the
``lang()`` function. This allows for very simple number translations and formatting::

    // The language file, Tests.php:
    return [
        "apples"      => "I have {0, number} apples.",
        "men"         => "I have {1, number} men out-performed the remaining {0, number}",
        "namedApples" => "I have {number_apples, number, integer} apples.",
    ];

    // Displays "I have 3 apples."
    echo lang('Tests.apples', [ 3 ]);

The first item in the placeholder corresponds to the index of the item in the array, if it's numerical::

    // Displays "The top 23 men out-performed the remaining 20"
    echo lang('Tests.men', [20, 23]);

You can also use named keys to make it easier to keep things straight, if you'd like::

    // Displays "I have 3 apples."
    echo lang("Tests.namedApples", ['number_apples' => 3]);

Obviously, you can do more than just number replacement. According to the
`official ICU docs <https://unicode-org.github.io/icu-docs/apidoc/released/icu4c/classMessageFormat.html#details>`_ for the underlying
library, the following types of data can be replaced:

* numbers - integer, currency, percent
* dates - short, medium, long, full
* time - short, medium, long, full
* spellout - spells out numbers (i.e. 34 becomes thirty-four)
* ordinal
* duration

Here are a few examples::

    // The language file, Tests.php
    return [
        'shortTime'  => 'The time is now {0, time, short}.',
        'mediumTime' => 'The time is now {0, time, medium}.',
        'longTime'   => 'The time is now {0, time, long}.',
        'fullTime'   => 'The time is now {0, time, full}.',
        'shortDate'  => 'The date is now {0, date, short}.',
        'mediumDate' => 'The date is now {0, date, medium}.',
        'longDate'   => 'The date is now {0, date, long}.',
        'fullDate'   => 'The date is now {0, date, full}.',
        'spelledOut' => '34 is {0, spellout}',
        'ordinal'    => 'The ordinal is {0, ordinal}',
        'duration'   => 'It has been {0, duration}',
    ];

    // Displays "The time is now 11:18 PM"
    echo lang('Tests.shortTime', [time()]);
    // Displays "The time is now 11:18:50 PM"
    echo lang('Tests.mediumTime', [time()]);
    // Displays "The time is now 11:19:09 PM CDT"
    echo lang('Tests.longTime', [time()]);
    // Displays "The time is now 11:19:26 PM Central Daylight Time"
    echo lang('Tests.fullTime', [time()]);

    // Displays "The date is now 8/14/16"
    echo lang('Tests.shortDate', [time()]);
    // Displays "The date is now Aug 14, 2016"
    echo lang('Tests.mediumDate', [time()]);
    // Displays "The date is now August 14, 2016"
    echo lang('Tests.longDate', [time()]);
    // Displays "The date is now Sunday, August 14, 2016"
    echo lang('Tests.fullDate', [time()]);

    // Displays "34 is thirty-four"
    echo lang('Tests.spelledOut', [34]);

    // Displays "It has been 408,676:24:35"
    echo lang('Tests.ordinal', [time()]);

You should be sure to read up on the MessageFormatter class and the underlying ICU formatting to get a better
idea on what capabilities it has, like performing the conditional replacement, pluralization, and more. Both of the links provided
earlier will give you an excellent idea as to the options available.

确定地区
-----------------

To specify a different locale to be used when replacing parameters, you can pass the locale in as the
third parameter to the ``lang()`` method.
::

    // Displays "The time is now 23:21:28 GMT-5"
    echo lang('Test.longTime', [time()], 'ru-RU');

    // Displays "£7.41"
    echo lang('{price, number, currency}', ['price' => 7.41], 'en-GB');
    // Displays "$7.41"
    echo lang('{price, number, currency}', ['price' => 7.41], 'en-US');

嵌套数组
-------------

Language files also allow nested arrays to make working with lists, etc... easier.
::

    // Language/en/Fruit.php

    return [
        'list' => [
            'Apples',
            'Bananas',
            'Grapes',
            'Lemons',
            'Oranges',
            'Strawberries'
        ]
    ];

    // Displays "Apples, Bananas, Grapes, Lemons, Oranges, Strawberries"
    echo implode(', ', lang('Fruit.list'));

Language Fallback
=================

If you have a set of messages for a given locale, for instance
``Language/en/app.php``, you can add language variants for that locale,
each in its own folder, for instance ``Language/en-US/app.php``.

You only need to provide values for those messages that would be
localized differently for that locale variant. Any missing message
definitions will be automatically pulled from the main locale settings.

It gets better - the localization can fall all the way back to English,
in case new messages are added to the framework and you haven't had
a chance to translate them yet for your locale.

So, if you are using the locale ``fr-CA``, then a localized
message will first be sought in ``Language/fr/CA``, then in
``Language/fr``, and finally in ``Language/en``.

信息翻译
====================

在我们的 `仓库 <https://github.com/codeigniter4/translations>`_ .中，有一份"正式的"翻译集

你可以下载该仓库并复制其中的 ``Language`` 目录到你的 ``app`` 中。因为 ``App`` 命名空间映射到了你的 ``app`` 目录，对应的翻译就会被自动使用。

不过更好的使用方式是在你的项目中使用 ``composer require codeigniter4/translations`` ，因为翻译目录自动映射之后，这样被翻译过的信息就会自动被使用。
