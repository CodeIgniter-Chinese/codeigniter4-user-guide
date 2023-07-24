###########
控制器
###########

控制器是你应用程序的核心,因为它们确定了如何处理 HTTP 请求。

.. contents::
    :local:
    :depth: 2

什么是控制器?
*********************

一个控制器简单来说就是一个处理 HTTP 请求的类文件。:doc:`URI 路由 <routing>` 将一个 URI 与一个控制器关联起来。

你创建的每个控制器都应该扩展 ``BaseController`` 类。
这个类为你所有的控制器提供了几个可用的功能。

.. _controller-constructor:

构造函数
***********

CodeIgniter 的控制器有一个特殊的构造函数 ``initController()``。
它会在 PHP 的构造函数 ``__construct()`` 执行后由框架调用。

如果你想重写 ``initController()``,不要忘记在方法中添加 ``parent::initController($request, $response, $logger);`` :

.. literalinclude:: controllers/023.php

.. important:: 你不能在构造函数中使用 ``return``。所以 ``return redirect()->to('route');`` 不起作用。

``initController()`` 方法设置了以下三个属性。

包含的属性
*******************

CodeIgniter 的控制器提供了这些属性。

请求对象
==============

应用程序的主要 :doc:`请求实例 </incoming/incomingrequest>` 始终作为类属性 ``$this->request`` 可用。

响应对象
===============

应用程序的主要 :doc:`响应实例 </outgoing/response>` 始终作为类属性 ``$this->response`` 可用。

日志对象
=============

:doc:`日志 <../general/logging>` 类的一个实例作为类属性 ``$this->logger`` 可用。

.. _controllers-helpers:

辅助函数
========

你可以将辅助函数文件的数组定义为类属性。每当加载控制器时,这些辅助函数文件都会自动加载到内存中,以便你可以在控制器内的任何地方使用它们的方法:

.. literalinclude:: controllers/001.php

forceHTTPS
**********

所有控制器中都可以使用强制通过 HTTPS 访问方法的便利方法:

.. literalinclude:: controllers/002.php

默认情况下,在支持 HTTP 严格传输安全头的现代浏览器中,此调用应强制浏览器将非 HTTPS 调用转换为一年的 HTTPS 调用。你可以通过传递持续时间(以秒为单位)作为第一个参数来修改此设置:

.. literalinclude:: controllers/003.php

.. note:: 你可以始终使用一些 :doc:`基于时间的常量 </general/common_functions>`,包括 ``YEAR``、``MONTH`` 等。


.. _controllers-validating-data:

验证数据
***************

.. _controller-validate:

$this->validate()
=================

为了简化数据检查,控制器还提供了方便的 ``validate()`` 方法。
该方法在第一个参数中接受规则数组,在可选的第二个参数中,接受自定义错误消息的数组,以在项目无效时显示。在内部,这使用控制器的 ``$this->request`` 实例来获取要验证的数据。

.. warning::
    ``validate()`` 方法使用 :ref:`Validation::withRequest() <validation-withrequest>` 方法。
    它会验证来自 :ref:`$request->getJSON() <incomingrequest-getting-json-data>`
    或 :ref:`$request->getRawInput() <incomingrequest-retrieving-raw-data>`
    或 :ref:`$request->getVar() <incomingrequest-getting-data>` 的数据。
    使用哪些数据取决于请求。请记住,攻击者可以自由地向服务器发送任何请求。

:doc:`验证库文档 </libraries/validation>` 有关于规则和消息数组格式以及可用规则的详细信息:

.. literalinclude:: controllers/004.php

如果你发现在配置文件中保持规则更简单,你可以用 **app/Config/Validation.php** 中定义的组名替换 ``$rules`` 数组:

.. literalinclude:: controllers/005.php

.. note:: 验证也可以在模型中自动处理,但有时在控制器中更容易。由你决定在哪里。

.. _controller-validatedata:

$this->validateData()
=====================

.. versionadded:: 4.2.0

有时你可能想检查控制器方法的参数或其他自定义数据。
在这种情况下,你可以使用 ``$this->validateData()`` 方法。
该方法在第一个参数中接受要验证的数据数组:

.. literalinclude:: controllers/006.php

保护方法
******************

在某些情况下,你可能希望某些方法隐藏不对公众开放。
为此,只需将方法声明为 ``private`` 或 ``protected``。
这将阻止通过 URL 请求提供服务。

例如,如果你为 ``Helloworld`` 控制器定义了一个这样的方法:

.. literalinclude:: controllers/007.php

并为该方法定义一个路由(``helloworld/utitilty``)。然后尝试使用以下 URL 访问它不会起作用::

    example.com/index.php/helloworld/utility

自动路由也不会起作用。

.. _controller-auto-routing-improved:

自动路由(改进)
************************

.. versionadded:: 4.2.0

自 v4.2.0 起,引入了新的更安全的自动路由。

.. note:: 如果你熟悉自动路由,它在 CodeIgniter 3 到 4.1.x 中默认启用,你可以在
    :ref:`ChangeLog v4.2.0 <v420-new-improved-auto-routing>` 中看到差异。

本节描述了新自动路由的功能。
它会自动路由 HTTP 请求,并执行相应的控制器方法,
而无需路由定义。

自 v4.2.0 起,自动路由默认被禁用。要使用它,请参阅 :ref:`enabled-auto-routing-improved`。

考虑这个 URI::

    example.com/index.php/helloworld/

在上面的例子中,启用自动路由后,CodeIgniter 会尝试查找名为 ``App\Controllers\Helloworld`` 的控制器并加载它。

.. note:: 当控制器的短名称与 URI 的第一段匹配时,它会被加载。

让我们试一试:你好,世界!
==========================

让我们创建一个简单的控制器,以便你看到它的实际效果。使用文本编辑器,创建一个名为 **Helloworld.php** 的文件,并将以下代码放入其中。你会注意到 ``Helloworld`` 控制器正在扩展 ``BaseController``。你也可以扩展 ``CodeIgniter\Controller``,如果你不需要 BaseController 的功能的话。

BaseController 为加载组件和执行所有控制器需要的函数提供了方便的位置。你可以在任何新控制器中扩展此类。

.. literalinclude:: controllers/020.php

然后将该文件保存到你的 **app/Controllers** 目录中。

.. important:: 该文件必须命名为 **Helloworld.php**,H 字母大写。当你使用自动路由时,控制器类名称必须以大写字母开头,并且只有第一个字符可以大写。

.. important:: 通过自动路由(改进版)执行的控制器方法需要 HTTP 动词(``get``、``post``、``put`` 等)前缀,如 ``getIndex()``、``postCreate()``。

现在使用类似以下的 URL 访问你的站点::

    example.com/index.php/helloworld

如果你正确执行了,应该会看到::

    Hello World!

有效的写法:

.. literalinclude:: controllers/009.php

无效的写法:

.. literalinclude:: controllers/010.php

无效的写法:

.. literalinclude:: controllers/011.php

此外,始终确保你的控制器扩展父控制器类,以便它可以继承其所有方法。

.. note::
    如果没有与定义的路由匹配,系统将尝试通过匹配每个段与 **app/Controllers** 中的目录/文件来匹配 URI 与控制器。
    这就是为什么你的目录/文件必须以大写字母开头,其余必须是小写字母。

    如果你想要另一种命名约定,你需要使用 :ref:`定义路由 <defined-route-routing>` 手动定义它。
    这里有一个基于 PSR-4 自动加载的例子:

    .. literalinclude:: controllers/012.php

方法
=======

方法可见性
-----------------

当你定义通过 HTTP 请求可执行的方法时,该方法必须声明为 ``public``。

.. warning:: 为了安全起见,请确保将任何新实用程序方法声明为 ``protected`` 或 ``private``。

默认方法
--------------

在上面的示例中,方法名称是 ``getIndex()``。
方法(HTTP 动词 + ``Index()``)称为 **默认方法**,如果 URI 的 **第二段** 为空,则加载它。

普通方法
--------------

URI 的第二段通常确定控制器中的哪个方法被调用。

让我们试一试。向你的控制器添加一个新方法:

.. literalinclude:: controllers/021.php

现在加载以下 URL 以查看 ``getComment()`` 方法::

    example.com/index.php/helloworld/comment/

你应该会看到你的新消息。

将 URI 段传递给你的方法
====================================

如果 URI 包含超过两个段,它们将作为参数传递给你的方法。

例如,假设你有这样的 URI::

    example.com/index.php/products/shoes/sandals/123

你的方法将获取传入 URI 的第 3 和第 4 段(``'sandals'`` 和 ``'123'``):

.. literalinclude:: controllers/022.php

.. important:: 如果 URI 中的参数比方法的参数更多,
    自动路由(改进版)不会执行该方法,并导致 404
    未找到。

默认控制器
==================

默认控制器是一个特殊的控制器,当 URI 以目录名称结束时使用,或者当 URI 不存在时使用,这种情况将在仅请求站点根 URL 时出现。

定义默认控制器
-----------------------------

让我们用 ``Helloworld`` 控制器试一试。

要指定默认控制器,请打开 **app/Config/Routes.php** 文件并设置此变量:

.. literalinclude:: controllers/015.php

其中 ``Helloworld`` 是希望用作默认控制器的控制器类名称。

在 **Routes.php** 中的“路由定义”部分向下几行,注释掉该行:

.. literalinclude:: controllers/016.php

现在如果在不指定任何 URI 段的情况下浏览你的站点,你将看到 "Hello World" 消息。

.. important:: 当你使用自动路由(改进版)时,你必须删除 ``$routes->get('/', 'Home::index');`` 这一行。因为定义的路由优先于自动路由,并且出于安全考虑,自动路由(改进版)拒绝定义路由中的控制器访问。

有关更多信息,请参阅 :ref:`routes-configuration-options` 部分
:ref:`URI 路由 <routing-auto-routing-improved-configuration-options>` 文档。

将控制器组织到子目录中
================================================

如果你正在构建一个大型应用程序,你可能希望以分层的方式组织或结构化控制器到子目录中。CodeIgniter
允许你执行此操作。

只需在主 **app/Controllers** 下创建子目录,并将控制器类放在其中。

.. important:: 目录名称必须以大写字母开头,并且只有第一个字符可以大写。

使用此功能时,URI 的第一段必须指定目录。例如,假设你有一个位于这里的控制器::

    app/Controllers/Products/Shoes.php

要调用上面的控制器,你的 URI 将如下所示::

    example.com/index.php/products/shoes/show/123

.. note:: 你不能在 **app/Controllers** 和 **public** 中有相同名称的目录。
    这是因为如果存在目录,web 服务器将搜索它,而不会路由到 CodeIgniter。

你的每个子目录都可以包含一个默认控制器,如果 URL 只包含 *子目录*,则会调用该控制器。只需把一个控制器放在那里,使其与 **app/Config/Routes.php** 文件中指定的默认控制器名称匹配即可。

CodeIgniter 还允许你使用其 :ref:`定义的路由 <defined-route-routing>` 映射 URI。

.. _controller-auto-routing-legacy:

自动路由(传统)
*********************

本节描述自动路由(传统)的功能,这是 CodeIgniter 3 的路由系统。
它会自动路由 HTTP 请求,并执行相应的控制器方法,
而无需路由定义。自动路由默认被禁用。

.. warning:: 为了防止配置错误和编码错误,我们建议你不要使用
    自动路由(传统)。很容易创建漏洞应用,其中控制器过滤器
    或 CSRF 保护被绕过。

.. important:: 自动路由(传统)会将任何 HTTP 方法的 HTTP 请求路由到控制器方法。

考虑这个 URI::

    example.com/index.php/helloworld/

在上面的例子中,CodeIgniter 会尝试查找一个名为 **Helloworld.php** 的控制器并加载它。

.. note:: 当控制器的短名称与 URI 的第一段匹配时,它会被加载。

让我们试一试:你好,世界!(传统)
===================================

让我们创建一个简单的控制器,以便你看到它的实际效果。使用文本编辑器,创建一个名为 **Helloworld.php** 的文件,并将以下代码放入其中。你会注意到 ``Helloworld`` 控制器正在扩展 ``BaseController``。你也可以扩展 ``CodeIgniter\Controller``,如果你不需要 BaseController 的功能的话。

BaseController 为加载组件和执行所有控制器需要的函数提供了方便的位置。你可以在任何新控制器中扩展此类。

出于安全考虑,请确保将任何新实用程序方法声明为 ``protected`` 或 ``private``:

.. literalinclude:: controllers/008.php

然后将该文件保存到你的 **app/Controllers** 目录中。

.. important:: 该文件必须命名为 **Helloworld.php**,H 字母大写。当你使用自动路由时,控制器类名称必须以大写字母开头,并且只有第一个字符可以大写。

现在使用类似以下的 URL 访问你的站点::

    example.com/index.php/helloworld

如果你正确执行了,应该会看到::

    Hello World!

有效的写法:

.. literalinclude:: controllers/009.php

无效的写法:

.. literalinclude:: controllers/010.php

无效的写法:

.. literalinclude:: controllers/011.php

此外,始终确保你的控制器扩展父控制器类,以便它可以继承其所有方法。

.. note::
    如果没有与定义的路由匹配,系统将尝试通过匹配每个段与 **app/Controllers** 中的目录/文件来匹配 URI 与控制器。
    这就是为什么你的目录/文件必须以大写字母开头,其余必须是小写字母。

    如果你想要另一种命名约定,你需要使用 :ref:`定义路由 <defined-route-routing>` 手动定义它。
    这里有一个基于 PSR-4 自动加载的例子:

    .. literalinclude:: controllers/012.php

方法(传统)
=================

在上面的示例中,方法名称是 ``index()``。``index()`` 方法如果 URI 的 **第二段** 为空,总是被默认加载。另一种显示“Hello World”消息的方法是::

    example.com/index.php/helloworld/index/

**URI的第二段决定了控制器中调用哪个方法。**

让我们试一试。在你的控制器中添加一个新方法:

.. literalinclude:: controllers/013.php

现在使用下面的 URL 来查看 comment 方法的效果::

    example.com/index.php/helloworld/comment/

你应该可以看到新的消息。

将 URI 段传递给你的方法(传统)
=============================================

如果 URI 包含两个以上段,则会作为参数传递给你的方法。

例如,假设你有这样的一个 URI::

    example.com/index.php/products/shoes/sandals/123

你的方法将获取传入的 URI 的第 3 和第 4 段(``'sandals'`` 和 ``'123'``):

.. literalinclude:: controllers/014.php

默认控制器(传统)
===========================

默认控制器是一个特殊的控制器,在 URI 以目录名结束或者 URI 不存在的情况下使用,这通常发生在仅请求站点根 URL 的情况。

定义默认控制器(传统)
--------------------------------------

让我们以 ``Helloworld`` 控制器为例。

要指定默认控制器,打开配置文件 **app/Config/Routes.php**,设置如下变量:

.. literalinclude:: controllers/015.php

其中 ``Helloworld`` 是希望用作默认控制器的控制器类名称。

在 **Routes.php** 的“路由定义”部分,注释掉如下行:

.. literalinclude:: controllers/016.php

现在如果在不指定任何 URI 段的情况下浏览你的站点,你将看到 "Hello World" 消息。

.. note:: ``$routes->get('/', 'Home::index');`` 这一行是优化,在“真实的”应用中会使用。但是为了演示的目的,我们不想使用这个功能。``$routes->get()`` 在 :doc:`URI 路由 <routing>` 中有解释。

有关更多信息,请参阅 :ref:`routes-configuration-options` 部分
:ref:`URI 路由 <routing-auto-routing-legacy-configuration-options>` 文档。

将控制器组织到子目录中(传统)
==========================================================

如果你正在构建一个大型应用程序,你可能需要分层组织控制器结构到子目录中。CodeIgniter 支持这种方式。

只需要在主目录 **app/Controllers** 下创建子目录,并将控制器类放入其中即可。

.. important:: 目录名称必须以大写字母开头,只有首字母可以大写。

使用此功能时,URI 的第一段必须指定目录。例如,假设你有一个位于如下位置的控制器::

    app/Controllers/Products/Shoes.php

要调用上述控制器,你的 URI 将是这样::

    example.com/index.php/products/shoes/show/123

.. note:: 在 **app/Controllers** 和 **public** 中不能有同名的目录。这是因为如果目录存在,web 服务器会进行查找,路由不会转到 CodeIgniter。

每个子目录下可以包含一个默认控制器,如果 URL 仅包含 **子目录**,则会调用该默认控制器。只需在相应位置放置一个控制器,使其与 **app/Config/Routes.php** 文件中指定的默认控制器名称匹配即可。

CodeIgniter 也支持通过 :ref:`定义路由 <defined-route-routing>` 来映射 URI。

重映射方法调用
**********************

.. note:: **自动路由(改进版)** 有意不支持此功能。

如上所述,URI的第二段通常决定控制器中调用哪个方法。CodeIgniter 允许你通过使用 ``_remap()`` 方法来覆盖此行为:

.. literalinclude:: controllers/017.php

.. important:: 如果你的控制器包含名为 ``_remap()`` 的方法,无论 URI 包含什么,它都将 **始终** 被调用。它会覆盖 URI 决定调用哪个方法的正常行为,允许你定义自己的方法路由规则。

被覆盖的方法调用(通常是 URI 的第二段)将作为参数传递给 ``_remap()`` 方法:

.. literalinclude:: controllers/018.php

在方法名之后任何多余的段也会作为参数传递给 ``_remap()``。这些参数可以传递给该方法,以模拟 CodeIgniter 的默认行为。

例子:

.. literalinclude:: controllers/019.php

扩展控制器
************************

如果你想扩展控制器,请查看 :doc:`../extending/basecontroller`。

就这样了！
**********

这基本上就是关于控制器需要了解的所有内容。
