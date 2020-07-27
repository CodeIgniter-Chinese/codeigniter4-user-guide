=====================
蜜罐类
=====================

当一个机器人程序向 CodeIgniter4 应用做请求时蜜罐类可能成功终止它。
如果蜜罐类在 ``Application\Config\Filters.php`` 文件里授权。
作为附件的表格字段的任意表格已经完成，并且这个表格字段是人性化隐藏的，但会受机器人程序影响。
当数据进入到字段时，假设的请求来自于一个机器人程序，并且你能抛出一个 ``HoneypotException``.


.. contents::
    :local:
    :depth: 2

授权中的蜜罐
=====================

去授权一个蜜罐，必须使用 ``app/Config/Filters.php`` 来改变。
恰好从 ``$globals`` 数组取消批注的蜜罐，如同……::


    public $globals = [
            'before' => [
                'honeypot'
                // 'csrf',
            ],
            'after'  => [
                'toolbar',
                'honeypot'
            ]
        ];

一个蜜罐样本过滤器是捆绑的，例如 ``system/Filters/Honeypot.php``.
如果蜜罐样本过滤器不是合适的，确保你自身在  ``app/Filters/Honeypot.php`` 里，
并且在适当的配置里修改 ``$aliases`` 。


自定义蜜罐
=====================

蜜罐能被定制。接下来的字段能被或许被设置在 ``app/Config/Honeypot.php`` 里或者在 ``.env`` 里。


* ``hidden`` - true|false 去控制蜜罐字段的可见性，默认是 ``true``
* ``label`` - 为蜜罐字段准备的 HTML 标签，默认是 'Fill This Field'/填充字段
* ``name`` - HTML 表格字段的名字常习惯于为了模板使用；默认是 'honeypot'
* ``template`` - 表格字段模板习惯于为了蜜罐使用；默认是 '<label>{label}</label><input type="text" name="{name}" value=""/>'
