升级安全
################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.x 安全类文档 <https://codeigniter.org.cn/userguide3/libraries/security.html>`_
- :doc:`CodeIgniter 4.x 安全文档 </libraries/security>`

.. note::
    如果使用 :doc:`../helpers/form_helper` 并全局启用了 CSRF 过滤器，那么 :php:func:`form_open()` 会自动在表单中插入一个隐藏的 CSRF 字段。因此，不需要手动升级这部分。

变更内容
=====================
- 在 HTML 表单中实现 CSRF 令牌的方法已发生变化。

升级指南
=============
1. 要在 CI4 中启用 CSRF 保护，必须在 **app/Config/Filters.php** 中启用它：

   .. literalinclude:: upgrade_security/001.php

2. 在 HTML 表单中，必须移除 CSRF input 字段。它看起来类似于 ``<input type="hidden" name="<?= $csrf['name'] ?>" value="<?= $csrf['hash'] ?>" />``。
3. 现在，在 HTML 表单中，必须在表单主体的某处添加 ``<?= csrf_field() ?>``，除非使用的是 ``form_open()``。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_security/ci3sample/002.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_security/002.php
