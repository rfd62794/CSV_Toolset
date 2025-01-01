import re

class PatternProcessor:
    """Handles text pattern matching and formatting"""
    
    @staticmethod
    def compile_pattern(pattern, flags=0):
        """Safely compiles a regex pattern"""
        try:
            return re.compile(pattern, flags)
        except re.error as e:
            return None, f"Invalid pattern: {str(e)}"
    
    @staticmethod
    def find_matches(text, pattern, group_index=0):
        """Finds all matches in text using pattern"""
        try:
            matches = pattern.finditer(text)
            return [m.group(group_index) for m in matches]
        except (AttributeError, IndexError):
            return []
    
    @staticmethod
    def clean_text(text, chars_to_remove):
        """Removes specified characters from text"""
        if not text:
            return text
        return re.sub(f'[{re.escape(chars_to_remove)}]', '', text) 