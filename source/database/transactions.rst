############
事务
############

CodeIgniter 的数据库抽象层允许你在支持事务安全表类型的数据库中使用事务。在 MySQL 中，你需要使用 InnoDB 或 BDB 表类型，而不是更常见的 MyISAM。大多数其他数据库平台原生支持事务。

如果你不熟悉事务，我们建议你寻找适合你所用数据库的优质在线资源进行学习。以下内容假定你已经具备事务的基本理解。

.. contents::
    :local:
    :depth: 3

CodeIgniter 的事务处理方式
======================================

CodeIgniter 采用的事务处理方法与流行的数据库类库 ADODB 的处理过程非常相似。我们选择这种方法是因为它能极大简化事务的执行流程。在大多数情况下，你只需要两行代码即可完成操作。

传统的事务实现需要大量额外工作，因为需要跟踪所有查询并根据查询的成功与否决定提交或回滚。这在处理嵌套查询时尤为繁琐。相比之下，我们实现了一个智能事务系统，可以自动为你完成所有这些工作（你也可以选择手动管理事务，但实际上这样做没有任何优势）。

.. note::
    自 v4.3.0 起，在事务过程中，即使 ``DBDebug`` 设为 true，默认也不会抛出异常。

运行事务
====================

要通过事务执行查询，需使用 ``$this->db->transStart()`` 和 ``$this->db->transComplete()`` 方法，如下所示：

.. literalinclude:: transactions/001.php

你可以在 ``transStart()``/``transComplete()`` 方法之间运行任意数量的查询，系统将根据这些查询的整体成功或失败情况决定提交或回滚。

严格模式
===========

默认情况下，CodeIgniter 在严格模式下运行所有事务。

当启用严格模式时，如果运行多个事务组，其中一个组失败会导致所有后续组被回滚。

如果禁用严格模式，每个组将被独立处理，意味着一个组的失败不会影响其他组。

可以通过以下方式禁用严格模式：

.. literalinclude:: transactions/002.php

.. _transactions-resetting-transaction-status:

重置事务状态
----------------------------

.. versionadded:: 4.6.0

当启用严格模式时，如果某个事务失败，所有后续事务将被回滚。

若要在失败后重新启动事务，可以重置事务状态：

.. literalinclude:: transactions/009.php

.. _transactions-managing-errors:

错误处理
===============

.. note::
    自 v4.3.0 起，在事务过程中，即使 ``DBDebug`` 设为 true，默认也不会抛出异常。

你可以通过以下方式自行处理错误：

.. literalinclude:: transactions/003.php

.. _transactions-throwing-exceptions:

抛出异常
===================

.. versionadded:: 4.3.0

.. note::
    自 v4.3.0 起，在事务过程中，即使 ``DBDebug`` 设为 true，默认也不会抛出异常。

若要在查询出错时抛出异常，可以使用 ``$this->db->transException(true)``：

.. literalinclude:: transactions/008.php

如果发生查询错误，所有查询将被回滚，并抛出 ``DatabaseException`` 异常。

禁用事务
======================

事务功能默认启用。可以通过 ``$this->db->transOff()`` 禁用事务：

.. literalinclude:: transactions/004.php

禁用事务后，查询将自动提交，就像在没有使用事务的情况下运行查询一样。

测试模式
===========

你可以选择将事务系统置于「测试模式」，此模式下即使查询有效也会被回滚。要启用测试模式，只需将 ``$this->db->transStart()`` 方法的第一个参数设为 true：

.. literalinclude:: transactions/005.php

.. _transactions-manual-transactions:

手动运行事务
=============================

当在 **app/Config/Database.php** 文件中将 ``DBDebug`` 设为 false 时，可以通过以下方式手动运行事务：

.. literalinclude:: transactions/006.php

.. note:: 手动运行事务时请确保使用 ``$this->db->transBegin()``，**不要** 使用 ``$this->db->transStart()``。

嵌套事务
===================

在 CodeIgniter 中，事务可以嵌套执行，只有最外层（顶级）的事务命令会被真正执行。你可以在事务块中包含任意数量的 ``transStart()``/``transComplete()`` 或 ``transBegin()``/``transCommit()``/``transRollback()`` 组合。CodeIgniter 会跟踪事务的「深度」，并仅在最外层（零深度）执行实际操作。

.. literalinclude:: transactions/007.php

.. note:: 如果事务结构非常复杂，你需要确保内部事务能够再次到达最外层，以便数据库完整执行这些操作，从而避免意外的提交/回滚。
