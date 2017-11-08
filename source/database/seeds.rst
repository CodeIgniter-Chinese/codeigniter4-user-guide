################
数据填充
################

数据填充是一种简单的将数据添加到数据库的方式。这在开发的过程中特别有用，你只需要准备开发中所需要的示例数据填充到数据库中，而且不仅如此，这些数据可以包括你不想要包括的迁移的静态数据，例如国家/地区，地理编码表，事件或设置信息等等。

数据填充是必须有 **run()** 方法的简单类，并继承于 **CodeIgniter\Database\Seeder** 。在 **run()** 中，该类可以创建你所需要的任何类型的数据。该类可以创建需要的任何形式的数据。它可以分别通过建立 $this->db 和 $this->forge 访问数据库连接。填充文件必须存储在 **application/Database/Seeds** 目录中。文件名和类名必须保持一致。
::

	// application/Database/Seeds/SimpleSeeder.php
	class SimpleSeeder extends \CodeIgniter\Database\Seeder
	{
		public function run()
		{
			$data = [
				'username' => 'darth',
				'email' => 'darth@theempire.com'
			];

			// Simple Queries
			$this->db->query("INSERT INTO users (username, email) VALUES(:username, :email)",
				$data
			);

			// Using Query Builder
			$this->db->table('users')->insert($data);
		}
	}

嵌套数据填充
===============

你可以使用 **call()** 方法来运行其他的 seed 类。这允许你更容易使用 seeder，而且同时也将任务分发到各个 seeder 文件当中::

	class TestSeeder extends \CodeIgniter\Database\Seeder
	{
		public function run()
		{
			$this->call('UserSeeder');
			$this->call('CountrySeeder');
			$this->call('JobSeeder');
		}
	}

你也可以在 **call()** 方法中使用完全合格的类名，使你的 seeder 在任何地方都可以更好的加载。这对于更多模块化代码库来说非常方便::

	public function run()
	{
		$this->call('UserSeeder');
		$this->call('My\Database\Seeds\CountrySeeder');
	}

使用 Seeders
=============

你可以通过数据库配置类获取主 seeder

	$seeder = \Config\Database::seeder();
	$seeder->call('TestSeeder');

命令行填充数
--------------------

如果不想创建专用控制器，也可以从命令行填充数据，作为 Migrations CLI 工具的一部分::

	> php index.php migrations seed TestSeeder
