升级视图解析器
###################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.x 模板解析器文档 <https://codeigniter.org.cn/userguide3/libraries/parser.html>`_
- :doc:`CodeIgniter 4.x 视图解析器文档 </outgoing/view_parser>`

变更内容
=====================
- 需要修改解析器类的实现方式和加载方式。
- 视图可以直接从 CI3 复制过来。通常不需要修改。

升级指南
=============
1. 凡是使用视图解析器类的地方，都将 ``$this->load->library('parser');`` 替换为 ``$parser = service('parser');``。
2. 需要将控制器中的渲染部分从 ``$this->parser->parse('blog_template', $data);`` 改为 ``return $parser->setData($data)->render('blog_template');``。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_view_parser/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_view_parser/001.php
