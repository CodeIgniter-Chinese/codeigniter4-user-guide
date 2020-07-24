##############
AJAX请求
##############

``IncomingRequest::isAJAX()`` 方法使用了 ``X-Requested-With`` 请求头来确定一个请求是否是XHR(XML Http Request)或者是一个正常的请求。
然后最新的JavaScript实现（例如fetch方法）中不再随着请求发送这个头，因此使用 ``IncomingRequest::isAJAX()`` 就不那么可靠了，因为没有这个头，该方法就不能识别一个请求是否是一个XHR。

为了解决这个问题，最有效的解决方式（至今）就是人为定义一个请求头，迫使这个请求信息发送的服务器从而识别这个请求是否是一个XHR。

以下就是如何迫使在Fetch API和其他JavaScript库中发送 ``X-Requested-With`` 请求头。

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

对于类似jQuery之类的库来说，不需要额外发送这个头，因为根据 `官方文档 <https://api.jquery.com/jquery.ajax/>`_ ，对于所有 ``$.ajax()`` 请求来说，这都是一个标准头。
但是如果你还是不想担风险并强制发送这个头，就像下面这样做吧:

.. code-block:: javascript

    $.ajax({
        url: "your url",
        headers: {'X-Requested-With': 'XMLHttpRequest'}
    });


VueJS
=====

在VueJS中你只需要在 ``created`` 函数中增加以下代码，只要你在这类请求时使用Axios:

.. code-block:: javascript

    axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';


React
=====

.. code-block:: javascript

    axios.get("your url", {headers: {'Content-Type': 'application/json'}})
