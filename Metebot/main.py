from decimal import *
import requests, json, random, datetime, asyncio
import discord
from discord.ext import commands, tasks
from datetime import datetime
import time

async def obtenir_meteo(ctx):
    # API key de OpenWeather
    api_key = "061e506eb621d872477330a8dae4cb76"

    # Variable du début de l'url d'api openweather
    urlDebut = "http://api.openweathermap.org/data/2.5/weather?"
    
    # Give city name
    city_name = "Toulon"
    
    #Variable de l'url complete: début d'url avec la API key et la ville
    urlComplete = urlDebut + "appid=" + api_key + "&q=" + city_name
    
    # initialisation de la variable response avec la requête de la variable urlComplete avec get method
    response = requests.get(urlComplete)
    
    # Valeur du json d'openweather converti en list
    listeMeteo = response.json()
    # listeMeteo contient la liste du fichier json récupéré
    # Si erreur "404", une erreur dans la variable listeMeteo(ici la ville n'a pas été trouvé)
    if listeMeteo["cod"] != "404":
        # initialise la variable info avec la partie 'main' du fichier json
        info = listeMeteo["main"]
        # initialise temperareActuelle avec la valeur de 'temp' situé dans 'main'
        temperature = info["temp"]
        # Convertie la valeur de temperature de kelvin en celsium
        temperature = temperature - 273.15

        # initialise humidite avec la valeur de 'humidity' situé dans 'main'
        humidite = info["humidity"]
    
        # récupére la liste de weather et l'initialise dans a
        a = listeMeteo["weather"]

        #Sélection des messages en fonction de l'id du temps(weather):
        # Thunderstorm/Tempête
        if 200 <= a[0]['id'] <= 232:
            # récupére la valeur de 'description', premiére valeur de la liste a et l'initialise dans meteo
            meteo = a[0]["description"]
            await ctx.send(f" Temperature actuelle = {str(round(temperature, 1))}C°")
            await ctx.send(f" Taux d'humiditée = {str(humidite)}%")
            await ctx.send(f" Météo = {str(meteo)}")
            await ctx.send(f" Bon courage ! ⛈️🚣‍♂️")
            
        # Drizzle/Cracha
        elif 300<= a[0]['id'] <= 321:
            meteo = a[0]["description"]
            await ctx.send(f" Temperature actuelle = {str(round(temperature, 1))}C°")
            await ctx.send(f" Taux d'humiditée = {str(humidite)}%")
            await ctx.send(f" Météo = {str(meteo)}")
            await ctx.send(f" Bienvenue au mois de Juillet en Bretagne 💁🏼‍♂️☔")
        
        # Rain/Pluie
        elif 500<= a[0]['id'] <= 521:
            meteo = a[0]["description"]
            await ctx.send(f" Temperature actuelle = {str(round(temperature, 1))}C°")
            await ctx.send(f" Taux d'humiditée = {str(humidite)}%")
            await ctx.send(f" Météo = {str(meteo)}")
            await ctx.send(f" Il pleut il mouille, c'est la fête à la grenouille 🌧️🐸🎶")
        
        # Snow/Neige (rêve pas t'en verra jamais à Toulon..)
        elif 600 <= a[0]['id'] <= 622:
            meteo = a[0]["description"]
            await ctx.send(f" Temperature actuelle = {str(round(temperature, 1))}C°")
            await ctx.send(f" Taux d'humiditée = {str(humidite)}%")
            await ctx.send(f" Météo = {str(meteo)}")
            await ctx.send(f" STOP! Neige à Toulon = Maison + Chocolat chaud 🌨️📺☕")
            
        # Clear/Dégagé
        elif a[0]['id'] == 800:
            meteo = a[0]["description"]
            await ctx.send(f" Temperature actuelle = {str(round(temperature, 1))}C°")
            await ctx.send(f" Taux d'humiditée = {str(humidite)}%")
            await ctx.send(f" Météo = {str(meteo)}")
            await ctx.send(f" Y'a du soleil et des nanas la lalala la la 🎶☀️💃🏻")
        
        # Clouds/Nuageux
        elif 801<= a[0]['id'] <= 804:
            meteo = a[0]["description"]
            await ctx.send(f" Temperature actuelle = {str(round(temperature, 1))}C°")
            await ctx.send(f" Taux d'humiditée = {str(humidite)}%")
            await ctx.send(f" Météo = {str(meteo)}")
            await ctx.send(f" Encore une journée pour rester devant l'ordi 💻⛅")
        
        elif 701 <= a[0]['id'] <= 781:
            #Mist/Fog/Smoke/Haze du brouillard quoi en gros
            if 701 <= a[0]['id'] <= 721 or a[0]['id'] == 741:
                meteo = a[0]["description"]
                await ctx.send(f" Temperature actuelle = {str(round(temperature, 1))}C°")
                await ctx.send(f" Taux d'humiditée = {str(humidite)}%")
                await ctx.send(f" Météo = {str(meteo)}")
                await ctx.send(f" La tête dans l'cul, l'cul dans l'brouillard 🌫️🎶")
             # Dust n Sand and Dust or Sand
            elif a[0]['id'] == 731 or 751 <= a[0]['id'] <= 761:
                meteo = a[0]["description"]
                await ctx.send(f" Temperature actuelle = {str(round(temperature, 1))}C°")
                await ctx.send(f" Taux d'humiditée = {str(humidite)}%")
                await ctx.send(f" Météo = {str(meteo)}")
                await ctx.send(f" Aujourd'hui c'est sirocco ! 💨🏜️")
            # Ash/Cendre
            elif a[0]['id'] == 762:
                meteo = a[0]["description"]
                await ctx.send(f" Temperature actuelle = {str(round(temperature, 1))}C°")
                await ctx.send(f" Taux d'humiditée = {str(humidite)}%")
                await ctx.send(f" Météo = {str(meteo)}")
                await ctx.send(f" Si un jour ce message s'affiche, il faut commencer à s'inquiéter 🌋")
            # Squall/Rafale
            elif a[0]['id'] == 771:
                meteo = a[0]["description"]
                await ctx.send(f" Temperature actuelle = {str(round(temperature, 1))}C°")
                await ctx.send(f" Taux d'humiditée = {str(humidite)}%")
                await ctx.send(f" Météo = {str(meteo)}")
                await ctx.send(f" Attention ça va souffler ! 🌬️💨")
            # Tornado
            elif a[0]['id'] == 781:
                meteo = a[0]["description"]
                await ctx.send(f" Temperature actuelle = {str(round(temperature, 1))}C°")
                await ctx.send(f" Taux d'humiditée = {str(humidite)}%")
                await ctx.send(f" Météo = {str(meteo)}")
                await ctx.send(f" Ca va secouer ! 🤸‍♂️🌪️")
