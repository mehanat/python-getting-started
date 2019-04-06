from django.shortcuts import render
from django.http import HttpResponse
import json
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

TOKEN = "777893642:AAG3I_qD-yLxWHKdJzzOaua_CwFh5k6G4ME"
TelegramBot = telepot.Bot(TOKEN)
TelegramBot.setWebhook('https://mehanat-django.herokuapp.com/bot/'.format(bot_token=TOKEN))

# Create your views here.
def index(request):
    return HttpResponse('ok')

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    TelegramBot.answerCallbackQuery(query_id, text='Got it')

class CommandReceiveView(View):

    def post(self, request):
        print(request.body)
        payloadStr = request.body.decode('utf-8')
        payload = json.loads(payloadStr)

        if payloadStr.contains('callback_query'):
            chat_id = payload['callback_query']['message']['chat']['id']
            message = payload['callback_query']['data']
            TelegramBot.sendMessage(chat_id, f"Вы нажали кнопку `{message}`")
        else:

            chat_id = payload['message']['chat']['id']
            message = payload['message'].get('text')
            print(message)

            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Button1', callback_data='press1')],
                [InlineKeyboardButton(text='Button2', callback_data='press2')],
            ])
            TelegramBot.sendMessage(chat_id, 'Нажми кнопку', reply_markup=keyboard)
        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)