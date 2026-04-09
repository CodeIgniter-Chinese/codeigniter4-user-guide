####################################
跨域资源共享 (CORS)
####################################

.. versionadded:: 4.5.0

跨域资源共享（CORS）是一种基于 HTTP 标头的安全机制，
允许服务器声明除自身之外的任何源（域名、协议或端口），浏览器应允许从这些源加载资源。

CORS 通过向 HTTP 请求和响应中添加标头，以指示所请求的资源是否可以在不同源之间共享，
这样有助于防止跨站请求伪造（CSRF）和数据窃取等恶意攻击。

若对 CORS 及其标头不熟悉，请先阅读 `MDN CORS 文档`_。

.. _MDN CORS 文档: https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Guides/CORS#http_响应标头字段

CodeIgniter 提供了 CORS 过滤器和辅助类。

.. contents::
    :local:
    :depth: 2

****************
配置 CORS
****************

设置默认配置
======================

CORS 通过 **app/Config/Cors.php** 进行配置。

至少需要在 ``$default`` 属性中设置以下项：

- ``allowedOrigins``：显式列出允许的来源（Origin）。
- ``allowedHeaders``：显式列出允许的 HTTP 标头。
- ``allowedMethods``：显式列出允许的 HTTP 方法。

.. warning:: 遵循最小权限原则，仅允许必需的 Origin、Methods 和 Headers。

若跨域请求需要发送凭据（如 Cookie），将 ``supportsCredentials`` 设为 ``true``。

启用 CORS
=============

启用 CORS 需要完成两项设置：

1. 在允许 CORS 的路由上指定 ``cors`` 过滤器。
2. 为 CORS 预检请求添加 **OPTIONS** 路由。

在路由中设置
------------------

可在 **app/Config/Routes.php** 中为路由设置 ``cors`` 过滤器。

例如：

.. literalinclude:: cors/001.php

别忘了为预检请求添加 OPTIONS 路由。因为控制器过滤器（除 Required 过滤器外）
在路由不存在时不会生效。

CORS 过滤器会处理所有预检请求，因此 OPTIONS 路由的闭包控制器通常不会被调用。

在 Config\\Filters 中设置
-------------------------

或者，也可在 **app/Config/Filters.php** 中为 URI 路径设置 ``cors`` 过滤器。

例如：

.. literalinclude:: cors/002.php

别忘了为预检请求添加 OPTIONS 路由。因为控制器过滤器（除 Required 过滤器外）
在路由不存在时不会生效。

例如：

.. literalinclude:: cors/003.php

CORS 过滤器会处理所有预检请求，因此 OPTIONS 路由的闭包控制器通常不会被调用。

检查路由和过滤器
===========================

配置完成后，可使用 :ref:`routing-spark-routes` 命令检查路由和过滤器。

设置其他配置
======================

若需使用默认配置以外的其他配置，请在 **app/Config/Cors.php** 中添加属性。

例如，添加 ``$api`` 属性：

.. literalinclude:: cors/004.php

属性名称（上例中的 ``api``）将成为配置名称。

然后在过滤器参数中指定该属性名称，如 ``cors:api``：

.. literalinclude:: cors/005.php

也可使用 :ref:`filters-filters-filter-arguments`。

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

    添加 CORS 响应标头。

.. php:method:: handlePreflightRequest(RequestInterface $request, ResponseInterface $response): ResponseInterface

    :param RequestInterface $request: 请求实例
    :param ResponseInterface $response: 响应实例
    :returns: 响应实例
    :rtype: ResponseInterface

    处理预检请求。

.. php:method:: isPreflightRequest(IncomingRequest $request): bool

    :param IncomingRequest $request: 请求实例
    :returns: 若请求为预检请求则返回 true
    :rtype: bool

    检查请求是否为预检请求。
