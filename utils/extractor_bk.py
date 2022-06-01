import requests
import json
import pandas as pd


def get_data(schema_name):
    datasets= []
    for i in [0,1000,2000, 3000, 4000, 5000]:
        endpoint_packages = 'https://datenregister.berlin.de/api/action/package_search?rows=1000&start=' + str(i)

        # make the http request get
        packages_information = requests.get(endpoint_packages)

        #use the json module to load CKAN's response into dictionary
        packages_dict = json.loads(packages_information.content)
        datasets.extend(packages_dict['result']['results'])

    titles, ids, notes, author, source, date, author_contact, maintainer_contact = [], [], [], [], [], [], [], []

    for i in range(0, len(datasets)):
        titles.append(datasets[i]['title'])
        ids.append(datasets[i]['id'])
        notes.append(datasets[i]['notes'])
        author.append(datasets[i]['author'])
        source.append(datasets[i]['berlin_source'])
        author_contact.append(datasets[i]['author_email'])
        maintainer_contact.append(datasets[i]['maintainer_email'])
        try:
            date.append(datasets[i]['date_updated'])
        except: #wenn date_updated fehlt
            date.append(datasets[i]['date_released'])

    #extract tags as lists in dict with dataset id
    tags = {}
    for i in range(0, len(datasets)):
        id = datasets[i]['id']
        tags_per_id = []
        for j in range (0,200):
            try:
                tags_per_id.append(datasets[i]['tags'][j]['display_name'])
            except:
                pass
        tags[id] = tags_per_id

    #tags in dataframe
    tags_df = pd.DataFrame({'tags':tags})
    tags_df['tags'] = tags_df['tags'].astype('string')
    tags_df.reset_index(inplace = True)
    tags_df.rename(columns = {'index':'id'}, inplace = True)

    #extract formats as lists in dict with dataset id
    formats = {}
    for i in range(0, len(datasets)):
        id = datasets[i]['id']
        formats_per_id = []
        for j in range (0,datasets[i]['num_resources']):
            try:
                formats_per_id.append(datasets[i]['resources'][j]['format'])
            except: #wenn Formatangabe fehlt
                pass
        formats[id] = formats_per_id

    #format in dataframe
    formats_df = pd.DataFrame({'formats':formats})
    formats_df['formats'] = formats_df['formats'].astype('string')
    formats_df.reset_index(inplace = True)
    formats_df.rename(columns = {'index':'id'}, inplace = True)

    #extract categories as lists in dict with dataset id
    categories = {}
    for i in range(0, len(datasets)):
        id = datasets[i]['id']
        categories_per_id = []
        for j in range (0,10):
            try:
                categories_per_id.append(datasets[i]['groups'][j]['display_name'])
            except:
                pass
        categories[id] = categories_per_id

    #categories in dataframe
    categories_df = pd.DataFrame({'categories':categories})
    categories_df['categories'] = categories_df['categories'].astype('string')
    categories_df.reset_index(inplace = True)
    categories_df.rename(columns = {'index':'id'}, inplace = True)

    #combine lists in one list
    zipped = list(zip(titles, notes, ids, author, source, date, author_contact, maintainer_contact))

    #combine lists in a dataframe
    datasets_df = pd.DataFrame(zipped, columns=['title', 'notes', 'id', 'author', 'source', 'date', 'author_contact', 'maintainer_contact'])
    datasets_df.head()

    #join with tags_df and categories_df
    datasets_df = pd.merge(datasets_df, tags_df, on='id', how='outer')
    datasets_df = pd.merge(datasets_df, categories_df, on='id', how='outer')
    datasets_df = pd.merge(datasets_df, formats_df, on='id', how='outer')

    datasets_notfb_df = datasets_df[datasets_df['source'].str.contains('fisbroker', case=False) == False]

    keywords_geodata = 'bezirk|ortsteil|planungsraum|prognoseraum|bezirksregion|lor|quartier|kiez \
 |stadtteil|bezirksgrenze|postleitzahl|wahlkreis|wahlbezirk|zelle|block|fläche|gebiet|grundstück|\
 gewässer|straße|flur|weg|linie|route|fluss|gebäude|liegenschaft|standort|station|einrichtung|stätte|spot\
 |platz|stelle|wahllokal|zentrum|bau'


    # check for keywords in title and notes and add boolean values to dataframe in new columns
    datasets_notfb_df['title_incl'] = pd.Series(datasets_notfb_df['title'].str.contains(keywords_geodata, case=False))
    datasets_notfb_df['notes_incl'] = pd.Series(datasets_notfb_df['notes'].str.contains(keywords_geodata, case=False))

    potential_geodata_df = datasets_notfb_df
    potential_geodata_df = datasets_notfb_df[(potential_geodata_df['title_incl'] == True) | (potential_geodata_df.notes_incl == True)]

    #Anzahl der gefilterten Datensätze
    num_potential_geodata = (len(potential_geodata_df))

    potgeo_notsenges_df = potential_geodata_df[potential_geodata_df['source'].str.contains('senges', case=False) == False]

    years = '2020|2021|2022'

    #based on potential geodata not fisbroker and not senges
    potential_geodata_since2020_df = potgeo_notsenges_df[potgeo_notsenges_df['date'].str.contains(years)]

    # check formats for geodata formats
    geoformats = 'wms|wfs|geo|shp|shape|gjson'
    # check for keywords in title and notes and add boolean values to dataframe in new columns
    potential_geodata_since2020_df['geoformat'] = pd.Series(potential_geodata_since2020_df['formats'].str.contains(geoformats, case=False))

    #drop columns
    potential_geodata_since2020_df = potential_geodata_since2020_df.drop(['title_incl', 'notes_incl',], axis = 1)

    #potential_geodata_since2020_df = potential_geodata_since2020_df[["title","notes"]]

    result = potential_geodata_since2020_df.to_json(orient="records")
    parsed = json.loads(result)
    #print(result)
    return parsed
    #return datasets[int(schema_name)]
    #test = [{'id':1, 'name':"Oli Bob", 'progress':12, 'gender':"male", 'rating':1, 'col':"red", 'dob':"19/02/1984", 'car':1}]
        
    #return test

datasets_df = get_data(8)
#print(datasets_df)