升级安全性
################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.x 安全类文档 <http://codeigniter.com/userguide3/libraries/security.html>`_
- :doc:`CodeIgniter 4.x 安全性文档 </libraries/security>`

.. note::
    如果使用 :doc:`../helpers/form_helper` 并全局启用 CSRF 过滤器,那么 :php:func:`form_open()` 将自动在表单中插入隐藏的 CSRF 字段。所以你不需要自行升级这个。

变更点
=====================
- 实现 CSRF 令牌到 HTML 表单的方法已经更改。

升级指南
=============
1. 要在 CI4 中启用 CSRF 保护,必须在 **app/Config/Filters.php** 中启用它:

   .. literalinclude:: upgrade_security/001.php

2. 在 HTML 表单中,必须删除类似 ``<input type="hidden" name="<?= $csrf['name'] ?>" value="<?= $csrf['hash'] ?>" />`` 的 CSRF 输入字段。
3. 现在,在 HTML 表单中,必须在表单主体的某处添加 ``<?= csrf_field() ?>``,除非使用 ``form_open()``。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_security/ci3sample/002.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_security/002.php
