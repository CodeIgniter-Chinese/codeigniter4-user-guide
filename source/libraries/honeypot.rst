##############
蜜罐类
##############

如果在 **app/Config/Filters.php** 文件中启用蜜罐,蜜罐类可以确定何时机器人向 CodeIgniter4 应用程序发出请求。这是通过将表单字段附加到任何表单上完成的,这个表单字段对人类隐藏但对机器人可访问。当数据输入字段时,假定请求来自机器人,你可以抛出一个 ``HoneypotException``。

.. contents::
    :local:
    :depth: 2

*****************
启用蜜罐
*****************

要启用蜜罐,需要对 **app/Config/Filters.php** 进行更改。只需从 ``$globals`` 数组中取消注释 honeypot,如:

.. literalinclude:: honeypot/001.php

附带了一个示例蜜罐过滤器，位于 **system/Filters/Honeypot.php**。
如果它不合适，你可以在 **app/Filters/Honeypot.php** 创建自己的过滤器，
并相应地修改 **app/Config/Filters.php** 中的 ``$aliases``。

********************
自定义蜜罐
********************

可以自定义蜜罐。以下字段可以在
**app/Config/Honeypot.php** 或 **.env** 中设置。

* ``$hidden`` - ``true`` 或 ``false`` 来控制蜜罐字段的可见性; 默认为 ``true``
* ``$label`` - 蜜罐字段的 HTML 标签,默认为 ``'Fill This Field'``
* ``$name`` - 用于模板的 HTML 表单字段的名称; 默认为 ``'honeypot'``
* ``$template`` - 用于蜜罐的表单字段模板; 默认为 ``'<label>{label}</label><input type="text" name="{name}" value="">'``
* ``$container`` - 模板的容器标签; 默认为 ``'<div style="display:none">{template}</div>'``。
  如果你启用了 CSP,可以删除 ``style="display:none"``。
* ``$containerId`` - [v4.3.0 新增] 此设置仅在启用 CSP 时使用。你可以更改容器标签的 id 属性; 默认为 ``'hpc'``
