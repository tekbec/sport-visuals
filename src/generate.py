from sport_visuals_generator.generator import League, Team, generate
from sport_visuals_generator.utils import init_out_dir
from uploadthing.api import upload
import os, json

# Create temporary directory
srcs_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(srcs_path)
temp_path = os.path.join(root_path, 'tmp')
if not os.path.isdir(temp_path):
    os.mkdir(temp_path)

# Load leagues
league_file = os.path.join(srcs_path, 'teams.json')
leagues: dict = {}
with open(league_file, 'r') as file:
    leagues = json.load(file)

# Load visuals
visuals_file = os.path.join(root_path, 'visuals.json')
visuals: dict = {}
if os.path.isfile(visuals_file):
    try:
        with open(visuals_file, 'r') as file:
            visuals = json.load(file)
    except:
        pass

# Create visuals
for league_id, league_info in leagues.items():
    print(f'> {league_id}')
    league = League(league_info['logo'], league_info['scale'])
    if not league_id in visuals: visuals[league_id] = {}
    
    for team_1_abbr, team_1_info in league_info['teams'].items():
        team_1 = Team(team_1_info['city'], team_1_info['name'], team_1_abbr, tuple(team_1_info['color']), team_1_info['logo'].replace('{root}', root_path), team_1_info['scale'])
        if not team_1_abbr in visuals[league_id]: visuals[league_id][team_1_abbr] = {}

        for team_2_abbr, team_2_info in league_info['teams'].items():
            team_2 = Team(team_2_info['city'], team_2_info['name'], team_2_abbr, tuple(team_2_info['color']), team_2_info['logo'].replace('{root}', root_path), team_2_info['scale'])
            if not team_2_abbr in visuals[league_id][team_1_abbr]: visuals[league_id][team_1_abbr][team_2_abbr] = {}

            # File paths
            thumbnail_file = os.path.join(temp_path, f'{league_id}_{team_1.abbr}_{team_2.abbr}_thumbnail.png')
            poster_file    = os.path.join(temp_path, f'{league_id}_{team_1.abbr}_{team_2.abbr}_poster.png'   )
            square_file    = os.path.join(temp_path, f'{league_id}_{team_1.abbr}_{team_2.abbr}_square.png'   )

            print(f'  > {team_1_abbr} vs {team_2_abbr}')
           
            if os.path.isfile(thumbnail_file): os.unlink(thumbnail_file)
            if os.path.isfile(poster_file):    os.unlink(poster_file)
            if os.path.isfile(square_file):    os.unlink(square_file)

            # Generate & upload visuals
            if not 'thumbnail' in visuals[league_id][team_1_abbr][team_2_abbr]:
                print(f'    > Thumbnail')
                generate(league, team_1, team_2, 1280, 720,  thumbnail_file              )
                visuals[league_id][team_1_abbr][team_2_abbr]['thumbnail'] = upload(thumbnail_file)
                with open(visuals_file, 'w') as file:
                    json.dump(visuals, file, indent = 4)
            if not 'poster' in visuals[league_id][team_1_abbr][team_2_abbr]:
                print(f'    > Poster')
                generate(league, team_1, team_2, 680,  1000, poster_file, team_width=1.00)
                visuals[league_id][team_1_abbr][team_2_abbr]['poster']    = upload(poster_file)
                with open(visuals_file, 'w') as file:
                    json.dump(visuals, file, indent = 4)
            if not 'square' in visuals[league_id][team_1_abbr][team_2_abbr]:
                print(f'    > Square')
                generate(league, team_1, team_2, 1000, 1000, square_file, team_width=1.00)
                visuals[league_id][team_1_abbr][team_2_abbr]['square']    = upload(square_file)
                with open(visuals_file, 'w') as file:
                    json.dump(visuals, file, indent = 4)

            # Clean temp files
            if os.path.isfile(thumbnail_file): os.unlink(thumbnail_file)
            if os.path.isfile(poster_file):    os.unlink(poster_file)
            if os.path.isfile(square_file):    os.unlink(square_file)