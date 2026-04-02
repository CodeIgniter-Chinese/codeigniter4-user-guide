升级输出类
####################

.. contents::
    :local:
    :depth: 2

文档
==============
- `CodeIgniter 3.x 输出类文档 <https://codeigniter.org.cn/userguide3/libraries/output.html>`_
- :doc:`CodeIgniter 4.x HTTP 响应文档 </outgoing/response>`

变更内容
=====================
- 输出类已更改为 Response 类。
- 方法名已重命名。

升级指南
=============
1. HTTP Response 类中的方法名略有不同。最重要的命名变化，是从下划线命名法切换为小驼峰命名法。例如，版本 3 中的 ``set_content_type()`` 方法现在名为 ``setContentType()``，其他方法也同样如此。
2. 大多数情况下，需要将 ``$this->output`` 改为 ``$this->response``，然后调用相应的方法。你可以在 :doc:`../outgoing/response` 中找到所有方法。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_responses/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_responses/001.php
