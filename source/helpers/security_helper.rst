###############
安全辅助函数
###############

安全辅助函数文件包含安全相关联的函数。

.. contents::
  :local:

加载安全辅助函数
===================

安全辅助函数使用下面的代码加载::

	helper('security');

通用函数
===================

下面是通用函数:

.. php:function:: sanitize_filename($filename)

	:param	string	$filename: 文件名
    	:returns:	净化文件名
    	:rtype:	string

    	提供保护来应对磁盘遍历。

    	对于 ``\CodeIgniter\Security::sanitize_filename()`` 本函数仅是别名。
	更多信息，请查看文档  :doc:`Security Library <../libraries/security>` 。


.. php:function:: strip_image_tags($str)

	:param	string	$str: 输入 string
    	:returns:	无成像标签的输入
    	:rtype:	string

        这是一个将无成像标签从 string 中剥去的安全函数。它留下成像 URL 就像清楚的文本一样。   

    	例如::

		$string = strip_image_tags($string);

.. php:function:: encode_php_tags($str)

	:param	string	$str: 输入 string
    	:returns:	安全地格式化 string
    	:rtype:	string

    	这是一个安全函数去转换 PHP 标签为实体。

	例如::

		$string = encode_php_tags($string);
