import http.server
import socketserver
import os
import time
import random
import base64

# Render dynamically assigns a port via the PORT environment variable
PORT = int(os.environ.get("PORT", 10000))

# Credentials from the PHP script
USERNAME = "0319"
PASSWORD = "D2tu4boKhB6%$o"
EXPECTED_AUTH = "Basic " + base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()

CHECK_RESPONSE = """{
  "SMSDirectoryData": {
    "error": 0,
    "result": "OK",
    "service": "Example 1.1",
    "version": 1.0,
    "status": "Ready",
    "infourl": "https://help.mydomain.nz/",
    "privacystatement": "This is a placeholder privacy statement. This should state what data your service collects, why and steps you take to protect the privacy of student / staff data - especially in regards to the NZ Privacy Act of 2020",
    "options": {
      "ics": true,
      "students": {
        "details": true,
        "passwords": false,
        "photos": false,
        "groups": false,
        "awards": false,
        "timetables": true,
        "attendance": false,
        "assessments": false,
        "pastoral": false,
        "learningsupport": true,
        "fields": {
          "required": "firstname;lastname;gender;nsn",
          "optional": "username;caregivers;caregivers1;caregivers2;caregiver.name;caregiver.relationship;caregiver.mobile;caregiver.email"
        }
      },
      "staff": {
        "details": false,
        "passwords": false,
        "photos": false,
        "timetables": false,
        "fields": {
          "required": "firstname;lastname;gender",
          "optional": "username"
        }
      },
      "common": {
        "subjects": false,
        "notices": false,
        "calendar": false,
        "bookings": false
      }
    }
  }
}"""

class SMSDirectoryHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Log to standard output so it shows up in Render's dashboard logs
        print(f"[{self.log_date_time_string()}] {format % args}")

    def handle_request(self):
        # Check authentication
        auth_header = self.headers.get("Authorization", "")
        if auth_header != EXPECTED_AUTH:
            self.send_response(200) # PHP script returns 200 with error JSON
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "SMSDirectoryData": {
                    "error": 403,
                    "result": "Authentication Failed",
                    "service": "Example 1.1",
                    "version": 1.0
                }
            }
            import json
            self.wfile.write(json.dumps(response).encode())
            return

        # Get POST content
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ""

        if not post_data:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "SMSDirectoryData": {
                    "error": 401,
                    "result": "No Data",
                    "service": "Example 1.1",
                    "version": 1.0
                }
            }
            import json
            self.wfile.write(json.dumps(response).encode())
            return

        # Check if sync check request
        if '"sync": "check"' in post_data:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(CHECK_RESPONSE.encode())
            return

        # Otherwise, save the JSON data to the data/ folder
        os.makedirs("data", exist_ok=True)
        filename = f"data/{int(time.time())}_{random.randint(1000, 9999)}.json"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(post_data)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            # Replicating the success response
            success_response = '{"SMSDirectoryData": {"error": 0, "result": "OK"}}'
            self.wfile.write(success_response.encode())
            print(f"Successfully saved payload to {filename}")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error saving data: {str(e)}".encode())

    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

def run_server():
    # Bind to 0.0.0.0 so that Render can route external traffic to this container
    with socketserver.TCPServer(("0.0.0.0", PORT), SMSDirectoryHandler) as httpd:
        print(f"Listening on port {PORT}...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server.")

if __name__ == '__main__':
    run_server()
