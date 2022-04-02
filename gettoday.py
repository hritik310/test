from pysbr import *
from datetime import datetime
from datetime import timedelta
import pandas as pd
import time


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


   