
###########################
贡献给 CodeIgniter
###########################

.. toctree::
    :titlesonly:

    guidelines
    workflow
    signing
    roadmap
    internals
    documentation
    PHP Style Guide <styleguide>
    ../DCO


codeigniter是一个大众驱动项目并且它接受自大众提供的编码和文档编制贡献。这些贡献将在 Github 的 `CodeIgniter4 repository <https://github.com/bcit-ci/CodeIgniter4>`_  上以讨论的形式或者以 `Pull Requests <https://help.github.com/articles/using-pull-requests/>`_ 形式产生。


讨论是指出一个程序错误最快捷的方式。如果你在 Codeigniter 中找到了程序错误或者文档编制错误，请首先检查一些要事：

- 是否存在一个已经开放的讨论。
- 讨论已经被解决了。（检查开发分支，或者查看关闭的讨论。）
- 你明确的确实要独自解决问题吗？

发布讨论是有帮助而且发出 Pull Request 是一个更好的方式，PR 是基于 “Forking” 主要的内容并提交到你自己拷贝版本里。

*******
支持
*******

请记住 GitHub 决不支持一般使用性的问题！如果将来你在使用 Codeigniter 中有了困难，请去网络论坛寻求帮助代替发表在 `forums <http://forum.codeigniter.com/>`_ 上。

如果你不能保证你使用中出现的事情是否正确或者你又发现了一处程序错误，请首先在网络论坛中询问。

********
安全性
********

你已经在 CodeIgniter 中找到一个安全问题了吗？

请不要公开揭露你发现的安全问题，但是你要发送邮件给 security@codeigniter.com，或者经由我们 `HackerOne <https://hackerone.com/codeigniter>`_ 的页面发布它。
如果你已经找到了一个濒临崩溃的安全危险，我们很高兴把你的发现放在我们的 `ChangeLog <../changelog.html>`_ 里。

****************************
优良的讨论报告贴士
****************************

使用有描述的主题原则（例如 parser library chokes on commas）好于含糊不清的主题（例如 your code broke ）。

在报告里计算机物理地址是单独说明的问题。

识别清楚 codeigniter 的版本（例如 3.0 - develop）和你知道的组件（例如 parser library）

阐述你预期将要发生的事或者已经发生的事。包括任何错误的信息和堆栈轨迹。

如果代码程序段能够帮助说明要把短代码程序段考虑在内。使用 pastebin 或者 dropbox 很容易提取更长的代码程序段或者截图 ———— 截图并不包含讨论报告自身。
本段文字的主旨是设定问题解决的合理终结，直到问题解决或者关闭。

如果你知道如何解决讨论，你要在你自己的 fork & branch 做好解决方案，并且提交堆栈请求（pull request）。 
上文中的问题报告信息应当是整个报告的一部分。

如果你的讨论报告描述能分步骤的再现问题，那是极好的。如果你在再现问题时能把单元测试考虑在内，那将更好，讨论报告要给任何正在解决问题的人一个更加清楚的目标！
