升级视图解析器
###################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.x 模板解析器文档 <http://codeigniter.com/userguide3/libraries/parser.html>`_
- :doc:`CodeIgniter 4.x 视图解析器文档 </outgoing/view_parser>`

变更点
=====================
- 你必须更改解析器库的实现和加载方式。
- 视图可以从 CI3 复制。通常不需要对其进行任何更改。

升级指南
=============
1. 在使用视图解析器库的任何地方,用 ``$parser = service('parser');`` 替换 ``$this->load->library('parser');``。
2. 你必须将控制器中的渲染部分从 ``$this->parser->parse('blog_template', $data);`` 改为 ``return $parser->setData($data)->render('blog_template');``。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_view_parser/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_view_parser/001.php
