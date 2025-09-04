# Sheri File Server

A modular, feature-rich HTTP file server with web interface for uploading, browsing, viewing, and downloading files.

## Features

- **File Upload**: Web-based file upload with multiple file support
- **Directory Browsing**: Navigate through server directories with breadcrumb navigation
- **File Viewing**: View text files in browser with syntax highlighting (VSCode-like interface)
- **File Download**: Download individual files or entire folders as ZIP archives
- **Security**: HTTP Basic Authentication and path traversal protection
- **Responsive Design**: Mobile-friendly interface
- **Directory Selection**: Choose browse directory at startup

## Files Structure

```
enhanced_file_server/
├── server.py          # Main server file
├── config.py          # Configuration settings
├── utils.py           # Utility functions
├── templates.py       # HTML template renderer
├── static/
│   └── style.css      # External CSS file (optional)
├── uploads/           # Upload directory (created automatically)
└── README.md          # This file
```

## Quick Setup

1. **Download all files** and place them in a directory
2. **Run the server**:
   ```bash
   python server.py
   ```
3. **Select directory** when prompted (options: current dir, home dir, or custom path)
4. **Access the server** at: http://192.168.0.186:8000
5. **Login** with username: `admin`, password: `your_secure_password`

## Configuration

Edit `config.py` to customize:

```python
PORT = 8000                           # Server port
USERNAME = "admin"                    # Login username
PASSWORD = "your_secure_password"     # Change this!
UPLOAD_DIR = "./uploads"              # Upload directory
HOST = "0.0.0.0"                     # Listen on all interfaces
```

## Usage

### Main Dashboard
- Access at: `http://192.168.0.186:8000/`
- Shows server info and navigation to upload/browse

### File Upload
- Access at: `http://192.168.0.186:8000/upload`
- Upload single or multiple files
- View previously uploaded files

### File Browser
- Access at: `http://192.168.0.186:8000/browse`
- Navigate directories with breadcrumb navigation
- View, download, or ZIP folders

### File Viewer
- Click "View" button on text files
- Syntax highlighting for 25+ programming languages
- Features: line numbers, word wrap, copy to clipboard, font size control
- Supports files up to 10MB

## Supported File Types for Viewing

Text files with syntax highlighting support:
- **Programming**: .py, .js, .html, .css, .java, .cpp, .go, .rs, .php, .rb
- **Data**: .json, .xml, .yml, .yaml, .csv, .sql
- **Config**: .ini, .cfg, .conf, .env, .toml
- **Documentation**: .md, .txt, .log
- **Scripts**: .sh, .bat, .ps1

## Security Features

- **HTTP Basic Authentication**: Username/password protection
- **Path Traversal Protection**: Prevents access outside allowed directories
- **Directory Restriction**: Only browse within selected directory
- **Safe File Handling**: Validates file paths and extensions

## API Endpoints

- `GET /` - Main dashboard
- `GET /upload` - Upload page
- `POST /upload` - Handle file upload
- `GET /browse/[path]` - Browse directory
- `GET /view/[file]` - View file content
- `GET /download/[file]` - Download file
- `GET /zip/[folder]` - Download folder as ZIP
- `GET /uploads/[file]` - Serve uploaded file

## Customization

### External CSS
Place CSS in `static/style.css` for custom styling. The server will automatically use it if present.

### Templates
Modify `templates.py` to customize HTML templates and styling.

### File Type Support
Add new file extensions and languages in `config.py`:
```python
TEXT_EXTENSIONS.add('.newext')
LANGUAGE_MAP['.newext'] = 'language-name'
FILE_ICONS['.newext'] = '🔗'
```

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Troubleshooting

1. **Permission Errors**: Ensure write access to upload directory
2. **Port Already in Use**: Change PORT in config.py
3. **Large Files**: Increase MAX_VIEW_FILE_SIZE for viewing larger text files
4. **CSS Not Loading**: Ensure static/style.css exists or templates will use inline CSS

## Security Notes

- **Change Default Password**: Update PASSWORD in config.py
- **Network Access**: Server listens on all interfaces (0.0.0.0)
- **HTTPS**: Consider adding HTTPS for production use
- **Firewall**: Restrict access to trusted networks

## Development

The modular structure makes it easy to extend:
- Add new routes in `server.py`
- Add utility functions in `utils.py`
- Create new templates in `templates.py`
- Modify configuration in `config.py`

## License

Free to use and modify for personal and commercial projects.
