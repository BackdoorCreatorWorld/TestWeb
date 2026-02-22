@app.route('/bnn-logo')
def bnn_logo():
    """Return BNN logo as SVG"""
    return '''
    <svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
        <!-- Background Shield -->
        <rect x="50" y="50" width="300" height="200" fill="#F5F5F5" stroke="#8B4513" stroke-width="5" rx="30"/>
        
        <!-- Garuda -->
        <circle cx="200" cy="120" r="50" fill="#8B4513"/>
        <circle cx="170" cy="100" r="10" fill="white"/>
        <circle cx="230" cy="100" r="10" fill="white"/>
        <circle cx="175" cy="105" r="3" fill="black"/>
        <circle cx="225" cy="105" r="3" fill="black"/>
        <polygon points="200,120 215,135 185,135" fill="gold"/>
        
        <!-- Wings -->
        <path d="M120 120 Q80 60 40 80" stroke="#CD853F" stroke-width="20" fill="none"/>
        <path d="M280 120 Q320 60 360 80" stroke="#CD853F" stroke-width="20" fill="none"/>
        
        <!-- Text -->
        <text x="200" y="200" text-anchor="middle" fill="#8B4513" font-size="20">BADAN</text>
        <text x="200" y="230" text-anchor="middle" fill="#8B4513" font-size="30" font-weight="bold">NARKOTIKA</text>
        <text x="200" y="260" text-anchor="middle" fill="#8B4513" font-size="20">NASIONAL</text>
        <text x="200" y="300" text-anchor="middle" fill="#8B4513" font-size="40" font-weight="900">BNN</text>
    </svg>
    ''', 200, {'Content-Type': 'image/svg+xml'}
