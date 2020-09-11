************************
扩展 Controller
************************

CodeIgniter 的核心类 Controller 不应该被修改, 但是在 **app/Controllers/BaseController.php** 提供了一个默认的 Controller 扩展。
你创建的任何新控制器，都应该继承 ``BaseController`` 以利用组件预加载和你添加的任何其他功能：
::

	<?php namespace App\Controllers;
	
	use CodeIgniter\Controller;
	
	class Home extends BaseController {
	
	}

组件预加载
=====================

基础控制器是每次运行项目时，加载你希望使用的任何 helpers, models, libraries, services 等的好位置。 
Helpers 应该添加到预先提供的 ``$helpers`` 数组。例如, 如果你想要在所有控制器中使用 HTML 和 Text 辅助函数：
::

	protected $helpers = ['html', 'text'];

其他任何要加载的组件或者要处理的数据，都应该添加到 ``initController()`` 中。 例如，如果你的项目要大量使用 Session 类，那你可以在这里启动它：
::

	public function initController(...)
	{
		// Do Not Edit This Line
		parent::initController($request, $response, $logger);
		
		$this->session = \Config\Services::session();
	}

附加方法
==================

基础控制器不可以被路由（系统配置会将它路由到 404 Page Not Found）。作为一项附加的安全措施，你应该将创建的 **所有** 新方法声明为 ``protected`` 或者 ``private``，
并且只允许继承 ``BaseController`` 的控制器进行访问。 

其他配置
=============

你可能会需要多个基础控制器。你可以创建新的基础控制器，只要确保你创建的任何控制器正确继承了基础控制器。例如，你的项目同时有面向普通用户的公共控制器和面向管理员的后台控制器。
则你可以让所有公共控制器继承 ``BaseController`` ，创建一个 ``AdminController`` 让所有后台控制器来继承。

如果你不想使用基础控制器，则可以通过继承系统控制器来代替：
::

	class Home extends \CodeIgniter\Controller
	{
	
	}
