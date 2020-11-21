##################
Typography 类
##################

Typography 库包含一些方法用于帮助您以语义相关的方式设置文本格式。

*******************
加载类库
*******************

与 CodeIgniter 的所有其他服务一样，可以通过 ``Config\Services`` 来加载，通常不需要手动加载::

    $typography = \Config\Services::typography();

**************************
可用的静态方法
**************************

以下的方法是可用的：

**autoTypography()**

.. php:function:: autoTypography($str[, $reduce_linebreaks = FALSE])

	:param	string	$str: Input string
	:param	bool	$reduce_linebreaks: 是否将多个双重换行减少为两个
	:returns:	HTML 格式化的排版安全的字符串
	:rtype: string

	格式化文本使其成为语义和排版正确的 HTML 。

	使用示例::

		$string = $typography->autoTypography($string);

	.. note:: 格式排版可能会消耗大量处理器资源，特别是在排版大量内容时。 如果你选择使用这个函数的话，
		你可以考虑 :doc:`缓存 <../general/caching>` 你的页面。

**formatCharacters()**

.. php:function:: formatCharacters($str)

	:param	string	$str: Input string
	:returns:	带有格式化字符的字符串
	:rtype:	string

	将双引号或单引号转成正确的实体，也会转化—破折号，双空格和&符号。

	使用示例::

		$string = $typography->formatCharacters($string);

**nl2brExceptPre()**

.. php:function:: nl2brExceptPre($str)

	:param	string	$str: Input string
	:returns:	带有 HTML 格式化换行符的字符串
	:rtype:	string

	将换行转换为 <br /> 标签， 忽略 <pre> 标签中的换行符。
	这个函数和PHP原生的 ``nl2br()`` 函数是一样的，
	但忽略 <pre> 标签。

	使用示例::

		$string = $typography->nl2brExceptPre($string);
