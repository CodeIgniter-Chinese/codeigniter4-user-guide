升级 Session
################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.x Session 类文档 <https://codeigniter.org.cn/userguide3/libraries/sessions.html>`_
- :doc:`CodeIgniter 4.x Session 类文档 </libraries/sessions>`

变更内容
=====================
- 只变更了少量内容，例如方法名和类的加载方式。
- 数据库驱动中 session 表的定义已变更。

升级指南
=============
1. 凡是使用 Session 类的地方，都将 ``$this->load->library('session');`` 替换为 ``$session = session();``。
2. 从这里开始，凡是以 ``$this->session`` 开头的每一行，都要替换为 ``$session``，并使用新的方法名。

    - 访问 session 数据时，使用 ``$session->item`` 或 ``$session->get('item')``，而不要使用 CI3 的语法 ``$this->session->name``。
    - 设置数据时，使用 ``$session->set($array);``，而不要使用 ``$this->session->set_userdata($array);``。
    - 移除数据时，使用 ``unset($_SESSION['some_name']);`` 或 ``$session->remove('some_name');``，而不要使用 ``$this->session->unset_userdata('some_name');``。
    - 将 session 数据标记为 flashdata 时（它只会在下一次请求中可用），使用 ``$session->markAsFlashdata('item');``，而不要使用 ``$this->session->mark_as_flash('item');``。
3. 如果使用数据库驱动，则需要重新创建 session 表。参见 :ref:`sessions-databasehandler-driver`。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_sessions/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_sessions/001.php
