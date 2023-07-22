#############
XML 辅助函数
#############

XML 辅助函数文件包含帮助处理 XML 数据的函数。

.. contents::
    :local:
    :depth: 2

加载此辅助函数
===================

使用以下代码加载此辅助函数:

.. literalinclude:: xml_helper/001.php

可用函数
===================

以下函数可用:

.. php:function:: xml_convert($str[, $protect_all = false])

    :param string $str: 要转换的文本字符串
    :param bool $protect_all: 是否保护看起来像潜在实体的所有内容,而不仅仅是编号的实体,例如 &foo;
    :returns: XML 转换后的字符串
    :rtype:    string

    接受一个字符串作为输入,并将以下保留的 XML 字符转换为实体:

      - 和号: &
      - 小于号和大于号: < >
      - 单引号和双引号: ' "
      - 破折号: -

    如果它们是现有编号字符实体的一部分,此函数会忽略和号,例如 &#123;。示例:

    .. literalinclude:: xml_helper/002.php

    输出:

    .. code-block:: html

        &lt;p&gt;Here is a paragraph &amp; an entity (&#123;).&lt;/p&gt;
