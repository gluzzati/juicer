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
		ctx.user = user
		current_water = ctx.scale.get_weight() - user.glass.weight
		missing_water = user.glass.capacity - current_water
		ctx.gui.update(
			"hello, {}! your glass holds {}ml, do you want to fill up with {}ml?".format(
				user.name, user.glass.capacity, missing_water))
		ctx.start_pouring()
	else:
		ctx.gui.update("Hi stranger! want to register?")

	return True, None


def rfid_removed_handler(ctx, evt):
	log.debug("rfid removed handler")
	if ctx.get_state() in (Context.State.GLASS_ON, Context.State.POURING):
		if ctx.get_state() == Context.State.POURING:
			ctx.stop_pouring()
		ctx.set_state(Context.State.IDLE)
	else:
		log.debug("removed rfid, but there was no glass, mumble mumble...")

	return True, None


def auto_wateroff_handler(ctx, evt):
	if ctx.get_state() == Context.State.POURING:
		ctx.set_state(Context.State.GLASS_ON)
	else:
		log.debug("nothing to stop, not pouring, mumble mumble")
	return True, None


def registration_requested_handler(ctx, evt):
	user = evt.user
	exists, _ = ctx.database.lookup_rfid(user.tag)
	if exists:
		log.warn("user \"{}\" already exists in db - updating records".format(user.name))
	ctx.database.add(user)
	return True, None