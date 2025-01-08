# CSV Toolset

A comprehensive suite of Python tools for processing, analyzing, and transforming CSV files. Built with a focus on reliability, efficiency, and ease of use.

## 🚀 Features

- **Standalone Tools**
  - CSV Data Truncator - Truncate column data to specified lengths
  - CSV Column Splitter - Split files based on column values
  - CSV Inspector - Analyze and validate CSV structure
  - Phone Column Extractor - Process and standardize phone numbers
  - Sample Maker - Generate sample datasets

- **Core Framework**
  - Automatic encoding detection
  - Progress tracking and logging
  - Memory-efficient processing
  - Error handling and recovery
  - Extensible architecture

## 🛠 Installation

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

## 📚 Quick Start

### Data Truncation
```bash
python stand_alone/csv_data_truncator.py
```
Perfect for standardizing column lengths (e.g., SIC codes)

### File Splitting
```bash
python stand_alone/csv_column_splitter.py
```
Split files based on unique column values

### Data Inspection
```bash
python stand_alone/csv_inspector.py
```
Analyze CSV structure and content

## 📖 Documentation

- [Getting Started Guide](docs/tutorials/getting_started.md)
- [Tool Documentation](docs/tools/)
- [Tutorials](docs/tutorials/)
- [Contributing Guidelines](CONTRIBUTING.md)

## 🔧 Tools Overview

### CSV Data Truncator
- Truncate column data to specific lengths
- Preserve data integrity
- Automatic encoding detection
- Progress tracking

### CSV Column Splitter
- Split files by column values
- Preserve headers
- Create organized output
- Handle large files efficiently

### CSV Inspector
- Analyze file structure
- Validate data formats
- Generate statistics
- Identify issues

### Phone Column Extractor
- Extract phone numbers
- Standardize formats
- Validate entries
- Handle international formats

### Sample Maker
- Create data samples
- Maintain data distribution
- Configurable sample sizes
- Preserve relationships

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:
- Code style
- Development setup
- Testing requirements
- Pull request process

## 📋 Requirements

- Python 3.x
- Dependencies listed in requirements.txt
- Operating System: Windows/Linux/MacOS

## 🔒 Security

See [SECURITY.md](SECURITY.md) for:
- Security policy
- Reporting vulnerabilities
- Security best practices

## 📄 License

This project is licensed under [LICENSE](LICENSE.md) - see the file for details.

## 🙏 Acknowledgments

- Contributors and maintainers
- Open source community
- Tool users and testers 