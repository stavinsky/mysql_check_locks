import argparse
import sys
class Checker:
    """this class used to connect to mysql and check for locks and deadlocks"""
    def __init__(self):
        pass
    def init(self):
        pass
    def check_locks(self):
        pass
    
    def check_dead_lock(self):
        pass

class Settings:
    """this class will generate some settings that will be used to check locks. """
    def __init__(self):
        self.get_args()
        self.make_mysql_connection_string()
    
    def get_args(self):
        self.parser=argparse.ArgumentParser()
        self.parser.add_argument("dbhost", help="Your database server")
        self.parser.add_argument("--port", help="Port of your database server", type=int)
        self.parser.add_argument("--defaults_file", help="This is the name and path to mysql defaults file, usually there is ~/.my.cnf ")
        self.parser.add_argument("--login", help="Login to server")
        self.parser.add_argument("--password", help="Password to server. We recommend to use default file.")
        self.args=self.parser.parse_args()

    def make_mysql_connection_string(self):
        self.dbsettings = {}
        if self.args.defaults_file:
            self.dbsettings['read_default_file'] = self.args.defaults_file
        elif self.args.login and self.args.password:
            self.dbsettings['user'] = self.args.login
            self.dbsettings['passwd'] = self.args.password
        else: 
            print "You have to define the pair of login and password or use the defaults file"
            sys.exit(0)
        if self.args.port:
            self.dbsettings['port'] = self.args.port
        self.dbsettings['host'] = self.args.dbhost
        print self.dbsettings

settings=Settings()
settings.dbsettings
  