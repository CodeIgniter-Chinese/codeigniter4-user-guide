############
事务
############

CodeIgniter 的数据库抽象类，允许你将事务和支持事务安全表类型的数据库一起使用。在 MySQL 中，你需要将表设置为 InnoDB 或者 BDB 类型，
而不是更常见的 MyISAM。大多数的数据库本身支持事务。

如果你不熟悉事务，我们建议你找到一个很好的在线资源，以了解你使用的数据库。以下的信息假定你对事务有基本的了解

CodeIgniter 的事务方法
======================================
CodeIgniter 使用的方法与流行的数据库类 ADODB 使用的流程非常相似。我们选择了这种方法，因为它极大地简化了运行事务的过程。
在大多数情况下，所需要的只是两行代码。

传统上的事务需要相当多的工作才能实现，因为它们要求你跟踪查询并根据查询的成功或失败来确定是提交还是回滚。
嵌套查询这一点特别麻烦。相比之下，我们已经实施了一个智能事务系统，可以自动为你完成所有这些（如果你选择，
你也可以手动管理你的事务，但实际上没有任何好处）。

运行事务
====================

要使用事务运行查询，你将使用 $this->db->transStart() 和 $this->db->transComplete() 函数，如下所示::

	$this->db->transStart();
	$this->db->query('AN SQL QUERY...');
	$this->db->query('ANOTHER QUERY...');
	$this->db->query('AND YET ANOTHER QUERY...');
	$this->db->transComplete();

你可以在启动/完成功能之间运行任意数量的查询，并且它们将根据任何给定查询的成功或失败提交或回滚。

严格模式
===========

默认情况下，CodeIgniter 以严格模式运行所有事务。启用严格模式时，如果你正在运行多组事务，则如果一个组失败，则将回滚所有组。如果禁用严格模式，则会独立处理每个组，这意味着一个组的故障不会影响任何其他组。

可以按如下方式禁用严格模式::

	$this->db->transStrict(false);

管理错误
===============

如果在 Config / Database.php 文件中启用了错误报告，则在提交失败时会看到标准错误消息。如果关闭调试，你可以像下面这样管理自己的错误::

	$this->db->transStart();
	$this->db->query('AN SQL QUERY...');
	$this->db->query('ANOTHER QUERY...');
	$this->db->transComplete();

	if ($this->db->transStatus() === FALSE)
	{
		// 生成错误...或使用 log_message() 函数记录错误
	}

启用事务
=====================
使用 $this->db->transStart() 时，会自动启用事务。如果要禁用事务，可以使用 $this->db->transOff() 来执行此操作::

	$this->db->transOff();

	$this->db->trans_Start();
	$this->db->query('AN SQL QUERY...');
	$this->db->transComplete();

禁用事务时，你的查询将自动提交，就像在没有事务的情况下运行查询时一样。

测试模式
=========

你可以选择将事务系统置于“测试模式”，这将导致你的查询被回滚 - 即使查询产生有效结果。要使用测试模式，只需将 $this->db->transStart() 函数中的第一个参数设置为 TRUE::

	$this->db->transStart(true); // 查询将回滚
	$this->db->query('AN SQL QUERY...');
	$this->db->transComplete();

手动运行事务
=============================

如果你想手动运行事务，可以按如下方式执行::

	$this->db->transBegin();

	$this->db->query('AN SQL QUERY...');
	$this->db->query('ANOTHER QUERY...');
	$this->db->query('AND YET ANOTHER QUERY...');

	if ($this->db->transStatus() === FALSE)
	{
		$this->db->transRollback();
	}
	else
	{
		$this->db->transCommit();
	}

.. note:: 确保在运行手动事务时使用 $this->db->transBegin(), **而不是** $this->db->transStart().
