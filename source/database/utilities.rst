#########
实用工具
#########

数据库实用工具类包含帮助您管理数据库的方法。

.. contents::
    :local:
    :depth: 2

*******************
从结果中获取 XML
*******************

getXMLFromResult()
==================

此方法从数据库结果返回 xml 结果。您可以这样做:

.. literalinclude:: utilities/001.php

它将获取以下 xml 结果::

    <root>
        <element>
            <id>1</id>
            <name>bar</name>
        </element>
    </root>
