# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 21:27:51 2022

@author: Preston Robertson
"""

#%% Importing Libraries

from riotwatcher import LolWatcher
import pandas as pd
import urllib.request, json, time, os
from datetime import date



#%% Get API

def getAPI_key():
    f = open(path + "api_key.txt", "r")
    return f.read()



#%% Gathering Game List

def GetJSONdata():
    staticURL = 'https://canisback.com/matchId/matchlist_na1.json'
    # Only change URL if the there was an update to the website
    
    with urllib.request.urlopen(staticURL) as url:
        Match_List = json.load(url)
        print(Match_List[0])
        
    current_json = date.today().strftime("%b-%d-%Y")
    print(current_json)
    # Setting the date
    
    return(Match_List)



#%% Main



path = '...'
lol_watcher = LolWatcher(getAPI_key())
my_region = 'na1'
current_json = date.today().strftime("%b-%d-%Y")



me = lol_watcher.summoner.by_name(my_region, 'Leogi')
print(me)
# Test



#%% To Record

desired_list = ['assists',
                'baronKills',
                
                #'basicPings',
                # Some games just do not collect them
                
                'bountyLevel',
                'champExperience',
                'champLevel',
                'championName',
                'damageDealtToObjectives',
                'damageSelfMitigated',
                'deaths',
                'dragonKills',
                'firstBloodAssist',
                'firstBloodKill',
                'gameEndedInSurrender',
                'goldEarned',
                'goldSpent',
                'individualPosition',
                'inhibitorKills',
                'inhibitorsLost',
                'item0',
                'item1',
                'item2',
                'item3',
                'item4',
                'item5',
                'item6',
                'kills',
                'lane',
                'largestCriticalStrike',
                'largestKillingSpree',
                'longestTimeSpentLiving',
                'magicDamageDealtToChampions',
                'magicDamageTaken',
                'nexusLost',
                'objectivesStolen',
                'physicalDamageDealtToChampions',
                'physicalDamageTaken',
                'spell1Casts',
                'spell2Casts',
                'spell3Casts',
                'spell4Casts',
                'summoner1Casts',
                'summoner1Id',
                'summoner2Casts',
                'summoner2Id',
                'summonerId',
                'teamEarlySurrendered',
                'teamId',
                'timeCCingOthers',
                'timePlayed',
                'totalDamageDealtToChampions',
                'totalDamageShieldedOnTeammates',
                'totalDamageTaken',
                'totalHeal',
                'totalHealsOnTeammates',
                'totalMinionsKilled',
                'totalTimeCCDealt',
                'totalTimeSpentDead',
                'trueDamageDealtToChampions',
                'trueDamageTaken',
                'turretTakedowns',
                'turretsLost',
                'visionScore',
                'visionWardsBoughtInGame',
                'wardsKilled',
                'wardsPlaced',
                'win']




#%% Pulling from API





start_time = time.time()






def GetDesiredListData(n):
    # where "n" is the the number of games you want to extract
    
    start_time = time.time()
    
    
    Match_List = GetJSONdata()
    # Getting Match_List from website
    
    
    me = lol_watcher.summoner.by_name(my_region, 'Leogi')
    my_matches = lol_watcher.match.matchlist_by_puuid(my_region, me['puuid'])
    last_match = my_matches[0]
    match_detail = lol_watcher.match.by_id(my_region, match_id= last_match)
    current_mode = match_detail['info']['gameMode']
    # Setting up first column and testing
    
    
    
    
    
    participants_row = {}
    # Clearing repeatable dictionary
    
    for i in range(0, len(desired_list)):
    # Looping to gather all information from the desired list    
        
        participants_row[desired_list[i]] = match_detail['info']['participants'][0][desired_list[i]]
        # Gathering all data from desired list
        
        participants_row['GameID'] = last_match
        # Recording GameID
        
        participants_row['GameMode'] = current_mode
        # Recording GameMode
        
    games_info = pd.DataFrame.from_dict(participants_row, orient = 'index')
    # Turning the Dictionary to Dataframe
    
    games_info = games_info.T
    # Translating the Features to the columns
    
    
    # for z in range(0,len(Match_List)):
        
        
        
        
        
        
        # Turn on if you want all the data from the random game list
        # Roughly 10,000 games per.
        
    for z in range(0,n):
        
        match_detail = lol_watcher.match.by_id(my_region, match_id= "NA1_" + str(Match_List[z]))
        current_mode = match_detail['info']['gameMode']
        current_match = Match_List[z]
        
        
        for j in range(0, len(match_detail['info']['participants'])):
            
            participants_row = {}
            # Clearing repeatable dictionary
            
            for i in range(0,len(desired_list)):
                
                participants_row[desired_list[i]] = match_detail['info']['participants'][j][desired_list[i]]
                # Gathering all data from desired list
                
                participants_row['GameID'] = current_match
                # Recording GameID
                
                participants_row['GameMode'] = current_mode
                # Recording GameMode
            
                
            # Back to j For Loop
            temp_df = pd.DataFrame.from_dict(participants_row, orient = 'index')
            # Turning the Dictionary to Dataframe
            
            temp_df = temp_df.T
            # Translating the Features to the columns
            
            games_info = pd.concat([games_info,temp_df])
            # Adding newly recorded values to the dataframe
        
        print(z)
        
    
    print('---%s seconds ---' % (time.time() - start_time))    
    return(games_info)
    




#%% Making CSV file


def GetCSVofDesiredList(n):
    # Where "n" is the amount of games extracted
    
    games_info = GetDesiredListData(n)
    # Get the data
    
    matches = str(n)
    
    if os.path.exists(path+ '/' + current_json):
    # If folder for today exists then print to folder
        
        games_info.to_csv(path + '/' + current_json + '/' + current_json + '_' + matches +'matches' + '.csv')
        # Collected data 
        
    else: 
        new_path = os.path.join(path, current_json)
        # Creating folder for today's date
        
        print("Directory '% s' created" % current_json)
        
        try: 
            os.mkdir(new_path) 
            # Trying to make the folder in the new path
            
        except OSError as error: 
            print(error) 
            
        games_info.to_csv(path + '/' + current_json + '/' + current_json + '_' + matches +'matches' + '.csv')
        # Collected data 
            
        


