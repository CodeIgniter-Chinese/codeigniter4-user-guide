###############
HTML 辅助函数
###############

HTML 辅助函数包含的函数辅助 HTML 运行。

.. contents::
    :local:

.. raw:: html

    <div class="custom-index container"></div>

加载 HTML 辅助函数
===================

HTML 辅助函数使用下面的代码加载::

    helper('html');

通用函数
===================

下面的函数是通用的:

.. php:function:: img([$src = ''[, $indexPage = false[, $attributes = '']]])

    :param  mixed  $src:        Image 原始码数据
    :param  bool    $indexPage:  是否像路由的 URI 字符串处理 $src 
    :param  mixed   $attributes: HTML 属性
    :returns:   HTML image tag
    :rtype: string

    让你创建 HTML <img /> tags. 第一个参数包含 image 原始码。事例::

        echo img('images/picture.jpg');
        // <img src="http://site.com/images/picture.jpg" />

   有一个可选择的第二参数是特定的 true/false 值并规定如果 *src* 将经由 ``$config['indexPage']`` 被添加到地址并创建有明确说明的页面。推测起来，假如你正在使用一个 media 控制器那将是自以为是的::

        echo img('images/picture.jpg', true);
        // <img src="http://site.com/index.php/images/picture.jpg" alt="" />

此外，组合数组能被作为第一参数传达，为了完成控制额外的所有属性和值。 如果不提供 *alt* 属性，CodeIgniter 将产生空字符串。

    例如::

        $imageProperties = [
            'src'    => 'images/picture.jpg',
            'alt'    => 'Me, demonstrating how to eat 4 slices of pizza at one time',
            'class'  => 'post_images',
            'width'  => '200',
            'height' => '200',
            'title'  => 'That was quite a night',
            'rel'    => 'lightbox'
        ];

        img($imageProperties);
        // <img src="http://site.com/index.php/images/picture.jpg" alt="Me, demonstrating how to eat 4 slices of pizza at one time" class="post_images" width="200" height="200" title="That was quite a night" rel="lightbox" />

.. php:function:: link_tag([$href = ''[, $rel = 'stylesheet'[, $type = 'text/css'[, $title = ''[, $media = ''[, $indexPage = false]]]]]])

    :param  string  $href:      链接文件的原始码
    :param  string  $rel:       关系类型
    :param  string  $type:      关系文件夹的类型
    :param  string  $title:     链接主题
    :param  string  $media:     媒体类型
    :param  bool    $indexPage: 是否像路由的 URI 字符串处理 $src
    :returns:   HTML link tag
    :rtype: string

    让你创建 HTML <link /> tags. 这对样式表链接是有用的,和其他链接一样。参数是 *href* ，带着可选择的 *rel*,
    *type*, *title*, *media* 和 *indexPage*.

    *indexPage* 是 boolean 值并规定如果 *href* 将经由 ``$config['indexPage']`` 被添加到地址并创建有明确说明的页面。

    例如::

        echo link_tag('css/mystyles.css');
        // <link href="http://site.com/css/mystyles.css" rel="stylesheet" type="text/css" />

    更多示例::

        echo link_tag('favicon.ico', 'shortcut icon', 'image/ico');
        // <link href="http://site.com/favicon.ico" rel="shortcut icon" type="image/ico" />

        echo link_tag('feed', 'alternate', 'application/rss+xml', 'My RSS Feed');
        // <link href="http://site.com/feed" rel="alternate" type="application/rss+xml" title="My RSS Feed" />

    间隔地，为了完全控制额外的所有属性和值组合数组能被传达到 ``link_tag()`` 函数::

        $link = [
            'href'  => 'css/printer.css',
            'rel'   => 'stylesheet',
            'type'  => 'text/css',
            'media' => 'print'
        ];

        echo link_tag($link);
        // <link href="http://site.com/css/printer.css" rel="stylesheet" type="text/css" media="print" />

.. php:function:: script_tag([$src = ''[, $indexPage = false]])

    :param  mixed  $src: JavaScript 文件的原始码名称
    :param  bool    $indexPage: 是否像路由的 URI 字符串处理 $src 
    :returns:   HTML script tag
    :rtype: string

    让你创建 HTML <script></script> tags. 参数是 *src*, 与可选的 *indexPage* 一起.

	*indexPage* 是 boolean 值并规定如果 *src* 将经由 ``$config['indexPage']`` 被添加到地址并创建有明确说明的页面。

    例如::

        echo script_tag('js/mystyles.js');
        // <script src="http://site.com/js/mystyles.js" type="text/javascript"></script>

    间隔地，为了完全控制额外的所有属性和值组合数组能被通过 ``script_tag()`` 函数::

        $script = ['src'  => 'js/printer.js'];

        echo script_tag($script);
        // <script src="http://site.com/js/printer.js" type="text/javascript"></script>

.. php:function:: ul($list[, $attributes = ''])

    :param  array   $list: 目录登录
    :param  array   $attributes: HTML 属性
    :returns:   HTML-formatted 无序目录
    :rtype: string

   容许你从简单或者多倍空间的数组产生无序 HTML 目录。事例:::

        $list = [
            'red',
            'blue',
            'green',
            'yellow'
        ];

        $attributes = [
            'class' => 'boldlist',
            'id'    => 'mylist'
        ];

        echo ul($list, $attributes);

    上文的代码将产生下文这样地 HTML 代码:

    .. code-block:: html

        <ul class="boldlist" id="mylist">
            <li>red</li>
            <li>blue</li>
            <li>green</li>
            <li>yellow</li>
        </ul>

    下面是更复杂的事例，使用多维空间的数组::

        $attributes = [
            'class' => 'boldlist',
            'id'    => 'mylist'
        ];

        $list = [
            'colors' => [
                'red',
                'blue',
                'green'
            ],
            'shapes' => [
                'round',
                'square',
                'circles' => [
                    'ellipse',
                    'oval',
                    'sphere'
                ]
            ],
            'moods'  => [
                'happy',
                'upset'   => [
                    'defeated' => [
                        'dejected',
                        'disheartened',
                        'depressed'
                    ],
                    'annoyed',
                    'cross',
                    'angry'
                ]
            ]
        ];

        echo ul($list, $attributes);

    上文的代码将产生这样的 HTML 前端代码:

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
                    <li>suare</li>
                    <li>circles
                        <ul>
                            <li>elipse</li>
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

    :param  array   $list: 目录登录
    :param  array   $attributes: HTML 属性
    :returns:   HTML-formatted 有序目录
    :rtype: string

    完全相似于 :php:func:`ul()` ,为了代替有序目录 <ul> 它仅产生 <ol> tag.
    

.. php:function:: video($src[, $unsupportedMessage = ''[, $attributes = ''[, $tracks = [][, $indexPage = false]]]])

    :param  mixed   $src:                任一原始码字符串或者原始码的数组. 参看 :php:func:`source()` 函数
    :param  string  $unsupportedMessage: 如果 media tag 不支持由浏览器提供的消息会显示
    :param  string  $attributes:         HTML 属性
    :param  array   $tracks:            在数组里使用追踪函数。参看 :php:func:`track()` 函数
    :param  bool    $indexPage:
    :returns:                            HTML-formatted 影像元素
    :rtype: string

    容许你从简单的或者原始码数组产生 HTML 影像元素。事例::

        $tracks =
        [
            track('subtitles_no.vtt', 'subtitles', 'no', 'Norwegian No'),
            track('subtitles_yes.vtt', 'subtitles', 'yes', 'Norwegian Yes')
        ];

        echo video('test.mp4', 'Your browser does not support the video tag.', 'controls');

        echo video
        (
            'http://www.codeigniter.com/test.mp4',
            'Your browser does not support the video tag.',
            'controls',
            $tracks
        );

        echo video
        (
            [
              source('movie.mp4', 'video/mp4', 'class="test"'),
              source('movie.ogg', 'video/ogg'),
              source('movie.mov', 'video/quicktime'),
              source('movie.ogv', 'video/ogv; codecs=dirac, speex')
            ],
            'Your browser does not support the video tag.',
            'class="test" controls',
            $tracks
         );

    上文的编码将产生这样地 HTML 前端代码:

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

    :param  mixed   $src:                任一原始码字符串或者原始码数组。参看 :php:func:`source()` 函数
    :param  string  $unsupportedMessage: 如果 media tag 不支持由浏览器提供的消息会显示
    :param  string  $attributes:
    :param  array   $tracks:            在数组里用追踪函数. 参看 :php:func:`track()` 函数
    :param  bool    $indexPage:
    :returns:                            HTML-formatted 音频元素
    :rtype: string

    完全相似于 :php:func:`video()`, 它仅仅产生 <audio> tag 代替 <video>.
    

.. php:function:: source($src = ''[, $type = false[, $attributes = '']])

    :param  string  $src:        media source的路径
    :param  bool    $type:      以可选择的编码参数的资源 MIME（多用途的网络邮件扩充协议）类型
    :param  array   $attributes: HTML 属性
    :returns:   HTML source tag
    :rtype: string

   让你创建 HTML <source /> tags. 第一个参数包含起源 source. 例如::

        echo source('movie.mp4', 'video/mp4', 'class="test"');
        // <source src="movie.mp4" type="video/mp4" class="test" />

.. php:function:: embed($src = ''[, $type = false[, $attributes = ''[, $indexPage = false]]])

    :param  string  $src:        资源的路径 embed
    :param  bool    $type:      MIME（多用途的网络邮件扩充协议）类型
    :param  array   $attributes: HTML 属性
    :param  bool    $indexPage:
    :returns:   HTML embed tag
    :rtype: string

   让你创建 HTML <embed /> tags.第一参数包含 embed source. 例如::

        echo embed('movie.mov', 'video/quicktime', 'class="test"');
        // <embed src="movie.mov" type="video/quicktime" class="test"/>

.. php:function:: object($data = ''[, $type = false[, $attributes = '']])

    :param  string  $data:       资源 URL
    :param  bool    $type:       资源的内容类型
    :param  array   $attributes: HTML 属性
    :param  array   $params:     在数组里使用 param 函数。参看 :php:func:`param()` 函数
    :returns:   HTML object tag
    :rtype: string

    让你创建 HTML <object /> tags. 第一参数包含 object data. 事例::

        echo object('movie.swf', 'application/x-shockwave-flash', 'class="test"');

        echo object
        (
            'movie.swf',
            'application/x-shockwave-flash',
            'class="test"',
            [
                param('foo', 'bar', 'ref', 'class="test"'),
                param('hello', 'world', 'ref', 'class="test"')
            ]
        );

    上文编码将产生这样的 HTML 前端代码:

    .. code-block:: html

        <object data="movie.swf" class="test"></object>

        <object data="movie.swf" class="test">
          <param name="foo" type="ref" value="bar" class="test" />
          <param name="hello" type="ref" value="world" class="test" />
        </object>

.. php:function:: param($name = ''[, $type = false[, $attributes = '']])

    :param  string  $name:       参数的名字
    :param  string  $value:      参数的值
    :param  array   $attributes: HTML 属性
    :returns:   HTML param tag
    :rtype: string

    让你创建 HTML <param /> tags. 第一个参数包含 param source. 事例::

        echo param('movie.mov', 'video/quicktime', 'class="test"');
        // <param src="movie.mov" type="video/quicktime" class="test"/>

.. php:function:: track($name = ''[, $type = false[, $attributes = '']])

    :param  string  $name:       参数的名称
    :param  string  $value:      参数的值
    :param  array   $attributes: HTML 属性
    :returns:   HTML track tag
    :rtype: string

    产生一个跟踪元素去具体指定时间的轨迹。在 WebVVT 格式里轨迹已被格式化。事例::

        echo track('subtitles_no.vtt', 'subtitles', 'no', 'Norwegian No');
        // <track src="subtitles_no.vtt" kind="subtitles" srclang="no" label="Norwegian No" />

.. php:function:: doctype([$type = 'html5'])

    :param  string  $type: Doctype 名字
    :returns:   HTML DocType tag
    :rtype: string

    帮助你产生 document type 声明, 而 DTD's. HTML 5 是默认使用的，但是许多 doctypes 是通用的。
    
    事例::

        echo doctype();
        // <!DOCTYPE html>

        echo doctype('html4-trans');
        // <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

    接下来的是重定义 doctype 选择的目录。
    这些是可设置的， 被从 `application/Config/DocTypes.php` 出栈,或者在你的 `.env` 结构里它们能被加载。

    =============================== =================== ==================================================================================================================================================
    文档类型                       	 选项                 结果
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
