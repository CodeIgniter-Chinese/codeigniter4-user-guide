##############
错误处理
##############

CodeIgniter 通过 `SPL collection <http://php.net/manual/en/spl.exceptions.php>`_ 和一些框架内自定义异常来生成系统错误报告。错误处理的行为取决于你部署环境的设置，当一个错误或异常被抛出时，只要应用不是在 ``production`` 环境下运行，就会默认展示出详细的错误报告。在这种情况下，应为用户显示一个更为通用的信息来保证最佳的用户体验。

.. contents::
    :local:
    :depth: 2

使用异常处理
================
本节为新手程序员或没有多少异常处理使用经验的开发人员做一个简单概述。

异常处理是在异常被"抛出"的时候产生的事件。它会暂停当前脚本的执行，并将捕获到的异常发送到错误处理程序后显示适当的错误提示页 ::

	throw new \Exception("Some message goes here");

如果你调用了一个可能会产生异常的方法，你可以使用  ``try/catch block`` 去捕获异常 ::

	try {
		$user = $userModel->find($id);
	}
	catch (\Exception $e)
	{
		die($e->getMessage());
	}

如果 ``$userModel`` 抛出了一个异常，那么它就会被捕获，并执行 catch 代码块内的语句。在这个样例中，脚本终止并输出了 ``UserModel`` 定义的错误信息。

在这个例子中，我们可以捕捉任意类型的异常。如果我们仅仅想要监视特定类型的异常，比如 UnknownFileException，我们就可以把它在 catch 参数中指定出来。这样一来，其它异常和非监视类型子类的异常都会被传递给错误处理程序 ::

	catch (\CodeIgniter\UnknownFileException $e)
	{
		// do something here...
	}

这便于你自己进行错误处理或是在脚本结束前做好清理工作。如果你希望错误处理程序正常运行，可以在 catch 语句块中再抛出一个新的异常 ::

	catch (\CodeIgniter\UnknownFileException $e)
	{
		// do something here...

		throw new \RuntimeException($e->getMessage(), $e->getCode(), $e);
	}

配置
=============

默认情况下，CodeIgniter 将在 ``development`` 和 ``testing`` 环境中展示所有的错误，而在 ``production`` 环境中不展示任何错误。你可以在主 ``index.php`` 文件的顶部找到环境配置部分来更改此设置。

.. important:: 如果发生错误，禁用错误报告将不会阻止日志的写入。

记录异常
------------------

By default, all Exceptions other than 404 - Page Not Found exceptions are logged. This can be turned on and off
by setting the **$log** value of ``Config\Exceptions``::

    class Exceptions
    {
        public $log = true;
    }

To ignore logging on other status codes, you can set the status code to ignore in the same file::

    class Exceptions
    {
        public $ignoredCodes = [ 404 ];
    }

.. note:: It is possible that logging still will not happen for exceptions if your current Log settings
    are not set up to log **critical** errors, which all exceptions are logged as.

自定义异常
=================

下列是可用的自定义异常:

PageNotFoundException
---------------------

这是用来声明 404 ，页面无法找到的错误。当异常被抛出时，系统将显示后面的错误模板 ``/application/views/errors/html/error_404.php``。你应为你的站点自定义所有错误视图。如果在 ``Config/Routes.php`` 中，你指定了404 的重写规则，那么它将代替标准的 404 页来被调用 ::

	if (! $page = $pageModel->find($id))
	{
		throw \CodeIgniter\Exceptions\PageNotFoundException::forPageNotFound();
	}

你可以通过异常传递消息，它将在 404 页默认消息位置被展示。

ConfigException
---------------

当配置文件中的值无效或 class 类不是正确类型等情况时，请使用此异常 ::

	throw new \CodeIgniter\Exceptions\ConfigException();

它将 HTTP 状态码置为 500，退出状态码被置为 3.

UnknownFileException
--------------------

在文件没有被找到时，请使用此异常 ::

	throw new \CodeIgniter\UnknownFileException();

它将 HTTP 状态码置为 500，退出状态码被置为 4.

UnknownClassException
---------------------

当一个类没有被找到时，请使用此异常 ::

	throw new \CodeIgniter\UnknownClassException($className);

它将 HTTP 状态码置为 500，退出状态码被置为 5.

UnknownMethodException
----------------------

当一个类的方法不存在时，请使用此异常 ::

	throw new \CodeIgniter\UnknownMethodException();

它将 HTTP 状态码置为 500，退出状态码被置为 6.

UserInputException
------------------

当用户的输入无效时，请使用此异常 ::

	throw new \CodeIgniter\UserInputException();

它将 HTTP 状态码置为 500，退出状态码被置为 7.

DatabaseException
-----------------

当产生如连接不能建立或连接临时丢失的数据库错误时，请使用此异常 ::

	throw new \CodeIgniter\DatabaseException();

它将 HTTP 状态码置为 500，退出状态码被置为 8.

RedirectException
-----------------

This exception is a special case allowing for overriding of all other response routing and
forcing a redirect to a specific route or URL::

    throw new \CodeIgniter\Router\Exceptions\RedirectException($route);

``$route`` may be a named route, relative URI, or a complete URL. You can also supply a
redirect code to use instead of the default (``302``, "temporary redirect")::

    throw new \CodeIgniter\Router\Exceptions\RedirectException($route, 301);
