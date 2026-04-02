升级 HTML 表格
###################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.x HTML 表格文档 <https://codeigniter.org.cn/userguide3/libraries/table.html>`_
- :doc:`CodeIgniter 4.x HTML 表格文档 </outgoing/table>`

变更内容
=====================
- 只改动了少量内容，例如方法名以及类的加载方式。

升级指南
=============
1. 在类中，将 ``$this->load->library('table');`` 改为 ``$table = new \CodeIgniter\View\Table();``。
2. 从这里开始，需要把每一行以 ``$this->table`` 开头的代码替换为 ``$table``。例如：``echo $this->table->generate($query);`` 会变为 ``echo $table->generate($query);``
3. HTML 表格类中的方法名可能略有不同。最重要的命名变化是由带下划线的方法名改为驼峰命名法。3.x 版本中的 ``set_heading()`` 现在名为 ``setHeading()``，其他方法也是如此。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_html_tables/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_html_tables/001.php
