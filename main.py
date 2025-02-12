import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from services.service_scraping import ServiceScraping
from services.service_api import ServiceAPI
from configuration.config import Config
import datas.data_base as db
from tkinter import *


class Scraper:
    def __init__(self, root):
        self.root = root
        self.root.title("Scrapping")
        self.root.geometry("800x600")
        self.config = Config()
        self.db = db.DataBase()
        
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.scraping_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.scraping_frame, text="Scraping urls")
        
        self.api_frame = ttk.Frame(self.notebook)  
        self.notebook.add(self.api_frame, text="Scraping API Wiki")     
        
        self.search_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.search_frame, text="Buscar")
        
        self.setup_scraping_tab()
        self.setup_buscar_tab()
        self.setup_api_tab()
            
    def setup_api_tab(self):
        api_frame = ttk.LabelFrame(self.api_frame, text="Consultar API", padding="5")
        api_frame.pack(fill=tk.X, pady=5)
        
        self.palabra_var = tk.StringVar()
        self.palabra_var.set("Tema a buscar")  
        
        ttk.Label(api_frame, text="API URL:").pack(side=tk.LEFT, padx=5)
        palabra_var_entry = ttk.Entry(api_frame, textvariable=self.palabra_var, width=70)
        palabra_var_entry.pack(pady=5)
        
        fetch_btn = ttk.Button(api_frame, text="Consultar API", command=self.fetch_api_data)
        fetch_btn.pack(pady=5)
        btn_frame = ttk.Frame(api_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Seleccionar Todo", command=self.select_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Deseleccionar Todo", command=self.deselect_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Guardar Seleccionados", command=self.save_selected).pack(side=tk.RIGHT, padx=5)
        
        
        self.api_data_frame = ttk.LabelFrame(self.api_frame, text="Datos API", padding="5")
        self.api_data_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        
        self.canvas = tk.Canvas(self.api_data_frame)
        self.scrollbar = ttk.Scrollbar(self.api_data_frame, orient="vertical", command=self.canvas.yview)

        self.api_data_area = ttk.Frame(self.canvas)

        
        self.api_data_area.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        
        self.canvas.create_window((0, 0), window=self.api_data_area, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
    def setup_scraping_tab(self):
        url_frame = ttk.LabelFrame(self.scraping_frame, text="URLs Disponibles", padding="5")
        url_frame.pack(fill=tk.X, pady=5)
        
        self.url_var = tk.StringVar()
        urls = []
        for guerra in self.config.get_config().urls.guerras.primera_guera_mundial:
            urls.extend(guerra.urls)
        
        url_combo = ttk.Combobox(url_frame, textvariable=self.url_var, values=urls, width=70)
        url_combo.pack(pady=5)
        
        load_btn = ttk.Button(url_frame, text="Cargar URL", command=self.load_url)
        load_btn.pack(pady=5)
        
        content_frame = ttk.LabelFrame(self.scraping_frame, text="Contenido", padding="5")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Seleccionar Todo", command=self.select_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Deseleccionar Todo", command=self.deselect_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Guardar Seleccionados", command=self.save_selected).pack(side=tk.RIGHT, padx=5)
        
        self.content_area = ttk.Frame(content_frame)
        self.content_area.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.content_area)
        scrollbar = ttk.Scrollbar(self.content_area, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def setup_buscar_tab(self):
        search_control_frame = ttk.Frame(self.search_frame, padding="5")
        search_control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_control_frame, text="Búsqueda:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_control_frame, textvariable=self.search_var, width=50)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(search_control_frame, text="Buscar", command=self.search_content).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_control_frame, text="Generar HTML",command=lambda: self.generate_html(self.search_var.get())).pack(side=tk.RIGHT, padx=5)
        

        self.results_frame = ttk.LabelFrame(self.search_frame, text="Resultados", padding="5")
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        

        btn_frame = ttk.Frame(self.results_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Seleccionar Todo", command=self.select_all_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Deseleccionar Todo", command=self.deselect_all_results).pack(side=tk.LEFT, padx=5)
        
        self.results_area = ttk.Frame(self.results_frame)
        self.results_area.pack(fill=tk.BOTH, expand=True)
        
        self.results_canvas = tk.Canvas(self.results_area)
        results_scrollbar = ttk.Scrollbar(self.results_area, orient="vertical", command=self.results_canvas.yview)
        self.results_scrollable_frame = ttk.Frame(self.results_canvas)
        
        self.results_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all"))
        )
        
        self.results_canvas.create_window((0, 0), window=self.results_scrollable_frame, anchor="nw")
        self.results_canvas.configure(yscrollcommand=results_scrollbar.set)
        
        self.results_canvas.pack(side="left", fill="both", expand=True)
        results_scrollbar.pack(side="right", fill="y")
        
        self.search_results = []
        self.search_checkboxes = []
        self.search_vars = []
        
    def fetch_api_data(self):
        palabra = self.palabra_var.get()  
        if not palabra:
            messagebox.showwarning("!!!!", "Ingresar una palabra valida")
            return

        service = ServiceAPI(palabra)
        data = service.fetch_data()

        if not data:
            messagebox.showwarning("Error", "Api no encontrada")
            return

        for widget in self.api_data_area.winfo_children():
            widget.destroy()

        self.paragraph_vars = []  

        if isinstance(data, str):
            paragraphs = data.split('\n')

            self.current_data = {
                'url': "wikipedia_api: " + palabra,
                'titulo': palabra,
                'descripcion': palabra,
                'datos': [{'sub_titulo': palabra, 'contenido': p} for p in paragraphs if p.strip()]
            }

            for i, dato in enumerate(self.current_data['datos']):
                var = tk.BooleanVar()
                self.paragraph_vars.append(var)

                frame = ttk.Frame(self.api_data_area)
                frame.pack(fill=tk.X, pady=5)

                cb = ttk.Checkbutton(frame, variable=var)
                cb.pack(side=tk.LEFT)

                label = ttk.Label(frame, text=dato['contenido'], wraplength=700)
                label.pack(side=tk.LEFT, padx=5)

            ttk.Label(self.api_data_area, text="Selecciona algún párrafo para guardarlo").pack(pady=5)
        else:
            print(f"Datos No esperados: {data}")
            ttk.Label(self.api_data_area, text="Error: Formato de datos no esperado.").pack(pady=5)

    def load_url(self):
        url = self.url_var.get()
        if not url:
            messagebox.showwarning("Advertencia", "Por favor seleccione una URL")
            return
            
        scraping = ServiceScraping(url)
        titulo, descripcion, datos = scraping.get_data()
        

        for contenido in self.scrollable_frame.winfo_children():
            contenido.destroy()
        
        self.current_data = {
            'url': url,
            'titulo': titulo,
            'descripcion': descripcion,
            'datos': datos
        }
        
        self.paragraph_vars = []
        ttk.Label(self.scrollable_frame, text=f"Título: {titulo}", wraplength=700).pack(pady=5)
        ttk.Label(self.scrollable_frame, text=f"Descripción: {descripcion}", wraplength=700).pack(pady=5)
        
        for i, dato in enumerate(datos):
            var = tk.BooleanVar()
            self.paragraph_vars.append(var)
            
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(fill=tk.X, pady=5)
            
            cb = ttk.Checkbutton(frame, variable=var)
            cb.pack(side=tk.LEFT)
            
            text = f"Subtítulo: {dato['sub_titulo']}\nContenido: {dato['contenido']}"
            label = ttk.Label(frame, text=text, wraplength=700)
            label.pack(side=tk.LEFT, padx=5)
            
    def select_all(self):
        for par in self.paragraph_vars:
            par.set(True)
            
    def deselect_all(self):
        for par in self.paragraph_vars:
            par.set(False)
            
    def save_selected(self):
        if not hasattr(self, 'current_data'):
            messagebox.showwarning("!!!!", "No hay datos selecionados")
            return
            
        saved = False
        for i, var in enumerate(self.paragraph_vars):
            if var.get():
                print(self.current_data)
                dato = self.current_data['datos'][i]
                self.db.insert_data(
                    self.current_data['url'],
                    self.current_data['titulo'],
                    self.current_data['descripcion'],
                    dato['sub_titulo'],
                    dato['contenido']
                )
                saved = True
                
        if saved:
            messagebox.showinfo("OK", "Datos guardados correctamente")
        else:
            messagebox.showwarning("!!!!", "No hay datos selecionados")
            
    def search_content(self):
        regex = self.search_var.get()
        if not regex:
            messagebox.showwarning("!!!", "No se incontró ningúna palabra para buscar")
            return
            
        data = self.db.get_data_by_regex(regex)
        self.search_results = data

        for widget in self.results_scrollable_frame.winfo_children():
            widget.destroy()
        
        self.search_vars = []
        
        if len(data) > 0:
            for dato in data:
                var = tk.BooleanVar()
                self.search_vars.append(var)
                
                result_frame = ttk.Frame(self.results_scrollable_frame)
                result_frame.pack(fill=tk.X, pady=5, padx=5)
                
                cb = ttk.Checkbutton(result_frame, variable=var)
                cb.pack(side=tk.LEFT)
                
                url = dato[1]
                titulo = dato[2]
                sub_titulo = dato[3]
                descripcion = dato[4]
                contenido = dato[5]
                
                result_text = f"URL: {url}\nTITULO: {titulo}\nSUB-TITULO: {sub_titulo}\n"
                result_text += f"DESCRIPCION: {descripcion}\nCONTENIDO: {contenido}"
                
                label = ttk.Label(result_frame, text=result_text, wraplength=700)
                label.pack(side=tk.LEFT, padx=5)
        else:
            ttk.Label(self.results_scrollable_frame, text="Palabra no incontrada").pack(pady=10)
            
    def generate_html(self, name):
        if not self.search_results or not self.search_vars:
            messagebox.showwarning("!!!!", "No hay resultados para generar HTML")
            return
        
        selected_results = []
        for i, var in enumerate(self.search_vars):
            if var.get():
                selected_results.append(self.search_results[i])
        
        if not selected_results:
            messagebox.showwarning("!!!!", "Por favor seleccione al menos un resultado")
            return
            
        scraping = ServiceScraping()
        if scraping.generar_html(selected_results, name+".html" ):
            messagebox.showinfo("OK", "Archivo HTML generado correctamente")
        else:
            messagebox.showerror("!!!!", "Error al generar el archivo HTML")
            
    def select_all_results(self):
        for var in self.search_vars:
            var.set(True)
        
    def deselect_all_results(self):
        for var in self.search_vars:
            var.set(False)

if __name__ == "__main__":
    root = tk.Tk()
    app = Scraper(root)
    root.mainloop()