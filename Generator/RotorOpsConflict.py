import dcs
import random

jtf_red = "Combined Joint Task Forces Red"
jtf_blue = "Combined Joint Task Forces Blue"



def triggerSetup(rops, options):
    # get the boolean value from ui option and convert to lua string
    def lb(var):
        return str(options[var]).lower()

    if options["veaf"]: # create the first VEAF triggers

        #
        # /!\ CAVEAT
        #
        # This is weird: for string used in predicates we need to use the dcs.mission.string() object (which creates an entry in the translations dictionary with an id),
        #   whereas for other strings like DoScript actions, we simply need to use the dcs.action.String() object, passing it the text in the _id parameter.
        # I'm not sure why this is, perhaps an error in the original code, but it works.
        # The consequence of not using dcs.mission.string() in predicates is that the predicate works, but it cannot be changed in the DCS editor.

        # add trigger: choose VEAF scripts loading method
        trig = dcs.triggers.TriggerStart(comment="choose scripts loading method (false = static, true = dynamic)")
        trig.set_color("0x00ffffff") # cyan
        trig.rules.append(dcs.condition.Predicate(rops.m.string("return false -- scripts")))
        trig.actions.append(dcs.action.DoScript(dcs.action.String("VEAF_DYNAMIC_PATH = [[d:/dev/_VEAF/VEAF-Mission-Creation-Tools/]]")))
        rops.m.triggerrules.triggers.append(trig)

        # add trigger: choose VEAF config loading method
        trig = dcs.triggers.TriggerStart(comment="choose config loading method (false = static, true = dynamic)")    
        trig.set_color("0x00ffffff") # cyan
        trig.rules.append(dcs.condition.Predicate(rops.m.string("return false -- config")))
        trig.actions.append(dcs.action.DoScript(dcs.action.String("VEAF_DYNAMIC_MISSIONPATH = [[d:/dev/_VEAF/RotorOps/scripts/veaf/]]")))
        rops.m.triggerrules.triggers.append(trig)

        # add trigger: VEAF scripts loading (dynamic method)
        # the dynamic loading version loads the scripts from the Veaf Mission Creation Tools repository local clone
        trig = dcs.triggers.TriggerStart(comment="mission start - dynamic")    
        trig.set_color("0x00ff80ff") # light green
        trig.rules.append(dcs.condition.Predicate(rops.m.string("return VEAF_DYNAMIC_PATH~=nil")))
        trig.actions.append(dcs.action.DoScript(dcs.action.String("env.info(\"DYNAMIC SCRIPTS LOADING\")")))
        trig.actions.append(dcs.action.DoScript(dcs.action.String("assert(loadfile(VEAF_DYNAMIC_PATH .. \"/src/scripts/community/mist.lua\"))()")))
        trig.actions.append(dcs.action.DoScript(dcs.action.String("assert(loadfile(VEAF_DYNAMIC_PATH .. \"/src/scripts/community/DCS-SimpleTextToSpeech.lua\"))()")))
        trig.actions.append(dcs.action.DoScript(dcs.action.String("assert(loadfile(VEAF_DYNAMIC_PATH .. \"/src/scripts/community/CTLD.lua\"))()"))) 
        trig.actions.append(dcs.action.DoScript(dcs.action.String("assert(loadfile(VEAF_DYNAMIC_PATH .. \"/src/scripts/community/WeatherMark.lua\"))()")))
        trig.actions.append(dcs.action.DoScript(dcs.action.String("assert(loadfile(VEAF_DYNAMIC_PATH .. \"/src/scripts/community/skynet-iads-compiled.lua\"))()")))
        trig.actions.append(dcs.action.DoScript(dcs.action.String("assert(loadfile(VEAF_DYNAMIC_PATH .. \"/src/scripts/community/Hercules_Cargo.lua\"))()")))
        trig.actions.append(dcs.action.DoScript(dcs.action.String("assert(loadfile(VEAF_DYNAMIC_PATH .. \"/src/scripts/community/HoundElint.lua\"))()")))
        trig.actions.append(dcs.action.DoScript(dcs.action.String("assert(loadfile(VEAF_DYNAMIC_PATH .. \"/src/scripts/VeafDynamicLoader.lua\"))()")))
        rops.m.triggerrules.triggers.append(trig)

        # add trigger: VEAF scripts loading (static method)
        # the static loading version loads the scripts from the mission
        trig = dcs.triggers.TriggerStart(comment="mission start - static")    
        trig.set_color("0x00ff80ff") # light green
        trig.rules.append(dcs.condition.Predicate(rops.m.string("return VEAF_DYNAMIC_PATH==nil")))
        trig.actions.append(dcs.action.DoScript(dcs.action.String("env.info(\"STATIC SCRIPTS LOADING\")")))
        trig.actions.append(dcs.action.DoScriptFile(rops.scripts["mist.lua"]))
        trig.actions.append(dcs.action.DoScriptFile(rops.scripts["DCS-SimpleTextToSpeech.lua"]))
        trig.actions.append(dcs.action.DoScriptFile(rops.scripts["CTLD-veaf.lua"])) # had to rename CTLD to avoid conflict with the vanilla Rotorops version
        trig.actions.append(dcs.action.DoScriptFile(rops.scripts["WeatherMark.lua"]))
        trig.actions.append(dcs.action.DoScriptFile(rops.scripts["skynet-iads-compiled.lua"]))
        trig.actions.append(dcs.action.DoScriptFile(rops.scripts["Hercules_Cargo.lua"]))
        trig.actions.append(dcs.action.DoScriptFile(rops.scripts["HoundElint.lua"]))
        trig.actions.append(dcs.action.DoScriptFile(rops.scripts["veaf-scripts.lua"]))
        rops.m.triggerrules.triggers.append(trig)

    # add trigger: choose Rotorops scripts loading method
    trig = dcs.triggers.TriggerStart(comment="choose Rotorops scripts loading method (false = static, true = dynamic)")
    trig.set_color("0x00ffffff") # cyan
    trig.rules.append(dcs.condition.Predicate(rops.m.string("return false -- Rotorops scripts")))
    trig.actions.append(dcs.action.DoScript(dcs.action.String("ROTOROPS_DYNAMIC_PATH = [[d:/dev/_VEAF/RotorOps/]]")))
    rops.m.triggerrules.triggers.append(trig)

    # prepare Rotorops options setup script snippet
    options_script = ("--OPTIONS HERE!\n\n" +
              "RotorOps.CTLD_crates = " + lb("crates") + "\n\n" +
              "RotorOps.CTLD_sound_effects = true\n\n" +
              "RotorOps.force_offroad = " + lb("force_offroad") + "\n\n" +
              "RotorOps.voice_overs = " + lb("voiceovers") + "\n\n" +
              "RotorOps.zone_status_display = " + lb("game_display") + "\n\n" +
              "RotorOps.inf_spawn_messages = true\n\n" +
              "RotorOps.inf_spawns_total = " + lb("inf_spawn_qty") + "\n\n" +
              "RotorOps.apcs_spawn_infantry = " + lb("apc_spawns_inf") + " \n\n" +
              "RotorOps.fighter_min_detection_alt = 609\n\n" +
              "RotorOps.fighter_max_active = 2\n\n")
    if not options["smoke_pickup_zones"]:
        options_script = options_script + 'RotorOps.pickup_zone_smoke = "none"\n\n'

    # add trigger: RotorOps Setup Scripts (dynamic method)
    trig = dcs.triggers.TriggerStart(comment="RotorOps Setup Scripts - dynamic")    
    trig.set_color("0xffff00ff") # yellow
    trig.rules.append(dcs.condition.Predicate(rops.m.string("return ROTOROPS_DYNAMIC_PATH~=nil")))
    trig.actions.append(dcs.action.DoScript(dcs.action.String("env.info(\"DYNAMIC ROTOROPS SETUP SCRIPTS\")")))
    trig.actions.append(dcs.action.DoScript(dcs.action.String("assert(loadfile(ROTOROPS_DYNAMIC_PATH .. \"/scripts/mist_4_5_107_grimm.lua\"))()")))
    trig.actions.append(dcs.action.DoScript(dcs.action.String("assert(loadfile(ROTOROPS_DYNAMIC_PATH .. \"/scripts/Splash_Damage_2_0.lua\"))()")))
    trig.actions.append(dcs.action.DoScript(dcs.action.String("assert(loadfile(ROTOROPS_DYNAMIC_PATH .. \"/scripts/CTLD.lua\"))()")))
    trig.actions.append(dcs.action.DoScript(dcs.action.String("assert(loadfile(ROTOROPS_DYNAMIC_PATH .. \"/scripts/RotorOps.lua\"))()")))
    if options["perks"]:
            trig.actions.append(dcs.action.DoScript(dcs.action.String("assert(loadfile(ROTOROPS_DYNAMIC_PATH .. \"/scripts/RotorOpsPerks.lua\"))()")))
    trig.actions.append(dcs.action.DoScript(dcs.action.String((options_script))))
    if options["script"]:
        trig.actions.append(dcs.action.DoScript(dcs.action.String((options["script"]))))
    rops.m.triggerrules.triggers.append(trig)

    # add trigger: RotorOps Setup Scripts (static method)
    trig = dcs.triggers.TriggerStart(comment="RotorOps Setup Scripts - static")    
    trig.set_color("0xffff00ff") # yellow
    trig.rules.append(dcs.condition.Predicate(rops.m.string("return ROTOROPS_DYNAMIC_PATH==nil")))
    trig.actions.append(dcs.action.DoScript(dcs.action.String("env.info(\"STATIC ROTOROPS SETUP SCRIPTS\")")))
    trig.actions.append(dcs.action.DoScriptFile(rops.scripts["mist_4_5_107_grimm.lua"]))
    trig.actions.append(dcs.action.DoScriptFile(rops.scripts["Splash_Damage_2_0.lua"]))
    trig.actions.append(dcs.action.DoScriptFile(rops.scripts["CTLD.lua"]))
    trig.actions.append(dcs.action.DoScriptFile(rops.scripts["RotorOps.lua"]))
    if options["perks"]:
        trig.actions.append(dcs.action.DoScriptFile(rops.scripts["RotorOpsPerks.lua"]))
    trig.actions.append(dcs.action.DoScript(dcs.action.String((options_script))))
    if options["script"]:
        trig.actions.append(dcs.action.DoScript(dcs.action.String((options["script"]))))
    rops.m.triggerrules.triggers.append(trig)

    # Add the second trigger
    game_flag = 100
    trig = dcs.triggers.TriggerStart(comment="RotorOps Setup Zones")
    for s_zone in rops.staging_zones:
        trig.actions.append(dcs.action.DoScript(dcs.action.String("RotorOps.addStagingZone('" + s_zone + "')")))
    for c_zone in rops.conflict_zones:
        zone_flag = rops.conflict_zones[c_zone].flag
        trig.actions.append(
            dcs.action.DoScript(dcs.action.String("RotorOps.addZone('" + c_zone + "'," + str(zone_flag) + ")")))

    trig.actions.append(dcs.action.DoScript(dcs.action.String("RotorOps.setupConflict('" + str(game_flag) + "')")))

    rops.m.triggerrules.triggers.append(trig)

    if options["veaf"]: # create the remaining VEAF triggers

        # add trigger: mission config (dynamic method)
        trig = dcs.triggers.TriggerStart(comment="mission config - dynamic")
        trig.set_color("0x8080ffff") # violet
        trig.rules.append(dcs.condition.Predicate(rops.m.string("return VEAF_DYNAMIC_MISSIONPATH~=nil")))
        trig.actions.append(dcs.action.DoScript(dcs.action.String("env.info(\"DYNAMIC CONFIG LOADING\")")))
        #trig.actions.append(dcs.action.DoScript(dcs.action.String("assert(loadfile(VEAF_DYNAMIC_MISSIONPATH .. \"/src/scripts/missionConfig.lua\"))()")))
        trig.actions.append(dcs.action.DoScript(dcs.action.String("assert(loadfile(VEAF_DYNAMIC_MISSIONPATH .. \"/missionConfig.lua\"))()")))
        rops.m.triggerrules.triggers.append(trig)

        # add trigger: mission config (static method)
        trig = dcs.triggers.TriggerStart(comment="mission config - static")
        trig.set_color("0x8080ffff") # violet
        trig.rules.append(dcs.condition.Predicate(rops.m.string("return VEAF_DYNAMIC_MISSIONPATH==nil")))
        trig.actions.append(dcs.action.DoScript(dcs.action.String("env.info(\"STATIC CONFIG LOADING\")")))
        trig.actions.append(dcs.action.DoScriptFile(rops.scripts["missionConfig.lua"]))
        rops.m.triggerrules.triggers.append(trig)

    # Add the start trigger
    if options["start_trigger"] is not False:
        trig = dcs.triggers.TriggerOnce(comment="RotorOps Conflict Start")
        trig.rules.append(dcs.condition.TimeAfter(10))
        trig.actions.append(dcs.action.DoScript(dcs.action.String("RotorOps.startConflict(100)")))
        rops.m.triggerrules.triggers.append(trig)

    if options["rotorops_server"]:

        trig = dcs.triggers.TriggerOnce(comment="RotorOps Set Up Server")
        trig.rules.append(dcs.condition.TimeAfter(4))
        trig.actions.append(dcs.action.DoScriptFile(rops.scripts["RotorOpsServer.lua"]))
        # Slot block the zone spawns if SSB is available
        trig.actions.append(dcs.action.SetFlagValue('SSB', 100))
        for c_zone in rops.conflict_zones:
            for group in rops.all_zones[c_zone].player_helo_spawns:
                trig.actions.append(dcs.action.SetFlagValue(group.name, 100))

        rops.m.triggerrules.triggers.append(trig)


    # Add generic zone-based triggers
    for index, zone_name in enumerate(rops.conflict_zones):
        z_active_trig = dcs.triggers.TriggerOnce(comment=zone_name + " Active")
        z_active_trig.rules.append(dcs.condition.FlagEquals(game_flag, index + 1))
        z_active_trig.actions.append(dcs.action.DoScript(dcs.action.String("--Add any action you want here!")))
        rops.m.triggerrules.triggers.append(z_active_trig)

    # # Add CTLD beacons - this might be cool but we'd need to address placement of the 3D objects
    # trig = dcs.triggers.TriggerOnce(comment="RotorOps CTLD Beacons")
    # trig.rules.append(dcs.condition.TimeAfter(5))
    # trig.actions.append(dcs.action.DoScript(dcs.action.String("ctld.createRadioBeaconAtZone('STAGING','blue', 1440,'STAGING/LOGISTICS')")))
    # for c_zone in rops.conflict_zones:
    #     trig.actions.append(
    #         dcs.action.DoScript(dcs.action.String("ctld.createRadioBeaconAtZone('" + c_zone + "','blue', 1440,'" + c_zone + "')")))
    # rops.m.triggerrules.triggers.append(trig)

    # # Zone protection SAMs
    # if options["zone_protect_sams"]:
    #     for index, zone_name in enumerate(rops.conflict_zones):
    #         z_sams_trig = dcs.triggers.TriggerOnce(comment="Deactivate " + zone_name + " SAMs")
    #         z_sams_trig.rules.append(dcs.condition.FlagEquals(game_flag, index + 1))
    #         z_sams_trig.actions.append(dcs.action.DoScript(
    #             dcs.action.String("Group.destroy(Group.getByName('" + zone_name + " Protect Static'))")))
    #         rops.m.triggerrules.triggers.append(z_sams_trig)

    # Deactivate zone FARPs and player slots in defensive mode:
    # this will also deactivate players already in the air.
    # if options["defending"]:
    #     for index, zone_name in enumerate(rops.conflict_zones):
    #         z_farps_trig = dcs.triggers.TriggerOnce(comment="Deactivate " + zone_name + " FARP")
    #         z_farps_trig.rules.append(dcs.condition.FlagEquals(game_flag, index + 1))
    #         z_farps_trig.actions.append(dcs.action.DeactivateGroup(rops.m.country(jtf_blue).find_group(zone_name + " FARP Static").id))
    #         for group in rops.all_zones[zone_name].player_helo_spawns:
    #             z_farps_trig.actions.append(
    #                 dcs.action.DeactivateGroup(
    #                     group.id))
    #         rops.m.triggerrules.triggers.append(z_farps_trig)

    # Zone FARPS always
    if options["zone_farps"] == "farp_always" and not options["defending"]:
        for index, zone_name in enumerate(rops.conflict_zones):
            if index > 0:
                previous_zone = list(rops.conflict_zones)[index - 1]
                if not rops.m.country(jtf_blue).find_group(previous_zone + " FARP Static"):
                    continue
                z_farps_trig = dcs.triggers.TriggerOnce(comment="Activate " + previous_zone + " FARP")
                z_farps_trig.rules.append(dcs.condition.FlagEquals(game_flag, index + 1))
                z_farps_trig.actions.append(
                    dcs.action.ActivateGroup(rops.m.country(jtf_blue).find_group(previous_zone + " FARP Static").id))
                # Activate late-activated helicopters at FARPs if SSB slot blocking script is available
                for group in rops.all_zones[previous_zone].player_helo_spawns:
                    z_farps_trig.actions.append(
                        dcs.action.SetFlagValue(group.name, 0))
                z_farps_trig.actions.append(dcs.action.DoScript(dcs.action.String(
                    "RotorOps.farpEstablished(" + str(index) + ", '" + previous_zone + "_FARP')")))
                rops.m.triggerrules.triggers.append(z_farps_trig)

    # Zone FARPS conditional on staged units remaining
    if options["zone_farps"] == "farp_gunits" and not options["defending"]:
        for index, zone_name in enumerate(rops.conflict_zones):
            if index > 0:
                previous_zone = list(rops.conflict_zones)[index - 1]
                if not rops.m.country(jtf_blue).find_group(previous_zone + " FARP Static"):
                    continue
                z_farps_trig = dcs.triggers.TriggerOnce(comment="Activate " + previous_zone + " FARP")
                z_farps_trig.rules.append(dcs.condition.FlagEquals(game_flag, index + 1))
                z_farps_trig.rules.append(dcs.condition.FlagIsMore(111, 20))
                z_farps_trig.actions.append(dcs.action.DoScript(dcs.action.String(
                    "--The 100 flag indicates which zone is active.  The 111 flag value is the percentage of staged units remaining")))
                z_farps_trig.actions.append(
                    dcs.action.ActivateGroup(rops.m.country(jtf_blue).find_group(previous_zone + " FARP Static").id))
                # Activate late-activated helicopters at FARPs if SSB slot blocking script is available
                for group in rops.all_zones[previous_zone].player_helo_spawns:
                    z_farps_trig.actions.append(
                        dcs.action.SetFlagValue(group.name, 0))
                z_farps_trig.actions.append(dcs.action.DoScript(dcs.action.String(
                    "RotorOps.farpEstablished(" + str(index) + ", '" + previous_zone + "_FARP')")))
                rops.m.triggerrules.triggers.append(z_farps_trig)

    # Add attack helos triggers
    for index in range(options["e_attack_helos"]):
        random_zone_obj = random.choice(list(rops.conflict_zones.items()))
        zone = random_zone_obj[1]
        z_weak_trig = dcs.triggers.TriggerOnce(comment=zone.name + " Attack Helo")
        z_weak_trig.rules.append(dcs.condition.FlagIsMore(zone.flag, 1))
        z_weak_trig.rules.append(dcs.condition.FlagIsLess(zone.flag, random.randrange(20, 90)))
        z_weak_trig.actions.append(dcs.action.DoScript(dcs.action.String("---Flag " + str(
            zone.flag) + " value represents the percentage of defending ground units remaining in zone. ")))
        z_weak_trig.actions.append(dcs.action.DoScript(dcs.action.String("RotorOps.spawnAttackHelos()")))
        rops.m.triggerrules.triggers.append(z_weak_trig)

    # Add attack plane triggers
    for index in range(options["e_attack_planes"]):
        random_zone_obj = random.choice(list(rops.conflict_zones.items()))
        zone = random_zone_obj[1]
        z_weak_trig = dcs.triggers.TriggerOnce(comment=zone.name + " Attack Plane")
        z_weak_trig.rules.append(dcs.condition.FlagIsMore(zone.flag, 1))
        z_weak_trig.rules.append(dcs.condition.FlagIsLess(zone.flag, random.randrange(20, 90)))
        z_weak_trig.actions.append(dcs.action.DoScript(dcs.action.String("---Flag " + str(
            zone.flag) + " value represents the percentage of defending ground units remaining in zone. ")))
        z_weak_trig.actions.append(dcs.action.DoScript(dcs.action.String("RotorOps.spawnAttackPlanes()")))
        rops.m.triggerrules.triggers.append(z_weak_trig)

    # Add transport helos triggers
    for index in range(options["e_transport_helos"]):
        random_zone_obj = random.choice(list(rops.conflict_zones.items()))
        zone = random_zone_obj[1]
        z_weak_trig = dcs.triggers.TriggerOnce(comment=zone.name + " Transport Helo")
        z_weak_trig.rules.append(dcs.condition.FlagIsMore(zone.flag, 1))
        z_weak_trig.rules.append(dcs.condition.FlagIsLess(zone.flag, random.randrange(20, 100)))
        z_weak_trig.actions.append(dcs.action.DoScript(dcs.action.String(
            "---Flag " + str(game_flag) + " value represents the index of the active zone. ")))
        z_weak_trig.actions.append(dcs.action.DoScript(dcs.action.String("---Flag " + str(
            zone.flag) + " value represents the percentage of defending ground units remaining in zone. ")))
        z_weak_trig.actions.append(dcs.action.DoScript(
            dcs.action.String("RotorOps.spawnTranspHelos(8," + str(options["transport_drop_qty"]) + ")")))
        rops.m.triggerrules.triggers.append(z_weak_trig)

    # Add enemy CAP spawn trigger
    cap_trig = dcs.triggers.TriggerContinious(comment="Spawn Enemy CAP")
    cap_trig.rules.append(dcs.condition.TimeAfter(10))
    cap_trig.rules.append(dcs.condition.Predicate(rops.m.string("return RotorOps.predSpawnRedCap()")))
    cap_trig.actions.append(dcs.action.DoScript(dcs.action.String("RotorOps.deployFighters()")))
    rops.m.triggerrules.triggers.append(cap_trig)

    # Add game won/lost triggers


    # Add game won triggers
    mission_end_delay = 1200
    trig = dcs.triggers.TriggerOnce(comment="RotorOps Conflict WON")
    trig.rules.append(dcs.condition.FlagEquals(game_flag, 99))
    trig.actions.append(
        dcs.action.DoScript(dcs.action.String("---Add an action you want to happen when the game is WON")))
    if options["end_trigger"] is not False:
        trig.actions.append(
            dcs.action.DoScript(dcs.action.String("RotorOps.gameMsg(RotorOps.gameMsgs.success)")))
        trig.actions.append(dcs.action.DoScript(dcs.action.String(
            "timer.scheduleFunction(function()trigger.action.setUserFlag('mission_end', 2) end, {}, timer.getTime() + " + str(
                mission_end_delay) + ")")))
        trig.actions.append(dcs.action.MessageToAll(dcs.action.String("Time to RTB.  Mission will end soon."), mission_end_delay))

        mission_end_trigger = dcs.triggers.TriggerOnce(comment="End the mission")
        mission_end_trigger.rules.append(dcs.condition.FlagEquals("mission_end", 2))
        mission_end_trigger.actions.append(dcs.action.EndMission(text=dcs.action.String("Blue forces won!")))
        rops.m.triggerrules.triggers.append(mission_end_trigger)


    rops.m.triggerrules.triggers.append(trig)

    # Add game lost triggers
    trig = dcs.triggers.TriggerOnce(comment="RotorOps Conflict LOST")
    trig.rules.append(dcs.condition.FlagEquals(game_flag, 98))
    trig.actions.append(
        dcs.action.DoScript(dcs.action.String("---Add an action you want to happen when the game is LOST")))
    if options["end_trigger"] is not False:
        trig.actions.append(dcs.action.DoScript(dcs.action.String("RotorOps.gameMsg(RotorOps.gameMsgs.failure)")))
        trig.actions.append(dcs.action.DoScript(dcs.action.String(
            "timer.scheduleFunction(function()trigger.action.setUserFlag('mission_end', 1) end, {}, timer.getTime() + " + str(
                mission_end_delay) + ")")))
        trig.actions.append(
            dcs.action.MessageToAll(dcs.action.String("Time to RTB.  Mission will end soon."), mission_end_delay))
        mission_end_trigger = dcs.triggers.TriggerOnce(comment="End the mission")
        mission_end_trigger.rules.append(dcs.condition.FlagEquals("mission_end", 1))
        mission_end_trigger.actions.append(dcs.action.EndMission(text=dcs.action.String("Red forces won!")))
        rops.m.triggerrules.triggers.append(mission_end_trigger)

    rops.m.triggerrules.triggers.append(trig)