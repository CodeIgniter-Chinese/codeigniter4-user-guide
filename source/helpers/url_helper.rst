#############
URL 辅助函数
#############

URL 辅助函数文件包含的函数辅助 URLs 运行。

.. contents::
  :local:

.. raw:: html

  <div class="custom-index container"></div>

加载 URL 辅助函数
===================

在每个请求中 URL 辅助函数由框架自动地加载。

通用函数
===================

下文函数是通用的:

.. php:function:: site_url([$uri = ''[, $protocol = NULL[, $altConfig = NULL]]])

	:param	string	$uri: URI string
	:param	string	$protocol: 协议，处理资料传送的标准，例如 'http' 或者 'https'
	:param	\\Config\\App	$altConfig: 使用更替配置
	:returns:	Site URL
	:rtype:	string

        返回你的 site URL，就像在你的配置文件里说明的。
	index.php 文件（或者在你的配置文件里任何你已经设置在你网站的 **index_page**）
	将会添加到 URL，如同你通过函数程序段的一些 URL，外加在你的配置文件中已经设置的 **url_suffix**.
	
	在你的 URL 改变的事件中，你被鼓励在任何时间使用函数生成本地 URL 以便你的页面将变得更加便携。
	
	程序段能随意地像 string 或者 array 通过函数。下文是 string 事例::

		echo site_url('news/local/123');

	上文的事例返回的地址如下:
	*http://example.com/index.php/news/local/123*

	这里是一个通过数组程序段的事例::

		$segments = ['news', 'local', '123'];
		echo site_url($segments);

        对不同的网站如果生成 URLs 你或许会找到比你的配置更有用的更替配置，该函数包含不同配置优先权。
	我们为单元测试框架本身使用这个函数。
	

.. php:function:: base_url([$uri = ''[, $protocol = NULL]])

	:param	string	$uri: URI string
	:param	string	$protocol: 协议，处理资料传送的标准，例如 'http' 或者 'https'
	:returns:	基地址 URL
	:rtype:	string

	返回你网站的基地址 URL, 如同在你配置文件里具体说明的。事例::

		echo base_url();

	如同 :php:func:`site_url()` 该函数返回相同的事件,  
	排除 *index_page* 或者 *url_suffix* 被附加的情况。

	也如函数 :php:func:`site_url()`, 你能提供程序段如 string 或者 array. 
	这里是 string 事例::

		echo base_url("blog/post/123");

	上文事例返回的地址如下:
	*http://example.com/blog/post/123*

	因为不同的 :php:func:`site_url()` 函数是有用的, 你能提供 string 值到文件里，譬如图片或者层叠式样式表。
	例如::

		echo base_url("images/icons/edit.png");

	上文的输出函数将给你如下面的链接:
	*http://example.com/images/icons/edit.png*

.. php:function:: current_url([$returnObject = false])

	:param	boolean	$returnObject: True 如果你想要 URI 事例返回，代替 string。
	:returns:	最近的 URL
	:rtype:	string|URI

	返回最近被浏览过的页面的正确的 URL (包括程序段)。

	.. note:: 引用下面的函数是同样的:

	::

		base_url(uri_string());

.. php:function:: previous_url([$returnObject = false])

	:param boolean $returnObject: True 如果你想要 URI 事例返回，代替 string.
	:returns:  URL 用户以前通过的
	:rtype: string|URI

	返回完整页面的 URL （包含程序段）是用户以前通过的。

        由于安全问题造成盲目的信任 HTTP_REFERER 系统变量，在对话里如果它是有用的 CodeIgniter 将储存以前浏览的页面。
	这保证我们将常常使用已知且可信的源，如果对话已经被加载了，或者是别的方式不能得到的，那么 HTTP_REFERER 的净化版本将会被应用。
	

.. php:function:: uri_string()

	:returns:	An URI string
	:rtype:	string

	返回你的最近 URL 的路径部分。例如，如果你的 URL 是这样的::

		http://some-site.com/blog/comments/123

	函数将返回::

		blog/comments/123

.. php:function:: index_page([$altConfig = NULL])

	:param	\\Config\\App $altConfig: 使用更替配置
	:returns:	'index_page' 值
	:rtype:	mixed

	返回你网站的 **index_page**, 如同在你的配置文件里明确说明的。
	事例::

		echo index_page();

        如同用 :php:func:`site_url()`,你也许要具体制定一个更替配置。
	对不同的网站如果生成 URLs 你或许会找到比你现有的更有用的更替配置，函数包含不同配置优先权。
	我们为单元测试框架本身使用这个函数。

.. php:function:: anchor([$uri = ''[, $title = ''[, $attributes = ''[, $altConfig = NULL]]]])

	:param	mixed	$uri: URI 程序段的 URI string 或者 array 
	:param	string	$title: 锚定 title
	:param	mixed	$attributes: HTML 属性
	:param	\Config\App	$altConfig: 使用更替配置
	:returns:	HTML 超连结 (锚定 tag)
	:rtype:	string

	基于你本地网站 URL 创建标准 HTML 锚定链接。

	第一个参数能包含任意你希望应用到 URL 的程序段。
	如同上文用 :php:func:`site_url()` 函数，程序段可以是 string 或者 array.
	
	.. note:: 如果你正在构造的链接对于你的应用是内部的则不包含基地址 URL (http://...).在你的配置文件里函数将会明确说明的从信息里被自动添加。你希望附加到的 URL 仅仅包含 URI 的程序段。

	第二参数是你想要链接表达的正文。如果你留下第二个程序为空，URL 将会被应用。

	第三个参数包含你想要添加到链接里的的属性列表。属性可以是简单的 string 或者组合数组。 

	这里是一些示例 ::

		echo anchor('news/local/123', 'My News', 'title="News title"');
		// Prints: <a href="http://example.com/index.php/news/local/123" title="News title">My News</a>

		echo anchor('news/local/123', 'My News', array('title' => 'The best news!'));
		// Prints: <a href="http://example.com/index.php/news/local/123" title="The best news!">My News</a>

		echo anchor('', 'Click here');
		// Prints: <a href="http://example.com/index.php">Click here</a>

	如同上文阐述的，你也许可以明确说明更替配置。
	如果对不同网站生成链接你也许会发现更替配置比你的配置是更有用的，它包含不同的配置优先权。
	我们为单元测试框架自身使用这个函数。
	
	.. note:: 属性载入锚定函数是自动地退出对 XSS 攻击不利的保护。

.. php:function:: anchor_popup([$uri = ''[, $title = ''[, $attributes = FALSE[, $altConfig = NULL]]]])

	:param	string	$uri: URI string
	:param	string	$title: 锚定 title
	:param	mixed	$attributes: HTML 属性
	:param	\Config\App	$altConfig: 使用更替配置
	:returns:	自动跳起的 hyperlink
	:rtype:	string

	几乎同源于  :php:func:`anchor()` 函数，除了在新窗口里它是开放的 URL。
	在第三个参数中你能明确说明 JavaScript 窗口属性去控制窗口如何被打开。
	如果第三个参数没有设定，它将会带着你自身的浏览器设定去简单地打开一个新窗口。 

	这里是带着属性的事例::

		$atts = [
		    'width'       => 800,
		    'height'      => 600,
		    'scrollbars'  => 'yes',
		    'status'      => 'yes',
		    'resizable'   => 'yes',
		    'screenx'     => 0,
		    'screeny'     => 0,
		    'window_name' => '_blank'
		];

	echo anchor_popup('news/local/123', 'Click Me!', $atts);

	As above, you may specify an alternate configuration.
	You may find the alternate configuration useful if generating links for a
	different site than yours, which contains different configuration preferences.
	We use this for unit testing the framework itself.
    
	.. note:: 上文属性是默认函数因此你仅仅需要去设置哪些个不同于你需要的属性。在第三个参数里如果你想要函数去简单地通过空数组使用所有它的默认值:

	::
		echo anchor_popup('news/local/123', 'Click Me!', []);

	.. note::  **window_name** 不是真实的属性，但是对于 JavaScript 争论 `window.open()  <http://www.w3schools.com/jsref/met_win_open.asp>`_ 方法，它接受任何一方的窗口名或者窗口目标。

	.. note:: 任何超过上文列表的其他属性将会被分列就像 HTML 属性对于锚定 tag.
	       如同上文描述的，你也许可以明确说明更替配置。
	       你也许会发现如果正生成的链接对不同的网站更替配置比你的配置更有用，他包含不同的配置优先权。
	       我们为单元测试框架自身使用这个函数。

	.. note:: 属性载入锚定自动跳起函数是自动地退出对 XSS 攻击不利的保护。
	
.. php:function:: mailto($email[, $title = ''[, $attributes = '']])

	:param	string	$email: E-mail 地址
	:param	string	$title: 锚定 title
	:param	mixed	$attributes: HTML 属性
	:returns:	"mail to" 超连结
	:rtype:	string

	创建标准的 HTML 邮件链接。用法事例::

		echo mailto('me@my-site.com', 'Click Here to Contact Me');

	 如同用上文 :php:func:`anchor()` tab 函数, 
	 你可以使用第三个参数设定属性::

		$attributes = array('title' => 'Mail me');
		echo mailto('me@my-site.com', 'Contact Me', $attributes);

	.. note::  属性载入锚定 mailto 函数是自动地退出对 XSS 攻击不利的保护。

.. php:function:: safe_mailto($email[, $title = ''[, $attributes = '']])

	:param	string	$email: E-mail 地址
	:param	string	$title: 锚定 title
	:param	mixed	$attributes: HTML 属性
	:returns:	安全垃圾邮件 "mail to" 超连结
	:rtype:	string

	完全相似于 :php:func:`mailto()`  函数除了 *mailto* tag 的模糊版本，
	由于垃圾邮件群聊程序用 JavaScript 写了该函数正使用序数数字用以从保护已经收获的 e-mail 地址。
	

.. php:function:: auto_link($str[, $type = 'both'[, $popup = FALSE]])

	:param	string	$str: 输入 string
	:param	string	$type: 链接类型 ('email', 'url' 或者 'both')
	:param	bool	$popup: 是否创建自动跳起链接
	:returns:	链接化的 string
	:rtype:	string

	在字符到链接里自动地转换包含 URLs 和 e-mail 地址。事例::

		$string = auto_link($string);

	第二参数决定是否 URLs 和 e-mail 是转换了仅仅一个或者其他什么的。如果参数不是明确的说明默认行为是兼有的。
	E-mail 链接编码如同上文显示的 :php:func:`safe_mailto()` 一样。 

	仅转换 URLs::

		$string = auto_link($string, 'url');

	仅转换 e-mail 地址::

		$string = auto_link($string, 'email');

	第三个参数决定是否链接在新窗口被显示。
	值是 TRUE 或者 FALSE （boolean）::

		$string = auto_link($string, 'both', TRUE);

	.. note:: 仅有的被普遍承认的 URLs 这些链接用 "www." 或者用 "://" 开始。

.. php:function:: url_title($str[, $separator = '-'[, $lowercase = FALSE]])

	:param	string	$str: 输入 string
	:param	string	$separator: 字符分隔符
	:param	bool	$lowercase: 是否转换输出 string 为小写字型
	:returns:	已经格式化的 string
	:rtype:	string

	取 string 作为输入值并创建友好人性化的 URL string. 
	这是有用的，例如，在 URL 里你有个blog ，在 blog 里你想要使用你的整个主题。事例::

		$title     = "What's wrong with CSS?";
		$url_title = url_title($title);
		// Produces: Whats-wrong-with-CSS

	第二个参数决定词汇的定义符号。默认的破折号被使用。更好的选项是: **-** (破折号) 或者 **_** (下划线)。

	例如::

		$title     = "What's wrong with CSS?";
		$url_title = url_title($title, 'underscore');
		// Produces: Whats_wrong_with_CSS

	第三个参数决定是或者不是小写字符是被强迫的。默认他们不是。选项是 boolean TRUE/FALSE.

	例如::

		$title     = "What's wrong with CSS?";
		$url_title = url_title($title, 'underscore', TRUE);
		// Produces: whats_wrong_with_css

.. php:function:: prep_url($str = '')

	:param	string	$str: URL string
	:returns:	协议前缀 URL string
	:rtype:	string

	在事件里这个函数正从一个 URL 错过，它将添加 *http://*  协议前缀。
	通过 URL string 的函数像下文这样::

		$url = prep_url('example.com');
