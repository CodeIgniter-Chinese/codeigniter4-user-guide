###################################
在视图文件中使用PHP替代语法
###################################

如果你不使用模板引擎来简化输出，那么意味着你将在视图文件中使用纯 PHP 语法。为了精简视图文件中的 PHP 代码同时增强代码的可读性，建议你在写控制结构和 echo 语句时使用 PHP 的替代语法。如果你对这个语法还不熟悉，下面将介绍如何通过这个语法来消除你代码中的大括号和 echo 语句。


Echo 的替代语法
=================
通常来说，你在输出或打印一个变量的时候会这样做::

	<?php echo $variable; ?>

而使用替代语法，你可以写成这样::

	<?= $variable?>

	
控制结构的替代语法
==============================
像 if、for、foreach、while 这样的控制结构也可以写成简化格式。下面以 ``foreach`` 举例::

	<ul>

	<?php foreach ($todo as $item) : ?>

		<li><?= $item ?></li>

	<?php endforeach ?>

	</ul>

注意这里没有任何括号，结束括号被 ``endforeach`` 取而代之。上面列举出的那些控制结构都有相似的结束标志: ``endif``, ``endfor``, ``endforeach`` 和 ``endwhile``。

同时要注意的是，每个结构分支后面都要跟一个冒号(除了最后一个)，而不是分号,这很重要!

这是另外一个样例，使用了 ``if``/``elseif``/``else``，注意看分支语句后的冒号::

	<?php if ($username === 'sally') : ?>

		<h3>Hi Sally</h3>

	<?php elseif ($username === 'joe') : ?>

		<h3>Hi Joe</h3>

	<?php else : ?>

		<h3>Hi unknown user</h3>

	<?php endif ?>