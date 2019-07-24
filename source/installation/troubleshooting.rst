###############
故障排除
###############

以下是一些常见的安装问题，以及建议的解决方法。

我必须在我的URL中包含index.php
-------------------------------------

如果``/mypage/find/apple``类似的URL``/index.php/mypage/find/apple``不起作用，但类似的URL ，则你的``.htaccess``规则（对于Apache）未正确设置。


仅加载默认页面
---------------------------

如果你发现无论你在URL中放入什么内容，只会加载默认页面，可能是你的服务器不支持提供搜索引擎友好URL所需的REQUEST_URI变量。首先，打开*application/Config/App.php*文件并查找URI协议信息。它会建议你尝试一些备用设置。如果在你尝试此操作后仍然无效，则需要强制CodeIgniter向你的网址添加问号。为此，请打开*application/Config/App.php*文件并更改

::

	public $indexPage = 'index.php';

To this::

	public $indexPage = 'index.php?';

该教程给出了404错误:(
-------------------------------------------

你无法使用PHP的内置Web服务器来学习本教程。它不处理正确路由请求所需的`.htaccess`文件。

解决方案：使用Apache为你的站点提供服务。
