******************
使用文件类
******************

CodeIgniter提供了一个文件类,它将提供 `SplFileInfo <http://php.net/manual/en/class.splfileinfo.php>`_ class 
方法和一些额外的便利方法.这个类是 :doc:`uploaded files </libraries/uploaded_files>` 的基类
和 :doc:`images </libraries/images>`.

.. contents:: 目录
    :local:

获取文件类实例
=======================

通过传递构造函数中文件的路径来创建新的文件实例。默认情况下,文件不需要存在。但是您可以传递一个附加参数 "true" ,以检查该文件是否存在,并在不存在的情况下抛出 ``FileNotFoundException()`` 的异常提示.

::

    $file = new \CodeIgniter\Files\File($path);

利用Spl
=======================

一旦你有一个实例,你就可以完成 SplFileInfo 类的全部功能,包括::

    echo $file->getBasename();  // 获取文件的基本名称
   
    echo $file->getMTime();     // 获取上次修改的时间

    echo $file->getRealpath();  // 获取真正的实际路径

    
    echo $file->getPerms();     // 获取文件权限

    
    if ($file->isWritable())    // 向CSV中写入几行数据.
    {
        $csv = $file->openFile('w');

        foreach ($rows as $row)
        {
            $csv->fputcsv($row);
        }
    }

新功能
============

除了 SplFileInfo 类中的所有方法之外,还有一些新的方法.

**getRandomName()**

您可以生成一个加密安全的随机文件名,其中包含当前时间戳, ``getRandomName()``
方法在移动文件时重命名文件很有用::

	$newName = $file->getRandomName();  // 例如: 1465965676_385e33f741.jpg

**getSize()**

返回上传文件的大小(以字节为单位).可以将 'kb' 或 'mb' 作为第一个参数传入方法,
将分别返回千字节和兆字节的结果::

	$bytes     = $file->getSize();      // 256901
    
	$kilobytes = $file->getSize('kb');  // 250.880

	$megabytes = $file->getSize('mb');  // 0.245

**getMimeType()**

尽可能在确定文件安全的前提下,使用该方法获取文件的类型::

	$type = $file->getMimeType();

	echo $type; // image/png

**guessExtension()**

使用 ``getMimeType()`` 方法确定文件扩展名时.如果文件类型未知,将返回 null . ``guessExtension()`` 比使用 ``getMimeType()`` 来获取扩展名功能强一点.可以配置 **application/Config/Mimes.php** 中的配置文件来获取文件扩展名::

	$ext = $file->guessExtension();     // 例如:返回图片类型 'jpg' (没有句点'.')

移动文件
------------

每个文件可以使用 ``move()`` 方法移动到新的位置.指定文件的目录作作为
该方法的第一个参数::

	$file->move(WRITEPATH.'uploads');

默认情况下,使用原始文件名.您可以通过第二个参数重命名你要移动的文件::

	$newName = $file->getRandomName();
    
	$file->move(WRITEPATH.'uploads', $newName);
