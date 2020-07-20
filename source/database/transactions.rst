############
事务
############

CodeIgniter 的数据库抽象类允许你将事务和支持事务安全表类型的数据库一起使用。
在 MySQL 中，你需要将表设置为 InnoDB 或者 BDB 类型，
而不是更常见的 MyISAM。大多数的数据库本身支持事务。

如果你不熟悉事务，我们建议找个好的在线资源学习下，了解你正用的数据库。
以下的信息假定你对事务有基本的了解。

CodeIgniter 的事务方法
======================================

CodeIgniter 采用一种与流行的 ADODB 数据库类很相似的方式处理事务。
我们选用这种方法因为它极大地简化了运行事务的过程。
在大多数情况下，所需要的只是两行代码。

传统的事务需要相当多的工序才能实现，因为它要求你跟踪查询并根据查询的成功或失败来决定提交
还是回滚，这在嵌套查询时尤为麻烦。相比之下，我们已经实现了一个智能事务系统，可以自动为你
完成这些工作（如果你想要手动管理你的事务也可以，但这实际上没有任何好处）。

运行事务
====================

要使用事务运行查询，你将使用 $this->db->transStart() 
和 $this->db->transComplete() 方法，如下所示::

	$this->db->transStart();
	$this->db->query('AN SQL QUERY...');
	$this->db->query('ANOTHER QUERY...');
	$this->db->query('AND YET ANOTHER QUERY...');
	$this->db->transComplete();

你可以在启动/完成方法之间运行任意多的查询，并且根据任何给定查询的成功或失败结果，
他们都能被提交或回滚。

严格模式
===========

默认情况下，CodeIgniter 以严格模式运行所有事务。
启用严格模式时，如果你正在运行多组事务，假如一个组失败，所有组都将被回滚。
如果禁用严格模式，则会独立处理每个组，这意味着一个组的失败不会影响其他组。

可以按如下方式禁用严格模式::

	$this->db->transStrict(false);

错误处理
===============

如果在 Config / Database.php 文件中启用了错误报告，在提交失败时会看到标准错误消息。
如果关闭调试，你可以像下面这样处理自己的错误::

	$this->db->transStart();
	$this->db->query('AN SQL QUERY...');
	$this->db->query('ANOTHER QUERY...');
	$this->db->transComplete();

	if ($this->db->transStatus() === FALSE)
	{
		// 生成错误...或使用 log_message() 函数记录错误
	}

禁用事务
=====================

事务功能是默认开启的，如果要禁用事务，可以执行 $this->db->transOff() 操作::

	$this->db->transOff();

	$this->db->transStart();
	$this->db->query('AN SQL QUERY...');
	$this->db->transComplete();

禁用事务时，你的查询将自动提交，就像平时没事务那样的执行查询。

测试模式
=========

你可以选择将事务系统置于 "测试模式" ，这将导致你的查询被回滚 -- 
即使查询产生有效结果。要使用测试模式，只需将 $this->db->transStart() 方法的第一个参数设置为 TRUE::

	$this->db->transStart(true); // 查询将被回滚
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

.. 注解:: 确保在手动运行事务时使用 $this->db->transBegin()，
    **而不是** $this->db->transStart()。
