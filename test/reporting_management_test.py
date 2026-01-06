"""A test file for reporting management functions"""
from unittest.mock import patch, Mock
import pytest
import numpy as np
import pandas as pd
import json
from py2adobe_reporting.cja_functions.reporting_management import Reporting
from py2adobe_reporting import utils as ut



def test_rows_per_page_setting():
    reporting = Reporting()
    result = reporting.rows_per_page_setting(5000)
    assert result == 5000


def test_dim_rows_per_page_setting():
    reporting = Reporting()
    result = reporting.dim_rows_per_page_setting(1000)
    assert result == 400

@pytest.fixture
def total_table_rows_response():
    return {'totalPages': 2,
 'firstPage': True,
 'lastPage': False,
 'numberOfElements': 1,
 'number': 0,
 'totalElements': 2,
 'columns': {'dimensions': [{'id': 'variables/_experience.analytics.customDimensions.eVars.eVarXX',
    'dimensionColumnId': '12345c590540d-9f30-4087-8563-eb138a352954',
    'type': 'string'}],
  'columnIds': ['0'],
  'dimension': {'id': 'variables/_experience.analytics.customDimensions.eVars.eVarXX',
   'dimensionColumnId': '12345c590540d-9f30-4087-8563-eb138a352954',
   'type': 'string'}},
 'rows': [{'itemIds': ['12345py2AdobeHashedId'],
   'values': ['12345py2AdobeHashedId'],
   'data': [842.0],
   'itemId': '12345py2AdobeHashedId',
   'value': '12345py2AdobeHashedId'}],
 'summaryData': {'filteredTotals': [1247.0],
  'annotations': [],
  'totals': [1247.0],
  'annotationExceptions': [],
  'col-max': [842.0],
  'col-min': [405.0]}}

@patch('py2AdobeReporting.cja_functions.reporting_management.HttpClient')
def test_get_total_table_rows(mock_http_client, total_table_rows_response):
    reporting = Reporting()
    mock_response = Mock()
    mock_response.text = json.dumps(total_table_rows_response) 
    mock_response.status_code = 200
    mock_http_client.return_value.post.return_value = mock_response

    headers = {"Authorization": "Bearer token"}
    body = {"settings": {"limit": 1}}

    res = reporting.get_total_table_rows(headers, body)
    assert res == 2
    assert isinstance(total_table_rows_response, dict)
    assert total_table_rows_response["totalElements"] == 2

@patch('py2AdobeReporting.cja_functions.reporting_management.HttpClient')
def test_get_total_table_pages(mock_http_client, total_table_rows_response):
    reporting = Reporting()
    mock_response = Mock()
    mock_response.text = json.dumps(total_table_rows_response) 
    mock_response.status_code = 200
    mock_http_client.return_value.post.return_value = mock_response

    headers = {"Authorization": "Bearer token"}
    body = {"settings": {"limit": 1}}
    
    res = reporting.get_total_table_pages(headers, body)
    assert res == 1
    assert isinstance(total_table_rows_response, dict)
    total_rows = total_table_rows_response["totalElements"]
    total_pages = int(np.ceil(total_rows/50000))
    assert total_pages == 1

@pytest.fixture
def monthly_time_series_response():
    return {'totalPages': 1,
 'firstPage': True,
 'lastPage': True,
 'numberOfElements': 2,
 'number': 0,
 'totalElements': 2,
 'columns': {'dimensions': [{'id': 'variables/daterangemonth',
    'dimensionColumnId': '7a70d9a5-f12c-43bb-af3a-2ab69d6b07c1',
    'type': 'string'}],
  'columnIds': ['0'],
  'dimension': {'id': 'variables/daterangemonth',
   'dimensionColumnId': '7a70d9a5-f12c-43bb-af3a-2ab69d6b07c1',
   'type': 'string'}},
 'rows': [{'itemIds': ['1251001'],
   'values': ['Nov 2025'],
   'data': [127384952618.0],
   'itemId': '1251001',
   'value': 'Nov 2025'},
  {'itemIds': ['1251101'],
   'values': ['Dec 2025'],
   'data': [89274163547.0],
   'itemId': '1251101',
   'value': 'Dec 2025'}],
 'summaryData': {'filteredTotals': [216659116165.0],
  'annotations': [],
  'totals': [216659116165.0],
  'annotationExceptions': [],
  'col-max': [127384952618.0],
  'col-min': [89274163547.0]}}

@patch('py2AdobeReporting.cja_functions.reporting_management.HttpClient')
@patch('py2AdobeReporting.cja_functions.reporting_management.px.line')
def test_monthly_time_series_report(mock_plotly, mock_http_client, monthly_time_series_response):
    reporting = Reporting()
    mock_response = Mock(status_code=200)
    mock_http_client.return_value.post.return_value = mock_response
    mock_response.text = json.dumps(monthly_time_series_response)
    # Mock plotly to prevent visualization
    mock_fig = Mock()
    mock_plotly.return_value = mock_fig
    headers = {"Authorization": "Bearer token"}
    
    # Call the actual method
    df = reporting.monthly_time_series_report(
        headers,
        "dv_test123",
        "2025-11-01",
        "2025-12-31",
        "metrics/occurrences"
    )
    assert isinstance(df, pd.DataFrame)
    column_names = ["Month","Metric"]
    df_dict = ut.dict_creation(column_names)
    i = 0
    res = monthly_time_series_response
    while i < len(res['rows']):
        month = res['rows'][i]['value']
        value = res['rows'][i]['data']
        var_list = [month, value]
        df_dict = ut.append_function_loop(df_dict, var_list, column_names)
        i+=1
    df = pd.DataFrame.from_dict(df_dict)
    df['Metric'] = df['Metric'].str[0]
    df['Metric'] = df['Metric'].astype('int64')
    df['Month'] = pd.to_datetime(df['Month'])
    # Sort by the date column
    df.sort_values(by='Month', inplace=True)
    print(type(df))
    assert type(df) == pd.core.frame.DataFrame
    columns = df.columns.tolist()
    assert columns == ["Month","Metric"]
    assert df['Metric'].sum() == 216659116165
    
@pytest.fixture
def daily_time_series_response():
    return {'totalPages': 1,
 'firstPage': True,
 'lastPage': True,
 'numberOfElements': 2,
 'number': 0,
 'totalElements': 2,
 'columns': {'dimensions': [{'id': 'variables/daterangeday',
    'dimensionColumnId': '7a70d9a5-f12c-43bb-af3a-2ab69d6b07c1',
    'type': 'string'}],
  'columnIds': ['0'],
  'dimension': {'id': 'variables/daterangeday',
   'dimensionColumnId': '7a70d9a5-f12c-43bb-af3a-2ab69d6b07c1',
   'type': 'string'}},
 'rows': [{'itemIds': ['1251001'],
   'values': ['Nov 30, 2025'],
   'data': [127384952618.0],
   'itemId': '1251001',
   'value': 'Nov 2025'},
  {'itemIds': ['1251101'],
   'values': ['Dec 1, 2025'],
   'data': [89274163547.0],
   'itemId': '1251101',
   'value': 'Dec 1, 2025'}],
 'summaryData': {'filteredTotals': [216659116165.0],
  'annotations': [],
  'totals': [216659116165.0],
  'annotationExceptions': [],
  'col-max': [127384952618.0],
  'col-min': [89274163547.0]}}

@patch('py2AdobeReporting.cja_functions.reporting_management.HttpClient')
@patch('py2AdobeReporting.cja_functions.reporting_management.px.line')
def test_daily_time_series_report(mock_plotly, mock_http_client, daily_time_series_response):
    reporting = Reporting()
    mock_response = Mock(status_code=200)
    mock_http_client.return_value.post.return_value = mock_response
    mock_response.text = json.dumps(daily_time_series_response)
    # Mock plotly to prevent visualization
    mock_fig = Mock()
    mock_plotly.return_value = mock_fig
    headers = {"Authorization": "Bearer token"}
    
    # Call the actual method
    df = reporting.daily_time_series_report(
        headers,
        "dv_test123",
        "2025-11-01",
        "2025-12-31",
        "metrics/occurrences"
    )
    assert isinstance(df, pd.DataFrame)
    column_names = ["Day","Metric"]
    df_dict = ut.dict_creation(column_names)
    i = 0
    res = daily_time_series_response
    while i < len(res['rows']):
        day = res['rows'][i]['value']
        value = res['rows'][i]['data']
        var_list = [day, value]
        df_dict = ut.append_function_loop(df_dict, var_list, column_names)
        i+=1
    df = pd.DataFrame.from_dict(df_dict)
    df['Metric'] = df['Metric'].str[0]
    df['Metric'] = df['Metric'].astype('int64')
    df['Day'] = pd.to_datetime(df['Day'])
    # Sort by the date column
    df.sort_values(by='Day', inplace=True)
    assert isinstance(df, pd.core.frame.DataFrame)
    columns = df.columns.tolist()
    assert columns == ["Day","Metric"]
    assert df['Metric'].sum() == 216659116165

@pytest.fixture
def five_metrics_report_response():
    metrics = ["Metric1", "Metric2", "Metric3", "Metric4", "Metric5"]
    dimension = "Date"
    return metrics, dimension, [{'itemIds': ['1251101'],
   'values': ['Dec 1, 2025'],
   'data': [4582917634.0, 398746521.0, 2147893456.0, 9832147.0, 456789123.0],
   'itemId': '1251101',
   'value': 'Dec 1, 2025'}]

@patch('py2AdobeReporting.cja_functions.reporting_management.Reporting.get_all_rows_report')
def test_five_metrics_report(mock_post, five_metrics_report_response):
    reporting = Reporting()
    mock_response = Mock(status_code=200)
    metrics, dimension, res = five_metrics_report_response
    mock_post.return_value = res
    headers = {"Authorization": "Bearer token"}
    # Call the actual method
    df = reporting.five_metrics_report(
        headers,
        "dv_test123",
        "2025-12-01",
        "2025-12-01",
        ["metrics/m1", "metrics/m2", "metrics/m3", "metrics/m4", "metrics/m5"],
        "variables/daterangeday",
        50000
    )
    assert isinstance(res, list)
    column_names = [dimension,metrics[0],metrics[1],metrics[2],metrics[3],metrics[4]]
    df_dict = {
        key: [] for key in column_names
    }
    i = 0
    while i < len(res):
        met_values = []
        dim = res[i]['value']
        for metric in res[i]['data']:
            met_values.append(metric)
        df_dict[column_names[0]].append(dim)
        df_dict[column_names[1]].append(met_values[0])
        df_dict[column_names[2]].append(met_values[1])
        df_dict[column_names[3]].append(met_values[2])
        df_dict[column_names[4]].append(met_values[3])
        df_dict[column_names[5]].append(met_values[4])
        met_values = []
        i+=1
    df = pd.DataFrame.from_dict(df_dict)
    assert isinstance(df, pd.core.frame.DataFrame)
    columns  = df.columns.tolist() 
    assert columns == column_names
    assert df[metrics[0]].sum() == 4582917634
    assert df[metrics[1]].sum() == 398746521
    assert df[metrics[2]].sum() == 2147893456
    assert df[metrics[3]].sum() == 9832147
    assert df[metrics[4]].sum() == 456789123

@pytest.fixture
def get_top_ten_dimension_items_response():
    dimension = "Page"
    return dimension, {'totalPages': 1,
 'firstPage': True,
 'lastPage': True,
 'numberOfElements': 10,
 'number': 0,
 'totalElements': 10,
 'columns': {'dimensions': [{'id': 'variables/page',
    'dimensionColumnId': 'abc123-def456-ghi789',
    'type': 'string'}],
  'columnIds': ['0'],
  'dimension': {'id': 'variables/page',
   'dimensionColumnId': 'abc123-def456-ghi789',
   'type': 'string'}},
 'rows': [
  {'itemIds': ['page1'], 'values': ['/home'], 'data': [5432187.0], 'itemId': 'page1', 'value': '/home'},
  {'itemIds': ['page2'], 'values': ['/products'], 'data': [3214569.0], 'itemId': 'page2', 'value': '/products'},
  {'itemIds': ['page3'], 'values': ['/about'], 'data': [2156789.0], 'itemId': 'page3', 'value': '/about'},
  {'itemIds': ['page4'], 'values': ['/contact'], 'data': [1876543.0], 'itemId': 'page4', 'value': '/contact'},
  {'itemIds': ['page5'], 'values': ['/services'], 'data': [1654321.0], 'itemId': 'page5', 'value': '/services'},
  {'itemIds': ['page6'], 'values': ['/blog'], 'data': [1432198.0], 'itemId': 'page6', 'value': '/blog'},
  {'itemIds': ['page7'], 'values': ['/pricing'], 'data': [1234567.0], 'itemId': 'page7', 'value': '/pricing'},
  {'itemIds': ['page8'], 'values': ['/faq'], 'data': [987654.0], 'itemId': 'page8', 'value': '/faq'},
  {'itemIds': ['page9'], 'values': ['/support'], 'data': [765432.0], 'itemId': 'page9', 'value': '/support'},
  {'itemIds': ['page10'], 'values': ['/careers'], 'data': [543210.0], 'itemId': 'page10', 'value': '/careers'}
 ],
 'summaryData': {'filteredTotals': [19297470.0],
  'annotations': [],
  'totals': [19297470.0],
  'annotationExceptions': [],
  'col-max': [5432187.0],
  'col-min': [543210.0]}}

@patch("py2AdobeReporting.cja_functions.reporting_management.HttpClient")
def test_get_top_ten_dimension_items(mock_http_client, get_top_ten_dimension_items_response):
    reporting = Reporting()
    dimension, res = get_top_ten_dimension_items_response
        # Mock HTTP response
    mock_response = Mock()
    mock_response.text = json.dumps(res)
    mock_response.status_code = 200
    mock_http_client.return_value.get.return_value = mock_response
    assert isinstance(res, dict)
    headers = {"Authorization": "Bearer token"}

    df = reporting.get_top_ten_dimension_items(
        headers,
        "dv_test123",
        "2024-01-01",
        "2024-01-31",
        "variables/page"
    )
    
    val_list = []
    start_date_list = []
    end_date_list = []
    start_date = "2024-01-01"
    end_date = "2024-01-31"
    i = 0
    for _ in res['rows']:
        val = res['rows'][i]['value']
        val_list.append(val)
        start_date_list.append(start_date)
        end_date_list.append(end_date)
        i+=1
    df_dict = {
        "Start Date": start_date_list,
        "End Date": end_date_list,
        f"{dimension}": val_list
    }
    df = pd.DataFrame.from_dict(df_dict)
    assert isinstance(df, pd.core.frame.DataFrame)
    columns = df.columns.tolist()
    assert columns == ["Start Date", "End Date", dimension]
    assert len(df) == 10
    assert df[dimension].tolist() == ['/home', '/products', '/about', '/contact', '/services', 
                                       '/blog', '/pricing', '/faq', '/support', '/careers']



