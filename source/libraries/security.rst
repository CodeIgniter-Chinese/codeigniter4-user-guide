###########
Security 类
###########

Security 类提供用于防范跨站请求伪造（CSRF）攻击的方法。

.. contents::
    :local:
    :depth: 3

*******************
加载类
*******************

如仅需通过加载该库来处理 CSRF 防护，则无需手动加载，
因其以过滤器形式运行，无需手动交互。

如确有直接访问需求，可通过 Services 文件加载：

.. literalinclude:: security/001.php

.. _cross-site-request-forgery:

*********************************
跨站请求伪造（CSRF）
*********************************

.. warning:: CSRF 防护仅对 **POST/PUT/PATCH/DELETE** 请求有效。
    其他方法的请求不受保护。

前提条件
============

使用 CodeIgniter 的 CSRF 防护时，仍需按以下方式编码，
否则 CSRF 防护可能被绕过。

自动路由禁用时
-----------------------------

执行以下操作之一：

1. 不使用 ``$routes->add()``，路由中使用 HTTP 方法。
2. 处理前在控制器方法中检查请求方法。

示例::

    if (! $this->request->is('post')) {
        return $this->response->setStatusCode(405)->setBody('Method Not Allowed');
    }

.. note:: :ref:`$this->request->is() <incomingrequest-is>` 方法自 v4.3.0 起可用。
    早期版本需使用
    ``if (strtolower($this->request->getMethod()) !== 'post')``。

自动路由启用时
----------------------------

1. 处理前在控制器方法中检查请求方法。

示例::

    if (! $this->request->is('post')) {
        return $this->response->setStatusCode(405)->setBody('Method Not Allowed');
    }

CSRF 配置
===============

.. _csrf-protection-methods:

CSRF 防护方法
-----------------------

.. warning:: 如使用 :doc:`Session <./sessions>`，请务必使用基于 Session 的
    CSRF 防护。基于 Cookie 的 CSRF 防护无法防止同站攻击。
    详情请参见
    `GHSA-5hm8-vh6r-2cjq <https://github.com/codeigniter4/shield/security/advisories/GHSA-5hm8-vh6r-2cjq>`_ 。

默认使用基于 Cookie 的 CSRF 防护，即 OWASP 跨站请求伪造防护备忘单中的
`双重提交 Cookie <https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#double-submit-cookie>`_
方案。

也可使用基于 Session 的 CSRF 防护，即
`同步器令牌模式 <https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#synchronizer-token-pattern>`_ 。

编辑 **app/Config/Security.php** 中的以下配置参数值，可设置为使用基于 Session 的 CSRF 防护：

.. literalinclude:: security/002.php

令牌随机化
-------------------

为缓解 `BREACH`_ 等压缩旁道攻击，并防止攻击者猜测 CSRF 令牌，可配置令牌随机化（默认关闭）。

启用后，将为令牌添加随机掩码并对其混淆。

.. _`BREACH`: https://en.wikipedia.org/wiki/BREACH

编辑 **app/Config/Security.php** 中的以下配置参数值可启用：

.. literalinclude:: security/003.php

令牌重新生成
------------------

令牌可在每次提交时重新生成（默认），或
在 Session 或 CSRF Cookie 的整个生命周期内保持不变。

默认的令牌重新生成提供更强的安全性，但可能导致
可用性问题，因为其他令牌会失效（后退/前进
导航、多个标签页/窗口、异步操作等）。编辑 **app/Config/Security.php** 中的以下配置参数值可更改此行为：

.. literalinclude:: security/004.php

.. warning:: 如使用基于 Cookie 的 CSRF 防护，并在提交后使用 :php:func:`redirect()`，
    必须调用 ``withCookie()`` 发送重新生成的 CSRF Cookie。详情请参见 :ref:`response-redirect`。

.. note:: 自 v4.2.3 起，可使用 ``Security::generateHash()`` 方法手动重新生成 CSRF 令牌。

.. _csrf-redirection-on-failure:

失败时重定向
----------------------

自 v4.5.0 起，当请求未通过 CSRF 验证检查时，默认情况下，
生产环境中用户将被重定向到上一页，其他环境中将抛出 SecurityException。

.. note:: 生产环境中使用 HTML 表单时，建议
    启用此重定向以获得更好的用户体验。

    升级用户应检查其配置文件。

如希望重定向到上一页，在 **app/Config/Security.php** 中将以下配置参数值设为 ``true``：

.. literalinclude:: security/005.php

重定向时，会设置 ``error`` 闪存消息，可在视图中通过以下代码显示给最终用户::

    <?= session()->getFlashdata('error') ?>

这比直接崩溃提供了更好的体验。

即使 redirect 值为 ``true``，AJAX 调用也不会重定向，而是抛出 SecurityException。

.. _enable-csrf-protection:

启用 CSRF 防护
======================

修改 **app/Config/Filters.php** 并全局启用 `csrf` 过滤器，即可启用 CSRF 防护：

.. literalinclude:: security/006.php

特定 URI 可从 CSRF 防护中排除（例如接收外部 POST 内容的 API 端点）。可在过滤器中将其添加为例外：

.. literalinclude:: security/007.php

也支持正则表达式（不区分大小写）：

.. literalinclude:: security/008.php

也可仅为特定方法启用 CSRF 过滤器：

.. literalinclude:: security/009.php

.. warning:: 如使用 ``$methods`` 过滤器，应 :ref:`禁用自动路由（传统版）<use-defined-routes-only>`，
    因为 :ref:`auto-routing-legacy` 允许任何 HTTP 方法访问控制器。
    以意外的方法访问控制器可能绕过过滤器。

HTML 表单
==========

如使用 :doc:`表单辅助函数 <../helpers/form_helper>`，
:func:`form_open()` 会自动在表单中插入隐藏的 csrf 字段。

.. note:: 要使用 CSRF 字段自动生成功能，需要为表单页面开启 CSRF 过滤器。
    大多数情况下该页面使用 ``GET`` 方法请求。

如未使用表单辅助函数，可使用始终可用的 ``csrf_token()`` 和 ``csrf_hash()`` 函数::

    <input type="hidden" name="<?= csrf_token() ?>" value="<?= csrf_hash() ?>" />

此外，可使用 ``csrf_field()`` 方法生成此隐藏 input 字段::

    // 生成：<input type="hidden" name="{csrf_token}" value="{csrf_hash}" />
    <?= csrf_field() ?>

发送 JSON 请求时，CSRF 令牌也可作为参数之一传递。
传递 CSRF 令牌的另一种方式是使用特殊 HTTP 标头，其名称可通过 ``csrf_header()`` 函数获取。

此外，可使用 ``csrf_meta()`` 方法生成 meta 标签::

    // 生成：<meta name="{csrf_header}" content="{csrf_hash}" />
    <?= csrf_meta() ?>

用户发送令牌的顺序
================================

检查 CSRF 令牌可用性的顺序如下：

1. ``$_POST`` 数组
2. HTTP 标头
3. ``php://input`` （JSON 请求）— 注意此方式最慢，因为需要解码 JSON 然后重新编码
4. ``php://input`` （原始 body）— 用于 PUT、PATCH 和 DELETE 类型请求

.. note:: 自 v4.4.2 起，会检查 ``php://input`` （原始 body）。

*********************
其他实用方法
*********************

大部分 Security 类方法无需直接使用。以下是一些与 CSRF 防护无关但可能有用的方法。

sanitizeFilename()
==================

尝试清理文件名以防止目录遍历尝试和其他安全威胁，
对通过用户输入提供的文件特别有用。第一个参数为要清理的路径。

如允许用户输入包含相对路径，例如 **file/in/some/approved/folder.txt**，可将第二个可选参数 ``$relativePath`` 设为 ``true``。

.. literalinclude:: security/010.php

此方法是 Security 辅助函数中 ``sanitize_filename()`` 函数的别名。
