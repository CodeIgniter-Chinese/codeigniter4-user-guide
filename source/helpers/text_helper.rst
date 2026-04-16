############
文本辅助函数
############

文本辅助函数文件包含协助处理文本的函数。

.. contents::
    :local:
    :depth: 2

加载此辅助函数
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

    根据指定的类型和长度生成随机字符串。
    用于创建密码或生成随机哈希。

    .. warning:: 对于类型：**basic**、**md5** 和 **sha1**，生成的字符串
        不是加密安全的。因此，这些类型不能用于加密目的或需要不可预测返回值的目的。
        自 v4.3.3 起，这些类型已被弃用。

    第一个参数指定字符串类型，第二个参数指定长度。
    可用选项如下：

    - **alpha**: 仅包含大小写字母的字符串。
    - **alnum**: 包含大小写字母和数字的字母数字字符串。
    - **basic**: [已弃用] 基于 ``mt_rand()`` 的随机数（忽略长度）。
    - **numeric**: 数字字符串。
    - **nozero**: 不包含零的数字字符串。
    - **md5**: [已弃用] 基于 ``md5()`` 的加密随机数（固定长度 32）。
    - **sha1**: [已弃用] 基于 ``sha1()`` 的加密随机数（固定长度 40）。
    - **crypto**: 基于 ``random_bytes()`` 的随机字符串。

    .. note:: 使用 **crypto** 时，必须为第二个参数设置偶数。
        自 v4.2.2 起，如果设置奇数，将抛出 ``InvalidArgumentException`` 异常。

    .. note:: 自 v4.3.3 起，**alpha**、**alnum** 和 **nozero** 使用 ``random_byte()``,
        而 **numeric** 使用 ``random_int()``。
        在之前的版本中，它使用非加密安全的 ``str_shuffle()``。

    使用示例：

    .. literalinclude:: text_helper/002.php

.. php:function:: increment_string($str[, $separator = '_'[, $first = 1]])

    :param    string    $str: 输入字符串
    :param    string    $separator: 用于附加重复数字的分隔符
    :param    int    $first: 起始数字
    :returns:    递增后的字符串
    :rtype:    string

    通过附加数字或增加数字来递增字符串。
    用于创建文件"副本"或复制具有唯一标题或别名的数据库内容。

    使用示例：

    .. literalinclude:: text_helper/003.php

.. php:function:: alternator($args)

    :param    mixed    $args: 可变数量的参数
    :returns:    交替的字符串
    :rtype:    mixed

    允许在循环遍历时交替使用两个或更多项目。示例：

    .. literalinclude:: text_helper/004.php

    可以添加任意数量的参数，在循环的每次迭代中，将返回下一个项目。

    .. literalinclude:: text_helper/005.php

    .. note:: 要多次单独调用此函数，只需调用不带参数的函数即可重新初始化。

.. php:function:: reduce_double_slashes($str)

    :param    string    $str: 输入字符串
    :returns:    规范化斜杠的字符串
    :rtype:    string

    将字符串中的双斜杠转换为单斜杠，URL 协议前缀中的斜杠除外（如 http&#58;//）。

    示例：

    .. literalinclude:: text_helper/006.php

.. php:function:: strip_slashes($data)

    :param    mixed    $data: 输入字符串或字符串数组
    :returns:    移除斜杠的字符串或字符串数组
    :rtype:    mixed

    从字符串数组中移除所有斜杠。

    示例：

    .. literalinclude:: text_helper/007.php

    上述代码将返回以下数组：

    .. literalinclude:: text_helper/008.php

    .. note:: 出于历史原因，此函数也会接受和处理字符串输入。
        但这使其成为 ``stripslashes()`` 的别名。

.. php:function:: reduce_multiples($str[, $character = ','[, $trim = false]])

    :param    string    $str: 要搜索的文本
    :param    string    $character: 要减少的字符
    :param    bool    $trim: 是否同时修剪指定字符
    :returns:    减少后的字符串
    :rtype:    string

    减少连续出现的特定字符实例。示例：

    .. literalinclude:: text_helper/009.php

    如果第三个参数设置为 ``true``，它将移除字符串开头和结尾的字符。示例：

    .. literalinclude:: text_helper/010.php

.. php:function:: quotes_to_entities($str)

    :param    string    $str: 输入字符串
    :returns:    引号转换为 HTML 实体的字符串
    :rtype:    string

    将字符串中的单引号和双引号转换为相应的 HTML 实体。示例：

    .. literalinclude:: text_helper/011.php

.. php:function:: strip_quotes($str)

    :param    string    $str: 输入字符串
    :returns:    移除引号的字符串
    :rtype:    string

    从字符串中移除单引号和双引号。示例：

    .. literalinclude:: text_helper/012.php

.. php:function:: word_limiter($str[, $limit = 100[, $endChar = '&#8230;']])

    :param    string    $str: 输入字符串
    :param    int    $limit: 单词数量限制
    :param    string    $endChar: 结尾字符（通常是省略号）
    :returns:    截断后的字符串
    :rtype:    string

    将字符串截断到指定的 *单词* 数。示例：

    .. literalinclude:: text_helper/013.php

    第三个参数是添加到字符串的可选后缀。默认情况下，它会添加省略号。

.. php:function:: character_limiter($string[, $limit = 500[, $endChar = '&#8230;']])

    :param    string    $string: 输入字符串
    :param    int    $limit: 字符数
    :param    string    $endChar: 结尾字符（通常是省略号）
    :returns:    截断后的字符串
    :rtype:    string

    将字符串截断到指定的 *字符* 数。
    它会保持单词的完整性，因此字符计数可能比指定的稍多或稍少。

    示例：

    .. literalinclude:: text_helper/014.php

    第三个参数是添加到字符串的可选后缀，如果未声明，此辅助函数会使用省略号。

    .. note:: 如果需要截断到精确的字符数，请查看下面的 :php:func:`ellipsize()` 函数。

.. php:function:: ascii_to_entities($str)

    :param    string    $str: 输入字符串
    :returns:    ASCII 值转换为实体的字符串
    :rtype:    string

    将 ASCII 值转换为字符实体（包括那些在网页中使用时可能引发问题的高位 ASCII 和 MS Word 字符），
    以便它们无论在何种浏览器设置下都能一致地显示，或能被可靠地存储在数据库中。
    此功能在一定程度上依赖于服务器支持的字符集，
    因此可能无法在所有情况下都 100% 可靠，但在大多数情况下，
    它应该能正确识别标准范围之外的字符（例如带重音符号的字符）。

    示例：

    .. literalinclude:: text_helper/015.php

.. php:function:: entities_to_ascii($str[, $all = true])

    :param    string    $str: 输入字符串
    :param    bool    $all: 是否也转换不安全的实体
    :returns:    HTML 实体转换为 ASCII 字符的字符串
    :rtype:    string

    此函数与 :php:func:`ascii_to_entities()` 的功能相反。
    它将字符实体转换回 ASCII。

.. php:function:: convert_accented_characters($str)

    :param    string    $str: 输入字符串
    :returns:    重音字符已转换的字符串
    :rtype:    string

    将高位 ASCII 字符转换为对应的低位 ASCII 字符。
    当需要在仅能安全使用标准 ASCII 字符的场合（例如 URL 中）使用非英文字符时，此功能非常有用。

    示例：

    .. literalinclude:: text_helper/016.php

    .. note:: 此函数使用配套的配置文件
        **app/Config/ForeignCharacters.php** 来定义用于转写的源字符与目标字符数组。

.. php:function:: word_censor($str, $censored[, $replacement = ''])

    :param    string    $str: 输入字符串
    :param    array    $censored: 需要过滤的敏感词列表
    :param    string    $replacement: 用于替换敏感词的内容
    :returns:    过滤后的字符串
    :rtype:    string

    用于过滤文本字符串中的敏感词。第一个参数是原始字符串。
    第二个参数是包含被禁词汇的数组。第三个参数（可选）可包含用于替换这些词的内容。
    若未指定，它们将被替换为井号：####。

    示例：

    .. literalinclude:: text_helper/017.php

.. php:function:: highlight_code($str)

    :param    string    $str: 输入字符串
    :returns:    通过 HTML 高亮显示代码的字符串
    :rtype:    string

    为代码字符串（PHP、HTML 等）添加颜色。示例：

    .. literalinclude:: text_helper/018.php

    此函数使用 PHP 的 ``highlight_string()`` 函数，因此使用的颜色是在 php.ini 文件中指定的颜色。

.. php:function:: highlight_phrase($str, $phrase[, $tag_open = '<mark>'[, $tag_close = '</mark>']])

    :param    string    $str: 输入字符串
    :param    string    $phrase: 要高亮显示的短语
    :param    string    $tag_open: 用于高亮显示的起始标签
    :param    string    $tag_close: 高亮显示的闭合标签
    :returns:    通过 HTML 高亮显示短语的字符串
    :rtype:    string

    将在文本字符串中高亮显示一个短语。第一个参数包含原始字符串，
    第二个参数包含要高亮显示的短语。第三和第四个参数包含
    用于包装短语的起始/闭合 HTML 标签。

    示例：

    .. literalinclude:: text_helper/019.php

    上述代码输出::

        Here is a <span style="color:#990000;">nice text</span> string about nothing in particular.

    .. note:: 此函数默认使用 ``<strong>`` 标签。较旧的浏览器
        可能不支持新的 HTML5 mark 标签，因此如果需要支持此类浏览器，
        建议在样式表中插入以下 CSS 代码::

            mark {
                background: #ff0;
                color: #000;
            };

.. php:function:: word_wrap($str[, $charlim = 76])

    :param    string    $str: 输入字符串
    :param    int    $charlim: 字符限制
    :returns:    自动换行的字符串
    :rtype:    string

    在指定的 *字符* 数处换行文本，同时保持完整的单词。

    示例：

    .. literalinclude:: text_helper/020.php

.. php:function:: ellipsize($str, $max_length[, $position = 1[, $ellipsis = '&hellip;']])

    :param    string    $str: 输入字符串
    :param    int    $max_length: 字符串长度限制
    :param    mixed    $position: 分割位置（整数或浮点数）
    :param    string    $ellipsis: 用作省略号的字符
    :returns:    截断后的字符串
    :rtype:    string

    此函数将从字符串中去除标签，在定义的最大长度处分割，并插入省略号。

    第一个参数是待处理的字符串，第二个是最终字符串中的字符数。
    第三个参数是省略号在字符串中的位置，从 0 - 1，从左到右。
    例如，值为 1 将省略号放在字符串右侧，.5 在中间，0 在左侧。

    可选的第四个参数是省略号的类型。默认情况下，将插入 &hellip;。

    示例：

    .. literalinclude:: text_helper/021.php

    输出::

        this_string_is_e&hellip;ak_my_design.jpg

.. php:function:: excerpt($text, $phrase = false, $radius = 100, $ellipsis = '...')

    :param    string    $text: 待提取文本
    :param    string    $phrase: 中心短语
    :param    int        $radius: $phrase 前后的字符数
    :param    string    $ellipsis: 用作省略号的字符
    :returns:    提取的摘要
    :rtype:        string

    本函数以指定短语为中心，提取前后各 $radius 个字符的文本，并在两端添加省略号。

    第一个参数是用于提取摘录的文本，第二个参数是用来定位前后截取范围的中心单词或短语。
    第三个参数是中心短语前后需要保留的字符数。若未传入短语，摘录将包含前 $radius 个字符，
    并在末尾添加省略号。

    示例：

    .. literalinclude:: text_helper/022.php

    输出::

        ... non mauris lectus. Phasellus eu sodales sem. Integer dictum purus ac
        enim hendrerit gravida. Donec ac magna vel nunc tincidunt molestie sed
        vitae nisl. Cras sed auctor mauris, non dictum tortor. ...
