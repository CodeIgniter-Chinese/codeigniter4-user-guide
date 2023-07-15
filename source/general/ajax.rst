##############
AJAX 请求
##############

IncomingRequest::isAJAX() 方法使用 X-Requested-With 头来定义请求是否是 XHR 还是普通的。然而,最新的 JavaScript 实现(即 fetch)在发送请求时不再发送此头,因此 IncomingRequest::isAJAX() 的使用变得不太可靠,因为没有此头就无法定义请求是否是 XHR。

为了解决这个问题,最有效的解决方案(到目前为止)是手动定义请求头,强制向服务器发送信息,然后服务器将能够识别请求是 XHR。

下面是如何在 Fetch API 和其他 JavaScript 库中强制发送 X-Requested-With 头。

.. contents::
  :local:
  :depth: 2

Fetch API
=========

.. code-block:: javascript

  fetch(url, {
      method: "get",
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
      }
  });

jQuery
======

对于像 jQuery 这样的库,不必明确发送此头,因为根据官方文档,所有 $.ajax() 请求都是标准头。但如果您仍要强制发送以防万一,只需如下所示:

.. code-block:: javascript

  $.ajax({
      url: "your url",
      headers: {'X-Requested-With': 'XMLHttpRequest'}
  });

VueJS
=====

在 VueJS 中,只要您使用 Axios 进行这种请求,就需要将以下代码添加到 created 函数中。

.. code-block:: javascript

  axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

React
=====

.. code-block:: javascript

  axios.get("your url", {headers: {'Content-Type': 'application/json'}})

htmx
====

您可以使用 ajax-header 扩展。

.. code-block:: html

  <body hx-ext="ajax-header">
  ...
  </body>
