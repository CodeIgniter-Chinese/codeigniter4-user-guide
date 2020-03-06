[![image](https://travis-ci.org/CodeIgniter-Chinese/codeigniter4-user-guide.svg?branch=master)](https://travis-ci.org/CodeIgniter-Chinese/codeigniter4-user-guide)
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

# CodeIgniter 4 中文手册翻译项目

## 翻译准则

中文翻译请遵守
[中文文案排版指北](http://mazhuang.org/wiki/chinese-copywriting-guidelines/)
和 [文档翻译指南](translation-guide.md)

[文档翻译进度](TODO.md)

[预览最新文档](https://codeigniter-chinese.github.io/codeigniter4-user-guide/)

## 安装步骤

CodeIgniter 的用户指南是使用 Sphinx 软件进行管理，并可以生成各种不同的格式。 所有的页面都是采用 [ReStructured
Text](http://sphinx.pocoo.org/rest.html) 格式书写，这种格式非常方便人们阅读。

### 安装条件

Sphinx 软件依赖于 Python，如果你使用的是 OS X 系统，则系统已经自带 Python 了。 你可以在终端中执行不带参数的
`python` 命令，以确认你的系统是否已安装 Python 。 如果你已安装，会显示出你当前所使用的版本。 如果显示的不是 3.7
以上版本，你可以去这里下载并安装 3.7.6
<https://www.python.org/downloads/release/python-376/>

### 安装

1.  安装
    [easy\_install](http://peak.telecommunity.com/DevCenter/EasyInstall#installing-easy-install)
2.  `easy_install "sphinx==1.8.5"`
3.  `easy_install sphinxcontrib-phpdomain`
4.  `easy_install "jieba==0.42.1"`
5.  安装 CI Lexer，它可以高亮文档中的 PHP, HTML, CSS, 和 JavaScript 代码 (参见
    *cilexer/README*)
6.  返回代码库根目录
7.  `make html`

译注：

1.  Ubuntu 系统上安装 easy\_install 可以直接：`sudo apt-get install
    python-setuptools`
2.  easy\_install 需要 root 权限，前面加上 sudo

### 编辑并创建文档

所有的源文件都在 *source/* 目录下，在这里你可以添加新的文档或修改已有的文档。

### 那么，HTML 文档在哪里？

很显然，HTML 文档才是我们最关心的，因为这毕竟才是用户最终看到的。 由于对自动生成的文件进行版本控制没有意义，所以它们并不在版本控制之下。
你如果想要预览 HTML 文档，你可以重新生成它们。生成 HTML 文档非常简单，
首先进入你的用户指南目录，然后执行上面安装步骤中的最后一步:

    make html

你将会看到正在编译中的信息，编译成功后，生成的用户指南和图片都位于 *build/html/* 目录下。 在 HTML
第一次编译之后，后面将只会针对修改的文件进行重编译，这将大大的节约我们的时间。
如果你想再重新全部编译一次，只需删除 *build* 目录然后编译即可。

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="http://alexfu.cc"><img src="https://avatars3.githubusercontent.com/u/9924787?v=4" width="100px;" alt=""/><br /><sub><b>Alexander.Fu</b></sub></a><br /><a href="https://github.com/CodeIgniter-Chinese/codeigniter4-user-guide/commits?author=FlyingWings" title="Documentation">📖</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!