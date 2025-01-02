# CSV Toolkit Documentation

## Project Overview
CSV Toolkit is a comprehensive GUI application for manipulating and analyzing CSV files. It provides a modular architecture with various tools for different CSV operations.

## Directory Structure

### Root Directory
- `app.py` - Main application entry point
- `csv_toolkit.py` - Main application window class
- `csv_utils.py` - Core CSV handling utilities
- `requirements.txt` - Project dependencies

### GUI Components
- `gui/`
  - `toolkit_window.py` - Main window implementation

### Tools Directory (`tools/`)

#### Base Classes
- `base/`
  - `tool_frame.py` - Base class for all tool frames
  - `base_processor.py` - Base class for data processors

#### Tool Frames (`tools/frames/`)
Each frame represents a tool interface:
- `inspector_frame.py` - CSV file inspection
- `sweeper_frame.py` - Data cleaning and standardization
- `phone_frame.py` - Phone number formatting
- `sample_frame.py` - Data sampling
- `reverser_frame.py` - Row/column order reversal
- `appender_frame.py` - Column appending
- `merger_frame.py` - File merging
- `splitter_frame.py` - File splitting
- `transformer_frame.py` - Data transformation
- `filter_frame.py` - Data filtering
- `validator_frame.py` - Data validation
- `profiler_frame.py` - Data profiling
- `column_manager_frame.py` - Column management
- `reformatter_frame.py` - Data reformatting

#### Processors (`tools/processors/`)
Backend processing logic for each tool:
- `inspector_processor.py` - File inspection logic
- `sweeper_processor.py` - Data cleaning logic
- `phone_processor.py` - Phone number processing
- `sample_processor.py` - Sampling logic
- `reverser_processor.py` - Order reversal logic
- `appender_processor.py` - Column appending logic
- `merger_processor.py` - File merging logic
- `splitter_processor.py` - File splitting logic
- `transformer_processor.py` - Data transformation logic
- `filter_processor.py` - Filtering logic
- `validator_processor.py` - Validation logic
- `profiler_processor.py` - Profiling logic
- `column_processor.py` - Column operations
- `sampling_strategies.py` - Different sampling methods

#### Utilities (`tools/utils/`)
- `data_analyzer.py` - Data analysis utilities
- `data_cleaner.py` - Data cleaning utilities
- `data_merger.py` - Data merging utilities
- `data_reader.py` - File reading utilities
- `data_transformer.py` - Data transformation utilities
- `data_types.py` - Data type detection/conversion
- `data_validator.py` - Data validation utilities
- `data_writer.py` - File writing utilities
- `dialog_manager.py` - Dialog box management
- `error_handler.py` - Error handling utilities
- `file_manager.py` - File operations
- `file_operations.py` - Additional file utilities
- `logger.py` - Logging functionality
- `metrics_collector.py` - Performance metrics
- `pattern_processor.py` - Pattern matching/processing
- `performance_monitor.py` - Performance monitoring
- `progress_tracker.py` - Progress tracking
- `settings_manager.py` - Settings management
- `stats_formatter.py` - Statistics formatting
- `theme_manager.py` - UI theme management
- `tool_manager.py` - Tool registration/management
- `tool_registry.py` - Tool registry

#### Widgets (`tools/widgets/`)
Custom UI components:
- `config_panel.py` - Configuration panel
- `file_selector.py` - File selection widget
- `list_selector.py` - List selection widget
- `tooltip.py` - Tooltip widget
- `type_preview.py` - Data type preview
- `type_preview_dialog.py` - Type preview dialog

### Standalone Tools (`stand_alone/`)
Independent script versions of tools:
- `csv_append_column_filler_data.py` - Column appending
- `csv_columnsweep.py` - Column cleaning
- `csv_inspector.py` - Basic file inspection
- `csv_inspector_gadget.py` - Advanced file inspection
- `csv_order_reverse.py` - Order reversal
- `phoneColumnExtract.py` - Phone number extraction
- `sample_maker.py` - Sample creation

### Tests (`tests/`)
Test infrastructure and cases:
- `config.py` - Test configuration
- `fixtures.py` - Test fixtures
- `markers.py` - Test markers
- `run_tests.py` - Test runner
- `test_base.py` - Base test class
- `test_performance_base.py` - Performance test base
- `test_sample_processor.py` - Sample processor tests

## Key Features
- Modular architecture with separate UI and processing components
- Extensive error handling and validation
- Progress tracking and user feedback
- Configuration management
- Theme support
- Comprehensive testing framework
- Standalone tool versions
- Performance monitoring and optimization

## Dependencies
Key dependencies are listed in requirements.txt and include:
- tkinter - GUI framework
- pandas - Data processing
- numpy - Numerical operations
- chardet - Character encoding detection
- pytest - Testing framework 

## Application Versions

### Basic Version (`app.py`)
- Simple, focused interface
- Core CSV processing functionality
- Faster startup and lower resource usage
- Ideal for basic use cases and new users

### Advanced Version (`csv_toolkit.py`)
- Full feature set with advanced tools
- Complete tool management system
- Theme and configuration management
- Extended processing capabilities
- Suitable for power users and complex operations 