################
CodeIgniter URL
################

在默认情况下，CodeIgniter 中的 URL 被设计成对搜索引擎和用户友好的样式。 不同于使用传统的在动态系统中使用代词的标准 “查询字符串” 的方式，CodeIgniter 使用基于段的方法::

	example.com/news/article/my_article

URI 分段
============

如果遵循模型-视图-控制器模式，那么 URI 中的每一段通常表示下面的含义::

	example.com/class/method/ID

1. 第一段表示要调用的控制器 **类** ;
2. 第二段表示要调用的类中的 **函数** 或 **方法** ；
3. 第三段以及后面的段代表传给控制器的参数，如 ID 或其他任何变量；

:doc:`URI 类 <../libraries/uri>` 和 :doc:`URL 辅助函数 <../helpers/url_helper>` 包含了一些函数可以让你更容易的处理 URI 数据。此外，可以通过 :doc:`URI 路由 </incoming/routing>` 的方式进行重定向你的 URL 从而使得程序更加灵活。


移除 index.php 文件
===========================

默认情况，你的 URL 中会包含 **index.php** 文件::

	example.com/index.php/news/article/my_article


如果你的服务器支持重写 URL ，那么通过 URL 重写，我们可以轻易的去除这个文件。在不同的服务器中，处理方式各异，故而如下我们主要展示两个最为通用的 Web 服务器。

Apache服务器
-----------------

Apache需要开启 *mod_rewrite* 扩展。当开启时，我们可以使用一个 ``.htaccess`` 文件以及一些简单的规则来实现 URL 重写。如下为这个文件的一个样例，其中使用了”否定“方法来排除某些不需要重定向的项目:

.. code-block:: apache

	RewriteEngine On
	RewriteCond %{REQUEST_FILENAME} !-f
	RewriteCond %{REQUEST_FILENAME} !-d
	RewriteRule ^(.*)$ index.php/$1 [L]

在上面的例子中，除已存在的目录和文件外，其他的 HTTP 请求都会经过你的 index.php 文件。

.. note:: 这些规则并不是对所有服务器配置都有效。

.. note:: 确保使用上面的规则时，排除掉那些你希望能直接访问到的资源。

NGINX
-----
在NGINX中，我们可以定义一个 location 块并用 ``try_files`` 导向来取得如上文中 Apache 配置一样的效果:

.. code-block:: nginx

	location / {
            try_files $uri $uri/ /index.php/$args;
	}

服务器将会首先寻找符合对应 URI 的文件或目录（对于每个文件，通过根目录和别名目录来构建其完整的路径），然后再将其他的请求发送至 index.php 文件中。
