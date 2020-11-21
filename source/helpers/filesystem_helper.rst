#################
文件系统辅助函数
#################

目录辅助函数文件包含的函数协助目录运行。

.. contents::
  :local:

.. raw:: html

  <div class="custom-index container"></div>

加载文件系统辅助函数
======================

文件系统辅助函数使用下面的代码加载:

::

	helper('filesystem');

通用函数
===================

接下来的函数是通用的:

.. php:function:: directory_map($source_dir[, $directory_depth = 0[, $hidden = FALSE]])

	:param	string	$source_dir: 资源目录路径
	:param	int	$directory_depth: 遍历目录量度 (0 = 完全递归, 1 = 最近目录, 等等)
	:param	bool	$hidden: 是否包含隐藏目录
	:returns:	文件数组
	:rtype:	array

	例如::

		$map = directory_map('./mydirectory/');

	.. note:: 路径几乎常常与你的主要 index.php 文件有关系。

	 子文件夹包含的目录还会被映射。如果你希望控制递归量度，你会使用秒参数（整型）。1 的量度将仅仅映射根层目录::

		$map = directory_map('./mydirectory/', 1);

	默认情况下，在返回数组里将不会被包含隐藏文件。推翻这个运转状态，你也许要设置第三个参数为真（boolean）::

		$map = directory_map('./mydirectory/', FALSE, TRUE);

	每一个文件名将是数组索引，它包含的文件将会被用数值编入索引。下面是一个典型数组::

		Array (
			[libraries] => Array
				(
					[0] => benchmark.html
					[1] => config.html
					["database/"] => Array
						(
							[0] => query_builder.html
							[1] => binds.html
							[2] => configuration.html
							[3] => connecting.html
							[4] => examples.html
							[5] => fields.html
							[6] => index.html
							[7] => queries.html
						)
					[2] => email.html
					[3] => file_uploading.html
					[4] => image_lib.html
					[5] => input.html
					[6] => language.html
					[7] => loader.html
					[8] => pagination.html
					[9] => uri.html
				)

	如果没有找到结果，将会返回空数组。

.. php:function:: write_file($path, $data[, $mode = 'wb'])

	:param	string	$path: File 路径
	:param	string	$data: 数据写入 file
	:param	string	$mode: ``fopen()`` 模式
	:returns:	如果写入成功为 TRUE , 万一错误是 FALSE
	:rtype:	bool

	将数据写入指定路径中的文件。如果文件不存在，这个函数将创建文件。

	例如::

		$data = 'Some file data';
		if ( ! write_file('./path/to/file.php', $data))
		{     
			echo 'Unable to write the file';
		}
		else
		{     
			echo 'File written!';
		}

	你能随意地通过第三个参数设置写模式::

		write_file('./path/to/file.php', $data, 'r+');

	 默认模式是'wb'. 模式选项请查看 `PHP 用户指导 <http://php.net/manual/en/function.fopen.php>`_ .

	.. note:: 这个函数向文件里写入数据要按顺序，它的权限必须被设置成可写的。如果文件已经不存在，
	          那么目录下的文件必须是可写的。

	.. note:: 路径关联你的主站的 index.php 文件，不是你的 controller 或者 view 文件。
	          CodeIgniter 用前端 controller 因此路径常常关联主站的 index.

	.. note:: 当写入文件时函数捕获了文件上独占的锁定。

.. php:function:: delete_files($path[, $del_dir = FALSE[, $htdocs = FALSE]])

	:param	string	$path: 目录路径
	:param	bool	$del_dir: 是否也删除目录
	:param	bool	$htdocs: 是否跳过删除 .htaccess 和 index page 文件
	:returns:	万一为FALSE，TRUE 为真
	:rtype:	bool

	删除所有包含在备用路径里的文件。

	例如::

		delete_files('./path/to/directory/');

	如果第二个参数设置为 TRUE，包含备用根路径的任何目录将也会被删除。

	例如::

		delete_files('./path/to/directory/', TRUE);

	.. note:: 文件必须是可写的而已经归属至系统的文件原则上已被删除。

.. php:function:: get_filenames($source_dir[, $include_path = FALSE])

	:param	string	$source_dir: 目录路径
	:param	bool	$include_path: 作为文件名的部分是否包含路径
	:returns:	文件名数组
	:rtype:	array

	函数里取服务器路径输入并返回包含所有文件名的数组。设置第二参数为 TRUE 文件路径能很随意的被添加到文件名里。

	例如::

		$controllers = get_filenames(APPPATH.'controllers/');

.. php:function:: get_dir_file_info($source_dir, $top_level_only)

	:param	string	$source_dir: 目录路径
	:param	bool	$top_level_only: 是否仅仅查看特殊目录 (不包含子目录)
	:returns:	数组涵盖的信息在备用目录的内容中
	:rtype:	array

	阅读指定的目录并建立包含文件名，文件大小，日期和权限的数组。
	如果传送第二个参数被阻止成 FALSE 包含指定目录的子文件夹一定是只读的，如同这是个强调操作。
	

	事例::

		$models_info = get_dir_file_info(APPPATH.'models/');

.. php:function:: get_file_info($file[, $returned_values = array('name', 'server_path', 'size', 'date')])

	:param	string	$file: File 路径
	:param	array	$returned_values: 任何返回的信息类型
	:returns:	在指定文件上的数组包含的信息或失效的 FALSE 
	:rtype:	array

	约定的文件和路径，文件返回（随意地） the *name*, *path*, *size* and *date modified* 属性信息。
	第二参数允许你明确地声明任何你想返回的信息。
	

	有效的 ``$returned_values`` 选项是: `name`, `size`, `date`, `readable`, `writeable`,
	`executable` 和 `fileperms`.

.. php:function:: symbolic_permissions($perms)

	:param	int	$perms: 权限
	:returns:	象征权限的 string
	:rtype:	string

	抓取数值权限（就像是被 ``fileperms()`` 返回的）并且返回文件权限的标准符号记号。

	::

		echo symbolic_permissions(fileperms('./index.php'));  // -rw-r--r--

.. php:function:: octal_permissions($perms)

	:param	int	$perms: 权限
	:returns:	八进制权限的 string
	:rtype:	string

	抓取数值权限（就像是被 ``fileperms()`` 返回的）并且返回文件权限的一个由三个字母组成的八进制记号。 

	::

		echo octal_permissions(fileperms('./index.php')); // 644

.. php:function:: set_realpath($path[, $check_existance = FALSE])

	:param	string	$path: 路径
	:param	bool	$check_existance: 如果路径确实存在是否要去检查
	:returns:	绝对路径
	:rtype:	string

	函数会返回不带符号链接的服务器路径或者有关联的目录结构。
	如果路径不能决定选项的次一级争议将触发一个错误。

	例如::

		$file = '/etc/php5/apache2/php.ini';
		echo set_realpath($file); //  输出 '/etc/php5/apache2/php.ini'

		$non_existent_file = '/path/to/non-exist-file.txt';
		echo set_realpath($non_existent_file, TRUE);	// 显示错误，如同路径不能决定
		echo set_realpath($non_existent_file, FALSE);	// 输出 '/path/to/non-exist-file.txt'

		$directory = '/etc/php5';
		echo set_realpath($directory);	// 输出 '/etc/php5/'

		$non_existent_directory = '/path/to/nowhere';
		echo set_realpath($non_existent_directory, TRUE);	// 显示错误，如同路径不能决定
		echo set_realpath($non_existent_directory, FALSE);	// 输出 '/path/to/nowhere'
