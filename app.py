from flask import Flask, render_template, request
from datetime import datetime, timezone

# Initialize the Flask application
app = Flask(__name__)

FLEXIBLE_MODE = os.getenv('FLEXIBLE_MODE', 'false').lower() == 'true'

# Route for the main page
@app.route('/')
def show_info():
    """
    Gathers user/request information and renders it in an HTML table.
    """
    
    # 1. User IP Address
    # request.remote_addr gets the connecting IP. If running behind a proxy (like Nginx, Gunicorn), 
    # this will often be the proxy's internal IP.
    user_ip = request.remote_addr
    
    # 2. X-Forwarded-For Header
    # This header is typically set by proxies and should contain the original client IP
    # followed by any proxies. The first IP in the list is usually the client's.
    x_forwarded_for = request.headers.get('X-Forwarded-For', 'N/A (Header not present)')
    
    # 3. User-Agent Header
    user_agent = request.headers.get('User-Agent', 'N/A (Header not present)')
    
    # 4. Timestamp in UTC
    # Get the current time and format it as a UTC string
    timestamp_utc = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    # Prepare data for the template
    info_data = [
        ("User IP Address (remote_addr)", user_ip),
        ("X-Forwarded-For Header", x_forwarded_for),
        ("User-Agent Header", user_agent),
        ("Timestamp", timestamp_utc),
    ]

    # Render the template, passing the data
    return render_template('info_table.html', info_data=info_data)

# Run the application
if __name__ == '__main__':
    # Use '0.0.0.0' to make the server externally visible
    # In a local development environment, it usually runs on http://127.0.0.1:5000/
    app.run(debug=True, host='0.0.0.0')
