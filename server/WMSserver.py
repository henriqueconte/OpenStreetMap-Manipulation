#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import os

PORT_NUMBER = 4242


class WMSHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    # Example of get request: http://localhost:4242/wms?request=GetMap&layers=school,townhall&height=1000&width=1000&srs=EPSG:3857&bbox=5.7,5.8,45.1,45.2
    def do_GET(self):

        if self.path.startswith("/wms"):
            # Ici on récupère les valeurs de paramètres GET
            params = urlparse.parse_qs(urlparse.urlparse(self.path).query)

            try:
            # Question 12: 
                if params["request"][0] != "GetMap":
                    self.send_error(500, 'Requête non trouvé : %s' % params["request"][0])
                    return
                
                if int(params["width"][0]) < 0 or int(params["height"][0]) < 0: 
                    self.send_error(500, 'Taille invalide !')
                    return
                
                if params["srs"][0] != "EPSG:3857":
                    self.send_error(500, "SRS invalide: %s" % params["srs"][0])
                    return

                if len(params["bbox"][0].split(',')) != 4:
                    self.send_error(500, "BBox invalide : %s" % params["bbox"][0])
                    # We still need to format the bounding box to send as parameter on q11.py

                width = int(params["width"][0])
                height = int(params["height"][0])
                bbox_list = params["bbox"][0].split(',')
                init_x = float(bbox_list[0])
                init_y = float(bbox_list[1])
                end_x = float(bbox_list[2])
                end_y = float(bbox_list[3])
                layers = params["layers"][0]

                # Open question 11 Python file, sending parameters from get request
                # How to execute: python3 q11.py 5.7 5.8 45.1 45.2 1000 1000
                # print("init_x: ", init_x, "end_x: ", end_x, "init_y ", init_y, "end_y: ", end_y, "width: ", width, "height: ", height, "layers: ", layers)
                os.system(f'python3 q11.py {init_x} {init_y} {end_x} {end_y} {width} {height} {layers}')
                print("FINISHED CREATING MAP")

            except Exception as inst:
                self.send_error(500, 'Erreur : %s' % inst)

            self._set_headers()
            # params contient tous les paramètres GET
            # Il faut maintenant les traiter...
            # ... C'est à vous !
            
            return

        self.send_error(404, 'Fichier non trouvé : %s' % self.path)

    def send_plain_text(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=UTF-8')
        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))

    def send_png_image(self, filename):
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

    def send_html_file(self, filename):
        self.send_response(200)
        self.end_headers()
        self.serveFile(filename)


if __name__ == "__main__":
    try:
        # Ici on crée un serveur web HTTP, et on affecte le traitement
        # des requêtes à notre releaseHandler ci-dessus.
        server = HTTPServer(('', PORT_NUMBER), WMSHandler)
        print('Serveur démarré sur le port ', PORT_NUMBER)
        print('Ouvrez un navigateur et tapez dans la barre d\'url :'
              + ' http://localhost:%d/' % PORT_NUMBER)

        # Ici, on demande au serveur d'attendre jusqu'à la fin des temps...
        server.serve_forever()

    # ...sauf si l'utilisateur l'interrompt avec ^C par exemple
    except KeyboardInterrupt:
        print('^C reçu, je ferme le serveur. Merci.')
        server.socket.close()
