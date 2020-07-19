############
数组辅助函数
############

数组辅助函数提供几个不同函数去简易复杂数组的使用习惯。它并不是有意的复制任何一个确凿的PHP提供的功能 - 除非它过多的简化它们的使用方法。


.. contents::
    :local:

加载数组辅助函数
===================

该辅助函数被加载使用如下的代码::

	helper('array');

通用函数
===================

下面的函数是通用的:

..  php:function:: dot_array_search(string $search, array $values)

    :param  string  $search: 点表达式字符串描述如何搜索数组
    :param  array   $values: 所要搜索的数组
    :returns: 数组内创建的值，或者空值
    :rtype: 混合的

   这个方法允许你为了一个特殊的要诀使用点表达式通过数组去搜索并且允许使用通配符 '*'。指定下面的数组::

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

   我们能使用搜索字符串 "foo.buzz.fizz" 找出 'fizz' 的值。同样地，baz 的值也能从"foo.bar.baz"找到::

        // Returns: 11
        $fizz = dot_array_search('foo.buzz.fizz', $data);

        // Returns: 23
        $baz = dot_array_search('foo.bar.baz', $data);

   你能使用星号做为通配符去替换任何部分。当找到的时候，它将通过所有子目录搜索直到通配符找到它。
   如果你不知道值，或者如果你的值有一个数字的索引这个方法是很容易取得的::

        // Returns: 23
        $baz = dot_array_search('foo.*.baz', $data);
