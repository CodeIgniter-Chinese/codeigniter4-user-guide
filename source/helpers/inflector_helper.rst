##################
Inflector 辅助函数
##################

Inflector 辅助函数文件包含了一系列函数，可用于将 **英文** 单词转换为复数、单数、驼峰命名法等形式。

.. contents::
    :local:
    :depth: 2

加载此辅助函数
===================

使用以下代码加载此辅助函数：

.. literalinclude:: inflector_helper/001.php

可用函数
===================

提供以下函数：

.. php:function:: singular($string)

    :param    string    $string: 输入字符串
    :returns:    单数形式的单词
    :rtype:    string

    将复数单词更改为单数形式。示例：

    .. literalinclude:: inflector_helper/002.php

.. php:function:: plural($string)

    :param    string    $string: 输入字符串
    :returns:    复数形式的单词
    :rtype:    string

    将单数单词更改为复数形式。示例：

    .. literalinclude:: inflector_helper/003.php

.. php:function:: counted($count, $string)

    :param    int     $count:  项目数量
    :param    string    $string: 输入字符串
    :returns:    单数或复数形式的短语
    :rtype:    string

    将单词及其数量转换为短语。示例：

    .. literalinclude:: inflector_helper/004.php

.. php:function:: camelize($string)

    :param    string    $string: 输入字符串
    :returns:    驼峰命名法的字符串
    :rtype:    string

    将由空格或下划线分隔的单词字符串转换为驼峰命名法。示例：

    .. literalinclude:: inflector_helper/005.php

.. php:function:: pascalize($string)

    :param    string    $string: 输入字符串
    :returns:    Pascal 命名法的字符串
    :rtype:    string

    将由空格或下划线分隔的单词字符串转换为 Pascal 命名法，
    即首字母大写的驼峰命名法。示例：

    .. literalinclude:: inflector_helper/006.php

.. php:function:: underscore($string)

    :param    string    $string: 输入字符串
    :returns:    包含下划线而不是空格的字符串
    :rtype:    string

    接受由空格分隔的多个单词并用下划线连接它们。
    示例：

    .. literalinclude:: inflector_helper/007.php

.. php:function:: decamelize($string)

    :param    string    $string: 输入字符串
    :returns:    单词间包含下划线的字符串
    :rtype:    string

    接受 camelCase 或 PascalCase 格式的多个单词并将它们转换为 snake_case 格式。
    示例：

    .. literalinclude:: inflector_helper/014.php

.. php:function:: humanize($string[, $separator = '_'])

    :param    string    $string: 输入字符串
    :param    string    $separator: 输入分隔符
    :returns:    人性化格式的字符串
    :rtype:    string

    接受由下划线分隔的多个单词并在它们之间添加空格。
    每个单词首字母大写。

    示例：

    .. literalinclude:: inflector_helper/008.php

    使用减号而不是下划线：

    .. literalinclude:: inflector_helper/009.php

.. php:function:: is_pluralizable($word)

    :param    string    $word: 输入字符串
    :returns:    如果单词可数返回 true，否则返回 false
    :rtype:    bool

    检查给定单词是否有复数形式。示例：

    .. literalinclude:: inflector_helper/010.php

.. php:function:: dasherize($string)

    :param    string    $string: 输入字符串
    :returns:    破折号格式的字符串
    :rtype:    string

    将字符串中的下划线替换为减号。示例：

    .. literalinclude:: inflector_helper/011.php

.. php:function:: ordinal($integer)

    :param    int    $integer: 要确定后缀的整数
    :returns:    序数后缀
    :rtype:    string

    返回应该添加到数字后以表示位置的后缀，如
    1st、2nd、3rd、4th。示例：

    .. literalinclude:: inflector_helper/012.php

.. php:function:: ordinalize($integer)

    :param    int    $integer: 要转换为序数的整数
    :returns:    序数形式的整数
    :rtype:    string

    将数字转换为用于表示位置的序数字符串，如 1st、2nd、3rd、4th。
    示例：

    .. literalinclude:: inflector_helper/013.php
