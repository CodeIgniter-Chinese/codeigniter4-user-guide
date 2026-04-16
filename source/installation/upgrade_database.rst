升级数据库
################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.x 数据库参考文档 <https://codeigniter.org.cn/userguide3/database/index.html>`_
- :doc:`CodeIgniter 4.x 数据库操作文档 </database/index>`

变更内容
=====================
- CI4 的功能基本与 CI3 相同。
- CI3 中的 `数据库缓存 <https://codeigniter.org.cn/userguide3/database/caching.html>`_ 功能已被移除。
- 方法名改为小驼峰命名规则，并且 :doc:`查询构建器 <../database/query_builder>` 现在需要初始化后才能执行查询。

升级指南
=============
1. 将数据库凭证添加到 **app/Config/Database.php**。选项基本与 CI3 相同，仅部分名称略有调整。
2. 所有使用数据库的地方，将 ``$this->load->database();`` 替换为 ``$db = db_connect();``。
3. 如果使用多个数据库，可使用以下代码加载附加数据库：``$db = db_connect('group_name');``。
4. 现在必须修改所有数据库查询。最重要的更改是将 ``$this->db`` 替换为 ``$db``，并调整方法名。示例：

    - ``$this->db->query('YOUR QUERY HERE');`` 改为 ``$db->query('YOUR QUERY HERE');``
    - ``$this->db->simple_query('YOUR QUERY')`` 改为 ``$db->simpleQuery('YOUR QUERY')``
    - ``$this->db->escape("something")`` 改为 ``$db->escape("something");``
    - ``$this->db->affected_rows();`` 改为 ``$db->affectedRows();``
    - ``$query->result();`` 改为 ``$query->getResult();``
    - ``$query->result_array();`` 改为 ``$query->getResultArray();``
    - ``echo $this->db->count_all('my_table');`` 改为 ``echo $db->table('my_table')->countAll();``

5. 使用新的查询构建器类时，需要先初始化构建器 ``$builder = $db->table('mytable');``，之后可在 ``$builder`` 上执行查询。示例：

    - ``$this->db->get()`` 改为 ``$builder->get();``
    - ``$this->db->get_where('mytable', array('id' => $id), $limit, $offset);`` 改为 ``$builder->getWhere(['id' => $id], $limit, $offset);``
    - ``$this->db->select('title, content, date');`` 改为 ``$builder->select('title, content, date');``
    - ``$this->db->select_max('age');`` 改为 ``$builder->selectMax('age');``
    - ``$this->db->join('comments', 'comments.id = blogs.id');`` 改为 ``$builder->join('comments', 'comments.id = blogs.id');``
    - ``$this->db->having('user_id',  45);`` 改为 ``$builder->having('user_id',  45);``

6. CI4 不再提供 CI3 中的 `数据库缓存 <https://codeigniter.org.cn/userguide3/database/caching.html>`_ 层，如果需要缓存结果，请使用 :doc:`../libraries/caching`。
7. 如果在查询构建器中使用 ``limit(0)``，CI4 会返回所有记录而非空记录（CI3 的 bug 修复）。自 v4.5.0 起，可通过设置修改此行为。详细信息参见 :ref:`v450-query-builder-limit-0-behavior`。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_database/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_database/001.php
