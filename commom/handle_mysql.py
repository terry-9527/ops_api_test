import pymysql
from sshtunnel import SSHTunnelForwarder

from commom.read_data import readData


class MysqlDb:

    def __init__(self):
        self.conf = readData()
        # 获取config.ini文件中数据库相关配置
        self._host = self.conf.read_config("publicCloud", "host")
        self._port = self.conf.read_config("publicCloud", "ssh_port")
        self._user = self.conf.read_config("publicCloud", "ssh_user")
        self._password = self.conf.read_config("publicCloud", "ssh_pwd")
        self._dbuser = self.conf.read_config("publicCloud", "dbuser")
        self._dbpwd = self.conf.read_config("publicCloud", "dbpwd")
        self._dbname = self.conf.read_config("publicCloud", "dbname")
        self.sshtunnel = self.creat_sshtunnel()
        self.conn = self.login_database()
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 创建SSH tunnel通道
    def creat_sshtunnel(self):
        sshtunnel = SSHTunnelForwarder(
            ssh_address_or_host=self._host,  # 跳板机B地址
            ssh_port=self._port,  # 跳板机B端口
            ssh_username=self._user,  # 跳板机B账号
            ssh_password=self._password,  # 跳板机B密码
            local_bind_address=('127.0.0.1', 22),  # 这里必须填127.0.0.1
            remote_bind_address=('127.0.0.1', 3306)  # 目标机器A地址，端口
        )
        # print("sshtunnel 通道服务创建成功")
        return sshtunnel

    # 连接数据库
    def connect_database(self):
        conn = pymysql.connect(
            host='127.0.0.1',  # 这里必须填127.0.0.1
            port=22,  # 本地映射端口
            user=self._dbuser,  # 目标机器A账号
            password=self._dbpwd,  # 目标机器A密码
            db=self._dbname  # 目标机器A要连的库
        )
        return conn

    def query(self, sql, state="one", size=None):
        """
        默认取所有行行数据
        :param sql: 执行的sql语句
        :param state: 可取值：one,many,all
        :return: 结果返回字典列表
        """
        self.cursor.execute(sql)
        if state == "all":
            data = self.cursor.fetchall()
        elif state == "many":
            data = self.cursor.fetchmany(size)
        else:
            data = self.cursor.fetchone()
        return data

    def get_count(self, sql):
        count = self.cursor.execute(sql)
        return count

    def execute(self, sql):
        """
        更新、删除、新增
        :param sql:
        :return:
        """
        try:
            # 使用execute执行sql
            rows = self.cursor.execute(sql)
            # 提交事务
            self.conn.commit()
            return rows
        except Exception as e:
            print("数据库操作异常{0}".format(e))
            # 出现异常，进行回滚操作
            self.conn.rollback()
            raise e

    def login_database(self):
        # 创建ssh tunnel服务通道
        self.creat_sshtunnel()
        # 开启ssh tunnel服务通道
        self.sshtunnel.start()
        # 连接数据库
        conn = self.connect_database()
        return conn

    def init_database(self, filename):
        # 获取数据库初始化sql语句
        sqls = readData().read_sqls(filename)
        for sql in sqls:
            self.cursor.execute(sql)
        self.conn.commit()

    def close_conn(self):
        self.cursor.close()
        self.conn.close()
        self.sshtunnel.stop()


if __name__ == "__main__":
    db = MysqlDb()
    count = db.query("SELECT name FROM t_client", state="many", size=3)
    db.close_conn()
    print(count)
