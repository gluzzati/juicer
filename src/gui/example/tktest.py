import os
from xml.etree.ElementTree import XML

from core import log

os.environ["DISPLAY"] = ":0"
import tkinter as Tkinter


def realize(master, element):
	if element.tag == "form":
		frame = Tkinter.Frame(master, **element.attrib)
		for subelement in element:
			widget = realize(frame, subelement)
			widget.pack()
		return frame
	else:
		options = element.attrib
		if element:
			options = options.copy()
			for subelement in element:
				options[subelement.tag] = subelement.text
		widget_factory = getattr(Tkinter, element.tag.capitalize())
		return widget_factory(master, **options)


def print_test():
	log.yay("test!!")


class FullScreenApp(object):
	def __init__(self, master, **kwargs):
		self.master = master
		master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth(), root.winfo_screenheight()))
		master.overrideredirect(True)
		root.resizable(width=False, height=False)
		self.frame = realize(root, kwargs["xml"])
		self.print_test = print_test
		self.frame.pack()


form = XML("""\
<form>
    <label><text>entry:</text></label>
    <entry width='30' bg='gold' />
    <checkbutton><text>checkbutton</text></checkbutton>
    <button text='OK' relief='flat'  activebackground='gold' command='print_test' highlightthickness='0' borderwidth='0' />
    <button text='Cancel' />
</form>
""")

root = Tkinter.Tk()
try:
	app = FullScreenApp(root, xml=form)
	root.mainloop()
except KeyboardInterrupt:
	root.destroy()
