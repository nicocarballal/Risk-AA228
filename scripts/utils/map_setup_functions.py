from utils.game_map_class import GameMap
from utils.game_team_class import GameTeam
import random

def setGameBoardRandom(team_names, risk_map, strategy_classes = [None, None]):
    '''
    Inputs:
    team_names: Your desired team names
    risk_map: RiskMap
    strategy_class: A specific strategy (i.e. "RandomStrategy")

    Output:
    risk_map: Updated RiskMap with territories and troops assigned
    teams: Array of teams in the RiskMap
    '''
    teams = []
    i = 0
    for i in range(len(team_names)):
        strategy_class = strategy_classes[i]
        team_name = team_names[i]
        teams.append(GameTeam(team_name, risk_map, strategy = strategy_class, territories = []))
    num_teams = len(teams)
    i = 0
    territories = risk_map.getTerritories()
    random.shuffle(territories)
    for block in territories:
        teams[i % num_teams].addTerritory(block)
        teams[i % num_teams].addTroops(block, 1)
        risk_map.setTeam(block, team_names[i % num_teams])
        i += 1
    return risk_map, teams

def setGameBoardRandomWithTroops(team_names, risk_map, strategy_classes = [None, None]):
    risk_map, teams = setGameBoardRandom(team_names, risk_map, strategy_classes = strategy_classes)
    for team in teams:
        for i in range(19):
            random_territory = random.choice(team.getTerritories())
            team.addTroops(random_territory, 1)
    return risk_map, teams

def initializeFullRiskMap():
    risk_blocks = \
    {"North America":
         ("orange",
          ["Alaska",
            "North West Territory",
            "Alberta",
            "Ontario",
            "Quebec",
            "Western United States",
            "Eastern United States",
            "Central America",
            "Greenland"]
         ),

    "South America":
         ("yellow",
          ["Venezuela",
            "Brazil",
            "Peru",
            "Argentina"]
         ),

    "Europe":
         ("purple",
          ["Iceland",
            "Great Britain",
            "Western Europe",
            "Northern Europe",
            "Southern Europe",
            "Ukraine",
            "Scandinavia"]
         ),


    "Asia":
         ("green",
          ["Middle East",
            "Afghanistan",
            "Ural",
            "Siberia",
            "Yakutsk",
            "Irkutsk",
            "Mongolia",
            "China",
            "India",
            "Siam",
            "Kamchatka",
            "Japan"]
         ),

    "Australia":
         ("pink",
          ["Indonesia",
            "New Guinea",
            "Western Australia",
            "Eastern Australia"]
         ),

    "Africa":
         ("brown",
          ["Egypt",
           "North Africa",
           "East Africa",
           "Congo",
           "South Africa",
           "Madagascar"]
         )
    }
    risk_edges = [("Alaska","North West Territory"),
              ("Alaska","Alberta"),
              ("Alaska","Kamchatka"),
              ("North West Territory","Alberta"),
              ("North West Territory","Ontario"),
              ("North West Territory","Greenland"),
              ("Alberta","Ontario"),
              ("Alberta","Western United States"),
              ("Ontario","Greenland"),
              ("Ontario","Quebec"),
              ("Ontario","Western United States"),
              ("Ontario","Eastern United States"),
              ("Greenland","Quebec"),
              ("Greenland","Iceland"),
              ("Quebec","Eastern United States"),
              ("Western United States","Eastern United States"),
              ("Western United States","Central America"),
              ("Eastern United States","Central America"),
              ("Central America","Venezuela"),
              ("Venezuela","Brazil"),
              ("Venezuela","Peru"),
              ("Brazil","Peru"),
              ("Brazil","Argentina"),
              ("Brazil","North Africa"),
              ("Peru","Argentina"),
              ("Iceland","Great Britain"),
              ("Iceland","Scandinavia"),
              ("Great Britain","Scandinavia"),
              ("Great Britain","Northern Europe"),
              ("Great Britain","Western Europe"),
              ("Western Europe","Northern Europe"),
              ("Western Europe","Southern Europe"),
              ("Western Europe","North Africa"),
              ("Northern Europe","Scandinavia"),
              ("Northern Europe","Southern Europe"),
              ("Northern Europe","Ukraine"),
              ("Southern Europe","Ukraine"),
              ("Southern Europe","Middle East"),
              ("Southern Europe","Egypt"),
              ("Southern Europe","North Africa"),
              ("Ukraine","Scandinavia"),
              ("Ukraine","Ural"),
              ("Ukraine","Afghanistan"),
              ("Ukraine","Middle East"),
              ("Egypt","Middle East"),
              ("Egypt","East Africa"),
              ("Egypt","North Africa"),
              ("North Africa","East Africa"),
              ("North Africa","Congo"),
              ("East Africa","Middle East"),
              ("East Africa","Madagascar"),
              ("East Africa","South Africa"),
              ("East Africa","Congo"),
              ("Congo","South Africa"),
              ("South Africa","Madagascar"),
              ("Middle East","Afghanistan"),
              ("Middle East","India"),
              ("Afghanistan","Ural"),
              ("Afghanistan","China"),
              ("Afghanistan","India"),
              ("Ural","Siberia"),
              ("Ural","China"),
              ("Siberia","Yakutsk"),
              ("Siberia","Irkutsk"),
              ("Siberia","Mongolia"),
              ("Siberia","China"),
              ("Yakutsk","Kamchatka"),
              ("Yakutsk","Irkutsk"),
              ("Irkutsk","Kamchatka"),
              ("Irkutsk","Mongolia"),
              ("Mongolia","China"),
              ("Mongolia","Kamchatka"),
              ("Mongolia","Japan"),
              ("China","Siam"),
              ("China","India"),
              ("India","Siam"),
              ("Siam","Indonesia"),
              ("Kamchatka","Japan"),
              ("Indonesia","New Guinea"),
              ("Indonesia","Western Australia"),
              ("New Guinea","Western Australia"),
              ("New Guinea","Eastern Australia"),
              ("Western Australia","Eastern Australia")]
    return GameMap(risk_blocks,risk_edges,{})
