mysql_check_locks
=================

MySQL Locks and Deadlocks checker

This script will be a part of Nagios(check_mk) monitorring tool for MySQL server.

Now it get SHOW ENGINE INNODB STATUS and parce TRANSACTION part of this status text. 

This is very usfull, because one locking transaction can stop the whole server!
