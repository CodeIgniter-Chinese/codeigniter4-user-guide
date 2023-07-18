##############
HTML 辅助函数
##############

HTML 辅助函数文件包含了帮助处理 HTML 的函数。

.. contents::
    :local:
    :depth: 2

配置
=============

从 ``v4.3.0`` 开始,``html_helper`` 函数中的空 HTML 元素(如 ``<img>``)默认为兼容 HTML5,如果你需要兼容 XHTML,必须在 **app/Config/DocTypes.php** 中将 ``$html5`` 属性设置为 ``false``。

加载此辅助函数
===================

使用以下代码加载此辅助函数:

.. literalinclude:: html_helper/001.php

可用函数
===================

以下函数可用:

.. php:function:: img([$src = ''[, $indexPage = false[, $attributes = '']]])

    :param  string|array  $src: 图像源 URI,或属性和值的数组
    :param  bool    $indexPage:  是否将 ``$src`` 视为路由的 URI 字符串
    :param  mixed   $attributes: 其他 HTML 属性
    :returns:   HTML 图像标签
    :rtype: string

    允许你创建 HTML ``<img />`` 标签。第一个参数包含图像源。示例:

    .. literalinclude:: html_helper/002.php

    有一个可选的第二个参数,它是一个 true/false 值,指定 *src* 是否应该添加由 ``$config['indexPage']`` 指定的页面地址。这可能是如果你使用媒体控制器的情况:

    .. literalinclude:: html_helper/003.php

    另外,可以将关联数组作为第一个参数传递,以完全控制所有属性和值。如果没有提供 *alt* 属性,CodeIgniter 将生成一个空字符串。

    示例:

    .. literalinclude:: html_helper/004.php

.. php:function:: img_data([$src = ''[, $indexPage = false[, $attributes = '']]])

    :param string $path: 图像文件路径
    :param string|null $mime: 要使用的 MIME 类型,如果为 null 将猜测
    :returns: base64 编码的二进制图像字符串
    :rtype: string

    使用“数据:”协议从图像生成 src 就绪字符串。示例:

    .. literalinclude:: html_helper/005.php

    有一个可选的第二个参数来指定 MIME 类型,否则该函数将使用你的 MIME 配置进行猜测:

    .. literalinclude:: html_helper/006.php

    注意 ``$path`` 必须存在并且是一个 ``数据:`` 协议支持的可读图像格式。对于非常大的文件不推荐使用此函数,但它提供了一种方便的方法来从你的应用程序中获取图像,这些图像并非 Web 可访问的(例如在 **public/** 中)。

.. php:function:: link_tag([$href = ''[, $rel = 'stylesheet'[, $type = 'text/css'[, $title = ''[, $media = ''[, $indexPage = false[, $hreflang = '']]]]]]])

    :param  string  $href:      链接文件源
    :param  string  $rel:       关系类型
    :param  string  $type:      相关文档的类型
    :param  string  $title:     链接标题
    :param  string  $media:     媒体类型
    :param  bool    $indexPage: 是否将 ``$src`` 视为路由的 URI 字符串
    :param  string  $hreflang:  Hreflang 类型
    :returns:   HTML 链接标签
    :rtype: string

    允许你创建 HTML ``<link />`` 标签。这对于样式表链接很有用,也用于其他链接。参数是 *href*,可选的 *rel*、*type*、*title*、*media* 和 *indexPage*。

    *indexPage* 是一个布尔值,指定 *href* 是否应该添加由 ``$config['indexPage']`` 指定的页面地址。

    示例:

    .. literalinclude:: html_helper/007.php

    更多示例:

    .. literalinclude:: html_helper/008.php

    或者,可以将关联数组传递给 ``link_tag()`` 函数,以完全控制所有属性和值:

    .. literalinclude:: html_helper/009.php

.. php:function:: script_tag([$src = ''[, $indexPage = false]])

    :param  array|string  $src: JavaScript 文件的源名称或 URL,或指定属性的关联数组
    :param  bool          $indexPage: 是否将 ``$src`` 视为路由的 URI 字符串
    :returns:   HTML script 标签
    :rtype: string

    允许你创建 HTML ``<script></script>`` 标签。参数是 *src*,可选的 *indexPage*。

    *indexPage* 是一个布尔值,指定 *src* 是否应该添加由 ``$config['indexPage']`` 指定的页面地址。

    示例:

    .. literalinclude:: html_helper/010.php

    或者,可以将关联数组传递给 ``script_tag()`` 函数,以完全控制所有属性和值:

    .. literalinclude:: html_helper/011.php

.. php:function:: ul($list[, $attributes = ''])

    :param  array   $list: 列表项
    :param  array   $attributes: HTML 属性
    :returns:   HTML 格式的无序列表
    :rtype: string

    允许你从简单或多维数组生成无序 HTML 列表。示例:

    .. literalinclude:: html_helper/012.php

    以上代码将生成:

    .. code-block:: html

        <ul class="boldlist" id="mylist">
            <li>red</li>
            <li>blue</li>
            <li>green</li>
            <li>yellow</li>
        </ul>

    这是一个更复杂的示例,使用多维数组:

    .. literalinclude:: html_helper/013.php

    以上代码将生成:

    .. code-block:: html

        <ul class="boldlist" id="mylist">
            <li>colors
                <ul>
                    <li>red</li>
                    <li>blue</li>
                    <li>green</li>
                </ul>
            </li>
            <li>shapes
                <ul>
                    <li>round</li>
                    <li>square</li>
                    <li>circles
                        <ul>
                            <li>ellipse</li>
                            <li>oval</li>
                            <li>sphere</li>
                        </ul>
                    </li>
                </ul>
            </li>
            <li>moods
                <ul>
                    <li>happy</li>
                    <li>upset
                        <ul>
                            <li>defeated
                                <ul>
                                    <li>dejected</li>
                                    <li>disheartened</li>
                                    <li>depressed</li>
                                </ul>
                            </li>
                            <li>annoyed</li>
                            <li>cross</li>
                            <li>angry</li>
                        </ul>
                    </li>
                </ul>
            </li>
        </ul>

.. php:function:: ol($list, $attributes = '')

    :param  array   $list: 列表项
    :param  array   $attributes: HTML 属性
    :returns:   HTML 格式的有序列表
    :rtype: string

    与 :php:func:`ul()` 相同,只是它生成 ``<ol>`` 标签用于有序列表,而不是 ``<ul>``。

.. php:function:: video($src[, $unsupportedMessage = ''[, $attributes = ''[, $tracks = [][, $indexPage = false]]]])

    :param  mixed   $src:                 源字符串或源数组。参见 :php:func:`source()` 函数
    :param  string  $unsupportedMessage: 如果浏览器不支持媒体标签应显示的消息
    :param  string  $attributes:          HTML 属性
    :param  array   $tracks:              在数组内使用 track 函数。参见 :php:func:`track()` 函数
    :param  bool    $indexPage:
    :returns:                             HTML 格式的视频元素
    :rtype: string

    允许你从简单或源数组生成 HTML 视频元素。示例:

    .. literalinclude:: html_helper/014.php

    以上代码将生成:

    .. code-block:: html

        <video src="test.mp4" controls>
          你的浏览器不支持视频标签。
        </video>

        <video src="http://www.codeigniter.com/test.mp4" controls>
          <track src="subtitles_no.vtt" kind="subtitles" srclang="no" label="Norwegian No" />
          <track src="subtitles_yes.vtt" kind="subtitles" srclang="yes" label="Norwegian Yes" />
          你的浏览器不支持视频标签。
        </video>

        <video class="test" controls>
          <source src="movie.mp4" type="video/mp4" class="test" />
          <source src="movie.ogg" type="video/ogg" />
          <source src="movie.mov" type="video/quicktime" />
          <source src="movie.ogv" type="video/ogv; codecs=dirac, speex" />
          <track src="subtitles_no.vtt" kind="subtitles" srclang="no" label="Norwegian No" />
          <track src="subtitles_yes.vtt" kind="subtitles" srclang="yes" label="Norwegian Yes" />
          你的浏览器不支持视频标签。
        </video>

.. php:function:: audio($src[, $unsupportedMessage = ''[, $attributes = ''[, $tracks = [][, $indexPage = false]]]])

    :param  mixed   $src:                 源字符串或源数组。参见 :php:func:`source()` 函数
    :param  string  $unsupportedMessage: 如果浏览器不支持媒体标签应显示的消息
    :param  string  $attributes:
    :param  array   $tracks:              在数组内使用 track 函数。参见 :php:func:`track()` 函数
    :param  bool    $indexPage:
    :returns:                             HTML 格式的音频元素
    :rtype: string

    与 :php:func:`video()` 相同,只是它生成 ``<audio>`` 标签而不是 ``<video>``。

.. php:function:: source($src = ''[, $type = false[, $attributes = '']])

    :param  string  $src:        媒体资源路径
    :param  bool    $type:       资源的 MIME 类型,可选编解码器参数
    :param  array   $attributes: HTML 属性
    :returns:   HTML 源标签
    :rtype: string

    允许你创建 HTML ``<source />`` 标签。第一个参数包含源源。示例:

    .. literalinclude:: html_helper/015.php

.. php:function:: embed($src = ''[, $type = false[, $attributes = ''[, $indexPage = false]]])

    :param  string  $src:        要嵌入的资源路径
    :param  bool    $type:       MIME 类型
    :param  array   $attributes: HTML 属性
    :param  bool    $indexPage:
    :returns:   HTML 嵌入标签
    :rtype: string

    允许你创建 HTML ``<embed />`` 标签。第一个参数包含嵌入源。示例:

    .. literalinclude:: html_helper/016.php

.. php:function:: object($data = ''[, $type = false[, $attributes = '']])

    :param  string  $data:       资源 URL
    :param  bool    $type:       资源的内容类型
    :param  array   $attributes: HTML 属性
    :param  array   $params:     在数组中使用 param 函数。参见 :php:func:`param()` 函数
    :returns:   HTML 对象标签
    :rtype: string

    允许你创建 HTML ``<object />`` 标签。第一个参数包含对象数据。示例:

    .. literalinclude:: html_helper/017.php

    以上代码将生成:

    .. code-block:: html

        <object data="movie.swf" class="test"></object>

        <object data="movie.swf" class="test">
          <param name="foo" type="ref" value="bar" class="test" />
          <param name="hello" type="ref" value="world" class="test" />
        </object>

.. php:function:: param($name = ''[, $type = false[, $attributes = '']])

    :param  string  $name:       参数名称
    :param  string  $value:      参数值
    :param  array   $attributes: HTML 属性
    :returns:   HTML param 标签
    :rtype: string

    允许你创建 HTML ``<param />`` 标签。第一个参数包含 param 源。示例:

    .. literalinclude:: html_helper/018.php

.. php:function:: track($name = ''[, $type = false[, $attributes = '']])

    :param  string  $name:       参数名称
    :param  string  $value:      参数值
    :param  array   $attributes: HTML 属性
    :returns:   HTML track 标签
    :rtype: string

    生成用于指定定时轨道的 track 元素。轨道以 WebVTT 格式格式化。示例:

    .. literalinclude:: html_helper/019.php

.. php:function:: doctype([$type = 'html5'])

    :param  string  $type: 文档类型名称
    :returns:   HTML DocType 标签
    :rtype: string

    帮助生成文档类型声明或 DTD。默认使用 HTML 5,但有许多可用的文档类型。

    示例:

    .. literalinclude:: html_helper/020.php

    以下是预定义的文档类型选择的列表。这些是可配置的,从 **app/Config/DocTypes.php** 中获取,或者可以在你的 **.env** 配置中重写。

    =============================== =================== ==================================================================================================================================================
    文档类型                        选项                结果
    =============================== =================== ==================================================================================================================================================
    XHTML 1.1                       xhtml11             <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
    XHTML 1.0 严格                  xhtml1-strict       <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    XHTML 1.0 过渡                  xhtml1-trans        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    XHTML 1.0 框架集                xhtml1-frame        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">
    XHTML Basic 1.1                 xhtml-basic11       <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML Basic 1.1//EN" "http://www.w3.org/TR/xhtml-basic/xhtml-basic11.dtd">
    HTML 5                          html5               <!DOCTYPE html>
    HTML 4 严格                     html4-strict        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
    HTML 4 过渡                     html4-trans         <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
    HTML 4 框架集                   html4-frame         <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">
    MathML 1.01                     mathml1             <!DOCTYPE math SYSTEM "http://www.w3.org/Math/DTD/mathml1/mathml.dtd">
    MathML 2.0                      mathml2             <!DOCTYPE math PUBLIC "-//W3C//DTD MathML 2.0//EN" "http://www.w3.org/Math/DTD/mathml2/mathml2.dtd">
    SVG 1.0                         svg10               <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
    SVG 1.1 完整                    svg11               <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    SVG 1.1 基本                    svg11-basic         <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1 Basic//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11-basic.dtd">
    SVG 1.1 Tiny                    svg11-tiny          <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1 Tiny//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11-tiny.dtd">
    XHTML+MathML+SVG (XHTML 主机)   xhtml-math-svg-xh   <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1 plus MathML 2.0 plus SVG 1.1//EN" "http://www.w3.org/2002/04/xhtml-math-svg/xhtml-math-svg.dtd">
    XHTML+MathML+SVG (SVG 主机)     xhtml-math-svg-sh   <!DOCTYPE svg:svg PUBLIC "-//W3C//DTD XHTML 1.1 plus MathML 2.0 plus SVG 1.1//EN" "http://www.w3.org/2002/04/xhtml-math-svg/xhtml-math-svg.dtd">
    XHTML+RDFa 1.0                  xhtml-rdfa-1        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML+RDFa 1.0//EN" "http://www.w3.org/MarkUp/DTD/xhtml-rdfa-1.dtd">
    XHTML+RDFa 1.1                  xhtml-rdfa-2        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML+RDFa 1.1//EN" "http://www.w3.org/MarkUp/DTD/xhtml-rdfa-2.dtd">
    =============================== =================== ==================================================================================================================================================
