import database as db
from sys import argv
import re
import drawer


def parse_linestring(linestring):
    linestring = linestring.replace("LINESTRING(", "")
    linestring = linestring.replace(")", "")
    point_list_string = linestring.split(",")
    point_list = []

    for element in point_list_string:
        coordinate = element.split(" ")
        point_list.append((float(coordinate[0]), float(coordinate[1])))
    
    return point_list

def execute_query():

    try:
        init_x = float(argv[1])
        end_x = float(argv[2])
        init_y = float(argv[3])
        end_y = float(argv[4])
        width = int(argv[5])
        height = int(argv[6])

        image_drawer = drawer.Image(width, height)
        image_drawer.draw_rectangle(init_x, init_y, end_x, end_y, (100/255, 200/255, 20/255, 255/255), (200/255, 10/255, 60/255, 255/255))
        
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
       
        for row in cursor:
            point_list = parse_linestring(row[0])
            print(point_list)
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

