#############################
从 4.0.x 升级到 4.0.4
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

CodeIgniter 4.0.4 修复了 :doc:`控制器过滤器 </incoming/filters>` 实现中的一个 bug，这会破坏基于 ``FilterInterface`` 的代码实现。

破坏性变更
****************

更新 FilterInterface 声明
===================================

``after()`` 和 ``before()`` 的方法签名必须更新，以包含 ``$arguments``。函数定义需要从以下形式::

    public function before(RequestInterface $request)
    public function after(RequestInterface $request, ResponseInterface $response)

改为::

    public function before(RequestInterface $request, $arguments = null)
    public function after(RequestInterface $request, ResponseInterface $response, $arguments = null)
