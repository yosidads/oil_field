# coding: utf-8

from pygame.locals import * 

class GameConstUtil():

    @classmethod
    def get_game_title(cls):        
        return "THE OIL FIELD"

    @classmethod
    def get_game_status(cls, status):        
        game_status_dic = {"START":0, "BIG_MAP":1, "STRATEGY_EXEC":2, "STRATEGY_SPY":3 \
                           , "WAR_EXEC":4, "BIG_MAP_ICBM":5, "BIG_MAP_WAR":6, "BIG_MAP_ELECTION":7 \
                           , "STRATEGY_OIL_DERRICK":8, "GLORIOUS_ENDING":9, "GAMEOVER":10}
        
        return game_status_dic[status]

    @classmethod
    def get_game_event(cls, event):        
        game_event_dic = {"NORMAL":0, "WAR_OUTBREAK":1, "OIL_FOUND":2, "COUP_OUTBREAK":3 \
                           , "ICBM_LAUNCH":4, "PLAYER_TURN":5, "ERROR":6, "ELECTION":7}
        
        return game_event_dic[event]            
   
    @classmethod
    def get_game_object(cls, obj_type):        
        game_object_dic = {"FLATLAND":0, "CAPITAL":1, "CAPITAL_DESTROYED":2, "OIL_DERRICK_IN_SEARCH":3 \
                           , "OIL_DERRICK_ACTIVE":4, "OIL_DERRICK_DEAD":5, "OIL_DERRICK_DESTROYED":6, "MY_ARMY":7 \
                           , "ENEMY":8, "HIDDEN_OIL_WELL":9}
        
        return game_object_dic[obj_type]            
    
    #game settings
    #WAIT_MILLISEC = 100
    #@classmethod
    #def get_wait_millisec(cls):        
    #    return 100

    @classmethod
    def get_wait_millisec(cls, type_desc):        
        millsec_type_dic = {"NORMAL": 100, "ELECTION": 1000}
        return millsec_type_dic[type_desc]

    #SCR_RECT = Rect(0, 0, 640, 480)
    @classmethod
    def get_scr_rect(cls):        
        return Rect(0, 0, 640, 480)

    #SCR_MAP_X, SCR_MAP_Y = (40, 40)
    @classmethod
    def get_scr_map_x(cls):        
        return 40
    @classmethod
    def get_scr_map_y(cls):        
        return 40

    #SPRITE_SIZE = 32
    @classmethod
    def get_sprite_size(cls):        
        return 32
 
    #MAP_SIZE = 9
    @classmethod
    def get_map_size(cls):        
        return 9

    @classmethod
    def get_color(cls, color_desc):        
        game_color_dic = {"BLACK":(0, 0, 0), "WHITE":(255, 255, 255), "BLUE":(0, 0, 255), "GREEN":(0, 255, 0) \
                           , "RED":(255, 0, 0), "YELLOW":(255, 255, 0), "PURPLE":(255, 0, 255), "CYAN":(0, 255, 255)}
        
        return game_color_dic[color_desc]            
   
    #GAME_START_YEAR = 2021
    @classmethod
    def get_game_start_year(cls):        
        return 2021
    #GAME_OVER_YEAR = 2030
    @classmethod
    def get_game_over_year(cls):        
        return 2030
    
    #NUM_OF_OIL_DERRICK = 3
    @classmethod
    def get_num_of_oil_derrick(cls):        
        return 3

    @classmethod
    def get_cost(cls, activity_desc):        
        game_cost_dic = {"SPY": 5}
        
        return game_cost_dic[activity_desc]            
