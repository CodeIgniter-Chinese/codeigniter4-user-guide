############
文本辅助函数
############

文本辅助函数文件包含用于处理文本的辅助函数。

.. contents::
    :local:
    :depth: 2

加载辅助函数
===================

使用以下代码加载本辅助函数：

.. literalinclude:: text_helper/001.php

可用函数
===================

以下函数可用：

.. php:function:: random_string([$type = 'alnum'[, $len = 8]])

    :param    string    $type: 随机化类型
    :param    int    $len: 输出字符串长度
    :returns:    随机字符串
    :rtype:    string

    根据你指定的类型和长度生成随机字符串。适用于创建密码或生成随机哈希值。

    .. warning:: 对于 **basic**、**md5** 和 **sha1** 类型，生成的字符串不具备加密安全性。因此这些类型不能用于加密用途或需要不可预测返回值的场景。自 v4.3.3 起这些类型已弃用。

    第一个参数指定字符串类型，第二个参数指定长度。可用选项包括：

    - **alpha**: 仅包含大小写字母的字符串
    - **alnum**: 包含大小写字母和数字的字符串
    - **basic**: [已弃用] 基于 ``mt_rand()`` 的随机数（长度参数无效）
    - **numeric**: 纯数字字符串
    - **nozero**: 不含零的数字字符串
    - **md5**: [已弃用] 基于 ``md5()`` 加密的随机数（固定长度 32）
    - **sha1**: [已弃用] 基于 ``sha1()`` 加密的随机数（固定长度 40）
    - **crypto**: 基于 ``random_bytes()`` 的加密安全随机字符串

    .. note:: 使用 **crypto** 类型时，第二个参数必须设置为偶数。自 v4.2.2 起，如果传入奇数将抛出 ``InvalidArgumentException``。

    .. note:: 自 v4.3.3 起，**alpha**、**alnum** 和 **nozero** 改用 ``random_byte()``，**numeric** 改用 ``random_int()``。旧版本使用不具备加密安全性的 ``str_shuffle()``。

    使用示例：

    .. literalinclude:: text_helper/002.php

.. php:function:: increment_string($str[, $separator = '_'[, $first = 1]])

    :param    string    $str: 输入字符串
    :param    string    $separator: 重复数字的分隔符
    :param    int    $first: 起始数字
    :returns:    递增后的字符串
    :rtype:    string

    通过在字符串末尾追加数字或递增现有数字来实现字符串递增。适用于创建文件"副本"或复制具有唯一标题/slug 的数据库内容。

    使用示例：

    .. literalinclude:: text_helper/003.php

.. php:function:: alternator($args)

    :param    mixed    $args: 可变数量参数
    :returns:    交替输出的字符串
    :rtype:    mixed

    允许在循环中交替输出两个或多个项目。示例：

    .. literalinclude:: text_helper/004.php

    可以添加任意数量的参数，每次循环迭代会返回下一个项目。

    .. literalinclude:: text_helper/005.php

    .. note:: 要初始化多次独立调用，只需不带参数调用本函数即可重置状态。

.. php:function:: reduce_double_slashes($str)

    :param    string    $str: 输入字符串
    :returns:    标准化斜杠后的字符串
    :rtype:    string

    将字符串中的双斜杠转换为单斜杠，URL 协议前缀中的双斜杠除外（例如 http&#58;//）。

    示例：

    .. literalinclude:: text_helper/006.php

.. php:function:: strip_slashes($data)

    :param    mixed    $data: 输入字符串或字符串数组
    :returns:    去除斜杠后的字符串或数组
    :rtype:    mixed

    从字符串数组中移除所有斜杠。

    示例：

    .. literalinclude:: text_helper/007.php

    上述代码将返回：

    .. literalinclude:: text_helper/008.php

    .. note:: 由于历史原因，本函数也接受并处理字符串输入，这使得它成为 ``stripslashes()`` 的别名。

.. php:function:: reduce_multiples($str[, $character = ','[, $trim = false]])

    :param    string    $str: 输入文本
    :param    string    $character: 需要缩减的字符
    :param    bool    $trim: 是否同时去除首尾字符
    :returns:    缩减后的字符串
    :rtype:    string

    缩减连续出现的重复字符。示例：

    .. literalinclude:: text_helper/009.php

    如果第三个参数设为 ``true``，将同时去除字符串首尾的指定字符。示例：

    .. literalinclude:: text_helper/010.php

.. php:function:: quotes_to_entities($str)

    :param    string    $str: 输入字符串
    :returns:    引号转换为 HTML 实体后的字符串
    :rtype:    string

    将字符串中的单双引号转换为对应的 HTML 实体。示例：

    .. literalinclude:: text_helper/011.php

.. php:function:: strip_quotes($str)

    :param    string    $str: 输入字符串
    :returns:    去除引号后的字符串
    :rtype:    string

    移除字符串中的单双引号。示例：

    .. literalinclude:: text_helper/012.php

.. php:function:: word_limiter($str[, $limit = 100[, $endChar = '&#8230;']])

    :param    string    $str: 输入字符串
    :param    int    $limit: 单词数量限制
    :param    string    $endChar: 结尾字符（通常为省略号）
    :returns:    单词截断后的字符串
    :rtype:    string

    将字符串截断为指定数量的单词。示例：

    .. literalinclude:: text_helper/013.php

    第三个参数是可选的结尾后缀，默认添加省略号。

.. php:function:: character_limiter($string[, $limit = 500[, $endChar = '&#8230;']])

    :param    string    $string: 输入字符串
    :param    int    $limit: 字符数量
    :param    string    $endChar: 结尾字符（通常为省略号）
    :returns:    字符截断后的字符串
    :rtype:    string

    将字符串截断为指定数量的 *字符*，同时保持单词完整性，实际字符数可能略多于或少于指定值。

    示例：

    .. literalinclude:: text_helper/014.php

    第三个参数是可选的结尾后缀，未声明时使用省略号。

    .. note:: 如需精确截断到指定字符数，请参考下方 :php:func:`ellipsize()` 函数。

.. php:function:: ascii_to_entities($str)

    :param    string    $str: 输入字符串
    :returns:    ASCII 转换为实体后的字符串
    :rtype:    string

    将 ASCII 值转换为字符实体，包括可能引发网页显示问题的高位 ASCII 和 MS Word 字符，确保在不同浏览器设置下显示一致或可靠存储于数据库。由于依赖服务器支持的字符集，在极少数情况下可能不完全可靠，但能正确识别常规范围外的字符（如带重音符号的字符）。

    示例：

    .. literalinclude:: text_helper/015.php

.. php:function:: entities_to_ascii($str[, $all = true])

    :param    string    $str: 输入字符串
    :param    bool    $all: 是否转换不安全实体
    :returns:    实体转换回 ASCII 后的字符串
    :rtype:    string

    本函数功能与 :php:func:`ascii_to_entities()` 相反，将字符实体转换回 ASCII。

.. php:function:: convert_accented_characters($str)

    :param    string    $str: 输入字符串
    :returns:    转换重音字符后的字符串
    :rtype:    string

    将高位 ASCII 字符转写为对应的低位 ASCII 字符。适用于需要在仅支持标准 ASCII 的场合（如 URL）使用非英文字符的场景。

    示例：

    .. literalinclude:: text_helper/016.php

    .. note:: 本函数使用配置文件 **app/Config/ForeignCharacters.php** 来定义转写对照表。

.. php:function:: word_censor($str, $censored[, $replacement = ''])

    :param    string    $str: 输入字符串
    :param    array    $censored: 需屏蔽的敏感词列表
    :param    string    $replacement: 替换内容
    :returns:    敏感词过滤后的字符串
    :rtype:    string

    对文本中的敏感词进行过滤替换。第一个参数是原始字符串，第二个是敏感词数组，第三个（可选）是替换内容（默认使用井号 #### 替换）。

    示例：

    .. literalinclude:: text_helper/017.php

.. php:function:: highlight_code($str)

    :param    string    $str: 输入字符串
    :returns:    代码高亮后的 HTML 字符串
    :rtype:    string

    对代码字符串（PHP、HTML 等）进行语法高亮。示例：

    .. literalinclude:: text_helper/018.php

    本函数使用 PHP 的 ``highlight_string()``，颜色方案取决于 php.ini 中的设置。

.. php:function:: highlight_phrase($str, $phrase[, $tag_open = '<mark>'[, $tag_close = '</mark>']])

    :param    string    $str: 输入字符串
    :param    string    $phrase: 需高亮的短语
    :param    string    $tag_open: 高亮起始标签
    :param    string    $tag_close: 高亮结束标签
    :returns:    短语高亮后的 HTML 字符串
    :rtype:    string

    在文本中高亮指定短语。第一个参数是原始字符串，第二个是要高亮的短语，第三、四个参数是包裹短语的 HTML 标签。

    示例：

    .. literalinclude:: text_helper/019.php

    上述代码输出::

        Here is a <span style="color:#990000;">nice text</span> string about nothing in particular.

    .. note:: 本函数曾默认使用 ``<strong>`` 标签。如需支持旧版浏览器，建议在样式表中添加以下 CSS
        ::

            mark {
                background: #ff0;
                color: #000;
            };

.. php:function:: word_wrap($str[, $charlim = 76])

    :param    string    $str: 输入字符串
    :param    int    $charlim: 字符限制数
    :returns:    自动换行后的字符串
    :rtype:    string

    在指定字符数处进行换行，同时保持单词完整。

    示例：

    .. literalinclude:: text_helper/020.php

.. php:function:: ellipsize($str, $max_length[, $position = 1[, $ellipsis = '&hellip;']])

    :param    string    $str: 输入字符串
    :param    int    $max_length: 最大长度限制
    :param    mixed    $position: 分割位置（整数或浮点数）
    :param    string    $ellipsis: 省略符号
    :returns:    添加省略号后的字符串
    :rtype:    string

    本函数会去除标签，按最大长度分割字符串，并插入省略号。

    第一个参数是待处理字符串，第二个是最终字符串长度，第三个是省略号位置（0-1 表示从左到右，例如 1 在右侧，0.5 在中部，0 在左侧），第四个可选参数指定省略符号（默认使用 &hellip;）。

    示例：

    .. literalinclude:: text_helper/021.php

    输出::

        this_string_is_e&hellip;ak_my_design.jpg

.. php:function:: excerpt($text, $phrase = false, $radius = 100, $ellipsis = '...')

    :param    string    $text: 待提取文本
    :param    string    $phrase: 中心短语
    :param    int        $radius: 前后提取字符数
    :param    string    $ellipsis: 省略符号
    :returns:    提取的摘要
    :rtype:        string

    本函数以指定短语为中心，提取前后各 $radius 个字符的文本，并在两端添加省略号。

    第一个参数是源文本，第二个是中心短语，第三个是提取半径，第四个是省略符号。如果未传入短语，则提取前 $radius 个字符并在末尾加省略号。

    示例：

    .. literalinclude:: text_helper/022.php

    输出::

        ... non mauris lectus. Phasellus eu sodales sem. Integer dictum purus ac
        enim hendrerit gravida. Donec ac magna vel nunc tincidunt molestie sed
        vitae nisl. Cras sed auctor mauris, non dictum tortor. ...
