import pandas as pd
import numpy as np



# #Cleaning Unecessary columns
# newdf=pd.read_csv('matches.csv')
# # newdf=newdf.drop(['umpire1','umpire2','umpire3','date','result','dl_applied'],axis=1)
# print(newdf.head())
# newdf.to_csv('matches.csv',index=False)

df=pd.read_csv('matches.csv')

#Total Matches per season
total_matches=df.groupby('season')['id'].count()
print(total_matches,"\n")

#Most Successfull Team
most_matches_won=df['winner'].value_counts()
print(most_matches_won.sort_values(ascending=False),'\n')

#Most Common Venue
most_common_venue=df['venue'].value_counts().head(10)
print(most_common_venue.sort_values(ascending=False),"\n")

#Win Toss Win Match
df['toss_win_match_win']=df['toss_winner']==df['winner']
such_matches=len(df)
toss_and_match=df['toss_win_match_win'].sum()
print(f"Out of {such_matches} matches teams winning the toss won {toss_and_match} matches\n")

#Home Ground Advantage
matches_at_chin=df[df['venue']=='M Chinnaswamy Stadium']
total_matches_at_chin=matches_at_chin.shape[0]
rcb_won=(matches_at_chin['winner']=='Royal Challengers Bangalore').sum()
per=(rcb_won/total_matches_at_chin)*100
print(f"RCB won {rcb_won} matches out of {total_matches_at_chin} i.e. {per:.2f} % of matches.\n")

#Batting First
batting_first=df[df['win_by_runs']>0]['winner'].value_counts()
print('Teams winning when batting first:',batting_first,"\n")

#Bowling First
bowling_first=df[df["win_by_wickets"]>0]['winner'].value_counts()
print('Teams winning when bowling first',bowling_first,"\n")


#M.O.M winners
man_of_the_match=df['player_of_match'].value_counts().head(20)
print('Top 20 M.O.M winners in IPL',man_of_the_match,"\n")

#IPL Champions
champions=(df.groupby('season').apply(lambda x:x.iloc[-1]['winner']))
print(champions,"\n")

#Head to Head Record of Teams
df['loser']=df.apply(lambda x:x['team2'] if x['winner']=='team1' else x['team1'],axis=1)
head_to_head=pd.crosstab(df['winner'],df['loser'])
print("Head to Head Record:",head_to_head,"\n")

#Most Dominant Team at each venue
most_dominant_team=(df.groupby('venue').apply(lambda x:x['winner'].value_counts().head(1)).reset_index(level=1,name='wins')).sort_values(by='wins',ascending=False)
print(most_dominant_team.head(20),"\n")

#Ball by Ball Data

newdf=pd.read_csv('deliveries.csv')

#Most Runs
best_batsman=newdf.groupby('batsman')['total_runs'].sum().sort_values(ascending=False).head(20)
print('Batsman with most Runs:',best_batsman,"\n")

#Best Economy Rate
legal_balls=newdf[newdf['wide_runs']==0]
legal_balls=legal_balls[legal_balls['noball_runs']==0]
total_balls=legal_balls.groupby('bowler').size().sort_values(ascending=False)
total_overs=total_balls/6
qualified_bowlers=total_overs[total_overs>=100]


total_runs_conceded=newdf.groupby('bowler')['total_runs'].sum()
economy=(total_runs_conceded/qualified_bowlers).sort_values()
print(economy,"\n")

#Best Strike Rate

balls_faced=legal_balls.groupby('batsman').size()
qualified_batsman=balls_faced[balls_faced>500]
strike_rate=(best_batsman/qualified_batsman)*100
print(strike_rate.sort_values(ascending=False),"\n")