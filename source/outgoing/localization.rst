############
本地化
############

.. contents::
    :local:
    :depth: 3

********************
使用语言环境
********************

CodeIgniter 提供了几个工具来帮助你为不同的语言本地化应用程序。尽管完整地本地化一个应用程序是个复杂的题目,但在应用程序中用不同的支持语言交换字符串是非常简单的。

语言字符串存储在 **app/Language** 目录中,每个支持的语言都有对应的子目录::

    app/
        Language/
            en/
                App.php
            fr/
                App.php

.. important:: 仅基于网络的请求才会启用本地化检测,需要使用 IncomingRequest 类。
    命令行下的请求不支持这些特性。

配置语言环境
======================

.. _setting-the-default-locale:

设置默认语言环境
--------------------------

每个站点都会有一个它们运作的默认语言环境/区域设置。这可以在 **app/Config/App.php** 中设置:

.. literalinclude:: localization/001.php

这个值可以是你的应用程序用来管理文本字符串和其他格式的任意字符串。建议使用 `BCP 47 <http://www.rfc-editor.org/rfc/bcp/bcp47.txt>`_ 语言代码。这会产生像 en-US 表示美式英语,或者 fr-FR 表示法语/法国这样的语言代码。`W3C 网站 <https://www.w3.org/International/articles/language-tags/>`_ 上有更容易理解的介绍。

如果无法找到完全匹配的语言环境,系统足够智能到退回到更通用的语言代码。如果语言环境代码被设置为 ``en-US``,但我们只设置了 ``en`` 的语言文件,那么就会使用 ``en``,因为没有更具体的 ``en-US`` 存在。然而,如果 **app/Language/en-US** 目录存在,那么它将被首先使用。

语言环境检测
================

在请求期间支持两种方法来检测正确的语言环境。第一种方法是一个“设置完就忘记”的方式,将自动为你执行 :doc:`内容协商 </incoming/content_negotiation>` 以确定使用的正确语言环境。第二种方法允许你在路由中指定一个片段来设置语言环境。

如果你需要直接设置语言环境,请参见 `设置当前语言环境`_ 。

自 v4.4.0 起，添加了 ``IncomingRequest::setValidLocales()`` 方法，用于设置（和重置）从 ``Config\App::$supportedLocales`` 设置中设置的有效语言环境。

内容协商
-------------------

你可以通过在 **app/Config/App.php** 中设置两个附加配置来启用内容协商自动执行。第一个值告诉 Request 类我们确实希望协商一个语言环境,所以简单地设置为 true :

.. literalinclude:: localization/002.php

一旦启用,系统将自动根据你定义的语言环境列表 ``$supportLocales`` 协商出正确的语言。如果在你支持的语言和请求的语言之间找不到匹配, ``$supportedLocales`` 中的第一项将被使用。在下面的例子中,如果找不到匹配,将使用 ``en`` 语言环境:

.. literalinclude:: localization/003.php

.. _localization-in-routes:

在路由中
---------

第二种方法使用一个自定义占位符来检测所需的语言环境并在 Request 中设置它。可以将占位符 ``{locale}`` 作为路由中的一个片段。如果存在,匹配片段的内容将是你的语言环境:

.. literalinclude:: localization/004.php

在这个例子中,如果用户试图访问 **http://example.com/fr/books**,那么语言环境将被设置为 ``fr``,假设它已经在 ``$supportedLocales`` 中被配置为有效的语言环境。

如果该值与 ``app/Config/App.php`` 中定义的 ``$supportedLocales`` 中的有效语言环境不匹配,将使用默认语言环境取代,除非你设置只使用 App 配置文件中定义的受支持语言环境:

.. literalinclude:: localization/018.php

.. note:: ``useSupportedLocalesOnly()`` 方法可以在 v4.3.0 及以上版本中使用。

设置当前语言环境
==========================

如果你想直接设置语言环境，可以使用 ``IncomingRequest::setLocale(string $locale)``。

在设置语言环境之前，你必须设置有效的语言环境。因为任何尝试设置无效语言环境的操作都会导致设置 :ref:`默认语言环境 <setting-the-default-locale>`。

默认情况下，有效的语言环境在 **app/Config/App.php** 中的 ``Config\App::$supportedLocales`` 中定义：

.. literalinclude:: localization/003.php

.. note:: 自 v4.4.0 起，``IncomingRequest::setValidLocales()`` 已被添加用于设置（和重置）有效的语言环境。如果你想动态更改有效的语言环境，请使用它。

获取当前语言环境
=============================

当前语言环境始终可以从 IncomingRequest 对象中通过 ``getLocale()`` 方法获取。
如果你的控制器继承了 ``CodeIgniter\Controller``,它将通过 ``$this->request`` 可用:

.. literalinclude:: localization/005.php

或者,你可以使用 :doc:`Services 类 </concepts/services>` 来检索当前请求:

.. literalinclude:: localization/006.php

*********************
语言本地化
*********************

创建语言文件
=======================

.. note:: 语言文件没有命名空间。

语言文件没有任何特定的命名约定是必需的。文件名应该具有描述它所包含内容的逻辑名称。例如,假设你想创建一个包含错误信息的文件。你可以简单地将其命名为:**Errors.php**。

在文件中,你将返回一个数组,数组中的每个元素都有一个语言键和可以返回的字符串:

.. literalinclude:: localization/007.php

它也支持嵌套定义:

.. literalinclude:: localization/008.php

.. literalinclude:: localization/009.php

基本用法
===========

你可以使用 :php:func:`lang()` 辅助函数来检索任何语言文件中的文本,方法是将文件名和语言键作为第一个参数传递,用点号 (.) 分隔。例如,要从 **Errors.php** 语言文件加载 ``errorEmailMissing`` 字符串,你可以执行以下操作:

.. literalinclude:: localization/010.php

对于嵌套定义,你可以执行以下操作:

.. literalinclude:: localization/011.php

如果请求的语言键在当前语言环境的文件中不存在,字符串将原封不动地返回。在此例中,如果它不存在,将返回 'Errors.errorEmailMissing' 或者 'Errors.nested.error.message'。

替换参数
--------------------

.. note:: 以下函数都需要在你的系统上加载 `intl <https://www.php.net/manual/en/book.intl.php>`_ 扩展才能工作。如果没有加载该扩展,将不会尝试替换。你可以在 `Sitepoint <https://www.sitepoint.com/localization-demystified-understanding-php-intl/>`_ 上找到很好的概述。

你可以将值数组作为 ``lang()`` 函数的第二个参数传递,以替换语言字符串中的占位符。这允许非常简单的数字翻译和格式化:

.. literalinclude:: localization/012.php

数组中第一个项目对应于索引的项目的占位符,如果是数字的话:

.. literalinclude:: localization/013.php

你也可以使用命名键以保持简洁,如果你愿意的话:

.. literalinclude:: localization/014.php

显然,你不仅可以进行数字替换。根据项目底层库的
`官方 ICU 文档 <https://unicode-org.github.io/icu-docs/apidoc/released/icu4c/classMessageFormat.html#details>`_ ,
可以替换以下类型的数据:

* 数字 - 整数、货币、百分比
* 日期 - 短、中、长、完整
* 时间 - 短、中、长、完整
* 拼写 - 拼出数字(即 34 变为 thirty-four)
* 序数
* 时长

这里有一些例子:

.. literalinclude:: localization/015.php

你应该确保阅读 MessageFormatter 类和基础 ICU 格式相关的内容,以更好地了解它的功能,比如执行条件替换、复数化等。之前提供的两个链接都会给你关于可用选项的极好的主意。

指定语言环境
-----------------

要指定不同的语言环境用于替换参数,你可以将语言环境作为第三个参数传递给 ``lang()`` 函数。

.. literalinclude:: localization/016.php

嵌套数组
-------------

语言文件也允许使用嵌套数组使得使用列表等更简单。

.. literalinclude:: localization/017.php

语言回退
=================

如果你为一个给定的语言环境拥有一组消息,例如
**Language/en/app.php**,你可以为该语言环境添加语言变体,
每种变体各自一个文件夹,例如 **Language/en-US/app.php**。

你只需要为需要针对该语言环境变体进行本地化的消息提供不同的值。
任何缺失的消息定义将自动从主要的语言环境中获取。

更好的是,本地化可以一直回退到英语,
以防还没有机会为你的语言环境翻译框架中添加的新消息。

因此,如果你使用 ``fr-CA`` 语言环境,则本地化消息将首先在
**Language/fr-CA** 目录中查找,然后在 **Language/fr** 目录中查找,
最后在 **Language/en** 目录中查找。

消息翻译
====================

我们在自己的 `仓库 <https://github.com/codeigniter4/translations>`_ 中有一组“官方”翻译。

你可以下载该仓库,并将其 **Language** 文件夹复制到
你的 **app** 文件夹中。合并的翻译将被自动使用,因为 ``App`` 命名空间映射到你的 **app** 文件夹。

或者,在你的项目中运行以下命令会更好:

.. code-block:: console

    composer require codeigniter4/translations

翻译的消息将自动被使用,因为翻译文件夹得到了正确的映射。

.. _generating-translation-files-via-command:

通过命令生成翻译文件
====================

.. versionadded:: 4.5.0

你可以在 **app** 文件夹中自动生成和更新翻译文件。该命令将搜索 ``lang()`` 函数的使用，通过定义 ``Config\App`` 中的语言环境 ``defaultLocale`` 来合并 **app/Language** 中当前的翻译键。操作完成后，你需要自行翻译这些语言键。该命令能够正常识别嵌套键，例如 ``File.array.nested.text``。之前保存的键不会改变。

.. code-block:: console

    php spark lang:find

.. literalinclude:: localization/019.php

.. note:: 当命令扫描文件夹时，**app/Language** 将被跳过。

生成的语言文件很可能不符合你的编码标准。建议对它们进行格式化。例如，如果安装了 ``php-cs-fixer``，可以运行 ``vendor/bin/php-cs-fixer fix ./app/Language``。

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

为了更准确的搜索，可以指定所需的语言环境或要扫描的目录。

.. code-block:: console

    php spark lang:find --dir Controllers/Translation --locale en --show-new

详细信息可以通过运行以下命令找到：

.. code-block:: console

    php spark lang:find --help
