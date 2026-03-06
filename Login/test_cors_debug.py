#!/usr/bin/env python3
"""Debug Flask app to see exactly what routes are registered"""

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, 
     resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"], "allow_headers": ["Content-Type", "Authorization"]}},
     supports_credentials=True)

# Test route definitions
@app.route('/test-working', methods=['POST'])
def test_working():
    return {'status': 'ok'}, 200

@app.route('/test-new', methods=['POST'])
def test_new():
    return {'status': 'ok'}, 200

# Print immediately after routes are defined
print("=" * 60)
print("Routes registered:")
for rule in app.url_map.iter_rules():
    print(f"{rule.rule.ljust(40)} {sorted(rule.methods)}")
print("=" * 60)

if __name__ == '__main__':
    app.run(port=5001, debug=False)
