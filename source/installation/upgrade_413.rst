#############################
从 4.1.2 升级到 4.1.3
#############################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

重大增强
*********************

缓存 TTL
=========

在 **app/Config/Cache.php** 中有一个新的值:``$ttl``。这不会被框架中的处理程序使用,其中硬编码为60秒,但对项目和模块可能很有用。在未来的版本中,此值将替换硬编码的版本,因此请将其保留为 ``60``,或者停止依赖硬编码的版本。

项目文件
*************

项目空间(root、app、public、writable)中的只有少数文件收到了更新。由于这些文件超出系统范围,如果不进行干预,它们将不会更改。以下文件已被更改,建议你将更新后的版本与应用程序合并:

* ``app/Config/Cache.php``
* ``spark``
