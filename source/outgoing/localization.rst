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

第二种方法是用一个自定义的通配符来检测所需要的地区，并将其用于当前请求中。在你的路由中，通配符 ``{locale}}`` 可以被替换为一个路由分段。
如果该分段存在的话，所匹配到的路由分段就是你的地区::

    $routes->get('{locale}/books', 'App\Books::index');

在本例中，如果用户尝试访问 ``http://example.com/fr/books`` ，地区就会被设置为 ``fr`` ，并假设这是一个合理的地区参数。

.. note:: 如果该路由分段值匹配不到 App 配置文件中合理的地区值的话，就会用默认的地区来代替。

获取当前地区
=============================

当前地区默认从 IncomingRequest 实例中获取，通过 ``getLocale()`` 方法。
如果你的控制器继承了 ``CodeIgniter\Controller`` ，以上操作也可以通过 ``$this->request`` 来实现::

    <?php namespace App\Controllers;

    class UserController extends \CodeIgniter\Controller
    {
        public function index()
        {
            $locale = $this->request->getLocale();
        }
    }

或者你也可以用 :doc:`服务类 </concepts/services>` 来获取当前的请求::

    $locale = service('request')->getLocale();

*********************
语言本土化
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

你可以使用 ``lang()`` 辅助函数从所有语言文件中获取文本值，通过将文件名和语言键作为第一个参数，以点号(.)分隔。
举例来说，从 ``Errors`` 语言文件中加载 ``errorEmailMissing`` 字符串，你可以如下操作::

    echo lang('Errors.errorEmailMissing');

如果所请求的语言键对于当前的地区来说不存在的话，就会不做修改的返回请求的参数。在本例中，如果 'Errors.errorEmailMissing' 对应的翻译不存在的话，就会直接被返回。

参数替换
--------------------

.. note:: 以下函数需要加载并启用 `intl <https://www.php.net/manual/zh/book.intl.php>`_ 扩展。如果该扩展未加载，则不会进行替换操作。
    可参阅 `Sitepoint <https://www.sitepoint.com/localization-demystified-understanding-php-intl/>`_.

你可以在语言字符串中，通过对 ``lang()`` 函数的第二个参数传递一个值数组来替代通配符中的内容。这一操作对于简单的数字翻译和格式化来说非常方便::

    // 语言文件, Tests.php:
    return [
        "apples"      => "I have {0, number} apples.",
        "men"         => "I have {1, number} men out-performed the remaining {0, number}",
        "namedApples" => "I have {number_apples, number, integer} apples.",
    ];

    // 输出 "I have 3 apples."
    echo lang('Tests.apples', [ 3 ]);

通配符中的第一项对应着数组的索引下标（如果该下标是数字格式的话)::

    // 输出 "The top 23 men out-performed the remaining 20"
    echo lang('Tests.men', [20, 23]);

如果希望的话，你也可以使用命名数组来更为直接地传递参数::

    // 显示 "I have 3 apples."
    echo lang("Tests.namedApples", ['number_apples' => 3]);

显然你可以实现比起数字替换更为高级的功能。根据标准库 `official ICU docs <https://unicode-org.github.io/icu-docs/apidoc/released/icu4c/classMessageFormat.html#details>`_ 所示，以下类型的数据可被替换:

* numbers - 整数，汇率，百分比
* dates - 短，中，长，完整格式
* time - 短，中，长，完整格式
* spellout - 大写数字 (例如 34 变成 thirty-four)
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

你需要阅读 MessageFormatter 类以及 ICU 编码格式以充分使用这一功能的特性，例如执行条件替换，多元素替换等。以上两者的链接都在上文中有所提及，希望可以可以帮助你充分利用这一特性。

确定地区
-----------------

为了在替换参数时显式调用一个不同的地区，你可以通过将地区作为 ``lang()`` 方法的第三个参数来实现::

    // Displays "The time is now 23:21:28 GMT-5"
    echo lang('Test.longTime', [time()], 'ru-RU');

    // Displays "£7.41"
    echo lang('{price, number, currency}', ['price' => 7.41], 'en-GB');
    // Displays "$7.41"
    echo lang('{price, number, currency}', ['price' => 7.41], 'en-US');

嵌套数组
-------------

语言文件可以接受嵌套数组作为参数，以更为方便地处理列表类型的数据等::

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

语言回滚
=================

如果对于一个给定的地区，你有多种语言文件类型，例如对于 ``Language/en.php`` ，你可以通过为这一地区增加一个语言变量，例如 ``Language/en-US/app.php``

你唯一需要为这些信息提供的就是它们在不同地区里的值。如果对应的信息翻译不存在的话，就会从主地区设置中获取并赋值。

本土化功能可以将所有翻译信息回滚为英语，以防止在新的信息增加到框架中时，你没办法为所在地区实现翻译。

因此，如果你在使用地区 ``fr-CA`` ，那么翻译信息会首先从 ``Language/fr/CA`` 中搜索，然后在 ``Language/fr`` ，最后在 ``Language/en`` 中。

信息翻译
====================

在我们的 `仓库 <https://github.com/codeigniter4/translations>`_ .中，有一份"正式的"翻译集

你可以下载该仓库并复制其中的 ``Language`` 目录到你的 ``app`` 中。因为 ``App`` 命名空间映射到了你的 ``app`` 目录，对应的翻译就会被自动使用。

不过更好的使用方式是在你的项目中使用 ``composer require codeigniter4/translations`` ，因为翻译目录自动映射之后，这样被翻译过的信息就会自动被使用。
