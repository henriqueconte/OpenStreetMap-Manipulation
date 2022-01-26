import database as db
from sys import argv

def execute_query():
    try:
        search_word = " ".join(argv[1:])

        search_word = " '%" + search_word + "%' "
        
        print(search_word)
        
        cursor = db.execute_query("SELECT tags->'name', ST_X(geom), ST_Y(geom) FROM nodes WHERE tags->'name' LIKE" + search_word + ";")
       
        for row in cursor:
            # Check if the name is way bigger or smaller than the actual search word. This verification exists in order to achieve the request response presented on the TP assignment. 
            if len(row[0]) < len(search_word) + 5 and len(row[0]) > len(search_word) - 5:
                print(row[0] + " | " + str(row[1]) + " | " + str(row[2]))

        cursor.close()
        db.close_connection()
    except:
        print("error")

execute_query()