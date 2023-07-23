#############################
从 4.0.x 升级到 4.0.4
#############################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

CodeIgniter 4.0.4 修复了 :doc:`控制器过滤器 </incoming/filters>` 实现中的一个bug,破坏了
遵循 ``FilterInterface`` 的代码。

重大变更
******************

更新 FilterInterface 声明
===================================

``after()`` 和 ``before()`` 方法签名必须更新为包含 ``$arguments``。函数
定义应从::

    public function before(RequestInterface $request)
    public function after(RequestInterface $request, ResponseInterface $response)

更改为::

    public function before(RequestInterface $request, $arguments = null)
    public function after(RequestInterface $request, ResponseInterface $response, $arguments = null)
