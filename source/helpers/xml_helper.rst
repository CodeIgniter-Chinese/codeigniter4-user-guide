############
XML辅助函数
############

XML辅助函数文件包含一些用于处理XML数据的函数。

.. contents::
  :local:

.. raw:: html

  <div class="custom-index container"></div>

加载辅助函数
===================

辅助函数是通过以下代码加载的

::

	helper('xml');

可用的函数
===================

可使用以下函数:

.. php:function:: xml_convert($str[, $protect_all = FALSE])

	:param string $str:  所需要转换的文本字符串
	:param bool $protect_all:  是否保持那些看起来是一个潜在实体的结构而非将其转化为数字标识的实体，例如$foo。
	:returns:  转化成XML结构的字符串
	:rtype:	string

	将一个字符串作为输入并将以下的保留 XML 字符转化为实体:

	  - 与操作符: &
	  - 大于小于号: < >
	  - 单双引号: ' "
	  - 横杠: -

    该函数将忽略作为数字字符实体的一部分而存在的&符号，例如 ``&#123;`` 。如下所示::

		$string = '<p>Here is a paragraph & an entity (&#123;).</p>';
		$string = xml_convert($string);
		echo $string;

	输出:

	.. code-block:: html

		&lt;p&gt;Here is a paragraph &amp; an entity (&#123;).&lt;/p&gt;
