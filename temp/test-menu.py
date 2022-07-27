#!/usr/bin/env python3

import curses
from curses import panel

class Menu(object):
    def __init__(self, title_text, expl_text, menu_items, stdscreen):
        self.title_text = title_text
        self.title_window = stdscreen.subwin(0, 20)

        self.expl_text = expl_text
        self.expl_window = stdscreen.subwin(2, 1)


        self.menu_window = stdscreen.subwin(4, 2)
        self.menu_window.keypad(1)
        self.menu_panel = panel.new_panel(self.menu_window)
        self.position = 0

        self.menu_items = menu_items
        self.menu_panel.hide()
        panel.update_panels()

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = len(self.menu_items) - 1
        elif self.position >= len(self.menu_items):
            self.position = 0

    def display(self):
        self.title_window.addstr(self.title_text)
        self.title_window.refresh()

        self.expl_window.addstr(self.expl_text)
        self.expl_window.refresh()

        self.menu_panel.top()
        self.menu_panel.show()

        while True:
            start = 0
            self.menu_window.clear()

            while start + (curses.LINES - 1) < self.position:
                start += curses.LINES
            myrow = self.position - start
            mycol = 0
            for index, item in enumerate(self.menu_items[start:start + curses.LINES - 1], start=start):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                msg = f"{item[0]}"
                self.menu_window.addstr(index - start, 0, msg, mode)
                if index == self.position:
                    (myrow, mycol) = self.menu_window.getyx()

            self.menu_window.move(myrow, mycol)
            key = self.menu_window.getch()

            if key in [curses.KEY_ENTER, ord("\n")]:
                self.menu_items[self.position][1]()

            elif key == curses.KEY_F10:
                break

            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)


class Form(object):
    def __init__(self, title_text, expl_text, form_items, stdscreen):
        self.stdscreen = stdscreen
        self.title_text = title_text
        self.title_window = stdscreen.subwin(0, 20)

        self.expl_text = expl_text
        self.expl_window = stdscreen.subwin(2, 1)


        self.form_window = stdscreen.subwin(4, 2)
        self.form_window.keypad(1)
        self.form_panel = panel.new_panel(self.form_window)
        self.position = 0

        self.form_items = form_items
        self.form_panel.hide()
        panel.update_panels()

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = len(self.form_items) - 1
        elif self.position >= len(self.form_items):
            self.position = 0

    def display(self):
        self.title_window.addstr(self.title_text)
        self.title_window.refresh()

        self.expl_window.addstr(self.expl_text)
        self.expl_window.refresh()

        self.form_panel.top()
        self.form_panel.show()

        while True:
            start = 0
            self.form_window.clear()

            while start + (curses.LINES - 1) < self.position:
                start += curses.LINES
            myrow = self.position - start
            mycol = 0
            for index, item in enumerate(self.form_items[start:start + curses.LINES - 1], start=start):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                msg = f"{item}\t[]"
                self.form_window.addstr(index - start, 0, msg, mode)
                if index == self.position:
                    (myrow, mycol) = self.form_window.getyx()

            self.form_window.move(myrow, mycol)
            key = self.form_window.getch()

            if key in [curses.KEY_ENTER, ord("\n")]:
                self.form_items[self.position][1]()

            elif key == curses.KEY_F10:
                self.stdscreen.clear()
                break

            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

class MyApp(object):
    def __init__(self, stdscreen):
        self.screen = stdscreen
        curses.curs_set(0)


        form_title_text = "Test form"
        form_expl_text = "Type or select values in entry fields.\nPress enter AFTER making all desired changes"
        form_items = [
            ("Lorem ipsum"),
            ("Lorem ipsum"),
            ("Lorem ipsum"),
        ]

        form = Form(form_title_text, form_expl_text, form_items, self.screen)

        # First submenu
        submenu_title_text = "Submenu"
        submenu_expl_text = "Move cursor and press Enter. Press F10 to exit"
        submenu_items = [
            ("beep", curses.beep),
            ("flash", curses.flash),
            ("form", form.display),
        ]
        submenu = Menu(submenu_title_text, submenu_expl_text, submenu_items, self.screen)

        # Main menu
        main_menu_title_text = "Main"
        main_menu_expl_text = "Move cursor and press Enter. Press something to exit"
        main_menu_items = [
            ("beep", curses.beep),
            ("flash", curses.flash),
            ("submenu", submenu.display),
        ]
        main_menu = Menu(main_menu_title_text, main_menu_expl_text, main_menu_items, self.screen)
        main_menu.display()

        #expl_items = ["F1: Help", "F3: Refresh", "F10: Exit"]

        panel.update_panels()
        curses.doupdate()

if __name__ == "__main__":
    curses.wrapper(MyApp)
