身份验证
#####################################

CodeIgniter 为 CodeIgniter 4 提供了一个官方的身份验证和授权框架 :ref:`CodeIgniter Shield <shield>`，它被设计为安全、灵活且易于扩展，以满足许多不同类型网站的需求。

为了在开发者之间保持一致，以下是一些推荐的准则。

推荐
===============

* 处理登录和登出操作的模块在成功时应该触发 ``login`` 和 ``logout`` 事件
* 定义“当前用户”的模块应该定义 ``user_id()`` 函数以返回用户的唯一标识符，如果没有当前用户则返回 ``null``

符合这些推荐的模块可以在 **composer.json** 中添加以下内容表示兼容::

    "provide": {
        "codeigniter4/authentication-implementation": "1.0"
    },

你可以在 `Packagist <https://packagist.org/providers/codeigniter4/authentication-implementation>`_ 上查看提供该实现的模块列表。
