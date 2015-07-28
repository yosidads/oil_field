# coding: utf-8

from gameutil import *
import pygame
import random

class GameState:    

    ############################################################################
    # Private methods
    ############################################################################

    def __init__(self):
        
        self._status = GameConstUtil.get_game_status("START")

        #Sound related
        self._load_sounds()
        self._sound_to_play = None
        
        #Key input related
        self._keyinput = ""
        self._keyinput_confirmed = ""
        self._keyinput_confirmed_flag = False
        
        #Game conditions related
        self._game_date = {"YEAR":GameConstUtil.get_game_start_year(), "SEASON":0}
        self._election_date = {"YEAR":GameConstUtil.get_game_start_year() + 1, "SEASON":2}
        self._init_countries()
        self._init_rate()

    def _load_sounds(self):
        self._sounds = {"BEEP": pygame.mixer.Sound("./sound/beep.wav") \
                       , "BOMB": pygame.mixer.Sound("./sound/bomb.wav")}
               
    def _init_countries(self):
        country_0 = {"NAME":"Cucumbania", "COLOR":GameConstUtil.get_color("GREEN"), "DEFEATED":False, "HUMAN_CONTROLLED":False, "COUNTRY_NUM": 0, "CONQUERED_BY": 0, "BORDERING_COUNTRIES":[1, 2, 3]}
        country_1 = {"NAME":"Whalystan", "COLOR":GameConstUtil.get_color("CYAN"), "DEFEATED":False, "HUMAN_CONTROLLED":False, "COUNTRY_NUM": 1, "CONQUERED_BY": 1, "BORDERING_COUNTRIES":[0, 2]}
        country_2 = {"NAME":"Pinkzamia", "COLOR":GameConstUtil.get_color("PURPLE"), "DEFEATED":False, "HUMAN_CONTROLLED":False, "COUNTRY_NUM": 2, "CONQUERED_BY": 2, "BORDERING_COUNTRIES":[0, 1, 3]}
        country_3 = {"NAME":"Pikaland", "COLOR":GameConstUtil.get_color("YELLOW"), "DEFEATED":False, "HUMAN_CONTROLLED":False, "COUNTRY_NUM": 3, "CONQUERED_BY": 3, "BORDERING_COUNTRIES":[0, 2]}
        self.countries = [country_0, country_1, country_2, country_3]
        
        #Select a country controlled by the player.
        player_country = random.randint(0, len(self.countries) - 1)
        self.countries[player_country]["HUMAN_CONTROLLED"] = True
        #print "player_country= %d" % player_country
        
        #Set turn so that a human-played country takes turns at the last. 
        if player_country == len(self.countries) - 1:
            self._turn = 0
        else:
            self._turn = player_country + 1        
        
        for n in range(len(self.countries)):
            self._init_nation_resources(self.countries[n]) 
        #print "###: _init_countries: COMPLETED"  
          
    def _init_nation_resources(self, country):

        country_Map = CountryMap()
        country_Map.init_nation()
        country["COUNTRY_MAP"] = country_Map
        
        if country["HUMAN_CONTROLLED"] == True:
            country["SUPPORT_RATE"] = random.randint(40, 55)
            country["MONEY"] = random.randint(100, 200)
            country["OIL"] = random.randint(5, 10)
            country["COUNTRY_MAP"].get_capital().set_defense(random.randint(30, 50))
            country["ARMY"] = random.randint(20, 30)
            country["PLANE"] = random.randint(5, 10)
        else:
            country["SUPPORT_RATE"] = random.randint(45, 60)
            country["MONEY"] = random.randint(200, 250)
            country["OIL"] = random.randint(15, 20)
            country["COUNTRY_MAP"].get_capital().set_defense(random.randint(50, 60))
            country["ARMY"] = random.randint(30, 40)
            country["PLANE"] = random.randint(8, 12)
        
        country["TAX_RATE"] = 20
        country["ICBM"] = 0
    
    def _init_rate(self):
        self._oil_exchg_rate = 1.0
        self._plane_price = 200
        self._icbm_price = 3000        
        self._set_rate()
        
    def _set_rate(self):
        self._oil_exchg_rate = round(self._oil_exchg_rate * random.uniform(0.7, 1.4), 1)
        if self._oil_exchg_rate < 0.3:
            self._oil_exchg_rate = 0.3
        elif self._oil_exchg_rate > 4:
            self._oil_exchg_rate = 4
        
        self._plane_price = int(self._plane_price * random.uniform(0.7, 1.4))
        if self._plane_price < 100:
            self._plane_price = 100
        elif self._plane_price > 300:
            self._plane_price = 300

        self._icbm_price = int(self._icbm_price * random.uniform(0.7, 1.4))
        if self._icbm_price < 2000:
            self._icbm_price = 2000
        elif self._icbm_price > 4000:
            self._icbm_price = 4000
    
    def _increment_game_date(self):
        self._game_date["SEASON"] += 1
        if self._game_date["SEASON"] > 3:
            self._update_nation_resources()
            self._game_date["YEAR"] += 1
            self._game_date["SEASON"] = 0
    
    def _update_nation_resources(self):
        pass
    
    ############################################################################
    # Public methods
    ############################################################################
    
    def set_status(self, status):
        self._status = status    
    
    def get_status(self):
        return self._status
    
    def get_game_date(self):
        return self._game_date
 
    def get_election_date(self):
        return self._election_date
    
    def set_countries(self, countries):
        self.countries = countries
        
    def get_countries(self):
        return self.countries    
    
    def increment_turn(self):
        if self.countries[self._turn]["HUMAN_CONTROLLED"]:
            self._increment_game_date()
            self._set_rate()
        
        # Decides the next turn#. Fixed Turn# is assigned in each country.
        while True:
            self._turn += 1
            if self._turn > len(self.countries) - 1:
                self._turn = 0
            #If the country is already defeated, skip it
            if self.countries[self._turn]["DEFEATED"] == False:
                break 
        
    def get_turn(self):
        return self._turn
    
    def get_oil_exchg_rate(self):
        return self._oil_exchg_rate

    def get_plane_price(self):
        return self._plane_price
    
    def get_icbm_price(self):
        return self._icbm_price
    
    def get_sounds(self):
        return self._sounds
    
    def set_sound_to_play(self, sound_to_play):
        self._sound_to_play = sound_to_play
        
    def get_sound_to_play(self):
        return self._sound_to_play
    
    ############################
    # Key input-related
    ############################
    def set_keyinput(self, keyinput):
        self._keyinput = "? " + keyinput
    
    def get_keyinput(self):
        return self._keyinput

    def set_keyinput_confirmed(self, keyinput):
        self._keyinput_confirmed = keyinput
    
    def get_keyinput_confirmed(self):
        return self._keyinput_confirmed

    def set_keyinput_confirmed_flag(self, flag_value):
        self._keyinput_confirmed_flag = flag_value
    
    def get_keyinput_confirmed_flag(self):
        return self._keyinput_confirmed_flag

class MapObject:
    '''
    Represents an object on a country map such as Capital, HiddenOilWell, etc.
    '''
    def __init__(self, object_type):
        self._object_type = object_type
        self._locx = 0
        self._locy = 0
        self._active_flag = True
        self._object_state = None
        self._defense = 50 #by default
        self._proven_reserves = 0 #by default
            
    def get_object_type(self):
        return self._object_type
        
    def set_locx(self, locx):
        self._locx = locx
    
    def get_locx(self):
        return self._locx    
    
    def set_locy(self, locy):
        self._locy = locy
    
    def get_locy(self):
        return self._locy    

    def set_defense(self, defense):
        self._defense = defense
    
    def get_defense(self):
        return self._defense

    def set_active_flag(self, active_flag):
        self._active_flag = active_flag
    
    def get_active_flag(self):
        return self._active_flag
    
    def set_object_state(self, object_state):
        self._object_state = object_state
    
    def get_object_state(self):
        return self._object_state
    
    def set_proven_reserves(self, qty):
        self._proven_reserves = qty
    
    def get_proven_reserves(self):
        return self._proven_reserves

class CountryMap:
    '''
    Represents a country whole map.
    '''
    def __init__(self):
        self._map_objects = []

    def get_occupying_object_type(self, x, y):
        for n in range(len(self._map_objects)):
            map_object = self._map_objects[n]
            if map_object.get_locx() == x and map_object.get_locy() == y:
                return map_object.get_object_type()
        
        return GameConstUtil.get_game_object("FLATLAND")

    def get_occupying_map_object(self, x, y):
        for n in range(len(self._map_objects)):
            map_object = self._map_objects[n]
            if map_object.get_locx() == x and map_object.get_locy() == y:
                return map_object

    def init_nation(self):
        #Capital
        capital = MapObject(GameConstUtil.get_game_object("CAPITAL"))
        capital.set_locx(random.randint(1, 7))
        capital.set_locy(random.randint(4, 7))
        self._map_objects.append(capital)
        
        #Hidden Oil Well
        n = 0
        while n < 5:
            hidden_oil_well = MapObject(GameConstUtil.get_game_object("HIDDEN_OIL_WELL"))
            x = random.randint(0, 8)
            y = random.randint(0, 8)
            if self.get_occupying_object_type(x, y) != GameConstUtil.get_game_object("CAPITAL") and self.get_occupying_object_type(x, y) != GameConstUtil.get_game_object("HIDDEN_OIL_WELL"):
                hidden_oil_well.set_locx(x)
                hidden_oil_well.set_locy(y)
                self._map_objects.append(hidden_oil_well)
                n += 1
            
    def get_capital(self):
        for n in range(len(self._map_objects)):
            map_object = self._map_objects[n]
            if map_object.get_object_type() == GameConstUtil.get_game_object("CAPITAL"):
                return map_object
        print "###get_capital: Capital was not found."

    def get_num_of_active_oil_derrick(self):
        num = 0
        for n in range(len(self._map_objects)):
            map_object = self._map_objects[n]
            if map_object.get_object_type() == GameConstUtil.get_game_object("OIL_DERRICK_ACTIVE") \
                or map_object.get_object_type() == GameConstUtil.get_game_object("OIL_DERRICK_IN_SEARCH"):
                #print "###get_num_of_active_oil_derrick"
                num += 1
        
        return num

    def get_map_objects(self):
        return self._map_objects
    
    def remove_map_object(self, x, y):
        for n in range(len(self._map_objects)):
            map_object = self._map_objects[n]
            if map_object.get_locx() == x and map_object.get_locy() == y:
                del self._map_objects[n]
                break
        
    