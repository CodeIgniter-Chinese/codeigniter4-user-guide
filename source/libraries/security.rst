##############
安全类
##############

安全类包含了一些方法，用于帮助保护你的网站，以免受到跨站请求伪造（CSRF）的攻击。

.. contents::
    :local:
    :depth: 2

*******************
加载类
*******************

如果你加载这个类，只是想进行 CSRF 的防护，那就没必要加载它，因为它是作为一个过滤器运行的，而且没有手动调用的接口。

如果你想在某种情况下直接访问这个类，你可以通过服务文件来加载它::

	$security = \Config\Services::security();

*********************************
跨站请求伪造 （CSRF）
*********************************

打开你的 **application/Config/Filters.php** 文件并且全局开启 `csrf` 过滤器，即可开启 CSRF 防护::

	public $globals = [
		'before' => [
			'csrf'
		]
	];

你可以添加一个 URI 的白名单，跳过 CSRF 保护（例如某个 API 接口希望接受 原始的 POST 数据），
将这些 URI 添加到 `csrf` 过滤器的 'except' 配置参数中::

	public $globals = [
		'before' => [
			'csrf' => ['except' => ['api/record/save']]
		]
	];

同样支持正则表达式（不区分大小写）::

    public $globals = [
		'before' => [
			'csrf' => ['except' => ['api/record/[0-9]+']]
		]
	];

如果你使用 :doc:`表单辅助函数 <../helpers/form_helper>` ，:func:`form_open()`
函数将会自动地在你的表单中插入一个隐藏的 CSRF 字段。如果没有插入这个字段，
你可以手动调用 ``get_csrf_token_name()`` 和 ``get_csrf_hash()`` 这两个函数。
::

	<input type="hidden" name="<?= csrf_token() ?>" value="<?= csrf_hash() ?>" />

另外，你可以使用 ``csrf_field()`` 方法来帮你生成这个隐藏的 ``input`` 字段::

	// Generates: <input type="hidden" name="{csrf_token}" value="{csrf_hash}" />
	<?= csrf_field() ?>

令牌（tokens）默认会在每一次提交时重新生成，或者你也可以设置成在 CSRF cookie
的生命周期内一直有效。默认情况下令牌重新生成提供了更严格的安全机制，但可能会对
可用性带来一定的影响，因为令牌很可能会变得失效（例如使用浏览器的返回前进按钮、
使用多窗口或多标签页浏览、异步调用等等）。你可以修改下面这个参数来改变这一点。
::

	public $CSRFRegenerate  = true;

*********************
其它的辅助方法
*********************

你将永远不需要直接使用安全类中的大多数方法。下面的一些方法，你可能会觉得有用，这些方法和 CSRF 防护无关。

**sanitizeFilename()**

尝试对文件名进行净化，防止目录遍历尝试以及其他的安全威胁，这在文件名作为用户输入的参数时格外有用。第一个参数是需要净化的路径名。

如果用户输入包含相对路径是可以接受的，例如： file/in/some/approved/folder.txt ,那么你可以设置第二个可选参数， $relative_path
为 true 。
::

	$path = $security->sanitizeFilename($request->getVar('filepath'));
