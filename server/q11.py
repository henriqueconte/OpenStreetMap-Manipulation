SELECT tags->'highway'
FROM ways 
WHERE tags ? 'highway' AND NOT ST_IsEmpty(linestring) 
                    AND ST_Intersects(
                            linestring,
                            ST_SetSRID(
                                ST_MakeBox2D(
                                    ST_Point(5.7, 45.1),
                                    ST_Point(5.8, 45.2)
                                ),
                                4326
                            )
                    );


