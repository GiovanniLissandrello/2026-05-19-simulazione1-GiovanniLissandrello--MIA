from database.DB_connect import DBConnect
from model.artista import Artista
from model.genere import Genere
from model.track import Track


class DAO():

    @staticmethod
    def getAllGeneri():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                   from genre"""

        cursor.execute(query)

        for row in cursor:
            result.append(Genere(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArtisti(genereID):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.ArtistId, a.Name
                    from track t, artist a, album al
                    where al.ArtistId  = a.ArtistId
                    and t.AlbumId = al.AlbumId 
                    and t.GenreId = %s
                    group by a.ArtistId, a.Name"""

        cursor.execute(query,(genereID,))

        for row in cursor:
            result.append(Artista(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getCanzoniAcquistateCustomer(genereID):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.TrackId, t.Name, t.AlbumId, t.UnitPrice
                    from invoice iv, invoiceline ivl, track t
                    where iv.CustomerId = %s
                    and iv.InvoiceId = ivl.InvoiceId 
                    and ivl.TrackId = t.TrackId """

        cursor.execute(query, (genereID,))

        for row in cursor:
            result.append(Track(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllIdCustomer():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select CustomerId
                    from customer"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["CustomerId"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPopolarita():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select a2.ArtistId, count(*) as popolarita
                    from album a, track t, artist a2, invoiceline
                    where a.AlbumId = t.AlbumId 
                    and a.ArtistId = a2.ArtistId
                    and invoiceline.TrackId = t.TrackId 
                    group by a2.ArtistId"""

        cursor.execute(query)

        for row in cursor:
            result.append((row['ArtistId'] , row['popolarita']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArtista(idAlbum):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select a2.ArtistId , a2.Name 
                    from album a, track t, artist a2
                    where a.AlbumId = %s
                    and a.ArtistId = a2.ArtistId
                    group by a2.ArtistId , a2.Name """

        cursor.execute(query,(idAlbum,))

        for row in cursor:
            result.append(Artista(**row))

        cursor.close()
        conn.close()
        return result


