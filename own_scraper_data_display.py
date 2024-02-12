from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.datatables import MDDataTable
from kivymd.icon_definitions import md_icons
from kivymd.uix.button import MDIconButton
from kivy.metrics import dp
import pandas as pd
from kivy.clock import Clock
from openpyxl import load_workbook
import webbrowser
import validators
from kivy.core.window import Window
import openpyxl
import os
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import random
from kivy.uix.popup import Popup
guest = ""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.button import Button
#Used to check if items are in the cart
checked_items = []
#Storing item index
store_ids = []
#Cart counter
cart_count = 0
#Stores the data
data = []

text1 = ""


# Creates first screen
class ScreenOne(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Window.bind(on_request_close=lambda *args: True)

        # Create the data table
        self.data_table1 = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.9, 0.6),
            check=False,
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("ID", dp(25)),
                ("Data 1", dp(100)),
                ("Data 2", dp(100)),
                ("Data 3", dp(100)),
                ("Data 4", dp(100)),

            ],
            row_data=data,

        )

        # data_table.row_data[0]['check'] = False

        self.data_table1.bind(on_check_press=self.on_check_press)
        self.add_widget(self.data_table1)

        # Create the save selected button
        check_cart = Button(
            text="Check Cart",
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_normal='',
            background_color=(0, 0.349, 0.686, 1),
            color=(1, 1, 1, 1),
            border=(0, 0, 0, 5),
        )
        check_cart.bind(on_press=self.go_to_screen_two)
        self.add_widget(check_cart)




        # Create the save button
        save_button = Button(
            text="Save",
            size_hint=(0.1, 0.1),
            pos_hint={'center_x': 0.9, 'center_y': 0.1},
            background_normal='',
            background_color=(0.1, 0.5, 0.1, 1.0),
            color=(1, 1, 1, 1),
            border=(0, 0, 0, 5),
        )
        save_button.bind(on_press=self.save_file)
        self.add_widget(save_button)

        # Create the quit button
        quit_button = Button(
            text="Leave",
            size_hint=(0.1, 0.1),
            pos_hint={'center_x': 0.1, 'center_y': 0.1},
            background_normal='',
            background_color=(0.8, 0.2, 0.2, 1.0),
            color=(1, 1, 1, 1),
            border=(0, 0, 0, 5),

        )
        quit_button.bind(on_press=self.quit)
        self.add_widget(quit_button)
        # Create input text field
        self.item_id_input = TextInput(
            size_hint=(0.4, None),
            height=dp(30),
            hint_text="Enter/Remove Item ID",
            multiline=False,
            input_filter="int",
            pos_hint={'center_x': 0.74, 'center_y': 0.83},
        )
        self.add_widget(self.item_id_input)

        # Create a button for saving the entered item ID
        save_id_button = Button(
            text="Save ID",
            size_hint=(0.2, None),
            height=dp(30),
            pos_hint={'center_x': 0.84, 'center_y': 0.83},
            background_normal='',
            background_color=(0, 0.349, 0.686, 1),
            color=(1, 1, 1, 1),
            border=(0, 0, 0, 5),
        )
        save_id_button.bind(on_press=self.save_item_id)
        self.add_widget(save_id_button)
        # Create refresh button
        refresh_button = MDIconButton(
            icon="refresh",
            pos_hint={'center_x': 0.06, 'center_y': 0.9},
        )
        self.add_widget(refresh_button)
        refresh_button.bind(on_press=self.refresh_main_data)
        # Create item cart
        cart_layout = BoxLayout(
            size_hint=(None, None),
            size=(dp(120), dp(48)),
            pos_hint={'center_x': 0.5, 'center_y': 0.9},
            spacing=dp(10)
        )
        cart_icon = MDIconButton(
            icon="cart",
            theme_text_color="Custom",

        )
        self.cart_label = MDLabel(
            text="0",
            size_hint=(None, None),
            pos_hint={'center_x': 0.455, 'center_y': 0.94},
            size=(dp(32), dp(32)),
            halign="center",
            valign="center",
            font_style="Body2",
            theme_text_color="Custom",

        )
        cart_layout.add_widget(cart_icon)
        self.add_widget(cart_layout)
        self.add_widget(self.cart_label)
        # data_table.row_data[0]["active_check"] = False
    # Used to trigger screen three and closes screen one
    def sort_high(self, button):
        global screen_one_bool
        global screen_three_bool
        screen_one_bool = False
        screen_three_bool = True
        screen_one = self.manager.get_screen('screen_three')
        screen_one.refresh_cart()
        self.manager.current = 'screen_three'


    # Refresh  the cart
    def refresh_cart(self):
        # Get the current value of the cart and update the label
        self.cart_label.text = f"{cart_count}"
    # Used to refresh data when the screen freezes
    def refresh_main_data(self, button):
        self.remove_widget(self.data_table1)
        self.data_table1 = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(1.0, 0.6),
            check=False,
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("ID", dp(25)),
                ("Data 1", dp(100)),
                ("Data 2", dp(100)),
                ("Data 3", dp(100)),
                ("Data 4", dp(100)),
            ],
            row_data=data,

        )
        self.add_widget(self.data_table1)

    # Saves item id
    def save_item_id(self, instance):
        global cart_count
        global checked_items
        global store_ids
        # Text input
        try:
            item_id = int(self.item_id_input.text)


        # Checks if the input is a positive number and less than data length
            if item_id < len(data) and item_id >= 0:
                # If the item id is stored remove it from the list and update cart
                if item_id in store_ids:

                    # Gets the item index from the list which is the number ID
                    stored_index = store_ids.index(item_id)
                    # Used to delete item ids from stored ids and check_ids
                    del store_ids[stored_index]
                    del checked_items[stored_index]
                    # Update counter
                    cart_count -= 1
                    self.item_id_input.text = ""
                # Add item ID to the cart and update the cart
                else:

                    # Stores item in the list
                    store_ids.append(item_id)
                    checked_items.append(data[item_id])
                    cart_count += 1
                    self.item_id_input.text = ""
                self.cart_label.text = f"{cart_count}"

            else:
                show_popup(1, 1)
        except:
            show_popup(1, 1)


    def on_check_press(self, instance_table, current_row):
        global cart_count
        global checked_items
        global store_ids
        index = current_row[0]
        print(current_row[1])
        print(instance_table)

        if index in store_ids:
            stored_index = store_ids.index(index)
            del store_ids[stored_index]
            del checked_items[stored_index]
            cart_count -= 1
        else:
            # Remove item from list if it is unchecked
            print(current_row[0])
            store_ids.append(index)
            checked_items.append(current_row)
            cart_count += 1
        self.cart_label.text = f"Cart: {cart_count}"

    # Saves the display file

    def save_file(self, button):
        # connecting a path
        if guest == False:
            # opens the excel
            workbook = openpyxl.load_workbook(f'{text1}.xlsx')


            # Get the user's Downloads folder path
            try:
                # For Windows
                downloads_folder = os.path.join(os.environ["HOMEPATH"], "Downloads")
                print("winodw")
            except KeyError:
                try:
                    # For macOS/iOS
                    downloads_folder = os.path.join(os.environ["HOME"], "Downloads")
                    print("Mac")
                except KeyError:
                    # For Linux and other platforms
                    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
                    print("other")

            # Save the file to the Downloads folder with a filename
            filename = os.path.join(downloads_folder, f'{text1}.xlsx')
            try:
                workbook.save(filename)
                show_popup(0, 0)
            except PermissionError as e:
                show_popup(0, 6)
        else:
            show_popup(0, 3)




    #Quit method
    def quit(self, button):
        global cart_count
        global checked_items
        global store_ids
        if text1 == "":
            pass
        else:
            try:
                cart_count = 0
                checked_items.clear()
                store_ids.clear()
                os.remove(f'{text1}.xlsx')
                MyApp.get_running_app().stop()
            except:
                pass







    def go_to_screen_two(self, *args):
        screen_two = self.manager.get_screen('screen_two')
        screen_two.refresh_data(checked_items)
        self.manager.current = 'screen_two'


class ScreenTwo(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        check_cart = Button(
            text="Check data",
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_normal='',
            background_color=(0, 0.349, 0.686, 1),
            color=(1, 1, 1, 1),
            border=(0, 0, 0, 5),

        )
        check_cart.bind(on_press=self.go_to_screen_one)
        self.add_widget(check_cart)
        self.data_table2 = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(1.0, 0.6),
            check=False,
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("ID", dp(25)),
                ("Data 1", dp(100)),
                ("Data 2", dp(100)),
                ("Data 3", dp(100)),
                ("Data 4", dp(100)),
            ],
            row_data=checked_items,

        )

        self.add_widget(self.data_table2)

        save_select_items = Button(
            text="Save",
            size_hint=(0.1, 0.1),
            pos_hint={'center_x': 0.9, 'center_y': 0.1},
            background_normal='',
            background_color=(0.1, 0.5, 0.1, 1.0),
            color=(1, 1, 1, 1),
            border=(0, 0, 0, 5),
        )
        save_select_items.bind(on_press=self.save_selected_items)
        self.add_widget(save_select_items)

        # Create the quit button
        quit_button = Button(
            text="Leave",
            size_hint=(0.1, 0.1),
            pos_hint={'center_x': 0.1, 'center_y': 0.1},
            background_normal='',
            background_color=(0.8, 0.2, 0.2, 1.0),
            color=(1, 1, 1, 1),
            border=(0, 0, 0, 5),

        )
        quit_button.bind(on_press=self.quit)
        self.add_widget(quit_button)

        refresh_button = MDIconButton(
            icon="refresh",
            pos_hint={'center_x': 0.06, 'center_y': 0.9},
        )
        self.add_widget(refresh_button)
        refresh_button.bind(on_press=self.refresh_data)

        self.item_id_input = TextInput(
            size_hint=(0.4, None),
            height=dp(30),
            hint_text="Remove Item ID",
            multiline=False,
            input_filter="int",
            pos_hint={'center_x': 0.74, 'center_y': 0.83},
        )
        self.add_widget(self.item_id_input)

        # Create a button for saving the entered item ID
        self.remove_id_button = Button(
            text="Remove ID",
            size_hint=(0.2, None),
            height=dp(30),
            pos_hint={'center_x': 0.84, 'center_y': 0.83},
            background_normal='',
            background_color=(0, 0.349, 0.686, 1),
            color=(1, 1, 1, 1),
            border=(0, 0, 0, 5),
        )
        self.remove_id_button.bind(on_press=self.remove_item_id)
        self.remove_id_button.bind(on_release=self.refresh_data)

        self.add_widget(self.remove_id_button)

        self.item_id_link_input = TextInput(
            size_hint=(0.4, None),
            height=dp(30),
            hint_text="Enter ID for link",
            multiline=False,
            input_filter="int",
            pos_hint={'center_x': 0.24, 'center_y': 0.83},
        )
        self.add_widget(self.item_id_link_input)

        # Create a button for saving the entered item ID
        self.enter_link = Button(
            text="Get Link",
            size_hint=(0.2, None),
            height=dp(30),
            pos_hint={'center_x': 0.34, 'center_y': 0.83},
            background_normal='',
            background_color=(0, 0.349, 0.686, 1),
            color=(1, 1, 1, 1),
            border=(0, 0, 0, 5),
        )
        self.enter_link.bind(on_press=self.open_link)
        # self.enter_link.bind(on_release=self.refresh_data)

        self.add_widget(self.enter_link)

        self.data_table2.bind(on_check_press=self.on_row_press)

    def on_row_press(self, instance_table, instance_row):
        print(instance_row, instance_table)


    def go_to_screen_one(self, *args):
        screen_one = self.manager.get_screen('screen_one')
        screen_one.refresh_cart()
        self.manager.current = 'screen_one'


    def refresh_data(self, new_data):
        self.remove_widget(self.data_table2)
        self.data_table2 = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.9, 0.6),
            check=False,
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("ID.", dp(25)),
                ("Data 1", dp(100)),
                ("Data 2", dp(100)),
                ("Data 3", dp(100)),
                ("Data 4", dp(100)),
            ],
            row_data=checked_items,

        )
        self.add_widget(self.data_table2)

    def open_link(self, button):
        # Checks each index to see if there is a link
        try:
            item_id = int(self.item_id_link_input.text)
            stored_index = store_ids.index(item_id)
            if validators.url(checked_items[stored_index][1]):
                webbrowser.open(checked_items[stored_index][1])
                self.item_id_link_input.text = ''
            elif validators.url(checked_items[stored_index][2]):
                webbrowser.open(checked_items[stored_index][2])
                self.item_id_link_input.text = ''
            elif validators.url(checked_items[stored_index][3]):
                webbrowser.open(checked_items[stored_index][3])
                self.item_id_link_input.text = ''
            elif validators.url(checked_items[stored_index][4]):
                webbrowser.open(checked_items[stored_index][4])
                self.item_id_link_input.text = ''
            else:
                show_popup(0, 5)



        except:
            show_popup(0,4)
    # Used to download the items in the cart
    def save_selected_items(self, button):
        # Checks if items are in the cart
        if guest == False:
            if len(checked_items) == 0:
                show_popup(1,2)
            else:
                selected_rows = []
                for row_index in checked_items:
                    selected_row = {"ID": row_index[0], "Data 1": row_index[1], "Data 2": row_index[2], "Data 3": row_index[3],
                                    "Data 4": row_index[4]}
                    selected_rows.append(selected_row)

                # Create a pandas DataFrame from the selected rows
                selected_df = pd.DataFrame(selected_rows)

                # Random number code for saving data
                rand_num = random.randint(1, 10 ** 100)
                # Save the DataFrame to an Excel file
                filename = f"{text1}selected_items{rand_num}.csv"

                # Get the user's Downloads folder path
                try:
                    # For Windows
                    downloads_folder = os.path.join(os.environ["HOMEPATH"], "Downloads")
                except KeyError:
                    try:
                        # For macOS/iOS
                        downloads_folder = os.path.join(os.environ["HOME"], "Downloads")
                    except KeyError:
                        # For Linux and other platforms
                        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

                # Create the full file path
                filepath = os.path.join(downloads_folder, filename)

                # Save the DataFrame to the file path
                selected_df.to_csv(filepath, index=False)
                show_popup(0, 0)
        else:
            show_popup(0,3)

    def remove_item_id(self, instance):
        global cart_count
        global checked_items
        global store_ids
        # Text input
        try:
            print(self.item_id_input.text, "xxxx")
            item_id = int(self.item_id_input.text)


            # Checks if the input is a positive number and less than data length
            if item_id < len(data) and item_id >= 0:
                # If the item id is stored remove it from the list and update cart
                if item_id in store_ids:

                    stored_index = store_ids.index(item_id)
                    del store_ids[stored_index]
                    del checked_items[stored_index]
                    cart_count -= 1
                    self.item_id_input.text = ""

                # Add item ID to the cart and update the cart
                else:
                    print("cant only remove items")
            else:
                show_popup(1, 1)
        except:
            show_popup(1, 1)

    def quit(self, button):
        global cart_count
        global checked_items
        global store_ids
        if text1 == "":
            pass
        else:
            try:
                cart_count = 0
                checked_items.clear()
                store_ids.clear()
                os.remove(f'{text1}.xlsx')
                MyApp.get_running_app().stop()
            except:
                pass

class ScreenManagement(ScreenManager):
    pass

def show_popup(index_t, index_s):
    sentences = ["Data Saved", "Invalid number", "Must select items to use this button", "Guest users cannot save data", "ID is not in the cart", "Sorry, product link is not valid"]
    titles = ["Success", "Error"]
    content = Label(text=sentences[index_s])
    popup = Popup(title=titles[index_t], content=content, size_hint=(None, None), size=(400, 400))
    popup.open()
    # close popup after 3 seconds
    Clock.schedule_once(popup.dismiss, 3)

class MyApp(MDApp):
    def build(self):
        screen_manager = ScreenManagement()
        screen_manager.add_widget(ScreenOne(name='screen_one'))
        screen_manager.add_widget(ScreenTwo(name='screen_two'))
        return screen_manager

    def go_to_screen_two(self, instance):
        self.root.current = 'screen_two'














def run_data2(text, guest1):
    global data
    global text1
    global guest
    guest = guest1
    text1 = text
    # Read Excel file
    df = pd.read_excel(f'{text}.xlsx')

    # Stores the data
    data = []

    for row in df.itertuples(index=False):
        data.append((row[0], row[1], row[2], row[3], row[4]))

    MyApp().run()




