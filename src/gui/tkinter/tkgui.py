from gui.tkinter import gengui


def fullscreen(root):
    root.overrideredirect(True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))


class Fakeclass:
    @staticmethod
    def print_test(cb, event=None):
        print("test!")


if __name__ == '__main__':
    pad = 3
    root = gengui.TkYaml('gui.yml', title='Some test gui...')
    fullscreen(root)


    def ok(event=None):
        print(v.get())
        print(c.get())
        root.destroy()


    def print_test2(event=None):
        print("test2!")


    # config vars for checkboxes etc.
    c = root.checkbox('check')
    v = root.entry('entry', key='<Return>', cmd=ok, focus=True)

    # add button behaviour
    root.button('ok', ok)
    root.button('cancel', root.destroy)
    root.checkbox('check', Fakeclass.print_test)
    root.mainloop()
