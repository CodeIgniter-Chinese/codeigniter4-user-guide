##############
文本辅助函数
##############

文本辅助函数文件包括了一系列有助于处理文本的函数

.. contents::
  :local:

.. raw:: html

  <div class="custom-index container"></div>

加载辅助函数
===================

该系列函数通过以下方式加载::

	helper('text');

可用函数列表
===================

以下函数可用:

.. php:function:: random_string([$type = 'alnum'[, $len = 8]])

	:param	string	$type: 需要随机输出的类型
	:param	int	$len: 输出的字符串长度
	:returns:	一个随机字符串
	:rtype:	string

	基于类型和长度生成一个随机字符串。
	对于创建密码或随机哈希等非常有用。

	第一个参数给定字符串类型，第二个参数给定字符串长度，可使用以下类型:

	-  **alpha**: 仅有大小写字母构成的字符串
	-  **alnum**: 含有大小写字母和数字的字符串
	-  **basic**: 基于 ``mt_rand()`` 方法组成的随机数（忽略长度）
	-  **numeric**: 数字类型的字符串
	-  **nozero**: 数字类型字符串，其中不含有零
	-  **md5**: 基于 ``md5()`` 的加密随机数（固定长度32位）
	-  **sha1**: 基于 ``sha1()`` 的加密随机数（固定长度40位）
	-  **crypto**: 基于 ``random_bytes()`` 的随机字符串

	用例如下::

		echo random_string('alnum', 16);

.. php:function:: increment_string($str[, $separator = '_'[, $first = 1]])

	:param	string	$str: 输入的字符串
	:param	string	$separator: 用于增加一个数字的分隔符
	:param	int	$first: 起始数字
	:returns:	递增字符串
	:rtype:	string

	通过将一个每次在尾部递增数字的方式，递增一个字符串。用于创建"拷贝"或者用于拥有唯一标题或简介的文件或数据库内容。

	用例如下::

		echo increment_string('file', '_'); // "file_1"
		echo increment_string('file', '-', 2); // "file-2"
		echo increment_string('file_4'); // "file_5"

.. php:function:: alternator($args)

	:param	mixed	$args: 参数的一个变量数字
	:returns:	变化后的字符串
	:rtype:	mixed

	允许在进行循环时，两个或多个项目之间交换变化，例如::

		for ($i = 0; $i < 10; $i++)
		{     
			echo alternator('string one', 'string two');
		}

	如果你需要的话也可以增加尽可能多的参数，在下一次迭代时，下一个项目将会被返回。
	
	::
	
		for ($i = 0; $i < 10; $i++)
		{     
			echo alternator('one', 'two', 'three', 'four', 'five');
		}

	.. note:: 多个独立函数调用时，只需要不传参，不用重新初始化直接调用即可。

.. php:function:: reduce_double_slashes($str)

	:param	string	$str: 输入字符串
	:returns:	格式化斜线后的字符串
	:rtype:	string

	将一个字符串中的双斜线转变为单斜线，除了在 URL 协议前缀中的，比如 http&#58;//

	例如::

		$string = "http://example.com//index.php";
		echo reduce_double_slashes($string); // 返回 "http://example.com/index.php"

.. php:function:: strip_slashes($data)

	:param	mixed	$data: 输入的字符串或者字符串数组
	:returns:	去除斜杠后的字符串（数组）
	:rtype:	mixed

	从一组字符串中去除所有斜杠

	例如::

		$str = [
			'question' => 'Is your name O\'reilly?',
			'answer'   => 'No, my name is O\'connor.'
		];

		$str = strip_slashes($str);

	以上会返回数组::

		[
			'question' => "Is your name O'reilly?",
			'answer'   => "No, my name is O'connor."
		];

	.. note:: 基于历史原因，该函数也接受字符串类型的输入。这样看起来就跟 ``stripslashes()`` 函数的别名一样
		alias for ``stripslashes()``.

.. php:function:: reduce_multiples($str[, $character = ''[, $trim = FALSE]])

	:param	string	$str: 需要搜索的文本
	:param	string	$character: 需要简化的字符
	:param	bool	$trim: 是否在字符串首位同时去除指定的字符
	:returns:	简化后的字符串
	:rtype:	string

	将多个连续出现的相同字符简化为一个，例如::

		$string = "Fred, Bill,, Joe, Jimmy";
		$string = reduce_multiples($string,","); //结果 "Fred, Bill, Joe, Jimmy"

	如果第三个参数被设为 TRUE 的话，该函数就会将首部和尾部出现的该字符串同时去除，例如::

		$string = ",Fred, Bill,, Joe, Jimmy,";
		$string = reduce_multiples($string, ", ", TRUE); //结果是 "Fred, Bill, Joe, Jimmy"

.. php:function:: quotes_to_entities($str)

	:param	string	$str: 输入的字符串
	:returns:	拥有转义符号的字符串转换后的 HTML 实体
	:rtype:	string

	将一个单引号或双引号转换为对应的 HTML 实体，例如::

		$string = "Joe's \"dinner\"";
		$string = quotes_to_entities($string); //结果是 "Joe&#39;s &quot;dinner&quot;"

.. php:function:: strip_quotes($str)

	:param	string	$str: 输入字符串
	:returns:	去除了引号的字符串
	:rtype:	string

	从字符串中去除单双引号，例如::

		$string = "Joe's \"dinner\"";
		$string = strip_quotes($string); //结果是 "Joes dinner"

.. php:function:: word_limiter($str[, $limit = 100[, $end_char = '&#8230;']])

	:param	string	$str: 输入字符串
	:param	int	$limit: 限制
	:param	string	$end_char: 结尾字符（通常是省略号）
	:returns:	限制了单词的字符串
	:rtype:	string

	根据 *单词* 的长度截断字符串，例如::

		$string = "Here is a nice text string consisting of eleven words.";
		$string = word_limiter($string, 4);
		// Returns:  Here is a nice

	第三个参数是一个可选的字符串后缀。默认是一个省略号。

.. php:function:: character_limiter($str[, $n = 500[, $end_char = '&#8230;']])

	:param	string	$str: 输入字符串
	:param	int	$n: 字符数量
	:param	string	$end_char: 结尾字符
	:returns:	限定了字符的字符串
	:rtype:	string

	根据给定的 *字符* 的数量截断字符串。该方法将会保持单词的完整性，因此字符串长度可能会比你给定的略多或略少

	例如::

		$string = "Here is a nice text string consisting of eleven words.";
		$string = character_limiter($string, 20);
		// 返回:  Here is a nice text string

	第三个参数是一个可选的字符串后缀，未定义则默认使用省略号

	.. note:: 如果你想截断完全一致长度的字符串，参照下方的
		函数 :php:func:`ellipsize()`

.. php:function:: ascii_to_entities($str)

	:param	string	$str: 输入字符串
	:returns:	一个将 ASCII 值转化为实体的字符串
	:rtype:	string

	将 ASCII 码转化为字符实体，包括可能导致 web 页面中出现问题的高位 ASCII 码以及一些 Word 字符串。
	通过这一方法可以使得这些字符无论是浏览器设置或是存储于数据库中都可以正确地显示。
	不过该方法依赖于你浏览器所支持的字符集，因此不一定100%可靠。
	不过在大多数情况下，该方法可以正确识别非正常类型的字符（例如方言字符等）

	例如::

		$string = ascii_to_entities($string);

.. php:function:: entities_to_ascii($str[, $all = TRUE])

	:param	string	$str: 输入字符串
	:param	bool	$all: 是否同样转换非安全的实体
	:returns:	将 HTML 实体转化为 ASCII 码的字符串
	:rtype:	string

	该函数与 :php:func:`ascii_to_entities()` 相反，将字符实体转换为 ASCII 码

.. php:function:: convert_accented_characters($str)

	:param	string	$str: 输入字符串
	:returns:	一个字符串，其中方言字符已进行过转换
	:rtype:	string

	将高位 ASCII 码转化为等同功能的低位 ASCII 码。当面对只有标准 ASCII 码可以安全使用的情况，将非英语的字符进行转换，比如在 URL 中

	例如::

		$string = convert_accented_characters($string);

	.. note:: 该函数利用配置文件 `app/Config/ForeignCharacters.php` 来定义并进行数组翻译。

.. php:function:: word_censor($str, $censored[, $replacement = ''])

	:param	string	$str: 输入字符串
	:param	array	$censored: 一系列需要被探测的有问题的单词
	:param	string	$replacement: 用于替换问题单词的字符串
	:returns:	探测后的字符串
	:rtype:	string

	用于检测文本字符串中的敏感词。第一个参数为原有的字符串，第二个是一个含有你需要拦截的敏感词的数组。第三个参数（可选）为需要用于替换的单词。
	如果不声明的话就会用井号替换: ###

	例如::

		$disallowed = ['darn', 'shucks', 'golly', 'phooey'];
		$string     = word_censor($string, $disallowed, 'Beep!');

.. php:function:: highlight_code($str)

	:param	string	$str: 输入字符串
	:returns:	HTML 格式代码高亮的字符串
	:rtype:	string

	将一个代码字符串 （PHP, HTML, 等）加上颜色。例如::

		$string = highlight_code($string);

	该函数使用了 PHP 的 ``highlight_string()`` 方法，因此使用的颜色是在你的 php.ini 文件中定义的。

.. php:function:: highlight_phrase($str, $phrase[, $tag_open = '<mark>'[, $tag_close = '</mark>']])

	:param	string	$str: 输入字符串
	:param	string	$phrase: 高亮的片段
	:param	string	$tag_open: 用于高亮的开括号
	:param	string	$tag_close: 用于高亮的闭括号
	:returns:	通过 HTML 进行片段高亮后的字符串
	:rtype:	string

	在一个文本字符串中高亮一个片段。第一个参数是原本的字符串，第二个参数是你需要高亮的片段。
	第三个第四个参数包含你需要用于包裹高亮片段的 HTML 标签。

	例如::

		$string = "Here is a nice text string about nothing in particular.";
		echo highlight_phrase($string, "nice text", '<span style="color:#990000;">', '</span>');

	以上将会输出::

		Here is a <span style="color:#990000;">nice text</span> string about nothing in particular.

	.. note:: 该函数默认使用 ``<strong>`` 标签。
	    旧版本的浏览器可能不支持新型 HTML5 的格式标签，因此我们推荐你将下述 CSS 加入到你的样式表中，如果你需要支持这类浏览器的话::

			mark {
				background: #ff0;
				color: #000;
			};

.. php:function:: word_wrap($str[, $charlim = 76])

	:param	string	$str: 输入字符串
	:param	int	$charlim: 字符限制
	:returns:	单词换行过的字符串
	:rtype:	string

	将一个文本以指定的字符长度进行换行，并保持单词完整性

	例如::

		$string = "Here is a simple string of text that will help us demonstrate this function.";
		echo word_wrap($string, 25);

		// 输出如下:
		// Here is a simple string
		// of text that will help us
		// demonstrate this
		// function.

        过长的单词会被截断，不过 URL 不会

.. php:function:: ellipsize($str, $max_length[, $position = 1[, $ellipsis = '&hellip;']])

	:param	string	$str: 输入字符串
	:param	int	$max_length: 字符串长度限制
	:param	mixed	$position: 需要截断的位置（整数或浮点数）
	:param	string	$ellipsis: 作为省略的标记符
	:returns:	省略后的字符串
	:rtype:	string

	该函数将去除字符串中的标记并将其截断为指定长度，同时加上一个省略标记符

	第一个参数是需要省略的字符串，第二个是在输出的字符串中的字符长度。第三个参数是在省略后的字符串中，省略标记符号是否需要从0-1，从左到右的方式出现。
	例如，值为 1 时，就会在右边，0.5 就是中间，0 就是在左边。

	第四个可选的参数是省略符号类型，默认情况下会插入一个 &hellip;

	例如::

		$str = 'this_string_is_entirely_too_long_and_might_break_my_design.jpg';
		echo ellipsize($str, 32, .5);

	结果::

		this_string_is_e&hellip;ak_my_design.jpg

.. php:function:: excerpt($text, $phrase = false, $radius = 100, $ellipsis = '...')

	:param	string	$text: 需要截取摘要的文本
	:param	string	$phrase: 需要截取的文本附近的片段或单词
	:param	int		$radius: 在片段前后截取的字符数量
	:param	string	$ellipsis: 省略标记符
	:returns:	摘要.
	:rtype:		string

	该函数会取出指定 ``$phrase`` 前后各 ``$radius`` 个数量的字符。

	第一个参数是需要截取摘要的文本，第二个是需要截取的中心单词或片段。
	第三个参数是需要截取的数量。如果不传 ``$phrase`` 参数的话就会从头开始获取 ``$radius`` 个字符并加上省略标记符

	例如::

		$text = 'Ut vel faucibus odio. Quisque quis congue libero. Etiam gravida
		eros lorem, eget porttitor augue dignissim tincidunt. In eget risus eget
		mauris faucibus molestie vitae ultricies odio. Vestibulum id ultricies diam.
		Curabitur non mauris lectus. Phasellus eu sodales sem. Integer dictum purus
		ac enim hendrerit gravida. Donec ac magna vel nunc tincidunt molestie sed
		vitae nisl. Cras sed auctor mauris, non dictum tortor. Nulla vel scelerisque
		arcu. Cras ac ipsum sit amet augue laoreet laoreet. Aenean a risus lacus.
		Sed ut tortor diam.';

		echo excerpt($str, 'Donec');

	输出::

		... non mauris lectus. Phasellus eu sodales sem. Integer dictum purus ac
		enim hendrerit gravida. Donec ac magna vel nunc tincidunt molestie sed
		vitae nisl. Cras sed auctor mauris, non dictum ...
