from dbSite import execute_query as execute_querySite
from dbRage import execute_query as execute_queryRage
from dbMine import execute_query as execute_queryMine
import schedule
import time

def Sunc():
    try:
        print('start')
        playerdata = []
        resultsite = execute_querySite(f"SELECT name, money FROM data")
        resultMine = execute_queryMine(f"SELECT player_name, money FROM mpdb_economy")
        resultRage1 = execute_queryRage(f"SELECT login, character1 FROM accounts")
        resultRage2 = execute_queryRage(f"SELECT uuid, money FROM characters")
        for item1 in resultsite:
            for item2 in resultMine:
                for itemrage in resultRage1:
                    try:
                        if item1[0] == itemrage[0] and item1[0] == item2[0]:
                            if int(itemrage[1]) != -1: #без персонажа
                                for character1 in resultRage2:
                                    if int(itemrage[1]) == int(character1[0]):
                                        playerdata.append([item1[0],character1[0],float(item1[1]),float(item2[1]),float(character1[1])])
                    except:
                        print('Erorr')
        for player in playerdata:
            if player[2] != player[3]:
                execute_querySite(f"UPDATE data SET money = '{int(player[3])}' WHERE name = '{player[0]}';")
                execute_queryRage(f"UPDATE characters SET money = '{int(player[3])}' WHERE uuid = '{player[1]}';")
            if player[2] != player[4]:
                execute_querySite(f"UPDATE data SET money = '{int(player[4])}' WHERE name = '{player[0]}';")
                execute_queryMine(f"UPDATE Essentials_userdata SET money = '{int(player[4])}' WHERE player_name = '{player[0]}';")
                execute_queryMine(f"UPDATE mpdb_economy SET money = '{int(player[4])}' WHERE player_name = '{player[0]}';")
        print('good')
    except:
        print('Bad')
        
schedule.every(10).seconds.do(Sunc)

while True:
    schedule.run_pending()
    time.sleep(1)
