import requests
import json
import pandas as pd
import numpy as np
from difflib import SequenceMatcher

def fetch_data(start_date, end_date):

    datasets_list= []
    time_interval = '[' + start_date + ' TO ' + end_date + ']'

    for i in [0,1000,2000,3000,4000]:
        endpoint_packages = 'https://datenregister.berlin.de/api/action/package_search?q=date_released:' + time_interval + ' OR date_updated:' + time_interval + '&rows=1000&start=' + str(i)
        # make the http request get
        response = requests.get(endpoint_packages)

        #use the json module to load CKAN's response into dictionary
        packages_dict = json.loads(response.content)
        
        datasets_list.extend(packages_dict['result']['results'])
    return datasets_list
    

def extract_columns(datasets_list):
    #extract titles, ids, notes, authors, source, date, contact, resource link
    titles, ids, notes, author, source, contact, resource, geographical_granularity, date_released, date_updated = [], [], [], [], [], [], [], [], [], []
    for i in range(0, len(datasets_list)):
        titles.append(datasets_list[i]['title'])
        ids.append(datasets_list[i]['id'])
        notes.append(datasets_list[i]['notes'])
        author.append(datasets_list[i]['author'])
        source.append(datasets_list[i]['berlin_source'])
        contact.append(datasets_list[i]['maintainer_email'])
        date_released.append(datasets_list[i]['date_released'])
        try:
            date_updated.append(datasets_list[i]['date_updated'])
        except:
            date_updated.append('Erstveröffentlichung')
        try:
            if datasets_list[i]['geographical_granularity'] != "Berlin":
                geographical_granularity.append(datasets_list[i]['geographical_granularity'])
            else:
                geographical_granularity.append('?')
        except:
            geographical_granularity.append('?')
        for j in range(0,datasets_list[i]['num_resources']):  #get url of first resource that is not html
            if datasets_list[i]['resources'][j]['format'] != 'HTML' and datasets_list[i]['resources'][j]['url'] != '':
                resource.append(datasets_list[i]['resources'][j]['url'])
                break

    #extract formats as lists in dicts with dataset id
    formats = {}
    for i in range(0, len(datasets_list)):
        id = datasets_list[i]['id']
        formats_per_id = []
        for j in range (0,datasets_list[i]['num_resources']):
            try:
                formats_per_id.append(datasets_list[i]['resources'][j]['format'])
            except: #if format is missing
                pass
        formats[id] = formats_per_id
    #save formats in dataframes
    formats_df = pd.DataFrame({'formats':formats})
    formats_df['formats']= formats_df['formats'].astype('string')
    formats_df.reset_index(inplace = True)
    formats_df.rename(columns = {'index':'id'}, inplace = True)

    #combine lists in one list
    zipped = list(zip(titles, notes, ids, author, source, contact, resource, geographical_granularity, date_released, date_updated))

    #combine lists in a dataframe
    datasets_df = pd.DataFrame(zipped, columns=['Titel', 'Beschreibung', 'id', 'Herausgeber:in', 'source', 'Kontakt', 'Link zu einer Ressource', 'Raumbezug', "Erstveröffentlichung", "Aktualisierung"])

    #join with formats_df
    datasets_df = pd.merge(datasets_df, formats_df, on='id', how="outer")

    datasets_df['Geoformat'] = ""

    # check formats for geodata formats
    geoformats = ["wms","wfs","geojson","geo","shp","shape","gjson","kml","kmz","gtfs","gpx"]
    # if a geoformat is included, name them in new column 'geoformat'
    for index, row in datasets_df.iterrows(): #iterate through rows
        existing_geoformats = "" #empty string for existing geoformats
        for f in geoformats: #iterate through geoformats list
            if f in datasets_df.loc[index, 'formats'].lower():
                if existing_geoformats == "": #when it's the first one
                    existing_geoformats = str(f)
                else:
                    existing_geoformats = str(existing_geoformats) +", " + str(f)
        if existing_geoformats == "":
            existing_geoformats = "keines"
        datasets_df.loc[index,'Geoformat'] = existing_geoformats

    return datasets_df

def filter_data(datasets_df, tags_include, tags_exclude, fisbroker_check, gsi_check):
    #filter for datasets not from fisbroker
    if fisbroker_check == False:
        datasets_df = datasets_df[datasets_df['source'].str.contains('fisbroker', case=False) == False]
    
    #filter for datasets not from gsi
    if gsi_check == False:
        datasets_df = datasets_df[datasets_df['source'].str.contains('api-senges', case=False) == False]

    #filter for potential geodata with keywords
    # define keywords to include datasets
    tags_include = tags_include.replace('\r', '').replace('\n', '')
    tags_include = tags_include.replace(",", "|")
    keywords_geodata = tags_include.replace(" ", "")
    # check for keywords in title and notes and add boolean values to dataframe in new columns
    datasets_df['title_incl'] = pd.Series(datasets_df['Titel'].str.contains(keywords_geodata, case=False))
    datasets_df['notes_incl'] = pd.Series(datasets_df['Beschreibung'].str.contains(keywords_geodata, case=False))
    #filter for datasets with potential geodata
    datasets_df = datasets_df[(datasets_df['title_incl'] == True) | (datasets_df.notes_incl == True)]

    keywords_raumbezug = 'keine'
    # check for keywords in title and notes and add boolean values to dataframe in new columns
    datasets_df['raumbezug_excl'] = pd.Series(datasets_df['Raumbezug'].str.contains(keywords_raumbezug, case=False))
    #filter for datasets with potential geodata
    datasets_df = datasets_df[(datasets_df['raumbezug_excl'] == False)]


    # define keywords to exclude datasets
    if tags_exclude:
        tags_exclude = tags_exclude.replace('\r', '').replace('\n', '')
        tags_exclude = tags_exclude.replace(",", "|")
        keywords_exclude = tags_exclude.replace(" ", "")
        # check for keywords in title and notes and add boolean values to dataframe in new columns
        datasets_df['title_exclude'] = pd.Series(datasets_df['Titel'].str.contains(keywords_exclude, case=False))
        datasets_df['notes_exclude'] = pd.Series(datasets_df['Beschreibung'].str.contains(keywords_exclude, case=False))
        #filter for datasets with potential geodata
        datasets_df = datasets_df[(datasets_df['title_exclude'] == False) | (datasets_df.notes_exclude == False)]
        datasets_df = datasets_df.drop(['title_exclude', 'notes_exclude'], axis = 1)

    #drop columns
    datasets_df = datasets_df.drop(['title_incl', 'notes_incl','source', 'id', 'formats'], axis = 1)

    return datasets_df


def enrich_data(filtered_df):

    # add link to search query
    filtered_df['Link zu Datensatzeintrag'] = 'https://daten.berlin.de/search/node/'+ filtered_df['Titel']
    filtered_df

    #automatically fill in values for geographische Verfügbarkeit
    #filtered_df.loc[filtered_df['Herausgeber:in'].str.contains('senatsverwaltung|senatskanzlei|lageso|amt|landesamt', case=False), 'geographische Verfügbarkeit'] = 'landesweit'
    filtered_df.loc[~filtered_df['Herausgeber:in'].str.contains('bezirk|steglitz-zehlendorf|marzahn-hellersdorf|treptow-köpenick|neukölln|pankow|mitte|lichtenberg|spandau|reinickendorf|tempelhof-schöneberg|charlottenburg-wilmersdorf|friedrichshain-kreuzberg', case=False), 'geographische Verfügbarkeit'] = 'landesweit'
    filtered_df.loc[filtered_df['Herausgeber:in'].str.contains('bezirk|steglitz-zehlendorf|marzahn-hellersdorf|treptow-köpenick|neukölln|pankow|mitte|lichtenberg|spandau|reinickendorf|tempelhof-schöneberg|charlottenburg-wilmersdorf|friedrichshain-kreuzberg', case=False), 'geographische Verfügbarkeit'] = 'Bezirk'
    filtered_df.loc[filtered_df['Titel'].str.contains('steglitz-zehlendorf|marzahn-hellersdorf|treptow-köpenick|neukölln|pankow|mitte|lichtenberg|spandau|reinickendorf|tempelhof-schöneberg|charlottenburg-wilmersdorf|friedrichshain-kreuzberg', case=False), 'geographische Verfügbarkeit'] = 'Bezirk'
   
    filtered_df.loc[filtered_df['Titel'].str.replace(" |-|zur|der|steglitz-zehlendorf|marzahn-hellersdorf|treptow-köpenick|neukölln|pankow|mitte|lichtenberg|spandau|reinickendorf|tempelhof-schöneberg|charlottenburg-wilmersdorf|friedrichshain-kreuzberg", "", case=False).duplicated(keep=False), 'geographische Verfügbarkeit'] = 'mehrere Bezirke'

    #filtered_df.loc[filtered_df['geographische Verfügbarkeit'].str.contains('Bezirk')] = 

    #add empty column Raumbezug
    #filtered_df['Raumbezug'] = ''

    #automatically fill in Maßnahme
    filtered_df.loc[filtered_df['Geoformat']==True, 'notwendige Maßnahme zur Geoformatierung'] = 'keine notwendig'


    #add empty column Priorisierung
    filtered_df['Priorisierung'] = 0

    def calc_prio(row):
        prio = 0
        if row['geographische Verfügbarkeit'] == 'landesweit':
            prio += 2
        elif row['geographische Verfügbarkeit'] == 'mehrere Bezirke':
            prio += 1
        else:
            prio += 0

        if row['Geoformat'] != 'keines':
            if row['Raumbezug'] != 'Bezirk' and row['Raumbezug'] != '?':
                prio += 3
            else:
                prio += 2
        else:
            if row['Raumbezug'] != 'Bezirk' and row['Raumbezug'] != '?':
                prio += 1
            else:
                prio += 0

        return prio
        
    filtered_df["Priorisierung"] = filtered_df.apply(calc_prio, axis=1)


    #add empty column Notes

    def fill_notizen(row):
        if row['geographische Verfügbarkeit'] != 'landesweit' and row['Raumbezug'] == 'Bezirk':
            return 'Achtung: Der Raumbezug scheint in den Metadaten nicht korrekt angegeben worden zu sein.'
        else: 
            return ''


    filtered_df['Notizen'] = filtered_df.apply(fill_notizen, axis=1)


    return filtered_df



def transform_to_json(enriched_df):
    
    result = enriched_df.to_json(orient="records")
    parsed = json.loads(result)

    return parsed