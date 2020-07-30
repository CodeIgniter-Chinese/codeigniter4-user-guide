################
用户代理类
################

用户代理类提供的函数有助于识别浏览器，移动设备或者正访问您网站的机器人程序的信息。


.. contents::
    :local:
    :depth: 2

**************************
使用用户代理类
**************************

初始化类
======================

用户代理类经常从当前的实例文件 :doc:`IncomingRequest </incoming/incomingrequest>`  直接获得。
默认情况下，你可以在你的控制器类里请求实例并且你能从下面方法中重新获得用户代理类::


	$agent = $this->request->getUserAgent();

用户代理定义
======================

用户代理名字定义在一个配置文件里，该文件位于 **app/Config/UserAgents.php**.  
如果必要的话，你可以添加条目到不同的用户代理数组中。

示例
=======

当用户代理类被初始化时，它将会尝试确认用户代理正在浏览你的网站是否是网络浏览器、移动设备或者一个机器人。
如果参数是可获得的，它也将会搜集平台信息::


	$agent = $this->request->getUserAgent();

	if ($agent->isBrowser())
	{
		$currentAgent = $agent->getBrowser().' '.$agent->getVersion();
	}
	elseif ($agent->isRobot())
	{
		$currentAgent = $this->agent->robot();
	}
	elseif ($agent->isMobile())
	{
		$currentAgent = $agent->getMobile();
	}
	else
	{
		$currentAgent = 'Unidentified User Agent';
	}

	echo $currentAgent;

	echo $agent->getPlatform(); // Platform info (Windows, Linux, Mac, etc.)

***************
类参考
***************

.. php:class:: CodeIgniter\\HTTP\\UserAgent

	.. php:method:: isBrowser([$key = NULL])

		:param	string	$key: 可选浏览器名称
    		:returns:	如果用户代理是（指定的）用户浏览器则为 TRUE，否则为 FALSE
    		:rtype:	bool（布尔类型）

    		如果用户代理是已知的网络浏览器，则返回 TRUE/FALSE (boolean/布尔型)。
    		::

			if ($agent->isBrowser('Safari'))
			{
				echo 'You are using Safari.';
			}
			elseif ($agent->isBrowser())
			{
				echo 'You are using a browser.';
			}

		.. note:: 本例中的字符串 "Safari" 是浏览器定义列表中的数组键。
		如果你想添加新的浏览器或者改变字符串，你可以在 **app/Config/UserAgents.php** 中找到这个列表。
	.. php:method:: isMobile([$key = NULL])

		:param	string	$key: 可选的移动设备名称
    		:returns:  如果用户代理是（指定的）用户浏览器则为 TRUE，否则为 FALSE 
    		:rtype:	bool（布尔类型）

    		如果用户代理是已知的移动设备，则返回 TRUE/FALSE (boolean/布尔类型)。
    		::

			if ($agent->isMobile('iphone'))
			{
				echo view('iphone/home');
			}
			elseif ($agent->isMobile())
			{
				echo view('mobile/home');
			}
			else
			{
				echo view('web/home');
			}

	.. php:method:: isRobot([$key = NULL])

		:param	string	$key: 可选的机器人名称
    		:returns:	如果用户代理是（指定的）用户浏览器则为 TRUE，否则为 FALSE 
    		:rtype:	bool（布尔类型）

    		如果用户代理是已知的机器人，则返回 TRUE/FALSE (boolean/布尔类型)  。

    		.. note:: 用户代理库仅包括最常见的机器人定义。
		它不是完整的机器人列表。因此搜索数百个中的一个并不是完全有效的。
		如果你发现列表中通常访问你网站的机器人丢失了，你能添加它们到你的 **app/Config/UserAgents.php** 文件里。

	.. php:method:: isReferral()

		:returns:	如果过用户代理推荐则为 TRUE， 否则为 FALSE
		:rtype:	bool（布尔类型）

		如果来自其他站点的用户代理被推荐，则返回 TRUE/FALSE (boolean)。	

	.. php:method:: getBrowser()

		:returns:	检测浏览器或者空字符串
		:rtype:	string（字符串类型）

		返回一个包含正查看你网站的网络浏览器的名称。

	.. php:method:: getVersion()

		:returns:	检测浏览器版本或者空字符串
		:rtype:	string（字符串类型）

		返回一个包含正查看你网站的网络浏览器的版本号。

	.. php:method:: getMobile()

		:returns:	检测移动设备品牌或者空字符串
		:rtype:	string（字符串类型）

		返回一个包含正查看你网站的移动设备名称。

	.. php:method:: getRobot()

		:returns:	检测机器人名称或者空字符串
		:rtype:	string（字符串类型）

		返回一个包含正查看你网站机器人名称。

	.. php:method:: getPlatform()

		:returns:	检测操作系统或者空字符串
		:rtype:	string（字符串类型）

		返回一个包含正查看你网站系统平台（Linux, Windows, OS X, etc.）.

	.. php:method:: getReferrer()

		:returns:	检测引用页或者空字符串
		:rtype:	string（字符串类型）

		引用页，如果用户代理从其他网站被推荐。通常的你将对如下代码测试::

			if ($agent->isReferral())
			{
				echo $agent->referrer();
			}

	.. php:method:: getAgentString()

		:returns:	完整的用户代理字符串或者空字符串
		:rtype:	string（字符串类型）

		返回一个包含完整用户代理的字符串。通常它就像下面所述这样::

			Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.0.4) Gecko/20060613 Camino/1.0.2

	.. php:method:: parse($string)

		:param	string	$string: 自定义用户代理字符串
    		:rtype:	void（空值）

    		由最近浏览者解析定制的用户代理字符串，不同于报告上描述的。
