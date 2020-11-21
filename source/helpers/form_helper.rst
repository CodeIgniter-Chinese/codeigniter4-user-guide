##############
表单辅助函数
##############

表单辅助函数包含的函数辅助表单运行.

.. contents::
  :local:

.. raw:: html

  <div class="custom-index container"></div>

加载表单辅助函数
===================

表单辅助函数使用下文的代码加载::

	helper('form');

换码（转义）字段值
=====================

你也许需要使用 HTML 和字符像在你的表单内部的元素里引用。为了安全地执行，你将需要使用:doc:`common function <../general/common_functions>`
:func:`esc()`.

考虑下文的示例::

	$string = 'Here is a string containing "quoted" text.';

	<input type="text" name="myfield" value="<?= $string; ?>" />

由于上面字符串包含一套引用，那将导致表单中断。
The :php:func:`esc()` 函数转换 HTML 特殊字节以便它能安全地使用::

	<input type="text" name="myfield" value="<?= esc($string); ?>" />

.. note:: 如果你在页面使用任意表单辅助函数列举，并且你传达像组合的数组一样的值，表单值将会被自动换码，所以不需要调用这个函数。使用它只有你要创建你自己的将要传达作为字符串的表单元素。

通用函数
===================

接下来的函数是通用的:

.. php:function:: form_open([$action = ''[, $attributes = ''[, $hidden = array()]]])

	:param	string	$action: 表单行为/目标 URI 字符串
    	:param	mixed	$attributes: HTML 属性，就像数组或者换码字符串
    	:param	array	$hidden: 隐藏字段的定义的一组数组An array of hidden fields' definitions
    	:returns:	 HTML 表单随时可用的 tag
    	:rtype:	string

    	创建一个带着基地址URL的随时可用的表单标签**从你的配置优先选择营造**.
	它将随意地让你添加表单属性和隐藏输入字段，并且会常常在你的配置文件里添加基于 charset 值的 `accept-charset` 属性。

	宁可使用标签的绝对好处也不要艰苦的编码你自己的 HTML 是由于在事件里你的 URLs 曾改变而标签容许你的网址是更便携的。

	下面是一则简单的例子::

		echo form_open('email/send');

	上面的例子将创建一个指向你的基地址 URL 和 "email/send" URL 部分的表单，像这样::

		<form method="post" accept-charset="utf-8" action="http://example.com/index.php/email/send">
		
	You can also add {locale} like the following::

		echo form_open('{locale}/email/send');

	The above example would create a form that points to your base URL plus the current request locale with
	"email/send" URI segments, like this::

		<form method="post" accept-charset="utf-8" action="http://example.com/index.php/en/email/send">
		
	**添加属性**

		由正传达组合的数组到第二个参数的属性能被加入，像这样::

			$attributes = ['class' => 'email', 'id' => 'myform'];
			echo form_open('email/send', $attributes);

		二选一地，你能明确的像字符串一样说明第二个参数::

			echo form_open('email/send', 'class="email" id="myform"');

		上文的例子将会创建一个同样的表单相似于下文这个事例::

			<form method="post" accept-charset="utf-8" action="http://example.com/index.php/email/send" class="email" id="myform">
			
		If CSRF filter is turned on `form_open()` will generate CSRF field at the beginning of the form. You can specify ID of this field by passing csrf_id as one of the $attribute array:

			form_open('/u/sign-up', ['csrf_id' => 'my-id']);

		will return:

			<form action="/u/sign-up" method="post" accept-charset="utf-8">
			<input type="hidden" id="my-id" name="csrf_field" value="964ede6e0ae8a680f7b8eab69136717d" />

	**添加隐藏输入字段**

		由正传达组合的数组到第三个参数的隐藏字段能被添加，像这样::

			$hidden = ['username' => 'Joe', 'member_id' => '234'];
			echo form_open('email/send', '', $hidden);

		由正传达的任何false值到隐藏字段，你能忽略第二个参数.

		上面的事例将创建类似于下面的句子::

			<form method="post" accept-charset="utf-8" action="http://example.com/index.php/email/send">
				<input type="hidden" name="username" value="Joe" />
				<input type="hidden" name="member_id" value="234" />

.. php:function:: form_open_multipart([$action = ''[, $attributes = ''[, $hidden = array()]]])

	:param	string	$action: 表单行为/目标 URI 字符串
    	:param	mixed	$attributes:  HTML 属性，就像数组或者换码字符串
    	:param	array	$hidden: 隐藏字段的定义的一组数组 
    	:returns:	HTML 多部件的表单随时可用的 tag
    	:rtype:	string

    	这个函数对上文的 :php:func:`form_open()` 来说是类似的，
	除了它附加了一个 *multipart* 属性，如果你喜欢使用表单上传文件这个属性是必须的。

.. php:function:: form_hidden($name[, $value = ''])

	:param	string	$name: 字段名
    	:param	string	$value: 字段值
    	:returns:	HTML 隐藏输入字段 tag
    	:rtype:	string

    	让你生成隐藏输入字段。你也能提交名称/值字符串去创建一个字段::

		form_hidden('username', 'johndoe');
		// 将产生: <input type="hidden" name="username" value="johndoe" />

	... 或者你能提交组合数组去创建复合字段::

		$data = [
			'name'	=> 'John Doe',
			'email'	=> 'john@example.com',
			'url'	=> 'http://example.com'
		];

		echo form_hidden($data);

		/*
			将产生:
			<input type="hidden" name="name" value="John Doe" />
			<input type="hidden" name="email" value="john@example.com" />
			<input type="hidden" name="url" value="http://example.com" />
		*/

	你也能传达组合的数组给字段值::

		$data = [
			'name'	=> 'John Doe',
			'email'	=> 'john@example.com',
			'url'	=> 'http://example.com'
		];

		echo form_hidden('my_array', $data);

		/*
			将产生:

			<input type="hidden" name="my_array[name]" value="John Doe" />
			<input type="hidden" name="my_array[email]" value="john@example.com" />
			<input type="hidden" name="my_array[url]" value="http://example.com" />
		*/

	倘若你想创建额外属性的隐藏输入字段::

		$data = [
			'type'	=> 'hidden',
			'name'	=> 'email',
			'id'	=> 'hiddenemail',
			'value'	=> 'john@example.com',
			'class'	=> 'hiddenemail'
		];

		echo form_input($data);

		/*
			将产生:

			<input type="hidden" name="email" value="john@example.com" id="hiddenemail" class="hiddenemail" />
		*/

.. php:function:: form_input([$data = ''[, $value = ''[, $extra = ''[, $type = 'text']]]])

	:param	array	$data: 字段属性数据
	:param	string	$value: 字段值
	:param	mixed	$extra: 额外属性被添加到 tag 任何一方像数组或者文字字符串
	:param  string  $type: 输入字段类型。例如： 'text', 'email', 'number', 等等.
	:returns:	 HTML 文本输入字段 tag
	:rtype:	string

	让你生成标准的文本输入字段。你能最低程度地在第一和第二参数里传达字段名和值::

		echo form_input('username', 'johndoe');

	或者你能传达包含你希望你的表单要包含的任何数据的组合的数组::

		$data = [
			'name'      => 'username',
			'id'        => 'username',
			'value'     => 'johndoe',
			'maxlength' => '100',
			'size'      => '50',
			'style'     => 'width:50%'
		];

		echo form_input($data);

		/*
			将产生:

			<input type="text" name="username" value="johndoe" id="username" maxlength="100" size="50" style="width:50%"  />
		*/

	如果你想要你的表单包含一些额外的数据，像 JavaScript ，你能在第三参数里像字符串一样传达参数::

		$js = 'onClick="some_function()"';
		echo form_input('username', 'johndoe', $js);

	或者你能像数组一样传达参数::

		$js = ['onClick' => 'some_function();'];
		echo form_input('username', 'johndoe', $js);

	 支持HTML5 输入字段扩充范围，你能像第四个参数一样传达一个输入键入信息::

		echo form_input('email', 'joe@example.com', ['placeholder' => 'Email Address...'], 'email');

		/*
			将产生:

			<input type="email" name="email" value="joe@example.com" placeholder="Email Address..." />
		*/

.. php:function:: form_password([$data = ''[, $value = ''[, $extra = '']]])

	:param	array	$data: 字段属性数据
    	:param	string	$value: 字段值
    	:param	mixed	$extra: 额外的属性被添加到tag任何一方像数组或者文字的字符串
    	:returns:	HTML 密码输入字段 tag
    	:rtype:	string

    	此函数除了函数使用的 "password" 输入类型在完全关系到上文所述的 :php:func:`form_input()` 函数是完全相似的。

.. php:function:: form_upload([$data = ''[, $value = ''[, $extra = '']]])

	:param	array	$data:字段属性数据
    	:param	string	$value:字段值 
    	:param	mixed	$extra: 额外的属性被添加到 tag 任何一方像数组或者文字的字符串
    	:returns:	HTML 文件上传输入字段 tag
    	:rtype:	string

    	此函数除了使用 "file" 输入类型在完全关系到上文所述的 :php:func:`form_input()` 函数是完全相似的，接受函数适用于上传文件。

.. php:function:: form_textarea([$data = ''[, $value = ''[, $extra = '']]])

	:param	array	$data: 字段属性数据
    	:param	string	$value: 字段值
    	:param	mixed	$extra: 额外的属性被添加到 tag 任何一方像数组或者文字的字符串
    	:returns:	HTML 文本区域 tag
    	:rtype:	string

    	此函数除了产生 "textarea" 类型外在完全关系到上文所述的 :php:func:`form_input()`   函数是完全相似的。

	.. note:: 上文的例子里代替 *maxlength* 和 *size* 属性，你会更换具体指定的 *rows* 和 *cols* 。

.. php:function:: form_dropdown([$name = ''[, $options = array()[, $selected = array()[, $extra = '']]]])

	:param	string	$name: 字段名
	:param	array	$options: 选项的组合的数组被列举
    	:param	array	$selected: 字段的列表要标明 *selected* 属性
	:param	mixed	$extra: 额外的属性被添加到 tag 任何一方像数组或者文字的字符串 
    	:returns:	HTML 下拉菜单选择字段 tag
    	:rtype:	string

    	让你创建一个下拉菜单字段。第一个参数会包含字段名，第二个参数会包含一个组合的数组选项，而第三参数会包含你希望被选择的值。你也能通过第三参数传达一个符合选项数组，并且辅助函数会为你创建一个复合选项。

    	例如::

		$options = [
			'small'  => 'Small Shirt',
			'med'    => 'Medium Shirt',
			'large'  => 'Large Shirt',
			'xlarge' => 'Extra Large Shirt',
		];

		$shirts_on_sale = ['small', 'large'];
		echo form_dropdown('shirts', $options, 'large');

		/*
			将产生:

			<select name="shirts">
				<option value="small">Small Shirt</option>
				<option value="med">Medium  Shirt</option>
				<option value="large" selected="selected">Large Shirt</option>
				<option value="xlarge">Extra Large Shirt</option>
			</select>
		*/

		echo form_dropdown('shirts', $options, $shirts_on_sale);

		/*
			将产生:

			<select name="shirts" multiple="multiple">
				<option value="small" selected="selected">Small Shirt</option>
				<option value="med">Medium  Shirt</option>
				<option value="large" selected="selected">Large Shirt</option>
				<option value="xlarge">Extra Large Shirt</option>
			</select>
		*/

	 如果你想要开始部分的 <select> 包含额外的数据，像 id 属性或者 JavaScript ，你能在第四个参数里像字符串一样传达它::

		$js = 'id="shirts" onChange="some_function();"';
		echo form_dropdown('shirts', $options, 'large', $js);

	或者你能像传达数组一样传达参数::

		$js = [
			'id'       => 'shirts',
			'onChange' => 'some_function();'
		];
		echo form_dropdown('shirts', $options, 'large', $js);

	如果数组被传达象 ``$options`` 一样是一个多维数组，那么 ``form_dropdown()`` 将会产生一个像 label 一样带着数组键码的 <optgroup> 。

.. php:function:: form_multiselect([$name = ''[, $options = array()[, $selected = array()[, $extra = '']]]])

	:param	string	$name: 字段名
    	:param	array	$options: 选项的组合数组被列举
    	:param	array	$selected: 字段的列表要标明 *selected* 属性
	:param	mixed	$extra: 额外的属性被添加到 tag 任何一方像数组或者文字的字符串
    	:returns:	HTML 下拉菜单混合选项字段 tag
    	:rtype:	string

    	让你创建一个标准的混合字段。第一个参数将包含字段名，第二个参数会包含选项的一个组合的数组，
	而第三个参数会包含值或者你想要被选择的值。

	参数用法是完全相似于上文去使用的 :php:func:`form_dropdown()` ，除了当然地字段名将需要去用 POST 数组语法，例如：foo[].

.. php:function:: form_fieldset([$legend_text = ''[, $attributes = array()]])

	:param	string	$legend_text: Text 放进 <legend> tag 
    	:param	array	$attributes: 属性被置位在 <fieldset> tag 上 
    	:returns:	HTML 字段置位开始 tag
    	:rtype:	string

    	让你生成 fieldset/legend 字段。

    	例如::

		echo form_fieldset('Address Information');
		echo "<p>fieldset content here</p>\n";
		echo form_fieldset_close();

		/*
			生成:

				<fieldset>
					<legend>Address Information</legend>
						<p>form content here</p>
				</fieldset>
		*/

	相似于其他函数，如果你更喜欢设置额外属性你能在第二参数里提交一个组合的数组::

		$attributes = [
			'id'	=> 'address_info',
			'class'	=> 'address_info'
		];

		echo form_fieldset('Address Information', $attributes);
		echo "<p>fieldset content here</p>\n";
		echo form_fieldset_close();

		/*
			生成:

			<fieldset id="address_info" class="address_info">
				<legend>Address Information</legend>
				<p>form content here</p>
			</fieldset>
		*/

.. php:function:: form_fieldset_close([$extra = ''])

	:param	string	$extra: 闭合 tag 附加的任何字段, *as is*
	:returns:	HTML 字段置位关闭 tag
	:rtype:	string

	 产生一个正关闭的 </fieldset> tag. 使用这个函数仅有的优势是它允许你传达数据给将被添加的下文关联的 tag 。例如

	::

		$string = '</div></div>';
		echo form_fieldset_close($string);
		// 将生成: </fieldset></div></div>

.. php:function:: form_checkbox([$data = ''[, $value = ''[, $checked = FALSE[, $extra = '']]]])

	:param	array	$data: 字段属性数据 
    	:param	string	$value: 字段值
    	:param	bool	$checked: 是否去标明 checkbox 在 *checked* 状态 
	:param	mixed	$extra: 额外的属性被添加到 tag 任何一方像数组或者文字的字符串
    	:returns:	HTML checkbox 输入 tag
    	:rtype:	string

    	让你产生一个 checkbox 字段. 简单的例子::

		echo form_checkbox('newsletter', 'accept', TRUE);
		// 将生成:  <input type="checkbox" name="newsletter" value="accept" checked="checked" />

	第三个参数包含一个布尔值 TRUE/FALSE 去决定是否 box 应该被记号或者未记号。
	
	在这个辅助函数里类似的对于其他的表单函数来说，你也能传达属性的数组给函数::

		$data = [
			'name'    => 'newsletter',
			'id'      => 'newsletter',
			'value'   => 'accept',
			'checked' => TRUE,
			'style'   => 'margin:10px'
		];

		echo form_checkbox($data);
		// 将生成: <input type="checkbox" name="newsletter" id="newsletter" value="accept" checked="checked" style="margin:10px" />

	也跟其他函数一样，如果你想要 tag 去包含像 JavaScript 的额外数据，你能在第四个参数里像传达字符串一样传达它::

		$js = 'onClick="some_function()"';
		echo form_checkbox('newsletter', 'accept', TRUE, $js);

	或者你能像数组一样传达它::

		$js = ['onClick' => 'some_function();'];
		echo form_checkbox('newsletter', 'accept', TRUE, $js);

.. php:function:: form_radio([$data = ''[, $value = ''[, $checked = FALSE[, $extra = '']]]])

	:param	array	$data: 字符串属性数据
    	:param	string	$value: 字符串值
    	:param	bool	$checked: 是否标明 radio 按钮是 *checked* 状态 
	:param	mixed	$extra: 额外的属性被添加到tag任何一方像数组或者文字的字符串
    	:returns:	HTML radio 输入 tag
    	:rtype:	string

    	除了函数使用 "radio" 输入类型此函数在完全关系到上文所述的 :php:func:`form_checkbox()` 函数是完全类似的。

.. php:function:: form_label([$label_text = ''[, $id = ''[, $attributes = array()]]])

	:param	string	$label_text: Text 提交 <label> tag 
    	:param	string	$id: 我们正在制作的一个 label 表单元素的 ID 
    	:param	string	$attributes: HTML 属性
    	:returns:	HTML 字段 label tag
    	:rtype:	string

    	让你产生一个 <label>. 简单事例::

		echo form_label('What is your Name', 'username');
		// 将生成:  <label for="username">What is your Name</label>

	相似于其他函数，如果你更喜欢设置额外的属性你能在第三个参数里提交一个组合的数组.

	例如::
	
		$attributes = [
			'class' => 'mycustomclass',
			'style' => 'color: #000;'
		];

		echo form_label('What is your Name', 'username', $attributes);
		// 将生成:  <label for="username" class="mycustomclass" style="color: #000;">What is your Name</label>

.. php:function:: form_submit([$data = ''[, $value = ''[, $extra = '']]])

	:param	string	$data: Button 名
    	:param	string	$value: Button 值
    	:param	mixed	$extra: 额外的属性被添加到 tag 任何一方像数组或者文字的字符串
    	:returns:	HTML 输入submit tag
    	:rtype:	string

    	让你产生一个标准的 submit 按钮。简单事例::

		echo form_submit('mysubmit', 'Submit Post!');
		// 将生成:  <input type="submit" name="mysubmit" value="Submit Post!" />

	相似于其他函数，如果你更喜欢设置你的本身的属性你能在第一个参数里提交一个组合数组。第三个参数让你添加额外的数据到你的表单，象 JavaScript.

.. php:function:: form_reset([$data = ''[, $value = ''[, $extra = '']]])

	:param	string	$data: Button 名
    	:param	string	$value: Button 值
    	:param	mixed	$extra: 额外的属性被添加到tag任何一方像数组或者文字的字符串
    	:returns:	HTML 输入重新设定 button tag
    	:rtype:	string

    	让你生成标准重新设定 button 。 使用习惯对 :func:`form_submit()` 是完全相似的.
	

.. php:function:: form_button([$data = ''[, $content = ''[, $extra = '']]])

	:param	string	$data: Button 名
    	:param	string	$content: Button label
    	:param	mixed	$extra: 额外的属性被添加到tag任何一方像数组或者文字的字符串
    	:returns:	An HTML button tag
    	:rtype:	string

    	让你生成标准 button 元素. 你能在第一和第二参数里最低程度地传达 button 名称和内容::

		echo form_button('name','content');
		// 将生成: <button name="name" type="button">Content</button>

	或者你能传达你的表单去包含你希望包含任何数据的一个组合的数组::

		$data = [
			'name'    => 'button',
			'id'      => 'button',
			'value'   => 'true',
			'type'    => 'reset',
			'content' => 'Reset'
		];

		echo form_button($data);
		// 将生成: <button name="button" id="button" value="true" type="reset">Reset</button>

	如果你想要你的表单包含一些额外的数据，例如 JavaScript ， 你能在第三个参数里像字符串一样传达它::

		$js = 'onClick="some_function()"';
		echo form_button('mybutton', 'Click Me', $js);

.. php:function:: form_close([$extra = ''])

	:param	string	$extra: 在关闭 tag 后任何事要追加的, *as is*
	:returns:	HTML 表单关闭 tag
	:rtype:	string

	生成正关闭的 </form> tag. 最佳的优势去使用这个函数容许你去传达数据给它，它将会被添加如下文的 tag 。例如::

		$string = '</div></div>';
		echo form_close($string);
		// 将生成:  </form> </div></div>

.. php:function:: set_value($field[, $default = ''[, $html_escape = TRUE]])

	:param	string	$field: 字段名
    	:param	string	$default: 默认值
    	:param  bool	$html_escape: 是否关闭 HTML 值的转义
    	:returns:	字段值
    	:rtype:	string

    	容许你去设置输入表单或者文本区域的值。你必须经过函数的第一个参数提供字段名。第二个操作参数允许你为表单设置一个默认值。第三个操作参数允许你去关闭 HTML 值的转义，万一你需要使用此函数联合， 即 :php:func:`form_input()` 并规避双层转义。

	例如::

		<input type="text" name="quantity" value="<?php echo set_value('quantity', '0'); ?>" size="50" />

	当第一次加载时下文的表单将显示 "0".

.. php:function:: set_select($field[, $value = ''[, $default = FALSE]])

	:param	string	$field: 字段名
    	:param	string	$value: 检测的值 
    	:param	string	$default: 是否值也是默认的
    	:returns:	'selected' 属性或者一个空字符串
    	:rtype:	string

    	如果你使用 <select> 菜单, 此函数允许你显示已经被选择的菜单题目。.

    	第一个参数必须包含选择菜单的包含名，第二个参数必须包含选择菜单包含值，
	而第三个操作参数仍你设置像默认值 (use boolean TRUE/FALSE) 的一个项.

    	例如::

		<select name="myselect">
			<option value="one" <?php echo  set_select('myselect', 'one', TRUE); ?> >One</option>
			<option value="two" <?php echo  set_select('myselect', 'two'); ?> >Two</option>
			<option value="three" <?php echo  set_select('myselect', 'three'); ?> >Three</option>
		</select>

.. php:function:: set_checkbox($field[, $value = ''[, $default = FALSE]])

	:param	string	$field: 字段名
    	:param	string	$value: 检测的值
    	:param	string	$default: 是否值也是默认的
    	:returns:	'checked' 属性或者一个空字符串 
    	:rtype:	string

    	容许你在已经提交状况下显示一个 checkbox.

    	第一个参数必须包含 checkbox 的名，第二个参数必须包含它的值，并且第三个操作参数让你设置一个像默认值 (use boolean TRUE/FALSE) 的项.

    	例如::

		<input type="checkbox" name="mycheck" value="1" <?php echo set_checkbox('mycheck', '1'); ?> />
		<input type="checkbox" name="mycheck" value="2" <?php echo set_checkbox('mycheck', '2'); ?> />

.. php:function:: set_radio($field[, $value = ''[, $default = FALSE]])

	:param	string	$field: 字段名
    	:param	string	$value: 检测的值
    	:param	string	$default: 是否值也是默认的
    	:returns:	'checked' 属性或者空字符串
    	:rtype:	string

    	容许你去显示它们已经提交状态下的 radio buttons . 此函数对于上文 :php:func:`set_checkbox()` 函数是完全相似的。

	事例::

		<input type="radio" name="myradio" value="1" <?php echo  set_radio('myradio', '1', TRUE); ?> />
		<input type="radio" name="myradio" value="2" <?php echo  set_radio('myradio', '2'); ?> />

	.. note:: 如果你正在使用表单验证类，你必须常常为你的字段明确说明一个规范，即使空的，适当的为了 ``set_*()`` 函数去工作。
	          这是因为如果表单验证对象已经定义了，控制器为了 ``set_*()`` 已经送交了类方法替代一般的辅助函数。

