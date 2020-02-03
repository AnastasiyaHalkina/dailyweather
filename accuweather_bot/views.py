import json
import telebot
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .weather import get_weather_12h, get_weather_1day

# Create your views here.

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)


def display_start(request):
    return render(request, template_name='start.html')


def display_help(request):
    return render(request, template_name='help.html')


def display_weather_12h(request):
    return render(request, 'weather_12h.html', {'values': get_weather_12h()})


def display_weather_1day(request):
    return render(request, 'weather_1day.html', {'values': get_weather_1day()})


@csrf_exempt
def command_view(request, bot_token):

    if bot_token != settings.TELEGRAM_BOT_TOKEN:
        return HttpResponseForbidden('Invalid token')

    commands = {
        '/start': display_start,
        '/help': display_help,
        '/weather12h': display_weather_12h,
        '/weather1d': display_weather_1day
    }

    raw = request.body.decode(encoding='utf-8')
    try:
        payload = json.loads(raw)
    except ValueError:
        return HttpResponseBadRequest('Invalid request body')
    else:
        chat_id = payload['message']['chat']['id']
        command = payload['message']['text']
        answer = commands.get(command.strip(" .,").split()[0].lower())
        if answer:
            bot.send_message(chat_id, answer(request), parse_mode='HTML')
        else:
            bot.send_message(chat_id, "Такой команды"
                                      " нет в списке команд."
                                      " Для справки обратитесь к /help")

    return JsonResponse({}, status=200)
