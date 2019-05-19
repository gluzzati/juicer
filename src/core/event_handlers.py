from core import log
from core.context import Context
from core.events import Event


def rfid_detected_handler(ctx, evt):
	log.debug("rfid detected handler: " + str(evt.rfid))
	next_state = ctx.state

	if ctx.state != Context.State.IDLE:
		log.error("machine not ready! " + ctx.state)
		return False, next_state

	next_state = Context.State.GLASS_ON

	known, user = ctx.database.lookup_rfid(evt.rfid)
	if known:
		ctx.user = user
		current_water = ctx.scale.get_weight() - user.glass.weight
		missing_water = user.glass.capacity - current_water
		ctx.gui.update(
			"hello, {}! your glass holds {}ml, do you want to fill up with {}ml?".format(
				user.name, user.glass.capacity, missing_water))

		# todo delete this
		evt = Event(Event.POUR_REQUESTED)
		ctx.queue.put(evt)
	else:
		ctx.gui.update("Hi stranger! want to register?")

	return True, next_state


def rfid_removed_handler(ctx, evt):
	log.debug("rfid removed handler")
	next_state = ctx.state
	if ctx.state in (Context.State.GLASS_ON, Context.State.POURING):
		if ctx.state == Context.State.POURING:
			ctx.relay.water_off()  # emergency wateroff, bypasses normal procedure
		next_state = Context.State.IDLE
	else:
		log.debug("removed rfid, but there was no glass, mumble mumble... " + ctx.state)

	return True, next_state


def auto_wateroff_handler(ctx, evt):
	next_state = ctx.state
	if ctx.state == Context.State.POURING:
		next_state = Context.State.GLASS_ON
	else:
		log.debug("nothing to stop, not pouring, mumble mumble")
	return True, next_state


def registration_requested_handler(ctx, evt):
	user = evt.user
	exists, _ = ctx.database.lookup_rfid(user.tag)
	if exists:
		log.warn("user \"{}\" already exists in db - updating records".format(user.name))
	ctx.database.add(user)
	return True, ctx.state


def pour_requested_handler(ctx, evt):
	if ctx.state is Context.State.GLASS_ON:
		return True, Context.State.POURING
	else:
		log.info("POUR button press ignored")
		return True, ctx.state
