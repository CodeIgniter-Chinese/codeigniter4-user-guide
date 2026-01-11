###############
数据库事件
###############

数据库类包含一些 :doc:`事件 </extending/events>`，你可以利用这些事件来了解数据库执行过程中的详细情况。这些事件可用于收集数据分析和生成报告。:doc:`调试工具栏 </testing/debugging>` 就是利用这些事件来收集查询信息并显示在工具栏中。

.. contents::
    :local:
    :depth: 2

**********
事件
**********

.. _database-events-dbquery:

DBQuery
=======

每当执行一个新查询（无论成功与否）时，都会触发此事件。该事件唯一的参数是当前查询的 :doc:`Query </database/queries>` 实例。

你可以利用此事件将所有查询输出到 STDOUT，或记录到文件中，甚至创建工具进行自动查询分析，以帮助你发现可能缺少的索引、慢查询等问题。

记录所有查询的示例：

.. literalinclude:: events/001.php
