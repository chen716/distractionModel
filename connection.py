import psycopg2
from config import config
from sshtunnel import SSHTunnelForwarder
import paramiko
from datetime import datetime, timezone


class connection():
    def __init__(self):
        """ Connect to the PostgreSQL database server """
        self.conn = None
        try:
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')

            mypkey = paramiko.RSAKey.from_private_key_file("/Users/yangchen/Downloads/Qidix.pem")
            tunnel = SSHTunnelForwarder(
                ('ec2-13-57-184-27.us-west-1.compute.amazonaws.com', 22),
                ssh_username='ubuntu',
                ssh_pkey=mypkey,
                remote_bind_address=('localhost', 5432))
            tunnel.start()
            
            self.conn = psycopg2.connect(
                dbname='engagment',
                user='postgres',
                password='chenyang',
                host='127.0.0.1',
                port=tunnel.local_bind_port)
            #conn = psycopg2.connect(**params)
		
            # create a cursor
            self.cur = self.conn.cursor()
            
	    # execute a statement
            print('PostgreSQL database version:')
            #self.cur.execute('SELECT * from sever_student')

            # display the PostgreSQL database server version
            #db_version = cur.fetchone()
            #print(db_version)
       
	    # close the communication with the PostgreSQL
            #cur.close()
    
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
        #finally:
         #   if self.conn is not None:
         #       conn.close()
         #       print('Database connection closed.')





    def getVer(self):
        self.cur.execute('SELECT * from sever_student')
        db_version = self.cur.fetchone()
        print(db_version)





    def sendStudentEngagementInfo(self, studentname = "", engaging = ""):
        dt = datetime.now(timezone.utc)
        self.cur.execute('INSERT into sever_event_table (students_id,time, value) VALUES'+
'((SELECT id from \"sever_student\" ss where ss.name = \''+studentname+'\'),\''+str(dt) +'\','+str(engaging)+' )')
        self.conn.commit()
        
