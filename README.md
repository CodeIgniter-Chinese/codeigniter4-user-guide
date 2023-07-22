# CodeIgniter 4 中文手册翻译项目

[![image](https://travis-ci.org/CodeIgniter-Chinese/codeigniter4-user-guide.svg?branch=master)](https://travis-ci.org/CodeIgniter-Chinese/codeigniter4-user-guide) <!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-29-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## 翻译准则

中文翻译请遵守
[中文文案排版指北](http://mazhuang.org/wiki/chinese-copywriting-guidelines/)
和 [文档翻译指南](translation-guide.md)

[预览最新文档](https://codeigniter-chinese.github.io/codeigniter4-user-guide/)

## 安装步骤

CodeIgniter 的用户指南使用 Sphinx 软件进行管理，并可以生成各种不同的格式。所有页面都采用 [ReStructured Text](https://en.wikipedia.org/wiki/ReStructuredText) 格式书写，这种格式非常方便人们阅读。

### 安装条件

#### Python

Sphinx 需要 Python 3.5+ 版本，如果你正在运行 macOS 或 Linux，则可能已经安装了它。
你可以在终端窗口中执行 `python` 或 `python3` 来确认。

```bash
python --version
Python 2.7.17

python3 --version
Python 3.6.9

# 对于使用 Python 启动器的 Windows
py -3 --version
Python 3.8.1
```

如果你的版本低于 3.5+，请从 [Python.org](https://www.python.org/downloads/) 安装最新的 3.x 版本。Linux 用户应该使用操作系统自带的包管理器来更新。

#### pip

现在你已经安装并运行了 Python 3.x，我们将安装 [pip](https://pip.pypa.io/en/stable/) (Python 包安装程序)。

你可以使用 `pip` 或 `pip3` 检查是否已安装 pip。如你所见，pip 遵循与 Python 相同的命名约定。请注意，输出的末尾应该显示 `python 3.x`。

```bash
pip --version
pip 9.0.1 from /usr/lib/python2.7/dist-packages (python 2.7)

pip3 --version
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.6)

# 对于使用 Python 启动器的 Windows
py -3 -m pip --version
pip 20.0.2 from C:\Users\<username>\AppData\Local\Programs\Python\Python38\lib\site-packages\pip (python 3.8)
```

##### Linux

[使用 Linux 包管理器安装 pip/setuptools/wheel](https://packaging.python.org/guides/installing-using-linux-tools/)

##### 其他

如果你使用从 [Python.org](https://www.python.org/downloads/) 下载的 Python 3.5+，则 pip 已经安装好了。

### 安装

现在我们需要安装 Sphinx 和它的依赖项。根据操作系统选择 `pip` 或 `pip3`。
此步骤之后，你需要重启终端窗口，否则 Python 将找不到我们刚刚安装的所有应用程序。

```bash
pip install -r requirements.txt

pip3 install -r requirements.txt

# 对于使用 Python 启动器的 Windows
py -3 -m pip install -r requirements.txt
```

是时候总结一下并生成文档了。

```bash
make html
```

### 使用 Docker

如果你喜欢使用 Docker 构建文档的话，可以这样：

1. clone 代码库到本地，例如 `/my/ci4` 目录
2. 在 `/my/ci4` 目录下执行 `docker build -t ci4 .`
3. 在 `/my/ci4` 目录下执行 `docker run -t --rm -v /my/ci4:/ci ci4`

执行完毕后，`/my/ci4/build/html` 目录就是生成的文档啦。

### 编辑并创建文档

所有的源文件都在 *source/* 目录下，在这里你可以添加新的文档或修改已有的文档。

### 那么，HTML 文档在哪里？

很显然，HTML 文档才是我们最关心的，因为这毕竟才是用户最终看到的。 由于对自动生成的文件进行版本控制没有意义，所以它们并不在版本控制之下。
你如果想要预览 HTML 文档，你可以重新生成它们。生成 HTML 文档非常简单，
首先进入你的用户指南目录，然后执行上面安装步骤中的最后一步:

    make html

你将会看到正在编译中的信息，编译成功后，生成的用户指南和图片都位于 *build/html/* 目录下。在 HTML
第一次编译之后，后面将只会针对修改的文件进行重编译，这将大大的节约我们的时间。
如果你想再重新全部编译一次，只需删除 *build* 目录然后编译即可。

## 贡献者 ✨

感谢这些可爱的童鞋为中文手册做出的卓越贡献。 ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="http://alexfu.cc"><img src="https://avatars3.githubusercontent.com/u/9924787?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Alexander.Fu</b></sub></a><br /><a href="#translation-FlyingWings" title="Translation">🌍</a></td>
    <td align="center"><a href="http://www.wazidw.com"><img src="https://avatars0.githubusercontent.com/u/4579995?v=4?s=100" width="100px;" alt=""/><br /><sub><b>wazidw</b></sub></a><br /><a href="#translation-wazidw" title="Translation">🌍</a> <a href="#projectManagement-wazidw" title="Project Management">📆</a> <a href="https://github.com/CodeIgniter-Chinese/codeigniter4-user-guide/pulls?q=is%3Apr+reviewed-by%3Awazidw" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/zhangxiaoshua"><img src="https://avatars3.githubusercontent.com/u/31472394?v=4?s=100" width="100px;" alt=""/><br /><sub><b>zhangxiaoshua</b></sub></a><br /><a href="#translation-zhangxiaoshua" title="Translation">🌍</a></td>
    <td align="center"><a href="https://www.qichengzx.com"><img src="https://avatars0.githubusercontent.com/u/1927478?v=4?s=100" width="100px;" alt=""/><br /><sub><b>xin zhao</b></sub></a><br /><a href="#translation-qichengzx" title="Translation">🌍</a></td>
    <td align="center"><a href="https://www.minipudding.com"><img src="https://avatars0.githubusercontent.com/u/11162253?v=4?s=100" width="100px;" alt=""/><br /><sub><b>icicle198514</b></sub></a><br /><a href="#translation-icicle198514" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/calciferlh"><img src="https://avatars0.githubusercontent.com/u/14966692?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Calcifer</b></sub></a><br /><a href="#translation-calciferlh" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/DuXuanXuan"><img src="https://avatars1.githubusercontent.com/u/17022815?v=4?s=100" width="100px;" alt=""/><br /><sub><b>DuXuanXuan</b></sub></a><br /><a href="#translation-DuXuanXuan" title="Translation">🌍</a></td>
  </tr>
  <tr>
    <td align="center"><a href="http://amberoracle.blog.163.com/"><img src="https://avatars0.githubusercontent.com/u/9973560?v=4?s=100" width="100px;" alt=""/><br /><sub><b>amberhu</b></sub></a><br /><a href="#translation-amberzizi" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/te-riper"><img src="https://avatars3.githubusercontent.com/u/33308188?v=4?s=100" width="100px;" alt=""/><br /><sub><b>te-riper</b></sub></a><br /><a href="#translation-te-riper" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/tlingYX"><img src="https://avatars3.githubusercontent.com/u/28684950?v=4?s=100" width="100px;" alt=""/><br /><sub><b>tlingYX</b></sub></a><br /><a href="#translation-tlingYX" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.red"><img src="https://avatars3.githubusercontent.com/u/12731778?v=4?s=100" width="100px;" alt=""/><br /><sub><b>John Wu</b></sub></a><br /><a href="#translation-wuhan005" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/FirstPunch"><img src="https://avatars0.githubusercontent.com/u/47411716?v=4?s=100" width="100px;" alt=""/><br /><sub><b>FirstPunch</b></sub></a><br /><a href="#translation-FirstPunch" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/chengshao2014"><img src="https://avatars2.githubusercontent.com/u/6170936?v=4?s=100" width="100px;" alt=""/><br /><sub><b>chengshao2014</b></sub></a><br /><a href="#translation-chengshao2014" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/wuzheng40"><img src="https://avatars2.githubusercontent.com/u/1391798?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ryan Wu</b></sub></a><br /><a href="#translation-wuzheng40" title="Translation">🌍</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/lsc77"><img src="https://avatars2.githubusercontent.com/u/17445192?v=4?s=100" width="100px;" alt=""/><br /><sub><b>lsc77</b></sub></a><br /><a href="#translation-lsc77" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/lockemgt"><img src="https://avatars0.githubusercontent.com/u/50262134?v=4?s=100" width="100px;" alt=""/><br /><sub><b>LockeMGT</b></sub></a><br /><a href="#translation-lockemgt" title="Translation">🌍</a></td>
    <td align="center"><a href="https://www.cnblogs.com/Andres/"><img src="https://avatars2.githubusercontent.com/u/24663432?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Li Wang</b></sub></a><br /><a href="#translation-leven87" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/crazePhper"><img src="https://avatars2.githubusercontent.com/u/21233129?v=4?s=100" width="100px;" alt=""/><br /><sub><b>小叮当的肚兜</b></sub></a><br /><a href="#translation-crazePhper" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/arcsinw"><img src="https://avatars3.githubusercontent.com/u/10514065?v=4?s=100" width="100px;" alt=""/><br /><sub><b>arcsinw</b></sub></a><br /><a href="#translation-arcsinw" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/Qnurye"><img src="https://avatars0.githubusercontent.com/u/50016379?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Qnurye</b></sub></a><br /><a href="#translation-Qnurye" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/JerryGai"><img src="https://avatars2.githubusercontent.com/u/38777583?v=4?s=100" width="100px;" alt=""/><br /><sub><b>JerryGai</b></sub></a><br /><a href="#translation-JerryGai" title="Translation">🌍</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://codeigniter.org.cn"><img src="https://avatars1.githubusercontent.com/u/13709?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Hex</b></sub></a><br /><a href="#translation-hex-ci" title="Translation">🌍</a> <a href="#maintenance-hex-ci" title="Maintenance">🚧</a> <a href="#projectManagement-hex-ci" title="Project Management">📆</a> <a href="https://github.com/CodeIgniter-Chinese/codeigniter4-user-guide/pulls?q=is%3Apr+reviewed-by%3Ahex-ci" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/bangbangda"><img src="https://avatars1.githubusercontent.com/u/13864407?v=4?s=100" width="100px;" alt=""/><br /><sub><b>24Kdabaiyang</b></sub></a><br /><a href="#translation-bangbangda" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/tianpanhaha"><img src="https://avatars3.githubusercontent.com/u/8691684?v=4?s=100" width="100px;" alt=""/><br /><sub><b>tianpanhaha</b></sub></a><br /><a href="#translation-tianpanhaha" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/visvoy"><img src="https://avatars1.githubusercontent.com/u/376332?v=4?s=100" width="100px;" alt=""/><br /><sub><b>visvoy</b></sub></a><br /><a href="#translation-visvoy" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/yeye978151"><img src="https://avatars1.githubusercontent.com/u/23291154?v=4?s=100" width="100px;" alt=""/><br /><sub><b>张叶</b></sub></a><br /><a href="#translation-yeye978151" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/binhaiit"><img src="https://avatars0.githubusercontent.com/u/68095133?v=4?s=100" width="100px;" alt=""/><br /><sub><b>binhaiit</b></sub></a><br /><a href="#translation-binhaiit" title="Translation">🌍</a></td>
    <td align="center"><a href="https://www.orz2.com"><img src="https://avatars2.githubusercontent.com/u/9927289?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Kang Jing</b></sub></a><br /><a href="#translation-Instrye" title="Translation">🌍</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/honwooh"><img src="https://avatars.githubusercontent.com/u/46131621?v=4?s=100" width="100px;" alt=""/><br /><sub><b>honwooh</b></sub></a><br /><a href="#translation-honwooh" title="Translation">🌍</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

本项目遵循 [all-contributors](https://github.com/all-contributors/all-contributors) 规范。欢迎任何形式的贡献！
