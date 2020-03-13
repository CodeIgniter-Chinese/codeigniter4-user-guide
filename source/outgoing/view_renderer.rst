#############
视图渲染器
#############

.. contents::
    :local:
    :depth: 2

使用视图渲染器
***************************

``view()`` 方法是一种便捷功能，可以获取 ``renderer`` 服务实例，然后可以设置数据并显示视图。
这种方式是我们常用的方式，但有时候我们需要一种更为直接的使用方式；在这种情况下你可以直接以视图服务的形式调用它::

	$view = \Config\Services::renderer();

如果不使用 ``View`` 类作为默认渲染器，则可以直接实例化它::

	$view = new \CodeIgniter\View\View();

.. important:: 你应该只在控制器内创建、使用服务。如果你想在其他类（Library）中使用，则应在类的构造函数中将其设置为依赖项。

然后，您可以使用它提供的三种标准方法中的任何一种:
**render(viewpath, options, save)**, **setVar(name, value, context)** 和 **setData(data, context)**.

它是做什么的
============

``View`` 类将视图的参数提取到可在脚本内部访问的PHP变量后，处理存储在应用程序视图路径中的标准 HTML/PHP 脚本。
这意味着视图中的参数名称必须是合法的 PHP 变量名。

``View`` 类在内部使用一个关联数组，以保存视图参数，直到调用 ``render()`` 方法为止。这意味着视图参数（或变量）名称必须是
唯一的，否则后面变量的值将覆盖前面的变量。

同时，这还会影响脚本中不同上下文的参数值，你将必须为每个值赋予唯一的参数名称。

数组类型的值没有任何特殊含义，可以根据自己的 PHP 代码处理数组。

链式调用方法
===============

`setVar()` 和 `setData()` 方法支持链式调用，允许将多个不同的调用组合到一个方法链中使用::

	$view->setVar('one', $one)
	     ->setVar('two', $two)
	     ->render('myView');

转义数据
=============

当你将数据传递给 ``setVar()`` 和 ``setData()`` 方法时，可以选择转义数据以防止跨站点脚本攻击。作为这两种方法中的最后一个参数，你
可以传递所需的上下文，以选择是否对数据进行转义。

如果你不想对数据进行转义，你可以向每个方法的最后一个参数传递 `null` 或 `raw`，这样将不会对数据进行转义::

	$view->setVar('one', $one, 'raw');

如果选择不转义数据，或者要传递对象实例，则可以使用 ``esc()`` 辅助方法在视图中手动转义数据。第一个参数是要转义的字符串，第二个参数是
用于转义数据的上下文（请参见下文）::

	<?= \esc($object->getStat()) ?>

.. note:: 译者注：框架内部使用 ``\Zend\Escaper\Escaper`` 类中以 escape 开头的相关方法对数据进行的转义处理。

转义上下文
-----------------

默认情况下，``esc()`` 方法认为要转义的数据会在 HTML 中使用。如果数据打算用于 Javascript、CSS 或 href 属性时，需要不同的转义规则才
能生效。你可以传入转义类型名称作为第二个参数，选择合适的规则。规则支持 'html', 'js', 'css', 'url' 和 'attr'::

	<a href="<?= esc($url, 'url') ?>" data-foo="<?= esc($bar, 'attr') ?>">Some Link</a>

	<script>
		var siteName = '<?= esc($siteName, 'js') ?>';
	</script>

	<style>
		body {
			background-color: <?= esc('bgColor', 'css') ?>
		}
	</style>

视图渲染器选项
=====================

可以将多个选项信息传递给 ``render()`` 或 ``renderString()`` 方法：

-   ``cache`` - 缓存视图结果的时间（以秒为时间单位）， renderString() 方法中会忽略
-   ``cache_name`` - 保存缓存视图结果的文件名，默认是 viewpath， renderString() 方法中会忽略
-   ``saveData`` - 如果要保留视图的参数，并在后续调用中使用，应设置为 true

类参考
***************

.. php:class:: CodeIgniter\\View\\View

	.. php:method:: render($view[, $options[, $saveData=false]]])
                :noindex:

		:param  string  $view: 源视图文件的文件名
		:param  array   $options: 以键值对传递的选项数组
		:param  boolean $saveData: 如果该值为 true , 该方法会保留该数据并为其他调用使用；反之就会在渲染视图后清除该数据
		:returns: 指定视图文件所渲染的文字内容
		:rtype: string

		根据传入的文件名和预先设置的数据来渲染输出::

			echo $view->render('myview');

	.. php:method:: renderString($view[, $options[, $saveData=false]]])
                :noindex:

		:param  string  $view: 需要渲染的视图的内容，例如从数据库里返回的内容等
		:param  array   $options: 以键值对传递的选项数组
		:param  boolean $saveData: 如果该值为 true , 该方法会保留该数据并为其他调用使用；反之就会在渲染视图后清除该数据
		:returns: 指定视图文件所渲染的文字内容
		:rtype: string

		根据给定的视图分块和预先设置的数据来渲染输出::

			echo $view->renderString('<div>My Sharona</div>');

		该方法可以用于输出一些例如数据库中存储的内容。但是你需要意识到这一操作可能是有安全风险的，并且**必须**对这些数据进行验证以及尽可能进行转义！

	.. php:method:: setData([$data[, $context=null]])
                :noindex:

		:param  array   $data: 以键值对传递的视图数据数组
		:param  string  $context: 使用数据转义的上下文
		:returns: 用于方法链式调用的渲染器
		:rtype: CodeIgniter\\View\\RendererInterface.

		同时设置多组视图数据::

			$view->setData(['name'=>'George', 'position'=>'Boss']);

        支持以下的上下文: html, css, js, url, or attr or raw, 如果是 'raw' 的话，就不进行转义

        每个调用都会为对象附加一个属性数据，直到视图被渲染

	.. php:method:: setVar($name[, $value=null[, $context=null]])
                :noindex:

		:param  string  $name: 视图数据变量的变量名
		:param  mixed   $value: 该变量的变量值
		:param  string  $context: 使用数据转义的上下文
		:returns: 用于方法链式调用的渲染器
		:rtype: CodeIgniter\\View\\RendererInterface.

		设置单个数据变量::

			$view->setVar('name','Joe','html');

		支持以下的上下文: html, css, js, url, or attr or raw, 如果是 'raw' 的话，就不进行转义

		如果你想要使用对该对象已使用过的视图数据变量，新的值就会取代老的值。
