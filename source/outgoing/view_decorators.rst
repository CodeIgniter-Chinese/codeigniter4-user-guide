###############
视图装饰器
###############

视图装饰器允许您的应用程序在渲染过程中修改 HTML 输出。这发生在缓存之前,允许您将自定义功能应用于视图。

*******************
创建装饰器
*******************

创建自己的视图装饰器需要创建一个新的类,该类实现 ``CodeIgniter\View\ViewDecoratorInterface``。
这需要一个单一的方法,它获取生成的 HTML 字符串,对其执行任何修改,并返回结果 HTML。

.. literalinclude:: view_decorators/001.php

创建后,必须在 ``app/Config/View.php`` 中注册该类:

.. literalinclude:: view_decorators/002.php

现在它已注册,每渲染或解析的视图都将调用装饰器。
装饰器的调用顺序与此配置设置中指定的顺序相同。
