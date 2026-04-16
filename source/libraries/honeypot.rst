##############
Honeypot 类
##############

Honeypot 类用于检测 CodeIgniter4 应用程序中的 Bot 请求，前提是在 **app/Config/Filters.php** 文件中启用。实现方式是在表单中附加一个字段，该字段对人类隐藏但对 Bot 可见。当字段被填入数据时，即视为请求来自 Bot，此时可抛出 ``HoneypotException``。

.. contents::
    :local:
    :depth: 2

*****************
启用 Honeypot
*****************

启用 Honeypot 需修改 **app/Config/Filters.php**。取消 ``$globals`` 数组中 honeypot 的注释即可：

.. literalinclude:: honeypot/001.php

系统自带示例 Honeypot 过滤器 **system/Filters/Honeypot.php**。若不符合需求，可在 **app/Filters/Honeypot.php** 创建自定义过滤器，并相应修改 **app/Config/Filters.php** 中的 ``$aliases``。

********************
自定义 Honeypot
********************

Honeypot 支持自定义。以下字段可在 **app/Config/Honeypot.php** 或 **.env** 中设置：

* ``$hidden`` - ``true`` 或 ``false``，控制 honeypot 字段可见性；默认为 ``true``
* ``$label`` - honeypot 字段的 HTML 标签，默认为 ``'Fill This Field'``
* ``$name`` - 模板中 HTML 表单字段的名称；默认为 ``'honeypot'``
* ``$template`` - honeypot 使用的表单字段模板；默认为 ``'<label>{label}</label><input type="text" name="{name}" value="">'``
* ``$container`` - 模板容器标签；默认为 ``'<div style="display:none">{template}</div>'``。若启用 CSP，可移除 ``style="display:none"``。
* ``$containerId`` - [v4.3.0 新增] 仅在启用 CSP 时使用。可更改容器标签的 id 属性；默认为 ``'hpc'``
