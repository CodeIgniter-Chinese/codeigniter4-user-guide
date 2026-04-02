#############################
从 4.1.2 升级到 4.1.3
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

破坏性增强
*********************

缓存 TTL
=========

**app/Config/Cache.php** 中新增了一个配置项：``$ttl``。
该值当前未被框架内置的缓存处理器使用（其 TTL 仍然硬编码为 60 秒），
但对项目和模块可能会有用。
在未来的版本中，此配置将取代当前的硬编码值，
因此请将其保持为 ``60``，或避免依赖硬编码的 TTL 值。

项目文件
*************

项目空间中只有少量文件（根目录、app、public、writable）发生了更新。
由于这些文件不属于 system 范畴，
框架不会在未征得你同意的情况下自动修改它们。
以下文件已发生变更，建议将更新后的版本合并到你的应用中：

* ``app/Config/Cache.php``
* ``spark``
