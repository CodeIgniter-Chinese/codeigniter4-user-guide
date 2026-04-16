#############################
从 4.0.4 升级到 4.0.5
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

Cookie SameSite 支持
=======================

CodeIgniter 4.0.5 引入了用于设置 Cookie SameSite 属性的配置项。此前的版本完全没有设置该属性。
现在 Cookie 的默认设置为 `Lax`。这将影响 Cookie 在跨域场景中的处理方式，你可能需要在项目中调整该设置。
在 **app/Config/App.php** 中，分别为 Response Cookie 和 CSRF Cookie 提供了独立的配置项。

更多信息请参阅 `MDN Web 文档 <https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Headers/Set-Cookie#samesitesamesite-value>`_。
SameSite 的规范定义见 `RFC 6265 <https://datatracker.ietf.org/doc/html/rfc6265>`_
以及 `RFC 6265bis 修订版 <https://datatracker.ietf.org/doc/draft-ietf-httpbis-rfc6265bis/?include_text=1>`_。

Message::getHeader(s)
=====================

HTTP 层正逐步向 `PSR-7 规范 <https://www.php-fig.org/psr/psr-7/>`_ 靠拢。为此，
``Message::getHeader()`` 和 ``Message::getHeaders()`` 已被弃用，应分别改用
``Message::header()`` 和 ``Message::headers()``。需要注意的是，这同样适用于
所有继承 ``Message`` 的类：``Request``、``Response`` 及其子类。

HTTP 层中其他相关的弃用项包括：

* ``Message::isJSON()``：请直接检查 "Content-Type" HTTP 标头
* ``Request[Interface]::isValidIP()``：请使用 Validation 类并结合 ``valid_ip``
* ``Request[Interface]::getMethod()``：``$upper`` 参数将被移除，请使用 strtoupper()
* ``Request[Trait]::$ipAddress``：该属性将变为 private
* ``Request::$proxyIPs``：该属性将被移除；请直接访问 ``config('App')->proxyIPs``
* ``Request::__construct()``：构造函数将不再接收 ``Config\App``，并已设为可空以便过渡
* ``Response[Interface]::getReason()``：请改用 ``getReasonPhrase()``
* ``Response[Interface]::getStatusCode()``：将移除显式的 ``int`` 返回类型（无需采取任何操作）

ResponseInterface
=================

该接口旨在包含任何与框架兼容的响应类所需的方法。此前，框架期望的一些方法在接口中缺失，
现已全部补充。如果你直接使用了实现 ``ResponseInterface`` 的类，
它们需要符合更新后的接口要求。新增的方法如下：

* ``setLastModified($date)``
* ``setLink(PagerInterface $pager)``
* ``setJSON($body, bool $unencoded = false)``
* ``getJSON()``
* ``setXML($body)``
* ``getXML()``
* ``send()``
* ``sendHeaders()``
* ``sendBody()``
* ``setCookie($name, $value = '', $expire = '', $domain = '', $path = '/', $prefix = '', $secure = false, $httponly = false, $samesite = null)``
* ``hasCookie(string $name, string $value = null, string $prefix = ''): bool``
* ``getCookie(string $name = null, string $prefix = '')``
* ``deleteCookie(string $name = '', string $domain = '', string $path = '/', string $prefix = '')``
* ``getCookies()``
* ``redirect(string $uri, string $method = 'auto', int $code = null)``
* ``download(string $filename = '', $data = '', bool $setMime = false)``

为便于使用该接口，这些方法已从框架的 ``Response`` 类中移入 ``ResponseTrait``，
你可以直接使用该 Trait。同时，``DownloadResponse`` 现在直接继承 ``Response``，
以确保最大的兼容性。

Config\\Services
================

服务发现机制已更新，在启用 Modules 时，允许第三方服务优先于核心服务。
请更新 **app/Config/Services.php**，使该类继承 ``CodeIgniter\Config\BaseService``，
以确保第三方服务能够被正确发现。

项目文件
*************

项目空间中的大量文件（根目录、app、public、writable）已获得更新。由于这些文件不属于 system 范畴，
框架不会在未征得你同意的情况下自动修改它们。有一些第三方 CodeIgniter 模块可用于协助合并
项目空间中的变更：`在 Packagist 上浏览 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

.. note:: 除极少数用于修复 bug 的情况外，对项目空间文件所做的更改不会破坏你的应用。
    此处列出的所有更改在下一个主版本发布之前都是可选的，任何强制性的更改都会在上文相关章节中说明。

内容变更
===============

以下文件发生了较大的变更（包括弃用项或界面调整），建议将更新后的版本合并到你的应用中：

* ``app/Views/*``
* ``public/index.php``
* ``public/.htaccess``
* ``spark``
* ``phpunit.xml.dist``
* ``composer.json``

所有变更
===========

以下是项目空间中所有发生变更的文件列表；
其中许多只是简单的注释或格式调整，对运行时没有影响：

* ``LICENSE``
* ``README.md``
* ``app/Config/App.php``
* ``app/Config/Autoload.php``
* ``app/Config/Boot/development.php``
* ``app/Config/Boot/production.php``
* ``app/Config/Boot/testing.php``
* ``app/Config/Cache.php``
* ``app/Config/Constants.php``
* ``app/Config/ContentSecurityPolicy.php``
* ``app/Config/Database.php``
* ``app/Config/DocTypes.php``
* ``app/Config/Email.php``
* ``app/Config/Encryption.php``
* ``app/Config/Events.php``
* ``app/Config/Exceptions.php``
* ``app/Config/Filters.php``
* ``app/Config/ForeignCharacters.php``
* ``app/Config/Format.php``
* ``app/Config/Generators.php``
* ``app/Config/Honeypot.php``
* ``app/Config/Images.php``
* ``app/Config/Kint.php``
* ``app/Config/Logger.php``
* ``app/Config/Migrations.php``
* ``app/Config/Mimes.php``
* ``app/Config/Modules.php``
* ``app/Config/Pager.php``
* ``app/Config/Paths.php``
* ``app/Config/Routes.php``
* ``app/Config/Security.php``
* ``app/Config/Services.php``
* ``app/Config/Toolbar.php``
* ``app/Config/UserAgents.php``
* ``app/Config/Validation.php``
* ``app/Config/View.php``
* ``app/Controllers/BaseController.php``
* ``app/Controllers/Home.php``
* ``app/Views/errors/cli/error_404.php``
* ``app/Views/errors/cli/error_exception.php``
* ``app/Views/errors/html/debug.css``
* ``app/Views/errors/html/debug.js``
* ``app/Views/errors/html/error_exception.php``
* ``composer.json``
* ``env``
* ``license.txt``
* ``phpunit.xml.dist``
* ``public/.htaccess``
* ``public/index.php``
* ``spark``
