import sys
from winstealer import *
from commons.utils import *
from commons.skills import *
from commons.items import *
from commons.targeting import *
from evade import checkEvade
import json, time, math
import urllib3, json, urllib, ssl
from commons.targit import *
winstealer_script_info = {
    "script": "SA1-Riven",
    "author": "SA1",
    "description": "SA1-Riven",
    "target_champ": "riven",
}

combo_key = 57
harass_key = 45
laneclear_key = 47
killsteal_key = 46


autoQKey=48
use_q_stack=True

use_q_in_combo = True
use_w_in_combo = True
use_e_in_combo = True
use_r_in_combo = False

use_flash_R=True

lane_clear_with_q = True
lane_clear_with_w = True
lane_clear_with_e = True

jungle_clear_with_q = True
jungle_clear_with_w = True
jungle_clear_with_e = True
smart_combo=1

draw_q_range = True
draw_w_range = True
draw_e_range = True
draw_r_range = True

q = {"Range": 350}
w = {"Range": 260}

r = {"Range": 500}

spell_priority = {"Q": 0, "W": 0, "E": 0, "R": 0}


mana_q = [130, 115, 100, 85, 70]

# Get player stats from local server
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def getPlayerStats():
    response = urllib.request.urlopen("https://127.0.0.1:2999/liveclientdata/activeplayer").read()
    stats = json.loads(response)
    return stats

def winstealer_load_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,use_r_in_combo,use_flash_R
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e,autoQKey,use_q_stack
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,smart_combo
    
    combo_key = cfg.get_int("combo_key", 57)
    harass_key = cfg.get_int("harass_key", 45)
    laneclear_key = cfg.get_int("laneclear_key", 47)
    killsteal_key = cfg.get_int("killsteal_key", 46)

    use_q_in_combo = cfg.get_bool("use_q_in_combo", True)
    use_w_in_combo = cfg.get_bool("use_w_in_combo", True)
    use_e_in_combo = cfg.get_bool("use_e_in_combo", True)
    use_r_in_combo=cfg.get_bool("use_r_in_combo",True)
    use_flash_R=cfg.get_bool("use_flash_R",True)

    autoQKey=cfg.get_int("autoQKey",1)
    use_q_stack = cfg.get_bool("use_q_stack",use_q_stack)

    draw_q_range = cfg.get_bool("draw_q_range", False)
    draw_w_range = cfg.get_bool("draw_w_range", False)
    draw_e_range = cfg.get_bool("draw_e_range", False)
    draw_r_range = cfg.get_bool("draw_r_range", True)

    lane_clear_with_q = cfg.get_bool("lane_clear_with_q", True)
    lane_clear_with_w = cfg.get_bool("lane_clear_with_w", True)
    lane_clear_with_e = cfg.get_bool("lane_clear_with_e", True)
    
    smart_combo=cfg.get_int("smart_combo",smart_combo)
    #spell_priority = json.loads(
        #cfg.get_str("spell_priority", json.dumps(spell_priority))
    #)


def winstealer_save_cfg(cfg):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,use_r_in_combo,use_flash_R
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e,autoQKey,use_q_stack
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,smart_combo
    
    cfg.set_int("combo_key", combo_key)
    cfg.set_int("harass_key", harass_key)
    cfg.set_int("laneclear_key", laneclear_key)

    cfg.set_bool("use_q_in_combo", use_q_in_combo)
    cfg.set_bool("use_w_in_combo", use_w_in_combo)
    cfg.set_bool("use_e_in_combo", use_e_in_combo)
    cfg.set_bool("use_r_in_combo", use_r_in_combo)

    cfg.set_bool("use_flash_R",use_flash_R)

    cfg.set_int("autoQKey",autoQKey)
    cfg.set_bool("use_q_stack", use_q_stack)

    cfg.set_bool("draw_q_range", draw_q_range)
    cfg.set_bool("draw_w_range", draw_w_range)
    cfg.set_bool("draw_e_range", draw_e_range)
    cfg.set_bool("draw_r_range", draw_r_range)

    cfg.set_bool("lane_clear_with_q", lane_clear_with_q)
    cfg.set_bool("lane_clear_with_w", lane_clear_with_w)
    cfg.set_bool("lane_clear_with_e", lane_clear_with_e)
    cfg.set_int("smart_combo",smart_combo)

def winstealer_draw_settings(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo,use_r_in_combo,use_flash_R
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, harass_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e,use_q_stack,autoQKey
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,smart_combo
    
    
    combo_key = ui.keyselect("Combo key", combo_key)
    laneclear_key = ui.keyselect("Laneclear key", laneclear_key)

    autoQKey=ui.keyselect("Auto W key",autoQKey)

    ui.text("SA1-Riven : 1.0.0.0")
    ui.separator ()
    
    # smart_combo=ui.listbox("",["Spam Q/W/E","Combo E>W>Q"],smart_combo)
    if ui.treenode("Combo Settings"):
        use_q_in_combo = ui.checkbox("Use Q in Combo", use_q_in_combo)
        use_w_in_combo = ui.checkbox("Use W in Combo", use_w_in_combo)
        use_e_in_combo = ui.checkbox("Use E in Combo", use_e_in_combo)
        use_r_in_combo = ui.checkbox("Use R in Combo", use_r_in_combo)
        use_flash_R=ui.checkbox("Use Flash To kill steal", use_flash_R)
        use_q_stack=ui.checkbox("Auto W",use_q_stack)
        ui.treepop()

    if ui.treenode("Lane Clear Settings"):
        lane_clear_with_q = ui.checkbox("Laneclear with Q", lane_clear_with_q)
        lane_clear_with_w = ui.checkbox("Laneclear with W", lane_clear_with_w)
        lane_clear_with_e = ui.checkbox("Laneclear with E", lane_clear_with_e)
        ui.treepop()


    if ui.treenode("Draw Settings"):
        draw_q_range = ui.checkbox("Draw Q Range", draw_q_range)
        draw_w_range = ui.checkbox("Draw W Range", draw_w_range)
        draw_r_range = ui.checkbox("Draw R Range", draw_r_range)
        ui.treepop()

    

#mana_q = [50,60,70,80,90]
#mana_w = [70,80,90,100,110]
#mana_e = [50,48,46,44,42]
#mana_r = 100 ##for mana check later update???


########################
class Fake_target ():
    def __init__(self, name, pos, gameplay_radius):
        self.name = name
        self.pos = pos
        self.gameplay_radius = gameplay_radius

def predict_pos(target,casttime):
    """Predicts the target's new position after a duration"""
    target_direction = target.ai_navEnd.sub(target.ai_navBegin).normalize()

    veloc=target.ai_velocity
    orientation = veloc.normalize()
    if veloc.x ==0.0 and veloc.y == 0.0:
        return target.pos   

    # Target movement speed
    target_movement_speed = target.movement_speed
    # The distance that the target will have traveled after the given duration
    distance_to_travel = target_movement_speed * casttime 
    # distance_to_travel2=(timetoimpact / 2.2)* 1.5 
    return target.pos.add(target_direction.scale(distance_to_travel))



def RDamage(game, target):
    # Calculate raw R damage on target
    r_lvl = game.player.R.level
    if r_lvl == 0:
        return 0
    ap = getPlayerStats()["championStats"]["attackDamage"]
    min_dmg = [300,450,600]
    missing_hp = (target.max_health - target.health)
    missing_hp_pct = (missing_hp / target.max_health) * 100
    increased_pct = 0.015 * missing_hp_pct
    if increased_pct > 1:
        increased_pct = 1
    r_damage = (1 + increased_pct) * (min_dmg[r_lvl - 1] + 0.75 * ap)

    # Reduce damage based on target's magic resist
    mr = target.magic_resist
    if mr >= 0:
        dmg_multiplier = 100 / (100 + mr)
    else:
        dmg_multiplier = 2 - 100 / (100 - mr)
    r_damage *= dmg_multiplier
    return r_damage

lastQ=0



def AutoQ(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_e_range, draw_w_range, draw_r_range
    global combo_key, harass_key, laneclear_key,autoQKey,use_q_stack
    global lane_clear_with_e
    global q, w, e, r
    global lastQ, i
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")

    if use_w_in_combo and IsReady(game, w_spell) :
                targetQ = GetBestTargetsInRange (game,260)
                if targetQ :
                    w_spell.trigger(False)
def Evade(game):
    global e, lastW
    e_spell = getSkill(game, "E")
    w_spell = getSkill(game, "W")
    for missile in game.missiles:
        br = game.player.gameplay_radius
        if not game.player.is_alive or missile.is_ally_to(game.player):
            continue
        if not is_skillshot(missile.name):
            continue
        spell = get_missile_parent_spell(missile.name)
        if not spell:
            continue
        if InSkillShot( game, game.player.pos, missile, spell, game.player.gameplay_radius * 2) and game.is_point_on_screen(missile.pos):
        
            if use_w_in_combo:    
                if IsReady(game, w_spell):
                    w_spell.move_and_trigger(game.world_to_screen(missile.pos))
                
def effHP(game, target):
    global unitArmour, unitHP, debug_hp

    #target = GetBestTargetsInRange(game, e["Range"])
    unitArmour = target.armour
    unitHP = target.health

    return (
        (((1+(unitArmour / 100))*unitHP))
        )

def Combo(game):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo, use_r_in_combo
    global draw_q_range, draw_e_range, draw_w_range, draw_r_range
    global combo_key, laneclear_key,smart_combo
    global q, w, e, r,lastQ
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    r_spell = getSkill(game, "R")
    flash = game.player.get_summoner_spell(SummonerSpellType.Flash)
    before_cpos = game.get_cursor()
    if use_q_in_combo and IsReady(game, q_spell) :
        # for b in game.player.buffs:
        #     print(b.name)
                targetQ = TargetSelector (game,500)
                if targetQ :
                        q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))
                                   

    if use_w_in_combo and IsReady(game, w_spell) :
                target=TargetSelector(game,260)
                if target:
                        w_spell.trigger(False)                                
    if use_e_in_combo and IsReady(game, e_spell) :
                targetQ = TargetSelector (game,400)
                
                if targetQ :
                    e_spell.move_and_trigger(game.world_to_screen(targetQ.pos))
                    
    if use_r_in_combo and IsReady(game, r_spell) :
                            targetQ=TargetSelector(game,2500)

                            if targetQ:
                                hp = int(targetQ.health / targetQ.max_health * 100)
                                if hp<50 or RDamage(game,targetQ)>=effHP(game,targetQ):
                                    if game.player.R.name=="rivenfengshuiengine"  :
                                        r_spell.trigger(False)
                                if getBuff(game.player,"rivenwindslashready"):    
                                    if game.player.pos.distance (targetQ.pos) >= 800 :
                                        if use_flash_R and  IsReady(game,flash):
                                            if RDamage(game,targetQ)>=effHP(game,targetQ):
                                                flash.move_and_trigger(game.world_to_screen(targetQ.pos))
                                                time.sleep(0.01)
                                                r_spell.move_and_trigger(game.world_to_screen(targetQ.pos))
                                    if RDamage(game,targetQ)>=effHP(game,targetQ):
                                        
                                        r_spell.move_and_trigger(game.world_to_screen(targetQ.pos))   
                                         

                           
                        
                        
                        

                                        
def Laneclear(game):
    #global w, e, r
    global q, w, e, r
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e,lastQ
    global spell_priority, combo_key, laneclear_key, killsteal_key
    #q = {"Range": 600}
    
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    before_cpos = game.get_cursor()
    if lane_clear_with_q and IsReady(game, q_spell) :
                    targetQ = GetBestMinionsInRange (game,500)
                    if targetQ :
                            q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))
    if lane_clear_with_w and IsReady(game, w_spell):
        target=GetBestMinionsInRange(game,260)
        if target:
            w_spell.trigger(False)
    if lane_clear_with_e and IsReady(game,e_spell):
            targetQ = GetBestMinionsInRange (game,400)
            if targetQ :
                e_spell.move_and_trigger(game.world_to_screen(targetQ.pos))
def Jungleclear(game):
    global q, w, e, r
    global spell_priority, combo_key, laneclear_key, killsteal_key
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,lastQ
    q_spell = getSkill(game, "Q")
    w_spell = getSkill(game, "W")
    e_spell = getSkill(game, "E")
    before_cpos = game.get_cursor()
    if lane_clear_with_q and IsReady(game, q_spell) :
                    targetQ = GetBestJungleInRange (game,500)
                    if targetQ :
                            q_spell.move_and_trigger(game.world_to_screen(targetQ.pos))
    if lane_clear_with_w and IsReady(game, w_spell):
        target=GetBestJungleInRange(game,260)
        if target:
            w_spell.trigger(False)
    if lane_clear_with_e and IsReady(game,e_spell):
            targetQ = GetBestJungleInRange (game,400)
            if targetQ :
                e_spell.move_and_trigger(game.world_to_screen(targetQ.pos))
                                     
def DrawAutoQ(game):
    
    pos = game.player.pos
    if game.player.is_alive and game.player.is_visible and game.is_point_on_screen(game.player.pos):
        game.draw_button(game.world_to_screen(pos).add(Vec2(-50,20)), "Auto W: Enabled", Color.BLACK, Color.GREEN, 10.0)
def DrawNotAutoQ(game):
    
    pos = game.player.pos
    if game.player.is_alive and game.player.is_visible and game.is_point_on_screen(game.player.pos):
        game.draw_button(game.world_to_screen(pos).add(Vec2(-50,20)), "Auto W: Disabled", Color.BLACK, Color.RED, 10.0)
                                
def winstealer_update(game, ui):
    global use_q_in_combo, use_w_in_combo, use_e_in_combo
    global draw_q_range, draw_w_range, draw_e_range, draw_r_range
    global spell_priority, combo_key, laneclear_key, killsteal_key
    global lane_clear_with_q, lane_clear_with_w, lane_clear_with_e
    global jungle_clear_with_q, jungle_clear_with_w, jungle_clear_with_e,autoQKey,use_q_stack
    global q, w, e, r
    
    self = game.player
    player = game.player

   
    if self.is_alive  and  game.is_point_on_screen(game.player.pos):
        if game.was_key_pressed(combo_key):
            Combo(game)
        if use_q_stack:
            AutoQ(game)  
            DrawAutoQ(game)
        if not use_q_stack:
            DrawNotAutoQ(game)
        if game.was_key_pressed(autoQKey):
            use_q_stack=not use_q_stack        
        if game.was_key_pressed(laneclear_key):
            Laneclear(game)
            Jungleclear(game)
            