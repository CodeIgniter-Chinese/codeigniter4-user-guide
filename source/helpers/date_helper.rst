###########
日期辅助函数
###########

日期辅助函数文件包含协助处理日期的函数。

.. contents::
  :local:

.. raw:: html

  <div class="custom-index container"></div>

加载日期辅助函数
===================

日期辅助函数以如下代码形式加载::

	helper('date');

通用函数
===================

下面的函数是通用的:

.. php:function:: now([$timezone = NULL])

	:param	string	$timezone: 时区
	:returns:	UNIX 时区戳
	:rtype:	int（整型）

	在你的配置文件里基于"time reference"设定，
	参考任一个你服务器本地时间或者任何PHP支持的时区以UNIX时间戳返回最近的时间。
	如果你没有打算参考任何其他的PHP支持的时区去设置你主要的时间
	（如果你运行一个网站可以让每一个用户设置他们自己的时区设定，你的做法将是具有代表性的。），
	从头到尾使用PHP的 ``time()`` 函数是没有益处的。
	::

		echo now('Australia/Victoria');

	如果没有提供时区，函数会基于 **time_reference**  设定返回 ``time()`` . 
	

.. php:function:: timezone_select([$class = '', $default = '', $what = \DateTimeZone::ALL, $country = null])

	:param	string	$class: 应用于选择范围的任意分类
	:param	string	$default: 首字母选项默认值
	:param	int	$what: 日期时区分类恒量（查看 `listIdentifiers <https://www.php.net/manual/en/datetimezone.listidentifiers.php>`_)
	:param	string	$country: 一份双字母ISO 3166-1 兼容的国家代码（查看 `listIdentifiers <https://www.php.net/manual/en/datetimezone.listidentifiers.php>`_)
	:returns:	预订（HTML）选项
	:rtype:	string（字符串）

	产生一个 `select` 通用时区表格选项（`$what` 和 `$country`可选过滤器 ）。
	你可以提供一个应用于使格式化更简单区域的分类选项，就像默认选择的值一样。
	::

		echo timezone_select('custom-select', 'America/New_York');

在 CodeIgniter 3 ``date_helper`` 许多不成熟的发现已经被移到  CodeIgniter 4 的  ``I18n`` 模块。

