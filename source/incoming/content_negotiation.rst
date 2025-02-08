###################
内容协商
###################

.. contents::
    :local:
    :depth: 2

****************************
什么是内容协商？
****************************

内容协商是一种根据客户端处理能力和服务器处理能力，决定返回何种内容类型给客户端的方式。这种方式可用于判断客户端需要 HTML 还是 JSON 响应，图像应以 JPEG 还是 PNG 格式返回，支持哪种压缩类型等。该机制通过分析四个不同的头部实现，每个头部可支持多个具有优先级的选项值。

手动实现这种匹配可能颇具挑战。CodeIgniter 提供了 ``Negotiator`` 类来为你处理这些工作。

本质上，内容协商是 HTTP 规范的一部分，允许单一资源提供多种内容类型，让客户端请求最适合其需求的数据格式。

一个经典例子是：无法显示 PNG 文件的浏览器可以请求仅限 GIF 或 JPEG 图像。服务器接收请求时，会查看客户端请求的可用文件类型，并从支持的图像格式中选择最佳匹配（本例中可能选择返回 JPEG 图像）。

这种协商可应用于四种数据类型：

* **媒体/文档类型** - 可以是图像格式，或 HTML、XML、JSON 等文档格式
* **字符集** - 返回文档应使用的字符集，通常为 UTF-8
* **文档编码** - 通常指对结果使用的压缩类型
* **文档语言** - 对于支持多语言的站点，帮助确定返回哪种语言版本

*****************
加载类
*****************

你可以通过 Service 类手动加载该类的实例：

.. literalinclude:: content_negotiation/001.php

这将获取当前请求实例并自动注入到 Negotiator 类中。

此类无需单独加载。你可以通过请求的 ``IncomingRequest`` 实例访问其方法。虽然不能直接访问，但可以通过 ``negotiate()`` 方法轻松调用所有功能：

.. literalinclude:: content_negotiation/002.php

通过此方式访问时，第一个参数是你尝试匹配的内容类型，第二个参数是支持的选项数组。

***********
协商过程
***********

本节将讨论可协商的四种内容类型，并展示使用上述两种方法访问协商器的示例。

媒体类型
========

首要处理的是「媒体类型」协商。这些信息由 ``Accept`` 头部提供，是最复杂的头部之一。常见用例是客户端告知服务器期望的数据格式，这在 API 中尤为常见。例如，客户端可能请求 API 端点返回 JSON 格式数据::

    GET /foo HTTP/1.1
    Accept: application/json

服务器现在需要提供其支持的内容类型列表。在此示例中，API 可能返回原始 HTML、JSON 或 XML 格式数据。该列表应按优先级顺序排列：

.. literalinclude:: content_negotiation/003.php

本例中，客户端和服务器都同意使用 JSON 格式，因此 negotiate 方法返回 'json'。默认情况下，若未找到匹配项，将返回 ``$supported`` 数组的第一个元素。但有时需要严格匹配格式，若将最后一个参数设为 ``true``，则无匹配时返回空字符串：

.. literalinclude:: content_negotiation/004.php

语言协商
========

另一个常见用途是确定返回内容的语言。对于单语言站点影响不大，但任何支持多语言翻译的站点都会发现其用处，因为浏览器通常会在 ``Accept-Language`` 头部发送首选语言::

    GET /foo HTTP/1.1
    Accept-Language: fr; q=1.0, en; q=0.5

本例中，浏览器首选法语，次选英语。若你的网站支持英语和德语，可进行如下操作：

.. literalinclude:: content_negotiation/005.php

此例将返回 'en' 作为当前语言。若无匹配项，则返回 ``$supported`` 数组的第一个元素，因此该元素应始终设为首选语言。

严格区域设置协商
-------------------------

.. versionadded:: 4.6.0

默认情况下，区域设置基于近似匹配（仅考虑 locale 字符串的首部分即语言）。这通常已足够。但有时我们需要区分诸如 ``en-US`` 和 ``en-GB`` 等区域版本以提供不同内容。

针对此类情况，我们新增了可通过 ``Config\Feature::$strictLocaleNegotiation`` 启用的设置。这将确保首先进行严格比较。

.. note::

    CodeIgniter 仅为主语言标签（'en', 'fr' 等）提供翻译。若启用此功能且 ``Config\App::$supportedLocales`` 包含区域语言标签（'en-US', 'fr-FR' 等），请注意：若你拥有自定义翻译文件，**必须同时修改** CodeIgniter 翻译文件的文件夹名称以匹配 ``$supportedLocales`` 数组中的设置。

现在考虑以下示例，浏览器首选语言设置为::

    GET /foo HTTP/1.1
    Accept-Language: fr; q=1.0, en-GB; q=0.5

本例中，浏览器首选法语，次选英语（英国）。而你的网站支持德语和英语（美国）：

.. literalinclude:: content_negotiation/008.php

此例将返回 'en-US' 作为当前语言。若无匹配项，则返回 ``$supported`` 数组的首元素。以下是区域选择过程的具体工作原理。

尽管浏览器首选 'fr'，但其不在我们的 ``$supported`` 数组中。'en-GB' 同样存在匹配问题，但我们可以搜索变体。首先回退到最通用的区域设置（本例为 'en'），其仍不在数组中。接着搜索区域设置 'en-''，此时将匹配 ``$supported`` 数组中的 'en-US' 并返回。

区域选择流程如下：

#. 严格匹配（'en-GB'）- ISO 639-1 加 ISO 3166-1 alpha-2
#. 通用区域匹配（'en'）- ISO 639-1
#. 区域通配符匹配（'en-'）- ISO 639-1 加 ISO 3166-1 alpha-2 通配符

编码协商
========

``Accept-Encoding`` 头部包含客户端偏好的字符集，用于指定支持的压缩类型::

    GET /foo HTTP/1.1
    Accept-Encoding: compress, gzip

你的 Web 服务器将定义可使用的压缩类型。某些服务器（如 Apache）仅支持 **gzip**：

.. literalinclude:: content_negotiation/006.php

更多信息参见 `维基百科 <https://en.wikipedia.org/wiki/HTTP_compression>`_。

字符集协商
=============

期望的字符集通过 ``Accept-Charset`` 头部传递::

    GET /foo HTTP/1.1
    Accept-Charset: utf-16, utf-8

默认情况下若无匹配项，将返回 **utf-8**：

.. literalinclude:: content_negotiation/007.php
