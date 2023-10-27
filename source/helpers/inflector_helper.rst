####################
Inflector 辅助函数
####################

Inflector 辅助函数文件包含了允许你将 **英语** 单词更改为复数、单数、驼峰式等的函数。

.. contents::
    :local:
    :depth: 2

加载此辅助函数
===================

使用以下代码加载此辅助函数:

.. literalinclude:: inflector_helper/001.php

可用函数
===================

以下函数可用:

.. php:function:: singular($string)

    :param    string    $string: 输入字符串
    :returns:    单数词
    :rtype:    string

    将复数词变为单数。示例:

    .. literalinclude:: inflector_helper/002.php

.. php:function:: plural($string)

    :param    string    $string: 输入字符串
    :returns:    复数词
    :rtype:    string

    将单数词变为复数。示例:

    .. literalinclude:: inflector_helper/003.php

.. php:function:: counted($count, $string)

    :param    int     $count:  项目数量
    :param    string    $string: 输入字符串
    :returns:    单数或复数短语
    :rtype:    string

    将词及其计数更改为短语。示例:

    .. literalinclude:: inflector_helper/004.php

.. php:function:: camelize($string)

    :param    string    $string: 输入字符串
    :returns:    驼峰字符串
    :rtype:    string

    将由空格或下划线分隔的词字符串更改为驼峰式。示例:

    .. literalinclude:: inflector_helper/005.php

.. php:function:: pascalize($string)

    :param    string    $string: 输入字符串
    :returns:    帕斯卡式字符串
    :rtype:    string

    将由空格或下划线分隔的词字符串更改为帕斯卡式,即首字母大写的驼峰式。示例:

    .. literalinclude:: inflector_helper/006.php

.. php:function:: underscore($string)

    :param    string    $string: 输入字符串
    :returns:    包含下划线而不是空格的字符串
    :rtype:    string

    获取多个由空格分隔的词并在其下添加下划线。示例:

    .. literalinclude:: inflector_helper/007.php

.. php:function:: decamelize($string)

    :param    string    $string: 输入字符串
    :returns:    在词中间包含下划线的字符串
    :rtype:    string

    获取多个驼峰或帕斯卡单词并将它们转换为下划线分隔的单词。示例:

    .. literalinclude:: inflector_helper/014.php

.. php:function:: humanize($string[, $separator = '_'])

    :param    string    $string: 输入字符串
    :param    string    $separator: 输入分隔符
    :returns:    人性化字符串
    :rtype:    string

    获取多个由下划线分隔的词并在它们之间添加空格。每个单词的首字母大写。

    示例:

    .. literalinclude:: inflector_helper/008.php

    要使用破折号代替下划线:

    .. literalinclude:: inflector_helper/009.php

.. php:function:: is_pluralizable($word)

    :param    string    $word: 输入字符串
    :returns:    如果单词可数则为 true,如果不可数则为 false
    :rtype:    bool

    检查给定单词是否有复数形式。示例:

    .. literalinclude:: inflector_helper/010.php

.. php:function:: dasherize($string)

    :param    string    $string: 输入字符串
    :returns:    短划线字符串
    :rtype:    string

    用破折号替换字符串中的下划线。示例:

    .. literalinclude:: inflector_helper/011.php

.. php:function:: ordinal($integer)

    :param    int    $integer: 确定后缀的整数
    :returns:    序数后缀
    :rtype:    string

    返回应添加到数字以表示位置的后缀,例如 1st、2nd、3rd、4th。示例:

    .. literalinclude:: inflector_helper/012.php

.. php:function:: ordinalize($integer)

    :param    int    $integer: 要转为序数的整数
    :returns:    序数整数
    :rtype:    string

    将数字转换为用于表示位置的序数字符串,如 1st、2nd、3rd、4th。示例:

    .. literalinclude:: inflector_helper/013.php
