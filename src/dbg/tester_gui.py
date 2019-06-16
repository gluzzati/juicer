from core.events import create_event, EventType, EventKey
from dbg import gengui


def fullscreen(root):
    root.overrideredirect(True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))


class TesterGui:
    def __init__(self, ctx):
        self.ctx = ctx
        self.root = gengui.TkYaml('dbg/gui.yml', title='Juicer Tester')
        root = self.root
        self.glasson = False
        root.button('exit', self.sigint)
        root.button('disp_ef_st', self.dispense_efst)
        root.button('disp_ef_sp', self.dispense_efsp)
        root.button('disp_rb_st', self.dispense_rbst)
        root.button('disp_rb_sp', self.dispense_rbsp)
        root.button('disp_w_st', self.dispense_wst)
        root.button('disp_w_sp', self.dispense_wsp)
        root.button('glasson', self.toggle_glass)

        fullscreen(self.root)

    def main(self):
        self.root.mainloop()

    def destroy(self):
        self.root.destroy()

    def toggle_glass(self):
        if not self.glasson:
            tag = 323984762367
            evt = create_event(EventType.RFID_DETECTED)
            evt[EventKey.rfid] = tag
            self.ctx.queue.put(evt)
            self.glasson = True
        else:
            evt = create_event(EventType.RFID_REMOVED)
            self.ctx.queue.put(evt)
            self.glasson = False

    def sigint(self):
        evt = create_event(EventType.SIGINT)
        self.ctx.queue.put(evt)
        self.destroy()

    def dispense_efst(self):
        self.trigger_recipe("elderflower_still")

    def dispense_efsp(self):
        self.trigger_recipe("elderflower_sparkling")

    def dispense_rbst(self):
        self.trigger_recipe("raspberry_still")

    def dispense_rbsp(self):
        self.trigger_recipe("raspberry_sparkling")

    def dispense_wst(self):
        self.trigger_recipe("water_still")

    def dispense_wsp(self):
        self.trigger_recipe("water_sparkling")

    def trigger_recipe(self, recipe):
        evt = create_event(EventType.POUR_REQUESTED)
        evt[EventKey.requested_recipe] = recipe
        self.ctx.queue.put(evt)
