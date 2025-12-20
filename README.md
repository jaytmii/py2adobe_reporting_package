# py2AdobeReporting

A Python wrapper for Adobe Customer Journey Analytics (CJA) Reporting API that enables analysts to easily extract and analyze data programmatically.

## Features

- **Time Series Reports** - Daily and monthly aggregated metrics
- **Multi-Metric Analysis** - Pull up to 5 metrics in a single report
- **Dimension Breakdowns** - Break down metrics by multiple dimensions
- **Top Items Analysis** - Get top 10 dimension items with optional search
- **Pagination Support** - Handle large datasets with automatic pagination (up to 50,000 rows per page)
- **Server-to-Server Authentication** - Secure OAuth 2.0 authentication

## Installation

```bash
pip install py2AdobeReporting
```

Or install from source:

```bash
git clone https://github.com/jaytmii/py2AdobeReportingPackage.git
cd py2AdobeReportingPackage
pip install -e .
```

## Requirements

- Python >= 3.8
- Adobe CJA API credentials (OAuth 2.0 Server-to-Server)

## Quick Start

### 1. Set Up Authentication

Create a JSON configuration file with your Adobe credentials:

```json
{
  "clientSecret": "your-client-secret",
  "defaultHeaders": {
    "x-api-key": "your-api-key",
    "x-gw-ims-org-id": "your-org-id"
  },
  "companyId": "your-company-id",
  "scopes": "api_scopes",
  "imsHost": "ims",
  "tokenUrl": "token_url"
}
```

### 2. Authenticate

```python
from py2AdobeReporting.auth import s2sAuth

# Authenticate and get environment object
env = s2sAuth("path/to/config.json")
```

### 3. Generate Headers

```python
from py2AdobeReporting.auth import cja_oauth_headers

# Create headers for API calls
headers = cja_oauth_headers("path/to/config.json", env.token)
```

### 4. Pull a Report

```python
from py2AdobeReporting.cja_functions.reporting_management import Reporting

# Initialize reporting class
reporting = Reporting()

# Get daily time series report
df = reporting.daily_time_series_report(
    headers=headers,
    data_view_id="your-data-view-id",
    start_date="2024-01-01",
    end_date="2024-01-31",
    metric="metrics/visits"
)

print(df.head())
```

## Available Functions

### Time Series Reports
- `monthly_time_series_report()` - Month-level aggregated metrics
- `daily_time_series_report()` - Day-level aggregated metrics

### Multi-Dimensional Reports
- `five_metrics_report()` - Pull 5 metrics with a dimension
- `breakdown_report()` - Break down a metric by two dimensions
- `get_all_rows_report()` - Get all rows for custom request body

### Utility Functions
- `get_single_call_report()` - Single API call with custom body
- `get_total_table_rows()` - Get row count for a table
- `get_total_table_pages()` - Calculate total pages needed
- `get_top_ten_dimension_items()` - Get top 10 items for a dimension

## Documentation

For detailed function parameters and examples, see:
- [Reporting Management Documentation](docs/reporting_management.md)

## Example Use Cases

### Get Monthly Visits

```python
df = reporting.monthly_time_series_report(
    headers=headers,
    data_view_id="dv_123",
    start_date="2024-01-01",
    end_date="2024-12-31",
    metric="metrics/visits"
)
```

### Breakdown by Multiple Dimensions

```python
df = reporting.breakdown_report(
    headers=headers,
    data_view_id="dv_123",
    start_date="2024-01-01",
    end_date="2024-01-31",
    dimension="variables/page",
    metric="metrics/visits",
    dim_rows_per_page=50,
    breakdown_dim="variables/browser",
    breakdown_rows_per_page=50
)
```

### Search for Dimension Items

```python
df = reporting.get_top_ten_dimension_items(
    headers=headers,
    data_view_id="dv_123",
    start_date="2024-01-01",
    end_date="2024-01-31",
    dimension="variables/page",
    search_type="contains",
    contains_term="( CONTAINS 'product' )"
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

James Mitchell - jaytmii@gmail.com

## Acknowledgments

Built for Adobe Customer Journey Analytics API v2.0
