#############
HTML 辅助函数
#############

HTML 辅助函数文件包含用于处理 HTML 的辅助函数。

.. contents::
    :local:
    :depth: 2

配置
=============

自 ``v4.3.0`` 起，``html_helper`` 函数中的空 HTML 元素（例如 ``<img>``）默认更改为 HTML5 兼容，如果需要兼容 XHTML，必须将 **app/Config/DocTypes.php** 中的 ``$html5`` 属性设置为 ``false``。

加载此辅助函数
===================

使用以下代码加载此辅助函数：

.. literalinclude:: html_helper/001.php

可用函数
===================

提供以下函数：

.. php:function:: img([$src = ''[, $indexPage = false[, $attributes = '']]])

    :param  string|array  $src:  图片源 URI，或属性和值的数组
    :param  bool    $indexPage:  是否应该在源路径中添加 ``Config\App::$indexPage``
    :param  mixed   $attributes: 附加 HTML 属性
    :returns:   HTML 图像元素
    :rtype: string

    允许你创建 HTML ``<img>`` 元素。第一个参数包含图片源。例如：

    .. literalinclude:: html_helper/002.php

    有一个可选的第二参数，一个 true/false 值，指定是否应该在创建的地址中添加 ``Config\App::$indexPage``。通常在使用媒体控制器时会用到：

    .. literalinclude:: html_helper/003.php

    此外，可以将关联数组作为第一个参数传递，以完全控制所有属性和值。如果没有提供 *alt* 属性，CodeIgniter 将生成一个空的 alt 属性值。

    例如：

    .. literalinclude:: html_helper/004.php

.. php:function:: img_data($path[, $mime = null])

    :param string $path: 图片文件路径
    :param string|null $mime: 使用的 MIME 类型，或 null 来猜测
    :returns: base64 编码的二进制图片字符串
    :rtype: string

    使用 "data:" 协议从图片生成可用于 src 的字符串。例如：

    .. literalinclude:: html_helper/005.php

    有一个可选的第二参数来指定 MIME 类型，否则函数将使用你的 Mimes 配置来猜测：

    .. literalinclude:: html_helper/006.php

    请注意，``$path`` 必须存在并且是 ``data:`` 协议支持的可读图片格式。
    不建议对非常大的文件使用此函数，但它提供了一种便捷的方式来提供应用程序中无法通过 Web 访问的图片（例如，不在 **public/** 目录中的文件）。

.. php:function:: link_tag([$href = ''[, $rel = 'stylesheet'[, $type = 'text/css'[, $title = ''[, $media = ''[, $indexPage = false[, $hreflang = '']]]]]]])

    :param  string  $href:      链接文件的源
    :param  string  $rel:       关系类型
    :param  string  $type:      相关文档的类型
    :param  string  $title:     链接标题
    :param  string  $media:     媒体类型
    :param  bool    $indexPage: 是否应该将 indexPage 添加到链接路径
    :param  string  $hreflang:  Hreflang 类型
    :returns:   HTML link 元素
    :rtype: string

    允许你创建 HTML ``<link>`` 元素。这对于样式表链接以及其他链接很有用。参数是 *href*，以及可选的 *rel*、*type*、*title*、*media*、*indexPage* 和 *hreflang*。

    *indexPage* 是一个布尔值，指定是否应该在 *href* 创建的地址中添加由 ``Config\App::$indexPage`` 指定的页面。

    例如：

    .. literalinclude:: html_helper/007.php

    更多示例：

    .. literalinclude:: html_helper/008.php

    或者，可以将关联数组传递给 ``link_tag()`` 函数，以完全控制所有属性和值：

    .. literalinclude:: html_helper/009.php

.. php:function:: script_tag([$src = ''[, $indexPage = false]])

    :param  array|string  $src: JavaScript 文件的源名称或 URL，或指定属性的关联数组
    :param  bool          $indexPage: 是否将 ``$src`` 视为路由的 URI 字符串
    :returns:   HTML script 元素
    :rtype: string

    允许你创建 HTML ``<script>`` 元素。参数是 *src* 和可选的 *indexPage*。

    *indexPage* 是一个布尔值，指定是否应该在 *src* 创建的地址中添加由 ``Config\App::$indexPage`` 指定的页面。

    例如：

    .. literalinclude:: html_helper/010.php

    或者，可以将关联数组传递给 ``script_tag()`` 函数，以完全控制所有属性和值：

    .. literalinclude:: html_helper/011.php

.. php:function:: ul($list[, $attributes = ''])

    :param  array   $list: 列表项
    :param  array   $attributes: HTML 属性
    :returns:   HTML 无序列表元素
    :rtype: string

    允许你从简单或多维数组生成无序 HTML 列表。例如：

    .. literalinclude:: html_helper/012.php

    上面的代码将生成：

    .. code-block:: html

        <ul class="boldlist" id="mylist">
            <li>red</li>
            <li>blue</li>
            <li>green</li>
            <li>yellow</li>
        </ul>

    这里是一个更复杂的示例，使用多维数组：

    .. literalinclude:: html_helper/013.php

    上面的代码将生成：

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
    :returns:   HTML 有序列表元素
    :rtype: string

    与 :php:func:`ul()` 相同，只是它生成 ``<ol>`` 元素用于有序列表而不是 ``<ul>``。

.. php:function:: video($src[, $unsupportedMessage = ''[, $attributes = ''[, $tracks = [][, $indexPage = false]]]])

    :param  mixed   $src:                源字符串或源数组。参见 :php:func:`source()` 函数
    :param  string  $unsupportedMessage: 如果浏览器不支持 video 元素时显示的消息
    :param  string  $attributes:         HTML 属性
    :param  array   $tracks:             在数组中使用 track 函数。参见 :php:func:`track()` 函数
    :param  bool    $indexPage:          是否应该将 indexPage 添加到视频源路径
    :returns:                            HTML video 元素
    :rtype: string

    允许你从源字符串或源数组生成 HTML video 元素。例如：

    .. literalinclude:: html_helper/014.php

    上面的代码将生成：

    .. code-block:: html

        <video src="test.mp4" controls>
          Your browser does not support the video tag.
        </video>

        <video src="http://www.codeigniter.com/test.mp4" controls>
          <track src="subtitles_no.vtt" kind="subtitles" srclang="no" label="Norwegian No" />
          <track src="subtitles_yes.vtt" kind="subtitles" srclang="yes" label="Norwegian Yes" />
          Your browser does not support the video tag.
        </video>

        <video class="test" controls>
          <source src="movie.mp4" type="video/mp4" class="test" />
          <source src="movie.ogg" type="video/ogg" />
          <source src="movie.mov" type="video/quicktime" />
          <source src="movie.ogv" type="video/ogv; codecs=dirac, speex" />
          <track src="subtitles_no.vtt" kind="subtitles" srclang="no" label="Norwegian No" />
          <track src="subtitles_yes.vtt" kind="subtitles" srclang="yes" label="Norwegian Yes" />
          Your browser does not support the video tag.
        </video>

.. php:function:: audio($src[, $unsupportedMessage = ''[, $attributes = ''[, $tracks = [][, $indexPage = false]]]])

    :param  mixed   $src:                源字符串或源数组。参见 :php:func:`source()` 函数
    :param  string  $unsupportedMessage: 如果浏览器不支持 audio 元素时显示的消息
    :param  string  $attributes:
    :param  array   $tracks:             在数组中使用 track 函数。参见 :php:func:`track()` 函数
    :param  bool    $indexPage:          是否应该将 indexPage 添加到音频源路径
    :returns:                            HTML audio 元素
    :rtype: string

    与 :php:func:`video()` 相同，只是它生成 ``<audio>`` 元素而不是 ``<video>``。

.. php:function:: source($src, $type = 'unknown', $attributes = '', $indexPage = false)

    :param  string  $src:        媒体资源的路径
    :param  bool    $type:       资源的 MIME 类型，带有可选的解码器参数
    :param  array   $attributes: HTML 属性
    :returns:   HTML source 元素
    :rtype: string

    允许你创建 HTML ``<source>`` 元素。第一个参数包含资源的路径。例如：

    .. literalinclude:: html_helper/015.php

.. php:function:: embed($src = ''[, $type = false[, $attributes = ''[, $indexPage = false]]])

    :param  string  $src:        要嵌入的资源路径
    :param  bool    $type:       MIME 类型
    :param  array   $attributes: HTML 属性
    :param  bool    $indexPage:  是否应该将 indexPage 添加到源路径
    :returns:   HTML embed 元素
    :rtype: string

    允许你创建 HTML ``<embed>`` 元素。第一个参数包含嵌入源。例如：

    .. literalinclude:: html_helper/016.php

.. php:function:: object($data[, $type = 'unknown'[, $attributes = ''[, $params = [][, $indexPage = false]]]])

    :param  string  $data:       资源 URL
    :param  bool    $type:       资源的内容类型
    :param  array   $attributes: HTML 属性
    :param  bool    $indexPage:  是否应该将 indexPage 添加到资源 URL
    :param  array   $params:     在数组中使用 param 函数。参见 :php:func:`param()` 函数
    :returns:   HTML object 元素
    :rtype: string

    允许你创建 HTML ``<object>`` 元素。第一个参数包含对象数据。例如：

    .. literalinclude:: html_helper/017.php

    上面的代码将生成：

    .. code-block:: html

        <object data="movie.swf" class="test"></object>

        <object data="movie.swf" class="test">
          <param name="foo" type="ref" value="bar" class="test" />
          <param name="hello" type="ref" value="world" class="test" />
        </object>

.. php:function:: param($name, $value[, $type = 'ref'[, $attributes = '']])

    :param  string  $name:       参数的名称
    :param  string  $value:      参数的值
    :param  array   $attributes: HTML 属性
    :returns:   HTML param 元素
    :rtype: string

    允许你创建 HTML ``<param>`` 元素。第一个参数包含参数源。例如：

    .. literalinclude:: html_helper/018.php

.. php:function:: track($src, $kind, $srcLanguage, $label)

    :param  string $src:         轨道的路径（.vtt 文件）
    :param  string $kind:        定时轨道的类型
    :param  string $srcLanguage: 定时轨道的语言
    :param  string $label:       定时轨道的用户可读标题
    :returns:   HTML track 元素
    :rtype: string

    生成 track 元素以指定定时轨道。轨道以 WebVTT 格式格式化。例如：

    .. literalinclude:: html_helper/019.php

.. php:function:: doctype([$type = 'html5'])

    :param  string  $type: 文档类型名称
    :returns:   HTML DocType 声明
    :rtype: string

    帮助你生成文档类型声明（DTD）。默认使用 HTML 5，但许多文档类型都可用。

    例如：

    .. literalinclude:: html_helper/020.php

    以下是预定义文档类型的列表。这些从 **app/Config/DocTypes.php** 中提取，或者可以在你的 **.env** 配置中覆盖。

    =============================== =================== ==================================================================================================================================================
    文档类型                        $type 参数          返回值
    =============================== =================== ==================================================================================================================================================
    XHTML 1.1                       xhtml11             <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
    XHTML 1.0 Strict                xhtml1-strict       <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    XHTML 1.0 Transitional          xhtml1-trans        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    XHTML 1.0 Frameset              xhtml1-frame        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">
    XHTML Basic 1.1                 xhtml-basic11       <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML Basic 1.1//EN" "http://www.w3.org/TR/xhtml-basic/xhtml-basic11.dtd">
    HTML 5                          html5               <!DOCTYPE html>
    HTML 4 Strict                   html4-strict        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
    HTML 4 Transitional             html4-trans         <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
    HTML 4 Frameset                 html4-frame         <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">
    MathML 1.01                     mathml1             <!DOCTYPE math SYSTEM "http://www.w3.org/Math/DTD/mathml1/mathml.dtd">
    MathML 2.0                      mathml2             <!DOCTYPE math PUBLIC "-//W3C//DTD MathML 2.0//EN" "http://www.w3.org/Math/DTD/mathml2/mathml2.dtd">
    SVG 1.0                         svg10               <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
    SVG 1.1 Full                    svg11               <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
    SVG 1.1 Basic                   svg11-basic         <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1 Basic//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11-basic.dtd">
    SVG 1.1 Tiny                    svg11-tiny          <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1 Tiny//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11-tiny.dtd">
    XHTML+MathML+SVG (XHTML host)   xhtml-math-svg-xh   <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1 plus MathML 2.0 plus SVG 1.1//EN" "http://www.w3.org/2002/04/xhtml-math-svg/xhtml-math-svg.dtd">
    XHTML+MathML+SVG (SVG host)     xhtml-math-svg-sh   <!DOCTYPE svg:svg PUBLIC "-//W3C//DTD XHTML 1.1 plus MathML 2.0 plus SVG 1.1//EN" "http://www.w3.org/2002/04/xhtml-math-svg/xhtml-math-svg.dtd">
    XHTML+RDFa 1.0                  xhtml-rdfa-1        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML+RDFa 1.0//EN" "http://www.w3.org/MarkUp/DTD/xhtml-rdfa-1.dtd">
    XHTML+RDFa 1.1                  xhtml-rdfa-2        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML+RDFa 1.1//EN" "http://www.w3.org/MarkUp/DTD/xhtml-rdfa-2.dtd">
    =============================== =================== ==================================================================================================================================================
