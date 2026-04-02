#############################
从 4.1.7 升级到 4.1.8
#############################

请根据你的安装方式参考对应的升级说明。

- :ref:`Composer 安装：App Starter 方式的升级说明 <app-starter-upgrading>`
- :ref:`Composer 安装：将 CodeIgniter4 添加到现有项目的升级说明 <adding-codeigniter4-upgrading>`
- :ref:`手动安装：升级说明 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

破坏性变更
****************

- 由于 ``API\ResponseTrait`` 中的一个安全问题，该 trait 中的所有方法现在都被限定为 ``protected`` 作用域。
  更多信息请参见 `安全公告 GHSA-7528-7jg5-6g62 <https://github.com/codeigniter4/CodeIgniter4/security/advisories/GHSA-7528-7jg5-6g62>`_。
