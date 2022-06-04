from pysbr import *
from datetime import datetime
from datetime import timedelta
import pandas as pd
import time
from pysbr import *
from datetime import datetime
from datetime import timedelta
import pandas as pd
import time

from django.core.mail import send_mail as sm
	
from crontab import CronTab

pd.options.mode.chained_assignment = None

def today():  
    # res = sm(
    # subject = 'Subject here',
    # message = 'Hii there. I am Inspector',
    # from_email = 'testsood981@gmail.com',
    # recipient_list = ['davinder@codenomad.net'],
    # fail_silently=False,
    # )
    gameDay = datetime.today()
   


    day = gameDay.day

    month = gameDay.month

    year = gameDay.year



    spreadDF = pd.DataFrame()
    print(spreadDF)

    nba = NBA()
    print(nba)
    sb = Sportsbook()
    print(sb)
    cols = ['event', 'participant', 'spread / total', 'decimal odds', 'american odds']

    today = str(year)+'-'+str(month)+'-'+str(day)
    print(today)


    today = datetime.strptime(today, '%Y-%m-%d')
    print(today)



    e = EventsByDate(nba.league_id, today)
    print(e)


    spread = CurrentLines(e.ids(), nba.market_ids('pointspread'), sb.ids('Bovada')[0])
    print(spread)
    spread = spread.dataframe(e)
    print(spread)



def gettoday():
 
#get over under
    # res = sm(
    # subject = 'Subject here',
    # message = 'Hii there. I am don',
    # from_email = 'testsood981@gmail.com',
    # recipient_list = ['davinder@codenomad.net'],
    # fail_silently=False,
    # )

    oldTotals = pd.read_csv('/home/codenomad/Documents/GitHub/datasport/totalcsv/totals.csv')



    newDateList = []
    for index, row in oldTotals.iterrows():
        year=str(row['joinValue'])[0:4]
        month=str(row['joinValue'])[4:6]
        day=str(row['joinValue'])[6:8]
        newDate = year+'/'+month+'/'+day

        newDateList.append(datetime.strptime(newDate,'%Y/%m/%d'))
    oldTotals['datetime'] = newDateList






    maxDate = max(oldTotals['datetime'])
    print('maxDate',maxDate)


    dateRange = pd.date_range(maxDate+timedelta(1),datetime.today()-timedelta(1),freq='d')


    #get all of the spread dataframes
    totalDF = pd.DataFrame()

    nba = NBA()
    sb = Sportsbook()
    cols = ['event', 'participant', 'over_under_total', 'decimal odds', 'american odds']

    #brute force requesting spreads from site
    #sometimes the site fails so this will keep trying until every date succeeds
    for i in dateRange:
        currentState = ''
        count = 0
        while currentState == '':
            try:
                dt = datetime.strptime(i.strftime('%Y-%m-%d'), '%Y-%m-%d')
                print(dt)
    
                e = EventsByDate(nba.league_id, dt)
                total = CurrentLines(e.ids(), nba.market_ids('total'), sb.ids('Bovada')[0])
                total = total.dataframe(e)
                frames = [totalDF,total]
                result = pd.concat(frames)
                totalDF = result
                count +=1
                currentState = 'done'
            except:
                print('failed')

    totalDF = totalDF.drop_duplicates(subset=['event id'], keep='first')
    totalDF.rename(columns={'spread / total':'over_under_total'},inplace=True)




    #convert the time column. This is used to help join to the training table later on
    #convert time stamps to yyyy/mm/dd
    newTime = []

    for index, row in totalDF.iterrows():
        tIndex = row['datetime'].find('T')
        #row['datetime'] = row['datetime'][:tIndex]
        newTime.append(row['datetime'][:tIndex])
    totalDF['datetime'] = newTime


    #split event column to get home and away teams
    #this will also help with joining to training data
    homeTeam = []
    awayTeam = []

    for index, row in totalDF.iterrows():
        atIndex = row['event'].find('@')
        homeTeam.append(row['event'][atIndex+1:])
        awayTeam.append(row['event'][:atIndex])
        
    totalDF['home'] = homeTeam
    totalDF['away'] = awayTeam



    #getting rid of - in dates
    #this will help for joining


    #finally creating join value



    dateForJoin = []
    import re
    for index, row in totalDF.iterrows():
        if row['home'] != 'Team USA' and row['home'] != 'Team Giannis East' and row['home'] != 'Team James West' and row['home'] != 'Team LeBron West':
            newDate = re.sub("[^0-9]", "", row['datetime']) + '0'
            dateForJoin.append(newDate)
        else:
            totalDF.drop(index, inplace=True)
    totalDF['dateForJoin'] = dateForJoin





    #drop columns that arent used
    totalDF = totalDF.drop(['market id','event id','sportsbook id','participant id', 'market', 'result', 'profit', 'sportsbook', 'sportsbook alias'],axis=1)
    #abb lookup dictionary
    #used for the join
    abbLookup = {
        'Milwaukee Bucks':'MIL',
        'Washington Wizards':'WAS',
        'Detroit Pistons' : 'DET',
        'Chicago Bulls' : 'CHI',
        'Brooklyn Nets' : 'BKN',
        'Houston Rockets' : 'HOU',
        'Utah Jazz' : 'UTA',
        'Toronto Raptors' : 'TOR',
        'Cleveland Cavaliers' : 'CLE',
        'Boston Celtics' : 'BOS',
        'Sacramento Kings' : 'SAC',
        'Charlotte Hornets' : 'CHA',
        'Oklahoma City' : 'OKC',
        'L.A. Lakers' : 'LAL',
        'Philadelphia 76ers' : 'PHI',
        'New Orleans' : 'NOP',
        'Dallas Mavericks' : 'DAL',
        'Portland Trail Blazers' : 'POR',
        'Golden State' : 'GSW',
        'LA Clippers' : 'LAC',
        'New York' : 'NYK',
        'Orlando Magic' : 'ORL',
        'Indiana Pacers' : 'IND',
        'Minnesota Timberwolves' : 'MIN',
        'Denver Nuggets' : 'DEN',
        'Memphis Grizzlies' : 'MEM',
        'Phoenix Suns' : 'PHO',
        'Atlanta Hawks' : 'ATL',
        'San Antonio' : 'SAS',
        'Miami Heat' : 'MIA'  
    }





    #finally creating join value
    joinValue = []
    for index,row in totalDF.iterrows():
        joinValue.append(str(row['dateForJoin']) + abbLookup[row['home']])

    totalDF['joinValue'] = joinValue
    totalDF.reset_index(inplace=True)

    finalTotal = pd.DataFrame()
    finalTotal['joinValue'] = joinValue
    finalTotal['over_under_total'] = totalDF['over_under_total']

    oldTotals = oldTotals[['joinValue','over_under_total']]

    frames = [oldTotals, finalTotal]
    result_total = pd.concat(frames)

    result_total = result_total.drop_duplicates(keep='first')



    result_total.to_csv('/home/codenomad/Documents/GitHub/datasport/totalcsv/to.csv')

    #drop duplicates
    result_total = result_total.drop_duplicates(subset=['joinValue'], keep='last')


    joinTotals = pd.DataFrame()
    joinTotals['over_under_total'] = result_total['over_under_total']
    joinTotals['joinValue'] = result_total['joinValue']


    #training data
    df = pd.read_csv('/home/codenomad/Documents/GitHub/datasport/totalcsv/finalDS.csv')


    # df = df.join(joinTotals.set_index('joinValue'),on='joinValue')


    df.to_csv('/home/codenomad/Documents/GitHub/datasport/totalcsv/finalDS.csv')









