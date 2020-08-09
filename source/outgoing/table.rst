################
HTML表格类
################

表格类提供的功能使你可以从数组或者数据库结果集中自动生成 HTML 表格。


.. contents::
  :local:

.. raw:: html

  <div class="custom-index container"></div>

*********************
使用表格类
*********************

初始化表格类
======================

表格类不会作为服务提供，并且应该被 “合理地” 实例化，例如::

	$table = new \CodeIgniter\View\Table();

实例
========

下面的示例展现了如何从多维数组中创建一个表格。
注意，第一个数组索引将会变成表格标题（或者你可以在下面函数中参照描述的 ``setHeading()`` 方法中设置你自己的标题）

::

	$table = new \CodeIgniter\View\Table();

	$data = [
		['Name', 'Color', 'Size'],
		['Fred', 'Blue',  'Small'],
		['Mary', 'Red',   'Large'],
		['John', 'Green', 'Medium'],
	];

	echo $table->generate($data);


下面的表格示例展示了从数据库查询结果中创建的表格。
表格类将根据表格名自动生成标题（或者你可以在下面函数中参照描述的 ``setHeading()`` 方法中设置你自己的标题）


::

	$table = new \CodeIgniter\View\Table();

	$query = $db->query('SELECT * FROM my_table');

	echo $table->generate($query);

下面的示例展示了如何使用离散参数创建表格::

	$table = new \CodeIgniter\View\Table();

	$table->setHeading('Name', 'Color', 'Size');

	$table->addRow('Fred', 'Blue', 'Small');
	$table->addRow('Mary', 'Red', 'Large');
	$table->addRow('John', 'Green', 'Medium');

	echo $table->generate();

下面是相同的示例，除了替换了个别参数之外，还使用了数组::

	$table = new \CodeIgniter\View\Table();

	$table->setHeading(array('Name', 'Color', 'Size'));

	$table->addRow(['Fred', 'Blue', 'Small']);
	$table->addRow(['Mary', 'Red', 'Large']);
	$table->addRow(['John', 'Green', 'Medium']);

	echo $table->generate();

改变你的表格的外观
===============================

表格类允许你设置一个指定布局设计的表格模板。下面是模板原型::

	$template = [
		'table_open'         => '<table border="0" cellpadding="4" cellspacing="0">',

		'thead_open'         => '<thead>',
		'thead_close'        => '</thead>',

		'heading_row_start'  => '<tr>',
		'heading_row_end'    => '</tr>',
		'heading_cell_start' => '<th>',
		'heading_cell_end'   => '</th>',

		'tfoot_open'         => '<tfoot>',
		'tfoot_close'        => '</tfoot>',

		'footing_row_start'  => '<tr>',
		'footing_row_end'    => '</tr>',
		'footing_cell_start' => '<td>',
		'footing_cell_end'   => '</td>',

		'tbody_open'         => '<tbody>',
		'tbody_close'        => '</tbody>',

		'row_start'          => '<tr>',
		'row_end'            => '</tr>',
		'cell_start'         => '<td>',
		'cell_end'           => '</td>',

		'row_alt_start'      => '<tr>',
		'row_alt_end'        => '</tr>',
		'cell_alt_start'     => '<td>',
		'cell_alt_end'       => '</td>',

		'table_close'        => '</table>'
	];

	$table->setTemplate($template);

.. note:: 在样板中你会被告知有两套“列”模块。这些列模块允许你创建交替的列颜色或者创建交替每一个重复的列数据的设计元素。

          你不需要确认完成的样板。如果你仅需要改变部分布局，你能很容易确定设计元素。在下面这个示例里，只有表格开放标签被改变了::

	$template = [
		'table_open' => '<table border="1" cellpadding="2" cellspacing="1" class="mytable">'
	];

	$table->setTemplate($template);
	
           对于表格构造函数来说，对于下面这些元素你也可以通过样本设置数组设置默认值。::

	$customSettings = [
		'table_open' => '<table border="1" cellpadding="2" cellspacing="1" class="mytable">'
	];

	$table = new \CodeIgniter\View\Table($customSettings);


***************
类参考
***************

.. php:class:: Table

	.. attribute:: $function = NULL

		 允许你指定一个本地 PHP 函数或者一个有效函数数组以应用于所有单元数据。
		::

			$table = new \CodeIgniter\View\Table();

			$table->setHeading('Name', 'Color', 'Size');
			$table->addRow('Fred', '<strong>Blue</strong>', 'Small');

			$table->function = 'htmlspecialchars';
			echo $table->generate();

		在上面的例子中，所有单元格数据都将通过 PHP 的 :php:func:`htmlspecialchars()`
                函数，结果是::

			<td>Fred</td><td>&lt;strong&gt;Blue&lt;/strong&gt;</td><td>Small</td>

	.. php:method:: generate([$tableData = NULL])

		:param	mixed	$tableData: 填充表格行的数据
		:returns:	HTML 表格
		:rtype:	string（字符类型）

		返回包含生成表的字符串。接受可选择的参数，该参数可以是数组或者数据库结果对象。

	.. php:method:: setCaption($caption)

		:param	string	$caption: 表格标题
		:returns:	表格例证（方法链接）
		:rtype:	Table（表格类型）

		允许你为表格添加标题。
		::

			$table->setCaption('Colors');

	.. php:method:: setHeading([$args = [] [, ...]])

		:param	mixed	$args: 包含表纵行标题的数组或者多个字符串
		:returns:	表格例证（方法链接）
		:rtype:	Table（表格类型）

		允许你设置表格标题。你可以提交一个数组或者离散参数
		::

			$table->setHeading('Name', 'Color', 'Size'); // or

			$table->setHeading(['Name', 'Color', 'Size']);

	.. php:method:: setFooting([$args = [] [, ...]])

		:param	mixed	$args: 包含表格基准值的数组或者多个字符串
		:returns:	 表格例证（方法链接）
		:rtype:	Table（表格类型）

		允许你设置表格基准。你可以确认数组或者离散参数 ::

			$table->setFooting('Subtotal', $subtotal, $notes); // or

			$table->setFooting(['Subtotal', $subtotal, $notes]);

	.. php:method:: addRow([$args = array()[, ...]])

		:param	mixed	$args: 包含列值的数组或者多个字符串
		:returns:	 表格例证（方法链接） (method chaining)
		:rtype:	Table（表格类型）

		允许你添加列到表格。你能确定数组或者离散参数::

			$table->addRow('Blue', 'Red', 'Green'); // or

			$table->addRow(['Blue', 'Red', 'Green']);

		如果你想要设置个别单元的标签属性，为了单元格你可以使用组合数组。
                关联键的 **数据** 定义了单元格的数据。任何其他的键值 => val 的对都会添加到标签属性 key='val' ::

			$cell = ['data' => 'Blue', 'class' => 'highlight', 'colspan' => 2];
			$table->addRow($cell, 'Red', 'Green');

			// generates
			// <td class='highlight' colspan='2'>Blue</td><td>Red</td><td>Green</td>

	.. php:method:: makeColumns([$array = [] [, $columnLimit = 0]])

		:param	array	$array: 包含多列的数据的数组
		:param	int	$columnLimit: 表格中纵行的数量
		:returns:	表格纵行数组
		:rtype:	array（数组）

		这个方法选取了单独数组输入并且创建了有足够匹配纵行数量请求的多维数组。这个方法允许许多元素显示在固定纵行数量的表格里的单个数组。参考下面的示例 ::

			$list = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve'];

			$newList = $table->makeColumns($list, 3);

			$table->generate($newList);

			// 产生最初形态的表格

			<table border="0" cellpadding="4" cellspacing="0">
			<tr>
			<td>one</td><td>two</td><td>three</td>
			</tr><tr>
			<td>four</td><td>five</td><td>six</td>
			</tr><tr>
			<td>seven</td><td>eight</td><td>nine</td>
			</tr><tr>
			<td>ten</td><td>eleven</td><td>twelve</td></tr>
			</table>


	.. php:method:: setTemplate($template)

		:param	array	$template: 包含样板值的关联数组
		:returns:	成功为 TRUE，失败为 FALSE
		:rtype:	bool（布尔类型）

		允许你设置你的样板。你可以确定完整的或者部分的样板。
		::

			$template = [
				'table_open'  => '<table border="1" cellpadding="2" cellspacing="1" class="mytable">'
			];
		
			$table->setTemplate($template);

	.. php:method:: setEmpty($value)

		:param	mixed	$value: 将值放入空单元格里
		:returns:	表格实例（方法链接）
		:rtype:	Table（表格类型）

		在任何空值表格单元里为了使用让你设置默认值。 你可以的，例如，设置一个非间断的空格 ::

			$table->setEmpty("&nbsp;");

	.. php:method:: clear()

		:returns:	表格实例（方法链接）
		:rtype:	Table（表格类型）

		让你清理表格标题，列数据和题注。
		如果你需要显示带有不同数据的多行表格，你要在已经清理了前面表格信息的每一个表格后引用这个方法 。 
		

		示例 ::

			$table = new \CodeIgniter\View\Table();


			$table->setCaption('Preferences')
                            ->setHeading('Name', 'Color', 'Size')
                            ->addRow('Fred', 'Blue', 'Small')
                            ->addRow('Mary', 'Red', 'Large')
                            ->addRow('John', 'Green', 'Medium');

			echo $table->generate();

			$table->clear();

			$table->setCaption('Shipping')
                            ->setHeading('Name', 'Day', 'Delivery')
                            ->addRow('Fred', 'Wednesday', 'Express')
                            ->addRow('Mary', 'Monday', 'Air')
                            ->addRow('John', 'Saturday', 'Overnight');

			echo $table->generate();
