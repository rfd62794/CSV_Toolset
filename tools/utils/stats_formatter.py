class StatsFormatter:
    """Handles formatting of statistics for display"""
    
    @staticmethod
    def format_file_stats(stats):
        """Formats basic file statistics"""
        return [
            "File Statistics:",
            f"- Size: {stats['size']:,} bytes",
            f"- Encoding: {stats['encoding']}",
            f"- Rows: {stats['total_rows']:,}",
            f"- Columns: {stats['total_columns']:,}"
        ]
    
    @staticmethod
    def format_column_stats(column_stats):
        """Formats column statistics"""
        lines = ["Column Information:"]
        for col, stats in column_stats.items():
            lines.extend([
                f"\n{col}:",
                f"- Type: {stats['type']}",
                f"- Unique Values: {stats['unique_values']:,}",
                f"- Null Count: {stats['null_count']:,}",
                "- Sample Values: " + ", ".join(str(v) for v in stats['sample_values'])
            ])
        return lines
    
    @classmethod
    def format_full_stats(cls, stats):
        """Formats complete statistics"""
        lines = cls.format_file_stats(stats['file_info'])
        lines.append("")  # Add spacing
        lines.extend(cls.format_column_stats(stats['column_stats']))
        return '\n'.join(lines) 