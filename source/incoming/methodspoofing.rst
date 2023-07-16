####################
HTTP 方法欺骗
####################

当使用 HTML 表单时,你只能使用 GET 或 POST HTTP 动词。在大多数情况下,这已经足够了。然而,为了
支持 RESTful 路由,你需要支持其他更正确的动词,比如 DELETE 或 PUT。由于浏览器
不支持这些,CodeIgniter 为你提供了一种办法来欺骗所使用的方法。这使得你可以
发出一个 POST 请求,但是告诉应用程序它应该被视为不同的请求类型。

要欺骗方法,需要在表单中添加一个隐藏的输入,名称为 ``_method``。它的值是你希望
请求采用的 HTTP 动词::

    <form action="" method="post">
        <input type="hidden" name="_method" value="PUT">
    </form>

这个表单会被转换成一个 PUT 请求,对于路由和 IncomingRequest
类来说,它是一个真正的 PUT 请求。

你使用的表单必须是一个 POST 请求。GET 请求无法被欺骗。

.. note:: 请确保检查你的 Web 服务器配置,因为一些服务器默认配置不支持所有 HTTP 动词,
    必须启用其他软件包才能正常工作。
