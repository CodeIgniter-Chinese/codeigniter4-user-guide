############
本地化
############

.. contents::
    :local:
    :depth: 3

********************
使用语言环境
********************

CodeIgniter 提供了多种工具，帮助开发者将应用本地化为不同语言。虽然应用的完整本地化是一个复杂
的主题，但在应用中切换受支持的语言字符串却非常简单。

配置语言环境
======================

.. _setting-the-default-locale:

设置默认语言环境
--------------------------

每个站点都会有一个默认的语言环境。可在 **app/Config/App.php** 中设置：

.. literalinclude:: localization/001.php

此值可设为应用管理文本及格式所用的任意字符串。
建议使用 `BCP 47 <http://www.rfc-editor.org/rfc/bcp/bcp47.txt>`_ 语言代码，
例如美式英语使用 en-US，法语（法国）使用 fr-FR。
访问 `W3C 网站 <https://www.w3.org/International/articles/language-tags/>`_ 可查看更易读的相关介绍。

若找不到精确匹配，系统会自动回退到更通用的语言代码。
例如，若语言环境设为 ``en-US`` 但未配置专属的语言文件，系统将退而使用 ``en`` 目录下的配置。
反之，若 **app/Language/en-US** 目录存在，则优先使用该目录。

语言环境检测
================

.. important:: 语言环境检测仅适用于使用 IncomingRequest 类的 Web 请求。
    命令行请求不支持这些功能。

请求期间检测正确的语言环境支持两种方法。

1. `内容协商`_：第一种是"一次设置，无需再管"的方法，会自动执行 :doc:`内容协商 </incoming/content_negotiation>` 来确定正确的语言环境。
2. `在路由中`_：第二种方法允许在路由中指定一个用于设置语言环境的段。

如需直接设置语言环境，请参阅 `设置当前语言环境`_。

自 v4.4.0 起，新增 ``IncomingRequest::setValidLocales()`` 方法，用于
设置（和重置）来自 ``Config\App::$supportedLocales`` 配置的有效语言环境。

内容协商
-------------------

可在 **app/Config/App.php** 中设置两个额外的配置项，使内容协商自动进行。
第一个值告诉 Request 类需要协商语言环境，因此将其设置为 true：

.. literalinclude:: localization/002.php

启用后，系统会根据你在 ``$supportLocales`` 中定义的语言环境数组自动协商正确的语言。如果
支持的语言与请求的语言之间找不到匹配项，将使用 ``$supportedLocales`` 中的第一项。在以下
示例中，如果找不到匹配项，将使用 ``en`` 语言环境：

.. literalinclude:: localization/003.php

.. _localization-in-routes:

在路由中
---------

第二种方法使用自定义占位符来检测所需的语言环境并在 Request 上设置它。
占位符 ``{locale}`` 可作为路由中的一个段放置。如果存在，匹配段的内容
即为当前语言环境：

.. literalinclude:: localization/004.php
    :lines: 2-

在此示例中，如果用户尝试访问 **http://example.com/fr/books**，则语言环境会
设置为 ``fr``，前提是其已配置为有效语言环境。

若该值与 **app/Config/App.php** 中 ``$supportedLocales`` 定义的有效语言环境不匹配，
则会改用默认语言环境，除非设置为仅使用 App 配置文件中定义的语言环境：

.. literalinclude:: localization/018.php
    :lines: 2-

.. note:: ``useSupportedLocalesOnly()`` 方法自 v4.3.0 起可用。

设置当前语言环境
==========================

IncomingRequest 语言环境
------------------------

如需直接设置语言环境，可使用 :doc:`../incoming/incomingrequest` 中的 ``setLocale()`` 方法：

.. literalinclude:: localization/020.php
    :lines: 2-

设置语言环境前，必须先设置有效语言环境。因为尝试设置
无效语言环境会导致设置为
:ref:`默认语言环境 <setting-the-default-locale>`。

默认情况下，有效语言环境在 **app/Config/App.php** 的 ``Config\App::$supportedLocales`` 中定义：

.. literalinclude:: localization/003.php

.. note:: 自 v4.4.0 起，新增 ``IncomingRequest::setValidLocales()`` 方法，
    用于设置（和重置）有效语言环境。如需动态更改有效语言环境，请使用此方法。

Language 类的语言环境
---------------------

:php:func:`lang()` 函数使用的 ``Language`` 类也包含当前语言环境。
该环境在实例化时设置为 ``IncomingRequest`` 的语言环境。

如需在实例化 Language 类后更改语言环境，请使用
``Language::setLocale()`` 方法。

.. literalinclude:: localization/021.php
    :lines: 2-

获取当前语言环境
=============================

可通过 ``getLocale()`` 方法从 IncomingRequest 对象获取当前语言环境。
如果控制器继承了 ``CodeIgniter\Controller``，可通过 ``$this->request`` 获取：

.. literalinclude:: localization/005.php

此外，也可使用 :doc:`Services 类 </concepts/services>` 获取当前请求：

.. literalinclude:: localization/006.php
    :lines: 2-

.. _language-localization:

*********************
语言本地化
*********************

创建语言文件
=======================

语言字符串存储在 **app/Language** 目录中，每种支持的语言（语言环境）各有一个子目录::

    app/
        Language/
            en/
                App.php
            fr/
                App.php

.. note:: 语言文件没有命名空间。

语言文件没有特定的命名规范。文件应按逻辑命名，以描述其包含的内容类型。例如，
假设你想创建一个包含错误消息的文件，可以简单地命名为：**Errors.php**。

在文件中，返回一个数组，数组中的每个元素对应一个语言键和要返回的字符串：

.. literalinclude:: localization/007.php

.. note:: 语言键的开头和结尾不能包含点号（``.``）。

也支持嵌套定义：

.. literalinclude:: localization/008.php

.. literalinclude:: localization/009.php

基本用法
===========

可使用 :php:func:`lang()` 辅助函数从任意语言文件中检索文本，将文件名和语言键作为
第一个参数传入，以点号（``.``）分隔。

例如，要从 **Errors.php** 语言文件中加载 ``errorEmailMissing`` 字符串，
可以执行以下操作：

.. literalinclude:: localization/010.php
    :lines: 2-

对于嵌套定义，可以执行以下操作：

.. literalinclude:: localization/011.php
    :lines: 2-

如果当前语言环境的文件中不存在请求的语言键（在 `语言回退`_ 之后），将原样返回该字符串。
在此示例中，如果不存在，将返回 ``Errors.errorEmailMissing`` 或 ``Errors.nested.error.message``。

替换参数
--------------------

.. note:: 以下函数均需要在系统上加载 `intl <https://www.php.net/manual/zh/book.intl.php>`_ 扩展
    才能正常工作。如果未加载该扩展，将不执行任何替换。
    关于这个扩展的全面介绍可在 `Sitepoint <https://www.sitepoint.com/localization-demystified-understanding-php-intl/>`_ 找到。

将数组作为第二个参数传递给 ``lang()`` 函数，即可替换语言字符串中的占位符。
由此可轻松实现数字替换与格式化：

.. literalinclude:: localization/012.php

占位符中的第一项对应数组中的索引（如果是数字索引）：

.. literalinclude:: localization/013.php
    :lines: 2-

也可以使用命名键来使结构更清晰：

.. literalinclude:: localization/014.php
    :lines: 2-

显然，不只是能做数字替换。根据底层库的
`官方 ICU 文档 <https://unicode-org.github.io/icu-docs/apidoc/released/icu4c/classMessageFormat.html#details>`_，
可以替换以下类型的数据：

* 数字 — 整数、货币、百分比
* 日期 — short, medium, long, full
* 时间 — short, medium, long, full
* spellout — 拼写数字（如 34 变为 thirty-four）
* 序数
* 持续时间

以下是一些示例：

.. literalinclude:: localization/015.php

建议阅读 MessageFormatter 类和底层 ICU 格式化的相关文档，以更好地了解其功能，
如执行条件替换、复数形式等。前面提供的两个链接都会让你清楚地了解可用选项。

指定语言环境
-----------------

如需在替换参数时使用不同的语言环境，可将语言环境作为
第三个参数传递给 :php:func:`lang()` 函数。

.. literalinclude:: localization/016.php

如需更改当前语言环境，请参阅 `Language 类的语言环境`_。

嵌套数组
-------------

语言文件还支持嵌套数组，使处理列表等操作更加容易。

.. literalinclude:: localization/017.php

语言回退
=================

如果你为某个语言环境设置了一组消息，例如
**Language/en/App.php**，可以为该语言环境添加变体，
每个变体各自位于一个文件夹中，例如 **Language/en-US/App.php**。

只需为该语言环境变体提供不同的消息值即可。任何缺失的消息
定义会自动从主语言环境设置中获取。

不仅如此 — 本地化甚至可以一直回退到英文（**en**），
以防框架新增了消息而你还来不及翻译。

因此，如果使用 ``fr-CA`` 语言环境，本地化消息将首先在 **Language/fr-CA** 目录中查找，
然后在 **Language/fr** 目录中查找，最后在 **Language/en** 目录中查找。

系统消息翻译
===========================

我们有一套"官方"系统消息翻译，位于
`独立仓库 <https://github.com/codeigniter4/translations>`_ 中。

可以下载该仓库，将其中的 **Language** 文件夹
复制到 **app** 文件夹中。引入的翻译会自动
生效，因为 ``App`` 命名空间映射到了 **app** 文件夹。

另一种更好的做法是在项目中运行以下命令：

.. code-block:: console

    composer require codeigniter4/translations

翻译消息会自动生效，
因为翻译文件夹会被正确映射。

覆盖系统消息翻译
======================================

框架提供了 `系统消息翻译`_，
已安装的包也可能提供了消息翻译。

如需覆盖某些语言消息，在 **app/Language** 目录中创建语言文件。
然后，在文件中仅返回想要覆盖的数组。

.. _generating-translation-files-via-command:

通过命令生成翻译文件
========================================

.. versionadded:: 4.5.0

可以自动生成和更新 **app** 文件夹中的翻译文件。该命令会搜索 ``lang()`` 函数的使用，
结合 **app/Language** 中当前的翻译键，并定义来自 ``Config\App`` 的语言环境 ``defaultLocale``。
操作完成后，需要自行翻译语言键。
该命令能够正常识别嵌套键，如 ``File.array.nested.text``。
之前保存的键不会改变。

.. code-block:: console

    php spark lang:find

.. literalinclude:: localization/019.php

.. note:: 命令扫描文件夹时，会跳过 **app/Language**。

命令生成的语言文件可能不符合编码标准。
建议对其进行格式化。例如，如果已安装 ``php-cs-fixer``，可运行 ``vendor/bin/php-cs-fixer fix ./app/Language``。

更新前，可以预览命令找到的翻译：

.. code-block:: console

    php spark lang:find --verbose --show-new

``--verbose`` 的详细输出还会显示无效键列表。例如：

.. code-block:: console

    ...

    Files found: 10
    New translates found: 30
    Bad translates found: 5
    +------------------------+---------------------------------+
    | Bad Key                | Filepath                        |
    +------------------------+---------------------------------+
    | ..invalid_nested_key.. | app/Controllers/Translation.php |
    | .invalid_key           | app/Controllers/Translation.php |
    | TranslationBad         | app/Controllers/Translation.php |
    | TranslationBad.        | app/Controllers/Translation.php |
    | TranslationBad...      | app/Controllers/Translation.php |
    +------------------------+---------------------------------+

    All operations done!

如需更精确的搜索，可以指定要扫描的语言环境或目录。

.. code-block:: console

    php spark lang:find --dir Controllers/Translation --locale en --show-new

运行以下命令可获取详细信息：

.. code-block:: console

    php spark lang:find --help

.. _sync-translations-command:

通过命令同步翻译文件
---------------------------------------------

.. versionadded:: 4.6.0

在完成当前语言的翻译后，可能需要为另一种语言创建文件。可以使用 spark ``lang:find`` 命令来辅助完成。
但是，它可能无法检测所有翻译，特别是那些带有动态设置参数的翻译，如 ``lang('App.status.' . $key, ['payload' => 'John'], 'en')``。

为确保不遗漏翻译，最好的做法是复制已完成的语言文件并手动翻译。这种方法可以保留命令可能忽略的唯一键。

只需执行：

.. code-block:: console

    // 指定新/更新翻译的语言环境
    php spark lang:sync --target ru

    // 或设置原始语言环境
    php spark lang:sync --locale en --target ru

结果将获得带有翻译键的文件。
如果目标语言环境中存在重复键，这些键会被保留。

.. warning:: 不匹配的键在新翻译中会被删除！
