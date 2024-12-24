import pymongo
import yaml
from mitmproxy import http
from mitmproxy import ctx

# MongoDB client setup
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI if using Atlas
db = client["traffic_monitoring"]
collection = db["requests"]

# Read the YAML test file (example: BOLA test)
try:
    with open("bola.yaml", "r") as file:
        bola_test = yaml.safe_load(file)
except Exception as e:
    ctx.log.error(f"Error loading YAML test file: {e}")
    bola_test = {}

# Store request and response data in MongoDB
def store_traffic_data(flow: http.HTTPFlow, test_result=None):
    try:
        data = {
            "url": flow.request.url,
            "method": flow.request.method,
            "headers": dict(flow.request.headers),
            "request_body": flow.request.content.decode("utf-8", errors="ignore")[:100],  # Body limited
            "response_code": flow.response.status_code,
            "response_body": flow.response.content.decode("utf-8", errors="ignore")[:100],  # Body limited
            "test_result": test_result,
            "impact": test_result.get('impact', '') if test_result else '',
            "severity": test_result.get('severity', '') if test_result else '',
            "details": test_result.get('details', '') if test_result else ''
        }
        collection.insert_one(data)
        ctx.log.info("Traffic data stored successfully.")
    except Exception as e:
        ctx.log.error(f"Error storing traffic data in MongoDB: {e}")

# Function to run BOLA test (based on YAML configuration)
def run_bola_test(flow: http.HTTPFlow):
    test_result = None
    try:
        if "auth" in flow.request.url:  # Adjust this check based on the test conditions in the YAML
            if bola_test.get("execute", {}).get("type") == "single":
                for req in bola_test["execute"]["requests"]:
                    if req.get("remove_auth_header"):
                        # Remove the Authorization header (for testing BOLA)
                        flow.request.headers.pop("Authorization", None)
                        test_result = {
                            "name": bola_test["info"].get("name", "N/A"),
                            "impact": bola_test["impact"],
                            "severity": bola_test["severity"],
                            "details": bola_test["info"].get("details", "No details provided.")
                        }
    except Exception as e:
        ctx.log.error(f"Error running BOLA test: {e}")
    return test_result

# Intercept and handle requests
class TrafficMonitor:
    def request(self, flow: http.HTTPFlow):
        # Handle the intercepted request and execute test logic
        test_result = run_bola_test(flow)
        store_traffic_data(flow, test_result)

    def response(self, flow: http.HTTPFlow):
        # Handle the intercepted response and store data
        store_traffic_data(flow)

# Set up mitmproxy hooks to call the request/response functions
def start():
    ctx.log.info("Starting mitmproxy and capturing both HTTP and HTTPS traffic.")
    # Initialize and register the addon
    return TrafficMonitor()

# Register the addon to mitmproxy
addons = [
    TrafficMonitor()
]
