升级视图
#############

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.X 视图文档 <http://codeigniter.com/userguide3/general/views.html>`_
- :doc:`CodeIgniter 4.X 视图文档 </outgoing/views>`

变更点
=====================

- 你的视图看起来与以前基本相似,但是调用它们的方式不同......不是 CI3 的
  ``$this->load->view('x');``,可以使用 ``return view('x');``。
- CI4 支持 :doc:`../outgoing/view_cells` 来分段构建响应,
  和 :doc:`../outgoing/view_layouts` 用于页面布局。
- :doc:`模板解析器 <../outgoing/view_parser>` 仍然存在,并得到实质性增强。

升级指南
=============

1. 首先,将所有视图移动到 **app/Views** 文件夹
2. 在每个加载视图的脚本中更改视图加载语法:
    - 从 ``$this->load->view('directory_name/file_name')`` 到 ``return view('directory_name/file_name');``
    - 从 ``$content = $this->load->view('file', $data, TRUE);`` 到 ``$content = view('file', $data);``
3. (可选)可以将视图中的 echo 语法从 ``<?php echo $title; ?>`` 更改为 ``<?= $title ?>``
4. 如果存在,请删除 ``defined('BASEPATH') OR exit('No direct script access allowed');`` 这一行。

代码示例
============

CodeIgniter 3.x 版本
------------------------

路径:**application/views**:

.. literalinclude:: upgrade_views/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

路径:**app/Views**:

.. literalinclude:: upgrade_views/001.php
