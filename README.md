# REST API
Flask REST api with object and face detection capabilities.

**Extract model.zip**

Change the paths of model data in find_faces_api/app.py to the local paths and the url in find_faces_frontend/scripts.js according to the local host.

# How to use?

## createCollage

Make a collage of human faces from a given set of images.

-Run main.py in find_faces_api to run the service. It listens for requests in port:5000.

-Use the index.html in find_faces_frontend to send POST requests to the api.

## getImageDetails

-Run main.py in find_faces_api to run the service. It listens for requests in port:5000.

-Use POSTMAN to drop POST requests with an image file to get the number of human faces, animals and objects in the image in JSON format.
