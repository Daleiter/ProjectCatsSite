from service.dbSite import execute_query as execute_querySite
from service.dbRage import execute_query as execute_queryRage
from service.dbMine import execute_query as execute_queryMine
from flask import Flask, send_from_directory
from flask_restful import Resource, reqparse

class AddMoney(Resource):
    def get(user):
        try:
            print('start', user)
            playerdata = []
            resultsite = execute_querySite(f"SELECT name, money FROM data WHERE name = '{user}'")
            resultMine = execute_queryMine(f"SELECT player_name, money FROM mpdb_economy WHERE player_name = '{user}'")
            resultRage1 = execute_queryRage(f"SELECT login, character1 FROM accounts WHERE login = '{user}'")
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
                    try:
                        execute_querySite(f"UPDATE data SET money = '{int(player[2])+1000}' WHERE name = '{player[0]}';")
                    except:
                        pass
                    try:
                        execute_queryRage(f"UPDATE characters SET money = '{int(player[4])+1000}' WHERE uuid = '{player[1]}';")
                    except:
                        pass
                    try:
                        execute_queryMine(f"UPDATE Essentials_userdata SET money = '{int(player[3])+1000}' WHERE player_name = '{player[0]}';")
                    except:
                        pass
                    try:
                        execute_queryMine(f"UPDATE mpdb_economy SET money = '{int(player[3])+1000}' WHERE player_name = '{player[0]}';")
                    except:
                        pass
            print('good')
        except:
            print('Bad')
            