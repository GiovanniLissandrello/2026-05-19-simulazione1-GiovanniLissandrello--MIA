from database.DB_connect import DBConnect
from model.Arco import Arco
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
    def getArtistiCompleto():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select ArtistId, Name
                       from artist a"""

        cursor.execute(query,)

        for row in cursor:
            result.append(Artista(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getCanzoniAcquistateCustomer(Id): #restituisce tutte le canzoni acquistate di uno specifico customer
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.TrackId, t.Name, t.AlbumId, t.UnitPrice
                    from invoice iv, invoiceline ivl, track t
                    where iv.CustomerId = %s
                    and iv.InvoiceId = ivl.InvoiceId 
                    and ivl.TrackId = t.TrackId """

        cursor.execute(query, (Id,))

        for row in cursor:
            result.append(Track(**row))                                     #restituisce oggetto di tipo Track

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllIdCustomer(): #tutti gli ID dei customer
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct CustomerId
                    from customer"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["CustomerId"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPopolarita(genereId): #popolarità di ogni artista
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select a2.ArtistId, count(*) as popolarita
                    from album a, track t, artist a2, invoiceline
                    where a.AlbumId = t.AlbumId 
                    and a.ArtistId = a2.ArtistId
                    and invoiceline.TrackId = t.TrackId 
                    and t.GenreId = %s
                    group by a2.ArtistId"""

        cursor.execute(query, (genereId,))

        for row in cursor:
            result.append((row["ArtistId"] , row["popolarita"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArtista(idAlbum): #query per recuperare l'artista dall'ID dell'album
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select a2.ArtistId , a2.Name 
                    from album a, artist a2
                    where a.AlbumId = %s
                    and a.ArtistId = a2.ArtistId
                    group by a2.ArtistId , a2.Name """

        cursor.execute(query,(idAlbum,))

        for row in cursor:
            artista = Artista(**row)

        cursor.close()
        conn.close()
        return artista

    @staticmethod
    def getCollegamenti(idCustomer, dict_artisti, genere): #query per recuperare l'artista dall'ID dell'album
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select t1.ArtistId as id1, t2.ArtistId as id2
from (select iv.CustomerId, a2.ArtistId, t.GenreId
      from invoice iv, invoiceline ivl, track t, album a, artist a2
      where iv.InvoiceId = ivl.InvoiceId 
        and ivl.TrackId = t.TrackId 
        and a.AlbumId = t.AlbumId 
        and a.ArtistId = a2.ArtistId 
        and iv.CustomerId = %s
        and t.GenreId = %s
      group by iv.CustomerId, a2.ArtistId, t.GenreId
     ) t1,
     (select iv.CustomerId, a2.ArtistId, t.GenreId
      from invoice iv, invoiceline ivl, track t, album a, artist a2
      where iv.InvoiceId = ivl.InvoiceId 
        and ivl.TrackId = t.TrackId 
        and a.AlbumId = t.AlbumId 
        and a.ArtistId = a2.ArtistId 
        and iv.CustomerId = %s
        and t.GenreId = %s
      group by iv.CustomerId, a2.ArtistId, t.GenreId
     ) t2
where t1.CustomerId = t2.CustomerId
  and t1.ArtistId < t2.ArtistId
  and t1.GenreId = t2.GenreId"""

        cursor.execute(query,(idCustomer,genere,idCustomer,genere,))

        for row in cursor:
                result.append((dict_artisti.get(row["id1"]), dict_artisti.get(row["id2"])))

        cursor.close()
        conn.close()
        return result


