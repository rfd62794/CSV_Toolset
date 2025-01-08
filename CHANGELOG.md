# Changelog

All notable changes to CSV Toolset will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- Standalone tools:
  - csv_data_truncator.py: Column data truncation tool
  - csv_column_splitter.py: File splitting by column values
  - csv_inspector.py: CSV analysis tool
  - phoneColumnExtract.py: Phone number processing
  - sample_maker.py: Sample dataset generator
- Core framework components:
  - Automatic encoding detection
  - Progress tracking
  - Error handling
  - Logging system
- Documentation:
  - Tool documentation
  - Getting started guide
  - Installation instructions
  - Contributing guidelines

### Changed
- Improved error handling in all tools
- Enhanced progress reporting
- Standardized GUI layouts
- Updated documentation structure

### Fixed
- Encoding detection issues
- Memory management in large file processing
- GUI responsiveness during long operations

## [1.0.0] - 2025-01-08

### Added
- First stable release
- Complete set of standalone tools
- Core framework functionality
- Basic documentation
- Test suite
- Configuration system

### Security
- Input validation
- File access controls
- Error handling for malformed files

## Types of Changes
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities

## Version Format
- Major version: Incompatible API changes
- Minor version: Add functionality in a backward compatible manner
- Patch version: Backward compatible bug fixes 