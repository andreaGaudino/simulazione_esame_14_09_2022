from database.DB_connect import DBConnect
from model.album import Album


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def getNodi(durata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.AlbumId as id, a.Title as title, sum(t.Milliseconds/60/1000) as durata
                    from itunes.album a , itunes.track t 
                    where a.AlbumId = t.AlbumId 
                    group by a.AlbumId
                    having durata>%s """

        cursor.execute(query, (durata,))

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinctrow t.AlbumID as a1, t2.AlbumId as a2
                    from itunes.playlisttrack p , itunes.track t, itunes.track t2, itunes.playlisttrack p2 
                    where p.TrackID = t.TrackID
                    and t2.TrackId = p2.TrackId 
                    and t2.AlbumId < t.AlbumID
                    and p.PlaylistID = p2.PlaylistId  """

        cursor.execute(query, ())

        for row in cursor:
            result.append((row["a1"], row["a2"]))

        cursor.close()
        conn.close()
        return result
