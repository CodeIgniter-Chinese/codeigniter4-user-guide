鉴权
#####################################

CodeIgniter本身不提供一个内部鉴权或认证的类。不过有许多优秀的第三方模块可以提供类似的服务，而且在社区里也有许多资源以帮助你自己实现一个类似的功能。
我们鼓励开发者们基于以下原则来共享模块，项目以及框架本身。

Recommendations
===============

* 处理登入和登出操作的模块需要在操作成功时触发 ``login`` 和 ``logout`` 事件
* 定义了“当前用户”的模块应该定义一个 ``user_id()`` 方法来返回当前用户的唯一识别符，或者是在不存在当前用户时返回 ``null``