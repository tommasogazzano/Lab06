import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fill_year(self):
        for y in self._model.getYear():
            self._view._yearDD.options.append(ft.dropdown.Option(y))

    def fill_brand(self):
        for b in self._model.getBrand():
            self._view._brandDD.options.append(ft.dropdown.Option(b))

    def fill_retailer(self):
        for r in self._model.getRetailer():
            self._view._retailerDD.options.append(ft.dropdown.Option(key = r.Retailer_code, text=r.Retailer_name, data=r, on_click = self._read_retailer))

    def _read_retailer(self, e):
        self._retailer = e.control.data
        print(self._retailer)

    def handle_vendite(self, e):
        # Converti 'nessun filtro' in None
        anno = None if self._view._yearDD.value == 'nessun filtro' else self._view._yearDD.value
        brand = None if self._view._brandDD.value == 'nessun filtro' else self._view._brandDD.value
        retailer = None if self._view._retailerDD.value == 'nessun filtro' else self._view._retailerDD.value

        # Pulisci i risultati precedenti
        self._view.txt_result.controls.clear()

        # Debug: stampa i valori dei filtri
        print(f"Filtri - Anno: {anno}, Brand: {brand}, Retailer: {retailer}")

        topVendite = self._model.getVendite(anno, brand, retailer)

        # Debug: stampa i risultati
        print(f"Risultati query: {topVendite}")

        if not topVendite:
            # Aggiungi un messaggio se non ci sono risultati
            self._view.txt_result.controls.append(ft.Text("Nessun risultato trovato"))
        else:
            for r in topVendite:
                self._view.txt_result.controls.append(
                    ft.Text(f"Data: {r[0]}, ricavo: € {r[1]}, retailer: {r[3]}, prodotto: {r[2]}"))

        self._view.update_page()

    def handle_analizza_vendite(self, e):
        anno = None if self._view._yearDD.value == 'nessun filtro' else self._view._yearDD.value
        brand = None if self._view._brandDD.value == 'nessun filtro' else self._view._brandDD.value
        retailer = None if self._view._retailerDD.value == 'nessun filtro' else self._view._retailerDD.value


        self._view.txt_result.controls.clear()

        stats = self._model.getAnalisiVendite(anno, brand, retailer)

        if stats:
            self._view.txt_result.controls.append(ft.Text(f"Giro d'affari: € {stats[0]:,.2f}"))
            self._view.txt_result.controls.append(ft.Text(f"Numero di vendite: {stats[1]}"))
            self._view.txt_result.controls.append(ft.Text(f"Numero di retailers: {stats[2]}"))
            self._view.txt_result.controls.append(ft.Text(f"Numero di prodotti: {stats[3]}"))
        else:
            self._view.txt_result.controls.append(ft.Text("Nessun risultato trovato"))

        self._view.update_page()