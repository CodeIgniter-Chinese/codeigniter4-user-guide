**************
PSR 兼容性
**************

`PHP-FIG <http://www.php-fig.org/>`_ 创建于 2009 年，旨在帮助各个框架之间更自由的协作标准，遵循统一的编码和风格规范。 CodeIgniter 虽然并非 FIG 的成员之一，但我们的宗旨是一致的。这份文档主要是用来列出现有我们所遵循已被提案通过和一些草案的情况。

**PSR-1: 基础编码规范**

此建议涵盖了基本的类、方法和文件名命名规范。我们的 `代码规范 <https://github.com/codeigniter4/CodeIgniter4/blob/develop/contributing/styleguide.md>`_ 符合 PSR-1 且在此基础上添加了自己的要求。

**PSR-12:扩展代码风格**

我们的 `代码规范 <https://github.com/codeigniter4/CodeIgniter4/blob/develop/contributing/styleguide.md>`_ 遵循该建议,并添加了一组我们自己的代码风格约定。

**PSR-3: 日志接口规范**

CodeIgniter 的 :doc:`日志 <general/logging>` 实现了此 PSR 定义的所有接口。

**PSR-4: 自动加载规范**

此 PSR 提供了一种组织文件和命名空间的方法,以允许标准化的自动加载类的方式。我们的 :doc:`自动加载 <concepts/autoloader>` 符合 PSR-4 建议。

**PSR-6:缓存接口**
**PSR-16: 简单缓存接口**

虽然框架的缓存组件不遵循 PSR-6 或 PSR-16,但 CodeIgniter4 组织提供了一组独立的适配器作为补充模块。建议项目直接使用原生的缓存驱动,因为适配器仅用于与第三方库的兼容性。详情参见 `CodeIgniter4 缓存仓库 <https://github.com/codeigniter4/cache>`_。

**PSR-7: HTTP 消息接口规范**

此 PSR 标准化了表示 HTTP 交互的方式。尽管其许多概念成为了我们的 HTTP 层的一部分,但 CodeIgniter 不追求与此建议兼容。

---

如果您发现我们声称遵循某个 PSR 但实际执行不正确的地方,请告知我们,我们将修复它,或者您可以通过提交 PR 来提供所需的更改。
