##########################
管理多个应用
##########################

默认情况下，我们假设你只是用CodeIgniter来管理一个应用，并将该应用在 **application** 目录下进行构建。
然而也存在这样的可能性：多个应用共享一个CodeIgniter的安装目录，甚至开发者会将 application目录进行重命名或移动位置。

重命名或迁移应用程序目录
==================================

如果你想重命名你的应用文件夹或者移动
it to a different location on your server, other than your project root, open
your main **app/Config/Paths.php** and set a *full server path* in the
``$appDirectory`` variable (at about line 38)::

	public $appDirectory = '/path/to/your/application';
	
You will need to modify two additional files in your project root, so that
they can find the ``Paths`` configuration file:

- ``/spark`` runs command line apps; the path is specified on or about line 36::

    require 'app/Config/Paths.php';
    // ^^^ Change this if you move your application folder


- ``/public/index.php`` is the front controller for your webapp; the config
  path is specified on or about line 16::

    $pathsPath = FCPATH . '../app/Config/Paths.php';
    // ^^^ Change this if you move your application folder

单个CodeIgniter对应运行多个应用
===============================================================

如果你想要让多个不同的应用来共享一次CodeIgniter的安装文件，只需要将你的应用目录下的所有目录都移动到他们对应的子目录中即可。

举例而言，加入你想要创建两个应用程序，命名为"foo"和"bar"，你可以将你的应用目录排列如下:

.. code-block:: text

    /foo
        /app
        /public
        /tests
        /writable
    /bar
        /app
        /public
        /tests
        /writable
    /codeigniter
        /system
        /docs

This would have two apps, "foo" and "bar", both having standard application directories
and a ``public`` folder, and sharing a common codeigniter framework.

The ``index.php`` inside each application would refer to its own configuration,
``../app/Config/Paths.php``, and the ``$systemDirectory`` variable inside each
of those would be set to refer to the shared common "system" folder.

If either of the applications had a command-line component, then you would also
modify ``spark`` inside each application's project folder, as directed above.
