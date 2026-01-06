# reporting_management
-----------------------
This module is used by the CJA Reporting API and provides significant value for extracting data

## Functionality
* Get Single Call Report
* Get Total Table Rows
* Get Total Table Pages
* Get All Rows Report
* Monthly Time Series Report
* Daily Time Series Report
* Five Metrics Report
* Breakdown Report
* Get Top Ten Dimension Items


## Dependencies
* pandas
* requests
* numpy
* plotly


## Common Input Parameters
* headers are generated using the auth file and are required for all calls
* req_num is an optional parameter that can be used to set the number of retries
* data_view_id is the unique identifier of the dataView
* start_date this is formatted in the standard `YYYY-MM-DD` format
* end_date this is formatted in the standard `YYYY-MM-DD` format
* metric this is the schema location for a single metric
* metrics this is a list of metrics, it must contain five separate entries in list format
* rows_per_page allows you to set the number of rows per page of pull, can accept a max of int 50000
* limit this is differentiated as an input name, but is functionally the same as rows_per_page

## Get Single Call Report
```python
get_single_call_report(headers=dict, body=dict, req_num=int)
```

## Get Total Table Rows
```python
get_total_table_rows(headers=dict, body=dict, req_num=int)
```

## Get Total Table Pages
```python
get_total_table_pages(headers=dict, body=dict, req_num=int)
```

## Get All Rows Report
```python
get_all_rows_report(headers=dict, body=dict, rows_per_page=int, req_num=int)
```

## Monthly Time Series Report
```python
monthly_time_series_report(headers=dict, data_view_id=str, start_date=str, end_date=str, metric=str, req_num=int, limit=int)
```
* This will get a month based report for a single metric

## Daily Time Series Report
```python
daily_time_series_report(headers=dict, data_view_id=str, start_date=str, end_date=str, metric=str, req_num=int, limit=int)
```
* This will get a day's based report for a single metric

## Five Metrics Report
```python
five_metrics_report(headers=dict, data_view_id=str, start_date=str, end_date=str, metrics=list, dimension=str, rows_per_page=int, req_num=int, limit=int)
```
* You must include five metrics in the entry for this to work and in a list format

## Breakdown Report
```python
breakdown_report(headers=dict, data_view_id=str, start_date=str, end_date=str, dimension=str, metric=str, dim_rows_per_page=int, breakdown_dim=str, breakdown_rows_per_page=int, req_num=int, limit=int)
```
* This will breakdown a single metric by two dimensions, rows_per_page will set the rows per page for each dimension

## Get Top Ten Dimension Items 
```python
get_top_ten_dimension_items(headers=dict, data_view_id=str, start_date=str, end_date=str, dimension=str, search_type=str, contains_term=str, req_num=int)
```
* dimension uses the full schema path
* search_type currently should be set to `contain` to access search functionality
* contains_term must use the following formatting "( CONTAINS 'click' )"

