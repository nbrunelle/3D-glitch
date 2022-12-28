#coding:utf-8

from kivy.app import App
from kivy.properties import ObjectProperty
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import numpy as np
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window

input_t = []
i = 0
t_n = []
i_ind = 0
text = "Default text"
file = "monkey.obj"
lvl = 0.5

class Menu(Widget):
    import_btn = ObjectProperty(None)
    glitch_text = ObjectProperty(None)
    f_src = ObjectProperty(None)
    renderer = ObjectProperty(None)
    g_lvl = ObjectProperty(None)
    pass

    def lvl(self, value):
        global lvl
        lvl = value

    def load(file):

        pass

    def import_file(self):
        root = tk.Tk()
        root.withdraw()
        FILEOPENOPTIONS = dict(defaultextension='.obj',
                  filetypes=[('OBJ files','*.obj')])
        file_path = filedialog.askopenfilename(**FILEOPENOPTIONS)
        print(file_path)
        self.f_src.text = Path(file_path).name
        global file
        file = os.path.relpath(file_path)
        pass


class GlitchGUI(Widget):
    pass

class GlitchApp(App):
    def build(self):
        return GlitchGUI()

    def getText(instance, value):
        global text
        text = value.text
        pass

    def corrupt(instance):
        input_t = []
        global file
        global text
        i_l = i = 0
        t_n = v_amp = []
        vn_nbr = v_nbr = 0

        # max range ASCII is 255, so here it'll be at max 1
        for c in text:
            input_t.append(ord(c) / 255)

        # Global clock iteraton of input_t
        def ind():
            global i_ind
            if i_ind + 1 == len(input_t) - 1:
                i_ind = 0
            else:
                i_ind += 1
            return input_t[i_ind]

        f = open(file)
        vect = []
        vect_n = []
        faces = []
        faces_index = []
        head = []
        old_faces = []
        for i, ln in enumerate(f):
            # Blank is for distinction between v and vn
            if ln.startswith("v "):
                vect.extend([float(i) for i in ln[2:-2].split(" ")])
            elif ln.startswith("vn"):
                vect_n.extend([float(i) for i in ln[3:-2].split(" ")])
            elif ln.startswith("f"):
                old_faces.append(ln)
                faces_split = ln[2:-1].split(" ")
                faces_vect = len(faces_split)
                faces_index.append(faces_vect)
                for i in ln[2:-1].split(" "):
                    faces.extend(i.split("/"))
            else:
                head.append([ln, i])
        f.close()
        # Don't forget to scale it back to original, save the factor
        factor = np.max(vect)
        step_new_vect = int(len(vect) / (np.ceil((len(vect) * lvl))))
        step_new = int(len(faces) / (np.ceil((len(faces) * lvl))))

        vect = np.divide(vect, factor)

        def digit_sum(num):
            s = 0
            for d in list(str(num)):
                try:
                    s += int(d)
                except ValueError:
                    pass
            if s % 2:
                return True
            else:
                return False

        def corrupt(data):
            n_d = []
            for i, d in enumerate(data):
                if digit_sum(d):

                    n_d.extend([round(d * ind() * factor, 3)])

                else:
                    n_d.extend([round(d / ind() * factor, 3)])
                if i % step_new_vect:
                    # find solution for new data
                    for d_ in list(str(d)):
                        try:
                            n_d.extend([round(int(d_) ** int(d_) / ind() * factor, 3)])
                        except ValueError:
                            pass
            return n_d

        # Corruption of vect, vect_n and AFTER, faces
        n_vect = corrupt(vect)
        n_vect_n = corrupt(vect_n)

        new_faces = []
        print(len(faces_index))
        i_index_faces = 0
        new_ln = ""
        for i, f in enumerate(n_vect):
            if i % 3 == 0:
                new_ln += "\nv "
            new_ln += str(f) + " "

        for i, f in enumerate(n_vect_n):
            if i % 3 == 0:
                new_ln += "\nvn "
            new_ln += str(f) + " "

        new_ln += "\n"
        for i, f in enumerate(old_faces):
            new_ln += old_faces[i]

        print(new_ln)
        new_filename = os.path.splitext(file)[0] + "_glitched.obj"
        print(new_filename)
        file = open(new_filename, "w")

        file.write(new_ln)
        file.close()
        pass


if __name__ == '__main__':
    GlitchApp().run()
