#############################
从 4.0.4 升级到 4.0.5
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

Cookie SameSite 支持
=======================

CodeIgniter 4.0.5 引入了 cookie 的 SameSite 属性设置。先前版本没有设置此属性。
cookie的默认设置现在是`Lax`。这将影响 cookie 在跨域环境中的处理,你可能需要在项目中调整此设置。
在 **app/Config/App.php** 中为响应 cookie 和 CSRF cookie 分别存在独立设置。

有关详细信息,请参阅 `MDN Web 文档 <https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Set-Cookie/SameSite>`_。
SameSite 规范描述在 `RFC 6265 <https://tools.ietf.org/html/rfc6265>`_ 和
`RFC 6265bis 修订版 <https://datatracker.ietf.org/doc/draft-ietf-httpbis-rfc6265bis/?include_text=1>`_ 中。

Message::getHeader(s)
=====================

HTTP 层正在向 `PSR-7 兼容 <https://www.php-fig.org/psr/psr-7/>`_ 迈进。
为此, ``Message::getHeader()`` 和 ``Message::getHeaders()`` 已被废弃,
应分别替换为 ``Message::header()`` 和 ``Message::headers()``。
请注意,这也涉及到所有扩展 ``Message`` 的类:``Request``、``Response`` 及其子类。

来自 HTTP 层的其他相关废弃:

* ``Message::isJSON()``:直接检查 "Content-Type" 头
* ``Request[Interface]::isValidIP()``:使用 Validation 类及 ``valid_ip``
* ``Request[Interface]::getMethod()``:将删除 ``$upper`` 参数,使用 strtoupper()
* ``Request[Trait]::$ipAddress``:该属性将变为私有
* ``Request::$proxyIPs``:该属性将被删除;直接访问 ``config('App')->proxyIPs``
* ``Request::__construct()``:构造函数不再接收 ``Config\App`` ,已变为可空以方便过渡
* ``Response[Interface]::getReason()``:请使用 ``getReasonPhrase()``
* ``Response[Interface]::getStatusCode()``:将删除显式的 ``int`` 返回类型(无需操作)

ResponseInterface
=================

该接口旨在包括任何框架兼容的响应类所需的方法。缺少许多框架所需的方法,现已添加。
如果你使用任何直接实现 ``ResponseInterface`` 的类,它们需要与更新后的要求兼容。
这些方法如下:

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

为方便使用此接口,这些方法已从框架的 ``Response`` 移至 ``ResponseTrait`` 中,你可以使用它,
``DownloadResponse`` 现在直接扩展 ``Response`` 以确保最大兼容性。

Config\\Services
================

服务发现已更新,允许第三方服务(在通过 Modules 启用时)优先于核心服务。
请更新 **app/Config/Services.php**,使类扩展 ``CodeIgniter\Config\BaseService``
以允许正确发现第三方服务。

项目文件
*************

项目空间(根目录、app、public、writable)中的许多文件都已更新。
由于这些文件超出系统范围,如果不进行干预,它们将不会更改。
有一些第三方 CodeIgniter 模块可用于帮助合并项目空间中的更改:
`在 Packagist 上探索 <https://packagist.org/explore/?query=codeigniter4%20updates>`_。

.. note:: 除了极少数的错误修复情况外,对项目空间文件的任何更改都不会破坏你的应用程序。
    直到下一个主版本之前,这里注明的所有更改都是可选的,任何强制性更改都将在上面的部分中介绍。

内容更改
===============

建议你将更新版本与应用程序合并,因为以下文件收到显着更改(包括不推荐使用或视觉调整):

* ``app/Views/*``
* ``public/index.php``
* ``public/.htaccess``
* ``spark``
* ``phpunit.xml.dist``
* ``composer.json``

所有更改
===========

这是项目空间中已更改的所有文件的列表;其中许多只是注释或格式更改,不会对运行时产生影响:

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
