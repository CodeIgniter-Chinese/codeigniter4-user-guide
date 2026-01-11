##############
AJAX 请求
##############

``IncomingRequest::isAJAX()`` 方法使用 ``X-Requested-With`` 请求头来判断请求是 XHR 还是普通请求。然而，最新的 JavaScript 实现（例如 fetch）不再随请求发送此请求头，因此 ``IncomingRequest::isAJAX()`` 的使用变得不太可靠，因为如果没有此请求头，就无法确定请求是否为 XHR。

为了解决这个问题，目前最有效的解决方案是手动定义请求头，强制将信息发送到服务器，服务器随后就能识别出该请求是 XHR。

以下是强制在 Fetch API 和其他 JavaScript 库中发送 ``X-Requested-With`` 请求头的方法。

.. contents::
    :local:
    :depth: 2

Fetch API
=========

.. code-block:: javascript

    fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Requested-With": "XMLHttpRequest"
        }
    });

jQuery
======

对于 jQuery 等库，无需显式发送此请求头，因为根据 `官方文档 <https://api.jquery.com/jquery.ajax/>`_，它是所有 ``$.ajax()`` 请求的标准请求头。但如果你仍想强制发送以降低风险，只需按如下方式操作：

.. code-block:: javascript

    $.ajax({
        url: "your url",
        headers: {'X-Requested-With': 'XMLHttpRequest'}
    });

VueJS
=====

在 VueJS 中，只要你使用 Axios 处理此类请求，只需将以下代码添加到 ``created`` 函数中即可。

.. code-block:: javascript

    axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

React
=====

.. code-block:: javascript

    axios.get("your url", {headers: {'Content-Type': 'application/json'}})

htmx
====

可以使用 `ajax-header <https://github.com/bigskysoftware/htmx-extensions/blob/main/src/ajax-header/README.md>`_ 扩展。

.. code-block:: html

    <body hx-ext="ajax-header">
    ...
    </body
