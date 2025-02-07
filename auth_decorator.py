from functools import wraps
from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

def authorize(f):
    @wraps(f)
    def auth_required(*args, **kwargs):
            if not 'Authorization' in request.headers:
               return jsonify({"message": "Authorization token missing"}), 401

            user = None
            data = request.headers['Authorization'].encode('ascii','ignore')
            token = str.replace(str(data), 'Bearer ','')
            try:
                user = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])['sub']
            except:
                return jsonify({"message": "Token mismatch"}), 401

            return f(user, *args, **kwargs)            
    return auth_required

@app.route('/api/health', methods=["GET", "POST"])
@authorize
def health():
    return jsonify({"message": "System up and running"}), 200
   
if __name == "__main__":
    app.run()
