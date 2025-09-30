import mysql.connector
from mysql.connector import pooling

# 数据库配置
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "xmueducn",
    "database": "algorithm_testing_system"
}

# 数据库连接池
connection_pool = pooling.MySQLConnectionPool(pool_name="pool", pool_size=10, **db_config)

# 获取连接
def get_connection():
    return connection_pool.get_connection()

# 数据库初始化
def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    # 创建表的 SQL 语句
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS testers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            contact_info VARCHAR(255) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hardware (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            details TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS software (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            version VARCHAR(50) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS models (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            test_requirements TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            data_format VARCHAR(50) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            model VARCHAR(255) NOT NULL,
            is_occupied BOOLEAN DEFAULT FALSE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            tester_id INT NOT NULL,
            model_id INT NOT NULL,
            dataset_id INT NOT NULL,
            server_id INT NOT NULL,
            test_status ENUM('Pending', 'Running', 'Completed', 'Stopped') DEFAULT 'Pending',
            test_results TEXT,
            FOREIGN KEY (tester_id) REFERENCES testers(id),
            FOREIGN KEY (model_id) REFERENCES models(id),
            FOREIGN KEY (dataset_id) REFERENCES datasets(id),
            FOREIGN KEY (server_id) REFERENCES servers(id)
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()
    print("数据库初始化完成！")
