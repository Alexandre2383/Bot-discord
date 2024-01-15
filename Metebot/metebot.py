from decimal import *
import requests, json, random, datetime, asyncio
import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from decouple import config
import time

DISCORD_TOKEN = config('DISCORD_TOKEN')
OPENWEATHER_API_KEY = config('OPENWEATHER_API_KEY')
CHANNEL_ID = config('CHANNEL_ID')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

print("Bot script started")

class MeteoContainer:
    def __init__(self):
        self.message_to_send = "Aucune information disponible."

meteo_container = MeteoContainer()

# Fonction pour obtenir la météo
def obtenir_meteo_ville(ville="Toulon"):
    api_key = OPENWEATHER_API_KEY
    urlDebut = "http://api.openweathermap.org/data/2.5/weather?"
    urlComplete = urlDebut + "appid=" + api_key + "&q=" + ville
    response = requests.get(urlComplete)
    listeMeteo = response.json()

    if listeMeteo["cod"] != "404":
        info = listeMeteo["main"]
        temperature = info["temp"] - 273.15
        humidite = info["humidity"]
        a = listeMeteo["weather"]
        meteo = a[0]["description"]
        if 200 <= a[0]['id'] <= 232:
            # récupére la valeur de 'description', premiére valeur de la liste a et l'initialise dans meteo
            meteo = a[0]["description"]
            return f" Temperature actuelle = {str(round(temperature, 1))}C°\n Taux d'humidité = {str(humidite)}%\n Météo = {str(meteo)}\n Bon courage ! ⛈️🚣‍♂️"
                            
        # Drizzle/Cracha
        elif 300<= a[0]['id'] <= 321:
            meteo = a[0]["description"]
            return f" Temperature actuelle = {str(round(temperature, 1))}C°\n Taux d'humidité = {str(humidite)}%\n Météo = {str(meteo)}\n Bienvenue au mois de Juillet en Bretagne 💁🏼‍♂️☔"
                        
        # Rain/Pluie
        elif 500<= a[0]['id'] <= 521:
            meteo = a[0]["description"]
            return f" Temperature actuelle = {str(round(temperature, 1))}C°\n Taux d'humidité = {str(humidite)}%\n Météo = {str(meteo)}\n Il pleut il mouille, c'est la fête à la grenouille 🌧️🐸🎶"
                        
        # Snow/Neige (rêve pas t'en verra jamais à Toulon..)
        elif 600 <= a[0]['id'] <= 622:
            meteo = a[0]["description"]
            return f" Temperature actuelle = {str(round(temperature, 1))}C°\n Taux d'humidité = {str(humidite)}%\n Météo = {str(meteo)}\n STOP! Neige à {str(ville)} = Maison + Chocolat chaud 🌨️📺☕"
            
        # Clear/Dégagé
        elif a[0]['id'] == 800:
            meteo = a[0]["description"]
            return f" Temperature actuelle = {str(round(temperature, 1))}C°\n Taux d'humidité = {str(humidite)}%\n Météo = {str(meteo)}\n Y'a du soleil et des nanas la lalala la la 🎶☀️💃🏻"
        
        # Clouds/Nuageux
        elif 801<= a[0]['id'] <= 804:
            meteo = a[0]["description"]
            return f" Temperature actuelle = {str(round(temperature, 1))}C°\n Taux d'humidité = {str(humidite)}%\n Météo = {str(meteo)}\n Encore une journée pour rester devant l'ordi 💻⛅"
            
        elif 701 <= a[0]['id'] <= 781:
            #Mist/Fog/Smoke/Haze du brouillard quoi en gros
            if 701 <= a[0]['id'] <= 721 or a[0]['id'] == 741:
                meteo = a[0]["description"]
                return f" Temperature actuelle = {str(round(temperature, 1))}C°\n Taux d'humidité = {str(humidite)}%\n Météo = {str(meteo)}\n La tête dans l'cul, l'cul dans l'brouillard 🌫️🎶"
                
            # Dust n Sand and Dust or Sand
            elif a[0]['id'] == 731 or 751 <= a[0]['id'] <= 761:
                meteo = a[0]["description"]
                return f" Temperature actuelle = {str(round(temperature, 1))}C°\n Taux d'humidité = {str(humidite)}%\n Météo = {str(meteo)}\n Aujourd'hui c'est sirocco ! 💨🏜️"
                
            # Ash/Cendre
            elif a[0]['id'] == 762:
                meteo = a[0]["description"]
                return f" Temperature actuelle = {str(round(temperature, 1))}C°\n Taux d'humidité = {str(humidite)}%\n Météo = {str(meteo)}\n Si un jour ce message s'affiche, il faut commencer à s'inquiéter 🌋"

            # Squall/Rafale
            elif a[0]['id'] == 771:
                meteo = a[0]["description"]
                return f" Temperature actuelle = {str(round(temperature, 1))}C°\n Taux d'humidité = {str(humidite)}%\n Météo = {str(meteo)}\n Attention ça va souffler ! 🌬️💨"
            # Tornado
            elif a[0]['id'] == 781:
                meteo = a[0]["description"]
                return f" Temperature actuelle = {str(round(temperature, 1))}C°\n Taux d'humidité = {str(humidite)}%\n Météo = {str(meteo)}\n Ca va secouer ! 🤸‍♂️🌪️"
    else:
        return "Je ne connais pas cette ville."


target_hours = [8, 13]
# Décorateur de boucle: 1 fois par heure, vérifie si l'heure est == à celle de la variable target_hours
@tasks.loop(hours=1)
async def send_scheduled_message():
    now = datetime.now()
    current_hour = now.hour
    
    # Si l'heure actuelle correspond à l'une des heures définies
    if current_hour in target_hours:
        channel = bot.get_channel(CHANNEL_ID)
        message = obtenir_meteo_ville()
        meteo_container.message_to_send = message
        await channel.send(message)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    # Démarrer la tâche périodique une fois que le bot est prêt
    send_scheduled_message.start()

@bot.command(name='meteo')
async def meteo(ctx, *args):
    if args:
        ville = " ".join(args)
    else:
        ville = "Toulon"

    resultat = obtenir_meteo_ville(ville)
    await ctx.send(resultat)

bot.run(DISCORD_TOKEN)