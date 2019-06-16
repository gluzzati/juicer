from core import log
from core.context import Context
from core.events import EventKey
from core.recipe import Recipe
from core.user import User, Glass


def rfid_detected_handler(ctx, evt):
    ctx.onscale = ctx.scale.get_weight()
    log.debug("rfid detected handler: " + str(evt[EventKey.rfid]))
    next_state = ctx.state

    if ctx.state != Context.State.IDLE:
        log.error("machine not ready! " + ctx.state)
        return False, next_state

    next_state = Context.State.GLASS_ON

    known, user = ctx.database.lookup_rfid(evt[EventKey.rfid])
    if known:
        ctx.user = user
        current_water = ctx.onscale - user.glass.weight
        missing_water = user.glass.capacity - current_water
        log.yay(
            "hello, {}! your glass holds {}ml, do you want to fill up with {}ml?".format(
                user.name, user.glass.capacity, missing_water))
    else:
        log.yay("Hi stranger! want to register?")

    return True, next_state


def rfid_removed_handler(ctx, evt):
    log.debug("rfid removed handler")
    next_state = ctx.state
    if ctx.state in (Context.State.GLASS_ON, Context.State.POURING):
        if ctx.state == Context.State.POURING:
            ctx.relay_board.shut_all()  # emergency wateroff, bypasses normal procedure
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


def new_user_handler(ctx, evt):
    userdict = evt[EventKey.user]
    user = User()
    user.name = userdict[User.Key.name]
    user.glass = Glass()
    user.glass.weight = userdict[User.Key.glass][Glass.Key.weight]
    user.glass.capacity = userdict[User.Key.glass][Glass.Key.capacity]
    user.tag = userdict[User.Key.tag]

    exists, _ = ctx.database.lookup_rfid(user.tag)
    if exists:
        log.warn("user \"{}\" already exists in db - updating records".format(user.name))
    ctx.database.add(user)
    log.ok("added user " + user.name)
    return True, ctx.state


def pour_requested_handler(ctx, evt):
    if ctx.state is Context.State.GLASS_ON:
        recipe_name = evt[EventKey.requested_recipe]
        if recipe_name in ctx.recipes:
            ctx.requested_recipe = ctx.recipes[recipe_name]
            log.info("requested \"" + recipe_name + "\" recipe")
            return True, Context.State.POURING
        else:
            log.error("unknown recipe \"" + recipe_name + "\"")
            return False, ctx.state
    else:
        log.info("NO GLASS - POUR button press ignored")
        return True, ctx.state


def new_recipe_handler(ctx, evt):
    recipedict = evt[EventKey.add_recipe]
    recipe = Recipe()
    recipe.name = recipedict[Recipe.Key.name]
    recipe.steps = recipedict[Recipe.Key.steps]
    ok = ctx.add_recipe(recipe)
    if ok:
        log.ok("added recipe \"" + recipe.name + "\"")
        return True, ctx.state
    else:
        return False, ctx.state
