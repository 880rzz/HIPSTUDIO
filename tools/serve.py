"""Local preview with real 404 responses; no upload or deployment."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import os
ROOT=Path(__file__).resolve().parents[1]/'dist'
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def send_error(self,code,message=None,explain=None):
  if code==404:
   data=(ROOT/'404.html').read_bytes();self.send_response(404);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
  else:super().send_error(code,message,explain)
print('Preview http://127.0.0.1:4173',flush=True)
ThreadingHTTPServer(('127.0.0.1',4173),Handler).serve_forever()
