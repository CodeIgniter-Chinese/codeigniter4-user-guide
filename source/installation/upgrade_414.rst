#############################
从 4.1.3 升级到 4.1.4
#############################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

此版本专注于代码风格。所有更改(除下面注明的外)都是为了使代码符合新的
`CodeIgniter 编码标准 <https://github.com/CodeIgniter/coding-standard>`_ (基于 PSR-12)。

重大变更
****************

方法作用域
============

以下方法的作用域从 ``public`` 改为 ``protected``,以匹配其父类方法并更好地与其用法保持一致。
如果你依赖任何这些方法是 public 的(极少可能),请相应调整你的代码:

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

项目空间中的所有文件都使用新的编码风格进行了重新格式化。这不会影响现有代码,但是你可能希望将更新的编码风格应用于自己的项目,以使它们与这些文件的框架版本保持一致。
