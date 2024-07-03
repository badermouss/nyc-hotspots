import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # Row 1
        self._ddProvider = ft.Dropdown(label="Provider")
        self._controller.fillDD()
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo)
        row1 = ft.Row([self._ddProvider, self._btnCreaGrafo], ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # Row 2
        self._txtInDistanza = ft.TextField(label="Inserisci distanza")
        self._btnAnalizzaGrafo = ft.ElevatedButton(text="Analisi Grafo", on_click=self._controller.handleAnalizzaGrafo)
        row2 = ft.Row([self._txtInDistanza, self._btnAnalizzaGrafo], ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # Row 3
        self._txtInStringa = ft.TextField(label="Inserisci una stringa")
        self._btnPercorso = ft.ElevatedButton(text="Calcola percorso", on_click=self._controller.handlePercorso)
        row3 = ft.Row([self._txtInStringa, self._btnPercorso], ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        # ROW4
        self._ddTarget = ft.Dropdown(label="Target")
        row4 = ft.Row([ft.Container(self._ddTarget, width=300),
                       ft.Container(None, width=200)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row4)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
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
