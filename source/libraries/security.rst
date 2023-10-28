########
安全
########

安全类包含帮助保护你的网站免受跨站请求伪造(CSRF)攻击的方法。

.. contents::
    :local:
    :depth: 3

*******************
加载库
*******************

如果你加载库的唯一兴趣是处理 CSRF 保护,那么你永远不需要加载它,因为它作为过滤器运行且没有手动交互。

但是,如果你发现确实需要直接访问,你可以通过 Services 文件加载它:

.. literalinclude:: security/001.php

.. _cross-site-request-forgery:

*********************************
跨站请求伪造(CSRF)
*********************************

.. warning:: CSRF 保护仅适用于 **POST/PUT/PATCH/DELETE** 请求。不保护其他方法的请求。

先决条件
============

当你使用 CodeIgniter 的 CSRF 保护时,仍需要按如下方式编写代码。否则,CSRF 保护可能会被绕过。

当自动路由被禁用时
-----------------------------

执行以下操作之一:

1. 不要使用 ``$routes->add()``,并在路由中使用 HTTP 动词。
2. 在处理之前,在控制器方法中检查请求方法。

例如::

    if (! $this->request->is('post')) {
        return $this->response->setStatusCode(405)->setBody('Method Not Allowed');
    }

.. note:: 自 v4.3.0 起,可以使用 :ref:`$this->request->is() <incomingrequest-is>` 方法。
    在以前的版本中,你需要使用 ``if (strtolower($this->request->getMethod()) !== 'post')``。

当自动路由被启用时
----------------------------

1. 在处理之前,在控制器方法中检查请求方法。

例如::

    if (! $this->request->is('post')) {
        return $this->response->setStatusCode(405)->setBody('Method Not Allowed');
    }

CSRF 配置
===============

.. _csrf-protection-methods:

CSRF 保护方法
-----------------------

默认情况下,使用基于 Cookie 的 CSRF 保护。它是 OWASP 跨站请求伪造预防备忘单上的
`双重提交 Cookie <https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#double-submit-cookie>`_。

你也可以使用基于会话的 CSRF 保护。它是
`同步令牌模式 <https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#synchronizer-token-pattern>`_。

你可以通过编辑以下配置参数的值在 **app/Config/Security.php** 来设置使用基于会话的 CSRF 保护:

.. literalinclude:: security/002.php

令牌随机化
-------------------

为了缓解像 `BREACH`_ 这样的压缩旁道攻击,并阻止攻击者猜测 CSRF 令牌,你可以配置令牌随机化(默认关闭)。

如果你启用它,随机掩码会添加到令牌中并用于扰乱它。

.. _`BREACH`: https://en.wikipedia.org/wiki/BREACH

你可以通过编辑以下配置参数的值在 **app/Config/Security.php** 来启用它:

.. literalinclude:: security/003.php

令牌再生成
------------------

令牌可以在每次提交时重新生成(默认),或者在 CSRF cookie 的整个生命周期内保持不变。令牌的默认再生成提供了更严格的安全性,但可能导致可用性问题,因为其他令牌变得无效(后退/前进导航、多个选项卡/窗口、异步操作等)。你可以通过编辑以下配置参数的值在 **app/Config/Security.php** 来更改此行为:

.. literalinclude:: security/004.php

.. note:: 自 v4.2.3 起,你可以用 ``Security::generateHash()`` 方法手动重新生成 CSRF 令牌。

.. _csrf-redirection-on-failure:

失败时重定向
----------------------

自 v4.3.0 起,当请求失败 CSRF 验证检查时,它将默认抛出 SecurityException。

.. note:: 在生产环境中,当你使用 HTML 表单时,建议启用此重定向以获得更好的用户体验。

如果你想重定向到上一页,请在 **app/Config/Security.php** 中更改以下配置参数的值:

.. literalinclude:: security/005.php

重定向后,会设置一个 ``error`` 闪存消息,可以使用以下视图代码显示给最终用户::

    <?= session()->getFlashdata('error') ?>

这比简单地崩溃提供了更好的体验。

即使重定向值为 ``true``,AJAX 调用也不会重定向,而会抛出 SecurityException。

启用 CSRF 保护
======================

你可以通过更改 **app/Config/Filters.php** 并全局启用 `csrf` 过滤器来启用 CSRF 保护:

.. literalinclude:: security/006.php

可以将某些 URI 从 CSRF 保护中排除(例如期望外部 POST 内容的 API 端点)。你可以通过在过滤器中将它们添加为例外来添加这些 URI:

.. literalinclude:: security/007.php

正则表达式也支持(不区分大小写):

.. literalinclude:: security/008.php

也可以仅针对特定方法启用 CSRF 过滤器:

.. literalinclude:: security/009.php

.. Warning:: 如果使用 ``$methods`` 过滤器,你应该 :ref:`禁用自动路由(传统) <use-defined-routes-only>`,因为 :ref:`auto-routing-legacy` 允许任何 HTTP 方法访问控制器。使用你不期望的方法访问控制器可能会绕过过滤器。

HTML 表单
==========

如果使用 :doc:`表单辅助函数 <../helpers/form_helper>`,那么 :func:`form_open()` 将自动在你的表单中插入一个隐藏的 csrf 字段。

.. note:: 要使用 CSRF 字段的自动生成,你需要对表单页面打开 CSRF 过滤器。在大多数情况下,它使用 ``GET`` 方法请求。

如果没有,你可以使用始终可用的 ``csrf_token()`` 和 ``csrf_hash()`` 函数::

    <input type="hidden" name="<?= csrf_token() ?>" value="<?= csrf_hash() ?>" />

另外,你可以使用 ``csrf_field()`` 方法为你生成这个隐藏的输入字段::

    // 生成:<input type="hidden" name="{csrf_token}" value="{csrf_hash}" />
    <?= csrf_field() ?>

在发送 JSON 请求时,CSRF 令牌也可以作为一个参数传递。
通过 ``csrf_header()`` 函数可用的下一个传递 CSRF 令牌的方式是特殊的 Http 头。

另外,你可以使用 ``csrf_meta()`` 方法为你生成这个方便的 meta 标签::

    // 生成:<meta name="{csrf_header}" content="{csrf_hash}" />
    <?= csrf_meta() ?>

用户发送令牌的顺序
=================================

检查 CSRF 令牌可用性的顺序如下:

1. ``$_POST`` 数组
2. HTTP 头
3. ``php://input`` (JSON 请求) - 请记住,这种方法是最慢的,因为我们必须解码 JSON 然后重新编码它
4. ``php://input`` (原始 body) - 适用于 PUT、PATCH 和 DELETE 类型的请求

.. note:: 自 v4.4.2 起，会检查 ``php://input`` (原始 body)。

*********************
其他有用的方法
*********************

你很少需要直接使用 Security 类中的大多数方法。以下是与 CSRF 保护无关的可能对你有帮助的方法。

sanitizeFilename()
==================

试图清理文件名以防止目录遍历攻击和其他安全威胁,这对于通过用户输入提供的文件特别有用。第一个参数是要清理的路径。

如果用户输入可以包含相对路径,例如 **file/in/some/approved/folder.txt**,你可以将第二个可选参数 ``$relativePath`` 设置为 ``true``。

.. literalinclude:: security/010.php
