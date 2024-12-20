import csv
import os
import chardet
from collections import defaultdict, Counter
import re
import time
import statistics
import pandas as pd
import psutil

class CSVAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.file_size = None
        self.encoding = None
        self.column_names = []
        self.num_rows = 0
        self.data_types = defaultdict(set)
        self.unique_values = defaultdict(set)
        self.null_counts = defaultdict(int)
        self.value_counts = defaultdict(Counter)
        self.numeric_stats = defaultdict(dict)

    def get_file_info(self):
        self.file_size = os.path.getsize(self.filename)
        with open(self.filename, 'rb') as f:
            rawdata = f.read()
            result = chardet.detect(rawdata)
            self.encoding = result['encoding']

    def detect_delimiter(self):
        with open(self.filename, 'r', encoding=self.encoding) as f:
            sample = f.read(1024)
            sniffer = csv.Sniffer()
            return sniffer.sniff(sample).delimiter

    def estimate_row_size(self, sample_size=100):
        with open(self.filename, 'r', encoding=self.encoding) as f:
            reader = csv.reader(f)
            sample_rows = [next(reader) for _ in range(sample_size)]
            total_size = sum(len(','.join(row).encode(self.encoding)) for row in sample_rows)
            return total_size / sample_size

    def estimate_chunk_size(self):
        available_memory = psutil.virtual_memory().available
        average_row_size = self.estimate_row_size()
        max_memory_usage = available_memory * 0.05
        chunk_size = int(max_memory_usage / average_row_size)
        return min(max(chunk_size, 1000), 100000)

    def analyze_data(self):
        chunk_size = self.estimate_chunk_size()
        print(f"Using chunk size: {chunk_size} rows")
        delimiter = self.detect_delimiter()
        with open(self.filename, 'r', encoding=self.encoding) as f:
            reader = csv.reader(f, delimiter=delimiter)
            try:
                self.column_names = next(reader)
            except StopIteration:
                print("Error: The CSV file is empty.")
                return

            for row in reader:
                self.num_rows += 1
                self.process_row(row)

    def process_row(self, row):
        for i, value in enumerate(row):
            self.process_value(value, self.column_names[i])

    def process_value(self, value, column_name):
        detected_type = self.detect_data_type(value)
        self.data_types[column_name].add(detected_type)
        self.unique_values[column_name].add(value)
        if value == '' or value is None:
            self.null_counts[column_name] += 1
        self.value_counts[column_name][value] += 1
        self.update_numeric_stats(column_name, value)

    def detect_data_type(self, value):
        try:
            int(value)
            return int
        except ValueError:
            try:
                float(value)
                return float
            except ValueError:
                patterns = {
                    'date': [r'\d{4}-\d{2}-\d{2}', r'\d{2}/\d{2}/\d{4}'],
                    'email': [r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'],
                    'url': [r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)'],
                    'phone': [r'(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'],
                    'postcode': [r'^(?:[A-Z]{1,2}\d{1,2}[A-Z]?)\s*\d[A-Z]{2}$'],
                    'boolean': [r'^(true|false)$'],
                    'time': [r'\d{2}:\d{2}(:\d{2})?']
                }
                for data_type, pattern_list in patterns.items():
                    for pattern in pattern_list:
                        if re.match(pattern, value, re.IGNORECASE):
                            return data_type
                return str

    def update_numeric_stats(self, column_name, value):
        num_value = self.convert_to_numeric(value)
        if num_value is not None:
            self.update_stats(self.numeric_stats[column_name], num_value)

    def convert_to_numeric(self, value):
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return None

    def update_stats(self, stats, num_value):
        stats.setdefault('count', 0)
        stats['count'] += 1
        stats.setdefault('min', num_value)
        stats['min'] = min(stats['min'], num_value)
        stats.setdefault('max', num_value)
        stats['max'] = max(stats['max'], num_value)
        stats.setdefault('values', []).append(num_value)
        if 'values' in stats:
            stats['median'] = statistics.median(stats['values'])
            stats['std_dev'] = statistics.stdev(stats['values']) if len(stats['values']) > 1 else 0

    def print_static_info(self):
        file_stats = os.stat(self.filename)
        last_modified = time.ctime(file_stats.st_mtime)
        creation_time = time.ctime(file_stats.st_ctime)

        print("\n--- Static Information ---")
        print(f"File size: {self.file_size} bytes")
        print(f"Detected encoding: {self.encoding}")
        print(f"Last modified: {last_modified}")
        print(f"Creation time: {creation_time}")
        print(f"Number of columns: {len(self.column_names)}")
        print(f"Number of rows: {self.num_rows}")

    def print_data_completeness_summary(self):
        print("\n--- Data Completeness Summary ---")
        for col, null_count in self.null_counts.items():
            completeness = (1 - null_count / self.num_rows) * 100
            print(f"{col}: {completeness:.2f}% complete")

    def print_top_frequent_values(self, top_n=5):
        print("\n--- Top Frequent Values ---")
        for col, counts in self.value_counts.items():
            top_values = counts.most_common(top_n)
            print(f"{col}: {top_values}")

def main():
    filename = 'your_file.csv'  # Replace with your file path
    analyzer = CSVAnalyzer(filename)
    analyzer.get_file_info()
    analyzer.analyze_data()
    analyzer.print_static_info()
    analyzer.print_data_completeness_summary()
    analyzer.print_top_frequent_values()

if __name__ == "__main__":
    main()