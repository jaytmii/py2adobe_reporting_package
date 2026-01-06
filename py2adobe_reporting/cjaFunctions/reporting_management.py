"""For managing all 2.0 API extracts"""
import json
import time
from itertools import chain
import pandas as pd
import numpy as np
from py2adobe_reporting.http_client import HttpClient, DEFAULT_RETRY_COUNT
from py2adobe_reporting import utils as ut
from py2adobe_reporting.reporting_api import ReportingAPI

class Reporting(ReportingAPI):
    """Class for all CJA Reporting Management functions"""

    def __init__(self):
        super().__init__()

    def rows_per_page_setting(self, data_input):
        """Helper function to get Rows Per Page | limit"""
        ## For inputs on rowsPerPage
        if data_input > 50000:
            data_input = 50000
            return data_input
        else:
            data_input1 = data_input
            return data_input1

    def dim_rows_per_page_setting(self, data_input):
        """Helper function to get Limit Per Page"""
        ## For inputs on rowsPerPage for dimension and breakdowns
        if data_input > 400:
            data_input = 400
        else:
            data_input1 = data_input
            return data_input1


    ## Input body of your choice
    def get_single_call_report(self, headers, body):
        """Package function for inputing your body for a report completed in one call"""
        url = ReportingAPI.base_url()
        res = HttpClient(url, 
                         headers, 
                         req_num=DEFAULT_RETRY_COUNT, 
                         payload_type="json", 
                         body=body).post()
        res = json.loads(res.text)
        return res

    def get_total_table_rows(self, headers, body):
        """Pacakge function for getting the total rows available in a table"""
        url = ReportingAPI.base_url()
        body['settings']['limit']=1
        res = HttpClient(url, 
                         headers, 
                         req_num=DEFAULT_RETRY_COUNT, 
                         payload_type="json", 
                         body=body).post()
        res = json.loads(res.text)
        res = res['totalElements']
        return res

    def get_total_table_pages(self, headers, body):
        """Package function for getting the Total Table Pages"""
        total_rows = self.get_total_table_rows(headers, body)
        total_pages = int(np.ceil(total_rows/50000))
        return total_pages

    def get_all_rows_report(self, headers, body, rows_per_page):
        """Package function built to get all the rows present 
        on a table for a single call(one dimension, multiple metrics)"""
        row_num = self.get_total_table_rows(headers, body)
        time.sleep(2)
        ## Set to max Rows per pull
        rows_per_page = self.rows_per_page_setting(rows_per_page)
        num_of_calls = int(np.ceil(row_num/rows_per_page))
        url = ReportingAPI.base_url()
        num_pages = self.get_total_table_pages(headers, body)
        body['settings']['limit']=rows_per_page
        output = []
        i = 0
        print("Total Pages to be pulled: " + str(num_of_calls))
        print("Starting pull....")
        for _ in range(num_of_calls):
            while i < num_pages:
                body['settings']['page']=i
                time.sleep(2)
                print("Pulling Page: " + str(i))
                res = HttpClient(url, 
                                 headers, 
                                 req_num=DEFAULT_RETRY_COUNT, 
                                 payload_type="json", 
                                 body=body).post()
                res = json.loads(res.text)
                new_data = res['rows']
                output.append(new_data)
                i+=1
        output = list(chain.from_iterable(output))
        return output

    def monthly_time_series_report(self, headers, data_view_id, start_date, end_date, metric, limit=50000):
        """Package functiuon for month level time series reports"""
        url = ReportingAPI.base_url()
        limit = self.rows_per_page_setting(limit)
        body = {"globalFilters": [
            {
                "type": "dateRange",
                "dateRange": start_date + "T00:00:00.000/" + end_date + "T00:00:00.000"
            }
        ],
                "metricContainer": {
                    "metrics": [
                        {
                            "columnId": "0",
                            "id": metric,
                            "sort": "desc"
                        }
                    ]
                },
                "dimension": "variables/daterangemonth",
                "settings": {
                    "countRepeatInstances": "true",
                    "includeAnnotations": "true",
                    "limit": limit,
                    "page": 0,
                    "nonesBehavior": "return-nones"
                },
                "statistics": {
                    "functions": [
                        "col-max",
                        "col-min"
                    ]
                },
                "dataId": data_view_id
            }
        res = HttpClient(url, 
                         headers, 
                         req_num=DEFAULT_RETRY_COUNT, 
                         payload_type="json", 
                         body=body).post()
        res = json.loads(res.text)
        column_names = ["Month","Metric"]
        df_dict = ut.dict_creation(column_names)
        i = 0
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
        return df

    def daily_time_series_report(self, headers, data_view_id, start_date, end_date, metric, 
                              limit=50000):
        """Package functions for time series daily level reports"""
        url = ReportingAPI.base_url()
        limit = self.rows_per_page_setting(limit)
        body = {"globalFilters": [
            {
                "type": "dateRange",
                "dateRange": start_date + "T00:00:00.000/" + end_date + "T00:00:00.000"
            }
        ],
                "metricContainer": {
                    "metrics": [
                        {
                            "columnId": "0",
                            "id": metric,
                            "sort": "desc"
                        }
                    ]
                },
                "dimension": "variables/daterangeday",
                "settings": {
                    "countRepeatInstances": "true",
                    "includeAnnotations": "true",
                    "limit": limit,
                    "page": 0,
                    "nonesBehavior": "return-nones"
                },
                "statistics": {
                    "functions": [
                        "col-max",
                        "col-min"
                    ]
                },
                "dataId": data_view_id
            }
        res = HttpClient(url, 
                         headers, 
                         req_num=DEFAULT_RETRY_COUNT, 
                         payload_type="json", 
                         body=body).post()
        res = json.loads(res.text)
        column_names = ["Day","Metric"]
        df_dict = ut.dict_creation(column_names)
        i = 0
        while i < len(res['rows']):
            month = res['rows'][i]['value']
            value = res['rows'][i]['data']
            var_list = [month, value]
            df_dict = ut.append_function_loop(df_dict, var_list, column_names)
            i+=1
        df = pd.DataFrame.from_dict(df_dict)
        df['Metric'] = df['Metric'].str[0]
        df['Metric'] = df['Metric'].astype('int64')
        df['Day'] = pd.to_datetime(df['Day'])
        # Sort by the date column
        df.sort_values(by='Day', inplace=True)
        return df

    def five_metrics_report(self, headers, data_view_id, start_date, end_date,
                        metrics, dimension, rows_per_page):
        """Package function for pulling a table with five metrics"""
        rows_per_page = self.rows_per_page_setting(rows_per_page)
        body = {"globalFilters": [
            {
                "type": "dateRange",
                "dateRange": start_date + "T00:00:00.000/" + end_date + "T00:00:00.000"
            }
        ],
                "metricContainer": {
                    "metrics": [
                        {
                            "columnId": "0",
                            "id": metrics[0],
                            "sort": "desc"
                        },
                        {
                            "columnId": "1",
                            "id": metrics[1],
                            "sort": "desc"
                        },
                        {
                            "columnId": "2",
                            "id": metrics[2],
                            "sort": "desc"
                        },
                        {
                            "columnId": "3",
                            "id": metrics[3],
                            "sort": "desc"
                        },
                        {
                            "columnId": "4",
                            "id": metrics[4],
                            "sort": "desc"
                        }
                    ]
                },
                "dimension": dimension,
                "settings": {
                    "countRepeatInstances": "true",
                    "includeAnnotations": "true",
                    "limit": rows_per_page,
                    "page": 0,
                    "nonesBehavior": "return-nones"
                },
                "statistics": {
                    "functions": [
                        "col-max",
                        "col-min"
                    ]
                },
                "dataId": data_view_id
            }
        res = self.get_all_rows_report(headers, body, rows_per_page)
        column_names = [dimension,metrics[0],metrics[1],metrics[2],metrics[3],metrics[4]]
        df_dict = ut.dict_creation(column_names)
        i = 0
        while i < len(res):
            dim = res[i]['value']
            l = 0
            while l < len(res[i]['data']):
                met1 = res[i]['data'][l]
                met2 = res[i]['data'][l]
                met3 = res[i]['data'][l]
                met4 = res[i]['data'][l]
                met5 = res[i]['data'][l]
                l+=1
            var_list = [dim, met1, met2, met3, met4, met5]
            df_dict = ut.append_function_loop(df_dict, var_list, column_names)
            i+=1
        df = pd.DataFrame.from_dict(df_dict)
        return df

    def breakdown_report(self, headers, data_view_id, start_date, end_date, dimension,
                        metric, dim_rows_per_page, breakdown_dim, breakdown_rows_per_page):
        """Package function that is used to create a report with 
        one metric and one dimension broken down by another"""
        url = ReportingAPI.base_url()
        dim_rows_per_page = self.dim_rows_per_page_setting(dim_rows_per_page)
        breakdown_rows_per_page = self.dim_rows_per_page_setting(breakdown_rows_per_page)
        body = {"globalFilters": [
            {
                "type": "dateRange",
                "dateRange": start_date + "T00:00:00.000/" + end_date + "T00:00:00.000"
            }
        ],
                "metricContainer": {
                    "metrics": [
                        {
                            "columnId": "0",
                            "id": metric,
                            "sort": "desc"
                        }
                    ]
                },
                "dimension": dimension,
                "settings": {
                    "countRepeatInstances": "true",
                    "includeAnnotations": "true",
                    "limit": dim_rows_per_page,
                    "page": 0,
                    "nonesBehavior": "return-nones"
                },
                "statistics": {
                    "functions": [
                        "col-max",
                        "col-min"
                    ]
                },
                "dataId": data_view_id
            }
        print("Pulling rows to be broken down....")
        res = HttpClient(url, 
                         headers, 
                         req_num=DEFAULT_RETRY_COUNT, 
                         payload_type="json", 
                         body=body).post()
        res = json.loads(res.text)
        num_of_calls = len(res['rows'])
        print("Total Rows to be broken down by " + breakdown_dim + ": " + str(num_of_calls))
        print("Rows per breakdown: " + str(breakdown_rows_per_page))
        i = 0
        breakdown_body =   {
            "globalFilters": [
                {
                    "type": "dateRange",
                    "dateRange": start_date + "T00:00:00.000/"+ end_date +"T00:00:00.000"
                }
            ],
                        "metricContainer": {
                            "metrics": [
                                {
                                    "columnId": "0",
                                        "id": metric,
                                        "sort": "desc",
                                        "filters": [
                                            "0"
                                        ]
                                    }
                            ],
                            "metricFilters": [
                                    {
                                        "id": "0",
                                        "type": "breakdown",
                                        "dimension": dimension,
                                        "itemId":""
                                    }]},
                        "dimension": breakdown_dim,
                        "settings": {
                            "countRepeatInstances": "true",
                            "includeAnnotations": "true",
                            "limit": breakdown_rows_per_page,
                            "page": 0,
                            "nonesBehavior": "return-nones"
                        },
                            "statistics": {
                                "functions": [
                                    "col-max",
                                    "col-min"
                                ]
                            },
                            "dataId": data_view_id
                        }
        dimension_value_list = []
        dimension_metric_value_list = []
        breakdown_value_list = []
        breakdown_metric_value_list = []
        time.sleep(1)
        for _ in range(num_of_calls):
            breakdown_body['metricContainer']['metricFilters'][0]['itemId'] = res['rows'][i]['itemId']
            print("Breaking row " + str(i) + " down....")
            breakdown_rows = HttpClient(url, 
                                       headers, 
                                       req_num=DEFAULT_RETRY_COUNT, 
                                       payload_type="json", 
                                       body=breakdown_body).post()
            breakdown_rows = json.loads(breakdown_rows.text)
            print("Breakdown complete for row: " + str(i))
            l = 0
            while l < len(breakdown_rows['rows']):
                dim_val = res['rows'][i]['value']
                dim_met_val = res['rows'][i]['data']
                breakdown_val = breakdown_rows['rows'][l]['value']
                breakdown_met_val = breakdown_rows['rows'][l]['data']
                dimension_value_list.append(dim_val)
                dimension_metric_value_list.append(dim_met_val)
                breakdown_value_list.append(breakdown_val)
                breakdown_metric_value_list.append(breakdown_met_val)
                l+=1
            i+=1
            time.sleep(2)
        df_dict = {
            dimension:dimension_value_list,
            breakdown_dim:breakdown_value_list,
            "Metric Value":dimension_metric_value_list,
            "Breakdown Metric Value":breakdown_metric_value_list
        }
        df = pd.DataFrame.from_dict(df_dict)
        df['Metric Value'] = df['Metric Value'].str[0]
        df['Metric Value'] = df['Metric Value'].astype('int64')
        df['Breakdown Metric Value'] = df['Breakdown Metric Value'].str[0]
        df['Breakdown Metric Value'] = df['Breakdown Metric Value'].astype('int64')
        return df


    def get_top_ten_dimension_items_call(self, headers, data_view_id, start_date, end_date, dimension,
                                search_type=str, contains_term=str):
        """API Call function for getting the top ten dimension items for a time period"""
        limit = 10
        date_range = f"{start_date}T00:00:00.000/{end_date}T00:00:00.000"
        base_url = ReportingAPI.build_get_top_items_url()
        try:
            if "contains" in search_type:
                url = f"{base_url}?dataId={data_view_id}&dimension={dimension}&dateRange={date_range}&search-clause={contains_term}&limit={limit}"
                res = HttpClient(url,headers).get()
                res = json.loads(res.text)
        except TypeError:
            url = f"{base_url}?dataId={data_view_id}&dimension={dimension}&dateRange={date_range}&limit={limit}"
            res = HttpClient(url,headers).get()
            res = json.loads(res.text)
        return res

    def get_top_ten_dimension_items_clean(self, res, start_date, end_date, dimension):
        """Cleaning function for Top Ten Dimensions"""
        val_list = []
        start_date_list = []
        end_date_list = []
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
            f"{dimension}":val_list
        }
        df = pd.DataFrame.from_dict(df_dict)
        return df


    def get_top_ten_dimension_items(self, headers, data_view_id, start_date, end_date, dimension,
                                search_type=str, contains_term=str):
        """Package function for getting the top ten dimension items for a time period"""
        res = self.get_top_ten_dimension_items_call(headers, data_view_id, start_date, end_date, dimension,
                                search_type, contains_term)
        df = self.get_top_ten_dimension_items_clean(res, start_date, end_date, dimension)
        return df
