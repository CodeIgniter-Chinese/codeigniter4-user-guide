###############
数据库事件
###############

数据库类包含几个可以利用的 :doc:`事件 </extending/events>`,以了解数据库执行期间发生的更多信息。这些事件可用于收集数据以进行分析和报告。 :doc:`调试工具栏 </testing/debugging>` 使用此操作来收集在工具栏中显示的查询。

.. contents::
    :local:
    :depth: 2

**********
事件
**********

.. _database-events-dbquery:

DBQuery
=======

此事件在每次运行新查询时触发，无论成功与否。唯一的参数是当前查询的 :doc:`Query </database/queries>` 实例。

你可以使用此事件将所有查询显示在 STDOUT，或记录到文件，甚至创建工具进行自动查询分析，以帮助你发现潜在的缺失索引、慢查询等。

记录所有查询的示例：

.. literalinclude:: events/001.php
