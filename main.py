from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
import weekday_checker
import random
import scraper
import string
import own_scraper_data_display
import built_in_scraper_data_display
#from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle
from kivymd.uix.button import MDRaisedButton
#from kivymd.uix.toolbar import MDTopAppBar
from kivy.config import Config
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.boxlayout import BoxLayout

import data
import register
import sqlite3
import hashlib
import re
from kivy.utils import get_color_from_hex

import webbrowser
import validators
import building_scraper as bs
guest = False
user = ''
recommend_items = False
number = 0
screen_helper = """
ScreenManager:
    MenuScreen:
    Login:
    UploadScreen:
    Register:
    ScraperOptionsMenu:
    ForgotPassword:
    Scraper_options:
    BuildScraper:
    Recommendations:
    ScraperData:

    
<MenuScreen>:
    name: 'menu'
    MDCard:
        size_hint: None, None
        size: 300, 480
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 1000
        padding:25
        spacing: 25
        md_bg_color: get_color_from_hex('#E1D9D1')
    
        orientation: 'vertical'
        
        MDLabel:
            text: "Welcome to Best Match"
            font_size: 30
            halign: 'center'
            pos_hint: {'center_x':0.5,'center_y':1}
            padding_y: 15
            

        MDRaisedButton:
            text: 'Login'
            pos_hint: {'center_x':0.5,'center_y':0.8}
            on_press: root.manager.current = 'Login'
            size_hint_x: 0.45
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)
            
        MDRaisedButton:
            text: 'Register'
            pos_hint: {'center_x':0.5,'center_y':0.7}
            on_press: root.manager.current = 'Register'
            size_hint_x: 0.45
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)
            
        
        MDRaisedButton:
            text: 'Guest'
            pos_hint: {'center_x':0.5,'center_y':0.6}
            on_press: app.guest()
            size_hint_x: 0.45
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)    
        
        MDRaisedButton:
            text: 'Forgot Password'
            pos_hint: {'center_x':0.5,'center_y':0.5}
            on_press: root.manager.current = 'Forgot'
            size_hint_x: 0.45
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)
            
            
            
        MDRaisedButton:
            text: 'Quit'
            pos_hint: {'center_x':0.5,'center_y':0.4}
            on_press: app.quit()
            size_hint_x: 0.45
            md_bg_color: (0.8, 0, 0, 1)
            text_color: (1, 1, 1, 1)
            
        
    MDIconButton:
        size_hint: None, None
        icon: "facebook"
        pos_hint: {'center_x':0.4, 'y':0.1}
        theme_text_color: "Custom"
        text_color: (1, 1, 1, 1)
        icon_color: (0.09, 0.47, 0.95, 1) 
        
        on_release: app.open_facebook()
        
    MDIconButton:
        size_hint: None, None
        icon: "instagram"
        theme_text_color: "Custom"
        text_color: (0.57, 0.21, 0.80, 1)  # set the color of the icon to white
        pos_hint: {'center_x':0.35, 'y':0.1}
        on_release: app.open_instagram()
        

<BuildScraper>:
    name: 'buildScraper'
    MDCard:
        size_hint: None, None
        size: 800, 800
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 1000
        md_bg_color: get_color_from_hex('#E1D9D1')
        padding:25
        spacing: 25

        orientation: 'vertical'
    
        
    MDTextField:
        id: base_url
        hint_text: "Enter base_url"
        icon_right: "key-link"
        size_hint_x: None
        width: 200
        font_size: 18
        pos_hint: {"center_x":0.5, 'center_y':0.9}
        hint_text_color_normal: (0, 0.349, 0.686, 1)
        text_color_focus: (0, 0, 0, 1)
        text_color_normal: (0, 0, 0, 1)
        line_color_focus: (0, 0.349, 0.686, 1)
        line_text_color_focus: (0, 0.349, 0.686, 1)
        password: False

        
    MDTextField:
        id: url
        hint_text: "Enter item url"
        icon_right: "link"
        size_hint_x: None
        width: 200
        font_size: 18
        pos_hint: {"center_x":0.5, 'center_y':0.8}
        hint_text_color_normal: (0, 0.349, 0.686, 1)
        text_color_focus: (0, 0, 0, 1)
        text_color_normal: (0, 0, 0, 1)
        line_color_focus: (0, 0.349, 0.686, 1)
        line_text_color_focus: (0, 0.349, 0.686, 1)
        password: False
        
    MDTextField:
        id: item
        hint_text: "Enter item name"
        icon_right: "tag-text"
        size_hint_x: None
        width: 200
        font_size: 18
        pos_hint: {"center_x":0.5, 'center_y':0.7}
        hint_text_color_normal: (0, 0.349, 0.686, 1)
        text_color_focus: (0, 0, 0, 1)
        text_color_normal: (0, 0, 0, 1)
        line_color_focus: (0, 0.349, 0.686, 1)
        line_text_color_focus: (0, 0.349, 0.686, 1)
        password: False

    
    MDLabel:
        text: "Enter product html list"
        pos_hint: {'x':0.1,'y':0.1}
    
    
    MDTextField:
        id: product_list1
        hint_text: "tag"
        size_hint_x: None
        width: 60
        font_size: 18
        hint_text_color_normal: (0, 0.349, 0.686, 1)
        text_color_focus: (0, 0, 0, 1)
        text_color_normal: (0, 0, 0, 1)
        line_color_focus: (0, 0.349, 0.686, 1)
        line_text_color_focus: (0, 0.349, 0.686, 1)
        pos_hint: {"center_x":0.4, 'center_y':0.6}
        password: False

        
    MDTextField:
        id: product_list2
        hint_text: "class"
        size_hint_x: None
        width: 60
        font_size: 18
        hint_text_color_normal: (0, 0.349, 0.686, 1)
        text_color_focus: (0, 0, 0, 1)
        text_color_normal: (0, 0, 0, 1)
        line_color_focus: (0, 0.349, 0.686, 1)
        line_text_color_focus: (0, 0.349, 0.686, 1)
        pos_hint: {"center_x":0.5, 'center_y':0.6}
        password: False
 
    
    MDTextField:
        id: product_list3
        hint_text: "value"
        size_hint_x: None
        width: 60
        font_size: 18
        hint_text_color_normal: (0, 0.349, 0.686, 1)
        text_color_focus: (0, 0, 0, 1)
        text_color_normal: (0, 0, 0, 1)
        line_color_focus: (0, 0.349, 0.686, 1)
        line_text_color_focus: (0, 0.349, 0.686, 1)
        pos_hint: {"center_x":0.6, 'center_y':0.6}
        password: False
    
    
    MDTextField:
        id: first_data1
        hint_text: "tag"
        size_hint_x: None
        width: 60
        font_size: 18
        hint_text_color_normal: (0, 0.349, 0.686, 1)
        text_color_focus: (0, 0, 0, 1)
        text_color_normal: (0, 0, 0, 1)
        line_color_focus: (0, 0.349, 0.686, 1)
        line_text_color_focus: (0, 0.349, 0.686, 1)
        pos_hint: {"center_x":0.4, 'center_y':0.5}
        password: False

        
        
    MDTextField:
        id: first_data2
        hint_text: "class"
        size_hint_x: None
        width: 60
        font_size: 18
        hint_text_color_normal: (0, 0.349, 0.686, 1)
        text_color_focus: (0, 0, 0, 1)
        text_color_normal: (0, 0, 0, 1)
        line_color_focus: (0, 0.349, 0.686, 1)
        line_text_color_focus: (0, 0.349, 0.686, 1)
        pos_hint: {"center_x":0.5, 'center_y':0.5}
        password: False
  
    
    MDTextField:
        id: first_data3
        hint_text: "value"
        size_hint_x: None
        width: 60
        font_size: 18
        hint_text_color_normal: (0, 0.349, 0.686, 1)
        text_color_focus: (0, 0, 0, 1)
        text_color_normal: (0, 0, 0, 1)
        line_color_focus: (0, 0.349, 0.686, 1)
        line_text_color_focus: (0, 0.349, 0.686, 1)
        pos_hint: {"center_x":0.6, 'center_y':0.5}
        password: False

    

    MDTextField:
        id: second_data1
        hint_text: "tag"
        size_hint_x: None
        width: 60
        font_size: 18
        hint_text_color_normal: (0, 0.349, 0.686, 1)
        text_color_focus: (0, 0, 0, 1)
        text_color_normal: (0, 0, 0, 1)
        line_color_focus: (0, 0.349, 0.686, 1)
        line_text_color_focus: (0, 0.349, 0.686, 1)
        pos_hint: {"center_x":0.4, 'center_y':0.4}
        password: False

        
        
    MDTextField:
        id: second_data2
        hint_text: "class"
        size_hint_x: None
        width: 60
        font_size: 18
        hint_text_color_normal: (0, 0.349, 0.686, 1)
        text_color_focus: (0, 0, 0, 1)
        text_color_normal: (0, 0, 0, 1)
        line_color_focus: (0, 0.349, 0.686, 1)
        line_text_color_focus: (0, 0.349, 0.686, 1)
        pos_hint: {"center_x":0.5, 'center_y':0.4}
        password: False

    
    MDTextField:
        id: second_data3
        hint_text: "value"
        size_hint_x: None
        width: 60
        font_size: 18
        hint_text_color_normal: (0, 0.349, 0.686, 1)
        text_color_focus: (0, 0, 0, 1)
        text_color_normal: (0, 0, 0, 1)
        line_color_focus: (0, 0.349, 0.686, 1)
        line_text_color_focus: (0, 0.349, 0.686, 1)
        pos_hint: {"center_x":0.6, 'center_y':0.4}
        password: False
  
    

        
    MDTextField:
        id: third_data1
        hint_text: "tag"
        size_hint_x: None
        width: 60
        font_size: 18
        hint_text_color_normal: (0, 0.349, 0.686, 1)
        text_color_focus: (0, 0, 0, 1)
        text_color_normal: (0, 0, 0, 1)
        line_color_focus: (0, 0.349, 0.686, 1)
        line_text_color_focus: (0, 0.349, 0.686, 1)
        pos_hint: {"center_x":0.4, 'center_y':0.3}
        password: False

        
        
    MDTextField:
        id: third_data2
        hint_text: "class"
        size_hint_x: None
        width: 60
        font_size: 18
        hint_text_color_normal: (0, 0.349, 0.686, 1)
        text_color_focus: (0, 0, 0, 1)
        text_color_normal: (0, 0, 0, 1)
        line_color_focus: (0, 0.349, 0.686, 1)
        line_text_color_focus: (0, 0.349, 0.686, 1)
        pos_hint: {"center_x":0.5, 'center_y':0.3}
        password: False

    
    MDTextField:
        id: third_data3
        hint_text: "value"
        size_hint_x: None
        width: 60
        font_size: 18
        hint_text_color_normal: (0, 0.349, 0.686, 1)
        text_color_focus: (0, 0, 0, 1)
        text_color_normal: (0, 0, 0, 1)
        line_color_focus: (0, 0.349, 0.686, 1)
        line_text_color_focus: (0, 0.349, 0.686, 1)
        pos_hint: {"center_x":0.6, 'center_y':0.3}
        password: False

    
    MDTextField:
        id: fourth_data1
        hint_text: "tag"
        size_hint_x: None
        width: 60
        font_size: 18
        hint_text_color_normal: (0, 0.349, 0.686, 1)
        text_color_focus: (0, 0, 0, 1)
        text_color_normal: (0, 0, 0, 1)
        line_color_focus: (0, 0.349, 0.686, 1)
        line_text_color_focus: (0, 0.349, 0.686, 1)
        pos_hint: {"center_x":0.4, 'center_y':0.2}
        password: False

        
        
    MDTextField:
        id: fourth_data2
        hint_text: "class"
        size_hint_x: None
        width: 60
        font_size: 18
        hint_text_color_normal: (0, 0.349, 0.686, 1)
        text_color_focus: (0, 0, 0, 1)
        text_color_normal: (0, 0, 0, 1)
        line_color_focus: (0, 0.349, 0.686, 1)
        line_text_color_focus: (0, 0.349, 0.686, 1)
        pos_hint: {"center_x":0.5, 'center_y':0.2}
        password: False
    
    
    MDTextField:
        id: fourth_data3
        hint_text: "value"
        size_hint_x: None
        width: 60
        font_size: 18
        hint_text_color_normal: (0, 0.349, 0.686, 1)
        text_color_focus: (0, 0, 0, 1)
        text_color_normal: (0, 0, 0, 1)
        line_color_focus: (0, 0.349, 0.686, 1)
        line_text_color_focus: (0, 0.349, 0.686, 1)
        pos_hint: {"center_x":0.6, 'center_y':0.2}
        password: False
       
        
    MDRaisedButton:
        text: 'Start'
        pos_hint: {'center_x':0.5,'center_y':0.1}
        md_bg_color: (0, 0.349, 0.686, 1)
        text_color: (1, 1, 1, 1)
        on_press: app.check_html()
        
    MDRaisedButton:
        text: 'Help'
        pos_hint: {'center_x':0.4,'center_y':0.1}
        md_bg_color: (0, 0.349, 0.686, 1)
        text_color: (1, 1, 1, 1)
        on_press: app.show_popup_video()
        
    MDRaisedButton:
        text: 'Back'
        pos_hint: {'center_x':0.6,'center_y':0.1}
        md_bg_color: (0, 0.349, 0.686, 1)
        text_color: (1, 1, 1, 1)
        on_press: root.manager.current = 'Scraper_options'

        
        
        
<ScraperData>:
    name: 'ScraperData'
    MDCard:
        size_hint: None, None
        size: 300, 480
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 1000
        md_bg_color: get_color_from_hex('#E1D9D1')
        padding:25
        spacing: 25

        orientation: 'vertical'
        
        MDLabel:
            text: "Enter an item to check if it has been extracted from built in scrapers"
            font_size: 30
            halign: 'center'
            pos_hint: {"center_x": 0.5, "center_y": 0.55}
            padding_y: 15
        

        
        MDTextField:
            id: item
            hint_text: "Enter item"
            icon_right: "search-web"
            size_hint_x: None
            width: 200
            font_size: 18
            pos_hint: {"center_x":0.5, 'center_y':0.9}
            password: False
            hint_text_color_normal: (0, 0.349, 0.686, 1)
            text_color_focus: (0, 0, 0, 1)
            text_color_normal: (0, 0, 0, 1)
            line_color_focus: (0, 0.349, 0.686, 1)
            line_text_color_focus: (0, 0.349, 0.686, 1)
            on_text: app.check_data_text()  # bind on_text event to check_text function
            
        MDRaisedButton:
            id: data
            text: 'Check data'
            pos_hint: {'center_x':0.5,'center_y':0.7}
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)
            disabled: True
            size_hint_x: 0.45
            on_press : app.check_database()
        
        MDIconButton:
            icon: "arrow-left"
            pos_hint: {"center_x": 0.5, "center_y": 1}
            on_press: root.manager.current = 'Scraper_options'
        
            
        

        
    

     
<ScraperOptionsMenu>:
    name: 'optionsMenu'
    MDCard:
        size_hint: None, None
        size: 300, 480
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 1000
        md_bg_color: get_color_from_hex('#E1D9D1')
        padding:25
        spacing: 25

        orientation: 'vertical'
        MDIconButton:
            icon: "arrow-left"
            pos_hint: {"center_x": 0.5, "center_y": 0.6}
            on_press: root.manager.current = 'recommendations_menu'
        
        MDTextField:
            id: item
            hint_text: "Enter item"
            icon_right: "search-web"
            size_hint_x: None
            width: 200
            font_size: 18
            pos_hint: {"center_x":0.5, 'center_y':0.8}
            password: False
            hint_text_color_normal: (0, 0.349, 0.686, 1)
            text_color_focus: (0, 0, 0, 1)
            text_color_normal: (0, 0, 0, 1)
            line_color_focus: (0, 0.349, 0.686, 1)
            line_text_color_focus: (0, 0.349, 0.686, 1)
            on_text: app.check_text()  # bind on_text event to check_text function
            
        MDRaisedButton:
            id: All_websites
            text: 'All websites'
            pos_hint: {'center_x':0.5,'center_y':0.6}
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)
            disabled: True
            size_hint_x: 0.45
            on_press: app.all_websites()
    
        MDRaisedButton:
            id: amazon
            text: 'Amazon'
            pos_hint: {'center_x':0.5,'center_y':0.5}
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)
            disabled: True
            size_hint_x: 0.45
            on_press: app.amazon()
    
    
        MDRaisedButton:
            id: argos
            text: 'Argos'
            pos_hint: {'center_x':0.5,'center_y':0.4}
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)
            disabled: True
            size_hint_x: 0.45
            on_press: app.argos()
    
        MDRaisedButton:
            id: ebay
            text: 'Ebay'
            pos_hint: {'center_x':0.5,'center_y':0.3}
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)
            disabled: True
            size_hint_x: 0.45
            on_press: app.ebay()
    
        MDRaisedButton:
            id: johnlewis
            text: 'Johnlewis'
            pos_hint: {'center_x':0.5,'center_y':0.2}
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)
            disabled: True
            size_hint_x: 0.45
            on_press: app.john_lewis()
        

<ForgotPassword>:
    name: 'Forgot'
    MDCard:
        size_hint: None, None
        size: 300, 480
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 1000
        md_bg_color: get_color_from_hex('#E1D9D1')
        padding: 15
        spacing: 15

        orientation: 'vertical'

        MDLabel:
            text: "Forgot Password"
            font_size: 30
            halign: 'center'
            pos_hint: {"center_x": 0.5, "center_y": 0.55}
            padding_y: 15

        MDTextField:
            id: user
            hint_text: "username"
            icon_right: "account"
            size_hint_x: None
            width: 200
            font_size: 18
            pos_hint: {"center_x":0.5}
            hint_text_color_normal: (0, 0.349, 0.686, 1)
            text_color_focus: (0, 0, 0, 1)
            text_color_normal: (0, 0, 0, 1)
            line_color_focus: (0, 0.349, 0.686, 1)
            line_text_color_focus: (0, 0.349, 0.686, 1)
            
        MDTextField:
            id: word
            hint_text: "2FA"
            icon_right: "file-word-box"
            size_hint_x: None
            width: 200
            font_size: 18
            pos_hint: {"center_x":0.5}
            password: False
            hint_text_color_normal: (0, 0.349, 0.686, 1)
            text_color_focus: (0, 0, 0, 1)
            text_color_normal: (0, 0, 0, 1)
            line_color_focus: (0, 0.349, 0.686, 1)
            line_text_color_focus: (0, 0.349, 0.686, 1)

        MDTextField:
            id: password
            hint_text: "new password"
            icon_right: "eye"
            size_hint_x: None
            width: 200
            font_size: 18
            pos_hint: {"center_x":0.5}
            password: False
            hint_text_color_normal: (0, 0.349, 0.686, 1)
            text_color_focus: (0, 0, 0, 1)
            text_color_normal: (0, 0, 0, 1)
            line_color_focus: (0, 0.349, 0.686, 1)
            line_text_color_focus: (0, 0.349, 0.686, 1)
            
        MDTextField:
            id: confirmpassword
            hint_text: "Confirm password"
            icon_right: "eye-off"
            size_hint_x: None
            width: 200
            font_size: 18
            pos_hint: {"center_x":0.5}
            password: True
            hint_text_color_normal: (0, 0.349, 0.686, 1)
            text_color_focus: (0, 0, 0, 1)
            text_color_normal: (0, 0, 0, 1)
            line_color_focus: (0, 0.349, 0.686, 1)
            line_text_color_focus: (0, 0.349, 0.686, 1)
        
        
        MDRoundFlatButton:
            text: "Confirm"
            font_size: 12
            pos_hint: {"center_x":0.5}
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)
            on_press: app.forgot_password()

        MDRoundFlatButton:
            text: "Menu"
            font_size: 12
            pos_hint: {"center_x":0.5}
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)
            on_press: root.manager.current = 'menu'
        

<Recommendations>:
    name: 'recommendations_menu'
    MDCard:
        size_hint: None, None
        size: 300, 480
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 1000
        md_bg_color: get_color_from_hex('#E1D9D1')
        padding:25
        spacing: 25

        orientation: 'vertical'
        
        MDLabel:
            text: "Scraper Options"
            font_size: 30
            halign: 'center'
            pos_hint: {"center_x": 0.5, "center_y": 0.55}
            padding_y: 15
            
            
            
        MDRaisedButton:
            text: "Extract Page"
            pos_hint: {"center_x": 0.5}
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)
            size_hint_x: 0.5
            on_press: root.manager.current = 'optionsMenu'
            
        MDRaisedButton:
            text: "Extract Input"
            pos_hint: {"center_x":0.5}
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)
            size_hint_x: 0.5
            on_press: app.recommend_option_guest()
            
        MDRaisedButton:
            text: "Extracted Data"
            pos_hint: {"center_x": 0.5}
            md_bg_color: (0, 0.349, 0.686, 1)
            size_hint_x: 0.5
            text_color: (1, 1, 1, 1)
            on_press : app.extract_data_guest()
            
        MDRaisedButton:
            text: "Items in Cart"
            pos_hint: {"center_x": 0.5}
            md_bg_color: (0, 0.349, 0.686, 1)
            size_hint_x: 0.5
            text_color: (1, 1, 1, 1)
            on_press : app.check_cart()
        
        MDRaisedButton:
            text: "Help"
            pos_hint: {"center_x": 0.5}
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)
            size_hint_x: 0.5
            on_press: app.show_popup(2, 34)
            
        MDRaisedButton:
            text: "Previous Page"
            pos_hint: {"center_x": 0.5}
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)
            size_hint_x: 0.5
            on_press: root.manager.current = 'Scraper_options'
            
        MDRaisedButton:
            text: "Quit"
            pos_hint: {"center_x": 0.5}
            md_bg_color: (0.8, 0, 0, 1)
            text_color: (1, 1, 1, 1)
            size_hint_x: 0.5
            on_press: app.quit()



<Scraper_options>:
    name: 'Scraper_options'
    MDCard:
        size_hint: None, None
        size: 300, 480
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 1000
        md_bg_color: get_color_from_hex('#E1D9D1')
        padding:25
        spacing: 25

        orientation: 'vertical'
        
        MDLabel:
            text: "Types of Scrapers"
            font_size: 30
            halign: 'center'
            pos_hint: {"center_x": 0.5, "center_y": 0.55}
            padding_y: 15
            
        MDRaisedButton:
            text: "Pre-made Websites"
            pos_hint: {"center_x":0.5}
            on_press: root.manager.current = 'recommendations_menu'
            md_bg_color: (0, 0.349, 0.686, 1)
            size_hint_x: 0.5
            text_color: (1, 1, 1, 1)
    
        MDRaisedButton:
            text: "Own Websites"
            pos_hint: {"center_x": 0.5}
            on_press: app.own_website()
            md_bg_color: (0, 0.349, 0.686, 1)
            size_hint_x: 0.5
            text_color: (1, 1, 1, 1)
            
            
        
        MDRaisedButton:
            text: "Help"
            pos_hint: {"center_x": 0.5}
            md_bg_color: (0, 0.349, 0.686, 1)
            size_hint_x: 0.5
            text_color: (1, 1, 1, 1)
            on_press: app.show_popup(2, 33)
        MDRaisedButton:
            text: "Menu"
            pos_hint: {"center_x": 0.5}
            md_bg_color: (0, 0.349, 0.686, 1)
            size_hint_x: 0.5
            text_color: (1, 1, 1, 1)
            on_press: root.manager.current = 'menu'
        
        MDRaisedButton:
            text: "Quit"
            pos_hint: {"center_x": 0.5}
            md_bg_color: (0.8, 0, 0, 1)
            text_color: (1, 1, 1, 1)
            size_hint_x: 0.5
            on_press: app.quit()
        

<Register>:
    name: 'Register'
    MDCard:
        size_hint: None, None
        size: 300, 480
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 1000
        md_bg_color: get_color_from_hex('#E1D9D1')
        padding:25
        spacing: 25

        orientation: 'vertical'

        MDLabel:
            text: "Register"
            font_size: 30
            halign: 'center'
            pos_hint: {"center_x": 0.5, "center_y": 0.55}
            padding_y: 15

        MDTextField:
            id: user
            hint_text: "username"
            icon_right: "account"
            size_hint_x: None
            width: 200
            font_size: 18
            hint_text_color_normal: (0, 0.349, 0.686, 1)
            text_color_focus: (0, 0, 0, 1)
            text_color_normal: (0, 0, 0, 1)
            line_color_focus: (0, 0.349, 0.686, 1)
            line_text_color_focus: (0, 0.349, 0.686, 1)
            pos_hint: {"center_x":0.5}

        MDTextField:
            id: password
            hint_text: "password"
            icon_right: "eye"
            size_hint_x: None
            width: 200
            font_size: 18
            pos_hint: {"center_x":0.5}
            hint_text_color_normal: (0, 0.349, 0.686, 1)
            text_color_focus: (0, 0, 0, 1)
            text_color_normal: (0, 0, 0, 1)
            line_color_focus: (0, 0.349, 0.686, 1)
            line_text_color_focus: (0, 0.349, 0.686, 1)
            password: False
            
        MDTextField:
            id: confirmpassword
            hint_text: "Confirm password"
            icon_right: "eye"
            size_hint_x: None
            width: 200
            font_size: 18
            pos_hint: {"center_x":0.5}
            hint_text_color_normal: (0, 0.349, 0.686, 1)
            text_color_focus: (0, 0, 0, 1)
            text_color_normal: (0, 0, 0, 1)
            line_color_focus: (0, 0.349, 0.686, 1)
            line_text_color_focus: (0, 0.349, 0.686, 1)
            password: False
        
        MDRoundFlatButton:
            text: "Register"
            font_size: 12
            pos_hint: {"center_x":0.5}
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)
            on_press: app.register()
            

        MDRoundFlatButton:
            text: "Menu"
            font_size: 12
            pos_hint: {"center_x":0.5}
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)
            on_press: root.manager.current = 'menu'

<Login>:
    name: 'Login'
    MDCard:
        size_hint: None, None
        size: 300, 480
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        elevation: 1000
        padding:25
        spacing: 25
        md_bg_color: get_color_from_hex('#E1D9D1')
        orientation: 'vertical'

        MDLabel:
            text: "Please login"
            font_size: 30
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: 15
            

        MDTextField:
            id: user
            hint_text: "username"
            icon_right: "account"
            size_hint_x: None
            width: 200
            font_size: 18
            pos_hint: {"center_x":0.5}
            hint_text_color_normal: (0, 0.349, 0.686, 1)
            text_color_focus: (0, 0, 0, 1)
            text_color_normal: (0, 0, 0, 1)
            line_color_focus: (0, 0.349, 0.686, 1)
            line_text_color_focus: (0, 0.349, 0.686, 1)


        MDTextField:
            id: password
            hint_text: "password"
            icon_right: "eye-off"
            size_hint_x: None
            width: 200
            font_size: 18
            pos_hint: {"center_x":0.5}
            password: True
            hint_text_color_normal: (0, 0.349, 0.686, 1)
            text_color_focus: (0, 0, 0, 1)
            text_color_normal: (0, 0, 0, 1)
            line_color_focus: (0, 0.349, 0.686, 1)
            line_text_color_focus: (0, 0.349, 0.686, 1)

        MDRoundFlatButton:
            text: "Login"
            font_size: 12
            pos_hint: {"center_x":0.5}
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1) 
            on_press: app.login()

        MDRoundFlatButton:
            text: "Menu"
            font_size: 12
            pos_hint: {"center_x":0.5}
            md_bg_color: (0, 0.349, 0.686, 1)
            text_color: (1, 1, 1, 1)
            on_press: root.manager.current = 'menu'
            
<UploadScreen>:
    name: 'upload'
    MDLabel:
        text: 'Upload'
        halign: 'center'
    MDRectangleFlatButton:
        text: 'Back'
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: root.manager.current = 'menu'
        

"""

'''
All of these classes are used to create the screens
'''
class MenuScreen(Screen):
    pass

class BuildScraper(Screen):
    pass


class Login(Screen):
    pass


class UploadScreen(Screen):
    pass

class Register(Screen):
    pass

class ScraperOptionsMenu(Screen):
    pass

class ForgotPassword(Screen):
    pass

class Scraper_options(Screen):
    pass

class Recommendations(Screen):
    pass
class ScraperData(Screen):
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(Login(name='Login'))
sm.add_widget(Register(name='Register'))
sm.add_widget(ScraperOptionsMenu(name='optionsMenu'))
sm.add_widget(UploadScreen(name='quit'))
sm.add_widget(ForgotPassword(name="Forgot"))
sm.add_widget(ForgotPassword(name="Scraper_options"))
sm.add_widget(BuildScraper(name="BuildScraper"))
sm.add_widget(Recommendations(name="recommendations_menu"))
sm.add_widget(ScraperData(name="ScraperData"))




class DemoApp(MDApp):
    #Builds the demo app
    def build(self):
        self.theme_cls.bg_color = (0, 0, 0, 1)  # Set background color to black
        self.theme_cls.theme_style = "Light"
        #self.theme_cls.primary_palette = "BlueGray"
        Config.set('graphics', 'resizable', False)
        #Builds the screen
        screen = Builder.load_string(screen_helper)


        return screen
    # Enables guest
    def guest(self):
        global guest
        guest = True
        self.root.current = 'Scraper_options'
    # Enables scraping only input
    def recommend_items(self):
        global recommend_items
        recommend_items = True
        self.root.current = 'optionsMenu'
    # Guest users are not allowed to use only input scraper
    def recommend_option_guest(self):
        if guest == True:
            self.show_popup(0,31)
        else:
            self.recommend_items()
    # Guest is not allowed to gain access to masterdata
    def extract_data_guest(self):
        if guest == True:
            self.show_popup(0,31)
        else:
            self.root.current = 'ScraperData'




    # Goes to the build your own website scraper, guest is not allowed to use it
    def own_website(self):
        if guest == True:
            self.show_popup(0,31)
        else:
            self.root.current = 'buildScraper'
    '''
    Used to access the build your own web scraper checks
    Checks if all the used text boxes are properly filled and checks if the links are valid
    '''
    def check_html(self):
        # All the text inputs
        base_url = self.root.get_screen("buildScraper").ids.base_url.text
        print(base_url)
        product_list1 = self.root.get_screen("buildScraper").ids.product_list1.text
        product_list2 = self.root.get_screen("buildScraper").ids.product_list2.text
        product_list3 = self.root.get_screen("buildScraper").ids.product_list3.text
        first_data1 = self.root.get_screen("buildScraper").ids.first_data1.text
        first_data2 = self.root.get_screen("buildScraper").ids.first_data2.text
        first_data3 = self.root.get_screen("buildScraper").ids.first_data3.text
        second_data1 = self.root.get_screen("buildScraper").ids.second_data1.text
        second_data2 = self.root.get_screen("buildScraper").ids.second_data2.text
        second_data3 = self.root.get_screen("buildScraper").ids.second_data3.text
        third_data1 =  self.root.get_screen("buildScraper").ids.third_data1.text
        third_data2 = self.root.get_screen("buildScraper").ids.third_data2.text
        third_data3 = self.root.get_screen("buildScraper").ids.third_data3.text
        fourth_data1 = self.root.get_screen("buildScraper").ids.fourth_data1.text
        fourth_data2 = self.root.get_screen("buildScraper").ids.fourth_data2.text
        fourth_data3 = self.root.get_screen("buildScraper").ids.fourth_data3.text
        item = self.root.get_screen("buildScraper").ids.item.text

        # Checks if the url is an actual link
        if validators.url(base_url):
            print("url valid")
            url = self.root.get_screen("buildScraper").ids.url.text
            if url == base_url:
                self.show_popup(0, 13)
            # Checks if the product url is valid
            elif validators.url(url):
                # Checks if an item is typed
                if len(item) != 0:
                    # Makes sure product list is not empty
                    if len(product_list1) > 0 and len(product_list2) > 0 and len(product_list3) > 0:
                        # Checks if the first html element data is not empty and makes sure the rest are
                        if len(first_data1) > 0 and len(first_data2) > 0 and len(first_data3) > 0:
                            if len(second_data1) > 0 and len(second_data2) > 0 and len(second_data3) > 0:
                                if len(third_data1) > 0  and len(third_data2) > 0 and len(third_data3) > 0:
                                    if len(fourth_data1) > 0 and len(fourth_data2) > 0 and len(fourth_data3) > 0:
                                        own_scraper = bs.build_scraper(item_name=item,
                                                                       normal_url=base_url, url=url,
                                                                       html_tag1=[product_list1, product_list2,
                                                                                  product_list3],
                                                                       html_tag2=[first_data1, first_data2,
                                                                                  first_data3],
                                                                       html_tag3=[second_data1, second_data2,
                                                                                  second_data3],
                                                                       html_tag4=[third_data1, third_data2,
                                                                                  third_data3], html_tag5=[fourth_data1, fourth_data2, fourth_data3])
                                        own_scraper.check_tags()
                                        data = own_scraper.scraper()
                                        if len(data) == 0:
                                            print("No data extracted")
                                        else:
                                            own_scraper.data_save()
                                            DemoApp.get_running_app().stop()
                                            own_scraper_data_display.run_data2(item, guest)
                                            DemoApp().run()
                                    # Checks if the fourth html element data is not empty and makes sure the rest are
                                    elif fourth_data1 == "" and fourth_data2 == "" and fourth_data3 == "":
                                        own_scraper = bs.build_scraper(item_name=item,
                                                                       normal_url=base_url, url=url,
                                                                       html_tag1=[product_list1, product_list2,
                                                                                  product_list3],
                                                                       html_tag2=[first_data1, first_data2,
                                                                                  first_data3],
                                                                       html_tag3=[second_data1, second_data2,
                                                                                  second_data3],
                                                                       html_tag4=[third_data1, third_data2, third_data3], html_tag5=["", "", ""])
                                        own_scraper.check_tags()
                                        data = own_scraper.scraper()

                                        if len(data) == 0:
                                            print("No data extracted")
                                        else:
                                            own_scraper.data_save()
                                            DemoApp.get_running_app().stop()
                                            own_scraper_data_display.run_data2(item, guest)
                                            DemoApp().run()
                                    else:
                                        self.show_popup(0, 19)
                                # Checks if the third html element data is not empty and makes sure the rest are
                                if third_data1 == "" and third_data2 == "" and third_data3 == "":
                                    if fourth_data1 == "" and fourth_data2 == "" and fourth_data3 == "":
                                        own_scraper = bs.build_scraper(item_name=item,
                                                                       normal_url=base_url, url=url,
                                                                       html_tag1=[product_list1, product_list2,
                                                                                  product_list3],
                                                                       html_tag2=[first_data1, first_data2,
                                                                                  first_data3], html_tag3=[second_data1, second_data2, second_data3],
                                                                       html_tag4=["", "", ""], html_tag5=["", "", ""])
                                        own_scraper.check_tags()
                                        data = own_scraper.scraper()
                                        if len(data) == 0:
                                            print("No data extracted")
                                        else:
                                            own_scraper.data_save()
                                            DemoApp.get_running_app().stop()
                                            own_scraper_data_display.run_data2(item, guest)
                                            DemoApp().run()
                                    else:
                                        self.show_popup(0, 18)
                            # Checks if the second html element data is not empty and makes sure the rest are
                            if second_data1 == "" and second_data2 == "" and second_data3 == "":
                                if third_data1 == "" and third_data2 == "" and third_data3 == "":
                                    if fourth_data1 == "" and fourth_data2 == "" and fourth_data3 == "":
                                        print("ready to scrape 1")
                                        own_scraper = bs.build_scraper(item_name=item,
                                                                       normal_url=base_url, url=url,
                                                                       html_tag1=[product_list1, product_list2,
                                                                                  product_list3],
                                                                       html_tag2=[first_data1, first_data2,
                                                                                  first_data3], html_tag3=["", "", ""],
                                                                       html_tag4=["", "", ""], html_tag5=["", "", ""])
                                        own_scraper.check_tags()
                                        data = own_scraper.scraper()
                                        if len(data) == 0:
                                            self.show_popup(0, 18)
                                            print("No data extracted")
                                        else:
                                            own_scraper.data_save()
                                            DemoApp.get_running_app().stop()
                                            own_scraper_data_display.run_data2(item, guest)
                                            DemoApp().run()
                                    else:
                                        self.show_popup(0, 17)
                else:
                    self.show_popup(0, 16)
            else:
                self.show_popup(0, 14)
        else:
            self.show_popup(0, 12)



    '''
    Used to register users by checking if the current data is valid. If it is and no error message
    is shown then the data is added to the database and goes to the login screen
    '''
    def register(self):
        global guest
        global number
        flag = False
        #print(self.root.user)
        username = self.root.get_screen('Register').ids.user.text
        password1 = self.root.get_screen('Register').ids.password.text
        password2 = self.root.get_screen('Register').ids.confirmpassword.text
        user = register.register_user(username)
        # Username exists
        if user == 1:
            self.show_popup(0, 1)

        # Username should consist of 5-12 characters
        elif user == 2:
            self.show_popup(0, 28)


        # Check username string, should contain number
        elif user == 3:
            self.show_popup(0, 29)


        elif user == 4:
            self.show_popup(0, 30)

        # If username is valid
        elif len(user) > 2:
            # Check password


            pass1 = register.register_password(password1)


                    #messagebox.showerror(title="Error", message="Username should consist of 5-12 characters with letters and numbers")

            #Used to check if passwords match such as have a letter, digit, captial letter, small letter, and number
            if pass1 == 1:
                self.show_popup(0,3)

            elif pass1 == 2:
                self.show_popup(0,22)
            elif pass1 == 3:
                self.show_popup(0,23)
            elif pass1 == 4:
                self.show_popup(0,24)
            elif pass1 == 5:
                self.show_popup(0,25)
            elif pass1 == 6:
                self.show_popup(0, 26)
            try:
                # Username and password are valid
                if len(user) > 2 and len(pass1) > 2:
                    # Check if comfirm password is correct
                    if password1 == password2:
                        #show_popup(1, 11)

                        # Random generated 2FA pin
                        characters = string.ascii_letters + string.digits

                        # generate a random string of length 6
                        word = ''.join(random.choice(characters) for i in range(6)).upper()
                        number = word
                        # Add to the database by hashing all the values
                        username1, password1, word1 = hashlib.sha256(username.encode()).hexdigest(), hashlib.sha256(
                            pass1.encode()).hexdigest(), hashlib.sha256(word.encode()).hexdigest()
                        data.cur.execute("INSERT INTO userdata (username, password, word) VALUES (?,?,?)",
                                         (username1, password1, word1))
                        data.connect.commit()

                        guest = False
                        self.show_popup(1, 32)
                        self.root.current = 'Login'



                    else:
                        self.show_popup(0, 0)
                        pass

                else:
                    self.show_popup(0,5)
            except:
                pass



    # Opens instagram link on the web
    def open_instagram(self):
        webbrowser.open('https://instagram.com/bestmatchscraper?igshid=YmMyMTA2M2Y=')
    # Opens facebook link on the web
    def open_facebook(self):
        webbrowser.open('https://www.facebook.com/people/WS-Pyhon/pfbid035wTuYuFqa7m2FsaFad29joQVXYbVQAVXoB1CXuC7YmRLgMMXxcGTQHXGKJujWzmjl/')
    '''
    Used to login the user once they register or forget password
    Once the user logs on the are taken to the screen where you can pick scraping options
    It compares the user data with the data in the database if the data is the same the user will be able to login
    '''
    def login(self):
        global user
        global guest
        username = self.root.get_screen('Login').ids.user.text.strip()
        password = self.root.get_screen('Login').ids.password.text.strip()
        print(username, password)
        # Hashes the values because the users data is stored as hash values
        username_hash = hashlib.sha256(username.encode()).hexdigest()
        # First check for the username
        query_user = "SELECT username FROM userdata WHERE username = ?"
        cur1 = data.connect.cursor()
        cur1.execute(query_user, (username_hash,))
        # If username matches then check for the password using the username
        result1 = cur1.fetchone()
        if result1 is not None:
            # checks for the password using the username
            query = "SELECT password FROM userdata WHERE username = ?"
            cur2 = data.connect.cursor()
            cur2.execute(query, (username_hash,))
            result2 = cur2.fetchone()
            # Checks if the password after getting hashed is the same as the stored password
            if result2 is not None and hashlib.sha256(password.encode()).hexdigest() == result2[0]:
                print("Username and password combination is valid")
                guest = False
                user = username_hash
                print(user)
                self.root.current = 'Scraper_options'


            else:
                # data.connect.close()
                self.show_popup(0, 4)

        else:
            # The username does not exist, so we can proceed to create a new user
            self.show_popup(0,21)
            return username
    # Used to enable or disable buttons based on adding a text input
    def check_data_text(self):
        text = self.root.get_screen('ScraperData').ids.item.text.strip()
        if text:
            self.root.get_screen('ScraperData').ids.data.disabled = False
        else:
            self.root.get_screen('ScraperData').ids.data.disabled = True
    # Same as the previous function
    def check_text(self):
        text = self.root.get_screen('optionsMenu').ids.item.text.strip()
        print(text, "sksksa")
        """
        Enable/disable buttons based on whether textfield has text or not
        """
        if text:
            self.root.get_screen('optionsMenu').ids.All_websites.disabled = False
            self.root.get_screen('optionsMenu').ids.amazon.disabled = False
            self.root.get_screen('optionsMenu').ids.argos.disabled = False
            self.root.get_screen('optionsMenu').ids.ebay.disabled = False
            self.root.get_screen('optionsMenu').ids.johnlewis.disabled = False
        else:
            self.root.get_screen('optionsMenu').ids.All_websites.disabled = True
            self.root.get_screen('optionsMenu').ids.amazon.disabled = True
            self.root.get_screen('optionsMenu').ids.argos.disabled = True
            self.root.get_screen('optionsMenu').ids.ebay.disabled = True
            self.root.get_screen('optionsMenu').ids.johnlewis.disabled = True
    # Used to scrape all the websites
    def all_websites(self):

        values, text = scraper.scrape().pick_options(self.root.get_screen('optionsMenu').ids.item.text.strip(), '1', recommend_items)

        if len(values) == 0:
            self.show_popup(0,9)
        else:
            DemoApp.get_running_app().stop()
            built_in_scraper_data_display.run_data(text,guest, user)
            DemoApp().run()

    # Used for master database
    def check_database(self):
        import master_data
        import os
        text = self.root.get_screen('ScraperData').ids.item.text.strip()
        # Checks if the masterdata base has been scraped today
        if os.path.exists("masterdata.xlsx"):
            # Checks if the input matches a datas description
            if master_data.get_exact_data(text):
                    DemoApp.get_running_app().stop()
                    built_in_scraper_data_display.run_data2(text, user)
                    DemoApp().run()
            else:
                self.show_popup(0,36)
        else:
            self.show_popup(0,35)
    # Scrapes johnlewis
    def john_lewis(self):
        values, text = scraper.scrape().pick_options(self.root.get_screen('optionsMenu').ids.item.text.strip(), '2',recommend_items)
        if len(values) == 0:
            self.show_popup(0,9)
        else:
            DemoApp.get_running_app().stop()
            built_in_scraper_data_display.run_data(text,guest, user)

            DemoApp().run()

    def remove_screen(self, screen_name):
        screen = self.root.get_screen(screen_name)

        self.root.remove_widget(screen)
        self.root.run_file()
    # Scrapes argos
    def argos(self):
        values, text = scraper.scrape().pick_options(self.root.get_screen('optionsMenu').ids.item.text.strip(), '3', recommend_items)
        if len(values) == 0:
            self.show_popup(0,9)
        else:
            DemoApp.get_running_app().stop()
            built_in_scraper_data_display.run_data(text,guest, user)
            DemoApp().run()
    # Scrapes ebay
    def ebay(self):
        values, text = scraper.scrape().pick_options(self.root.get_screen('optionsMenu').ids.item.text.strip(), '4',recommend_items)
        if len(values) == 0:
            self.show_popup(0,9)
        else:
            DemoApp.get_running_app().stop()
            built_in_scraper_data_display.run_data(text,guest, user)
            DemoApp().run()
    # Scrapes amazon
    def amazon(self):
        values, text = scraper.scrape().pick_options(self.root.get_screen('optionsMenu').ids.item.text.strip(), '5',recommend_items)
        if len(values) == 0:
            self.show_popup(0,9)
        else:
            DemoApp.get_running_app().stop()
            built_in_scraper_data_display.run_data(text,guest, user)
            DemoApp().run()
    '''
    This function is used to change the password if the user forgets it
    To change password the user should have an account and the user needs to use there 2FA code which was given
    after registeration. The software checks if the data is valid by checking the hash valued inputs, if it is correct
    Then the user can change password and once the user changes it they go to the login screen
    '''
    def forgot_password(self):
        username = self.root.get_screen('Forgot').ids.user.text
        password1 = self.root.get_screen('Forgot').ids.password.text
        password2 = self.root.get_screen('Forgot').ids.confirmpassword.text
        word = self.root.get_screen('Forgot').ids.word.text

        # Hash username
        username_hash = hashlib.sha256(username.encode()).hexdigest()
        # Retrive the hased username
        query_user = "SELECT username FROM userdata WHERE username = ?"
        cur1 = data.connect.cursor()
        cur1.execute(query_user, (username_hash,))
        result1 = cur1.fetchone()
        # Checks if the username exists
        if result1 is not None:
            print("Username already exists")
            # If username exists then check if the 2FA word is valid based on username
            query2 = "SELECT word FROM userdata WHERE username = ?"
            cur2 = data.connect.cursor()
            cur2.execute(query2, (username_hash,))
            result2 = cur2.fetchone()
            # If 2FA is valid then the user can change the password
            if result2 is not None and hashlib.sha256(word.encode()).hexdigest() == result2[0]:
                print("word is valid")
                pass1 = register.register_password(password1)
                if pass1 == 1:
                    self.show_popup(0, 3)

                elif pass1 == 2:
                    self.show_popup(0, 22)
                elif pass1 == 3:
                    self.show_popup(0, 23)
                elif pass1 == 4:
                    self.show_popup(0, 24)
                elif pass1 == 5:
                    self.show_popup(0, 25)
                elif pass1 == 6:
                    self.show_popup(0, 26)
                else:
                    if password1 == password2:
                        if len(pass1) > 2:
                            # Update password by hashing it and then updates it in the database
                            password1 = hashlib.sha256(password1.encode()).hexdigest()
                            cur2.execute("UPDATE userdata SET password=? WHERE username=?", (password1, username_hash))
                            data.connect.commit()
                            self.show_popup(1,10)
                            self.root.current = 'Login'
                    else:
                            self.show_popup(0,0)


            else:

                self.show_popup(0,8)
        else:
            self.show_popup(0,7)
    # Quit button
    def quit(self):
        DemoApp.get_running_app().stop()




    # Displays all the pop ups
    def show_popup(self, index_t, index_s):
        sentences = ['Confirm password does not match', "Username exists", 'Length should be between 5 to 20', 'Password length should be 5 to 20', 'Password combination is invalid', "Secret word must have 4 or more words", "Secret word must be letters", "Username does not exist", "2FA is incorrect", "Item does not exists", "Password updated", "Accounted created", "Invalid Url", "Url cannot be the same as base url", "Invalid item url", "Item name is empty", "First html text field is missing data", "Second html text field is missing data", "Third html text field is missing data", "Fourth or Fifth text field is missing data", "No data extracted", "Username does not exist", "Password should contain at least one lowercase letter", "Password should contain at least one uppercase letter", "Password should contain at least one digit", "Password should contain at least one special character", "Password cannot contain any white spaces", "Two Factor Authentication must have a length of 4+", "Username length should be between 4 to 12", "Username should start with a letter", "Username should only contain letters and digits", "Guest users do not have access to this", f'Thank you for creating an account\nYour 2FA is: {number} \nPlease save it incase you forget password', 'Pre made websites:\nconsists of four websites:\nAmazon, Argos, Ebay and Johnlewis\nAll users have the ability to use either\nall of the websites or just one\nOnly registered users have the ability to use build your own scraper', "Exact Page\nAccess is to all the users\nUsed to extract the whole page\nExact Input\nOnly for registered users\nUsed to extract EXACT input as typed", "No data was scraped today", "Item was not scraped", "Please do not close the program\nPlease wait till the scraping process is done\nor an error message is displayed"]
        title = ["Error", "Success", "Help"]
        content = BoxLayout(orientation="vertical")
        label = Label(text=sentences[index_s])
        '''
                if title[index_t] == "Help":
            label = Label(text=sentences[index_s])
        elif title[index_t] == "Success":
            label = Label(text=sentences[index_s])
        elif title[index_t] == "Error":
            label = Label(text=sentences[index_s], color=(1, 0, 0, 1))
        '''

        ok_button = MDRaisedButton(text="OK", size_hint=(None, None), size=(100, 50),
                                   md_bg_color=(0, 0.349, 0.686, 1), text_color=(1, 1, 1, 1))
        #ok_button.background_color = (1, 0, 0, 1)
        content.add_widget(label)
        content.add_widget(ok_button)
        '''
        Looks to ugly
                if title[index_t] == 'Error':
            popup = Popup(title=title[index_t], content=content, size_hint=(None, None), size=(400, 400), background_color=(1, 0, 0, 1))
        elif title[index_t] == "Help":
            popup = Popup(title=title[index_t], content=content, size_hint=(None, None), size=(500, 500),
                          background_color=(0.6, 0.6, 0, 1))
        elif title[index_t] == "Success":
            popup = Popup(title=title[index_t], content=content, size_hint=(None, None), size=(400, 400),
                          background_color=(0, 0.6, 0, 1))
        '''
        if title[index_t] == "Help":
            popup = Popup(title=title[index_t], content=content, size_hint=(None, None), size=(500, 500))
        else:
            popup = Popup(title=title[index_t], content=content, size_hint=(None, None), size=(400, 400))

        ok_button.bind(on_press=popup.dismiss)  # bind button press to dismiss popup
        popup.open()
    #Shows a pop up with a video link
    def show_popup_video(self):
        content = BoxLayout(orientation="vertical")
        label = Label(text="Base Url: Just the website link\nItem Url: URL after typing product name\nItem name: Name of product\nHTML Product list:The html code of the product\nThe rest should contain data which you want to scrape")
        youtube_button = MDRaisedButton(text="Watch on YouTube", size_hint=(None, None), size=(200, 50),
                                        md_bg_color=(1, 0, 0, 1), text_color=(1, 1, 1, 1))
        youtube_button.bind(on_press=self.play_video)

        ok_button = MDRaisedButton(text="OK", size_hint=(None, None), size=(100, 50),
                                   md_bg_color=(0, 0.349, 0.686, 1), text_color=(1, 1, 1, 1))


        content.add_widget(label)
        content.add_widget(youtube_button)
        content.add_widget(ok_button)

        popup = Popup(title="Help", content=content, size_hint=(None, None), size=(500, 500))
        ok_button.bind(on_press=popup.dismiss)
        popup.open()
    # Plays the video to help understand own scraper
    def play_video(self, instance):
        webbrowser.open('https://www.youtube.com/watch?v=EG0Zp8dQbWI')

    def check_cart(self):
        if guest == True:
            self.show_popup(0,31)
        else:
            DemoApp.get_running_app().stop()
            built_in_scraper_data_display.run_data3("cart", user)

            DemoApp().run()

    # Adding a sound did not seem to fit
    #def sounds(self):

        #release_sound = SoundLoader.load('release_sound.wav')
        #print(release_sound)
        # play the release sound
        #if release_sound:
            #release_sound.play()


weekday_checker.day()
DemoApp().run()