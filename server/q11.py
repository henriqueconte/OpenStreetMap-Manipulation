import database as db
from sys import argv
import re
import drawer
import random
import cv2
import numpy as np

########
#
# How to execute: python3 q11.py 635956.0753326665 5645333.161029978 640848.0451429178 5650225.13084023 1000 1000 school,townhall
#
########

# We are going to receive coordinates, but we need to present them proportionally to the output image size
def normalize(position, init, end, total_size):
    proportion = (end - position) / (end - init)
    return proportion * total_size

# We receive the linestring with all points separated by ",", so we need to cast it into an array of tuples of floats (coordinates).
def parse_linestring(linestring, init_x, end_x, init_y, end_y, width, height):
    linestring = linestring.replace("LINESTRING(", "")
    linestring = linestring.replace(")", "")
    point_list_string = linestring.split(",")
    point_list = []

    # For every point, we cast it into float and calculate the position that will be displayed on the final image
    for element in point_list_string:
        coordinate = element.split(" ")
        point = (normalize(float(coordinate[0]), init_x, end_x, width),
                normalize(float(coordinate[1]), init_y, end_y, height))
        point_list.append(point)

    return point_list

def execute_query(init_x, init_y, end_x, end_y, width, height, layers):

    # try:

    # Instantiating the drawer helper
    image_drawer = drawer.Image(width, height)

    cursor = db.execute_query(f"""SELECT ST_AsText(ST_Transform(linestring, 3857))
                                    FROM ways 
                                    WHERE tags ? 'highway' 
                                        AND NOT ST_IsEmpty(linestring) 
                                        AND ST_Intersects(
                                            linestring,
                                            ST_Transform(ST_MakeEnvelope(
                                                {init_x}, {init_y}, {end_x}, {end_y}, 3857
                                            ), 4326)    
                                        );"""
        )
    
    # For every linestring received, we parse the coordinates and draw them on the final image. 
    for row in cursor:
        point_list = parse_linestring(row[0], init_x, end_x, init_y, end_y, width, height)
        image_drawer.draw_linestring(point_list, (2/255, 130/255, 200/255, 255/255))


    # for element in layers:
    #     cursor = db.execute_query(f"""SELECT ST_AsText(ST_Transform(linestring, 3857))
    #                         FROM ways 
    #                         WHERE ways.tags->'amenity' = '{element}'
    #                             AND NOT ST_IsEmpty(linestring) 
    #                             AND ST_Intersects(
    #                                         ST_SetSRID(linestring, 3857),
    #                                         ST_SetSRID(
    #                                             ST_MakeBox2D(
    #                                                 ST_Transform(
    #                                                     ST_SetSRID(
    #                                                         ST_Point({init_x}, {init_y}),
    #                                                         3857), 
    #                                                     4326),
    #                                                 ST_Transform(
    #                                                     ST_SetSRID(
    #                                                         ST_Point({end_x}, {end_y}),
    #                                                         3857), 
    #                                                     4326)
    #                                             ),
    #                                             3857
    #                                         )
    #                                     );"""
    #     )
        
    #     stroke_color = (random.randint(0, 255)/255, random.randint(0, 255)/255, random.randint(0,255)/255, 255/255)
    #     # For every linestring received, we parse the coordinates and draw them on the final image. 
    #     for row in cursor:
    #         point_list = parse_linestring(row[0], init_x, end_x, init_y, end_y, width, height)
    #         image_drawer.draw_linestring(point_list, stroke_color)
    
    filename = f"tuiles/highway-{init_x}-{init_y}-{end_x}-{end_y}.png"
    image_drawer.save(filename)
    mirror_image(filename)
    cursor.close()
    db.close_connection()

    return filename
    # except:
    #     print("error")

def mirror_image(filename):
    img = cv2.imread(filename)
    img_mirror = np.flip(img, axis=1)
    cv2.imwrite(filename, img_mirror)


######
# Use this if wants to run only q11.py without using the server.
######

# init_x = min(float(argv[1]), float(argv[3]))
# init_y = min(float(argv[2]), float(argv[4]))
# end_x = max(float(argv[1]), float(argv[3]))
# end_y = max(float(argv[2]), float(argv[4]))
# width = int(argv[5])
# height = int(argv[6])
# layers = argv[7].split(",")

# execute_query(init_x, init_y, end_x, end_y, width, height, layers)

