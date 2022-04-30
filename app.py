#import libraries
from flask import Flask, jsonify
import pandas as pd
import datetime as dt
from datetime import date
from dateutil.relativedelta import relativedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask_cors import CORS
from flask_compress import Compress

#create engine and classes
engine = create_engine("sqlite:///RocketLeague.db")
inspector = inspect(engine)
inspector.get_table_names()
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

players = Base.classes.games_by_players_clean
teams = Base.classes.games_by_teams_clean
main = Base.classes.main_clean

session = Session(engine)


#create variables for most recent recording date, date 12 months prior, and station with most recordings
#latest_recording = (session.query(Measurement.date).order_by(Measurement.date.desc()).first()).date
#last_12m_iso = date.fromisoformat(latest_recording)- relativedelta(years=1)
#last_12m = date.isoformat(last_12m_iso)

#top_station = (session.query(func.count(Measurement.date),Measurement.station).\
#    group_by(Measurement.station).\
#    order_by(func.count(Measurement.date).desc()).first()).station



#################################################
# Flask Setup
#################################################
# @TODO: Initialize your Flask app here
# YOUR CODE GOES HERE
app = Flask(__name__)
Compress(app)
CORS(app)
#################################################
# Flask Routes
#################################################

#Home page with route ids
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return(f"<h1>Project 2 - Rocket League</h1><hr>"
          "<p>by Cheng, Musah, and Dion</p>"
          "<hr><strong>Do not use for data exploration! Due to size of datasets load times are slow 30s + </strong>"
          "<p>/api/v1.0/raw_main</p>"
          "<p>/api/v1.0/raw_players</p>"
          "<p>/api/v1.0/raw_teams</p>"
          "<p>/api/v1.0/IDs</p>"
          "<p>/api/v1.0/<region>/<player_id></p>"
          "<p>/api/v1.0/<region></p>") 

# page for last 12 months of percipitation data
@app.route('/api/v1.0/raw_main')
def main_raw_data():
    stmt = session.query(main).statement
    df2 = pd.read_sql_query(stmt, session.bind).dropna()
    
    return jsonify(df2.to_dict())

@app.route('/api/v1.0/raw_players')
def players_raw_data():
    stmt = session.query(players).statement
    df2 = pd.read_sql_query(stmt, session.bind).dropna()
    
    return jsonify(df2.to_dict())

@app.route('/api/v1.0/raw_teams')
def team_raw_data():
    stmt = session.query(teams).statement
    df2 = pd.read_sql_query(stmt, session.bind).dropna()
    
    return jsonify(df2.to_dict())
@app.route('/api/v1.0/test')
def test():
    stmt = session.query(main.game_id).statement
    df2 = pd.read_sql_query(stmt, session.bind).dropna()
    
    return jsonify(df2.to_dict())
    
@app.route('/api/v1.0/IDs')
def id():
    stmt = session.query(players.team_region, players.player_tag, players.player_id).statement
    df2 = pd.read_sql_query(stmt, session.bind).dropna()
    names = df2.drop_duplicates(subset=['player_tag', 'player_id'])
    regions = df2.drop_duplicates(subset='team_region')
    thisdict =	{
        "region": regions['team_region'].tolist(),
        "player_tag": names['player_tag'].tolist(),
        "player_id": names['player_id'].tolist()
    }
    return jsonify(thisdict)

@app.route('/api/v1.0/<region>/<player_id>')
def player_select(region,player_id):
    
    stmt = session.query(players).\
            filter((players.team_region ==region)&(players.player_id ==player_id)).statement
    df3 = pd.read_sql_query(stmt, session.bind).dropna()
    thisdict ={
        "player_id": df3["player_id"].drop_duplicates()[0],
        "player_tag": df3["player_tag"].drop_duplicates()[0],
        "region": df3["team_region"].drop_duplicates()[0],
        "color": df3["color"].tolist(),
        "wins_loses":  df3["winner"].tolist(),
        "games": float(df3["winner"].count()),
        "wins":  float(df3["winner"][df3["winner"]=="True"].count()),
        "loses": float(df3["winner"][df3["winner"]=="False"].count()),
        "Win_percent": round(df3["winner"][df3["winner"]=="True"].count()/ df3["winner"].count()*100,2),
        "lose_percent": round(df3["winner"][df3["winner"]=="False"].count()/ df3["winner"].count()*100,2),
        "avg_score": round(df3["core_score"].mean(),2),
        "score": df3["core_score"].tolist(),
        "avg_assists": round(df3["core_assists"].mean(),2),
        "assists": df3["core_assists"].tolist(),
        "avg_goals": round(df3["core_goals"].mean(),2),
        "goals": df3["core_goals"].tolist(),
        "avg_saves": round(df3["core_saves"].mean(),2),
        "saves": df3["core_saves"].tolist(),
        "avg_shoot_percentage": round(df3["core_shooting_percentage"].mean(),2),
        "shoot_percentage": df3["core_shooting_percentage"].tolist(),
        "avg_shots": round(df3["core_shots"].mean(),2),
        "shots": df3["core_shots"].tolist(),
    }
    return jsonify(thisdict)

@app.route('/api/v1.0/<region>')
def region_select(region):
    
    stmt = session.query(players).\
            filter((players.team_region ==region)).statement
    df3 = pd.read_sql_query(stmt, session.bind).dropna()
    return jsonify(df3.to_dict())

if __name__ == "__main__":
    app.run(debug=True)
