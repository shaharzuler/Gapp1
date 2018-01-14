from kivy.app import App
#kivy.require("1.8.0")
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
import xlrd
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
import pdb


class MainScreen(Screen):
    pass    
        
    

class AnotherScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.d={}
        self.my_pos_y = 0.95
        self.my_pos_x = 0.15

        workbook = xlrd.open_workbook( 'my_file_name.xls')
        sheet = workbook.sheet_by_index(0)
        num_rows = sheet.nrows - 1
        self.num_rows=num_rows
        self.word_list = ('The quick brown fox jumps over the lazy old dog').split(' ')

        
        
        
    def create_recipe(self):
        workbook = xlrd.open_workbook( 'my_file_name.xls')
        sheet = workbook.sheet_by_index(0)
        num_rows = sheet.nrows - 1

        for xl_row in range(num_rows):
            #adding new num label:
            l_num = Label()
            l_num.text=str(int(sheet.cell(xl_row+1, 0).value))
            l_num.pos_hint = {"x":self.my_pos_x, "top":self.my_pos_y}
            l_num.font_size = 30
            l_num.size_hint = (0.06, 0.1)
            self.add_widget(l_num)
            #adding new unit label:
            l_unit = Label()
            l_unit.text=sheet.cell(xl_row+1, 1).value
            l_unit.pos_hint = {"x":self.my_pos_x + 0.1, 'top':  self.my_pos_y}
            l_unit.font_size = 30
            l_unit.size_hint = (0.2, 0.1)
            self.add_widget(l_unit)
            #adding new ingredient:
            l_ing = Label()
            l_ing.text=sheet.cell(xl_row+1, 2).value
            l_ing.pos_hint = {"x":self.my_pos_x + 0.2, 'top':  self.my_pos_y}
            l_ing.font_size = 30
            l_ing.size_hint = (0.2, 0.1)
            #start updating dict:
            self.d[l_ing.text]={}
            self.d[l_ing.text]['l_num_obj']= l_num
            self.d[l_ing.text]['l_ing_obj']= l_ing
            self.d[l_ing.text]['l_unit_obj']= l_unit
            self.d[l_ing.text]['l_num']= l_num.text
            self.d[l_ing.text]['l_ing']= l_ing.text
            self.d[l_ing.text]['l_unit']= l_unit.text
            self.add_widget(l_ing)
            #adding new (+) button:
            p = Button()
            p.text='+'
            p.color=(0,1,1,1)
            p.pos_hint = {"right":0.85, "top": self.my_pos_y}
            p.font_size = 25
            p.size_hint = (0.08,0.09)
            p.bind(on_press = self.label_change_dynamic )
            self.d[l_ing.text]['plus_button']= p
            self.add_widget(p)  ############
            #adding new (-) button:
            m = Button()
            m.text='-'
            m.color=(0,1,1,1)
            m.pos_hint = {"right":0.75, "top": self.my_pos_y}
            m.font_size = 25
            m.size_hint = (0.08,0.09)
            m.bind(on_press = self.label_change_dynamic )
            self.d[l_ing.text]['minus_button']= m
            self.add_widget(m)  
            self.my_pos_y -= 0.07

        
    def label_change(self, event, label0):
        self.event = event
        if self.event == "plus":
            self.ids[label0].text  = str(int(self.ids[label0].text) +1 )
        if self.event == "minus":
            self.ids[label0].text  = str(int(self.ids[label0].text) -1 )

    def label_change_dynamic(self, instance):
        for ingredient in self.d.keys():
            if instance in self.d[ingredient].values():
                if instance.text == "+":
                    self.d[ingredient]['l_num_obj'].text = str(int(self.d[ingredient]['l_num_obj'].text)+1)
                if instance.text == "-":
                    if int(self.d[ingredient]['l_num_obj'].text)>0:
                        self.d[ingredient]['l_num_obj'].text = str(int(self.d[ingredient]['l_num_obj'].text)-1)
                self.d[ingredient]['l_num'] = self.d[ingredient]['l_num_obj'].text

    
    def on_text(self, root, value):#, instance, value):
        
        """ Include all current text from textinput into the word list to
        emulate the same kind of behavior as sublime text has.
        """
        print(type(root))
        root.suggestion_text = 'aaaaa'
        #root.suggestion_text = ''
        #word_list = list(set(
         #   self.word_list + value[:value.rfind(' ')].split(' ')))
        #val = value[value.rfind(' ') + 1:]
        #if not val:
         #   return
        #try:
            # grossly inefficient just for demo purposes
         #   word = [word for word in word_list
          #          if word.startswith(val)][0][len(val):]
           # if not word:
            #    return
            #self.root.suggestion_text = word
        #except IndexError:
         #   print 'Index Error.'
        


    def add_row(self, new_num, new_unit ,new_ing):
        if (len(new_num)<1 or len(new_unit)<1 or len(new_ing)<1 ):
            return
        #adding new num label:
        l_num = Label()
        l_num.text=str(new_num)
        l_num.color=(1,1,0,1)
        l_num.pos_hint = {"x":self.my_pos_x, 'top':  self.my_pos_y}
        l_num.font_size = 30
        l_num.size_hint = (0.06, 0.07)
        self.ids['layout_content3'].add_widget(l_num)
        #adding new unit label:
        l_unit = Label()
        l_unit.text=str(new_unit) 
        l_unit.color=(1,1,0,1)
        l_unit.pos_hint = {"x":self.my_pos_x+0.1, 'top':  self.my_pos_y}
        l_unit.font_size = 30
        l_unit.size_hint = (0.2, 0.07)
        self.ids['layout_content3'].add_widget(l_unit)
        #adding new ingredient label:
        l_ing = Label()
        l_ing.text=str(new_ing)
        l_ing.color=(1,1,0,1)
        l_ing.pos_hint = {"x":self.my_pos_x + 0.2, 'top':  self.my_pos_y}
        l_ing.font_size = 30
        l_ing.size_hint = (0.2, 0.07)
        #start updating dict:
        self.d[l_ing.text]={}
        self.d[l_ing.text]['l_num_obj']= l_num
        self.d[l_ing.text]['l_ing_obj']= l_ing
        self.d[l_ing.text]['l_unit_obj']= l_unit
        self.d[l_ing.text]['l_num']= l_num.text
        self.d[l_ing.text]['l_ing']= l_ing.text
        self.d[l_ing.text]['l_unit']= l_unit.text
        self.ids['layout_content3'].add_widget(l_ing)
        #adding new (+) button:
        p = Button()
        p.text='+'
        p.color=(0,1,1,1)
        p.pos_hint = {"right":0.85, "top": self.my_pos_y}
        p.font_size = 25
        p.size_hint = (0.08,0.07)
        p.bind(on_press = self.label_change_dynamic )
        self.d[l_ing.text]['plus_button']= p
        self.ids['layout_content3'].add_widget(p)   ###      
        #adding new (-) button:
        m = Button()
        m.text='-'
        m.color=(0,1,1,1)
        m.pos_hint = {"right":0.75, "top": self.my_pos_y}
        m.font_size = 25
        m.size_hint = (0.08,0.07)
        m.bind(on_press = self.label_change_dynamic )
        self.d[l_ing.text]['minus_button']= m
        self.ids['layout_content3'].add_widget(m)  
        #updating y_pos:
        self.my_pos_y -= 0.07
        #moving input fields and cleaning text:
        self.ids['new_num'].pos_hint = { 'top':  self.my_pos_y}
        self.ids['new_unit'].pos_hint = { 'top':  self.my_pos_y}
        self.ids['new_ing'].pos_hint = { 'top':  self.my_pos_y}
        self.ids['new_num'].text = ''
        self.ids['new_unit'].text = ''
        self.ids['new_ing'].text = ''
        print('')
        print(self.ids['layout_content3'].parent)
        #moving add botton:
        self.ids['add_button'].pos_hint = {'top':  self.my_pos_y}
        

    def cook(self): ##TODO REFRESH POPUP WINDOW
        for ingredient in self.d:
            self.d[ingredient]['l_num_obj'].color=(1,1,1,1)
            self.d[ingredient]['l_unit_obj'].color=(1,1,1,1)
            self.d[ingredient]['l_ing_obj'].color=(1,1,1,1)
            self.d[ingredient]['plus_button'].disabled = True
            self.d[ingredient]['minus_button'].disabled = True
            self.ids['add_button'].disabled = True
            self.ids['new_num'].disabled = True
            self.ids['new_unit'].disabled = True
            self.ids['new_ing'].disabled = True
        self.parent.current = 'Cooking'
        for key in self.d.keys():
            print(key)
            print(self.d[key]['l_num']+ ' ' +self.d[key]['l_unit']+ ' ' +self.d[key]['l_ing'])

class WaitScreen(Screen): 
    pass


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        ScreenManager.__init__(self, **kwargs)
        self.containement={}
        for container in xrange(6):
            self.containement['container_'+str(container+1)] = 0
        print (self.containement) #

class MyPopup_main(Popup):
    def charge_fun(self, button_obj):
        button_obj.disabled = True
        container=str(button_obj.text)[-1]
        presentation.containement['container_'+str(container)]=1
        print(presentation.containement) #

    def use_fun(self, button_obj):
        button_obj.disabled = True
        container=str(button_obj.text)[-1]
        presentation.containement['container_'+str(container)]=1
        print(presentation.containement) #

class MyPopup_qin(Popup): ##TODO MAKE SURE BUTTON STAYES DISABLED
    def charge_fun(self, button_obj):
        button_obj.disabled = True
        container=str(button_obj.text)[-1]
        presentation.containement['container_'+str(container)]=1
        print(presentation.containement) #

    def use_fun(self, button_obj):
        button_obj.disabled = True
        container=str(button_obj.text)[-1]
        presentation.containement['container_'+str(container)]=1
        print(presentation.containement) #

presentation = Builder.load_file("ginieApp11.kv")
presentation.softmode= 'pan'
#pdb.set_trace()


def create_recipe():
        workbook = xlrd.open_workbook( 'my_file_name.xls')
        sheet = workbook.sheet_by_index(0)
        num_rows = sheet.nrows - 1

        for xl_row in range(num_rows):
            #adding new num label:
            l_num = Label()
            l_num.text=str(int(sheet.cell(xl_row+1, 0).value))
            l_num.pos_hint = {"x":presentation.screens[1].my_pos_x, "top":presentation.screens[1].my_pos_y}
            l_num.font_size = 30
            l_num.size_hint = (0.06, 0.07)
            presentation.screens[1].children[0].children[-1].children[0].add_widget(l_num)
            #adding new unit label:
            l_unit = Label()
            l_unit.text=sheet.cell(xl_row+1, 1).value
            l_unit.pos_hint = {"x":presentation.screens[1].my_pos_x + 0.1, 'top':  presentation.screens[1].my_pos_y}
            l_unit.font_size = 30
            l_unit.size_hint = (0.2, 0.07)
            presentation.screens[1].children[0].children[-1].children[0].add_widget(l_unit)
            #adding new ingredient:
            l_ing = Label()
            l_ing.text=sheet.cell(xl_row+1, 2).value
            l_ing.pos_hint = {"x":presentation.screens[1].my_pos_x + 0.3, 'top':  presentation.screens[1].my_pos_y}
            l_ing.font_size = 30
            l_ing.size_hint = (0.2, 0.07)
            #start updating dict:
            presentation.screens[1].d[l_ing.text]={}
            presentation.screens[1].d[l_ing.text]['l_num_obj']= l_num
            presentation.screens[1].d[l_ing.text]['l_ing_obj']= l_ing
            presentation.screens[1].d[l_ing.text]['l_unit_obj']= l_unit
            presentation.screens[1].d[l_ing.text]['l_num']= l_num.text
            presentation.screens[1].d[l_ing.text]['l_ing']= l_ing.text
            presentation.screens[1].d[l_ing.text]['l_unit']= l_unit.text
            presentation.screens[1].children[0].children[-1].children[0].add_widget(l_ing)
            #adding new (+) button:
            p = Button()
            p.text='+'
            p.color=(0,1,1,1)
            p.pos_hint = {"right":0.85, "top": presentation.screens[1].my_pos_y}
            p.font_size = 25
            p.size_hint = (0.08,0.07)
            p.bind(on_press = presentation.screens[1].label_change_dynamic )
            presentation.screens[1].d[l_ing.text]['plus_button']= p
            presentation.screens[1].children[0].children[-1].children[0].add_widget(p)
            #adding new (-) button:
            m = Button()
            m.text='-'
            m.color=(0,1,1,1)
            m.pos_hint = {"right":0.75, "top": presentation.screens[1].my_pos_y}
            m.font_size = 25
            m.size_hint = (0.08,0.07)
            m.bind(on_press = presentation.screens[1].label_change_dynamic )
            presentation.screens[1].d[l_ing.text]['minus_button']= m
            presentation.screens[1].children[0].children[-1].children[0].add_widget(m)
            presentation.screens[1].my_pos_y -= 0.07
        print(presentation.screens[1].d.keys())
create_recipe()


class MainApp(App):

    def build(self):

        return presentation
    


if __name__ == "__main__":

    #pdb.set_trace()
    Window.softinput_mode = 'pan'
    MainApp().run()
        
    
