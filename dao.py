"""import psycopg2 as pg


conn = pg.connect(host="ec2-13-57-184-27.us-west-1.compute.amazonaws.com", database = "engagment", user="postgres", password="chenyang")

cur = conn.cursor()
cur.execute("SELECT version()")

print(cur.fetchone())


"""

import psycopg2
from sshtunnel import SSHTunnelForwarder

try:

    with SSHTunnelForwarder(
         ('ec2-13-57-184-27.us-west-1.compute.amazonaws.com', 22),
         ssh_private_key="~/Downloads/Qidix.pem",
         ssh_username="ubuntu",
         remote_bind_address=('localhost', 5432)) as server:

        
        #conn = pg.connect(host="ec2-13-57-184-27.us-west-1.compute.amazonaws.com", database = "engagment", user="postgres", password="chenyang")
        conn = psycopg2.connect(database="engagment",port=server.local_bind_port, user="postgres", password="chenyang")
        curs = conn.cursor()
        
    
except(Exception, psycopg2.DatabaseError) as error:
    print(error)
