升级 HTML 表格
###################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.X HTML表格文档 <http://codeigniter.com/userguide3/libraries/table.html>`_
- :doc:`CodeIgniter 4.X HTML表格文档 </outgoing/table>`

变更点
=====================
- 只是一些小变化,如方法名称和库的加载。

升级指南
=============
1. 在类中,将 ``$this->load->library('table');`` 改为 ``$table = new \CodeIgniter\View\Table();``。
2. 从那时起,需要将以 ``$this->table`` 开头的每一行改为 ``$table``。例如:``echo $this->table->generate($query);`` 会变成 ``echo $table->generate($query);``
3. HTML 表格类中的方法可能命名稍有不同。最重要的命名变化是从下划线方法名切换到 camelCase。版本 3 中的方法 ``set_heading()`` 现在命名为 ``setHeading()``,等等。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_html_tables/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_html_tables/001.php
