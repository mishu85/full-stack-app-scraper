from tkinter import Tk, Label, Button, Entry, StringVar, Frame, LEFT, RIGHT, Y, Scrollbar, Canvas
import requests
import json
import webbrowser
import functools

def request(query):
    response = requests.get("http://127.0.0.1:5000/", params={"search":query})
    if response.text is None or response.text is "":
        return None
    return json.loads(response.text)["data"]

def open_url(url):
    webbrowser.open_new_tab(url)

class App:
    def __init__(self, master):
        self.master = master
        master.title("Search online stores")
        self.search_field_value = StringVar()

        self.nav_container = Frame(master)
        self.nav_container.pack()
        self.search_field = Entry(self.nav_container, width = 100, textvariable = self.search_field_value)
        self.search_field.grid(row=0, column=2)
        self.search_button = Button(self.nav_container, text="Search", command=self.search_callback)
        self.search_button.grid(row=0, column=3)

        self.results_container = Frame(master)
        self.results_container.pack()
        self.welcome_label = Label(self.results_container, text="Bun venit! Cauta produsul dorit")
        self.welcome_label.pack()

    def clear_results_container(self):
        self.results_container.destroy()
        self.results_container = Frame(self.master)
        self.results_container.pack()

    def show_results(self, data):
        self.clear_results_container()
        if data is None:
            label = Label(self.results_container, text="Nu s-au gasit produse")
            label.pack()
        else:
            canvas_container=Canvas(self.results_container, width = 700, height=500)
            frame2=Frame(canvas_container)
            myscrollbar=Scrollbar(self.results_container,orient="vertical",command=canvas_container.yview)
            canvas_container.create_window((0,0),window=frame2,anchor='nw')
            products = list(data.values())
            for index, item in enumerate(products):
                item["price"] = int(item["price"].replace(".", "").replace("Lei", "").strip())
                products[index] = item
            products = sorted(products, key = lambda i: i['price'])
            for item in products:
                card = Frame(frame2)
                name = ""
                if len(item["name"]) > 100:
                    name = item["name"][:100] + "..."
                else:
                    name = item["name"]
                item_name = Label(card, text = name)
                item_store = Label(card, text = "Store: " + item["store"])
                item_price = Label(card, text = "Pret: " + str(item["price"]) + " Lei")
                item_button = Button(card, text = "View", command = functools.partial(open_url,item["link"]))
                item_name.pack(anchor='w')
                item_store.pack(anchor='w')
                item_price.pack(anchor='w')
                item_button.pack(anchor='w')
                card.pack(anchor='w')
            frame2.update()
            canvas_container.configure(yscrollcommand=myscrollbar.set, scrollregion="0 0 0 %s" % frame2.winfo_height())
            canvas_container.pack(side=LEFT)
            myscrollbar.pack(side=RIGHT, fill = Y)

    def search_callback(self):
        # search_query = self.search_field.get("1.0","end-1c") #de la linia 1, index x; pana la final - ultimul element
        search_query = self.search_field_value.get()
        data = request(search_query)
        self.show_results(data)

root = Tk()
my_gui = App(root)
root.mainloop() 

# text box + search button - DONE
# daca vine un array gol, trebuie sa se afiseze "Nu s-au gasit produse" - DONE
# Cand porneste, in spatiul rezultatelor sa afizee "Bun venit! Cauta produsul dorit" - DONE
# popularea interfata cu rezultate, sa fie scrollable
# Linkurile tre sa fie clickable
