**************
PSR 规范
**************

`PHP-FIG <http://www.php-fig.org/>`_ 创建于 2009 年，旨在帮助各个框架之间更自由的协作标准，遵循统一的编码和风格规范。 CodeIgniter 虽然并非 FIG 的成员之一，但我们的宗旨是一致的。这份文档主要是用来列出现有我们所遵循已被提案通过和一些草案的情况。

**PSR-1: 基础编码规范**

这份规范覆盖了基本类，方法和文件的命名标准。我们的 :doc:`开发规范 </contributing/styleguide>` 符合 PSR-1，并且在它的基础上添加了自己的标准。

**PSR-2: 编码风格规范**

这份 PSR 的争议性是比较大的，在它第一次出现的时候。CodeIgniter 在其中遇到了许多建议，但不会完全符合这些规范。

**PSR-3: 日志接口规范**

CodeIgniter 的 :doc:`Logger </general/logging>` 实现了该 PSR 提供的所有接口。

**PSR-4: 自动加载规范**

这份 PSR 提供了组织文件和命名空间以允许自动加载类的标准方法的方法。我们的 :doc:`自动加载类 </concepts/autoloader>` 符合 PSR-4 规范。

**PSR-6: 缓存接口规范**

CodeIgniter 不会尝试符合这份 PSR ，因为我们相信它超越了它的需求。我们会考虑新提出的 `SimpleCache 接口  <https://github.com/dragoonis/fig-standards/blob/psr-simplecache/proposed/simplecache.md>`_ 。

**PSR-7: HTTP 消息接口规范**

这份 PSR 标准化了表示 HTTP 交互的方式。虽然许多概念成为我们的 HTTP 层的一部分，但 CodeIgniter 并不力求与此规范兼容。

---

如果你发现任何我们声称实现 PSR 但未能正确执行的地方，请通知我们，我们会将其修正，或提交需要更改的拉动请求。
