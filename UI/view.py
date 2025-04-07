import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._btnAn = None
        self._btnTop = None
        self._retailerDD = None
        self._brandDD = None
        self._yearDD = None
        self._page = page
        self._page.title = "Lab06"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_result = None

    def load_interface(self):
        # title
        self._title = ft.Text("Analizza Vendite", color="blue", size=24)
        self._page.controls.append(self._title)

        self._yearDD = ft.Dropdown(label="anno", width = 150, options = [ft.dropdown.Option("nessun filtro")])
        self._brandDD = ft.Dropdown(label="Brand", width = 150, options = [ft.dropdown.Option("nessun filtro")])
        self._retailerDD = ft.Dropdown(label="Retailer", width = 350, options = [ft.dropdown.Option("nessun filtro")])

        self._controller.fill_year()
        self._controller.fill_brand()
        self._controller.fill_retailer()
        
        self._btnTop = ft.ElevatedButton(text="Top Vendite", width = 200, on_click=self._controller.handle_vendite)
        self._btnAn = ft.ElevatedButton(text="Analizza Vendite", width = 200, on_click=self._controller.handle_analizza_vendite)

        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        
        
        row1 = ft.Row([self._yearDD, self._brandDD, self._retailerDD], alignment=ft.MainAxisAlignment.CENTER)
        row2 = ft.Row([self._btnTop, self._btnAn], alignment=ft.MainAxisAlignment.CENTER)
        
        self._page.add(row1, row2, self.txt_result)
        

        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
