import argparse
import sys
import MySQLdb as mdb
import re

class Checker:
    """this class used to connect to mysql and check for locks and deadlocks"""
    def __init__(self,dbsettings):
        self.connect(dbsettings)
    def __del__(self):
        self.disconnect()
    def get_whole_status(self):
        self.cursor.execute("SHOW ENGINE INNODB STATUS") 
        innodb_status = self.cursor.fetchone()[2]#3rd column gives us the status of innodb by one big text 
        return innodb_status
    def find_part(self,part_name, status):
        """split raw data to parts with headers and return part by it header"""
        split_by_topics=re.split('(-{3,}\n[ /A-Z]*\n-{3,})',status)
        i=0
        for part in  split_by_topics:
            
            if '------------\n%s\n------------' % part_name in part:
                result = split_by_topics[i+1]
            i=i+1
        return result    
    def check_empty_transaction(self, transaction):
        """3 line transactions is almost sleep transactions"""
        if len(transaction.split('\n'))<=3:
            return False
        else:
            return True
    def check_lock_transaction(self, transaction):
        """if transaction does not lock anything it has "locked 0"""
        if "locked 0" in transaction:
            return False
        else:
            return True
    def active_transactions(self, transactions):
        active_transactions=[]
        for transaction in  transactions:
            if "ACTIVE" in transaction and self.check_empty_transaction(transaction):
                active_transactions.append(transaction)
        return active_transactions
    def split_transactions(self, raw_transactions):
        transactions=re.findall('TRANSACTION(.*?)---', raw_transactions, re.DOTALL)
        return transactions
    def locking_transactions(self, active_transactions):
        locking_transactions=[]
        for transaction in active_transactions:
            if self.check_lock_transaction(transaction):
                locking_transactions.append(transaction)
        return locking_transactions   
    def connect(self, dbsettings):
        try:
            self.db=mdb.connect(**dbsettings)
            self.cursor=self.db.cursor()
        except Exception, e:
            print repr(e)
    def disconnect(self):
        if self.db:
            print "closing connection"
            self.db.close()
class Settings:
    """this class will generate some settings that will be used to check the locks. """
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


if __name__ == "__main__":
    settings=Settings()
    checker = Checker(settings.dbsettings)
    status=checker.get_whole_status()
    raw_transactions=checker.find_part("TRANSACTIONS", status)
    transactions = checker.split_transactions(raw_transactions)
    active=checker.active_transactions(transactions)
    locking=checker.locking_transactions(active)

    for transaction in locking:
        print transaction