"""
Template renderer for the Enhanced File Server
Contains HTML templates and rendering functions
"""

import os
from config import PORT

class TemplateRenderer:
    def __init__(self):
        pass
    
    def get_base_css(self):
        """Load CSS from external file or return inline CSS"""
        css_file = os.path.join(os.path.dirname(__file__), 'static', 'style.css')
        if os.path.exists(css_file):
            with open(css_file, 'r') as f:
                return f.read()
        else:
            # Fallback inline CSS
            return self.get_inline_css()
    
    def get_inline_css(self):
        """Inline CSS as fallback"""
        return """
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .header { 
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
            .header p { opacity: 0.9; font-size: 1.1rem; }
            .dashboard-grid { 
                display: grid; 
                grid-template-columns: 1fr 1fr; 
                gap: 20px; 
                padding: 30px;
            }
            .card {
                background: #f8f9fa;
                padding: 25px;
                border-radius: 8px;
                border-left: 4px solid #4CAF50;
                text-align: center;
            }
            .card h3 { color: #333; margin-bottom: 10px; }
            .card p { color: #666; margin-bottom: 20px; }
            .btn {
                display: inline-block;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 6px;
                font-weight: 500;
                transition: all 0.3s ease;
                border: none;
                cursor: pointer;
                font-size: 14px;
            }
            .btn-primary { 
                background: linear-gradient(135deg, #4CAF50, #45a049);
                color: white;
            }
            .btn-secondary { 
                background: linear-gradient(135deg, #2196F3, #1976D2);
                color: white;
            }
            .btn-small {
                padding: 6px 12px;
                font-size: 12px;
                text-decoration: none;
                background: #4CAF50;
                color: white;
                border-radius: 4px;
                display: inline-block;
                margin: 2px;
            }
            .btn-view { background: #9C27B0; }
            .btn-download { background: #2196F3; }
            .btn-zip { background: #ff9800; }
            .btn-copy { background: #607D8B; }
            .btn:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
            .btn-small:hover { transform: translateY(-1px); }
            .toolbar { 
                padding: 20px 30px; 
                background: #f8f9fa; 
                border-bottom: 1px solid #e9ecef;
                display: flex;
                gap: 10px;
                align-items: center;
            }
            .path-info { 
                margin-left: auto; 
                color: #666; 
                font-family: monospace;
                background: white;
                padding: 8px 12px;
                border-radius: 4px;
            }
            .breadcrumbs { 
                margin-top: 10px;
                font-size: 14px;
            }
            .breadcrumb { 
                color: rgba(255,255,255,0.8); 
                text-decoration: none; 
                margin: 0 5px;
            }
            .breadcrumb:hover { color: white; }
            .breadcrumb.current { color: white; font-weight: bold; }
            .file-listing { padding: 30px; }
            .file-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                margin-bottom: 10px;
                transition: all 0.3s ease;
            }
            .file-item:hover { 
                background: #f8f9fa; 
                transform: translateY(-1px);
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            .file-item.folder { border-left: 4px solid #FFC107; }
            .file-item.file { border-left: 4px solid #2196F3; }
            .file-info { display: flex; align-items: center; gap: 15px; flex: 1; }
            .file-info .icon { font-size: 24px; }
            .file-info .name { font-weight: 500; color: #333; }
            .file-info .details { color: #666; font-size: 12px; }
            .actions { display: flex; gap: 8px; flex-wrap: wrap; }
            .upload-section { padding: 30px; }
            .upload-area {
                border: 2px dashed #4CAF50;
                border-radius: 8px;
                padding: 40px;
                text-align: center;
                background: #f9f9f9;
            }
            .file-input-wrapper { margin-bottom: 20px; }
            #fileInput { display: none; }
            .file-input-label {
                display: inline-block;
                padding: 40px;
                border: 2px dashed #ccc;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s ease;
                background: white;
                width: 100%;
                max-width: 400px;
            }
            .file-input-label:hover { 
                border-color: #4CAF50; 
                background: #f0f8f0;
            }
            .uploaded-section { 
                padding: 30px; 
                border-top: 1px solid #e9ecef;
                background: #f8f9fa;
            }
            .uploaded-files { 
                list-style: none; 
                max-height: 300px; 
                overflow-y: auto;
            }
            .uploaded-files li {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px;
                border-bottom: 1px solid #e9ecef;
            }
            .uploaded-files li:last-child { border-bottom: none; }
            .file-name { flex: 1; font-weight: 500; }
            .file-size { color: #666; font-size: 12px; margin-right: 10px; }
            .info-section { 
                padding: 30px; 
                background: #f8f9fa; 
                border-top: 1px solid #e9ecef;
            }
            .info-section h4 { margin-bottom: 15px; color: #333; }
            .info-section ul { list-style-position: inside; }
            .info-section li { margin-bottom: 8px; color: #666; }
            .success-message { 
                padding: 30px; 
                text-align: center;
                background: #d4edda;
                border: 1px solid #c3e6cb;
                border-radius: 8px;
                margin: 30px;
            }
            .actions { 
                text-align: center; 
                padding: 30px;
                display: flex;
                gap: 15px;
                justify-content: center;
            }
            .empty-dir { 
                text-align: center; 
                color: #666; 
                padding: 40px;
                font-style: italic;
            }
            .no-files { 
                text-align: center; 
                color: #666; 
                font-style: italic; 
                padding: 20px;
            }
            .stats { 
                font-size: 12px; 
                color: #666; 
                margin-top: 10px;
                font-style: italic;
            }
            @media (max-width: 768px) {
                .dashboard-grid { grid-template-columns: 1fr; }
                .toolbar { flex-direction: column; align-items: stretch; }
                .actions { flex-direction: column; }
                .file-item { flex-direction: column; gap: 10px; text-align: center; }
            }
        """
    
    def get_viewer_css(self):
        """CSS specific to file viewer"""
        return """
            .file-info-bar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px 30px;
                background: #f8f9fa;
                border-bottom: 1px solid #e9ecef;
                flex-wrap: wrap;
                gap: 15px;
            }
            .file-details {
                display: flex;
                flex-direction: column;
                gap: 5px;
            }
            .filename {
                font-weight: bold;
                font-size: 1.2rem;
                color: #333;
            }
            .file-meta {
                font-size: 0.9rem;
                color: #666;
            }
            .file-actions {
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
            }
            .file-viewer {
                display: flex;
                background: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                max-height: 80vh;
                overflow: auto;
            }
            .line-numbers {
                background: #252526;
                color: #858585;
                padding: 20px 10px;
                font-size: 14px;
                line-height: 1.6;
                min-width: 60px;
                text-align: right;
                user-select: none;
                border-right: 1px solid #3e3e42;
            }
            .line-number {
                display: block;
                height: 1.6em;
            }
            .code-content {
                flex: 1;
                margin: 0;
                padding: 20px;
                font-size: 14px;
                line-height: 1.6;
                white-space: pre;
                overflow-x: auto;
                background: transparent;
            }
            .viewer-controls {
                padding: 15px 30px;
                background: #f8f9fa;
                border-top: 1px solid #e9ecef;
                display: flex;
                gap: 20px;
                align-items: center;
                flex-wrap: wrap;
            }
            .viewer-controls label {
                display: flex;
                align-items: center;
                gap: 5px;
                cursor: pointer;
                font-size: 14px;
            }
            .viewer-controls select {
                padding: 4px 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            .hljs {
                background: #1e1e1e !important;
                color: #d4d4d4;
            }
            @media (max-width: 768px) {
                .file-info-bar {
                    flex-direction: column;
                    align-items: stretch;
                    text-align: center;
                }
                .file-actions {
                    justify-content: center;
                }
                .viewer-controls {
                    flex-direction: column;
                    align-items: stretch;
                    gap: 10px;
                }
                .line-numbers {
                    min-width: 40px;
                    padding: 20px 5px;
                }
                .code-content {
                    font-size: 12px;
                    padding: 20px 10px;
                }
            }
        """
    
    def render_dashboard(self, context):
        """Render the main dashboard page"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>File Server Dashboard</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                {self.get_base_css()}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>File Server Dashboard</h1>
                    <p>Upload files or browse/download from server directories</p>
                </div>
                
                <div class="dashboard-grid">
                    <div class="card">
                        <h3>Upload Files</h3>
                        <p>Upload files to the server for sharing</p>
                        <a href="/upload" class="btn btn-primary">Go to Upload</a>
                        <div class="stats">Uploaded files: {context['uploaded_count']}</div>
                    </div>
                    
                    <div class="card">
                        <h3>Browse & Download</h3>
                        <p>Browse server directories and download files</p>
                        <a href="/browse" class="btn btn-secondary">Browse Files</a>
                        <div class="stats">Root: {context['browse_root']}</div>
                    </div>
                </div>
                
                <div class="info-section">
                    <h4>Server Information</h4>
                    <ul>
                        <li><strong>Server Address:</strong> {context['server_address']}</li>
                        <li><strong>Upload Directory:</strong> {context['upload_dir']}</li>
                        <li><strong>Browse Directory:</strong> {context['browse_root']}</li>
                        <li><strong>Features:</strong> Upload, Download, File Viewing, Directory Browsing, ZIP Archives</li>
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """
    
    def render_browser(self, context):
        """Render the file browser page"""
        # Generate parent directory link
        parent_link = ""
        if context['has_parent']:
            parent_path = os.path.dirname(context['rel_path'])
            if parent_path == '.':
                parent_path = ''
            parent_link = f"""
            <div class="file-item folder">
                <div class="file-info">
                    <span class="icon">📁</span>
                    <span class="name">..</span>
                    <span class="details">Parent Directory</span>
                </div>
                <a href="/browse/{parent_path}" class="btn-small">Back</a>
            </div>
            """
        
        # Generate directories listing
        directories_html = ""
        for directory in context['directories']:
            browse_path = f"{context['rel_path']}/{directory}" if context['rel_path'] else directory
            directories_html += f"""
            <div class="file-item folder">
                <div class="file-info">
                    <span class="icon">📁</span>
                    <span class="name">{directory}</span>
                    <span class="details">Folder</span>
                </div>
                <div class="actions">
                    <a href="/browse/{browse_path}" class="btn-small">Open</a>
                    <a href="/zip/{browse_path}" class="btn-small btn-zip">ZIP</a>
                </div>
            </div>
            """
        
        # Generate files listing
        files_html = ""
        for file_info in context['files']:
            view_button = f'<a href="/view/{file_info["path"]}" class="btn-small btn-view">View</a>' if file_info['can_view'] else ''
            files_html += f"""
            <div class="file-item file">
                <div class="file-info">
                    <span class="icon">{file_info['icon']}</span>
                    <span class="name">{file_info['name']}</span>
                    <span class="details">{file_info['size']}</span>
                </div>
                <div class="actions">
                    {view_button}
                    <a href="/download/{file_info['path']}" class="btn-small btn-download">Download</a>
                </div>
            </div>
            """
        
        listing_html = parent_link + directories_html + files_html
        if not listing_html.strip():
            listing_html = "<p class='empty-dir'>This directory is empty or you don't have permission to view its contents.</p>"
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Browse: /{context['rel_path']}</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                {self.get_base_css()}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>File Browser</h1>
                    <div class="breadcrumbs">{context['breadcrumbs']}</div>
                </div>
                
                <div class="toolbar">
                    <a href="/" class="btn btn-primary">Home</a>
                    <a href="/upload" class="btn btn-secondary">Upload</a>
                    <span class="path-info">Current: /{context['rel_path'] or 'root'}</span>
                </div>
                
                <div class="file-listing">
                    {listing_html}
                </div>
            </div>
        </body>
        </html>
        """
    
    def render_file_viewer(self, context):
        """Render the file viewer page"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>View: {context['filename']}</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/vs-code-dark.min.css">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
            <style>
                {self.get_base_css()}
                {self.get_viewer_css()}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>File Viewer</h1>
                    <div class="breadcrumbs">{context['breadcrumbs']}</div>
                </div>
                
                <div class="file-info-bar">
                    <div class="file-details">
                        <span class="filename">{context['filename']}</span>
                        <span class="file-meta">Size: {context['file_size']} | Language: {context['language']}</span>
                    </div>
                    <div class="file-actions">
                        <button onclick="copyToClipboard()" class="btn-small btn-copy">Copy All</button>
                        <button onclick="selectAll()" class="btn-small">Select All</button>
                        <a href="/download/{context['rel_path']}" class="btn-small btn-download">Download</a>
                        <a href="/browse/{context['parent_dir']}" class="btn-small">Back to Folder</a>
                    </div>
                </div>
                
                <div class="file-viewer">
                    <div class="line-numbers" id="lineNumbers"></div>
                    <pre class="code-content"><code class="language-{context['language']}" id="codeContent">{context['content']}</code></pre>
                </div>
                
                <div class="viewer-controls">
                    <label>
                        <input type="checkbox" id="wrapLines" onchange="toggleWordWrap()"> Word Wrap
                    </label>
                    <label>
                        <input type="checkbox" id="showLineNumbers" checked onchange="toggleLineNumbers()"> Line Numbers
                    </label>
                    <select id="fontSize" onchange="changeFontSize()">
                        <option value="12">12px</option>
                        <option value="14" selected>14px</option>
                        <option value="16">16px</option>
                        <option value="18">18px</option>
                        <option value="20">20px</option>
                    </select>
                </div>
            </div>
            
            <script>
                // Initialize syntax highlighting
                hljs.highlightAll();
                
                // Generate line numbers
                function updateLineNumbers() {{
                    const code = document.getElementById('codeContent');
                    const lineNumbers = document.getElementById('lineNumbers');
                    const lines = code.textContent.split('\\n');
                    const lineNumbersHtml = lines.map((_, index) => 
                        `<span class="line-number">${{index + 1}}</span>`
                    ).join('');
                    lineNumbers.innerHTML = lineNumbersHtml;
                }}
                
                // Copy content to clipboard
                function copyToClipboard() {{
                    const code = document.getElementById('codeContent');
                    navigator.clipboard.writeText(code.textContent).then(() => {{
                        const btn = document.querySelector('.btn-copy');
                        const originalText = btn.textContent;
                        btn.textContent = 'Copied!';
                        btn.style.background = '#4CAF50';
                        setTimeout(() => {{
                            btn.textContent = originalText;
                            btn.style.background = '';
                        }}, 2000);
                    }});
                }}
                
                // Select all text
                function selectAll() {{
                    const code = document.getElementById('codeContent');
                    const selection = window.getSelection();
                    const range = document.createRange();
                    range.selectNodeContents(code);
                    selection.removeAllRanges();
                    selection.addRange(range);
                }}
                
                // Toggle word wrap
                function toggleWordWrap() {{
                    const code = document.querySelector('.code-content');
                    const checkbox = document.getElementById('wrapLines');
                    if (checkbox.checked) {{
                        code.style.whiteSpace = 'pre-wrap';
                        code.style.wordWrap = 'break-word';
                    }} else {{
                        code.style.whiteSpace = 'pre';
                        code.style.wordWrap = 'normal';
                    }}
                }}
                
                // Toggle line numbers
                function toggleLineNumbers() {{
                    const lineNumbers = document.getElementById('lineNumbers');
                    const checkbox = document.getElementById('showLineNumbers');
                    lineNumbers.style.display = checkbox.checked ? 'block' : 'none';
                }}
                
                // Change font size
                function changeFontSize() {{
                    const select = document.getElementById('fontSize');
                    const code = document.querySelector('.code-content');
                    const lineNumbers = document.getElementById('lineNumbers');
                    const size = select.value + 'px';
                    code.style.fontSize = size;
                    lineNumbers.style.fontSize = size;
                }}
                
                // Initialize line numbers
                updateLineNumbers();
                
                // Handle keyboard shortcuts
                document.addEventListener('keydown', function(e) {{
                    if (e.ctrlKey || e.metaKey) {{
                        switch(e.key) {{
                            case 'a':
                                e.preventDefault();
                                selectAll();
                                break;
                            case 'c':
                                // Let default copy work for selected text
                                break;
                        }}
                    }}
                }});
            </script>
        </body>
        </html>
        """
    
    def render_upload_page(self, context):
        """Render the upload page"""
        files_html = ""
        if context['uploaded_files']:
            files_html = "<ul class='uploaded-files'>"
            for file_info in context['uploaded_files']:
                files_html += f"""
                <li>
                    <span class="file-name">{file_info['name']}</span>
                    <span class="file-size">{file_info['size']}</span>
                    <a href="/uploads/{file_info['name']}" class="btn-small">Download</a>
                </li>
                """
            files_html += "</ul>"
        else:
            files_html = "<p class='no-files'>No uploaded files yet.</p>"
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Upload Files</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                {self.get_base_css()}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Upload Files</h1>
                    <p>Upload files to share with others</p>
                </div>
                
                <div class="toolbar">
                    <a href="/" class="btn btn-primary">Home</a>
                    <a href="/browse" class="btn btn-secondary">Browse Files</a>
                </div>
                
                <div class="upload-section">
                    <div class="upload-area">
                        <h3>Select Files to Upload</h3>
                        <form action="/upload" method="post" enctype="multipart/form-data" class="upload-form">
                            <div class="file-input-wrapper">
                                <input type="file" name="files" multiple accept="*/*" id="fileInput">
                                <label for="fileInput" class="file-input-label">
                                    Choose Files<br>
                                    <small>Click here or drag files</small>
                                </label>
                            </div>
                            <div class="upload-controls">
                                <button type="submit" class="btn btn-primary">Upload Files</button>
                            </div>
                        </form>
                    </div>
                </div>
                
                <div class="uploaded-section">
                    <h3>Previously Uploaded Files ({context['files_count']})</h3>
                    {files_html}
                </div>
            </div>
        </body>
        </html>
        """
    
    def render_upload_success(self, context):
        """Render upload success page"""
        files_list = ''.join([f'<li>{filename}</li>' for filename in context['uploaded_files']])
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Upload Successful</title>
            <style>{self.get_base_css()}</style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Upload Successful!</h1>
                </div>
                <div class="success-message">
                    <p>Successfully uploaded {context['files_count']} file(s):</p>
                    <ul>
                        {files_list}
                    </ul>
                </div>
                <div class="actions">
                    <a href="/upload" class="btn btn-primary">Upload More Files</a>
                    <a href="/" class="btn btn-secondary">Go Home</a>
                    <a href="/browse" class="btn btn-secondary">Browse Files</a>
                </div>
            </div>
        </body>
        </html>
        """