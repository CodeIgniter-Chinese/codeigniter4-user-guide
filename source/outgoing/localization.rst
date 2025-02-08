############
本地化
############

.. contents::
    :local:
    :depth: 3

********************
处理区域设置
********************

CodeIgniter 提供了多种工具来帮助你对应用程序进行不同语言的本地化。虽然完整的应用程序本地化是一个复杂的主题，但替换应用程序中不同支持语言的字符串非常简单。

配置区域设置
======================

.. _setting-the-default-locale:

设置默认区域设置
--------------------------

每个站点都有一个默认的操作语言/区域设置。这可以在 **app/Config/App.php** 中设置：

.. literalinclude:: localization/001.php

该值可以是应用程序用于管理文本字符串和其他格式的任何字符串。建议使用 `BCP 47 <http://www.rfc-editor.org/rfc/bcp/bcp47.txt>`_ 语言代码。这会生成像 en-US（美式英语）或 fr-FR（法语/法国）这样的语言代码。在 `W3C 的网站 <https://www.w3.org/International/articles/language-tags/>`_ 上可以找到更易读的介绍。

如果找不到完全匹配项，系统会智能回退到更通用的语言代码。如果区域设置代码设置为 ``en-US``，而我们只设置了 ``en`` 的语言文件，则将使用这些文件，因为更具体的 ``en-US`` 不存在。但是，如果 **app/Language/en-US** 目录中存在语言目录，则将优先使用该目录。

区域检测
================

.. important:: 区域检测仅适用于使用 IncomingRequest 类的基于 Web 的请求。命令行请求将不具备这些功能。

有两种支持的方法可以在请求期间检测正确的区域设置。

1. `内容协商`_：第一种是 "设置即忘记" 方法，将自动执行 :doc:`内容协商 </incoming/content_negotiation>` 以确定要使用的正确区域设置。
2. `在路由中`_：第二种方法允许你在路由中指定一个段来设置区域设置。

如果需要直接设置区域设置，请参阅 `设置当前区域设置`_。

自 v4.4.0 起，添加了 ``IncomingRequest::setValidLocales()`` 来设置（和重置）从 ``Config\App::$supportedLocales`` 设置的有效区域。

内容协商
-------------------

你可以通过 **app/Config/App.php** 中的两个附加设置来配置自动内容协商。第一个值告诉 Request 类我们确实希望协商区域设置，因此只需将其设置为 true：

.. literalinclude:: localization/002.php

启用此功能后，系统将根据你在 ``$supportLocales`` 中定义的区域设置数组自动协商正确的语言。如果在你支持的语言与请求的语言之间找不到匹配项，则将使用 ``$supportedLocales`` 中的第一个项。在以下示例中，如果找不到匹配项，将使用 ``en`` 区域设置：

.. literalinclude:: localization/003.php

.. _localization-in-routes:

在路由中
---------

第二种方法使用自定义占位符来检测所需区域设置并在请求中设置。占位符 ``{locale}`` 可以作为段放置在路由中。如果存在，匹配段的内容将是你的区域设置：

.. literalinclude:: localization/004.php
    :lines: 2-

在此示例中，如果用户尝试访问 **http://example.com/fr/books**，则区域设置将设置为 ``fr``，前提是它被配置为有效区域设置。

如果该值与 **app/Config/App.php** 中 ``$supportedLocales`` 定义的有效区域设置不匹配，则将使用默认区域设置，除非你设置为仅使用 App 配置文件中定义的受支持区域设置：

.. literalinclude:: localization/018.php
    :lines: 2-

.. note:: 自 v4.3.0 起可以使用 ``useSupportedLocalesOnly()`` 方法。

设置当前区域设置
==========================

IncomingRequest 区域设置
------------------------

如果要直接设置区域设置，可以使用 :doc:`../incoming/incomingrequest` 中的 ``setLocale()`` 方法：

.. literalinclude:: localization/020.php
    :lines: 2-

在设置区域设置之前，必须设置有效区域。因为任何尝试设置无效区域设置的操作都将导致设置 :ref:`默认区域设置 <setting-the-default-locale>`。

默认情况下，有效区域在 **app/Config/App.php** 的 ``Config\App::$supportedLocales`` 中定义：

.. literalinclude:: localization/003.php

.. note:: 自 v4.4.0 起，添加了 ``IncomingRequest::setValidLocales()`` 来设置（和重置）有效区域。如果要动态更改有效区域，请使用此方法。

语言区域设置
---------------

:php:func:`lang()` 函数中使用的 ``Language`` 类也具有当前区域设置。该设置在实例化期间设置为 ``IncommingRequest`` 区域设置。

如果要在实例化语言类后更改区域设置，请使用 ``Language::setLocale()`` 方法。

.. literalinclude:: localization/021.php
    :lines: 2-

获取当前区域设置
=============================

始终可以通过 ``getLocale()`` 方法从 IncomingRequest 对象获取当前区域设置。如果你的控制器继承自 ``CodeIgniter\Controller``，则可以通过 ``$this->request`` 获取：

.. literalinclude:: localization/005.php

或者，你可以使用 :doc:`Services 类 </concepts/services>` 来获取当前请求：

.. literalinclude:: localization/006.php
    :lines: 2-

.. _language-localization:

*********************
语言本地化
*********************

创建语言文件
=======================

语言字符串存储在 **app/Language** 目录中，每个支持的语言（区域设置）都有一个子目录::

    app/
        Language/
            en/
                App.php
            fr/
                App.php

.. note:: 语言文件没有命名空间。

语言没有必须遵循的特定命名约定。文件应逻辑命名以描述其包含的内容类型。例如，假设你要创建一个包含错误消息的文件。你可以简单地将其命名为：**Errors.php**。

在文件中，你将返回一个数组，其中数组中的每个元素都有一个语言键，并可以返回字符串：

.. literalinclude:: localization/007.php

.. note:: 不能在语言键的开头和结尾使用点（``.``）。

它还支持嵌套定义：

.. literalinclude:: localization/008.php

.. literalinclude:: localization/009.php

基本用法
===========

你可以使用 :php:func:`lang()` 辅助函数通过传递文件名和语言键作为第一个参数（用句点 ``.`` 分隔）从任何语言文件中检索文本。

例如，要从 **Errors.php** 语言文件加载 ``errorEmailMissing`` 字符串，可以执行以下操作：

.. literalinclude:: localization/010.php
    :lines: 2-

对于嵌套定义，可以执行以下操作：

.. literalinclude:: localization/011.php
    :lines: 2-

如果请求的语言键在当前区域设置的文件中不存在（在 `语言回退`_ 之后），将原样返回字符串。在此示例中，如果不存在，它将返回 ``Errors.errorEmailMissing`` 或 ``Errors.nested.error.message``。

替换参数
--------------------

.. note:: 以下函数都需要在系统上加载 `intl <https://www.php.net/manual/zh/book.intl.php>`_ 扩展才能工作。如果未加载扩展，将不会尝试替换。在 `Sitepoint <https://www.sitepoint.com/localization-demystified-understanding-php-intl/>`_ 上可以找到一个很好的概述。

你可以将值的数组作为第二个参数传递给 ``lang()`` 函数，以替换语言字符串中的占位符。这允许进行非常简单的数字翻译和格式化：

.. literalinclude:: localization/012.php

占位符中的第一个项对应于数组中的项索引（如果是数字）：

.. literalinclude:: localization/013.php
    :lines: 2-

你也可以使用命名键以便更清晰：

.. literalinclude:: localization/014.php
    :lines: 2-

显然，你可以做的不仅仅是数字替换。根据底层库的 `官方 ICU 文档 <https://unicode-org.github.io/icu-docs/apidoc/released/icu4c/classMessageFormat.html#details>`_，可以替换以下类型的数据：

* 数字 - 整数、货币、百分比
* 日期 - 短、中、长、完整
* 时间 - 短、中、长、完整
* 拼写 - 拼出数字（例如，34 变为三十四）
* 序数
* 持续时间

以下是一些示例：

.. literalinclude:: localization/015.php

你应该阅读 MessageFormatter 类和底层 ICU 格式化的文档，以更好地了解其功能，例如执行条件替换、复数化等。前面提供的两个链接将让你很好地了解可用选项。

指定区域设置
-----------------

要指定用于替换参数的不同区域设置，可以将区域设置作为第三个参数传递给 :php:func:`lang()` 函数。

.. literalinclude:: localization/016.php

如果要更改当前区域设置，请参阅 `语言区域设置`_。

嵌套数组
-------------

语言文件还允许使用嵌套数组以便更轻松地处理列表等。

.. literalinclude:: localization/017.php

语言回退
=================

如果你为某个区域设置（例如 **Language/en/App.php**）提供了一组消息，则可以为该区域设置添加语言变体，每个变体位于自己的文件夹中，例如 **Language/en-US/App.php**。

你只需为该区域变体本地化不同的消息提供值。任何缺失的消息定义将自动从主区域设置中提取。

更好的是，本地化可以一直回退到英语（**en**），以防框架添加了新消息而你尚未有机会为你的区域设置翻译它们。

因此，如果你使用区域设置 ``fr-CA``，则将首先在 **Language/fr-CA** 目录中查找本地化消息，然后在 **Language/fr** 目录中查找，最后在 **Language/en** 目录中查找。

系统消息翻译
===========================

我们在 `自己的仓库 <https://github.com/codeigniter4/translations>`_ 中提供了一套 "官方" 系统消息翻译。

你可以下载该仓库，并将其 **Language** 文件夹复制到你的 **app** 文件夹中。由于 ``App`` 命名空间映射到你的 **app** 文件夹，因此合并的翻译将自动被识别。

或者，更好的做法是在项目中运行以下命令：

.. code-block:: console

    composer require codeigniter4/translations

由于翻译文件夹被正确映射，翻译后的消息将自动被识别。

覆盖系统消息翻译
======================================

框架提供 `系统消息翻译`_，你安装的包也可能提供消息翻译。

如果要覆盖某些语言消息，请在 **app/Language** 目录中创建语言文件。然后，在文件中仅返回要覆盖的数组。

.. _generating-translation-files-via-command:

通过命令生成翻译文件
========================================

.. versionadded:: 4.5.0

你可以自动生成和更新 **app** 文件夹中的翻译文件。该命令将搜索 ``lang()`` 函数的使用，通过定义 ``Config\App`` 中的 ``defaultLocale`` 区域设置来合并 **app/Language** 中的当前翻译键。操作完成后，你需要自行翻译语言键。该命令通常能够识别嵌套键 ``File.array.nested.text``。先前保存的键不会更改。

.. code-block:: console

    php spark lang:find

.. literalinclude:: localization/019.php

.. note:: 扫描文件夹时，将跳过 **app/Language**。

生成的翻译文件很可能不符合你的编码标准。建议进行格式化。例如，如果安装了 ``php-cs-fixer``，则运行 ``vendor/bin/php-cs-fixer fix ./app/Language``。

在更新之前，可以预览命令找到的翻译：

.. code-block:: console

    php spark lang:find --verbose --show-new

``--verbose`` 的详细输出还会显示无效键的列表。例如：

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

为了更精确地搜索，请指定要扫描的区域设置或目录。

.. code-block:: console

    php spark lang:find --dir Controllers/Translation --locale en --show-new

可以通过运行命令获取详细信息：

.. code-block:: console

    php spark lang:find --help

.. _sync-translations-command:

通过命令同步翻译文件
---------------------------------------------

.. versionadded:: 4.6.0

当你完成当前语言的翻译后，可能需要为另一种语言创建文件。你可以使用 spark ``lang:find`` 命令来帮助完成此操作。但是，它可能无法检测到所有翻译，特别是那些具有动态设置参数的翻译，例如 ``lang('App.status.' . $key, ['payload' => 'John'], 'en')``。

为了确保不遗漏任何翻译，最好复制已完成的语言文件并手动翻译它们。这种方法可以保留命令可能遗漏的任何唯一键。

只需执行：

.. code-block:: console

    // 指定新/更新翻译的区域设置
    php spark lang:sync --target ru

    // 或设置原始区域设置
    php spark lang:sync --locale en --target ru

结果你将获得包含翻译键的文件。如果目标区域设置中存在重复键，则会保存这些键。

.. warning:: 新翻译中不匹配的键将被删除！
