import ibm_db;
con=ibm_db.connect("DATABASE=bludb;HOSTNAME=2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32328;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=bkj82229;PWD=KCwhio0Cb0XQmB5H",'','')

sql_command="""CREATE TABLE user_login
            (
            User_fname VARCHAR(20),
            User_lname VARCHAR(20),
            User_mailid VARCHAR(25),
            User_pswd VARCHAR(20),
            User_phoneno VARCHAR(13)
            );"""

stmt= ibm_db.prepare(con,sql_command)
ibm_db.execute(stmt)


