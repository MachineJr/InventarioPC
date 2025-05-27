# prueba_http.py
import http.server
import socketserver

PORT = 5050

Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Servidor HTTP activo en el puerto", PORT)
    httpd.serve_forever()
