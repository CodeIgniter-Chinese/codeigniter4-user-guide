====================
贡献署名
====================

我们要求的贡献有编码提交已署名。**证明贡献署名很重要，如同在贡献起源的地方我们能做的最有效的事情。**

如果编码提交不被署名，开发者推送一个编码提交就像一个 PR 的部分不必要的人最初做了编码提交。这将扭曲编码提交历史并且让源代码很难讲述源自哪。

如果有人 “署名” 了编码提交，他们可以自由使用任何名字，明确地一个而不是他们自身拥有的。再者，如果一个开发者正哄骗另一个开发者，编码提交历史不能依赖编码起源的裁定。恶毒的人能提交恶意代码（例如病毒）并且导致恶意代码看起来像另外一个开发者创造的。

最好的解决方案虽然不是防呆法，是去 “安全地署名” 你的编码提交。这样的编码提交是与你 github 账户的 GPG 密钥相匹配的数字署名。那仍旧不是防呆法，因为一个恶毒的开发者能创建伪造电子邮件和账户，但这个方法比不署名或者一个 “署名” 过的编码提交更可靠。

如果你没有署名你的编码提交，我们**也许** 会接受你的贡献，假定贡献符合有效性和贡献原则，但只要不是危险的代码而且只能在仔细的检查后。如果代码完成了一次重要的任务，我们将坚持编码提交要被署名，并且如果是临界危险的代码（无论如何是我们解释的那样），我们将坚持你的贡献要被安全地署名。

阅读下面的文字会找出如何去为你的编码提交署名。:)


简化署名
=============
 
你必须署名你的工作，证明你也参与了记录工作或相反的有权利把工作传递给开源项目。

建立你的编码提交说明用户名字和电子邮件地址。查看  `Setting your email in Git <https://help.github.com/articles/setting-your-email-in-git/>`_   去全局地创建署名还是为了单独的存储库。

.. code-block:: bash

	git config --global user.email "john.public@example.com"
	git config --global user.name "John Q Public"
 
一旦有适当的位置，你只是不得不在你的编码提交上对你的 CodeIgniter fork 使用 --signoff 。

.. code-block:: bash

	git commit --signoff

或者简写

.. code-block:: bash

	git commit -s

下面将介绍在你的git配置中署名你的带有消息建立的编码提交，例如

	Signed-off-by: John Q Public <john.public@example.com>

你的 IDE 也许在编码提交窗口有 "Sign-Off" 复选框，或者甚至一个选项去自动地 sign-off 所有你创建的编码提交。你甚至能化名 git 编码提交使用 -s 特征位标记所以你不必回顾 Sign-Off。

在上面的风格中署名你的工作，你证实了一个 “开发者的源证书” 。上面证书的最新版在文件夹的根目录 :doc:`/DCO` 文件里。


安全署名
==============

上文描述过的 “简化署名” 不能被检验，可是那仍是重要的出发点。检验你的编码提交，你将需要建立 GPG 密钥，而且要作为附件添加到你的 github 账户内。

See the `git tools <https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work>`_
page for directions on doing this. The complete story is part of
`Github help <https://help.github.com/categories/gpg/>`_.

做这件事时的指导要查看 `git tools <https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work>`_ 页面。完整的说法是 `Github help <https://help.github.com/categories/gpg/>`_ 部分。

简化步骤是：

-   `生成你的 GPG 密钥 <https://help.github.com/articles/generating-a-new-gpg-key/>`_，并且复制它的ASCII表述。
-   `添加你的密钥到你 Github 账户 <https://help.github.com/articles/adding-a-new-gpg-key-to-your-github-account/>`_ 。
-  `向Git告知 <https://help.github.com/articles/telling-git-about-your-gpg-key/>`_ 关于你的GPG密钥 。
-  自动地对所有你的编码提交的安全署名 `设置默认署名 <https://help.github.com/articles/signing-commits-using-gpg/>`_ 。
-  提供你的GPG密钥密码，像当你完成了编码提交时提示过一样。

依赖你的 IDE ，你也许必须从你的 Git bash shell 去使用 **-S** 选项阻止安全的署名完成你的 Git 编码提交。


编码提交说明
===============

无论如何你怎样署名编码提交，编码提交说明也是重要的。它们简明地传达了特性改变的意图。它们更容易的成功回顾编码，并且如果编码史被延迟检查它们会找出为什么发生了改变。

你的编码提交说明的读者群将是编码库的维护者、一些编码评论者，而且当程序错误已经被引入时程序调试器会尝试解决。

尽量设法使你的编码提交说明富有意义。
.
