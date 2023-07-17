###############
故障排除
###############

以下是一些常见的安装问题及建议的解决方法。

.. contents::
    :local:
    :depth: 2

如何知道我的安装是否正常工作?
---------------------------------------

在项目根目录的命令行中::

    > php spark serve

然后在浏览器中打开 ``http://localhost:8080`` 应该可以看到默认的欢迎页面:

|CodeIgniter4 欢迎页面|

我的 URL 中必须包含 index.php
-------------------------------------

如果像 ``/mypage/find/apple`` 这样的 URL 不起作用,但类似的 ``/index.php/mypage/find/apple`` 可以正常访问,这可能是因为您的 **.htaccess** 规则(用于 Apache)没有正确设置,或者 Apache 的 **httpd.conf** 中的 ``mod_rewrite`` 扩展被注释掉了。
请参阅 :ref:`urls-remove-index-php`。

只有默认页面加载
---------------------------

如果您发现无论在 URL 中输入什么,只有默认页面加载,这可能是因为您的服务器不支持提供搜索引擎友好 URL 所需的 REQUEST_URI 变量。作为第一步,打开 **app/Config/App.php** 文件,查看 URI 协议信息。它会建议您尝试一些替代设置。如果在您尝试后仍然不起作用,则需要强制 CodeIgniter 在 URL 中添加问号(?)。要做到这一点,请打开 **app/Config/App.php** 文件,并将此内容:

.. literalinclude:: troubleshooting/001.php

改为:

.. literalinclude:: troubleshooting/002.php

未指定输入文件
-----------------------

如果看到“未指定输入文件”,请尝试如下更改重写规则(在 ``index.php`` 后添加 ``?``):

.. code-block:: apache

    RewriteRule ^([\s\S]*)$ index.php?/$1 [L,NC,QSA]

我的应用在本地正常工作,但在生产服务器上不正常
----------------------------------------------------------

确保文件夹和文件名的大小写与代码匹配。

许多开发者在 Windows 或 macOS 的大小写不敏感的文件系统上开发。
然而,大多数服务器环境使用大小写敏感的文件系统。

例如,当您有 **app/Controllers/Product.php** 时,必须使用
``Product`` 作为短类名,而不是 ``product``。

如果文件名大小写不正确,服务器上就找不到该文件。

教程中的所有页面都显示 404 错误 :(
-------------------------------------------

您不能使用 PHP 的内置 Web 服务器 following 这个教程。
它不会处理路由请求所需的 **.htaccess** 文件。

解决方案:使用 Apache  serve 您的网站,或者从项目根目录使用内置的
CodeIgniter 等价命令 ``php spark serve``。

.. |CodeIgniter4 欢迎页面| image:: ../images/welcome.png

“Whoops!” 页面是什么?
----------------------------------------

您会发现您的应用程序显示一个“Whoops!”页面,然后是文本行“We seem to have hit a snag. Please try again later...”。

这表示您处于生产模式并遇到了不可恢复的错误,我们不想让 webapp 的查看者看到,以实现更好的安全性。

您可以在日志文件中看到错误。请参阅下面的“CodeIgniter 错误日志”。

如果在开发过程中达到此页面,应将环境设置为“development”(在 **.env** 中)。有关更多详细信息,请参阅 :ref:`setting-development-mode`。
之后,重新加载页面。您将看到错误和回溯。

CodeIgniter 错误日志
----------------------

CodeIgniter 根据 **app/Config/Logger.php** 中的设置记录错误消息。

您可以调整错误阈值以查看更多或更少的消息。有关详细信息,请参阅 :ref:`日志记录 <logging-configuration>`。

默认配置将每日日志文件存储在 **writable/logs** 中。
如果事情没有按您期望的那样工作,最好检查一下它们!
