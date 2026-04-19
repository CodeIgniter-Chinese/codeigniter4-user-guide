############
文本辅助函数
############

文本辅助函数文件包含了一系列辅助处理文本的函数。

.. contents::
    :local:
    :depth: 2

加载辅助函数
===================

使用以下代码加载此辅助函数：

.. literalinclude:: text_helper/001.php

可用函数
===================

提供以下函数：

.. php:function:: random_string([$type = 'alnum'[, $len = 8]])

    :param    string    $type: 随机化类型
    :param    int    $len: 输出字符串长度
    :returns:    随机字符串
    :rtype:    string

    根据指定的类型和长度生成随机字符串。适用于创建密码或生成随机哈希值。

    第一个参数指定字符串类型，第二个参数指定长度。可选类型如下：

    - **alpha**: 仅包含大小写字母的字符串。
    - **alnum**: 包含大小写字母和数字的字母数字字符串。
    - **numeric**: 数字字符串。
    - **nozero**: 不含 0 的数字字符串。
    - **crypto**: 基于 ``random_bytes()`` 的随机字符串。

    .. note:: 使用 **crypto** 时，第二个参数必须设为偶数。自 v4.2.2 起，若设为奇数，将抛出 ``InvalidArgumentException`` 异常。

    .. note:: 自 v4.3.3 起，**alpha**、**alnum** 和 **nozero** 使用 ``random_byte()``，**numeric** 使用 ``random_int()``。在之前的版本中，这些类型使用的是并非加密安全的 ``str_shuffle()``。

    用法示例：

    .. literalinclude:: text_helper/002.php

.. php:function:: increment_string($str[, $separator = '_'[, $first = 1]])

    :param    string    $str: 输入字符串
    :param    string    $separator: 用于追加重复数字的分隔符
    :param    int    $first: 起始数字
    :returns:    递增后的字符串
    :rtype:    string

    通过在字符串后追加数字或增加原有数字来递增字符串。适用于创建文件“副本”，或复制具有唯一标题或别名的数据库内容。

    用法示例：

    .. literalinclude:: text_helper/003.php

.. php:function:: alternator($args)

    :param    mixed    $args: 可变数量的参数
    :returns:    交替后的字符串
    :rtype:    mixed

    用于在循环中交替使用两个或多个项目。示例：

    .. literalinclude:: text_helper/004.php

    可根据需要添加任意数量的参数，每次循环迭代时将返回下一个项目。

    .. literalinclude:: text_helper/005.php

    .. note:: 若要多次独立调用此函数，只需在调用时不带任何参数即可重新初始化。

.. php:function:: reduce_double_slashes($str)

    :param    string    $str: 输入字符串
    :returns:    格式化斜杠后的字符串
    :rtype:    string

    将字符串中的双斜杠转换为单斜杠，但会忽略 URL 协议前缀（如 http&#58;//）中的双斜杠。

    示例：

    .. literalinclude:: text_helper/006.php

.. php:function:: strip_slashes($data)

    :param    mixed    $data: 输入字符串或字符串数组
    :returns:    移除斜杠后的字符串或数组
    :rtype:    mixed

    移除字符串数组中的所有斜杠。

    示例：

    .. literalinclude:: text_helper/007.php

    以上代码将返回以下数组：

    .. literalinclude:: text_helper/008.php

    .. note:: 出于历史原因，此函数也支持并处理字符串输入。此时，它仅作为 ``stripslashes()`` 的别名。

.. php:function:: reduce_multiples($str[, $character = ','[, $trim = false]])

    :param    string    $str: 待搜索文本
    :param    string    $character: 待压缩字符
    :param    bool    $trim: 是否同时 trim 指定的字符
    :returns:    压缩后的字符串
    :rtype:    string

    压缩连续出现的多个特定字符。示例：

    .. literalinclude:: text_helper/009.php

    若第三个参数设为 ``true``，则会同时移除字符串首尾出现的该字符。示例：

    .. literalinclude:: text_helper/010.php

.. php:function:: quotes_to_entities($str)

    :param    string    $str: 输入字符串
    :returns:    引号转换为 HTML 实体后的字符串
    :rtype:    string

    将字符串中的单引号和双引号转换为对应的 HTML 实体。示例：

    .. literalinclude:: text_helper/011.php

.. php:function:: strip_quotes($str)

    :param    string    $str: 输入字符串
    :returns:    移除引号后的字符串
    :rtype:    string

    移除字符串中的单引号和双引号。示例：

    .. literalinclude:: text_helper/012.php

.. php:function:: word_limiter($str[, $limit = 100[, $endChar = '&#8230;']])

    :param    string    $str: 输入字符串
    :param    int    $limit: 限制数量
    :param    string    $endChar: 结束字符（通常为省略号）
    :returns:    截断后的字符串
    :rtype:    string

    将字符串截断为指定的 **单词** 数。示例：

    .. literalinclude:: text_helper/013.php

    第三个参数是添加到字符串末尾的可选后缀，默认使用省略号。

.. php:function:: character_limiter($string[, $limit = 500[, $endChar = '&#8230;']])

    :param    string    $string: 输入字符串
    :param    int    $limit: 字符数
    :param    string    $endChar: 结束字符（通常为省略号）
    :returns:    截断后的字符串
    :rtype:    string

    将字符串截断为指定的 **字符** 数。该函数会保持单词的完整性，因此字符数可能会略多或略少于设定值。

    示例：

    .. literalinclude:: text_helper/014.php

    第三个参数是添加到字符串末尾的可选后缀。若未声明，则使用省略号。

    .. note:: 如需截断为精确数量的字符，请参阅下文的 :php:func:`ellipsize()` 函数。

.. php:function:: ascii_to_entities($str)

    :param    string    $str: 输入字符串
    :returns:    ASCII 值转换为实体后的字符串
    :rtype:    string

    将 ASCII 值转换为字符实体（包括在网页中使用时可能引起问题的扩展 ASCII 和 MS Word 字符）。由此，无论浏览器如何设置都能一致显示，或可靠地存储到数据库中。此函数在一定程度上取决于服务器支持的字符集，因此在某些情况下可能并非 100% 可靠，但在大多数情况下，它能正确识别常规范围之外的字符（如重音字符）。

    示例：

    .. literalinclude:: text_helper/015.php

.. php:function:: entities_to_ascii($str[, $all = true])

    :param    string    $str: 输入字符串
    :param    bool    $all: 是否也转换不安全实体
    :returns:    HTML 实体转换为 ASCII 字符后的字符串
    :rtype:    string

    此函数功能与 :php:func:`ascii_to_entities()` 相反，负责将字符实体转回 ASCII。

.. php:function:: convert_accented_characters($str)

    :param    string    $str: 输入字符串
    :returns:    重音字符转换后的字符串
    :rtype:    string

    将高位 ASCII 字符音译为对应的低位 ASCII 字符。适用于必须使用标准 ASCII 字符的场景（如 URL）中处理非英语字符。

    示例：

    .. literalinclude:: text_helper/016.php

    .. note:: 此函数使用配套配置文件 **app/Config/ForeignCharacters.php** 来定义音译所需的转换数组。

.. php:function:: word_censor($str, $censored[, $replacement = ''])

    :param    string    $str: 输入字符串
    :param    array    $censored: 待过滤的敏感词列表
    :param    string    $replacement: 用于替换敏感词的内容
    :returns:    过滤后的字符串
    :rtype:    string

    用于过滤文本字符串中的词汇。第一个参数为原始字符串，第二个参数为禁用的词汇数组。第三个参数（可选）为替换值。若未指定，敏感词将被替换为井号：####。

    示例：

    .. literalinclude:: text_helper/017.php

.. php:function:: highlight_code($str)

    :param    string    $str: 输入字符串
    :returns:    经 HTML 高亮处理后的代码字符串
    :rtype:    string

    为代码字符串（PHP、HTML 等）着色。示例：

    .. literalinclude:: text_helper/018.php

    此函数使用 PHP 的 ``highlight_string()`` 函数，因此所用颜色为 php.ini 文件中指定的颜色。

.. php:function:: highlight_phrase($str, $phrase[, $tag_open = '<mark>'[, $tag_close = '</mark>']])

    :param    string    $str: 输入字符串
    :param    string    $phrase: 待高亮的短语
    :param    string    $tag_open: 用于高亮的起始标签
    :param    string    $tag_close: 用于高亮的结束标签
    :returns:    经 HTML 高亮处理后的短语字符串
    :rtype:    string

    高亮文本字符串中的特定短语。第一个参数为原始字符串，第二个参数为待高亮的短语。第三个和第四个参数为包裹短语的 HTML 起始/结束标签。

    示例：

    .. literalinclude:: text_helper/019.php

    以上代码输出::

        Here is a <span style="color:#990000;">nice text</span> string about nothing in particular.

    .. note:: 此函数以前默认使用 ``<strong>`` 标签。旧版浏览器可能不支持 HTML5 的 mark 标签。如需支持此类浏览器，建议在样式表中插入以下 CSS 代码
        ::

            mark {
                background: #ff0;
                color: #000;
            };

.. php:function:: word_wrap($str[, $charlim = 76])

    :param    string    $str: 输入字符串
    :param    int    $charlim: 字符限制
    :returns:    换行处理后的字符串
    :rtype:    string

    在保持单词完整的前提下，按指定的 **字符** 数对文本进行换行处理。

    示例：

    .. literalinclude:: text_helper/020.php

.. php:function:: ellipsize($str, $max_length[, $position = 1[, $ellipsis = '&hellip;']])

    :param    string    $str: 输入字符串
    :param    int    $max_length: 字符串长度限制
    :param    mixed    $position: 分割位置（整数或浮点数）
    :param    string    $ellipsis: 用作省略号的字符
    :returns:    省略处理后的字符串
    :rtype:    string

    此函数会从字符串中移除标签，按设定的最大长度截断并插入省略号。

    第一个参数是待处理字符串，第二个参数是最终字符串的字符数。第三个参数决定省略号出现的位置（0 - 1，从左至右）。例如：1 表示省略号在字符串右侧，0.5 表示在中间，0 表示在左侧。

    可选的第四个参数是省略号的类型。默认插入 &hellip;。

    示例：

    .. literalinclude:: text_helper/021.php

    输出：:

        this_string_is_e&hellip;ak_my_design.jpg

.. php:function:: excerpt($text, $phrase = false, $radius = 100, $ellipsis = '...')

    :param    string    $text: 待提取摘要的文本
    :param    string    $phrase: 用于提取周边文本的核心短语或单词
    :param    int        $radius: $phrase 前后的字符数
    :param    string    $ellipsis: 用作省略号的字符
    :returns:    文本摘要。
    :rtype:        string

    此函数会提取中心短语 ``$phrase`` 前后各 ``$radius`` 个字符，并在首尾添加省略号。

    第一个参数是待提取摘要的文本，第二个参数是用于计算前后长度的核心词或短语。第三个参数是核心短语前后需保留的字符数。若未传递短语，摘要将包含前 ``$radius`` 个字符并在末尾添加省略号。

    示例：

    .. literalinclude:: text_helper/022.php

    输出::

        ... non mauris lectus. Phasellus eu sodales sem. Integer dictum purus ac
        enim hendrerit gravida. Donec ac magna vel nunc tincidunt molestie sed
        vitae nisl. Cras sed auctor mauris, non dictum tortor. ...
