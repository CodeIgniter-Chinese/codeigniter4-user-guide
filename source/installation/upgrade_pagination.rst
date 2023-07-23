升级分页
##################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.X 分页类文档 <http://codeigniter.com/userguide3/libraries/pagination.html>`_
- :doc:`CodeIgniter 4.X 分页文档 </libraries/pagination>`

变更点
=====================
- 你需要更改视图和控制器以使用新的分页库。
- 如果要自定义分页链接,需要创建视图模板。
- 在 CI4 中,分页只使用实际的页码。你无法使用 CI3 默认的项目起始索引(偏移量)。
- 如果使用 :doc:`CodeIgnite\\Model </models/model>`,可以使用 Model 类中的内置方法。

升级指南
=============
1. 在视图中进行以下更改:

    - ``<?php echo $this->pagination->create_links(); ?>`` 改为 ``<?= $pager->links() ?>``

2. 在控制器中需要做以下更改:

    - 你可以在每个 Model 上使用内置的 ``paginate()`` 方法。请参阅下面的代码示例,看看如何在特定模型上设置分页。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_pagination/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_pagination/001.php
