###########
控制器
###########

控制器是你应用程序的核心，因为它们决定了如何处理 HTTP 请求。

.. contents::
    :local:
    :depth: 2

什么是控制器？
*********************

控制器只是一个处理 HTTP 请求的类文件。:doc:`URI 路由 <routing>` 将 URI 与控制器关联。它返回一个视图字符串或 ``Response`` 对象。

你创建的每个控制器都应该继承 ``BaseController`` 类。这个类提供了几个可用于所有控制器的功能。

.. _controller-constructor:

构造函数
***********

CodeIgniter 的控制器有一个特殊的构造函数 ``initController()``。它将在 PHP 的构造函数 ``__construct()`` 执行后由框架调用。

如果你想重写 ``initController()``，不要忘记在方法中添加 ``parent::initController($request, $response, $logger);``：

.. literalinclude:: controllers/023.php

.. important:: 你不能在构造函数中使用 ``return``。所以 ``return redirect()->to('route');`` 不起作用。

``initController()`` 方法设置以下三个属性。

包含的属性
*******************

CodeIgniter 的控制器提供这些属性。

Request 对象
==============

应用程序的主 :doc:`Request 实例 </incoming/incomingrequest>` 始终可用作类属性 ``$this->request``。

Response 对象
===============

应用程序的主 :doc:`Response 实例 </outgoing/response>` 始终可用作类属性 ``$this->response``。

Logger 对象
=============

:doc:`Logger <../general/logging>` 类的实例可用作类属性 ``$this->logger``。

.. _controllers-helpers:

辅助函数
========

你可以将辅助函数文件的数组定义为类属性。每当加载控制器时，这些辅助函数文件都会自动加载到内存中，以便你可以在控制器内的任何地方使用它们的方法：

.. literalinclude:: controllers/001.php

forceHTTPS
**********

所有控制器都提供了一个方便的方法来强制通过 HTTPS 访问方法：

.. literalinclude:: controllers/002.php

默认情况下，在支持 HTTP 严格传输安全标头的现代浏览器中，此调用应该强制浏览器将非 HTTPS 调用转换为 HTTPS 调用一年。你可以通过将持续时间（以秒为单位）作为第一个参数传递来修改这一点：

.. literalinclude:: controllers/003.php

.. note:: 许多 :doc:`基于时间的常量 </general/common_functions>` 始终可供你使用，包括 ``YEAR``、``MONTH`` 等等。

.. _controllers-validating-data:

验证数据
***************

.. _controller-validatedata:

$this->validateData()
=====================

.. versionadded:: 4.2.0

为了简化数据检查，控制器还提供了便利方法 ``validateData()``。

该方法接受 (1) 要验证的数据数组，(2) 规则数组，(3) 如果项目无效时显示的可选自定义错误消息数组，(4) 要使用的可选数据库组。

:doc:`验证库文档 </libraries/validation>` 详细说明了规则和消息数组格式，以及可用的规则：

.. literalinclude:: controllers/006.php

.. _controller-validate:

$this->validate()
=================

.. important:: 此方法仅为向后兼容而存在。不要在新项目中使用它。即使你已经在使用它，我们建议你改用 ``validateData()`` 方法。

控制器还提供了便利方法 ``validate()``。

.. warning:: 不要使用 ``validate()``，而要使用 ``validateData()`` 来仅验证 POST 数据。``validate()`` 使用 ``$request->getVar()``，它会按顺序返回 ``$_GET``、``$_POST`` 或 ``$_COOKIE`` 数据（取决于 php.ini `request-order <https://www.php.net/manual/zh/ini.core.php#ini.request-order>`_）。较新的值会覆盖较旧的值。如果 POST 值与 Cookie 同名，则可能会被覆盖。

该方法在第一个参数中接受规则数组，在可选的第二个参数中，接受如果项目无效时显示的自定义错误消息数组。

在内部，这使用控制器的 ``$this->request`` 实例来获取要验证的数据。

:doc:`验证库文档 </libraries/validation>` 详细说明了规则和消息数组格式，以及可用的规则：

.. literalinclude:: controllers/004.php

.. warning:: 当你使用 ``validate()`` 方法时，你应该使用 :ref:`getValidated() <validation-getting-validated-data>` 方法来获取已验证的数据。因为 ``validate()`` 方法内部使用了 :ref:`Validation::withRequest() <validation-withrequest>` 方法，它验证来自 :ref:`$request->getJSON() <incomingrequest-getting-json-data>` 或 :ref:`$request->getRawInput() <incomingrequest-retrieving-raw-data>` 或 :ref:`$request->getVar() <incomingrequest-getting-data>` 的数据，攻击者可能会更改验证的数据。

.. note:: :ref:`$this->validator->getValidated() <validation-getting-validated-data>` 方法从 v4.4.0 开始可用。

如果你发现将规则保存在配置文件中更简单，你可以用在 **app/Config/Validation.php** 中定义的组名替换 ``$rules`` 数组：

.. literalinclude:: controllers/005.php

.. note:: 验证也可以在模型中自动处理，但有时在控制器中处理更容易。这由你决定。

保护方法
******************

在某些情况下，你可能希望某些方法不被公开访问。要实现这一点，只需将方法声明为 ``private`` 或 ``protected``。这将防止它被 URL 请求访问。

例如，如果你为 ``Helloworld`` 控制器定义了这样一个方法：

.. literalinclude:: controllers/007.php

并为该方法定义路由（``helloworld/utitilty``）。然后尝试使用以下 URL 访问它将不起作用::

    example.com/index.php/helloworld/utility

自动路由也不会起作用。

.. _controller-auto-routing-improved:

自动路由（改进版）
************************

.. versionadded:: 4.2.0

自动路由（改进版）是一个新的、更安全的自动路由系统。

详情请参见 :doc:`auto_routing_improved`。

.. _controller-auto-routing-legacy:

自动路由（传统版）
*********************

.. important:: 此功能仅为向后兼容而存在。不要在新项目中使用它。即使你已经在使用它，我们建议你改用 :ref:`auto-routing-improved`。

本节描述了自动路由（传统版）的功能，这是来自 CodeIgniter 3 的路由系统。它自动路由 HTTP 请求，并执行相应的控制器方法，无需路由定义。自动路由默认是禁用的。

.. warning:: 为了防止配置错误和编码错误，我们建议你不要使用自动路由（传统版）。很容易创建漏洞应用程序，控制器过滤器或 CSRF 保护会被绕过。

.. important:: 自动路由（传统版）使用 **任何** HTTP 方法将 HTTP 请求路由到控制器方法。

.. important:: 从 v4.5.0 开始，如果自动路由（传统版）找不到控制器，它会在控制器过滤器执行之前抛出 ``PageNotFoundException`` 异常。

考虑这个 URI::

    example.com/index.php/helloworld/

在上面的例子中，CodeIgniter 将尝试找到名为 **Helloworld.php** 的控制器并加载它。

.. note:: 当控制器的短名称与 URI 的第一段匹配时，它将被加载。

让我们试试：Hello World!（传统版）
===================================

让我们创建一个简单的控制器，这样你就能看到它的实际效果。使用你的文本编辑器，创建一个名为 **Helloworld.php** 的文件，并在其中放入以下代码。你会注意到 ``Helloworld`` 控制器继承了 ``BaseController``。如果你不需要 BaseController 的功能，你也可以继承 ``CodeIgniter\Controller``。

BaseController 为加载组件和执行所有控制器需要的功能提供了一个方便的地方。你可以在任何新控制器中继承这个类。

出于安全考虑，请确保将任何新的实用方法声明为 ``protected`` 或 ``private``：

.. literalinclude:: controllers/008.php

然后将文件保存到你的 **app/Controllers** 目录。

.. important:: 文件必须命名为 **Helloworld.php**，带有大写字母 ``H``。当你使用自动路由时，控制器类名必须以大写字母开头，并且只有第一个字符可以大写。

现在使用类似于这样的 URL 访问你的网站::

    example.com/index.php/helloworld

如果你做对了，你应该看到::

    Hello World!

这是有效的：

.. literalinclude:: controllers/009.php

这是 **无效的**：

.. literalinclude:: controllers/010.php

这是 **无效的**：

.. literalinclude:: controllers/011.php

另外，始终确保你的控制器继承父控制器类，以便它可以继承其所有方法。

.. note::
    当没有找到与定义路由匹配的内容时，系统将尝试通过将每个段与 **app/Controllers** 中的目录/文件匹配来匹配 URI 与控制器。这就是为什么你的目录/文件必须以大写字母开头，其余部分必须是小写。

    如果你想要其他命名约定，你需要使用 :ref:`定义路由 <defined-route-routing>` 手动定义它。这里有一个基于 PSR-4 自动加载器的例子：

    .. literalinclude:: controllers/012.php

方法（传统版）
================

在上面的例子中，方法名是 ``index()``。如果 URI 的 **第二段** 为空，则总是默认加载 ``index()`` 方法。另一种显示"Hello World"消息的方法是这样::

    example.com/index.php/helloworld/index/

**URI 的第二段确定调用控制器中的哪个方法。**

让我们试试。向你的控制器添加一个新方法：

.. literalinclude:: controllers/013.php

现在加载以下 URL 来查看评论方法::

    example.com/index.php/helloworld/comment/

你应该看到你的新消息。

将 URI 段传递给你的方法（传统版）
=============================================

如果你的 URI 包含超过两个段，它们将作为参数传递给你的方法。

例如，假设你有一个像这样的 URI::

    example.com/index.php/products/shoes/sandals/123

你的方法将接收 URI 段 3 和 4（``'sandals'`` 和 ``'123'``）：

.. literalinclude:: controllers/014.php

默认控制器（传统版）
===========================

默认控制器是一个特殊的控制器，当 URI 以目录名结尾或当 URI 不存在时使用，这种情况会在只请求你的网站根 URL 时发生。

定义默认控制器（传统版）
--------------------------------------

让我们用 ``Helloworld`` 控制器试试。

要指定默认控制器，请打开你的 **app/Config/Routing.php** 文件并设置此属性::

    public string $defaultController = 'Helloworld';

其中 ``Helloworld`` 是你想要使用的控制器类的名称。

并注释掉 **app/Config/Routes.php** 中的行：

.. literalinclude:: controllers/016.php
    :lines: 2-

如果你现在浏览你的网站而不指定任何 URI 段，你将看到"Hello World"消息。

.. note:: ``$routes->get('/', 'Home::index');`` 是一个你在"真实世界"应用中会想要使用的优化。但出于演示目的，我们不想使用该功能。``$routes->get()`` 在 :doc:`URI 路由 <routing>` 中有解释。

有关更多信息，请参考 :ref:`routing-auto-routing-legacy-configuration-options` 文档。

将你的控制器组织到子目录（传统版）
=========================================================

如果你正在构建一个大型应用程序，你可能想要分层组织或构建你的控制器到子目录中。CodeIgniter 允许你这样做。

只需在主 **app/Controllers** 下创建子目录，并将你的控制器类放在其中。

.. important:: 目录名必须以大写字母开头，并且只有第一个字符可以大写。

当使用此功能时，你的 URI 的第一段必须指定目录。例如，假设你有一个位于此处的控制器::

    app/Controllers/Products/Shoes.php

要调用上述控制器，你的 URI 将如下所示::

    example.com/index.php/products/shoes/show/123

.. note:: 你不能在 **app/Controllers** 和 **public/** 中有同名的目录。这是因为如果有目录，Web 服务器将搜索它，不会路由到 CodeIgniter。

你的每个子目录都可以包含一个默认控制器，如果 URL *仅* 包含子目录，则将调用该控制器。只需在那里放置一个与在 **app/Config/Routing.php** 文件中指定的默认控制器名称匹配的控制器。

CodeIgniter 还允许你使用其 :ref:`定义路由 <defined-route-routing>` 映射你的 URI。

重新映射方法调用
**********************

.. note:: **自动路由（改进版）** 不支持此功能，这是有意为之。

如上所述，URI 的第二段通常确定调用控制器中的哪个方法。CodeIgniter 允许你通过使用 ``_remap()`` 方法来重写此行为：

.. literalinclude:: controllers/017.php

.. important:: 如果你的控制器包含名为 ``_remap()`` 的方法，它将 **总是** 被调用，无论你的 URI 包含什么。它重写了 URI 确定调用哪个方法的正常行为，允许你定义自己的方法路由规则。

被重写的方法调用（通常是 URI 的第二段）将作为参数传递给 ``_remap()`` 方法：

.. literalinclude:: controllers/018.php

方法名之后的任何额外段都会传递到 ``_remap()`` 中。这些参数可以传递给方法以模拟 CodeIgniter 的默认行为。

示例：

.. literalinclude:: controllers/019.php

扩展控制器
************************

如果你想扩展控制器，请参见 :doc:`../extending/basecontroller`。

就是这样！
**********

简而言之，这就是关于控制器你需要知道的全部内容。
