import requests
import json
import pandas as pd
import time
import numpy as np

def fetch_data(start_date, end_date):
    datasets_json= []
   # start_date = '2022-01-01'
   # end_date = 'NOW'
    time_interval = '[' + start_date + ' TO ' + end_date + ']'

    for i in [0,1000,2000,3000]:
        endpoint_packages = 'https://datenregister.berlin.de/api/action/package_search?q=date_released:' + time_interval + ' OR date_updated:' + time_interval + '&rows=1000&start=' + str(i)
        
        # make the http request get
        packages_information = requests.get(endpoint_packages)

        #use the json module to load CKAN's response into dictionary
        packages_dict = json.loads(packages_information.content)
        
        datasets_json.extend(packages_dict['result']['results'])

        return datasets_json

def extract_columns(datasets_json):
    #extract titles, ids, notes, authors, source, date, contact, resource link
    titles, ids, notes, author, source, contact, resource = [], [], [], [], [], [], []
    for i in range(0, len(datasets_json)):
        titles.append(datasets_json[i]['title'])
        ids.append(datasets_json[i]['id'])
        notes.append(datasets_json[i]['notes'])
        author.append(datasets_json[i]['author'])
        source.append(datasets_json[i]['berlin_source'])
        contact.append(datasets_json[i]['maintainer_email'])
        for j in range(0,datasets_json[i]['num_resources']):  #get url of first resource that is not html
            if datasets_json[i]['resources'][j]['format'] != 'HTML' and datasets_json[i]['resources'][j]['url'] != '':
                resource.append(datasets_json[i]['resources'][j]['url'])
                break

    #extract formats as lists in dicts with dataset id
    formats = {}
    for i in range(0, len(datasets_json)):
        id = datasets_json[i]['id']
        formats_per_id = []
        for j in range (0,datasets_json[i]['num_resources']):
            try:
                formats_per_id.append(datasets_json[i]['resources'][j]['format'])
            except: #if format is missing
                pass
        formats[id] = formats_per_id
    #save formats in dataframes
    formats_df = pd.DataFrame({'formats':formats})
    formats_df['formats']= formats_df['formats'].astype('string')
    formats_df.reset_index(inplace = True)
    formats_df.rename(columns = {'index':'id'}, inplace = True)

    #combine lists in one list
    zipped = list(zip(titles, notes, ids, author, source, contact, resource))

    #combine lists in a dataframe
    datasets_df = pd.DataFrame(zipped, columns=['Titel', 'Beschreibung', 'id', 'Herausgeber:in', 'source', 'Kontakt', 'Link zu einer Ressource'])

    #join with formats_df
    datasets_df = pd.merge(datasets_df, formats_df, on='id', how="outer")
    # check formats for geodata formats
    geoformats = 'wms|wfs|geo|shp|shape|gjson|kml|kmz|gtfs|gpx'
    # if a geoformat is included, add 'true' in new column 'geoformat'
    datasets_df['Geoformat'] = pd.Series(datasets_df['formats'].str.contains(geoformats, case=False))

    return datasets_df

def filter_data(datasets_df):
    #filter for datasets not from fisbroker
    datasets_df = datasets_df[datasets_df['source'].str.contains('fisbroker', case=False) == False]

    #filter for potential geodata with keywords
    # define keywords to include datasets
    keywords_geodata = 'bezirk|ortsteil|planungsraum|prognoseraum|bezirksregion|lor|quartier|kiez\
    |stadtteil|bezirksgrenze|postleitzahl|wahlkreis|wahlbezirk|zelle|block|fläche|gebiet|grundstück\
    |gewässer|straße|flur|weg|linie|route|fluss|gebäude|liegenschaft|standort|station|einrichtung|stätte|spot\
    |adress|platz|stelle|wahllokal|zentrum|bau'
    # check for keywords in title and notes and add boolean values to dataframe in new columns
    datasets_df['title_incl'] = pd.Series(datasets_df['Titel'].str.contains(keywords_geodata, case=False))
    datasets_df['notes_incl'] = pd.Series(datasets_df['Beschreibung'].str.contains(keywords_geodata, case=False))
    #filter for datasets with potential geodata
    datasets_df = datasets_df[(datasets_df['title_incl'] == True) | (datasets_df.notes_incl == True)]

    #drop columns
    datasets_df = datasets_df.drop(['title_incl', 'notes_incl','source', 'id', 'formats'], axis = 1)

    return datasets_df


def enrich_data(filtered_df):

    # add link to search query
    filtered_df['Link zu Datensatzeintrag'] = 'https://daten.berlin.de/search/node/'+ filtered_df['Titel']
    filtered_df

    #automatically fill in values for geographische Verfügbarkeit
    filtered_df.loc[filtered_df['Herausgeber:in'].str.contains('senatsverwaltung|senatskanzlei|lageso|amt für statistik', case=False), 'geographische Verfügbarkeit'] = 'landesweit'
    filtered_df.loc[filtered_df['Herausgeber:in'].str.contains('bezirk', case=False), 'geographische Verfügbarkeit'] = 'Bezirk'

    #add empty column Raumbezug
    filtered_df['Raumbezug'] = ''

    #automatically fill in Maßnahme
    filtered_df.loc[filtered_df['Geoformat']==True, 'notwendige Maßnahme zur Geoformatierung'] = 'na'


    #add empty column Priorisierung
    filtered_df['Priorisierung'] = ''

    return filtered_df



def transform_to_json(enriched_df):
    
    result = enriched_df.to_json(orient="records")
    parsed = json.loads(result)
    print(parsed)

    return parsed