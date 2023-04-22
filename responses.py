import random
import requests
import datetime
import pytz
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# API Call
def call_api(url: str) -> dict:
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {}

# Schedule
def get_schedule(month: str, day: str) -> str:
    api_key = os.environ["API_KEY"]
    url = f"https://api.sportradar.com/nba/trial/v8/en/games/2023/{month}/{day}/schedule.json?api_key={api_key}"
    data = call_api(url)

    schedule = ""
    for game in data['games']:
        home_team = game['home']['name']
        away_team = game['away']['name']
        scheduled_time = game['scheduled']

        # Parse and format the scheduled_time
        dt = datetime.datetime.fromisoformat(
            scheduled_time.rstrip('Z')).replace(tzinfo=pytz.utc)
        local_tz = pytz.timezone('Canada/Central')
        local_dt = dt.astimezone(local_tz)
        formatted_time = local_dt.strftime('%I:%M %p')

        schedule += f"**{home_team}** @ **{away_team}** at {formatted_time}\n"

    return schedule

# Standings
def get_standings() -> str:
    api_key = os.environ["API_KEY"]
    url = f"https://api.sportradar.com/nba/trial/v8/en/seasons/2022/REG/standings.json?api_key={api_key}"
    standings_data = call_api(url)

    if standings_data and standings_data.get("conferences"):
        standings_str = ""

        for conference in standings_data["conferences"]:
            teams = []

            for division in conference["divisions"]:
                teams.extend(division["teams"])

            teams.sort(key=lambda x: x["calc_rank"]["conf_rank"])

            standings_str += f"**{conference['name']} 2022-2023:**\n"
            standings_str += "\n".join(
                [f"{t['calc_rank']['conf_rank']}. {t['name']} ({t['wins']}-{t['losses']})" for t in teams])
            standings_str += "\n\n"

        return standings_str.strip()
    else:
        return "Sorry, no conference data found."
    
# Roster
def get_roster(team: str) -> str:
    api_key = os.environ["API_KEY_2"]
    url = f"https://api.sportsdata.io/v3/nba/scores/json/PlayersBasic/{team}?key={api_key}"
    data = call_api(url)

    if not data:
        return "Sorry, I couldn't find any roster information for the specified team."

    roster = f"**Roster for {team}:**\n"
    for player in data:
        roster += f"{player['Jersey']}. {player['FirstName']} {player['LastName']} ({player['Position']})\n"

    return roster

# Teams
def get_teams() -> str:
    api_key = os.environ["API_KEY_2"]
    url = f"https://api.sportsdata.io/v3/nba/scores/json/teams?key={api_key}"
    data = call_api(url)

    if not data:
        return "Sorry, I couldn't find any team information."

    # Group teams by conference
    conferences = {"Eastern": [], "Western": []}
    for team in data:
        conference = team["Conference"]
        conferences[conference].append(
            f"{team['Key']}: {team['City']} {team['Name']}")

    # Format the output
    output = "**NBA Teams:**\n\n"
    for conference, teams in conferences.items():
        output += f"**{conference} Conference**\n"
        for team_info in teams:
            output += f"{team_info}\n"
        output += "\n"

    return output

# Responses
def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message.startswith('!hello'):
        return 'Hey there!'

    if p_message.startswith('!schedule'):
        split_message = p_message.split(' ')

        if len(split_message) == 1:
            today = datetime.date.today()
            month = str(today.month).zfill(2)
            day = str(today.day).zfill(2)
        elif (len(split_message) == 2 and split_message[1] == 'tomorrow'):
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            month = str(tomorrow.month).zfill(2)
            day = str(tomorrow.day).zfill(2)
        else:
            date = split_message[1]
            month, day = date.split('-')

        return get_schedule(month, day)

    if p_message.startswith('!standings'):
        return get_standings()
    
    if p_message.startswith('!roster'):
        split_message = p_message.split(' ')

        if len(split_message) == 1:
            return "Please provide a team abbreviation, e.g. `!roster LAL`."
        else:
            team = split_message[1].upper()
        return get_roster(team)

    if p_message.startswith('!teams'):
        return get_teams()
        
    if p_message.startswith('!trivia'):
        x = (random.randint(1, 6))
        match x:
            case 1:
                return """**Fun Fact #1:** 
Did you know? Shaquille O\'Neal has only made one 3 pointer in his NBA career!"""
            case 2:
                return """**Fun Fact #2:** 
Did you know? Kyle Lowry helped design the 2019 NBA final ring - the biggest and most expensive one to date!"""
            case 3:
                return """**Fun Fact  #3:** 
Did you know? Giannis Antetokounmpo\'s family immigrated illegaly to Greece from Nigeria, where they lived in poverty until Giannis made it to the NBA and brought them with him."""
            case 4:
                return """**Fun Fact #4:**
Did you know? LeBron James has only missed the playoffs 4 times in his entire career!"""
            case 5:
                return """**Fun Fact  #5:** 
Did you know? Michael Jordan\'s shoe deal with Nike for Jordans is one of the most successful partnerships of all time!"""
            case 6:
                return """**Fun Fact #6:** 
Did you know? Steph Curry\'s first name is actually Wardell. His middle name is Stephen!"""

# Help
    if p_message.startswith('!help'):
        return '''**Commands:**
`!hello` - Say hello to the bot
`!schedule` - Get the schedule for today
`!schedule tomorrow` - Get the schedule for tomorrow
`!schedule [MM-DD]` - Get the schedule for a specific date
`!standings` - Get the current standings for the NBA
`!roster [team]` - Get the roster for a specific team, by team abbreviation (i.e. LAL)
`!teams` - Get a list of all NBA teams and their abbreviations
`!trivia` - Get a fun fact about the NBA
`!help` - Get a list of commands'''
