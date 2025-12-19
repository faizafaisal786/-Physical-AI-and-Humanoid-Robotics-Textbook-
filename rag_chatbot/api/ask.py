import os
import sys
import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

# Add backend to path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from agent import RAGAgent

# Global agent instance for reuse across requests
agent = None

def get_agent():
    """Lazy initialization of RAG agent"""
    global agent
    if agent is None:
        agent = RAGAgent()
    return agent

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests for RAG queries"""
        try:
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))

            # Read and parse request body
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)

            # Validate query
            query = data.get('query', '').strip()
            if not query:
                self.send_error_response(400, "Query cannot be empty")
                return

            if len(query) > 2000:
                self.send_error_response(400, "Query too long, maximum 2000 characters")
                return

            # Get RAG agent and process query
            rag_agent = get_agent()
            response = rag_agent.query_agent(query)

            # Format response
            formatted_response = {
                "answer": response.get("answer", ""),
                "sources": response.get("sources", []),
                "matched_chunks": [
                    {
                        "content": chunk.get("content", ""),
                        "url": chunk.get("url", ""),
                        "position": chunk.get("position", 0),
                        "similarity_score": chunk.get("similarity_score", 0.0)
                    }
                    for chunk in response.get("matched_chunks", [])
                ],
                "error": response.get("error"),
                "status": "error" if response.get("error") else "success",
                "query_time_ms": response.get("query_time_ms"),
                "confidence": response.get("confidence")
            }

            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(formatted_response).encode('utf-8'))

        except json.JSONDecodeError:
            self.send_error_response(400, "Invalid JSON in request body")
        except Exception as e:
            self.send_error_response(500, str(e))

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def send_error_response(self, status_code, message):
        """Send error response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        error_response = {
            "answer": "",
            "sources": [],
            "matched_chunks": [],
            "error": message,
            "status": "error"
        }
        self.wfile.write(json.dumps(error_response).encode('utf-8'))
