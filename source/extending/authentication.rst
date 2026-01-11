身份验证
#####################################

CodeIgniter 为 CodeIgniter 4 提供了官方的身份验证和授权框架 :ref:`CodeIgniter Shield <shield>`，
它旨在提供安全、灵活且易于扩展的功能，以满足各种类型网站的需求。

以下是推荐的指南，以鼓励模块、项目和框架本身的开发者之间保持一致性。

推荐实践
===============

* 处理登录和登出操作的模块应在成功时触发 ``login`` 和 ``logout`` 事件
* 定义“当前用户”的模块应定义 ``user_id()`` 函数以返回用户的唯一标识符，或对“无当前用户”情况返回 ``null``

满足这些推荐实践的模块可通过在 **composer.json** 中添加以下内容来表明其兼容性::

    "provide": {
        "codeigniter4/authentication-implementation": "1.0"
    },

你可以在 `Packagist <https://packagist.org/providers/codeigniter4/authentication-implementation>`_ 上查看提供此实现的模块列表。
