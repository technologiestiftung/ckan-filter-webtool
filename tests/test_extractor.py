"""Test the modules in extractor."""

import pytest
import pandas as pd

import sys
from pathlib import Path
path = Path(__file__).parent.parent

print(path.resolve())
sys.path.append(path.resolve)

from utils import extractor

START_DATE = "2022-04-01"
END_DATE = "2022-05-27"
TAGS_INCLUDE = 'bezirk, ortsteil, planungsraum, prognoseraum, bezirksregion, lor, quartier, kiez, stadtteil, bezirksgrenze, postleitzahl, wahlkreis, wahlbezirk, zelle, block, fläche, gebiet, grundstück, gewässer, straße, flur, weg, linie, route, fluss, gebäude, liegenschaft, standort, station, einrichtung, stätte, spot, adress, platz, stelle, wahllokal, zentrum, bau'
    

@pytest.mark.parametrize(
    "start_date, end_date, expected_result", [
        (START_DATE, END_DATE, 1),
        (END_DATE, START_DATE, 0),
    ]
)
def test_fetch_data(start_date, end_date, expected_result):
    """Test the fetch data module."""
    result = extractor.fetch_data(start_date, end_date)
    assert len(result) >= expected_result # result should not be empty
    assert isinstance(result, list)

def test_extract_columns():
    """."""
    datasets_list = extractor.fetch_data(START_DATE, END_DATE)
    datasets_df = extractor.extract_columns(datasets_list)

    assert isinstance(datasets_df, pd.DataFrame)

    expected_headers = ['Titel', 'Beschreibung', 'id', 'Herausgeber:in', 'source', 'Kontakt', 'Link zu einer Ressource', 'formats', 'Geoformat']

    for expected_header in expected_headers:
        assert expected_header in datasets_df

    assert len(datasets_list) == len(datasets_df)

    
def test_filter_data():

    datasets_list = extractor.fetch_data(START_DATE, END_DATE)
    datasets_df = extractor.extract_columns(datasets_list)
    filtered_df = extractor.filter_data(datasets_df, TAGS_INCLUDE)

    expected_headers = ['Titel', 'Beschreibung', 'Herausgeber:in', 'Kontakt', 'Link zu einer Ressource', 'Geoformat']

    for expected_header in expected_headers:
        assert expected_header in datasets_df

    assert len(filtered_df) < len(datasets_df)
    assert len(filtered_df) > 0

def test_enrich_data():

    datasets_list = extractor.fetch_data(START_DATE, END_DATE)
    datasets_df = extractor.extract_columns(datasets_list)
    filtered_df = extractor.filter_data(datasets_df, TAGS_INCLUDE)
    enriched_df = extractor.enrich_data(filtered_df)

    expected_headers =  ['Titel', 'Beschreibung', 'Herausgeber:in', 'Kontakt', 'Link zu einer Ressource', 'Geoformat', 'Link zu Datensatzeintrag', 'geographische Verfügbarkeit', 'Raumbezug', 'notwendige Maßnahme zur Geoformatierung', 'Priorisierung', 'Notizen']

    for expected_header in expected_headers:
        assert expected_header in enriched_df

    assert len(filtered_df) > 0

def test_transform_to_json():

    datasets_list = extractor.fetch_data(START_DATE, END_DATE)
    datasets_df = extractor.extract_columns(datasets_list)
    filtered_df = extractor.filter_data(datasets_df, TAGS_INCLUDE)
    enriched_df = extractor.enrich_data(filtered_df)
    parsed = extractor.transform_to_json(enriched_df)

    expected_headers =  ['Titel', 'Beschreibung', 'Herausgeber:in', 'Kontakt', 'Link zu einer Ressource', 'Geoformat', 'Link zu Datensatzeintrag', 'geographische Verfügbarkeit', 'Raumbezug', 'notwendige Maßnahme zur Geoformatierung', 'Priorisierung', 'Notizen']
    for expected_header in expected_headers:
        assert expected_header in parsed[1]

    assert len(parsed) == len(filtered_df)