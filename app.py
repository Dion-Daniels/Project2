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
from flask import Flask, render_template
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
@app.route('/index')
def index():
   return render_template("index.html")

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
          "<p>/api/v1.0/region/player_id</p>"
          "<p>/api/v1.0/region/player_tag</p>"          
          "<p>/api/v1.0/region</p>"
          "<hr>"
          "<p>player_tag Json file</p>"
                  '"player_tag": \
        <br>"player_id": \
        <br>"region": \
        <br>"color": \
        <br>"game_id": \
        <br>"wins_loses":  \
        <br>"games": \
        <p style="margin-left:50px; margin-top:-5px;">{ "total" : </p>\
        <p style="margin-left:50px; margin-top:-15px;">"total_orange" : </p>\
        <p style="margin-left:50px; margin-top:-15px;">"total_blue" : </p>\
        <p style="margin-left:50px; margin-top:-15px;">}</p>\
        "wins":  \
        <p style="margin-left:50px; margin-top:-5px;">{"total_wins": </p>\
        <p style="margin-left:50px; margin-top:-15px;">"total_wins_orange": </p>\
        <p style="margin-left:50px; margin-top:-15px;">"total_wins_blue": </p>\
        <p style="margin-left:50px; margin-top:-15px;">},</p>\
        "loses":  \
        <p style="margin-left:50px; margin-top:-5px;"> {"total_loses": </p>\
        <p style="margin-left:50px; margin-top:-15px;">"total_loses_orange": </p>\
        <p style="margin-left:50px; margin-top:-15px;">"total_loses_blue": </p>\
        <p style="margin-left:50px; margin-top:-15px;">}</p>\
        "goals_as":  \
        <p style="margin-left:50px; margin-top:-5px;"> {"goals_as_orange": </p>\
        <p style="margin-left:50px; margin-top:-15px;">"goals_as_blue": </p>\
        <p style="margin-left:50px; margin-top:-15px;">}</p>\
        "win_percent": \
        <br>"lose_percent": \
        <br>"avg_score": \
        <br>"score": \
        <br>"avg_assists": \
        <br>"assists": \
        <br>"avg_goals": \
        <br>"goals": \
        <br>"avg_saves": \
        <br>"saves": \
        <br>"avg_shoot_percentage": \
        <br>"shoot_percentage": \
        <br>"avg_shots": \
        <br>"shots": \
            '
          ) 

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

@app.route('/api/v1.0/<region>/<player_tag>')
def player_select_tag(region,player_tag):
    
    stmt = session.query(players).\
            filter((players.team_region ==region)&(players.player_tag == player_tag)).statement
    tag_df = pd.read_sql_query(stmt, session.bind).dropna()

    tag_dict ={
        "player_tag": tag_df["player_tag"].drop_duplicates()[0],
        "player_id": tag_df["player_id"].drop_duplicates().tolist(),
        "region": tag_df["team_region"].drop_duplicates()[0],
        "color": tag_df["color"].tolist(),
        "game_id": tag_df["game_id"].tolist(),
        "wins_loses":  tag_df["winner"].tolist(),
        "games": { "total" : float(tag_df["winner"].count()),
                    "total_orange" : float(tag_df["winner"][tag_df["color"]=="orange"].count()),
                    "total_blue" : float(tag_df["winner"][tag_df["color"]=="blue"].count())
                    },
        "wins":  {"total_wins": float(tag_df["winner"][tag_df["winner"]=="True"].count()),
                "total_wins_orange": float(tag_df["winner"][(tag_df["winner"]=="True")&(tag_df["color"]=="orange")].count()),
                "total_wins_blue": float(tag_df["winner"][(tag_df["winner"]=="True")&(tag_df["color"]=="blue")].count()),
                    },
        "loses":  {"total_loses": float(tag_df["winner"][tag_df["winner"]=="False"].count()),
                "total_loses_orange": float(tag_df["winner"][(tag_df["winner"]=="False")&(tag_df["color"]=="orange")].count()),
                "total_loses_blue": float(tag_df["winner"][(tag_df["winner"]=="False")&(tag_df["color"]=="blue")].count()),
                    },
        "win_percent": round(tag_df["winner"][tag_df["winner"]=="True"].count()/ tag_df["winner"].count()*100,2),
        "lose_percent": round(tag_df["winner"][tag_df["winner"]=="False"].count()/ tag_df["winner"].count()*100,2),
        "avg_score": round(tag_df["core_score"].mean(),2),
        "score": tag_df["core_score"].tolist(),
        "avg_assists": round(tag_df["core_assists"].mean(),2),
        "assists": tag_df["core_assists"].tolist(),
        "avg_goals": round(tag_df["core_goals"].mean(),2),
        "goals": tag_df["core_goals"].tolist(),
        "goals_as": {"goals_as_orange": float(tag_df["core_goals"][tag_df["color"]=="orange"].sum()),
                    "goals_as_blue":    float(tag_df["core_goals"][tag_df["color"]=="blue"].sum())
                    },
        "avg_saves": round(tag_df["core_saves"].mean(),2),
        "saves": tag_df["core_saves"].tolist(),
        "avg_shoot_percentage": round(tag_df["core_shooting_percentage"].mean(),2),
        "shoot_percentage": tag_df["core_shooting_percentage"].tolist(),
        "avg_shots": round(tag_df["core_shots"].mean(),2),
        "shots": tag_df["core_shots"].tolist(),
    }
    return jsonify(tag_dict)

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
        "game_id": df3["game_id"].tolist(),
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
    region_df = pd.read_sql_query(stmt, session.bind).dropna()
    region_dict ={
        "player_id": region_df["player_id"].drop_duplicates().tolist(),
        "player_tag": region_df["player_tag"].drop_duplicates().tolist(),
        "region": region_df["team_region"].drop_duplicates()[0],
        "games": float(region_df["winner"].count()),
        "wins":  float(region_df["winner"][region_df["winner"]=="True"].count()),
        "loses": float(region_df["winner"][region_df["winner"]=="False"].count()),
        "Win_percent": round(region_df["winner"][region_df["winner"]=="True"].count()/ region_df["winner"].count()*100,2),
        "lose_percent": round(region_df["winner"][region_df["winner"]=="False"].count()/ region_df["winner"].count()*100,2),
        "avg_score": round(region_df["core_score"].mean(),2),
        "avg_assists": round(region_df["core_assists"].mean(),2),
        "avg_goals": round(region_df["core_goals"].mean(),2),
        "avg_saves": round(region_df["core_saves"].mean(),2),
        "avg_shoot_percentage": round(region_df["core_shooting_percentage"].mean(),2),
        "avg_shots": round(region_df["core_shots"].mean(),2) 
        }
   
    return jsonify(region_dict)


if __name__ == "__main__":
    app.run(debug=True)
