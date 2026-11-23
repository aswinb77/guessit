import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Game

def index(request):
    return render(request, 'game/index.html')

def api_me(request):
    return JsonResponse({'name': request.session.get('player_name')})

@require_POST
def api_set_name(request):
    try:
        name = str(json.loads(request.body).get('name', '')).strip()[:20]
    except (json.JSONDecodeError, AttributeError):
        name = ''
    if not name:
        return JsonResponse({'error': 'Please enter a name'}, status=400)
    request.session['player_name'] = name
    return JsonResponse({'name': name})

@require_POST
def api_new(request):
    name = request.session.get('player_name')
    if not name:
        return JsonResponse({'error': 'Set a name first'}, status=400)
    game = Game.objects.create(player=name)
    request.session['game_id'] = game.id          
    return JsonResponse({'game_id': game.id, 'lives': game.lives})

@require_POST
def api_guess(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.session.get('game_id') != game.id:
        return JsonResponse({'error': 'This is not your game'}, status=403)
    if game.finished:
        return JsonResponse({'error': 'This game is already over'}, status=400)

    try:
        guess = int(json.loads(request.body).get('guess'))
    except (TypeError, ValueError, AttributeError, json.JSONDecodeError):
        return JsonResponse({'error': 'Enter a valid number'}, status=400)
    if not 1 <= guess <= 100:
        return JsonResponse({'error': 'Pick a number from 1 to 100'}, status=400)

    game.attempts += 1
    hint = None
    if guess == game.secret:
        result = 'correct'
        game.won = True
        game.finished = True
    else:
        hint = 'higher' if guess < game.secret else 'lower'
        game.lives -= 1
        if game.lives <= 0:
            result = 'lost'
            game.finished = True
        else:
            result = 'wrong'
    game.save()

    data = {'result': result, 'hint': hint, 'attempts': game.attempts, 'lives': game.lives}
    if game.finished:
        data['secret'] = game.secret     # only revealed once the game is over
    return JsonResponse(data)

def api_leaderboard(request):
    games = Game.objects.filter(won=True).order_by('attempts', 'created')[:10]
    return JsonResponse({'games': [{'player': g.player, 'attempts': g.attempts} for g in games]})