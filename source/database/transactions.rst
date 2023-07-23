############
事务
############

CodeIgniter 的数据库抽象允许你对支持事务安全表类型的数据库使用事务。在 MySQL 中,你需要运行 InnoDB 或 BDB 表类型,而不是更常用的 MyISAM。大多数其他数据库平台本身就支持事务。

如果你不熟悉事务,我们建议你找到一个好的在线资源来学习有关你特定数据库的事务知识。下面的信息假设你已经对事务有了基本的了解。

.. contents::
    :local:
    :depth: 2

CodeIgniter 处理事务的方法
======================================

CodeIgniter 使用一种非常类似于流行数据库类 ADODB 的方法来处理事务。我们选择这种方法是因为它大大简化了运行事务的过程。在大多数情况下,只需要两行代码。

传统上,实现事务需要相当多的工作,因为它们要求你跟踪查询并根据查询的成功或失败决定是提交还是回滚。这在嵌套查询中特别麻烦。相比之下,我们实现了一个智能事务系统,可以为你自动完成所有这些工作(如果你愿意,也可以手动管理事务,但真的没有好处)。

.. note::
    从 v4.3.0 开始,在事务期间,即使 ``DBDebug`` 为 true,默认情况下也不会抛出异常。

运行事务
====================

要使用事务运行查询,你将使用 ``$this->db->transStart()`` 和 ``$this->db->transComplete()`` 方法,如下所示:

.. literalinclude:: transactions/001.php

你可以在 ``transStart()``/``transComplete()`` 方法之间运行任意数量的查询,它们都将根据任何给定查询的成功或失败全部提交或回滚。

严格模式
===========

默认情况下,CodeIgniter 以严格模式运行所有事务。启用严格模式时,如果你正在运行多个事务组,如果一个组失败,所有后续组都将回滚。如果禁用严格模式,每个组都是独立的,这意味着一个组的失败不会影响任何其他组。

可以如下禁用严格模式:

.. literalinclude:: transactions/002.php

.. _transactions-managing-errors:

管理错误
===============

当你在 **app/Config/Database.php** 文件中设置 ``DBDebug`` 为 true 时,如果查询错误发生,
所有查询都将回滚,并抛出异常。所以你会看到一个标准的错误页面。

如果 ``DBDebug`` 为 false,你可以像这样管理自己的错误:

.. literalinclude:: transactions/003.php

.. _transactions-throwing-exceptions:

抛出异常
===================

.. versionadded:: 4.3.0

.. note::
    从 v4.3.0 开始,在事务期间,即使 ``DBDebug`` 为 true,默认情况下也不会抛出异常。

如果在查询错误发生时想抛出异常,可以使用 ``$this->db->transException(true)``:

.. literalinclude:: transactions/008.php

如果发生查询错误,所有查询都将回滚,并抛出 ``DatabaseException``。

禁用事务
======================

事务默认启用。如果要禁用事务,可以使用 ``$this->db->transOff()``:

.. literalinclude:: transactions/004.php

当事务被禁用时,你的查询将自动提交,就像在不使用事务运行查询时一样。

测试模式
=========

你可以可选地将事务系统置于“测试模式”,这将导致你的查询被回滚 - 即使查询生成有效结果也是如此。要使用测试模式,只需在 ``$this->db->transStart()`` 方法的第一个参数中设置为 true:

.. literalinclude:: transactions/005.php

.. _transactions-manual-transactions:

手动运行事务
=============================

当你在 **app/Config/Database.php** 文件中设置 ``DBDebug`` 为 false 时,如果要手动运行事务,可以按如下方式执行:

.. literalinclude:: transactions/006.php

.. note:: 运行手动事务时,请使用 ``$this->db->transBegin()``, **而不是** ``$this->db->transStart()``。

嵌套事务
===================

在 CodeIgniter 中,事务可以以嵌套的方式嵌套,以便只执行最外层或顶层的事务命令。
你可以在事务块中包含任意数量的 ``transStart()``/``transComplete()`` 或 ``transBegin()``/``transCommit()``/``transRollback()`` 对,等等。
CodeIgniter 将跟踪事务“深度”,并且只在最外层(零深度)采取操作。

.. literalinclude:: transactions/007.php

.. note:: 如果结构远比这更复杂,则必须确保内部事务能够再次到达最外层,以便数据库可以完全执行它们,从而防止意外的提交/回滚。
