"""
Utility functions for the Enhanced File Server
Contains helper functions for file operations, security, and formatting
"""

import os
import mimetypes
import math
from config import *

class FileServerUtils:
    def __init__(self):
        pass
    
    def is_safe_path(self, file_path, browse_root):
        """Check if a file path is within the allowed directory"""
        try:
            real_path = os.path.realpath(file_path)
            real_browse_root = os.path.realpath(browse_root)
            return real_path.startswith(real_browse_root)
        except Exception:
            return False
    
    def is_text_file(self, file_path):
        """Check if a file is viewable as text"""
        try:
            # Check file size (don't try to view very large files)
            if os.path.getsize(file_path) > MAX_VIEW_FILE_SIZE:
                return False
            
            # Check by extension first
            ext = os.path.splitext(file_path)[1].lower()
            if ext in TEXT_EXTENSIONS:
                return True
            
            # Check MIME type
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type and mime_type.startswith('text/'):
                return True
            
            # Try to detect if file is text by reading a small portion
            try:
                with open(file_path, 'rb') as f:
                    sample = f.read(1024)
                    # Check if the sample contains mostly printable characters
                    if not sample:
                        return True  # Empty file
                    
                    # Try to decode as UTF-8
                    try:
                        sample.decode('utf-8')
                        return True
                    except UnicodeDecodeError:
                        pass
                    
                    # Check if it's mostly printable ASCII
                    printable_chars = sum(1 for byte in sample if 32 <= byte <= 126 or byte in (9, 10, 13))
                    return printable_chars / len(sample) > 0.7
                    
            except Exception:
                return False
                
        except Exception:
            return False
    
    def get_language_for_syntax_highlighting(self, file_path):
        """Determine the programming language for syntax highlighting"""
        ext = os.path.splitext(file_path)[1].lower()
        return LANGUAGE_MAP.get(ext, 'text')
    
    def read_file_content(self, file_path):
        """Read file content with encoding fallback"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception:
                return None
        except Exception:
            return None
    
    def get_file_icon(self, ext):
        """Get appropriate icon for file extension"""
        return FILE_ICONS.get(ext, '📎')
    
    def format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"
    
    def generate_breadcrumbs(self, rel_path):
        """Generate breadcrumb navigation"""
        if not rel_path or rel_path == '.':
            return '<a href="/browse" class="breadcrumb">🏠 Home</a>'
        
        parts = rel_path.split('/')
        breadcrumbs = ['<a href="/browse" class="breadcrumb">🏠 Home</a>']
        
        current_path = ""
        for part in parts:
            current_path = f"{current_path}/{part}" if current_path else part
            breadcrumbs.append(f'<a href="/browse/{current_path}" class="breadcrumb">{part}</a>')
        
        return ' / '.join(breadcrumbs)
    
    def generate_file_breadcrumbs(self, rel_path):
        """Generate breadcrumb navigation for file viewer"""
        dir_path = os.path.dirname(rel_path) if os.path.dirname(rel_path) != '.' else ''
        filename = os.path.basename(rel_path)
        
        breadcrumbs = ['<a href="/browse" class="breadcrumb">🏠 Home</a>']
        
        if dir_path:
            parts = dir_path.split('/')
            current_path = ""
            for part in parts:
                current_path = f"{current_path}/{part}" if current_path else part
                breadcrumbs.append(f'<a href="/browse/{current_path}" class="breadcrumb">{part}</a>')
        
        breadcrumbs.append(f'<span class="breadcrumb current">📄 {filename}</span>')
        return ' / '.join(breadcrumbs)