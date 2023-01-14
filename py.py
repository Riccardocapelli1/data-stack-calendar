import tweepy
import pandas as pd
import os
import re

# Replace these with your own API keys and secrets
auth = tweepy.OAuthHandler(os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"])
auth.set_access_token(os.environ["ACCESS_TOKEN"], os.environ["ACCESS_TOKEN_SECRET"])
api = tweepy.API(auth, wait_on_rate_limit=True)

# Crea una lista dei profili di cui vuoi scaricare i tweet
profiles = ["apachesuperset","ApacheAirflow","awscloud","AirbyteHQ","Azure","dagster","DataCouncilAI","getdbt","dbt_labs","expectgreatdata","googlecloud","lightdash_devs","tableau","Materialize","meltanodata","montecarlodata","MSPowerBI","PrefectIO","singer_io","SnowflakeDB","thoughtspot","OpenLineage"]

# Crea una lista vuota per i tweet
tweets = []

# Scarica i tweet dei profili specificati
for profile in profiles:
    for tweet in api.user_timeline(screen_name=profile, count=20, include_rts=False, tweet_mode="extended"):
        tweets.append([tweet.created_at, tweet.user.screen_name, tweet.full_text])

# Crea un dataframe dei tweet scaricati
df = pd.DataFrame(tweets, columns=['Time', 'User', 'Tweet'])

#Conversione della colonna Time
df['Time'] = pd.to_datetime(df['Time'], format='%Y-%m-%d %H:%M:%S').apply(lambda x: 'day: ' + x.strftime('%Y-%m-%d') + '; time: ' + x.strftime('%H:%M'))

# Filtra il dataframe per i tweet che contengono le parole "event" o "conference" nel testo
df = df[df['Tweet'].str.contains('event|conference')]


def make_link(text):
    # Cerca tutte le occorrenze di link nella stringa
    links = re.findall(r'(https?:\/\/\S+)', text)
    # Sostituisci ogni occorrenza di link con il link cliccabile
    for link in links:
        text = text.replace(link, f'<a href="{link}">{link}</a>')
    return text

# Filtra il dataframe per i tweet che contengono le parole "event" o "conference" nel testo
df = df[df['Tweet'].str.contains('event|conference')]

# Crea una stringa vuota per il contenuto del file HTML
html_content = ""

# Aggiungi il contenuto iniziale del file HTML
html_content  = "<!DOCTYPE html>\n"
html_content += "<html>\n"
html_content += "<head>\n"
html_content += "  <link rel='stylesheet' type='text/css' href='assets/style.css'>\n"
html_content += "  <script src='assets/script.js'></script>\n"
html_content += "  <title>Modern-data-stack events and conferences for the analytics community</title>\n"
html_content += "</head>\n"
html_content += "<body>\n"
html_content += "  <h1>Events and conferences list updated every 24H</h1>\n"
html_content += "  <p>A modern data stack calendar aggregating events and conferences from Twitter for data engineers, analytics engineers and data analysts.</p>\n"

current_user = df.iloc[0]["User"]
html_content += f"  <h2>{current_user}</h2>\n"

for _, row in df.iterrows():
        user = row["User"]
        
        if user != current_user:
            current_user = user
            html_content += f"  <h2 class='h2'>{current_user}</h2>\n"
        
        date = row["Time"]
        text = make_link(row["Tweet"])
        html_content += f" <h3 date='{date}'>{date}</h3>\n"
        html_content += f"  <p>{text}</p>\n"

html_content += "</body>\n"
html_content += "</html>\n"

with open("./index.html", "w") as f:
    f.write(html_content)
