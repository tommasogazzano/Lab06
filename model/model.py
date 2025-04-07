from database.DAO import DAO


class Model:
    def __init__(self):
        pass

    def getYear(self):
        return DAO.getYear()

    def getBrand(self):
        return DAO.getBrand()

    def getRetailer(self):
        return DAO.getRetailer()

    def getVendite(self, anno, brand, retailer):
        return DAO.getTopVendite(anno, brand, retailer)

    def getAnalisiVendite(self, anno, brand, retailer):
        return DAO.analisi_Vendite(anno, brand, retailer)


