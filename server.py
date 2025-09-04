#!/usr/bin/env python3
"""
Enhanced File Server with Modular Architecture
Main server file that handles HTTP requests and routing
"""

import http.server
import socketserver
import os
import cgi
import base64
import urllib.parse
from pathlib import Path
import mimetypes
import zipfile
import tempfile
import html
import datetime

# Import local modules
from config import *
from utils import FileServerUtils
from templates import TemplateRenderer

class FileServer(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.utils = FileServerUtils()
        self.template_renderer = TemplateRenderer()
        super().__init__(*args, **kwargs)
    
    def do_authhead(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="File Server"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def check_auth(self):
        if 'Authorization' not in self.headers:
            return False
        
        auth_header = self.headers['Authorization']
        if not auth_header.startswith('Basic '):
            return False
        
        try:
            credentials = base64.b64decode(auth_header[6:]).decode('utf-8')
            username, password = credentials.split(':', 1)
            return username == USERNAME and password == PASSWORD
        except:
            return False
    
    def do_GET(self):
        if not self.check_auth():
            self.do_authhead()
            self.wfile.write(b'Authentication required')
            return
        
        parsed_path = urllib.parse.urlparse(self.path)
        path = urllib.parse.unquote(parsed_path.path)
        
        # Route requests
        if path == '/' or path == '':
            self.send_main_page()
        elif path == '/upload':
            self.send_upload_page()
        elif path.startswith('/browse'):
            browse_path = path.replace('/browse', '', 1)
            if browse_path == '' or browse_path == '/':
                browse_path = BROWSE_ROOT
            else:
                browse_path = os.path.join(BROWSE_ROOT, browse_path.lstrip('/'))
            self.browse_directory(browse_path)
        elif path.startswith('/view'):
            file_path = path.replace('/view', '', 1)
            self.view_file(os.path.join(BROWSE_ROOT, file_path.lstrip('/')))
        elif path.startswith('/download'):
            file_path = path.replace('/download', '', 1)
            self.download_file(os.path.join(BROWSE_ROOT, file_path.lstrip('/')))
        elif path.startswith('/zip'):
            folder_path = path.replace('/zip', '', 1)
            self.download_folder_as_zip(os.path.join(BROWSE_ROOT, folder_path.lstrip('/')))
        elif path.startswith('/uploads'):
            file_path = path.replace('/uploads', '', 1)
            self.serve_uploaded_file(os.path.join(UPLOAD_DIR, file_path.lstrip('/')))
        else:
            self.send_error(404)
    
    def do_POST(self):
        if not self.check_auth():
            self.do_authhead()
            self.wfile.write(b'Authentication required')
            return
        
        if self.path == '/upload':
            self.handle_upload()
        else:
            self.send_error(404)
    
    def send_main_page(self):
        """Send main dashboard page"""
        try:
            uploaded_files = os.listdir(UPLOAD_DIR) if os.path.exists(UPLOAD_DIR) else []
            uploaded_count = len([f for f in uploaded_files if os.path.isfile(os.path.join(UPLOAD_DIR, f))])
            
            context = {
                'uploaded_count': uploaded_count,
                'browse_root': BROWSE_ROOT,
                'server_address': f"{SERVER_IP}:{PORT}",
                'upload_dir': os.path.abspath(UPLOAD_DIR),
            }
            
            html_content = self.template_renderer.render_dashboard(context)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Error loading dashboard: {str(e)}")
    
    def browse_directory(self, dir_path):
        """Browse and display directory contents"""
        try:
            # Security check
            if not self.utils.is_safe_path(dir_path, BROWSE_ROOT):
                self.send_error(403, "Access denied - path outside allowed directory")
                return
            
            if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
                self.send_error(404, "Directory not found")
                return
            
            # Get relative path for display
            rel_path = os.path.relpath(dir_path, BROWSE_ROOT)
            if rel_path == '.':
                rel_path = ''
            
            # Get directory contents
            try:
                items = sorted(os.listdir(dir_path))
            except PermissionError:
                self.send_error(403, "Permission denied")
                return
            
            # Process directory contents
            directories = []
            files = []
            
            for item in items:
                item_path = os.path.join(dir_path, item)
                try:
                    if os.path.isdir(item_path):
                        directories.append(item)
                    elif os.path.isfile(item_path):
                        file_info = {
                            'name': item,
                            'size': self.utils.format_file_size(os.path.getsize(item_path)),
                            'icon': self.utils.get_file_icon(os.path.splitext(item)[1].lower()),
                            'can_view': self.utils.is_text_file(item_path),
                            'path': f"{rel_path}/{item}" if rel_path else item
                        }
                        files.append(file_info)
                except (OSError, PermissionError):
                    continue
            
            context = {
                'rel_path': rel_path,
                'breadcrumbs': self.utils.generate_breadcrumbs(rel_path),
                'directories': directories,
                'files': files,
                'has_parent': bool(rel_path)
            }
            
            html_content = self.template_renderer.render_browser(context)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Error browsing directory: {str(e)}")
    
    def view_file(self, file_path):
        """Display file content in browser with syntax highlighting"""
        try:
            # Security check
            if not self.utils.is_safe_path(file_path, BROWSE_ROOT):
                self.send_error(403, "Access denied")
                return
            
            if not os.path.exists(file_path) or not os.path.isfile(file_path):
                self.send_error(404, "File not found")
                return
            
            if not self.utils.is_text_file(file_path):
                # Redirect to download for binary files
                rel_path = os.path.relpath(file_path, BROWSE_ROOT)
                download_url = f"/download/{rel_path}"
                self.send_response(302)
                self.send_header('Location', download_url)
                self.end_headers()
                return
            
            # Read file content
            content = self.utils.read_file_content(file_path)
            if content is None:
                self.send_error(500, "Could not read file with any encoding")
                return
            
            # Get file info
            filename = os.path.basename(file_path)
            file_size = self.utils.format_file_size(os.path.getsize(file_path))
            rel_path = os.path.relpath(file_path, BROWSE_ROOT)
            parent_dir = os.path.dirname(rel_path) if os.path.dirname(rel_path) != '.' else ''
            language = self.utils.get_language_for_syntax_highlighting(file_path)
            
            context = {
                'filename': filename,
                'file_size': file_size,
                'language': language,
                'content': html.escape(content),
                'rel_path': rel_path,
                'parent_dir': parent_dir,
                'breadcrumbs': self.utils.generate_file_breadcrumbs(rel_path)
            }
            
            html_content = self.template_renderer.render_file_viewer(context)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Error viewing file: {str(e)}")
    
    def download_file(self, file_path):
        """Download a single file"""
        try:
            if not self.utils.is_safe_path(file_path, BROWSE_ROOT):
                self.send_error(403, "Access denied")
                return
            
            if not os.path.exists(file_path) or not os.path.isfile(file_path):
                self.send_error(404, "File not found")
                return
            
            # Determine content type
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'application/octet-stream'
            
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.send_header('Content-Length', str(file_size))
            self.end_headers()
            
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    
        except Exception as e:
            self.send_error(500, f"Error downloading file: {str(e)}")
    
    def download_folder_as_zip(self, folder_path):
        """Download folder as ZIP archive"""
        try:
            if not self.utils.is_safe_path(folder_path, BROWSE_ROOT):
                self.send_error(403, "Access denied")
                return
            
            if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
                self.send_error(404, "Folder not found")
                return
            
            folder_name = os.path.basename(folder_path)
            zip_filename = f"{folder_name}.zip"
            
            # Create temporary ZIP file
            with tempfile.NamedTemporaryFile(delete=False) as temp_zip:
                with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(folder_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, folder_path)
                            zipf.write(file_path, arcname)
                
                # Send ZIP file
                zip_size = os.path.getsize(temp_zip.name)
                self.send_response(200)
                self.send_header('Content-Type', 'application/zip')
                self.send_header('Content-Disposition', f'attachment; filename="{zip_filename}"')
                self.send_header('Content-Length', str(zip_size))
                self.end_headers()
                
                with open(temp_zip.name, 'rb') as f:
                    while True:
                        chunk = f.read(8192)
                        if not chunk:
                            break
                        self.wfile.write(chunk)
                
                # Clean up temporary file
                os.unlink(temp_zip.name)
                
        except Exception as e:
            self.send_error(500, f"Error creating ZIP: {str(e)}")
    
    def serve_uploaded_file(self, file_path):
        """Serve uploaded files"""
        try:
            if not os.path.exists(file_path) or not os.path.isfile(file_path):
                self.send_error(404, "File not found")
                return
            
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'application/octet-stream'
            
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.send_header('Content-Length', str(file_size))
            self.end_headers()
            
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    
        except Exception as e:
            self.send_error(500, f"Error serving file: {str(e)}")
    
    def send_upload_page(self):
        """Send file upload page"""
        try:
            uploaded_files = []
            if os.path.exists(UPLOAD_DIR):
                for filename in sorted(os.listdir(UPLOAD_DIR)):
                    filepath = os.path.join(UPLOAD_DIR, filename)
                    if os.path.isfile(filepath):
                        size = self.utils.format_file_size(os.path.getsize(filepath))
                        uploaded_files.append({'name': filename, 'size': size})
            
            context = {
                'uploaded_files': uploaded_files,
                'files_count': len(uploaded_files)
            }
            
            html_content = self.template_renderer.render_upload_page(context)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Error loading upload page: {str(e)}")
    
    def handle_upload(self):
        """Handle file upload"""
        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            
            if "files" not in form:
                raise ValueError("No files uploaded")
            
            uploaded_files = []
            files_field = form["files"]
            
            # Handle single or multiple files
            if isinstance(files_field, list):
                files_to_process = files_field
            else:
                files_to_process = [files_field]
            
            for file_item in files_to_process:
                if hasattr(file_item, 'filename') and file_item.filename:
                    # Save the uploaded file
                    safe_filename = os.path.basename(file_item.filename)
                    file_path = os.path.join(UPLOAD_DIR, safe_filename)
                    
                    with open(file_path, 'wb') as f:
                        f.write(file_item.file.read())
                    
                    uploaded_files.append(safe_filename)
            
            if not uploaded_files:
                raise ValueError("No valid files uploaded")
            
            context = {
                'uploaded_files': uploaded_files,
                'files_count': len(uploaded_files)
            }
            
            html_content = self.template_renderer.render_upload_success(context)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
        except Exception as e:
            self.send_error(400, f"Upload failed: {str(e)}")

def get_directory_from_user():
    """Prompt user to select the browse directory during startup"""
    print("🔧 SERVER CONFIGURATION")
    print("=" * 50)
    
    while True:
        print("\n📁 Select Browse Directory Options:")
        print("1. Use current directory:", os.getcwd())
        print("2. Use home directory:", os.path.expanduser("~"))
        print("3. Enter custom directory path")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            selected_dir = os.getcwd()
            break
        elif choice == "2":
            selected_dir = os.path.expanduser("~")
            break
        elif choice == "3":
            while True:
                custom_path = input("Enter full directory path: ").strip()
                if os.path.exists(custom_path) and os.path.isdir(custom_path):
                    selected_dir = os.path.abspath(custom_path)
                    break
                else:
                    print("❌ Invalid directory path. Please try again.")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
    
    print(f"\n✅ Selected browse directory: {selected_dir}")
    
    # Confirm the selection
    confirm = input("Proceed with this directory? (y/N): ").strip().lower()
    if confirm in ['y', 'yes']:
        return selected_dir
    else:
        print("Configuration cancelled.")
        return None

def main():
    """Main function to start the server"""
    global BROWSE_ROOT
    
    # Get directory selection from user
    BROWSE_ROOT = get_directory_from_user()
    
    if BROWSE_ROOT is None:
        print("Exiting...")
        return
    
    print("\n" + "=" * 70)
    print("🚀 ENHANCED FILE SERVER STARTING")
    print("=" * 70)
    print(f"📂 Upload Directory: {os.path.abspath(UPLOAD_DIR)}")
    print(f"📁 Browse Directory: {BROWSE_ROOT}")
    print(f"🌐 Server Address: {SERVER_IP}:{PORT}")
    print(f"📝 Username: {USERNAME}")
    print(f"🔒 Password: {PASSWORD}")
    print("=" * 70)
    print("✨ FEATURES:")
    print("   📤 File Upload")
    print("   📁 Directory Browsing") 
    print("   👁️  File Viewing (with syntax highlighting)")
    print("   ⬇️  File Downloads")
    print("   📦 Folder ZIP Downloads")
    print("   🔒 Password Protection")
    print("=" * 70)
    
    # Check if browse directory exists
    if not os.path.exists(BROWSE_ROOT):
        print(f"⚠️  WARNING: Browse directory '{BROWSE_ROOT}' does not exist!")
        print(f"   Please create it or restart the server.")
        return
    else:
        print(f"✅ Browse directory verified: {BROWSE_ROOT}")
    
    # Create upload directory and sample file
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    if not os.listdir(UPLOAD_DIR):
        sample_file = os.path.join(UPLOAD_DIR, "README.txt")
        with open(sample_file, 'w') as f:
            f.write("🌟 Welcome to Enhanced File Server!\n\n")
            f.write("FEATURES:\n")
            f.write("• Upload files through the web interface\n")
            f.write("• Browse and download files from server directories\n")  
            f.write("• View text files directly in browser with syntax highlighting\n")
            f.write("• Download entire folders as ZIP archives\n")
            f.write("• Secure password protection\n")
            f.write("• Directory access control\n\n")
            f.write(f"Server started: {datetime.datetime.now()}\n")
            f.write(f"Browse directory: {BROWSE_ROOT}\n")
        print(f"📝 Created sample file: {sample_file}")
    
    print("\n🎯 READY! Open your browser and navigate to:")
    print(f"   🏠 Main Dashboard: {SERVER_IP}:{PORT}")
    print(f"   📤 Upload Page: {SERVER_IP}:{PORT}/upload") 
    print(f"   📁 Browse Files: {SERVER_IP}:{PORT}/browse")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("-" * 70)
    
    with socketserver.TCPServer((HOST, PORT), FileServer) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n" + "=" * 70)
            print("🛑 SERVER STOPPED GRACEFULLY")
            print("=" * 70)

if __name__ == "__main__":
    main()
