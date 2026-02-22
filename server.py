#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ARCHITECT 01 - Local Web Server
Port: 7639
Max Connections: 2000
Auto-switch to BNN Garuda after limit
Shows all incoming IPs in Termux
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import threading
import time
import socket
import os
import sys
from datetime import datetime
from colorama import Fore, Style, init
import psutil

# Initialize colorama
init(autoreset=True)

# Configuration
PORT = 7639
MAX_REQUESTS = 2000
CURRENT_REQUESTS = 0
LOCK = threading.Lock()
SERVER_START_TIME = datetime.now()
REQUEST_LOG = []

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
CORS(app)

# Track request count
@app.before_request
def before_request():
    """Track every incoming request"""
    global CURRENT_REQUESTS
    
    client_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    path = request.path
    method = request.method
    
    with LOCK:
        CURRENT_REQUESTS += 1
        current = CURRENT_REQUESTS
    
    # Log to console
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_msg = (f"{Fore.GREEN}[{timestamp}]{Style.RESET_ALL} "
               f"{Fore.CYAN}{client_ip}{Style.RESET_ALL} "
               f"{Fore.YELLOW}{method}{Style.RESET_ALL} "
               f"{Fore.WHITE}{path}{Style.RESET_ALL} "
               f"{Fore.MAGENTA}[{current}/{MAX_REQUESTS}]{Style.RESET_ALL}")
    
    print(log_msg)
    
    # Store in log list (keep last 50)
    REQUEST_LOG.append({
        'timestamp': timestamp,
        'ip': client_ip,
        'method': method,
        'path': path,
        'ua': user_agent[:50]
    })
    if len(REQUEST_LOG) > 50:
        REQUEST_LOG.pop(0)

@app.route('/')
def index():
    """Main page - switches to blocked after MAX_REQUESTS"""
    with LOCK:
        if CURRENT_REQUESTS >= MAX_REQUESTS:
            return render_template('blocked.html')
    return render_template('index.html')

@app.route('/stats')
def stats():
    """Return server statistics as JSON"""
    with LOCK:
        remaining = max(0, MAX_REQUESTS - CURRENT_REQUESTS)
        return jsonify({
            'total_requests': CURRENT_REQUESTS,
            'max_requests': MAX_REQUESTS,
            'remaining': remaining,
            'status': 'BLOCKED' if CURRENT_REQUESTS >= MAX_REQUESTS else 'ACTIVE',
            'uptime': str(datetime.now() - SERVER_START_TIME).split('.')[0],
            'recent_ips': [log['ip'] for log in REQUEST_LOG[-10:]]
        })

@app.route('/logs')
def view_logs():
    """View recent request logs"""
    return jsonify(REQUEST_LOG[-20:])

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

def print_server_info():
    """Print server information in Termux"""
    print(f"\n{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.GREEN}   ARCHITECT 01 - LOCAL WEB SERVER{Style.RESET_ALL}")
    print(f"{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   Port: {Fore.WHITE}{PORT}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   Max Requests: {Fore.WHITE}{MAX_REQUESTS}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   Auto-switch: {Fore.WHITE}BNN Garuda after limit{Style.RESET_ALL}")
    print(f"{Fore.CYAN}───────────────────────────────────────────{Style.RESET_ALL}")
    
    # Get local IPs
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"{Fore.GREEN}   Local Access:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}   • http://localhost:{PORT}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}   • http://127.0.0.1:{PORT}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}   • http://{local_ip}:{PORT}{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}───────────────────────────────────────────{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   Monitoring every request...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   Press Ctrl+C to stop server{Style.RESET_ALL}")
    print(f"{Fore.CYAN}═══════════════════════════════════════════════{Style.RESET_ALL}\n")

def monitor_stats():
    """Background thread to show stats periodically"""
    while True:
        time.sleep(30)
        with LOCK:
            remaining = MAX_REQUESTS - CURRENT_REQUESTS
            percent = (CURRENT_REQUESTS / MAX_REQUESTS) * 100
            
        print(f"{Fore.CYAN}[STATS]{Style.RESET_ALL} "
              f"Total: {CURRENT_REQUESTS}/{MAX_REQUESTS} "
              f"({percent:.1f}%) | "
              f"Remaining: {remaining} | "
              f"Uptime: {datetime.now() - SERVER_START_TIME}")

def check_port_available(port):
    """Check if port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
            return True
        except:
            return False

if __name__ == '__main__':
    try:
        # Clear screen
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Check port
        if not check_port_available(PORT):
            print(f"{Fore.RED}❌ Port {PORT} is already in use!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Kill the process using: fuser -k {PORT}/tcp{Style.RESET_ALL}")
            sys.exit(1)
        
        # Print server info
        print_server_info()
        
        # Start stats monitor thread
        stats_thread = threading.Thread(target=monitor_stats, daemon=True)
        stats_thread.start()
        
        # Run Flask
        app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)
        
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}\n╰─❯ Server stopped by user{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}╰─❯ Total requests handled: {CURRENT_REQUESTS}{Style.RESET_ALL}")
        
        # Show top IPs
        if REQUEST_LOG:
            from collections import Counter
            ip_counter = Counter([log['ip'] for log in REQUEST_LOG])
            print(f"\n{Fore.CYAN}Top 5 IPs:{Style.RESET_ALL}")
            for ip, count in ip_counter.most_common(5):
                print(f"{Fore.WHITE}  • {ip}: {count} requests{Style.RESET_ALL}")
        
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        sys.exit(1)
