#!/usr/bin/env python3
"""
=============================================================================
PUKLLAY SPORT - SERVIDOR REST API Y MOTOR POO EN PYTHON 3
=============================================================================
Servidor HTTP nativo (sin dependencias externas) utilizando Python stdlib.
Permite consultar KPIs, Reportes, Usuarios y ejecutar código Python en vivo.
Uso:
    python3 servidor_api.py --port 8001
=============================================================================
"""

import sys
import json
import io
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from backend_poo import PukllayService


class PukllayAPIHandler(BaseHTTPRequestHandler):
    service = PukllayService()

    def _responder_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        query = parse_qs(parsed.query)

        if path in ["", "/", "/api", "/api/health"]:
            self._responder_json({
                "servicio": "Pukllay Sport Python 3 API",
                "estado": "ACTIVO",
                "versionPython": sys.version,
                "endpoints": [
                    "/api/kpis",
                    "/api/reporte",
                    "/api/usuarios",
                    "/api/sedes",
                    "/api/reservas"
                ]
            })

        elif path == "/api/kpis":
            anio = int(query.get("anio", [2026])[0])
            kpis = self.service.obtener_kpis_dashboard(anio=anio)
            self._responder_json(kpis)

        elif path == "/api/reporte":
            reporte = self.service.generar_reporte_formal()
            self._responder_json(reporte)

        elif path == "/api/usuarios":
            usuarios = [u.to_dict() for u in self.service.obtener_todos_usuarios()]
            self._responder_json({"total": len(usuarios), "usuarios": usuarios})

        elif path == "/api/sedes":
            sedes = [s.to_dict() for s in self.service.obtener_sedes()]
            self._responder_json({"total": len(sedes), "sedes": sedes})

        elif path == "/api/reservas":
            reservas = [r.to_dict() for r in self.service.obtener_todas_reservas()]
            self._responder_json({"total": len(reservas), "reservas": reservas})

        else:
            self._responder_json({"error": "Endpoint no encontrado", "ruta": self.path}, status=404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/api/ejecutar":
            try:
                content_len = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_len).decode("utf-8")
                payload = json.loads(body) if body else {}
                codigo = payload.get("codigo", "")

                # Capturar stdout y stderr
                buffer_out = io.StringIO()
                buffer_err = io.StringIO()
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                sys.stdout = buffer_out
                sys.stderr = buffer_err

                entorno = {"service": self.service, "PukllayService": PukllayService}
                error_msg = None
                try:
                    exec(codigo, entorno)
                except Exception as ex:
                    error_msg = str(ex)
                finally:
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr

                self._responder_json({
                    "exito": error_msg is None,
                    "stdout": buffer_out.getvalue(),
                    "stderr": buffer_err.getvalue(),
                    "error": error_msg
                })
            except Exception as e:
                self._responder_json({"error": str(e)}, status=400)
        else:
            self._responder_json({"error": "Ruta POST no soportada"}, status=404)


def iniciar_servidor(puerto=8001):
    servidor = HTTPServer(("0.0.0.0", puerto), PukllayAPIHandler)
    print(f"🐍 Servidor Python REST API iniciado en http://0.0.0.0:{puerto}")
    print("Presiona Ctrl+C para detener.")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")


if __name__ == "__main__":
    puerto = 8001
    for arg in sys.argv[1:]:
        if arg.startswith("--port="):
            puerto = int(arg.split("=")[1])
        elif arg.isdigit():
            puerto = int(arg)
    iniciar_servidor(puerto)
