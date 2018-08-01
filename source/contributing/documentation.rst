#################################
著述 CodeIgniter 文件
#################################


CodeIgniter 用多样的格式使用 Sphinx (文档生成工具)去生成它的文件，使用 reStructuredText（.rst 重新构建的文本）去处理格式。如果你熟悉 Markdown（文本编辑标记语言） 和 Textile （web文本生成器），你将会快速地领会 reStructuredText（.rst）。焦点在易读性和用户的友好性上。

尽管它们是完全专业的，但我们总是为人们著述。

本地内容表格应该总是被包含在内，就像下面的这个。

由下面插入的语句自动地创建表格：

::

	.. contents::
		:local:

	.. raw:: html

  	<div class="custom-index container"></div>

.. contents::
  :local:

.. raw:: html

  <div class="custom-index container"></div>


在当前页面里被插入的 <div> 事件依照未加工的 HTML（超文本标记语言）为了文件的 JavaScript（直译式程序语言）不断变化地添加链接到任何函数而且方法定义也被包含内。

**************
工具需求
**************

去查看提供的 HTML , ePub(电子图书), PDF， 等等，为了 Sphinx 你将需要与 PHP 域名延伸一起去安装 Sphinx . 最起码要安装 Python(计算机程序设计语言). 最后，为了 Pygments（通用高亮句法） 你将要安装 CI（CodeIgniter）词法，以便编码部分能恰当地高亮。

.. code-block:: bash

	easy_install "sphinx==1.2.3"
	easy_install sphinxcontrib-phpdomain



接下来的方向在 范例：``cilexer`` 文件夹里的文件库内的 README 文件里去安装 CI（CodeIgniter） 词法。


*****************************************
页面及段落标题和副标题
*****************************************
 
大量在页面里标题没有仅规定次序和段落，但是他们也同时惯常自动地创建页面和文档表格内容。
为了一小段文字标题格式要使用确定的带下划线的文字。主词标目，像页面名称和段落标题也使用重行。

其他的标题仅使用下划线，以下面的分级结构为准::

	# with overline for page titles
	* with overline for major sections
	= for subsections
	- for subsubsections
	^ for subsubsubsections
	" for subsubsubsubsections (!)


下载文件:  `TextMate ELDocs Bundle <./ELDocs.tmbundle.zip>`_  能帮助你创建下面的 tab（标签） 触发器 (
译者按：原文并没有 ``TextMate ELDocs Bundle`` 下载地址，请您自行搜索 ``eldocs.tmbundle`` 以获取 ``zip`` 下载包 )::

	title->

		##########
		Page Title
		##########

	sec->

		*************
		Major Section
		*************

	sub->

		Subsection
		==========

	sss->

		SubSubSection
		-------------

	ssss->

		SubSubSubSection
		^^^^^^^^^^^^^^^^

	sssss->

		SubSubSubSubSection (!)
		"""""""""""""""""""""""
