**************
PSR 兼容性
**************

`PHP-FIG <https://www.php-fig.org/>`_ 成立于 2009 年，旨在通过制定接口、风格指南等规范，帮助不同框架之间的代码实现更好的互操作性。各成员可以自由选择是否实现这些规范。尽管 CodeIgniter 并不是 FIG 的成员，但我们与其中多项提案保持兼容。本指南用于列出我们对各个已被接受、以及部分仍处于草案阶段的提案的兼容状态。

**PSR-1：基础编码规范**

该规范涵盖了类、方法以及文件命名等基础标准。我们的
`代码规范 <https://github.com/codeigniter4/CodeIgniter4/blob/develop/contributing/styleguide.md>`_
符合 PSR-1，并在此基础上增加了额外的要求。

**PSR-12：扩展编码风格**

我们的
`代码规范 <https://github.com/codeigniter4/CodeIgniter4/blob/develop/contributing/styleguide.md>`_
遵循该规范，并加入了一套我们自己的代码风格约定。

**PSR-3：日志接口规范**

CodeIgniter 的 :doc:`日志 </general/logging>` 实现了该 PSR 提供的全部接口。

**PSR-4：自动加载规范**

该 PSR 提供了一种组织文件和命名空间的方法，以实现统一的类自动加载机制。我们的
:doc:`自动加载器 </concepts/autoloader>` 符合 PSR-4 的推荐规范。

**PSR-6：缓存接口**
**PSR-16：SimpleCache 接口**

虽然框架内置的 Cache 组件并未遵循 PSR-6 或 PSR-16，但 CodeIgniter4 组织提供了一组独立的适配器，作为补充模块。建议项目直接使用原生的 Cache 驱动，因为这些适配器仅用于与第三方库的兼容。如需更多信息，请访问
`CodeIgniter4 Cache 仓库 <https://github.com/codeigniter4/cache>`_。

**PSR-7：HTTP 消息接口规范**

该 PSR 规范了表示 HTTP 交互的一种方式。虽然其中的许多概念已成为我们 HTTP 层的一部分，但 CodeIgniter 并不追求与该规范的兼容性。

---

如果你发现我们声称符合某个 PSR，但在实现上存在问题，请告知我们，我们会进行修复；或者也可以提交包含所需修改的 Pull Request。
