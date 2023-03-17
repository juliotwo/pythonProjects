#Código para crear la API
import base64
import psycopg2

conn = psycopg2.connect(
    host = "localhost",
    database = "mydb",
    user = "user",
    password = "password"
)

def upload_image(image_data):
    cur = conn.cursor()
    sql = "INSERT INTO images (image) VALUES (%s)"
    decoded_image = base64.b64decode(image_data)
    cur.execute(sql, (decoded_image, ))
    conn.commit()
    cur.close()

def get_image(image_id):
    cur = conn.cursor()
    sql = "SELECT image FROM images WHERE id = %s"
    cur.execute(sql, (image_id, ))
    image_data = cur.fetchone()[0]
    encoded_image = base64.b64encode(image_data)
    cur.close()
    return encoded_image

#Código para consumir la API

import requests 

#Subir una imagen
image_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+ip1sAAAAASUVORK5CYII="
resp = requests.post("http://localhost:5000/images/upload", data=image_data)

#Obtener una imagen
image_id = 1
resp = requests.get("http://localhost:5000/images/{}".format(image_id))
encoded_image = resp.json()