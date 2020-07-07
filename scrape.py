import requests
from bs4 import BeautifulSoup
import datetime
import mysql.connector
import time
start=time.time()
database_name='big'
table_name='matches'
mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database=database_name,
                               auth_plugin='mysql_native_password')

def delete_duplicates():
    global mycursor,mydb,table_name
    mycursor.execute("Select * from "+table_name+" group by teams having count(*)>1")
    result = mycursor.fetchall()
    # print(result)
    if len(result)>0:
        print("deleting the following duplicates ")
        for idm in result:
            mycursor.execute("DELETE FROM "+table_name+" WHERE id="+str(idm[0]))
            print(idm)
            f.write("Duplicate found: "+str(idm)+'\n')
        mydb.commit()
    else:
        print("no duplicates")

def insert_oneteam(team):
    global url_dict, f, mycursor,mydb
    resp = requests.get(url_dict.get(team))
    soup = BeautifulSoup(resp.text, 'html.parser')

    home = soup.find_all('span', class_='matches__item-col matches__participant matches__participant--side1')
    away = soup.find_all('span', class_='matches__item-col matches__participant matches__participant--side2')
    time = soup.find_all('span', class_='matches__date')
    date = soup.find_all('h4', class_='fixres__header2')
    if len(date)>0:
        for ho, aw, tim, dt in zip(home, away, time, date):
            s = dt.text.strip().split(" ")
            if len(s[1]) == 4: # 1st or 22nd
                day = s[1][:2]
            else:
                day = s[1][:1]
            mnth = calendar.get(s[2])  # month
            curr_time = datetime.date.today()
            match_date = datetime.date(curr_time.year, mnth, int(day))
            team = ho.text.strip() + " vs " + aw.text.strip()
            rs = str(int(tim.text.strip()[:2])+2)+tim.text.strip()[2:] # RO Time
            match = str(match_date) + " " + rs  + " " + team
            f.write(match + '\n')
            mycursor.execute("INSERT INTO "+table_name+"(date, time, teams) VALUES(%s,%s,%s)",
                            (match_date, rs, team))
    else:
        print(teamName +" doesn't have matches scheduled")
    mydb.commit()

# You can add more teams but make sure u put their fixtures link from skysports in the dictionary
url_dict = {
    'Barcelona': 'https://www.skysports.com/barcelona-fixtures',
    'Bayern': 'https://www.skysports.com/bayern-munich-fixtures',
    'Juventus': "https://www.skysports.com/juventus-fixtures",
    "Manchester City": "https://www.skysports.com/manchester-city-fixtures",
    "Liverpool": "https://www.skysports.com/liverpool-fixtures",
    "Real Madrid":'https://www.skysports.com/real-madrid-fixtures'
}
calendar = {"January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
            }


mycursor = mydb.cursor()
f = open("RaportInsert.txt", 'a+t')
if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    f.write("\n")

    for teamName in url_dict.keys():
        insert_oneteam(teamName)
    f.write("\n")
    delete_duplicates()
    f.write("----------------------------------------------------\n")
    f.write("IT MAY CONTAIN DUPLICATES HERE BUT NOT IN THE DB "+"raport updated on " + str(datetime.datetime.now()))
    mydb.close()

    print("It took ",time.time()-start," seconds ")
    f.close()
    exit()


    






