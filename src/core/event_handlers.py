from core import log
from core.context import Context


def unknown_event_handler(ctx, evt):
	log.error("unknown evt \"" + evt.type + "\"")
	return False, None


def rfid_detected_handler(ctx, evt):
	log.debug("rfid detected handler: " + str(evt.rfid))

	if ctx.state != Context.State.IDLE:
		log.error("machine not ready! " + ctx.state)
		return False, None

	ctx.set_state(Context.State.GLASS_ON)
	known, user = ctx.database.lookup_rfid(evt.rfid)
	if known:
		current_water = ctx.scale.get_weight() - user.glass_weight
		missing_water = user.glass_capacity - current_water
		ctx.gui.update(
			"hello, " + user.name + "! your glass holds " + user.glass_capacity + ", do you want to fill up (" + missing_water + "?")
	else:
		ctx.gui.update("Hi stranger! want to register?")

	return True, None


def rfid_removed_handler(ctx, evt):
	log.debug("rfid removed handler")
	if ctx.get_state() is Context.State.GLASS_ON:
		ctx.stop_pouring()
		ctx.set_state(Context.State.IDLE)
	else:
		log.debug("removed rfid, but there was no glass, mumble mumble...")

	return True, None


def fill_request_handler(ctx, evt):
	if ctx.get_state() == Context.State.GLASS_ON:
		ctx.set_state(Context.State.POURING)
		ctx.start_pouring()
	else:
		log.debug("can't fill, there's no glass")
	return True, None


def stop_request_handler(ctx, evt):
	if ctx.get_state() == Context.State.POURING:
		ctx.stop_pouring()
		ctx.set_state(Context.State.GLASS_ON)
	else:
		log.debug("nothing to stop, not pouring")
	return True, None
