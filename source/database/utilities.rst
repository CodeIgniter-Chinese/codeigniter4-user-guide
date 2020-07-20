########################
实用工具
########################

数据库实用工具类包含一系列可以帮助你管理数据库的方法。

.. 目录::
    :local:
    :depth: 2

*******************
从结果中获取XML
*******************

**getXMLFromResult()**

该方法从数据库查询结果中返回xml结果，可以如下进行::

    $model = new class extends \CodeIgniter\Model {
        protected $table      = 'foo';
        protected $primaryKey = 'id';
    };
    $db = \Closure::bind(function ($model) {
        return $model->db;
    }, null, $model)($model);

    $util = (new \CodeIgniter\Database\Database())->loadUtils($db);
    echo $util->getXMLFromResult($model->get());

将会返回如下的XML结果::

    <root>
        <element>
            <id>1</id>
            <name>bar</name>
        </element>
    </root>
