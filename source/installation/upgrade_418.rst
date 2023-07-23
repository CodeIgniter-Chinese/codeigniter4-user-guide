#############################
从 4.1.7 升级到 4.1.8
#############################

请参考与你的安装方法相对应的升级说明。

- :ref:`通过 Composer 安装应用启动器升级 <app-starter-upgrading>`
- :ref:`通过 Composer 安装到现有项目升级 <adding-codeigniter4-upgrading>`
- :ref:`手动安装升级 <installing-manual-upgrading>`

.. contents::
    :local:
    :depth: 2

重大变更
****************

- 由于 ``API\ResponseTrait`` 中的一个安全问题,所有 trait 方法的作用域现在都被限定为 ``protected``。更多信息请参阅 `安全公告 GHSA-7528-7jg5-6g62 <https://github.com/codeigniter4/CodeIgniter4/security/advisories/GHSA-7528-7jg5-6g62>`_。
