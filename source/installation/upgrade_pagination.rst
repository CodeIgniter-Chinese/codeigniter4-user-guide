升级分页
##################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.x 分页类文档 <https://codeigniter.org.cn/userguide3/libraries/pagination.html>`_
- :doc:`CodeIgniter 4.x 分页文档 </libraries/pagination>`

变更内容
=====================
- 要使用新的分页类，必须同时修改视图和控制器。
- 如果要自定义分页链接，则需要创建视图模板。
- 在 CI4 中，分页仅使用实际页码。不能再像 CI3 的默认行为那样，使用条目的起始索引（偏移量）。
- 如果使用 :doc:`CodeIgnite\\Model </models/model>`，则可以使用模型类中的内置方法。

升级指南
=============
1. 在视图中做如下修改：

    - 将 ``<?php echo $this->pagination->create_links(); ?>`` 改为 ``<?= $pager->links() ?>``

2. 在控制器中做如下修改：

    - 可以在任何模型上使用内置的 ``paginate()`` 方法。请参见下面的代码示例，了解如何在特定模型上设置分页。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_pagination/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_pagination/001.php
