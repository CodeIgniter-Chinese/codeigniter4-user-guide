############
文本辅助函数
############

文本辅助函数文件包含帮助处理文本的函数。

.. contents::
    :local:
    :depth: 2

加载此辅助函数
===================

使用以下代码加载此辅助函数:

.. literalinclude:: text_helper/001.php

可用函数
===================

以下函数可用:

.. php:function:: random_string([$type = 'alnum'[, $len = 8]])

    :param    string    $type: 随机化类型
    :param    int    $len: 输出字符串长度
    :returns:    随机字符串
    :rtype:    string

    根据你指定的类型和长度生成随机字符串。用于创建密码或生成随机哈希值非常有用。

    .. warning:: 对于类型:**basic**、**md5** 和 **sha1**,生成的字符串在加密上不是安全的。因此,这些类型不能用于加密目的或需要不可猜测返回值的目的。从 v4.3.3 开始,这些类型已弃用。

    第一个参数指定字符串的类型,第二个参数指定长度。可用的选择有:

    - **alpha**:仅包含小写和大写字母的字符串。
    - **alnum**:包含小写和大写字符的字母数字字符串。
    - **basic**:[已弃用]基于 ``mt_rand()`` 的随机数(忽略长度)。
    - **numeric**:数字字符串。
    - **nozero**:不包含零的数字字符串。
    - **md5**:[已弃用]基于 ``md5()`` 的加密随机数(固定长度 32)。
    - **sha1**:[已弃用]基于 ``sha1()`` 的加密随机数(固定长度 40)。
    - **crypto**:基于 ``random_bytes()`` 的随机字符串。

    .. note:: 当你使用 **crypto** 时,必须为第二个参数设置为偶数。从 v4.2.2 开始,如果你设置为奇数,将抛出 ``InvalidArgumentException``。

    .. note:: 从 v4.3.3 开始, **alpha**、**alnum** 和 **nozero** 使用 ``random_byte()``, **numeric** 使用 ``random_int()``。在以前的版本中,它使用在加密上不安全的 ``str_shuffle()``。

    使用示例:

    .. literalinclude:: text_helper/002.php

.. php:function:: increment_string($str[, $separator = '_'[, $first = 1]])

    :param    string    $str: 输入字符串
    :param    string    $separator: 要与重复数字一起追加的分隔符
    :param    int    $first: 起始数字
    :returns:    增量字符串
    :rtype:    string

    通过追加一个数字或增加数字来增加字符串。用于创建文件或数据库内容的“副本”非常有用,这些内容具有唯一的标题或 slug。

    使用示例:

    .. literalinclude:: text_helper/003.php

.. php:function:: alternator($args)

    :param    mixed    $args: 可变数量的参数
    :returns:    交替的字符串
    :rtype:    mixed

    在循环中允许在两个或多个项目之间交替。示例:

    .. literalinclude:: text_helper/004.php

    你可以添加尽可能多的参数,并且在每个循环迭代中将返回下一个项目。

    .. literalinclude:: text_helper/005.php

    .. note:: 要使用对此函数的多个单独调用,只需不带参数调用该函数即可重新初始化。

.. php:function:: reduce_double_slashes($str)

    :param    string    $str: 输入字符串
    :returns:    正规化斜杠的字符串
    :rtype:    string

    将字符串中紧邻出现的多个斜杠转换为单个斜杠,但不包括那些在 URL 协议前缀中找到的斜杠(例如 http&#58;//)。

    示例:

    .. literalinclude:: text_helper/006.php

.. php:function:: strip_slashes($data)

    :param    mixed    $data: 输入字符串或字符串数组
    :returns:    斜杠被剥离的字符串
    :rtype:    mixed

    从字符串数组中删除任何斜杠。

    示例:

    .. literalinclude:: text_helper/007.php

    以上将返回以下数组:

    .. literalinclude:: text_helper/008.php

    .. note:: 出于历史原因,此函数也接受并处理字符串输入。但是,这使它只是一个 ``stripslashes()`` 的别名。

.. php:function:: reduce_multiples($str[, $character = ''[, $trim = false]])

    :param    string    $str: 要搜索的文本
    :param    string    $character: 要缩减的字符
    :param    bool    $trim: 是否也去除指定的字符
    :returns:    缩减后的字符串
    :rtype:    string

    直接相继出现多个特定字符时,减少其出现次数。示例:

    .. literalinclude:: text_helper/009.php

    如果第三个参数设置为 true,则会移除字符串开头和结尾处的字符出现。示例:

    .. literalinclude:: text_helper/010.php

.. php:function:: quotes_to_entities($str)

    :param    string    $str: 输入字符串
    :returns:    引号转换为 HTML 实体的字符串
    :rtype:    string

    将字符串中的单引号和双引号转换为相应的 HTML 实体。示例:

    .. literalinclude:: text_helper/011.php

.. php:function:: strip_quotes($str)

    :param    string    $str: 输入字符串
    :returns:    不带引号的字符串
    :rtype:    string

    从字符串中删除单引号和双引号。示例:

    .. literalinclude:: text_helper/012.php

.. php:function:: word_limiter($str[, $limit = 100[, $end_char = '&#8230;']])

    :param    string    $str: 输入字符串
    :param    int    $limit: 限制
    :param    string    $end_char: 结束字符(通常是省略号)
    :returns:    限制字数的字符串
    :rtype:    string

    将字符串截断为指定的*词数*。示例:

    .. literalinclude:: text_helper/013.php

    第三个参数是一个可选的后缀,添加到字符串末尾。默认它添加一个省略号。

.. php:function:: character_limiter($str[, $n = 500[, $end_char = '&#8230;']])

    :param    string    $str: 输入字符串
    :param    int    $n: 字符数
    :param    string    $end_char: 结束字符(通常是省略号)
    :returns:    限制字符数的字符串
    :rtype:    string

    将字符串截断为指定的*字符数*。它保持词的完整性,所以字符数量可能略多于或略少于你指定的数量。

    示例:

    .. literalinclude:: text_helper/014.php

    第三个参数是一个可选的后缀,如果未声明则此辅助函数使用省略号。

    .. note:: 如果你需要截断为确切的字符数,请参见下面的 :php:func:`ellipsize()` 函数。

.. php:function:: ascii_to_entities($str)

    :param    string    $str: 输入字符串
    :returns:    ASCII 值转换为实体的字符串
    :rtype:    string

    将 ASCII 值转换为字符实体,包括可能在网页中造成问题的高 ASCII 和 MS Word 字符,以便它们可以与浏览器设置无关地一致显示,或者可靠地存储在数据库中。这在一定程度上取决于服务器支持的字符集,所以在所有情况下都可能不完全可靠,但在大多数情况下,它应该正确识别正常范围之外的字符(如带重音的字符)。

    示例:

    .. literalinclude:: text_helper/015.php

.. php:function:: entities_to_ascii($str[, $all = true])

    :param    string    $str: 输入字符串
    :param    bool    $all: 是否也转换不安全的实体
    :returns:    HTML 实体转换为 ASCII 字符的字符串
    :rtype:    string

    此函数与 :php:func:`ascii_to_entities()` 相反。它将字符实体转换回 ASCII。

.. php:function:: convert_accented_characters($str)

    :param    string    $str: 输入字符串
    :returns:    重音字符转换后的字符串
    :rtype:    string

    将高位 ASCII 字符转换为低位 ASCII 等效字符。在只能安全使用标准 ASCII 字符的地方需要非英语字符时很有用,例如 URL 中。

    示例:

    .. literalinclude:: text_helper/016.php

    .. note:: 此函数使用配套的配置文件 **app/Config/ForeignCharacters.php** 来定义音译的 to 和 from 数组。

.. php:function:: word_censor($str, $censored[, $replacement = ''])

    :param    string    $str: 输入字符串
    :param    array    $censored: 要审查的标记词列表
    :param    string    $replacement: 用什么替换标记词
    :returns:    审查后的字符串
    :rtype:    string

    使你能够审查文本字符串中的词。第一个参数将包含原始字符串。第二个将包含你不允许的词数组。第三个(可选)参数可以包含标记词的替换值。如果未指定,它们将被 #### 替换。

    示例:

    .. literalinclude:: text_helper/017.php

.. php:function:: highlight_code($str)

    :param    string    $str: 输入字符串
    :returns:    通过 HTML 着色的字符串
    :rtype:    string

    使用 HTML 对代码字符串(PHP、HTML等)上色。示例:

    .. literalinclude:: text_helper/018.php

    此函数使用 PHP 的 ``highlight_string()`` 函数,因此使用的颜色是在 php.ini 文件中指定的颜色。

.. php:function:: highlight_phrase($str, $phrase[, $tag_open = '<mark>'[, $tag_close = '</mark>']])

    :param    string    $str: 输入字符串
    :param    string    $phrase: 要突出显示的短语
    :param    string    $tag_open: 用于突出显示的开标签
    :param    string    $tag_close: 突出显示的闭标签
    :returns:    通过 HTML 突出显示短语的字符串
    :rtype:    string

    将文本字符串中的短语突出显示。第一个参数将包含原始字符串,第二个将包含你希望突出显示的短语。第三和第四个参数将包含你希望短语包裹在里面的开启/关闭 HTML 标记。

    示例:

    .. literalinclude:: text_helper/019.php

    以上代码打印::

        Here is a <span style="color:#990000;">nice text</span> string about nothing in particular.

    .. note:: 此函数过去默认使用 ``<strong>`` 标签。旧版浏览器可能不支持新的 HTML5 mark 标签,因此如果你需要支持这样的浏览器,
        建议你将以下 CSS 代码插入样式表中::

            mark {
                background: #ff0;
                color: #000;
            };

.. php:function:: word_wrap($str[, $charlim = 76])

    :param    string    $str: 输入字符串
    :param    int    $charlim: 字符限制
    :returns:    自动换行的字符串
    :rtype:    string

    在保持完整单词的同时,在指定的*字符数*处换行文本。

    示例:

    .. literalinclude:: text_helper/020.php

.. php:function:: ellipsize($str, $max_length[, $position = 1[, $ellipsis = '&hellip;']])

    :param    string    $str: 输入字符串
    :param    int    $max_length: 字符串长度限制
    :param    mixed    $position: 拆分位置(整数或浮点数)
    :param    string    $ellipsis: 要用作省略号的字符
    :returns:    省略的字符串
    :rtype:    string

    此函数将从字符串中剥离标签,在定义的最大长度处对其进行拆分,并在前后插入省略号。

    第一个参数是要提取摘录的字符串,第二个是最终字符串中的字符数。第三个参数是省略号应出现的字符串中的位置,从 0 到 1,从左到右。例如。值为 1 将省略号放在字符串的右边,.5 在中间,0 在左边。

    可选的第四个参数是省略号的类型。默认情况下,将插入 &hellip;。

    示例:

    .. literalinclude:: text_helper/021.php

    产生::

        this_string_is_e&hellip;ak_my_design.jpg

.. php:function:: excerpt($text, $phrase = false, $radius = 100, $ellipsis = '...')

    :param    string    $text: 要提取摘录的文本
    :param    string    $phrase: 要围绕其提取文本的短语或单词
    :param    int        $radius: $phrase 前后的字符数
    :param    string    $ellipsis: 要用作省略号的字符
    :returns:    摘录。
    :rtype:        string

    此函数将在中心短语 $phrase 前后提取 $radius 个字符,在前后都有省略号。

    第一个参数是要提取摘录的文本,第二个是计数前后中间的单词或短语。第三个参数是中央短语前后要计数的字符数。如果没有传递短语,摘录将包括第一个 $radius 个字符,以及末尾的省略号。

    示例:

    .. literalinclude:: text_helper/022.php

    产生::

        ... non mauris lectus. Phasellus eu sodales sem. Integer dictum purus ac
        enim hendrerit gravida. Donec ac magna vel nunc tincidunt molestie sed
        vitae nisl. Cras sed auctor mauris, non dictum tortor. ...
