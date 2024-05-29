####################################
跨域资源共享 (CORS)
####################################

.. versionadded:: 4.5.0

跨域资源共享 (CORS) 是一种基于 HTTP 头的安全机制，允许服务器指示浏览器应允许从其自身以外的任何来源（域名、协议或端口）加载资源。

CORS 通过在 HTTP 请求和响应中添加头来工作，以指示请求的资源是否可以跨不同来源共享，从而帮助防止恶意攻击，如跨站请求伪造 (CSRF) 和数据盗窃。

如果你不熟悉 CORS 和 CORS 头，请阅读 `MDN 上的 CORS 文档`_。

.. _MDN 上的 CORS 文档: https://developer.mozilla.org/zh-CN/docs/Web/HTTP/CORS#http_%E5%93%8D%E5%BA%94%E6%A0%87%E5%A4%B4%E5%AD%97%E6%AE%B5

CodeIgniter 提供了 CORS 过滤器和 helper 类。

.. contents::
    :local:
    :depth: 2

****************
配置 CORS
****************

设置默认配置
======================

可以通过 **app/Config/Cors.php** 配置 CORS。

至少需要设置 ``$default`` 属性中的以下项目：

- ``allowedOrigins``: 明确列出你想要允许的来源。
- ``allowedHeaders``: 明确列出你想要允许的 HTTP 头。
- ``allowedMethods``: 明确列出你想要允许的 HTTP 方法。

.. warning:: 基于最小特权原则，只应允许必要的最小来源、方法和头。

如果你在跨域请求中发送凭证（例如，cookies），请将 ``supportsCredentials`` 设置为 ``true``。

启用 CORS
=============

要启用 CORS，你需要做两件事：

1. 为允许 CORS 的路由指定 ``cors`` 过滤器。
2. 为 CORS 预检请求添加 **OPTIONS** 路由。

设置路由
------------------

你可以在 **app/Config/Routes.php** 中为路由设置 ``cors`` 过滤器。

例如，

.. literalinclude:: cors/001.php

不要忘记为预检请求添加 OPTIONS 路由。因为如果路由不存在，控制器过滤器（必需过滤器除外）将不起作用。

CORS 过滤器处理所有预检请求，因此通常不会调用 OPTIONS 路由的闭包控制器。

在 Config\\Filters 中设置
-------------------------

或者，你可以在 **app/Config/Filters.php** 中为 URI 路径设置 ``cors`` 过滤器。

例如，

.. literalinclude:: cors/002.php

不要忘记为预检请求添加 OPTIONS 路由。因为如果路由不存在，控制器过滤器（必需过滤器除外）将不起作用。

例如，

.. literalinclude:: cors/003.php

CORS 过滤器处理所有预检请求，因此通常不会调用 OPTIONS 路由的闭包控制器。

检查路由和过滤器
===========================

配置完成后，你可以使用 :ref:`routing-spark-routes` 命令检查路由和过滤器。

设置其他配置
======================

如果你想使用不同于默认配置的配置，请在 **app/Config/Cors.php** 中添加一个属性。

例如，添加 ``$api`` 属性。

.. literalinclude:: cors/004.php

属性名称（在上述示例中为 ``api``）将成为配置名称。

然后，像 ``cors:api`` 一样将属性名称指定为过滤器参数：

.. literalinclude:: cors/005.php

你也可以使用 :ref:`filters-filters-filter-arguments`。

***************
类参考
***************

.. php:namespace:: CodeIgniter\HTTP

.. php:class:: Cors

.. php:method:: addResponseHeaders(RequestInterface $request, ResponseInterface $response): ResponseInterface

    :param RequestInterface $request: 请求实例
    :param ResponseInterface $response: 响应实例
    :returns: 响应实例
    :rtype: ResponseInterface

    添加 CORS 的响应头。

.. php:method:: handlePreflightRequest(RequestInterface $request, ResponseInterface $response): ResponseInterface

    :param RequestInterface $request: 请求实例
    :param ResponseInterface $response: 响应实例
    :returns: 响应实例
    :rtype: ResponseInterface

    处理预检请求。

.. php:method:: isPreflightRequest(IncomingRequest $request): bool

    :param IncomingRequest $request: 请求实例
    :returns: 如果是预检请求则返回 True。
    :rtype: bool

    检查请求是否为预检请求。
