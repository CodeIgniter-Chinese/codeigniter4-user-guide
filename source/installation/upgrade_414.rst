#############################
从 4.1.3 升级到 4.1.4
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

本次版本发布主要聚焦于代码风格。除下文特别说明的变更外，其余改动均为外观层面的调整，
旨在使代码符合新的
`CodeIgniter 编码规范 <https://github.com/CodeIgniter/coding-standard>`_
（基于 PSR-12）。

破坏性变更
****************

方法可见性
============

以下方法的可见性已从 ``public`` 调整为 ``protected``，
以与其父类方法保持一致，并更好地契合其实际用途。
如果你的代码依赖这些方法为 public（这种情况极少见），
请相应调整实现：

* ``CodeIgniter\Database\MySQLi\Connection::execute()``
* ``CodeIgniter\Database\MySQLi\Connection::_fieldData()``
* ``CodeIgniter\Database\MySQLi\Connection::_indexData()``
* ``CodeIgniter\Database\MySQLi\Connection::_foreignKeyData()``
* ``CodeIgniter\Database\Postgre\Builder::_like_statement()``
* ``CodeIgniter\Database\Postgre\Connection::execute()``
* ``CodeIgniter\Database\Postgre\Connection::_fieldData()``
* ``CodeIgniter\Database\Postgre\Connection::_indexData()``
* ``CodeIgniter\Database\Postgre\Connection::_foreignKeyData()``
* ``CodeIgniter\Database\SQLSRV\Connection::execute()``
* ``CodeIgniter\Database\SQLSRV\Connection::_fieldData()``
* ``CodeIgniter\Database\SQLSRV\Connection::_indexData()``
* ``CodeIgniter\Database\SQLSRV\Connection::_foreignKeyData()``
* ``CodeIgniter\Database\SQLite3\Connection::execute()``
* ``CodeIgniter\Database\SQLite3\Connection::_fieldData()``
* ``CodeIgniter\Database\SQLite3\Connection::_indexData()``
* ``CodeIgniter\Database\SQLite3\Connection::_foreignKeyData()``
* ``CodeIgniter\Images\Handlers\GDHandler::_flatten()``
* ``CodeIgniter\Images\Handlers\GDHandler::_flip()``
* ``CodeIgniter\Images\Handlers\ImageMagickHandler::_flatten()``
* ``CodeIgniter\Images\Handlers\ImageMagickHandler::_flip()``
* ``CodeIgniter\Test\Mock\MockIncomingRequest::detectURI()``
* ``CodeIgniter\Test\Mock\MockSecurity.php::sendCookie()``

项目文件
*************

项目空间中的所有文件均已按照新的编码风格重新格式化。
这些更改不会影响现有代码的运行，
但建议你在自己的项目中也应用更新后的编码规范，
以便和框架里的这些文件风格保持一致。
