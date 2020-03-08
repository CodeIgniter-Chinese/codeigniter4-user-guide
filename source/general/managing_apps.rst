##########################
管理多个应用
##########################

默认情况下，我们假设你只是用CodeIgniter来管理一个应用，并将该应用在 **application** 目录下进行构建。
然而也存在这样的可能性：多个应用共享一个CodeIgniter的安装目录，甚至开发者会将 application目录进行重命名或移动位置。

重命名Application（应用）文件夹
==================================

如果你想重命名你的应用文件夹，实际上只需要打开 **application/Config/Paths.php** 文件并设置 ``$application_directory`` 变量的值::

	$application_directory = 'application';

移动你的项目文件夹
=====================================

将你的应用目录移动到服务器的另一个位置，而不是web根目录，也是可行的。
为了实现以上目标，请打开你的主 **index.php** 文件并为 ``$application_directory`` 变量赋值为一个 *服务器上的绝对路径* ::

	$application_directory = '/path/to/your/application';

单个CodeIgniter对应运行多个应用
===============================================================

如果你想要让多个不同的应用来共享一次CodeIgniter的安装文件，只需要将你的应用目录下的所有目录都移动到他们对应的子目录中即可。

举例而言，加入你想要创建两个应用程序，命名为"foo"和"bar"，你可以将你的应用目录排列如下::

	applications/foo/
	applications/foo/config/
	applications/foo/controllers/
	applications/foo/libraries/
	applications/foo/models/
	applications/foo/views/
	applications/bar/
	applications/bar/config/
	applications/bar/controllers/
	applications/bar/libraries/
	applications/bar/models/
	applications/bar/views/

为了选择指定的应用目录，你需要打开主index.php文件并设置 ``$application_directory`` 变量。例如，选择"foo"应用，进行以下操作::

	$application_directory = 'applications/foo';

.. note:: 你的每个应用都需要独立的 **index.php** 文件，并独自调用所需的应用文件。 **index.php** 文件也可以被改名为其他你希望的名称。
