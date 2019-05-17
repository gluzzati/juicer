from core import log
from core.water_machine import WaterMachine


class Event:
	SIGINT = "SIGINT"
	JSON = "JSON"
	RFID_DETECTED = "RFID_DETECTED"
	RFID_REMOVED = "RFID_REMOVED"
	INVALID = "INVALID"

	def __init__(self):
		self.data = None
		self.type = Event.INVALID


class Handlers:
	@staticmethod
	def unknown_event(ctx, evt):
		log.error("unknown evt \"" + evt.type + "\"")
		return False, None

	@staticmethod
	def rfid_detected(ctx, evt):
		log.debug("rfid detected: " + str(evt.rfid))

		if ctx.state_machine.state != WaterMachine.State.IDLE:
			log.error("machine not ready! " + ctx.state_machine.state)
			return False, None

		ctx.set_state(WaterMachine.State.GLASS_ON)
		known, user = ctx.database.lookup_rfid(evt.rfid)
		if known:
			current_water = ctx.scale.get_weight() - user.glass_weight
			missing_water = user.glass_capacity - current_water
			ctx.gui.update(
				"hello, " + user.name + "! your glass holds " + user.glass_capacity + ", do you want to fill up (" + missing_water + "?")
		else:
			ctx.gui.update("Hi stranger! want to register?")

		return True, None

	@staticmethod
	def rfid_removed(ctx, evt):
		if ctx.get_state() == WaterMachine.State.IDLE:
			log.debug("removed rfid, but state was IDLE already, mumble mumble...")
		else:
			ctx.stop_pouring()
			ctx.set_state(WaterMachine.State.IDLE)
		return True, None

	@staticmethod
	def fill_request(ctx, evt):
		if ctx.get_state() == WaterMachine.State.GLASS_ON:
			ctx.set_state(WaterMachine.State.POURING)
			ctx.start_pouring()
		else:
			log.debug("can't fill, there's no glass")
		return True, None

	@staticmethod
	def stop_request(ctx, evt):
		if ctx.get_state() == WaterMachine.State.POURING:
			ctx.stop_pouring()
			ctx.set_state(WaterMachine.State.GLASS_ON)
		else:
			log.debug("nothing to stop, not pouring")
		return True, None
