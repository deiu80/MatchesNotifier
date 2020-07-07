import datetime
import smtplib, ssl
import time
from scrape import url_dict, insert_oneteam, delete_duplicates,table_name
from scrape import mydb, mycursor, f

#  the mysql server has to be open

start_time = time.time()


def sendmail(message):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com" # enter email server u use , i used gmail
    sender_email = ""  # Enter your address
    receiver_email = ""  # Enter receiver address
    password = '' # Enter senders password
    context = ssl.create_default_context()
    file = open("Report.txt", "a+t")
    file.write("Email sent with the following message \n" + message + "\n ---------------------\n")

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.ehlo()
        server.sendmail(sender_email, receiver_email, message)
        server.close()
    file.write(str(datetime.datetime.now()) + "\n")
    file.close()


def delete_matches():
    global mydb, mycursor
    # deleting the (minimum 10) matches that are old in the database
    mycursor.execute("SELECT id FROM "+table_name+" where date < \'" + str(datetime.date.today) + "\'")
    nr = mycursor.fetchall()
    # print(nr)
    if len(nr) >= 10: 
        for tpl in nr:
            mycursor.execute("delete from "+table_name+" where id=" + str(tpl[0]))
    mydb.commit()


print(mydb)
print(mydb.get_server_info() + "\n")


def update_matches():
    global mydb, mycursor
    for teamName in url_dict.keys():
        mycursor.execute("select count(*) from "+table_name+" where teams like '%" + teamName + "%'")
        nr = mycursor.fetchall()
        if int(str(nr[0][0])) <= 3:
            print("inserting more matches for \n" + teamName + ' has ' + str(nr[0]) + ' matches in the current db')
            insert_oneteam(teamName)
        mydb.commit()


curr_time = datetime.date.today()


if __name__ == "__main__":
    # we have matches today !
    mycursor.execute("SELECT date,time,teams FROM "+table_name+" where date=\'" + str(curr_time) + "\' order by time asc")
    results = mycursor.fetchall()
    mydb.commit()

    message = """
    Meciurile de azi sunt:
    """
    if len(results) != 0:
        for match in results:
            print(match)
            message += "\n"+str(match[1]) + " " + str(match[2]) + '\n'
        print(message)
        sendmail(message)
        print('Email sent')
    delete_matches()
    # it updates the db with matches
    update_matches()
    delete_duplicates()
    f.write("----------------------------------------------------\n")
    f.write("IT MAY CONTAIN DUPLICATES HERE BUT NOT IN THE DB " + " raport updated on " + str(datetime.datetime.now()))
    print("--- %s seconds ---" % (time.time() - start_time))
    exit()
