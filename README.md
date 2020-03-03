# createCollage
A Flask REST api along with js based frontend which takes images as input and returns a collage of human faces in them.

Change the paths of model data in find_faces_api/app.py to the local paths and the url in find_faces_frontend/scripts.js according to the local host.

-Run main.py in find_faces_api to run the service. It listens for requests in port:5000.

-Use the index.html in find_faces_frontend to send POST requests to the api.
