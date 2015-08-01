# coding: utf-8

import pygame
from pygame.locals import *
from gameutil import *
from gamestate import *
from random import randint

class GameController():
    def __init__(self):
        self._game_control_phase = ''
        self._strategy_command = StrategyCommand()
    
    def _set_game_control_phase(self, game_control_phase):
        self._game_control_phase = game_control_phase
    
    def _get_game_control_phase(self):
        return self._game_control_phase
    
    def control_scene(self, screen, game_state):
        pass

class BigMapController(GameController):

    def __init__(self):
        GameController.__init__(self)
        self._strategy_acceptable_flag = True

    #GAME_CONTROL_PHASE
    PH_NORMAL, PH_FIRST_MESSAGE, PH_ADD_ARMY, PH_BUY_PLANE, PH_BUY_ICBM, \
    PH_ATTACH, PH_BOMB, PH_ICBM, PH_SPY, PH_SELL_OIL, PH_OIL_DERRICK, PH_SPEECH \
            = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
    
    def control_scene(self, screen, game_state):
        
        countries = game_state.get_countries()

        if game_state.get_status() == GameConstUtil.get_game_status("BIG_MAP"):
            if screen.get_strategy_acceptable_flag():
                ################################################################
                #Strategy Execution....
                ################################################################
                if countries[game_state.get_turn()]["HUMAN_CONTROLLED"]:
                    result = {"MESSAGE": "", "RESULT":GameConstUtil.get_game_event("PLAYER_TURN")}
                else:
                    result = {"MESSAGE": "Strategy in execution..\nThis is a 2nd line.\nthis is a 3rd line.", "RESULT":GameConstUtil.get_game_event("NORMAL")}
                
                screen.set_strategy_result(result)
        
            if screen.get_ready_to_next_flag():
                if countries[game_state.get_turn()]["HUMAN_CONTROLLED"]:
                    screen.set_strategy_acceptable_flag(True)
                    screen.set_ready_to_next_flag(False)
                    game_state.set_status(GameConstUtil.get_game_status("STRATEGY_EXEC"))
                    print "BIG_MAP:Turn %d" % game_state.get_turn()
                else:
                    screen.set_strategy_acceptable_flag(True)
                    screen.set_ready_to_next_flag(False)
                    game_state.increment_turn()

class StrategyExecController(GameController):
    
    #GAME_CONTROL_PHASE
    PH_NORMAL, PH_RAISE_TAX, PH_CAPITAL_DEFENSE, PH_ADD_ARMY, PH_BUY_PLANE, PH_BUY_ICBM, \
    PH_GROUND_ATTACK, PH_AIR_STRIKE, PH_ICBM, PH_SPY, PH_SELL_OIL, PH_OIL_DERRICK, PH_SPEECH \
            = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    
    def __init__(self):
        GameController.__init__(self)
        self._game_control_phase = self.PH_NORMAL
        self._result = {"MESSAGE":"", "RESULT":GameConstUtil.get_game_event("NORMAL")}
        self._status_reserved = GameConstUtil.get_game_status("STRATEGY_EXEC") 
        self._wait_flag = False
        self._ready_to_next_flag = False
        #self._game_status = GameConstUtil.get_game_status("STRATEGY_EXEC")
    
    def _increment_turn(self, game_state):

        if self._ready_to_next_flag:
            country_map = game_state.get_countries()[game_state.get_turn()]["COUNTRY_MAP"]
            print "country_turn %d" % game_state.get_turn()
            #If the number of oil derricks is short, placing a new oil derrick.
            print "Num of Active Derrick %d" % country_map.get_num_of_active_oil_derrick()
            if country_map.get_num_of_active_oil_derrick() < GameConstUtil.get_num_of_oil_derrick():
                #self._status_reserved = game_state.get_status()
                self._game_control_phase = self.PH_OIL_DERRICK
                self._ready_to_next_flag = False
                #game_state.set_status(GameConstUtil.get_game_status("STRATEGY_EXEC"))
            else:
                self._ready_to_next_flag = False
                print "###HERE: stauts_reserved=%d" % self._status_reserved
                game_state.set_status(self._status_reserved)
                game_state.increment_turn()
         
    def control_scene(self, screen, game_state):
        
        countries = game_state.get_countries()
        country = countries[game_state.get_turn()]

        #if self._result["RESULT"] == GameConstUtil.get_game_event("ERROR"):
        if self._wait_flag:
            pygame.time.wait(GameConstUtil.get_wait_millisec())
        
        self._increment_turn(game_state)
        
        ##############################
        #Standard Menu Message    
        ##############################
        if self._game_control_phase == self.PH_NORMAL:
            message_text = "Mr.President, what would you like to do? " + "\n" \
                            + "1.Speech 2.Raise Tax 3.Capital Defense 4.Add Army 5.Buy Plane 6.Buy ICBM 7.Ground Attack 8.Air Strike 9.ICBM 10.Spy 11.Sell Oil 0:Do nothing" + "\n" 
    
            self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
            screen.set_strategy_result(self._result)
            
            if game_state.get_keyinput_confirmed_flag():
                #0:Do Nothing
                if game_state.get_keyinput_confirmed() == str(0):
                    self._game_control_phase = self.PH_NORMAL
                    self._status_reserved = GameConstUtil.get_game_status("BIG_MAP")
                    #game_state.set_status(GameConstUtil.get_game_status("BIG_MAP"))
                    #self._increment_turn(game_state)
                    self._ready_to_next_flag = True
                #1:Speech
                elif game_state.get_keyinput_confirmed() == str(1):
                    message_text = "That's a good idea! Your support rate will be improved."
                    self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
                    screen.set_strategy_result(self._result)
                    self._wait_flag = True             
                    self._status_reserved = GameConstUtil.get_game_status("BIG_MAP")
                    
                    self._strategy_command.improve_support_rate(game_state)
                    
                    #game_state.set_status(GameConstUtil.get_game_status("BIG_MAP"))
                    #self._increment_turn(game_state)
                    self._ready_to_next_flag = True
                #2:Raise Tax
                elif game_state.get_keyinput_confirmed() == str(2):
                    self._game_control_phase = self.PH_RAISE_TAX
                #3:Capital Defense
                elif game_state.get_keyinput_confirmed() == str(3):
                    self._game_control_phase = self.PH_CAPITAL_DEFENSE
                #4:Add Army
                elif game_state.get_keyinput_confirmed() == str(4):
                    self._game_control_phase = self.PH_ADD_ARMY
                #5:Buy Plane
                elif game_state.get_keyinput_confirmed() == str(5):
                    self._game_control_phase = self.PH_BUY_PLANE
                #6:Buy ICBM
                elif game_state.get_keyinput_confirmed() == str(6):
                    self._game_control_phase = self.PH_BUY_ICBM
                #7:Ground Attack
                elif game_state.get_keyinput_confirmed() == str(7):
                    self._game_control_phase = self.PH_GROUND_ATTACK
                #8:Air Strike
                elif game_state.get_keyinput_confirmed() == str(8):
                    self._game_control_phase = self.PH_AIR_STRIKE
                #9:ICBM
                elif game_state.get_keyinput_confirmed() == str(9):
                    self._game_control_phase = self.PH_ICBM
                #10:Spy
                elif game_state.get_keyinput_confirmed() == str(10):
                    self._game_control_phase = self.PH_SPY
                #11:Sell Oil
                elif game_state.get_keyinput_confirmed() == str(11):
                    self._game_control_phase = self.PH_SELL_OIL
                else:
                    message_text = "Hey!" 
                    self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("ERROR")}
                    self._wait_flag = True
                    screen.set_strategy_result(self._result)

        ##############################
        #Raise Tax Menu Message    
        ##############################
        elif self._game_control_phase == self.PH_RAISE_TAX:
            message_text = "What will be the new rate (" + str(country["TAX_RATE"]) + "%-50%, 0:Cancel)? " 
            self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
            screen.set_strategy_result(self._result)

            if game_state.get_keyinput_confirmed_flag():
                if len(game_state.get_keyinput_confirmed()) == 0:   #Just a CR without entering any number
                    message_text = "Hey!" 
                    self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("ERROR")}
                    screen.set_strategy_result(self._result)
                    self._wait_flag = True
                else:
                    input_rate = int(game_state.get_keyinput_confirmed())
                    #0:Cancel
                    if input_rate == 0:
                        self._game_control_phase = self.PH_NORMAL
                    elif input_rate < country["TAX_RATE"]:
                        message_text = "Hey!" 
                        self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("ERROR")}
                        screen.set_strategy_result(self._result)
                        self._wait_flag = True
                    elif input_rate == country["TAX_RATE"]:
                        self._game_control_phase = self.PH_NORMAL
                    elif input_rate > 50:
                        message_text = "Are you killing us!" 
                        self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("ERROR")}
                        screen.set_strategy_result(self._result)
                        self._wait_flag = True
                    #Valid Input
                    else:
                        self._strategy_command.change_tax_rate(game_state, int(game_state.get_keyinput_confirmed()))
                        self._game_control_phase = self.PH_NORMAL
                        #game_state.set_status(GameConstUtil.get_game_status("BIG_MAP"))
                        message_text = "People are complaining..." 
                        self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
                        screen.set_strategy_result(self._result)                        
                        self._wait_flag = True
                        self._status_reserved = GameConstUtil.get_game_status("BIG_MAP")
                        #self._increment_turn(game_state)
                        self._ready_to_next_flag = True

        ##############################
        #Capital Defense Menu Message    
        ##############################
        elif self._game_control_phase == self.PH_CAPITAL_DEFENSE:
            message_text = "How much will you increase the defense (0-" + str((country["MONEY"]) / 10) + ", 0:Cancel)? " 
            self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
            screen.set_strategy_result(self._result)
            
            if game_state.get_keyinput_confirmed_flag():
                if len(game_state.get_keyinput_confirmed()) == 0:   #Just a CR without entering any number
                    message_text = "Hey!" 
                    self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("ERROR")}
                    screen.set_strategy_result(self._result)
                    self._wait_flag = True
                else:    
                    input_value = int(game_state.get_keyinput_confirmed())
                    #0:Cancel
                    if input_value == 0:
                        self._game_control_phase = self.PH_NORMAL
                    #Valid Input
                    elif input_value <= (country["MONEY"] / 10):
                        new_defense = country["COUNTRY_MAP"].get_capital().get_defense() + input_value
                        country["COUNTRY_MAP"].get_capital().set_defense(new_defense)
                        country["MONEY"] -= 10 * input_value

                        self._game_control_phase = self.PH_NORMAL
                        message_text = "The residents can sleep in peace!" 
                        self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
                        screen.set_strategy_result(self._result)                        
                        self._wait_flag = True
                        self._status_reserved = GameConstUtil.get_game_status("BIG_MAP")
                        self._ready_to_next_flag = True

        ##############################
        #Add Army Menu Message    
        ##############################
        elif self._game_control_phase == self.PH_ADD_ARMY:
            message_text = "How much will you increase your army (0-" + str((country["MONEY"]) / 10) + ", 0:Cancel)? " 
            self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
            screen.set_strategy_result(self._result)
            
            if game_state.get_keyinput_confirmed_flag():
                if len(game_state.get_keyinput_confirmed()) == 0:   #Just a CR without entering any number
                    message_text = "Hey!" 
                    self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("ERROR")}
                    screen.set_strategy_result(self._result)
                    self._wait_flag = True
                else:    
                    input_value = int(game_state.get_keyinput_confirmed())
                    #0:Cancel
                    if input_value == 0:
                        self._game_control_phase = self.PH_NORMAL
                    #Valid Input
                    elif input_value <= (country["MONEY"] / 10):
                        country["ARMY"] += input_value
                        country["MONEY"] -= 10 * input_value

                        self._game_control_phase = self.PH_NORMAL
                        message_text = "Glory to our army!" 
                        self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
                        screen.set_strategy_result(self._result)                        
                        self._wait_flag = True
                        self._status_reserved = GameConstUtil.get_game_status("BIG_MAP")
                        self._ready_to_next_flag = True

        ##############################
        #Buy Plane Menu Message    
        ##############################
        elif self._game_control_phase == self.PH_BUY_PLANE:
            message_text = "How many will you buy (0-" + str((country["MONEY"]) / game_state.get_plane_price()) + ", 0:Cancel)? " 
            self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
            screen.set_strategy_result(self._result)
            
            if game_state.get_keyinput_confirmed_flag():
                if len(game_state.get_keyinput_confirmed()) == 0:   #Just a CR without entering any number
                    message_text = "Hey!" 
                    self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("ERROR")}
                    screen.set_strategy_result(self._result)
                    self._wait_flag = True
                else:    
                    input_value = int(game_state.get_keyinput_confirmed())
                    #0:Cancel
                    if input_value == 0:
                        self._game_control_phase = self.PH_NORMAL
                    #Valid Input
                    elif input_value <= ((country["MONEY"]) / game_state.get_plane_price()):
                        country["PLANE"] += input_value
                        country["MONEY"] -= game_state.get_plane_price() * input_value

                        self._game_control_phase = self.PH_NORMAL
                        message_text = "Glory to our air force!" 
                        self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
                        screen.set_strategy_result(self._result)                        
                        self._wait_flag = True
                        self._status_reserved = GameConstUtil.get_game_status("BIG_MAP")
                        self._ready_to_next_flag = True

        ##############################
        #Buy ICBM Menu Message    
        ##############################
        elif self._game_control_phase == self.PH_BUY_ICBM:
            message_text = "How many will you buy (0-" + str((country["MONEY"]) / game_state.get_icbm_price()) + ", 0:Cancel)? " 
            self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
            screen.set_strategy_result(self._result)
            
            if game_state.get_keyinput_confirmed_flag():
                if len(game_state.get_keyinput_confirmed()) == 0:   #Just a CR without entering any number
                    message_text = "Hey!" 
                    self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("ERROR")}
                    screen.set_strategy_result(self._result)
                    self._wait_flag = True
                else:    
                    input_value = int(game_state.get_keyinput_confirmed())
                    #0:Cancel
                    if input_value == 0:
                        self._game_control_phase = self.PH_NORMAL
                    #Valid Input
                    elif input_value <= ((country["MONEY"]) / game_state.get_icbm_price()):
                        country["ICBM"] += input_value
                        country["MONEY"] -= game_state.get_icbm_price() * input_value

                        self._game_control_phase = self.PH_NORMAL
                        message_text = "You've got a lethal weapon..." 
                        self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
                        screen.set_strategy_result(self._result)                        
                        self._wait_flag = True
                        self._status_reserved = GameConstUtil.get_game_status("BIG_MAP")
                        self._ready_to_next_flag = True

        ##############################
        #Ground Attack Menu Message    
        ##############################
        elif self._game_control_phase == self.PH_GROUND_ATTACK:            
            #Determine the countries which you can attack.
            bordering_countires = []
            for n in range(len(countries)):
                if countries[n]["CONQUERED_BY"] == country["COUNTRY_NUM"]:
                    bordering_countires += countries[n]["BORDERING_COUNTRIES"]
            
            bordering_countires.sort()
            target_countries = []
            for n in range(len(bordering_countires)):
                if bordering_countires[n] == 0 and not countries[0]["DEFEATED"] and not countries[0]["HUMAN_CONTROLLED"]: 
                    if 0 not in target_countries:
                        target_countries.append(0)
                if bordering_countires[n] == 1 and not countries[1]["DEFEATED"] and not countries[1]["HUMAN_CONTROLLED"]: 
                    if 1 not in target_countries:
                        target_countries.append(1)
                if bordering_countires[n] == 2 and not countries[2]["DEFEATED"] and not countries[2]["HUMAN_CONTROLLED"]: 
                    if 2 not in target_countries:
                        target_countries.append(2)
                if bordering_countires[n] == 3 and not countries[3]["DEFEATED"] and not countries[3]["HUMAN_CONTROLLED"]: 
                    if 3 not in target_countries:
                        target_countries.append(3)
            print "target_countries" 
            print target_countries
            msg = ""
            for n in range(len(target_countries)):
                print countries[n]["NAME"]
                msg += str(n) + ":" + countries[target_countries[n]]["NAME"] + " "
                    
            message_text = "To which country will you send your army (" + msg +  ", 99:Cancel)? " 
            self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
            screen.set_strategy_result(self._result)
            
            if game_state.get_keyinput_confirmed_flag():
                if len(game_state.get_keyinput_confirmed()) == 0:   #Just a CR without entering any number
                    message_text = "Hey!" 
                    self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("ERROR")}
                    screen.set_strategy_result(self._result)
                    self._wait_flag = True
                else:    
                    input_value = int(game_state.get_keyinput_confirmed())
                    #0:Cancel
                    if input_value == 99:
                        self._game_control_phase = self.PH_NORMAL
                    #Valid Input
                    elif input_value in target_countries:
                        self._game_control_phase = self.PH_NORMAL
                        message_text = "Action station! Action station! March to the glory!" 
                        self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
                        screen.set_strategy_result(self._result)                        
                        self._wait_flag = True
                        self._status_reserved = GameConstUtil.get_game_status("BIG_MAP")
                        self._ready_to_next_flag = True

        ##############################
        #Air Strike Menu Message    
        ##############################
        elif self._game_control_phase == self.PH_AIR_STRIKE:
            #Determine the countries which you can attack.

            target_countries = []
            for n in range(len(countries)):
                if not countries[n]["DEFEATED"] and not countries[n]["HUMAN_CONTROLLED"]: 
                        target_countries.append(n)

            print "target_countries" 
            print target_countries
            msg = ""
            for n in range(len(target_countries)):
                print countries[n]["NAME"]
                msg += str(n) + ":" + countries[target_countries[n]]["NAME"] + " "
                    
            message_text = "Which country will you bombard (" + msg +  ", 99:Cancel)? " 
            self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
            screen.set_strategy_result(self._result)
            
            if game_state.get_keyinput_confirmed_flag():
                if len(game_state.get_keyinput_confirmed()) == 0:   #Just a CR without entering any number
                    message_text = "Hey!" 
                    self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("ERROR")}
                    screen.set_strategy_result(self._result)
                    self._wait_flag = True
                else:    
                    input_value = int(game_state.get_keyinput_confirmed())
                    #0:Cancel
                    if input_value == 99:
                        self._game_control_phase = self.PH_NORMAL
                    #Valid Input
                    elif input_value in target_countries:
                        self._game_control_phase = self.PH_NORMAL
                        message_text = "Roger! Take off!" 
                        self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
                        screen.set_strategy_result(self._result)                        
                        self._wait_flag = True
                        self._status_reserved = GameConstUtil.get_game_status("BIG_MAP")
                        self._ready_to_next_flag = True

        ##############################
        #ICBM Menu Message    
        ##############################
        elif self._game_control_phase == self.PH_ICBM:
            #Determine the countries which you can attack.

            target_countries = []
            for n in range(len(countries)):
                if not countries[n]["DEFEATED"] and not countries[n]["HUMAN_CONTROLLED"]: 
                        target_countries.append(n)

            print "target_countries" 
            print target_countries
            msg = ""
            for n in range(len(target_countries)):
                print countries[n]["NAME"]
                msg += str(n) + ":" + countries[target_countries[n]]["NAME"] + " "
                    
            message_text = "Which country will you destroy with the ICBM (" + msg +  ", 99:Cancel)? " 
            self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
            screen.set_strategy_result(self._result)
            
            if game_state.get_keyinput_confirmed_flag():
                if len(game_state.get_keyinput_confirmed()) == 0:   #Just a CR without entering any number
                    message_text = "Hey!" 
                    self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("ERROR")}
                    screen.set_strategy_result(self._result)
                    self._wait_flag = True
                else:    
                    input_value = int(game_state.get_keyinput_confirmed())
                    #0:Cancel
                    if input_value == 99:
                        self._game_control_phase = self.PH_NORMAL
                    #Valid Input
                    elif input_value in target_countries:
                        self._game_control_phase = self.PH_NORMAL
                        message_text = "Oh... The lethal weapon is going to be launched!" 
                        self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
                        screen.set_strategy_result(self._result)                        
                        self._wait_flag = True
                        self._status_reserved = GameConstUtil.get_game_status("BIG_MAP")
                        self._ready_to_next_flag = True

        ##############################
        #Spy Menu Message    
        ##############################
        elif self._game_control_phase == self.PH_SPY:
            #Spying costs money.
            if country["MONEY"] < GameConstUtil.get_cost("SPY"):
                message_text = "You don't have enough moeny to spy!" 
                self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("ERROR")}
                screen.set_strategy_result(self._result)
                self._wait_flag = True
            else:    
                #Determine the countries which you can spy
                target_countries = []
                for n in range(len(countries)):
                    if not countries[n]["DEFEATED"] and not countries[n]["HUMAN_CONTROLLED"]: 
                            target_countries.append(n)
    
                print target_countries
                msg = ""
                for n in range(len(target_countries)):
                    msg += str(n) + ":" + countries[target_countries[n]]["NAME"] + " "
                        
                message_text = "Which country will you have your spy infiltrate  (" + msg +  ", 99:Cancel)? " 
                self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
                screen.set_strategy_result(self._result)
                
                if game_state.get_keyinput_confirmed_flag():
                    if len(game_state.get_keyinput_confirmed()) == 0:   #Just a CR without entering any number
                        message_text = "Hey!" 
                        self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("ERROR")}
                        screen.set_strategy_result(self._result)
                        self._wait_flag = True
                    else:    
                        input_value = int(game_state.get_keyinput_confirmed())
                        #0:Cancel
                        if input_value == 99:
                            self._game_control_phase = self.PH_NORMAL
                        #Valid Input
                        elif input_value in target_countries:
                            self._game_control_phase = self.PH_NORMAL
                            
                            #Check if Spying is successful
                            i = random.randint(0, 2) % 2
                            if i == 0: #success                            
                                message_text = "Mission Complete!" 
                                self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
                                screen.set_strategy_result(self._result)                        
                                self._wait_flag = True
                                
                                #To change to Spy screen, set the game status directly without incrementing turn.    
                                game_state.set_spied_country(countries[target_countries[input_value]])
                                game_state.set_status(GameConstUtil.get_game_status("STRATEGY_SPY"))
                            else:
                                message_text = "Mission Incomplete! Our agent was caught!" 
                                self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("ERROR")}
                                screen.set_strategy_result(self._result)
                                self._wait_flag = True
                            
                            country["MONEY"] -= GameConstUtil.get_cost("SPY")
                            
       ##############################
        #Sell Oil Menu Message    
        ##############################
        elif self._game_control_phase == self.PH_SELL_OIL:
            message_text = "How much will you sell (0-" + str(country["OIL"]) + ", 0:Cancel)? " 
            self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
            screen.set_strategy_result(self._result)
            
            if game_state.get_keyinput_confirmed_flag():
                if len(game_state.get_keyinput_confirmed()) == 0:   #Just a CR without entering any number
                    message_text = "Hey!" 
                    self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("ERROR")}
                    screen.set_strategy_result(self._result)
                    self._wait_flag = True
                else:    
                    input_value = int(game_state.get_keyinput_confirmed())
                    #0:Cancel
                    if input_value == 0:
                        self._game_control_phase = self.PH_NORMAL
                    #Valid Input
                    elif input_value <= int(country["OIL"]):
                        country["OIL"] -= input_value
                        country["MONEY"] += int(round(game_state.get_oil_exchg_rate() * input_value, 0))

                        self._game_control_phase = self.PH_NORMAL
                        message_text = "Good gain!" 
                        self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
                        screen.set_strategy_result(self._result)                        
                        self._wait_flag = True
                        self._status_reserved = GameConstUtil.get_game_status("BIG_MAP")
                        self._ready_to_next_flag = True

        ##############################
        #Placing Oil Derrick Menu Message    
        ##############################
        elif self._game_control_phase == self.PH_OIL_DERRICK:
            country_map = country["COUNTRY_MAP"]
            
            #When you can place an oil derrick
            if country_map.get_num_of_active_oil_derrick() < GameConstUtil.get_num_of_oil_derrick():
                #print "###: # of derrick: %d" % country_map.get_num_of_active_oil_derrick()
                message_text =  "Where will you place an oil derrick (xy)?\n" + \
                                "(Remaining: " + str(GameConstUtil.get_num_of_oil_derrick() - country_map.get_num_of_active_oil_derrick()) + ")"
        
                self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
                screen.set_strategy_result(self._result)   
    
                if game_state.get_keyinput_confirmed_flag():
                    key_input = game_state.get_keyinput_confirmed()
                    if len(key_input) != 2:
                        message_text = "You cannot place it there!"
                        self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("ERROR")}
                        screen.set_strategy_result(self._result)
                        self._wait_flag = True 
                    else:
                        x = int(key_input[0])
                        y = int(key_input[1])
                        if x >= GameConstUtil.get_map_size() or y >= GameConstUtil.get_map_size():
                            message_text = "You cannot place it there!"
                            self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("ERROR")}
                            screen.set_strategy_result(self._result)                            
                            self._wait_flag = True 
                        elif (country_map.get_occupying_object_type(x, y) == GameConstUtil.get_game_object("FLATLAND") or country_map.get_occupying_object_type(x, y) == GameConstUtil.get_game_object("HIDDEN_OIL_WELL")):
                            oil_derrick = MapObject(GameConstUtil.get_game_object("OIL_DERRICK_IN_SEARCH"))
                            oil_derrick.set_locx(x)
                            oil_derrick.set_locy(y)
                            country_map.remove_map_object(x, y)
                            country_map.get_map_objects().append(oil_derrick)
                            #print "###APPEND SUCCESS!"
            #When you have sufficient number of oil derricks
            else:
                self._game_control_phase = self.PH_NORMAL
                #print "Status Reserved: %d" % self._status_reserved
                #game_state.set_status(self._status_reserved)
                self._ready_to_next_flag = True
                #print "here"
                #self._increment_turn(game_state)            

class StrategySpyController(GameController):
    
    #GAME_CONTROL_PHASE
    PH_NORMAL = (0)
    
    def __init__(self):
        GameController.__init__(self)
        self._game_control_phase = self.PH_NORMAL
        self._result = {"MESSAGE":"", "RESULT":GameConstUtil.get_game_event("NORMAL")}
        self._status_reserved = GameConstUtil.get_game_status("STRATEGY_EXEC") 
        self._wait_flag = False
        self._ready_to_next_flag = False
        #self._game_status = GameConstUtil.get_game_status("STRATEGY_EXEC")

    def _increment_turn(self, game_state):

        if self._ready_to_next_flag:
            self._ready_to_next_flag = False
            game_state.set_status(self._status_reserved)
             
    def control_scene(self, screen, game_state):

        #if self._result["RESULT"] == GameConstUtil.get_game_event("ERROR"):
        if self._wait_flag:
            pygame.time.wait(GameConstUtil.get_wait_millisec())
        
        self._increment_turn(game_state)

        if self._game_control_phase == self.PH_NORMAL:
            message_text = "Here is the confidential report about this country. Do you want to return (1=Yes)? "   
            self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("NORMAL")}
            screen.set_strategy_result(self._result)
            
            if game_state.get_keyinput_confirmed_flag():
                #1:Return
                if game_state.get_keyinput_confirmed() == str(1):
                    self._game_control_phase = self.PH_NORMAL
                    self._status_reserved = GameConstUtil.get_game_status("STRATEGY_EXEC")
                    self._ready_to_next_flag = True
                else:
                    message_text = "Hey!" 
                    self._result = {"MESSAGE": message_text, "RESULT":GameConstUtil.get_game_event("ERROR")}
                    self._wait_flag = True
                    screen.set_strategy_result(self._result)

class StrategyCommand():
    def __init__(self):
        pass
    
    def improve_support_rate(self, game_state):
        country = game_state.get_countries()[game_state.get_turn()]
        
        country["SUPPORT_RATE"] += random.randint(4, 7) 
        print country["SUPPORT_RATE"]
        
    def change_tax_rate(self, game_state, new_rate):
        country = game_state.get_countries()[game_state.get_turn()]
        old_rate = country["TAX_RATE"]
        country["TAX_RATE"] = new_rate
        
        new_support_rate = country["SUPPORT_RATE"] - int(round((new_rate - old_rate) * 0.7 * random.uniform(1, 2), 0))
        if new_support_rate < 0:
            new_support_rate = 0
            
        country["SUPPORT_RATE"] = new_support_rate
        