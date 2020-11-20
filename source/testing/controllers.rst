###################
测试控制器
###################

以一对新的辅助函数类和特性测试你的控制器较方便。
当测试控制器时，你能在控制器内执行代码，在通过整体应用 bootstrap 进程第一次运行之外。
大部分时候，使用  `Feature Testing tools <feature.html>`_  是简单的，但是在这里的功能是以备你需要它。


.. note:: 因为整体框架不需要被引导，以这个方式将会有很多次你不能测试控制器 。



特性辅助函数
================

你能使用任何一个基于测试的类，但是你需要在你的测试里使用 ``ControllerTester`` 特性::


    <?php namespace CodeIgniter;

    use CodeIgniter\Test\ControllerTester;

    class TestControllerA extends \CIDatabaseTestCase
    {
        use ControllerTester;
    }

一旦特性已经包含在里面，你能开始设置环境，包括请求和响应类，请求正文，URI ，甚至更多。
你要特别指定控制器使用 ``controller()`` 方法，通过你的控制器的完全地有资格的类名字。
最终，以方法的名字调用 ``execute()`` 方法作为参数去运行::


    <?php namespace CodeIgniter;

    use CodeIgniter\Test\ControllerTester;

    class TestControllerA extends \CIDatabaseTestCase
    {
        use ControllerTester;

        public function testShowCategories()
        {
            $result = $this->withURI('http://example.com/categories')
                           ->controller(\App\Controllers\ForumController::class)
                           ->execute('showCategories');

            $this->assertTrue($result->isOK());
        }
    }


辅助函数方法
==============

**controller($class)**

明确说明去测试的控制器的类名字。第一参数必须是完全地有资格的类名。（例如：包含命名空间）::

    $this->controller(\App\Controllers\ForumController::class);

**execute($method)**

在控制器内执行具体指定的方法。仅有的参数是方法的名称要运行::

    $results = $this->controller(\App\Controllers\ForumController::class)
                    ->execute('showCategories');

对于检查自身的响应这个例子返回一个新的辅助函数类并提供常规数目。详细情况查看下面的例子。


**withConfig($config)**

允许你通过修改的 **Config\App.php** 版本测试不同的设置::

    $config = new Config\App();
    $config->appTimezone = 'America/Chicago';

    $results = $this->withConfig($config)
                    ->controller(\App\Controllers\ForumController::class)
                    ->execute('showCategories');

如果你不提供设置，应用程序 App 配置文件将会被使用。

**withRequest($request)**

允许你去提供 **IncomingRequest** 接口定制到你的测试需求::

    $request = new CodeIgniter\HTTP\IncomingRequest(new Config\App(), new URI('http://example.com'));
    $request->setLocale($locale);

    $results = $this->withRequest($request)
                    ->controller(\App\Controllers\ForumController::class)
                    ->execute('showCategories');

如果你不提供接口，带默认应用值的新的传入请求接口将会传入你的控制器。


**withResponse($response)**

允许你提供 **Response** 接口::

    $response = new CodeIgniter\HTTP\Response(new Config\App());

    $results = $this->withResponse($response)
                    ->controller(\App\Controllers\ForumController::class)
                    ->execute('showCategories');

如果你没有提供接口，带默认应用值的新的应答接口将会传入你的控制器。


**withLogger($logger)**

允许你提供 **Logger** 接口::


    $logger = new CodeIgniter\Log\Handlers\FileHandler();

    $results = $this->withResponse($response)
                    ->withLogger($logger)
                    ->controller(\App\Controllers\ForumController::class)
                    ->execute('showCategories');

如果你没有提供接口，带默认配置值的新的记录器接口会进入到你的控制器。


**withURI($uri)**

当这个控制器运行时，允许你去提供新 URI 并且模仿过去一直观察的 URL 客户端。
在你的控制器内如果你需要检查 URI 部分这是有帮助的。
仅有的参数是象征 URI 有效的字符串::


    $results = $this->withURI('http://example.com/forums/categories')
                    ->controller(\App\Controllers\ForumController::class)
                    ->execute('showCategories');

在测试躲避突袭事件时间内，常常提供 URI 是好习惯。

**withBody($body)**

对于请求允许你提供订制的正文。
当测试你需要设置 JSON 值作为正文的 API 控制器时这能是有帮助的。
仅有的参数值是描述请求正文的字符串::


    $body = json_encode(['foo' => 'bar']);

    $results = $this->withBody($body)
                    ->controller(\App\Controllers\ForumController::class)
                    ->execute('showCategories');


检查应答
=====================

当控制器执行时，新的 **ControllerResponse** 接口会返回并且提供有帮助办法的数字，以及直接存取到请求和应答的产生。


**isOK()**

这个方法提供简单的检查照顾 "successful" 的应答。这首先要检查 HTTP 状态编码在 200 或者 300 范围内::


    $results = $this->withBody($body)
                    ->controller(\App\Controllers\ForumController::class)
                    ->execute('showCategories');

    if ($results->isOK())
    {
        . . .
    }

**isRedirect()**

如果最终的应答是一些分类的重定向要检查以查看::

    $results = $this->withBody($body)
                    ->controller(\App\Controllers\ForumController::class)
                    ->execute('showCategories');

    if ($results->isRedirect())
    {
        . . .
    }

**request()**

你能存取带这个方法产生的请求对象::

    $results = $this->withBody($body)
                    ->controller(\App\Controllers\ForumController::class)
                    ->execute('showCategories');

    $request = $results->request();

**response()**

这个控制器允许你存取被应答产生的对象，如果有的话::


    $results = $this->withBody($body)
                    ->controller(\App\Controllers\ForumController::class)
                    ->execute('showCategories');

    $response = $results->response();

**getBody()**

你能存取应答的正文将被发送到带  **getBody()** 方法的客户端。这能产生 HTML，或 JSON 应答，等等。::

    $results = $this->withBody($body)
                    ->controller(\App\Controllers\ForumController::class)
                    ->execute('showCategories');

    $body = $results->getBody();


应答辅助函数方法
-----------------------

你找回包含辅助函数方法的数字的应答去审查在应答内的 HTML 输出。在你的测试里，这些在声明内的使用是有益的。
如果该方法自己确凿存在，或者在更多具体地标签 （tag） 内，就像具体指定的类型 （type），类（class），或者标识符 (id)，在页面上 **see()**  方法检查页面的文本要领会。
::


    // 检查页面上的 "Hello World"
    $results->see('Hello World');
    // 检查包含 h1 标签（tag）内的 "Hello World" 
    $results->see('Hello World', 'h1');
    // 检查带 "notice" 类要素内的 "Hello World"
    $results->see('Hello World', '.notice');
    // 检查带 "title" 的标识符（id）要素内的 "Hello World" 
    $results->see('Hellow World', '#title');


**dontSee()** 方法是准确对立的::

    // 在页面上检查不确定的 "Hello World"
    $results->dontSee('Hello World');
    // 检查在任何 h1 标签（tag）内的不确定的 "Hellow World" 
    $results->dontSee('Hello World', 'h1');

**seeElement()** 和 **dontSeeElement()** 是与前面的方法是相似的，但是不要看要素的值。取而代之的是，特们简单地检查页面上确定的要素::

    // 检查带确凿的 'notice' 类的要素
    $results->seeElement('.notice');
    // 检查带确凿的 'title' 标识符（id）的要素
    $results->seeElement('#title')
    // 查证带不确凿的 'title' 标识符（id）的要素
    $results->dontSeeElement('#title');

你能使用 **seeLink()** 确保出现在页面上带具体指定文本的连接::


    // 检查带 'Upgrade Account' 确凿的连接作为文本::
    $results->seeLink('Upgrade Account');
    // 检查带 'Upgrade Account' 确凿的连接作为文本，以及 'upsell' 类 
    $results->seeLink('Upgrade Account', '.upsell');

对于任何确凿的带名字和值的输入标签 **seeInField()** 方法要检查::

    // 用 'John Snow' 值 检查确凿输入命名的 'user'  
    $results->seeInField('user', 'John Snow');
    // 检查多层面的输入
    $results->seeInField('user[name]', 'John Snow');

最后，你要检查是否复选框（checkbox） 确凿并且用 **seeCheckboxIsChecked()** 方法检查::


    // 检查是否带 'foo' 的类的复选框（checkbox）已经检查
    $results->seeCheckboxIsChecked('.foo');
    // 检查是否带 'bar' 标识符（id）的复选框（checkbox）已经检查 
    $results->seeCheckboxIsChecked('#bar');
