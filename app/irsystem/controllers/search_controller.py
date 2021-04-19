# from flask_login import login_required

from . import *
from app.irsystem.controllers.get_input_lists import *
from app.irsystem.controllers.tags_movie_match import *
from app.irsystem.controllers.titles_movie_match import *
import json

project_name = "Steamy Reviews: Game Recommendation Engine"
net_id = "Chang Wei: cw887, Qichen Hu: qh75, Yuwen Cai: yc687, Yitian Lin: yl698"


@irsystem.route('/', methods=['GET'])
def home():
    return render_template('search.html', genresData=json.dumps(get_genre_list()), moviesData=json.dumps(get_movie_list()))

@irsystem.route('/search', methods=['GET'])
def search():
    return redirect(url_for('irsystem.home'))

@irsystem.route('/search-run', methods=['POST'])
def search_action():
    tags = json.loads(request.form.get('gameTags')) if request.form.get('gameTags') else []
    movie = request.form.get('movieEnjoy') if request.form.get('movieEnjoy') else None
    genres = json.loads(request.form.get('gameGenre')) if request.form.get('gameGenre') else [] # TODO: add it to response
    response_body = {
        "based on keywords": str(match_tags_and_movie(tags, movie)),
        "based on titles": str(get_top_games_from_title(movie))
    }
    return Response(json.dumps(response_body))
