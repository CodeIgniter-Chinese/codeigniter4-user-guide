升级 HTTP 响应
######################

.. contents::
    :local:
    :depth: 2

文档
==============
- `CodeIgniter 3.X 输出类文档 <http://codeigniter.com/userguide3/libraries/output.html>`_
- :doc:`CodeIgniter 4.X HTTP 响应文档 </outgoing/response>`

变更点
=====================
- 方法已被重命名

升级指南
=============
1. HTTP 响应类中的方法命名略有不同。最重要的命名变化是从下划线方法名切换到 camelCase。版本 3 中的方法 ``set_content_type()`` 现在命名为 ``setContentType()``,等等。
2. 在大多数情况下,你需要将 ``$this->output`` 改为 ``$this->response`` 后跟方法。可以在 :doc:`../outgoing/response` 中找到所有方法。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_responses/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_responses/001.php
