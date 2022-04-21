from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/sensors/light":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("Hello\n", "utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


class Serv(Thread):
    def __init__(self, hostName, serverPort):
        super().__init__()
        self.webServer = HTTPServer((hostName, serverPort), MyServer)
        print("Server started http://%s:%s" % (hostName, serverPort))

    def run(self) -> None:
        try:
            self.webServer.serve_forever()
        except KeyboardInterrupt:
            self.join()
            self.webServer.server_close()
            print("Server stopped.")


if __name__ == "__main__":
    hostName = "192.168.88.42"
    serverPort = 8030
    serv = Serv(hostName, serverPort)
    serv.start()