# Encoding Handling Guide

## Overview
This guide provides comprehensive strategies and best practices for handling character encodings in CSV files. It covers detection, conversion, and validation of various encodings to ensure data integrity.

## Encoding Detection

### 1. Automatic Detection
```python
class EncodingDetector:
    def __init__(self):
        self.detectors = [
            ('chardet', self.detect_with_chardet),
            ('ftfy', self.detect_with_ftfy),
            ('bom', self.detect_with_bom)
        ]
    
    def detect_encoding(self, file_path: str) -> str:
        """Detect file encoding using multiple methods"""
        for name, detector in self.detectors:
            try:
                encoding = detector(file_path)
                if encoding:
                    return encoding
            except Exception as e:
                logging.warning(
                    f"Detector {name} failed: {str(e)}"
                )
        return 'utf-8'  # Default fallback
    
    def detect_with_chardet(self, file_path: str) -> Optional[str]:
        """Detect encoding using chardet"""
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            if result['confidence'] > 0.7:
                return result['encoding']
        return None
```

### 2. BOM Detection
```python
class BOMDetector:
    def __init__(self):
        self.bom_marks = {
            codecs.BOM_UTF8: 'utf-8-sig',
            codecs.BOM_UTF16_LE: 'utf-16-le',
            codecs.BOM_UTF16_BE: 'utf-16-be',
            codecs.BOM_UTF32_LE: 'utf-32-le',
            codecs.BOM_UTF32_BE: 'utf-32-be'
        }
    
    def detect_bom(self, file_path: str) -> Optional[str]:
        """Detect encoding from BOM marker"""
        with open(file_path, 'rb') as f:
            raw = f.read(4)
            for bom, encoding in self.bom_marks.items():
                if raw.startswith(bom):
                    return encoding
        return None
```

## Encoding Conversion

### 1. Safe Conversion
```python
class EncodingConverter:
    def convert_encoding(
        self,
        input_path: str,
        output_path: str,
        source_encoding: str,
        target_encoding: str = 'utf-8'
    ) -> bool:
        """Convert file from one encoding to another"""
        try:
            with open(input_path, 'r', encoding=source_encoding) as f:
                content = f.read()
            
            with open(output_path, 'w', encoding=target_encoding) as f:
                f.write(content)
            return True
        except UnicodeError as e:
            logging.error(f"Encoding conversion failed: {str(e)}")
            return False
```

### 2. Streaming Conversion
```python
class StreamingConverter:
    def convert_large_file(
        self,
        input_path: str,
        output_path: str,
        source_encoding: str,
        target_encoding: str = 'utf-8',
        buffer_size: int = 65536
    ):
        """Convert large files using streaming"""
        with open(input_path, 'r', encoding=source_encoding) as fin, \
             open(output_path, 'w', encoding=target_encoding) as fout:
            while True:
                chunk = fin.read(buffer_size)
                if not chunk:
                    break
                fout.write(chunk)
```

## Encoding Validation

### 1. Content Validation
```python
class EncodingValidator:
    def validate_encoding(
        self,
        file_path: str,
        encoding: str
    ) -> ValidationResult:
        """Validate file can be read with specified encoding"""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                # Try reading the entire file
                f.read()
            return ValidationResult(True)
        except UnicodeError as e:
            return ValidationResult(
                False,
                str(e)
            )
    
    def validate_content(
        self,
        content: str,
        encoding: str
    ) -> ValidationResult:
        """Validate content can be encoded"""
        try:
            # Try encoding and decoding
            encoded = content.encode(encoding)
            decoded = encoded.decode(encoding)
            # Verify no data loss
            if decoded == content:
                return ValidationResult(True)
            return ValidationResult(
                False,
                "Data loss during encoding"
            )
        except UnicodeError as e:
            return ValidationResult(
                False,
                str(e)
            )
```

### 2. Character Set Validation
```python
class CharsetValidator:
    def __init__(self):
        self.charset_patterns = {
            'ascii': re.compile(r'^[\x00-\x7F]*$'),
            'latin1': re.compile(r'^[\x00-\xFF]*$')
        }
    
    def validate_charset(
        self,
        text: str,
        charset: str
    ) -> bool:
        """Validate text contains only characters from charset"""
        pattern = self.charset_patterns.get(charset)
        if pattern:
            return bool(pattern.match(text))
        try:
            text.encode(charset)
            return True
        except UnicodeError:
            return False
```

## Error Handling

### 1. Error Recovery
```python
class EncodingErrorHandler:
    def handle_decode_error(
        self,
        input_bytes: bytes,
        encoding: str
    ) -> str:
        """Handle decoding errors with fallback strategies"""
        strategies = [
            ('strict', lambda: input_bytes.decode(encoding, 'strict')),
            ('replace', lambda: input_bytes.decode(encoding, 'replace')),
            ('ignore', lambda: input_bytes.decode(encoding, 'ignore')),
            ('fallback', lambda: input_bytes.decode('latin1'))
        ]
        
        for name, strategy in strategies:
            try:
                return strategy()
            except UnicodeError:
                continue
        
        raise UnicodeError("All decoding strategies failed")
```

### 2. Error Reporting
```python
@dataclass
class EncodingError:
    position: int
    bytes_data: bytes
    error_type: str
    message: str

class EncodingErrorCollector:
    def collect_errors(
        self,
        file_path: str,
        encoding: str
    ) -> List[EncodingError]:
        """Collect all encoding errors in file"""
        errors = []
        with open(file_path, 'rb') as f:
            data = f.read()
            try:
                data.decode(encoding)
            except UnicodeError as e:
                errors.append(
                    EncodingError(
                        position=e.start,
                        bytes_data=data[e.start:e.end],
                        error_type=type(e).__name__,
                        message=str(e)
                    )
                )
        return errors
```

## Performance Optimization

### 1. Efficient Reading
```python
class EfficientReader:
    def read_encoded_file(
        self,
        file_path: str,
        encoding: str,
        chunk_size: int = 65536
    ) -> Iterator[str]:
        """Read encoded file efficiently"""
        with open(file_path, 'rb') as f:
            decoder = codecs.getincrementaldecoder(encoding)()
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield decoder.decode(chunk)
            yield decoder.decode(b'', final=True)
```

### 2. Memory Management
```python
class MemoryEfficientConverter:
    def convert_with_memory_limit(
        self,
        input_path: str,
        output_path: str,
        source_encoding: str,
        target_encoding: str,
        memory_limit: int = 1024 * 1024  # 1MB
    ):
        """Convert file with memory usage limit"""
        chunk_size = memory_limit // 4  # Leave room for overhead
        
        with open(input_path, 'rb') as fin, \
             open(output_path, 'wb') as fout:
            
            decoder = codecs.getincrementaldecoder(source_encoding)()
            encoder = codecs.getincrementalencoder(target_encoding)()
            
            while True:
                chunk = fin.read(chunk_size)
                if not chunk:
                    break
                
                # Decode and encode in chunks
                decoded = decoder.decode(chunk)
                encoded = encoder.encode(decoded)
                fout.write(encoded)
            
            # Handle final chunks
            decoded = decoder.decode(b'', final=True)
            encoded = encoder.encode(decoded, final=True)
            fout.write(encoded)
```

## Best Practices

### 1. Encoding Handling
- Always specify encodings explicitly
- Use UTF-8 as default encoding
- Handle BOM markers correctly
- Implement fallback strategies
- Validate before converting

### 2. Error Management
- Implement proper error handling
- Collect detailed error information
- Provide clear error messages
- Use appropriate error recovery
- Log encoding issues

### 3. Performance
- Use streaming for large files
- Implement memory management
- Use efficient algorithms
- Cache encoding detection results
- Monitor performance metrics

### 4. Data Integrity
- Validate data after conversion
- Implement checksums
- Verify character sets
- Handle special characters
- Preserve metadata 