import database as db
from sys import argv
import re
import drawer

########
#
# How to execute: python3 q11.py 5.7 5.8 45.1 45.2 1000 1000
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

def execute_query():

    try:
        init_x = float(argv[1])
        end_x = float(argv[2])
        init_y = float(argv[3])
        end_y = float(argv[4])
        width = int(argv[5])
        height = int(argv[6])

        # Instantiating the drawer helper
        image_drawer = drawer.Image(width, height)
        
        cursor = db.execute_query("""SELECT ST_AsText(linestring)
                                    FROM ways 
                                    WHERE tags ? 'highway' 
                                        AND NOT ST_IsEmpty(linestring) 
                                        AND ST_Intersects(
                                            linestring,
                                            ST_SetSRID(
                                                ST_MakeBox2D(
                                                    ST_Point(5.7, 45.1),
                                                    ST_Point(5.8, 45.2)
                                                ),
                                                4326
                                            )
                                        );"""
                )
        
        # For every linestring received, we parse the coordinates and draw them on the final image. 
        for row in cursor:
            point_list = parse_linestring(row[0], init_x, end_x, init_y, end_y, width, height)
            image_drawer.draw_linestring(point_list, (2/255, 130/255, 200/255, 255/255))
        
        image_drawer.save("map.png")

        cursor.close()
        db.close_connection()
    except:
        print("error")

execute_query()


# SQL Request:
# SELECT ST_AsText(linestring)
#                                     FROM ways 
#                                     WHERE tags ? 'highway' 
#                                         AND NOT ST_IsEmpty(linestring) 
#                                         AND ST_Intersects(
#                                             linestring,
#                                             ST_SetSRID(
#                                                 ST_MakeBox2D(
#                                                     ST_Point(5.7, 45.1),
#                                                     ST_Point(5.8, 45.2)
#                                                 ),
#                                                 4326
#                                             )
#                                         );

