升级 Session
################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.X Session 库文档 <http://codeigniter.com/userguide3/libraries/sessions.html>`_
- :doc:`CodeIgniter 4.X Session 库文档 </libraries/sessions>`

变更点
=====================

- 只是一些小变化,如方法名称和库的加载。
- 在数据库驱动中，Session 表的定义已经发生了变化。

升级指南
=============

1. 在使用 Session 库的任何地方,用 ``$session = session();`` 替换 ``$this->load->library('session');``。
2. 从那时起,必须用 ``$session`` 后跟新方法名替换以 ``$this->session`` 开头的每一行。

    - 要访问 Session 数据,请使用 ``$session->item`` 或 ``$session->get('item')`` 语法,而不是 CI3 语法 ``$this->session->name``。
    - 要设置数据,请使用 ``$session->set($array);`` 代替 ``$this->session->set_userdata($array);``。
    - 要删除数据,请使用 ``unset($_SESSION['some_name']);`` 或 ``$session->remove('some_name');`` 代替 ``$this->session->unset_userdata('some_name');``。
    - 要将 Session 数据标记为只在下一个请求中可用的闪存数据,请使用 ``$session->markAsFlashdata('item');`` 代替 ``$this->session->mark_as_flash('item');```
3. 如果你使用数据库驱动，你需要重新创建 Session 表。参见 :ref:`sessions-databasehandler-driver`。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_sessions/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_sessions/001.php
