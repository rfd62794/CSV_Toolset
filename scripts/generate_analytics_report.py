#!/usr/bin/env python3
"""Generate documentation analytics report from Google Analytics data."""

import os
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

def get_analytics_client():
    """Create Google Analytics client."""
    return BetaAnalyticsDataClient()

def run_report(client, property_id, start_date, end_date, dimensions, metrics):
    """Run a Google Analytics report."""
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name=d) for d in dimensions],
        metrics=[Metric(name=m) for m in metrics],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    )
    return client.run_report(request)

def generate_page_views_chart(data, output_dir):
    """Generate chart for page views."""
    plt.figure(figsize=(12, 6))
    sns.barplot(data=data, x='page_path', y='page_views')
    plt.xticks(rotation=45, ha='right')
    plt.title('Most Viewed Documentation Pages')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/page_views.png')
    plt.close()

def generate_report():
    """Generate analytics report."""
    client = get_analytics_client()
    property_id = os.getenv('GOOGLE_ANALYTICS_KEY')
    
    # Calculate date range
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    # Get page views
    response = run_report(
        client,
        property_id,
        start_date,
        end_date,
        ['pagePath'],
        ['screenPageViews', 'averageSessionDuration', 'bounceRate']
    )
    
    # Process data
    data = []
    for row in response.rows:
        data.append({
            'page_path': row.dimension_values[0].value,
            'page_views': int(row.metric_values[0].value),
            'avg_time': float(row.metric_values[1].value),
            'bounce_rate': float(row.metric_values[2].value)
        })
    
    df = pd.DataFrame(data)
    df = df.sort_values('page_views', ascending=False).head(10)
    
    # Generate charts
    os.makedirs('analytics', exist_ok=True)
    generate_page_views_chart(df, 'analytics')
    
    # Generate markdown report
    report = f"""# 📊 Documentation Analytics Report
    
## Overview
Report period: {start_date} to {end_date}

## Most Viewed Pages
{df.to_markdown(index=False)}

## Key Metrics
- Total Page Views: {df['page_views'].sum()}
- Average Time on Page: {df['avg_time'].mean():.2f} seconds
- Average Bounce Rate: {df['bounce_rate'].mean():.2%}

## Recommendations
1. Pages with high bounce rates might need improvement
2. Consider adding more content to pages with low average time
3. Popular pages should be prioritized for updates

## Charts
![Page Views](analytics/page_views.png)

## Notes
- Data collected via Google Analytics 4
- Only showing top 10 most viewed pages
- Bounce rate indicates single-page sessions
"""
    
    with open('analytics_report.md', 'w') as f:
        f.write(report)

if __name__ == '__main__':
    generate_report() 