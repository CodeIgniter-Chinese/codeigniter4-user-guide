升级数据库
################

.. contents::
    :local:
    :depth: 2

文档
==============

- `CodeIgniter 3.X 数据库参考文档 <http://codeigniter.com/userguide3/database/index.html>`_
- :doc:`CodeIgniter 4.X 使用数据库文档 </database/index>`

变更点
=====================
- CI4 的功能基本与 CI3 相同。
- CI3 中已知的`数据库缓存 <https://www.codeigniter.com/userguide3/database/caching.html>`_ 功能已被删除。
- 方法名已更改为 camelCase 样式,并且在运行查询之前,现在需要初始化 :doc:`查询构建器 <../database/query_builder>`。

升级指南
=============
1. 将数据库凭据添加到 **app/Config/Database.php**。选项与 CI3 基本相同,只是一些名称略有变化。
2. 在使用数据库的任何地方,都必须用 ``$db = db_connect();`` 替换 ``$this->load->database();``。
3. 如果使用多个数据库,请使用以下代码加载其他数据库 ``$db = db_connect('group_name');``。
4. 现在必须更改所有数据库查询。这里最重要的变化是用 ``$db`` 替换 ``$this->db``,并调整方法名和 ``$db``。这里有一些例子:

    - ``$this->db->query('YOUR QUERY HERE');`` 改为 ``$db->query('YOUR QUERY HERE');``
    - ``$this->db->simple_query('YOUR QUERY')`` 改为 ``$db->simpleQuery('YOUR QUERY')``
    - ``$this->db->escape("something")`` 改为 ``$db->escape("something");``
    - ``$this->db->affected_rows();`` 改为 ``$db->affectedRows();``
    - ``$query->result();`` 改为 ``$query->getResult();``
    - ``$query->result_array();`` 改为 ``$query->getResultArray();``
    - ``echo $this->db->count_all('my_table');`` 改为 ``echo $db->table('my_table')->countAll();``

5. 要使用新的查询构建器类,必须在 ``$builder = $db->table('mytable');`` 之后初始化构建器,之后可以在 ``$builder`` 上运行查询。这里有一些例子:

    - ``$this->db->get()`` 改为 ``$builder->get();``
    - ``$this->db->get_where('mytable', array('id' => $id), $limit, $offset);`` 改为 ``$builder->getWhere(['id' => $id], $limit, $offset);``
    - ``$this->db->select('title, content, date');`` 改为 ``$builder->select('title, content, date');``
    - ``$this->db->select_max('age');`` 改为 ``$builder->selectMax('age');``
    - ``$this->db->join('comments', 'comments.id = blogs.id');`` 改为 ``$builder->join('comments', 'comments.id = blogs.id');``
    - ``$this->db->having('user_id',  45);`` 改为 ``$builder->having('user_id',  45);``
6. CI4 不提供 CI3 中已知的`数据库缓存 <https://www.codeigniter.com/userguide3/database/caching.html>`_
   层,所以如果需要缓存结果,请改用 :doc:`../libraries/caching`。

代码示例
============

CodeIgniter 3.x 版本
------------------------

.. literalinclude:: upgrade_database/ci3sample/001.php

CodeIgniter 4.x 版本
-----------------------

.. literalinclude:: upgrade_database/001.php
