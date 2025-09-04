"""
Configuration file for the Enhanced File Server
Contains all server settings and constants
"""

# Server Configuration
PORT = 8000
USERNAME = "Vajra"
PASSWORD = "Anja"  # Change this!
UPLOAD_DIR = "./uploads"  # Directory for uploads
HOST = "0.0.0.0"  # Listen on all interfaces

# This will be set during startup
BROWSE_ROOT = None

# IP Detection
import socket

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Connect to a remote address to determine local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Google DNS
            return s.getsockname()[0]
    except Exception:
        # Fallback methods
        try:
            return socket.gethostbyname(socket.gethostname())
        except:
            return "127.0.0.1"  # Final fallback

# Get system IP
SERVER_IP = get_local_ip()

# File type mappings for syntax highlighting
LANGUAGE_MAP = {
    '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
    '.html': 'html', '.htm': 'html', '.css': 'css', '.scss': 'scss',
    '.json': 'json', '.xml': 'xml', '.yml': 'yaml', '.yaml': 'yaml',
    '.sql': 'sql', '.sh': 'bash', '.bat': 'batch', '.ps1': 'powershell',
    '.php': 'php', '.rb': 'ruby', '.go': 'go', '.rs': 'rust',
    '.c': 'c', '.cpp': 'cpp', '.h': 'c', '.hpp': 'cpp',
    '.java': 'java', '.kt': 'kotlin', '.swift': 'swift',
    '.vue': 'vue', '.jsx': 'javascript', '.tsx': 'typescript',
    '.md': 'markdown', '.ini': 'ini', '.cfg': 'ini', '.conf': 'ini',
    '.log': 'log', '.csv': 'csv', '.dockerfile': 'dockerfile',
    '.makefile': 'makefile', '.toml': 'toml'
}

# File extensions that can be viewed as text
TEXT_EXTENSIONS = {
    '.txt', '.py', '.js', '.html', '.htm', '.css', '.json', '.xml', 
    '.md', '.yml', '.yaml', '.ini', '.cfg', '.conf', '.log', 
    '.sql', '.sh', '.bat', '.ps1', '.php', '.rb', '.go', '.rs',
    '.c', '.cpp', '.h', '.hpp', '.java', '.kt', '.swift', '.ts',
    '.vue', '.jsx', '.tsx', '.scss', '.sass', '.less', '.csv',
    '.env', '.gitignore', '.dockerfile', '.makefile', '.cmake',
    '.toml', '.properties', '.gradle', '.pom'
}

# File icons mapping
FILE_ICONS = {
    '.txt': '📄', '.doc': '📃', '.docx': '📃', '.pdf': '📕',
    '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️',
    '.mp4': '🎬', '.avi': '🎬', '.mov': '🎬',
    '.mp3': '🎵', '.wav': '🎵', '.flac': '🎵',
    '.zip': '📦', '.rar': '📦', '.7z': '📦',
    '.py': '🐍', '.js': '📜', '.html': '🌐', '.css': '🎨',
    '.xlsx': '📊', '.csv': '📊',
}

# Maximum file size for viewing (10MB)
MAX_VIEW_FILE_SIZE = 10 * 1024 * 1024
