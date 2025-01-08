# Getting Started with CSV Toolset

This tutorial will guide you through setting up and using the CSV Toolset for common data processing tasks.

## Installation

1. **Prerequisites**:
   - Python 3.x installed
   - Git installed
   - Basic knowledge of CSV files

2. **Setup**:
```bash
# Clone the repository
git clone [repository-url]
cd CSV_Toolset

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Unix/MacOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start Guide

### 1. Truncating Column Data

Perfect for standardizing column lengths (e.g., SIC codes):

```bash
python stand_alone/csv_data_truncator.py
```

1. Click "Select CSV File"
2. Choose the column to truncate
3. Enter desired length (e.g., 4 for SIC codes)
4. Click "Process File"

### 2. Splitting Files by Column Values

Useful for categorizing data:

```bash
python stand_alone/csv_column_splitter.py
```

1. Click "Select CSV File"
2. Choose the column to split on
3. Click "Split File"
4. Find results in the "Split" directory

### 3. Inspecting CSV Files

Analyze your data structure:

```bash
python stand_alone/csv_inspector.py
```

## Common Workflows

### Cleaning SIC Code Data

1. **Inspect the Data**:
   - Use `csv_inspector.py` to check SIC code format
   - Note any inconsistencies

2. **Standardize Codes**:
   - Use `csv_data_truncator.py`
   - Select SIC code column
   - Set length to 4

3. **Categorize Data**:
   - Use `csv_column_splitter.py`
   - Split by standardized SIC codes
   - Review categorized files

### Processing Phone Numbers

1. **Extract Numbers**:
   - Use `phoneColumnExtract.py`
   - Select phone number column
   - Process for standardization

2. **Validate Data**:
   - Use `csv_inspector.py`
   - Check formatted numbers
   - Identify any issues

### Creating Sample Datasets

1. **Generate Samples**:
   - Use `sample_maker.py`
   - Select source file
   - Choose sample size

2. **Verify Samples**:
   - Use `csv_inspector.py`
   - Check data distribution
   - Validate sample integrity

## Tips and Best Practices

### 1. File Management
- Keep original files backed up
- Use descriptive filenames
- Organize output directories

### 2. Data Preparation
- Check file encoding
- Verify column headers
- Clean data before processing

### 3. Processing Large Files
- Close unnecessary applications
- Monitor system resources
- Use appropriate chunk sizes

## Troubleshooting

### Common Issues

1. **File Won't Open**:
   - Check file encoding
   - Verify file permissions
   - Look for special characters

2. **Processing is Slow**:
   - Check file size
   - Monitor memory usage
   - Close other applications

3. **Unexpected Results**:
   - Review log messages
   - Check input data format
   - Verify tool settings

## Next Steps

1. **Explore Advanced Features**:
   - Try different tool combinations
   - Experiment with settings
   - Review tool documentation

2. **Automate Workflows**:
   - Learn about batch processing
   - Study integration options
   - Create processing scripts

3. **Contribute**:
   - Read CONTRIBUTING.md
   - Try fixing simple issues
   - Suggest improvements

## Getting Help

1. **Documentation**:
   - Read tool-specific docs
   - Check troubleshooting guides
   - Review examples

2. **Support**:
   - Open GitHub issues
   - Join discussions
   - Contact maintainers

3. **Community**:
   - Share your experience
   - Help other users
   - Contribute improvements

## Additional Resources

- [Tool Documentation](../tools/)
- [Contributing Guidelines](../../CONTRIBUTING.md)
- [Project README](../../README.md) 