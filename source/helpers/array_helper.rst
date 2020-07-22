############
数组辅助函数
############

数组辅助函数提供几个函数去精简复杂数组的使用习惯。它并不是故意的复制任何一个现存的PHP提供的功能 - 除非它极大的简化它们的用法。


.. contents::
    :local:

加载数组辅助函数
===================


该辅助函数使用如下的代码加载::

	helper('array');

通用函数
===================

下面的函数是通用的:


..  php:function:: dot_array_search(string $search, array $values)

    :param  string  $search: 点表达式字符串描写如何去搜索数组
    :param  array   $values: 在数组中搜寻
    :returns: 数组内创建的值，或者空值
    :rtype: 混合的类型


    这个方法允许你为一个特殊要诀使用点表达式通过一组数组去搜索并且允许使用通配符 '*'.   参考接下来的数组::
    
        $data = [
            'foo' => [
                'buzz' => [
                    'fizz' => 11
                ],
                'bar' => [
                    'baz' => 23
                ]
            ]
        ]

 
    我们能通过使用字符串搜索 "foo.buzz.fizz" 找出 'fizz' 的值。同样地，baz 的值也能从 "foo.bar.baz" 找到::

        // Returns: 11
        $fizz = dot_array_search('foo.buzz.fizz', $data);

        // Returns: 23
        $baz = dot_array_search('foo.bar.baz', $data);

 
    你能使用星号做为通配符去替换任何部分。当找到字符串的时候，它会通过所有子节点搜索直到字符串搜索找到它。
    如果你不知道值，或者如果你获得的值有一个数字索引这个方法是很便利的::

        // Returns: 23
        $baz = dot_array_search('foo.*.baz', $data);
