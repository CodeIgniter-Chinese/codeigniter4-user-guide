###############
数据库事件
###############

数据库类包括着一些你可以用来了解关于数据库执行过程的 :doc:`事件 </extending/events>` 相关的内容。
这些事件可以用来收集数据以供分析和报告。:doc:`Debug 工具条 </testing/debugging>` 类使用了这一特性来收集用于工具条中展示的语句。

==========
事件
==========

**DBQuery**

该事件会在一个新的语句运行完毕时，无论成功与否，都会触发。唯一的参数就是一个当前语句的 :doc:`Query </database/queries>`实例。
你可以使用该方法在标准输出流，日志文件中输出所有的查询语句。甚至可以使用工具来进行自动化的语句分析来监测可能会出现的索引丢失，慢查询等情况。可行的用例如下::

    // 在Config\Events.php文件中
    Events::on('DBQuery', 'CodeIgniter\Debug\Toolbar\Collectors\Database::collect');

    // 收集所有的查询语句以备后来所需
    public static function collect(CodeIgniter\Database\Query $query)
    {
        static::$queries[] = $query;
    }
