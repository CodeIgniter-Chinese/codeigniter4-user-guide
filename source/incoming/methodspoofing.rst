####################
HTTP 方法伪装
####################

在使用 HTML 表单时，你只能使用 GET 或 POST HTTP 动词。大多数情况下，这完全没问题。然而，为了支持 REST-ful 路由，你需要支持其他更正确的动词，例如 DELETE 或 PUT。由于浏览器不支持这些动词，CodeIgniter 提供了一种伪装所用方法的方式。这允许你发送 POST 请求，但告诉应用程序将其作为另一种请求类型来处理。

要伪装请求方法，需向表单添加一个名为 ``_method`` 的隐藏输入字段。其值是你希望请求使用的 HTTP 动词::

    <form action="" method="post">
        <input type="hidden" name="_method" value="PUT">
    </form>

该表单会被转换为 PUT 请求，就路由和 IncomingRequest 类而言，这就是一个真正的 PUT 请求。

你使用的表单必须发送 POST 请求。GET 请求无法被伪装。

.. note:: 请务必检查你的 Web 服务器配置，因为某些服务器的默认配置不支持所有 HTTP 动词，必须启用额外的包才能正常工作。
