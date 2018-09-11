################
辅助函数集(Helpers)
################

辅助函数集（Helpers)，顾名思义，是辅助我们完成任务的函数。每一个辅助函数文件都是某一特定种类函数的集合。比如，**URL辅助函数集(URL Helplers)** 能帮我们创建链接，**Form辅助函数集(Form Helpers)** 能帮我们表单元素，**Text辅助函数集(Text Helpers)** 提供各种文本格式化操作，**Cookie辅助函数集(Cookie Helpers)** 提供设置和读取cookie的相关操作，**File辅助函数集(File Helpers)** 帮我们处理文件操作，等等。

不用于CodeIgniter中的其他大部分系统，Helpers(辅助函数集)并不是用面向对象的方式实现。这些函数都是简单的，过程化的函数。每个辅助函数集都实现了某一特定任务，并不依赖于其他函数。

因此使用 Hepler 的第一步就是加载它。一旦加载完成，它就在你的控制器文件 :doc:`controller <../general/controllers>` 和视图文件 :doc:`views <../general/views>` 中变成全局可用。

Helper辅助函数集 一般保存在 **system/Helpers** 或者 **application/Helpers directory** 目录下。CI会先在 **application/Helpers** 目录中查找，如果目录或者对应的辅助函数集不在该位置，就会转到你的全局目录 *system/Helpers/* 下查找。



加载辅助函数集
================

加载辅助函数集(Helper)文件非常简单，方法如下::

	helper('name');

这里的 **name** 是辅助函数集的文件名，不带.php扩展名或者“helper”部分。



比如，要加载一个文件名为 **cookie_helper.php** 的 **Cookie辅助函数集** ，只需这样::

	helper('cookie');

如果您想一次性加载多个 Helper辅助函数集，可以通过数组传递文件名::

	helper(['cookie','date']);

辅助函数集可以在你控制器方法内的任何位置加载（甚至可以在视图文件中加载，虽然通常这么做并不好）。只要在使用之前加载就行。你也可以在控制器的构造函数中加载，这样就可以在该控制的任何函数中使用，当然也可以在有需要的时候在特定函数里单独加载。

.. note:: 辅助函数集的加载方法没有返回值，所以不要将其赋值给变量。直接使用就行了。

.. note:: URL辅助函数集会被自动加载，所以您无需手动加载。


从一个非标准位置加载
-----------------------------------

辅助函数集也可以从 **application/Helpers** 和 **system/Helpers** 之外的目录加载，只要目录路径名称能够通过命名空间中找到，你可以在自动加载配置文件 :doc:`Autoloader config file <../concepts/autoloader>` PSR-4章节建立命名空间。在那个已命名的空间目录中，加载器默认辅助函数集会放在名为Helper的子文件夹中。以下例子将有助于理解这个情况：

比如，我们将所有博客相关的代码放到一个独立的命名空间 ``Example\Blog`` 中。文件存在服务器上目录 **/Modules/Blog/** 下，于是，我们将博客模块的辅助函数文件放在 **/Modules/Blog/Helpers/** 目录下。 **blog_helper** 的文件路径将会是 **/Modules/Blog/Helpers/blog_helper.php** 。在控制器中，我们就可以使用如下命令来加载辅助函数集::

	helper('Modules\Blog\blog');

.. note:: 这种方式加载文件中的函数不是真正意义上的命名空间。这里使用命名空间只是为了方便定位文件。


使用 Helper 辅助函数集
====================

一旦你要使用的辅助函数集对应的Helper文件完成加载，你就可以用标准的PHP函数调用方式去使用它。

比如，在视图文件中使用 ``anchor()`` 函数创建链接:: 

	<?php echo anchor('blog/comments', 'Click Here');?>

这里的"Click Here"是链接的名字，“blog/comments”是控制器/方法（controller/method）链接的URI地址。

扩展辅助函数集
===================

目标: 确定怎么来扩展...命名空间等？。

想要扩展辅助函数集，先要在 **application/helpers/** 文件夹下新建一个和已有的Helper名字相同的文件，但是要在文件名加上 **MY\_** 前缀（该项可以配置，参见下文）。

如果你只是想在现有的Helper中添加一些功能，比如增加一两个函数，或者修改某个特定函数的实现方法--那么用你自己的版本对整个Helper进行替换就会显得矫枉过正，得不偿失。这种情况下，最好是只进行简单的扩展(extend).

.. note:: 扩展(extend)一词在这里用得并不是很严谨，因为这些辅助函数都是过程化的，相对独立的，并不能实现传统编程意义上的扩展。基于此，你可以在Helper中增加函数，或者替换Helper提供的函数。

比如，想要扩展原生的 **数组辅助函数集Array Helper** ，您要新建一个名叫 **application/helpers/MY_array_helper.php** 的文件，然后添加和重写函数::

	// any_in_array() is not in the Array Helper, so it defines a new function
	function any_in_array($needle, $haystack)
	{
		$needle = is_array($needle) ? $needle : array($needle);

		foreach ($needle as $item)
		{
			if (in_array($item, $haystack))
			{
				return TRUE;
			}
	        }

		return FALSE;
	}

	// random_element() is included in Array Helper, so it overrides the native function
	function random_element($array)
	{
		shuffle($array);
		return array_pop($array);
	}



接下来呢？
=========

在目录中，你能看到所有的 Helper辅助函数集 文件列表。浏览一下，看看这些函数能做什么吧!
