from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    @staticmethod
    def getYear():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()
        query = "select distinct year(gds.date) from go_daily_sales gds"
        cursor.execute(query)
        res = []
        for row in cursor:
            #print(row[0])  -> il risultato è una tupla
            res.append(row[0])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getBrand():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()
        query = "select DISTINCT gp.Product_brand from go_products gp"
        cursor.execute(query)
        res = []
        for row in cursor:
            #print(row[0])
            res.append(row[0])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getRetailer():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "select * from go_retailers gr"
        cursor.execute(query)
        res = []
        for row in cursor:
            # print(row[0])
            res.append(Retailer(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getTopVendite(anno=None, brand=None, retailer=None):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()

        query = """
        SELECT 
            gds.Date, 
            (gds.Quantity * gds.Unit_sale_price) as ricavo, 
            gds.Product_number, 
            gds.Retailer_code 
        FROM 
            go_sales.go_daily_sales gds, 
            go_sales.go_products gp, 
            go_sales.go_retailers gr 
        WHERE 
            gp.Product_number = gds.Product_number 
            AND gr.Retailer_code = gds.Retailer_code
        """

        params = []

        # Aggiungi condizioni solo se i parametri sono specificati

        if anno is not None:
            query += " AND YEAR(gds.Date) = %s"
            params.append(anno)

        if brand is not None:
            query += " AND gp.Product_brand = %s"
            params.append(brand)

        if retailer is not None:
            query += " AND gds.Retailer_code = %s"
            params.append(retailer)


        query += " ORDER BY ricavo DESC LIMIT 5"

        # Debug: stampa query completa
        print("Query finale:", query)
        print("Parametri:", params)

        cursor.execute(query, tuple(params))

        res = []
        for row in cursor:
            res.append(row)

        # Stampa risultati
        print("Risultati:", res)

        cursor.close()
        cnx.close()
        return res
    @staticmethod
    def analisi_Vendite(anno = None, brand = None, retailer = None):

        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()


        query = '''
        SELECT 
            round(sum(gds.Quantity * gds.Unit_sale_price), 2) as giro_affari,
            count(*) as numero_vendite,
            count(distinct gds.Retailer_code) as numero_retailers,
            count(distinct gds.Product_number) as numero_prodotti
        from
            go_sales.go_daily_sales gds, go_sales.go_products gp, go_sales.go_retailers gr
        where
            gp.Product_number = gds.Product_number 
            and gr.Retailer_code = gds.Retailer_code 
        '''

        params = []

        if anno is not None:
            query += " AND YEAR(gds.Date) = %s"
            params.append(anno)
        if brand is not None:
            query += " AND gp.Product_brand = %s"
            params.append(brand)

        if retailer is not None:
            query += " AND gds.Retailer_code = %s"
            params.append(retailer)

        cursor.execute(query, tuple(params))

        result = cursor.fetchone()
        cursor.close()
        cnx.close()

        return result



