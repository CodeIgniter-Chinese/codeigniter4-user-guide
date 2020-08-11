################
偏转辅助函数
################

偏转辅助函数文件包含的函数容许你改变**英文**词汇到复数，单数，驼峰式大小写，等等。

.. contents::
  :local:

.. raw:: html

  <div class="custom-index container"></div>

加载偏转辅助函数
===================

偏转辅助函数使用下面的代码加载::

	helper('inflector');

通用函数
===================

下面的函数是通用的:

.. php:function:: singular($string)

	:param	string	$string: 输入 string
	:returns:	单数单词
	:rtype:	string

	改变复数单词为单数。例如::

		echo singular('dogs'); //  打印出 'dog'

.. php:function:: plural($string)

	:param	string	$string: 输入 string
	:returns:	复数单词
	:rtype:	string

	 改变单数单词为复数。例如::

		echo plural('dog'); // 打印出 'dogs'
		
.. php:function:: counted($count, $string)

	:param	int 	$count:  Number of items
	:param	string	$string: Input string
	:returns:	A singular or plural phrase
	:rtype:	string

	Changes a word and its count to a phrase. 例如::

		echo counted(3, 'dog'); // 打印出 '3 dogs'

.. php:function:: camelize($string)

	:param	string	$string: 输入 string
	:returns:	驼峰化 string
	:rtype:	string

	由空格或者下划线改变单词分割的字符串为驼峰式大小写。例如::

		echo camelize('my_dog_spot'); // 打印出 'myDogSpot'

.. php:function:: pascalize($string)

	:param	string	$string: Input string
	:returns:	Pascal case string
	:rtype:	string

	Changes a string of words separated by spaces or underscores to Pascal
	case, which is camel case with the first letter capitalized. 例如::

		echo pascalize('my_dog_spot'); // 打印出 'MyDogSpot'

.. php:function:: underscore($string)

	:param	string	$string: 输入 string
	:returns:	字符串包含下划线代替空格
	:rtype:	string

	由多空格和下划线带来多样的单词分割。事例::

		echo underscore('my dog spot'); // 打印出 'my_dog_spot'

.. php:function:: humanize($string[, $separator = '_'])

	:param	string	$string: 输入 string
	:param	string	$separator: 输入分隔符Input separator
	:returns:	人性化的 string
	:rtype:	string

	由空格带来复合单词的分割并在他们中间添加空格。每个单词用大写书写。

	事例::

		echo humanize('my_dog_spot'); // 打印出 'My Dog Spot'

	使用波折号代替下划线::

		echo humanize('my-dog-spot', '-'); // 打印出 'My Dog Spot'

.. php:function:: is_pluralizable($word)

	:param	string	$word: 输入 string
	:returns:	如果单词为可数的则 TRUE 否则 FALSE
	:rtype:	bool

	多次核对假设约定的单词已经有一个复数版本。事例::

		is_pluralizable('equipment'); // 返回 FALSE

.. php:function:: dasherize($string)

	:param	string	$string: 输入 string
	:returns:	底线转换 string
	:rtype:	string

	在 string 里取代带着波折号的下划线。事例::

		dasherize('hello_world'); // 返回 'hello-world'

.. php:function:: ordinal($integer)

	:param	int	$integer: integer 决定词尾
	:returns:	顺序的词尾
	:rtype:	string

	返回的词尾应该添加一个数目去表示位置例如 1st, 2nd, 3rd, 4th. 事例::

		ordinal(1); // 返回 'st'

.. php:function:: ordinalize($integer)

	:param	int	$integer: integer 序号 
	:returns:	序数化 integer
	:rtype:	string

	转换数目为顺序的字符串过去总是指示位置例如 1st, 2nd, 3rd, 4th.
        事例::

		ordinalize(1); // 返回 '1st'
