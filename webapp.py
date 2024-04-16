uploaded = files.upload()

os.makedirs('/content/frontend', exist_ok=True)  
os.rename('Pervasive.html', '/content/frontend/Pervasive.html')  
os.rename('Pervasive.js', '/content/frontend/Pervasive.js') 
os.rename('Pervasive.css', '/content/frontend/Pervasive.css')

from IPython.display import HTML  # Import the HTML class

# Load the HTML file from the new directory
html_path = '/content/frontend/Pervasive.html'
with open(html_path, 'r') as f:
    html_content = f.read()

# Display the HTML content
HTML(html_content)

# Load the JavaScript file from the new directory
js_path = '/content/frontend/Pervasive.js'
with open(js_path, 'r') as f:
    js_content = f.read()

# Load the CSS file from the new directory
css_path = '/content/frontend/Pervasive.css'
with open(css_path, 'r') as f:
    css_content = f.read()

from IPython.display import HTML

# Define the file paths
html_path = '/content/frontend/Pervasive.html'
css_path = '/content/frontend/Pervasive.css'
js_path = '/content/frontend/Pervasive.js'

# Read the HTML content
with open(html_path, 'r') as f:
    html_content = f.read()

# Read the CSS content
with open(css_path, 'r') as f:
    css_content = f.read()

# Read the JavaScript content
with open(js_path, 'r') as f:
    js_content = f.read()

# Embed CSS and JavaScript into HTML
html_content_with_css = f'<style>{css_content}</style>{html_content}'
html_content_with_js = f'<script>{js_content}</script>{html_content_with_css}'

# Display the HTML content with CSS and JavaScript
HTML(html_content_with_js)

