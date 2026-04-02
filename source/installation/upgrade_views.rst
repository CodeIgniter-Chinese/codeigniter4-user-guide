升级视图
#############

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.x 视图文档 <https://codeigniter.org.cn/userguide3/general/views.html>`_
- :doc:`CodeIgniter 4.x 视图文档 </outgoing/views>`

变更内容
=====================

- 视图的写法与之前基本相同，但调用方式不同。CI3 使用
  ``$this->load->view('x');``，现在可以改用 ``return view('x');``。
- CI4 支持 :doc:`../outgoing/view_cells`，可将响应拆分为多个部分来构建；
  也支持 :doc:`../outgoing/view_layouts`，用于页面布局。
- :doc:`模板解析器 <../outgoing/view_parser>` 仍然可用，而且增强了很多。

升级指南
=============

1. 首先，将所有视图移动到 **app/Views** 目录。
2. 在所有加载视图的脚本中，修改视图的加载语法：

    - 将 ``$this->load->view('directory_name/file_name')`` 改为 ``return view('directory_name/file_name');``
    - 将 ``$content = $this->load->view('file', $data, TRUE);`` 改为 ``$content = view('file', $data);``

3. （可选）可以将视图中的 echo 语法从 ``<?php echo $title; ?>`` 改为 ``<?= $title ?>``。
4. 如果存在，删除 ``defined('BASEPATH') OR exit('No direct script access allowed');`` 这一行。

代码示例
============

CodeIgniter 3.x 版本
------------------------

路径：**application/views**：

.. literalinclude:: upgrade_views/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

路径：**app/Views**：

.. literalinclude:: upgrade_views/001.php
