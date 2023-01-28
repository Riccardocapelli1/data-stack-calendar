import tweepy
import pandas as pd
import os
import re
from datetime import datetime
import dateutil.parser as parser
import requests
import csv

# Replace these with your own API keys and secrets
auth = tweepy.OAuthHandler(os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"])
auth.set_access_token(os.environ["ACCESS_TOKEN"], os.environ["ACCESS_TOKEN_SECRET"])
api = tweepy.API(auth, wait_on_rate_limit=True)

#api by countapi
countapiID = os.environ['COUNTAPI_TOKEN']
countapi_workspace = "riccardocapelli1.github.io"
countapilink = "http://api.countapi.xyz/hit/"+ countapi_workspace +"/"+ countapiID +"?callback=websiteVisits"
countapi = countapilink.replace(countapilink,f'<script async src="{countapilink}"></script>')

#df Crea una lista dei profili di cui vuoi scaricare i tweet
profiles = ["AirbyteHQ","ApacheAirflow","ApacheArrow","ApacheCalcite","ApacheFlink","apachekafka","apachenifi","ApacheParquet","ApachePinot","astronomerio","awscloud","Azure","Azure_Synapse","census","ClickHouseDB","code","confluentinc","dagster","dask_dev","databricks","dataddo","datafoldcom","datameer","dbt_labs","DeepMind","DeltaLakeOSS","Docker","druidio","duckdb","duckdblabs","elastic","expectgreatdata","fastdotai","fivetran","getdbt","github","gitlab","googlecloud","grafana","HevoData","HightouchData","IBMData","Integrateio","keboola","ksqlDB","kubernetesio","lightdash_devs","mage_ai","mariadb","Materialize","meltanodata","Metabase","MicroStrategy","moderndatastack","motherduck","montecarlodata","MSPowerBI","myadverity","MySQL","MuleSoft","numpy_team","pandas_dev","PyData","PostgreSQL","ProjectJupyter","PrefectIO","preset_data","prestodb","qlik","RiveryData","SASsoftware","ScyllaDB","SkyviaService","singer_io","SnowflakeDB","SQLServer","Supermetrics","tableau","Talend","Teradata","thecubejs","thoughtspot","trinodb","y42dotcom","Workato"]

#df2 definire le keyword da cercare
keywords = ["CERTIFICATION", "CONFERENCE", "COURSE", "EVENT", "PODCAST", "TRAINING"]

# Crea una lista vuota per i tweet
tweets = []

# Scarica i tweet dei profili specificati
for profile in profiles:
    for tweet in api.user_timeline(screen_name=profile, count=300, include_rts=False, tweet_mode="extended"):
        tweets.append([tweet.created_at, tweet.user.screen_name, tweet.full_text])

# Crea un dataframe dei tweet scaricati
df = pd.DataFrame(tweets, columns=['Time', 'User', 'Tweet'])

#df Mappa la lista dei profili di cui vuoi scaricare i tweet
profiles_map = {"AirbyteHQ":"Airbyte","ApacheAirflow":"Apache Airflow","ApacheArrow":"Apache Arrow","ApacheCalcite":"Apache Calcite","ApacheFlink":"Apache Flink","apachekafka":"Apache Kafka","apachenifi":"Apache Nifi","ApacheParquet":"Apache Parquet","ApachePinot":"Apache Pinot","astronomerio":"Astronomer.io","awscloud":"AWS Cloud","Azure":"Azure","Azure_Synapse":"Azure Synapse","census":"Census","ClickHouseDB":"ClickHouse","code":"Visual Studio Code","confluentinc":"Confluent.io","dagster":"Dagster","dask_dev":"Dask","databricks":"Databricks","dataddo":"Dataddo","datafoldcom":"Datafold","datameer":"Datameer","dbt_labs":"Dbt labs","DeepMind":"Deep Mind","DeltaLakeOSS":"Delta Lake","Docker":"Docker","druidio":"Druidio","duckdb":"Duck DB","duckdblabs":"Duck DB Labs","elastic":"Elastic","expectgreatdata":"Expect Great Data","fastdotai":"Fast.ai","fivetran":"Fivetran","getdbt":"Getdbt.com","github":"Github","gitlab":"Gitlab","googlecloud":"Google Cloud","grafana":"Grafana","HevoData":"Hevo Data","HightouchData":"Hightouch Data","IBMData":"IBM Data","Integrateio":"Integrate.io","keboola":"Keboola","ksqlDB":"Ksql","kubernetesio":"kubernetes.io","lightdash_devs":"Lightdash","mage_ai":"Mage.ai","mariadb":"Mariadb","Materialize":"Materialize","meltanodata":"Meltano","Metabase":"Metabase.com","MicroStrategy":"MicroStrategy","moderndatastack":"Moderndatastack.xyz","motherduck":"Motherduck","montecarlodata":"Montecarlo","MSPowerBI":"PowerBI","myadverity":"Myadverity","MySQL":"MySQL","MuleSoft":"MuleSoft","numpy_team":"Numpy","pandas_dev":"Pandas","PyData":"Py Spark","PostgreSQL":"PostgreSQL","ProjectJupyter":"Jupyter","PrefectIO":"Prefect.io","preset_data":"Preset","prestodb":"Presto DB","qlik":"Qlik","RiveryData":"Rivery","SASsoftware":"SAS","ScyllaDB":"Scylla DB","SkyviaService":"Skyvia","singer_io":"singer.io","SnowflakeDB":"Snowflake","SQLServer":"SQL Server","Supermetrics":"Supermetrics","tableau":"Tableau","Talend":"Talend","Teradata":"Teradata","thecubejs":"Cube.dev","thoughtspot":"Thoughtspot","trinodb":"Trino DB","y42dotcom":"Y42.com","Workato":"Workato"}

profiles_weblink = {"AirbyteHQ":"https://airbyte.io/","ApacheAirflow":"https://airflow.apache.org/ Airflow","ApacheArrow":"https://arrow.apache.org/ Arrow","ApacheCalcite":"https://calcite.apache.org/ Calcite","ApacheFlink":"https://flink.apache.org/ Flink","apachekafka":"https://kafka.apache.org/ Kafka","apachenifi":"https://nifi.apache.org/ Nifi","ApacheParquet":"https://parquet.apache.org/ Parquet","ApachePinot":"https://pinot.apache.org/ Pinot","astronomerio":"https://astronomer.io/.io","awscloud":"https://aws.amazon.com/ Cloud","Azure":"https://azure.com/","Azure_Synapse":"https://azure.com/synapse Synapse","census":"https://census.gov/","ClickHouseDB":"https://clickhouse.tech/","code":"https://code.visualstudio.com/ Studio Code","confluentinc":"https://confluent.io/","dagster":"https://dagster.io/","dask_dev":"https://dask.org/","databricks":"https://databricks.com/","dataddo":"https://dataddo.com/","datafoldcom":"https://datafold.com/","datameer":"https://datameer.com/","dbt_labs":"https://getdbt.com/ labs","DeepMind":"https://deepmind.com/ Mind","DeltaLakeOSS":"https://deltalake.io/ Lake","Docker":"https://docker.com/","druidio":"https://druid.io/","duckdb":"https://duckdb.org/ DB","duckdblabs":"https://duckdb.org/ DB Labs","elastic":"https://elastic.co/","expectgreatdata":"https://expectgreatdata.com/ Great Data","fastdotai":"https://fast.ai","fivetran":"https://fivetran.com/","getdbt":"https://getdbt.com","github":"https://github.com/","gitlab":"https://gitlab.com/","googlecloud":"https://cloud.google.com/ Cloud","grafana":"https://grafana.com/","HevoData":"https://hevodata.com/ Data","HightouchData":"https://hightouchdata.com/ Data","IBMData":"https://ibm.com/analytics/data-science Data","Integrateio":"https://integrate.io","keboola":"https://keboola.com/","ksqlDB":"https://confluent.io/ksql/","kubernetesio":"https://kubernetes.io","lightdash_devs":"https://lightdash.dev/","mage_ai":"https://mage.ai","mariadb":"https://mariadb.org/","Materialize":"https://materialize.com/","meltanodata":"https://meltano.com/","Metabase":"https://metabase.com/","MicroStrategy":"https://microstrategy.com/","moderndatastack":"https://moderndatastack.xyz","motherduck":"https://motherduck.io/","montecarlodata":"https://montecarlodata.com/","MSPowerBI":"https://powerbi.microsoft.com/","myadverity":"https://myadverity.com/","MySQL":"https://mysql.com/","MuleSoft":"https://mulesoft.com/","numpy_team":"https://numpy.org/","pandas_dev":"https://pandas.pydata.org/","PyData":"https://spark.apache.org/ Spark","PostgreSQL":"https://postgresql.org/","ProjectJupyter":"https://jupyter.org/","PrefectIO":"https://prefect.io","preset_data":"https://preset.io/","prestodb":"https://prestodb.io/ DB","qlik":"https://qlik.com/","RiveryData":"https://rivery.io/","SASsoftware":"https://sas.com/","ScyllaDB":"https://scylladb.com/ DB","SkyviaService":"https://skyvia.com/","singer_io":"https://singer.io","SnowflakeDB":"https://snowflake.com/","SQLServer":"https://microsoft.com/en-us/sql-server/ Server","Supermetrics":"https://supermetrics.com/","tableau":"https://tableau.com/","Talend":"https://talend.com/","Teradata":"https://teradata.com/","thecubejs":"https://cube.dev","thoughtspot":"https://thoughtspot.com/","trinodb":"https://trino.io/ DB","y42dotcom":"https://y42.com","Workato":"https://workato.com/"}

profiles_twitter = {"AirbyteHQ":"https://twitter.com/AirbyteHQ","ApacheAirflow":"https://twitter.com/ApacheAirflow Airflow","ApacheArrow":"https://twitter.com/ApacheArrow Arrow","ApacheCalcite":"https://twitter.com/ApacheCalcite Calcite","ApacheFlink":"https://twitter.com/ApacheFlink Flink","apachekafka":"https://twitter.com/apachekafka Kafka","apachenifi":"https://twitter.com/apachenifi Nifi","ApacheParquet":"https://twitter.com/ApacheParquet Parquet","ApachePinot":"https://twitter.com/ApachePinot Pinot","astronomerio":"https://twitter.com/astronomerio","awscloud":"https://twitter.com/awscloud Cloud","Azure":"https://twitter.com/Azure","Azure_Synapse":"https://twitter.com/Azure_Synapse Synapse","census":"https://twitter.com/census","ClickHouseDB":"https://twitter.com/ClickHouseDB","code":"https://twitter.com/code Studio Code","confluentinc":"https://twitter.com/confluentinc","dagster":"https://twitter.com/dagster","dask_dev":"https://twitter.com/dask_dev","databricks":"https://twitter.com/databricks","dataddo":"https://twitter.com/dataddo","datafoldcom":"https://twitter.com/datafoldcom","datameer":"https://twitter.com/datameer","dbt_labs":"https://twitter.com/dbt_labs labs","DeepMind":"https://twitter.com/DeepMind Mind","DeltaLakeOSS":"https://twitter.com/DeltaLakeOSS Lake","Docker":"https://twitter.com/Docker","druidio":"https://twitter.com/druidio","duckdb":"https://twitter.com/duckdb DB","duckdblabs":"https://twitter.com/duckdblabs DB Labs","elastic":"https://twitter.com/elastic","expectgreatdata":"https://twitter.com/expectgreatdata Great Data","fastdotai":"https://twitter.com/fastdotai","fivetran":"https://twitter.com/fivetran","getdbt":"https://twitter.com/getdbt.com","github":"https://twitter.com/github","gitlab":"https://twitter.com/gitlab","googlecloud":"https://twitter.com/googlecloud Cloud","grafana":"https://twitter.com/grafana","HevoData":"https://twitter.com/HevoData Data","HightouchData":"https://twitter.com/HightouchData Data","IBMData":"https://twitter.com/IBMData Data","Integrateio":"https://twitter.com/Integrateio","keboola":"https://twitter.com/keboola","ksqlDB":"https://twitter.com/ksqlDB","kubernetesio":"https://twitter.com/kubernetesio","lightdash_devs":"https://twitter.com/lightdash_devs","mage_ai":"https://twitter.com/mage_ai","mariadb":"https://twitter.com/mariadb","Materialize":"https://twitter.com/Materialize","meltanodata":"https://twitter.com/meltanodata","Metabase":"https://twitter.com/Metabase","MicroStrategy":"https://twitter.com/MicroStrategy","moderndatastack":"https://twitter.com/moderndatastack.xyz","motherduck":"https://twitter.com/motherduck","montecarlodata":"https://twitter.com/montecarlodata","MSPowerBI":"https://twitter.com/MSPowerBI","myadverity":"https://twitter.com/myadverity","MySQL":"https://twitter.com/MySQL","MuleSoft":"https://twitter.com/MuleSoft","numpy_team":"https://twitter.com/numpy_team","pandas_dev":"https://twitter.com/pandas_dev","PyData":"https://twitter.com/PyData Spark","PostgreSQL":"https://twitter.com/PostgreSQL","ProjectJupyter":"https://twitter.com/ProjectJupyter","PrefectIO":"https://twitter.com/PrefectIO","preset_data":"https://twitter.com/preset_data","prestodb":"https://twitter.com/prestodb DB","qlik":"https://twitter.com/qlik","RiveryData":"https://twitter.com/RiveryData","SASsoftware":"https://twitter.com/SASsoftware","ScyllaDB":"https://twitter.com/ScyllaDB DB","SkyviaService":"https://twitter.com/SkyviaService","singer_io":"https://twitter.com/singer_io","SnowflakeDB":"https://twitter.com/SnowflakeDB","SQLServer":"https://twitter.com/SQLServer Server","Supermetrics":"https://twitter.com/Supermetrics","tableau":"https://twitter.com/tableau","Talend":"https://twitter.com/Talend","Teradata":"https://twitter.com/Teradata","thecubejs":"https://twitter.com/thecubejs.dev","thoughtspot":"https://twitter.com/thoughtspot","trinodb":"https://twitter.com/trinodb DB","y42dotcom":"https://twitter.com/y42dotcom","Workato":"https://twitter.com/Workato"}

#Create mapping for display name, official website and twitter profile page
df["Profile"] = df["User"].map(profiles_map)
df["Profile_web"] = df["User"].map(profiles_weblink)
df["Profile_twi"] = df["User"].map(profiles_twitter)

#Conversione della colonna Time
df['Time'] = pd.to_datetime(df['Time'], format='%Y-%m-%d %H:%M:%S').apply(lambda x: 'Posted on: ' + x.strftime('%Y-%m-%d') + '; at: ' + x.strftime('%H:%M'))

#Conversione della colonna User
df["User"] = df["User"].str.upper()

# Filtra il dataframe per i tweet che contengono le parole "event" o "conference" nel testo
df = df[df['Tweet'].str.contains('Event|event|Conference|conference|Podcast|podcast|Badge|badge|Certific|certific|Webinar|webinar|free resources|free courses|free learning')]
df = df[~df['Tweet'].str.contains('Of courses|of courses|event log|Event log|Steven|steven|Prevent|prevent|Event streaming|event streaming|SSL certificate|GhEvent|EventTimer')]

# creare una copia del dataframe
df2 = df.copy()

# aggiungere una colonna "keyword" vuota
df2['keyword' ] = ""

# aggiungere una colonna "date" con la data e ora attuali
df2['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ciclo for per verificare se una stringa contiene una parola chiave
df2['Tweet'] = df2['Tweet'].str.upper()
for index, row in df2.iterrows():
    Tweet = row['Tweet']
    for keyword in keywords:
        if keyword in Tweet:
            df2.at[index, "keyword"] = keyword
            break

# eliminare righe senza keyword
df2 = df2[df2['keyword'] != ""]

# raggruppare i dati per data e keyword e contare le occorrenze
df2 = df2.groupby(['date', 'keyword']).size().reset_index(name='occurrence')

# salvare i dati in un file csv
df2.to_csv("tweet_data.csv", mode='a', header=False, index=False)

# Leggi i dati dal file CSV
columns=['date', 'keyword','occurrence'] 
df3 = pd.read_csv('tweet_data.csv', names=columns, header=None)

df3['date'] = pd.to_datetime(df3['date'])
df3['year_month'] = df3['date'].dt.to_period('M')
df3_grouped = df3.groupby(['year_month','keyword']).agg({'occurrence': 'max'}).reset_index()

###
# Crea una stringa vuota per i dati del grafico
chart_data = ""

# Ciclo for per generare i dati del grafico per ogni keyword
for keyword in df3_grouped["keyword"].unique():
    keyword_data = df3_grouped[df3_grouped["keyword"] == keyword]
    chart_data += f"{{ label: '{keyword}', data: ["
    for index, row in keyword_data.iterrows():
        chart_data += f"{{x: '{row['year_month']}', y: {row['occurrence']}}},"
    chart_data = chart_data[:-1] # Rimuovi l'ultima virgola
    chart_data += "]},\n"

# Rimuovi l'ultima virgola e newline dai dati del grafico
chart_data = chart_data[:-2]
###
googleapi = "https://fonts.googleapis.com/css?family=Inconsolata|Roboto"
googleapi = googleapi.replace(googleapi,f'<link href="{googleapi}" rel="stylesheet" >')

# crea contenuto html principale
def make_link(text):
    # Cerca tutte le occorrenze di link nella stringa
    links = re.findall(r'(https?:\/\/\S+)', text)
    # Sostituisci ogni occorrenza di link con il link cliccabile
    for link in links:
        text = text.replace(link, f'<a href="{link}">{link}</a>')
    return text

# Crea una stringa vuota per il contenuto del file HTML
html_content = ""

# Aggiungi il contenuto iniziale del file HTML
html_content  = "<!DOCTYPE html>\n"
html_content += "<html>\n"
html_content += "<head>\n"
html_content += googleapi + "\n"
html_content += "  " + countapi + "\n"
html_content += "  <meta charset='utf-8'>\n"
html_content += "  <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=yes'>\n"
html_content += "  <link rel='stylesheet' type='text/css' href='assets/style.css'>\n"
html_content += "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
html_content += "  <script src='assets/script.js'></script>\n"
html_content += "  <script src='assets/load.js'></script>\n"
html_content += "  <title>Hacked-data-stack intel for the data and analytics communities</title>\n"

# Titolo all'html_content
html_content += "  <h1>Events, conferences, podcast and training list up-to-date</h1>\n"
html_content += "  <p>A tweet aggregator site dysplaying events, conferences, podcast, certification and courses links that can be useful for data practitioners of all kinds. Hope you enjoy ;) </p>\n"

# Aggiungi il codice per il grafico all'html_content
html_content += "<div class='container'>\n"
html_content += "<canvas id='myChart'></canvas>\n"
html_content += "</div>\n"
html_content += "  <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>\n"
html_content += "<script>\n"
html_content += "var ctx = document.getElementById('myChart').getContext('2d');\n"
html_content += "var myChart = new Chart(ctx, {\n"
html_content += "  type: 'line',\n"
html_content += "  data: {\n"
html_content += "    datasets: [\n"
html_content += chart_data + "\n"
html_content += "    ]\n"
html_content += "  },\n"
html_content += "  options: {\n"
html_content += "    scales: {\n"
html_content += "      xAxes: [{\n"
html_content += "        type: 'time',\n"
html_content += "        time: {\n"
html_content += "           unit: 'month',\n"
html_content += "           displayFormats: {\n"
html_content += "            month: 'YYYY-MM'\n"
html_content += "           }\n"
html_content += "        }\n"
html_content += "      }],\n"
html_content += "      yAxes: [{\n"
html_content += "        ticks: {\n"
html_content += "          beginAtZero: true\n"
html_content += "        }\n"
html_content += "      }]\n"
html_content += "    }\n"
html_content += "  }\n"
html_content += "});\n"
html_content += "</script>\n"
html_content += "  <p>Aggregated kewords tweeted stats by month</p>\n"


html_content += "</head>\n"
html_content += "<body>\n"

#, Crea un dizionario vuoto per gli utenti
users_dict = {}

# Utilizza un ciclo for per aggiungere gli utenti al dizionario e tenere traccia della loro posizione nell'HTML
pos = 0
for _, row in df.iterrows():
    user = row["Profile"]
    if user not in users_dict:
        users_dict[user] = pos
        pos += 1

# Utilizza un ciclo for per creare un elenco di link agli utenti nell'HTML
html_content += "  <h3>List of Authors</h3>\n"
html_content += "  <ul>\n"
for user in users_dict:
    html_content += f"    <li><a href='#user{users_dict[user]}'>{user}</a></li>\n"
html_content += "  </ul>\n"

# Utilizza un ciclo for per iterare attraverso ogni riga del dataframe
current_user = df.iloc[0]["Profile"]
html_content += f"  <h2 class='h2' style='text-transform: uppercase;' id='user{users_dict[current_user]}'>{current_user} </h2><br><a href='{row['Profile_web']}'>Official website</a><br><a href='{row['Profile_twi']}'>Twitter profile</a>\n"

for _, row in df.iterrows():
    user = row["Profile"]
    if user != current_user:
        current_user = user
        
# Crea un'ancora per ogni utente nell'HTML
        html_content += f"  <h2 class='h2' style='text-transform: uppercase;' id='user{users_dict[user]}'>{user}</h2><br><a href='{row['Profile_web']}'>Official website</a><br><a href='{row['Profile_twi']}'>Twitter profile</a>\n"
    date = row["Time"]
    text = make_link(row["Tweet"])
    html_content += f" <h3 date='{date}'>{date}</h3>\n"
    html_content += f"  <p>{text}</p>\n"

html_content += "</body>\n"
html_content += "<footer>\n"
html_content += "  <p>Made with ❤️ for the community by Riccardo</p>\n"
html_content += "</footer>\n"
html_content += "</html>\n"

with open("./index.html", "w") as f:
    f.write(html_content)

# write countapi data in csv file
url = "https://api.countapi.xyz/get/"+ countapi_workspace +"/"+ countapiID +"/"
response = requests.get(url)
data = response.json()
value = data["value"]
now = datetime.now()

with open("countapi.csv", "a") as f:
    writer = csv.writer(f)
    writer.writerow([now, value])
    