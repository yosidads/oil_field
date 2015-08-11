# coding: utf-8

from pygame.locals import *
from lib.word_wrapped_text_display_module import *
from gamesprite import *
from gameutil import *

class GameScreen:
    
    def __init__(self):
        self._strategy_result = {"MESSAGE": "", "RESULT": GameConstUtil.get_game_event("NORMAL")}
    
    def draw(self, screen, game_state):
        pass
    
    def set_strategy_result(self, result):
        self._strategy_result = result
        
    def get_strategy_result(self):
        return self._strategy_result
    
class StartScreen(GameScreen):
    
    def draw(self, screen, game_state):
        #TITLE
        title_font = pygame.font.SysFont(None, 80)
        title = title_font.render(GameConstUtil.get_game_title(), False, GameConstUtil.get_color("YELLOW"))
        screen.blit(title, ((GameConstUtil.get_scr_rect().width-title.get_width())/2, 100))
        #PUSH START
        push_font = pygame.font.SysFont(None, 40)
        push_space = push_font.render("PUSH SPACE KEY", False, GameConstUtil.get_color("WHITE"))
        screen.blit(push_space, ((GameConstUtil.get_scr_rect().width-push_space.get_width())/2, 250))
        #CREDIT
        credit_font = pygame.font.SysFont(None, 20)
        credit = credit_font.render("Programmed by Daisuke Y. in 2015", False, GameConstUtil.get_color("WHITE"))
        screen.blit(credit, ((GameConstUtil.get_scr_rect().width-credit.get_width())/2, 320))
        #SPECIAL THANKS TO
        special_thanks_font = pygame.font.SysFont(None, 20)
        special_thanks = credit_font.render("Special Thanks To:", False, GameConstUtil.get_color("CYAN"))
        screen.blit(special_thanks, ((GameConstUtil.get_scr_rect().width-special_thanks.get_width())/2, 350))

        sp_thanks_to_txt = "Somebody who taught me this game 30yrs ago\n"
                            #"Z.Yoshida\n" \
                            #"J.M.Yoshida"
        sp_thanks_to_font = pygame.font.SysFont(None, 20)                    
        sp_thanks_to_rect = pygame.Rect((0, 0, 320, 80))
        sp_thanks_to_rendered_text = \
                render_textrect(sp_thanks_to_txt, sp_thanks_to_font, sp_thanks_to_rect, GameConstUtil.get_color("CYAN"), GameConstUtil.get_color("BLACK"), 1)        
        screen.blit(sp_thanks_to_rendered_text, ((GameConstUtil.get_scr_rect().width-sp_thanks_to_rendered_text.get_width())/2, 365))   
        
        #special_thanks_zy_font = gamesprite.font.SysFont(None, 20)
        #special_thanks_zy = credit_font.render("Z.Yoshida", False, GameConstUtil.get_color("WHITE"))
        #screen.blit(special_thanks_zy, ((GameConstUtil.get_scr_rect().width-special_thanks_zy.get_width())/2, 380))
        #special_thanks_jy_font = gamesprite.font.SysFont(None, 20)
        #special_thanks_jy = credit_font.render("J.M.Yoshida", False, GameConstUtil.get_color("WHITE"))
        #screen.blit(special_thanks_jy, ((GameConstUtil.get_scr_rect().width-special_thanks_jy.get_width())/2, 410))

class GloriousEndingScreen(GameScreen):
    def draw(self, screen, game_state):
        pass
    
class GaveOverScreen(GameScreen):
    
    def draw(self, screen, game_state):
        pass
            
class BigMapScreen(GameScreen):
    def __init__(self):
        GameScreen.__init__(self)

        self._strategy_acceptable_flag = True
        #self._ready_to_next_flag = False
                
        self._sprite_capitals = []
        for n in range(4):
            sprite = Capital()
            self._sprite_capitals.append(sprite)
        
        self._init_narration()

    def _init_narration(self):
        self._current_narration_line = 0
        self._narration_msgs = []
                    
    def _draw_backdrop(self, screen, game_state):
        ########################################################################
        #Date Header
        ########################################################################
        if (game_state.get_game_date())["SEASON"] == 0:
            season_str = "Spring"
        elif (game_state.get_game_date())["SEASON"] == 1:
            season_str = "Summer"
        elif (game_state.get_game_date())["SEASON"] == 2:
            season_str = "Fall"
        elif (game_state.get_game_date())["SEASON"] == 3:
            season_str = "Winter"
            
        game_date_font = pygame.font.SysFont(None, 20)
        game_date_space = game_date_font.render("YEAR: " + str((game_state.get_game_date())["YEAR"]) \
                                                + " " + season_str, False, GameConstUtil.get_color("WHITE"))
        screen.blit(game_date_space, (40, 40))

        ########################################################################
        #Election Information Header
        ########################################################################
        election_date_font = pygame.font.SysFont(None, 20)
        if (game_state.get_election_date())["YEAR"] >= GameConstUtil.get_game_over_year() \
                and (game_state.get_game_date())["YEAR"] != GameConstUtil.get_game_over_year():
            election_msg = "Your tenure is over in the next election! You have to step down."
        elif (game_state.get_election_date())["YEAR"] >= GameConstUtil.get_game_over_year() \
                and (game_state.get_game_date())["YEAR"] == GameConstUtil.get_game_over_year():
            election_msg = "This is the last year!"
        else:
            election_msg = "Next election is held in " + str((game_state.get_election_date())["YEAR"]) + " Fall."
        
        election_date_space = election_date_font.render(election_msg, False, GameConstUtil.get_color("RED")) 
        screen.blit(election_date_space, (200, 40))

        ########################################################################
        #Countries            
        ########################################################################
        countries = game_state.get_countries()
        #Country:#0
        pygame.draw.lines(screen, countries[0]["COLOR"], True, [(70, 110), (80, 120), (280, 90), (500, 120), (600, 190), (320, 200), (60, 150)], 2)
        country0_font = pygame.font.SysFont(None, 20)
        country0_space = country0_font.render(countries[0]["NAME"], False, GameConstUtil.get_color("BLACK"), countries[0]["COLOR"])
        screen.blit(country0_space, (250, 120))
        
        capital0 = self._sprite_capitals[0]
        capital0.update(290, 140)
        capital0.draw(screen)
        #print "###sprite_capital.draw x=%d y=%d " % (capital0.get_locx(), capital0.get_locy())             
        #Country:#1
        pygame.draw.lines(screen, countries[1]["COLOR"], True, [(463, 198), (600, 193), (510, 260), (393, 240)], 2)
        country1_font = pygame.font.SysFont(None, 20)
        country1_space = country1_font.render(countries[1]["NAME"], False, GameConstUtil.get_color("BLACK"), countries[1]["COLOR"])
        screen.blit(country1_space, (510, 220))
        capital1 = self._sprite_capitals[1]
        capital1.update(470, 210)
        capital1.draw(screen)
        #Country:#2
        pygame.draw.lines(screen, countries[2]["COLOR"], True, [(190, 178), (320, 203), (460, 198), (390, 240), (480, 290), (320, 250), (300, 280)], 2)
        country2_font = pygame.font.SysFont(None, 20)
        country2_space = country2_font.render(countries[2]["NAME"], False, GameConstUtil.get_color("BLACK"), countries[2]["COLOR"])
        screen.blit(country2_space, (300, 230))
        capital2 = self._sprite_capitals[2]
        capital2.update(260, 200)
        capital2.draw(screen)
        #Country:#3
        pygame.draw.lines(screen, countries[3]["COLOR"], True, [(60, 153), (185, 178), (295, 280), (120, 300), (40, 250)], 2)
        country3_font = pygame.font.SysFont(None, 20)
        country3_space = country3_font.render(countries[3]["NAME"], False, GameConstUtil.get_color("BLACK"), countries[3]["COLOR"])
        screen.blit(country3_space, (80, 240))
        capital3 = self._sprite_capitals[3]
        capital3.update(80, 200)
        capital3.draw(screen)
        
    def _draw_message_screen(self, screen, game_state):
        ########################################################################
        #Narration            
        ########################################################################
        
        #Display Country Name
        countries = game_state.get_countries()

        country_name = "[" + countries[game_state.get_turn()]["NAME"] + "]"
        country_font = pygame.font.SysFont(None, 20)
        country_space = country_font.render(country_name, False, countries[game_state.get_turn()]["COLOR"])
        screen.blit(country_space, (40, 320))          
        
        #Narration        
        msg_color = GameConstUtil.get_color("WHITE")    
        
        if self._strategy_acceptable_flag:
            pygame.time.wait(GameConstUtil.get_wait_millisec("NORMAL"))
 
            result = self._strategy_result
            if result["RESULT"] == GameConstUtil.get_game_event("NORMAL"):
                msg_color = GameConstUtil.get_color("WHITE")
                game_state.set_sound_to_play(game_state.get_sounds()["BEEP"])
                game_state.set_screen_message_wait(GameConstUtil.get_wait_millisec("NORMAL"))
            elif result["RESULT"] == GameConstUtil.get_game_event("PLAYER_TURN"):
                msg_color = GameConstUtil.get_color("CYAN")
                game_state.set_sound_to_play(game_state.get_sounds()["BEEP"])
                game_state.set_screen_message_wait(GameConstUtil.get_wait_millisec("NORMAL"))
            elif result["RESULT"] == GameConstUtil.get_game_event("ELECTION"):
                msg_color = GameConstUtil.get_color("CYAN")
                game_state.set_sound_to_play(game_state.get_sounds()["BEEP"])
                game_state.set_screen_message_wait(GameConstUtil.get_wait_millisec("ELECTION"))
            else:
                msg_color = GameConstUtil.get_color("RED")
             
            #No more strategy is acceptable and not ready to next until the message is fully populated.   
            self._strategy_acceptable_flag = False
            #self._ready_to_next_flag = False
            
            self._narration_msgs = result["MESSAGE"].split("\n")  
              
            msg_str = ""
        else:
            game_state.set_sound_to_play(None)     
            msg_str = ""
            for n in range(self._current_narration_line + 1):
                msg_str += self._narration_msgs[n]
                msg_str += "\n"
                
            self._current_narration_line += 1    
            
        msg_rect = pygame.Rect((0, 0, 400, 150))
        msg_font = pygame.font.SysFont(None, 20)
        rendered_text = render_textrect(msg_str, msg_font, msg_rect, msg_color, GameConstUtil.get_color("BLACK"), 0)
            
        screen.blit(rendered_text, (180, 320))          
        pygame.time.wait(game_state.get_screen_message_wait())
        
        if self._current_narration_line >= len(self._narration_msgs):       
            self._init_narration()
            #ready to accept more message.
            self._strategy_acceptable_flag = True
            #self._ready_to_next_flag = True
    
    ############################################################################
    # Public methods            
    ############################################################################
    def set_strategy_acceptable_flag(self, flag_value):
        self._strategy_acceptable_flag = flag_value
        
    def get_strategy_acceptable_flag(self):
        return self._strategy_acceptable_flag
    
    #def set_ready_to_next_flag(self, flag_value):
    #    self._ready_to_next_flag = flag_value
        
    #def get_ready_to_next_flag(self):
    #    return self._ready_to_next_flag
 
    def draw(self, screen, game_state):
        self._draw_backdrop(screen, game_state)
        self._draw_message_screen(screen, game_state)

class BigMapIcbmScreen(BigMapScreen):
    
    def _draw_message_screen(self, screen, game_state):
        pass

class BigMapWarScreen(BigMapScreen):
    
    def _draw_message_screen(self, screen, game_state):
        pass

class BigMapElectionScreen(BigMapScreen):
    
    def _draw_message_screen(self, screen, game_state):
        pass
        
class StrategyExecScreen(GameScreen):
    def __init__(self):
        GameScreen.__init__(self)
        self._sprite_capital = Capital()
        self._sprite_oil_derrick_in_search = []
        for n in range(GameConstUtil.get_num_of_oil_derrick()):
            sprite = OilDerrickInSearch()
            self._sprite_oil_derrick_in_search.append(sprite)
        self._sprite_oil_derrick_in_search_idx = 0
        
    def _draw_backdrop(self, screen, game_state, country):
        for n in range(GameConstUtil.get_map_size() + 1): 
            #Horizontal Line
            pygame.draw.line(screen, GameConstUtil.get_color("WHITE"), (GameConstUtil.get_scr_map_x(), GameConstUtil.get_scr_map_y() + (GameConstUtil.get_sprite_size()+2) * n), \
                                                                        (GameConstUtil.get_scr_map_x() + (GameConstUtil.get_sprite_size()+2) * GameConstUtil.get_map_size(), GameConstUtil.get_scr_map_y() + (GameConstUtil.get_sprite_size()+2) * n))
            #Vertical Line
            pygame.draw.line(screen, GameConstUtil.get_color("WHITE"), (GameConstUtil.get_scr_map_x() + (GameConstUtil.get_sprite_size()+2) * n, GameConstUtil.get_scr_map_y()), \
                                                                        (GameConstUtil.get_scr_map_x() + (GameConstUtil.get_sprite_size()+2) * n, GameConstUtil.get_scr_map_y() + (GameConstUtil.get_sprite_size()+2) * GameConstUtil.get_map_size()))
        
        for n in range(GameConstUtil.get_map_size()): 
            horizontal_num = str(n)
            horizontal_font = pygame.font.SysFont(None, 20)
            horizontal_space = horizontal_font.render(horizontal_num, False, GameConstUtil.get_color("WHITE"))
            screen.blit(horizontal_space, (GameConstUtil.get_scr_map_x() + 10 + (GameConstUtil.get_sprite_size()+2) * n, GameConstUtil.get_scr_map_y() - 10))         
        
        for n in range(GameConstUtil.get_map_size()): 
            vertical_num = str(n)
            vertical_font = pygame.font.SysFont(None, 20)
            vertical_space = vertical_font.render(vertical_num, False, GameConstUtil.get_color("WHITE"))
            screen.blit(vertical_space, (GameConstUtil.get_scr_map_x() - 10, GameConstUtil.get_scr_map_y() + 10 + (GameConstUtil.get_sprite_size()+2) * n))         
            
        #country = game_state.get_countries()[game_state.get_turn()]
        country_map = country["COUNTRY_MAP"]

        #Place objects. Add 1 pixel so that the object does not overwrite a vertical or a horizontal line 
        for n in range(GameConstUtil.get_map_size()):
            for m in range(GameConstUtil.get_map_size()):
                if country_map.get_occupying_object_type(n, m) == GameConstUtil.get_game_object("CAPITAL"):
                    map_object = country_map.get_occupying_map_object(n, m)
                    self._sprite_capital.update(GameConstUtil.get_scr_map_x() + (GameConstUtil.get_sprite_size()+2) * map_object.get_locx() + 1, GameConstUtil.get_scr_map_y() + (GameConstUtil.get_sprite_size()+2)  * map_object.get_locy() + 1)
                    self._sprite_capital.draw(screen)   
                    #print "###sprite_capital.draw x=%d y=%d " % (self._sprite_capital.get_locx(), self._sprite_capital.get_locy())

                if country_map.get_occupying_object_type(n, m) == GameConstUtil.get_game_object("OIL_DERRICK_IN_SEARCH"):
                    map_object = country_map.get_occupying_map_object(n, m)
                    sprite = self._sprite_oil_derrick_in_search[self._sprite_oil_derrick_in_search_idx]
                    sprite.update(GameConstUtil.get_scr_map_x() + (GameConstUtil.get_sprite_size()+2)  * map_object.get_locx() + 1, GameConstUtil.get_scr_map_y() + (GameConstUtil.get_sprite_size()+2) * map_object.get_locy() + 1)
                    sprite.draw(screen)
                    self._sprite_oil_derrick_in_search_idx += 1  
        
        self._sprite_oil_derrick_in_search_idx = 0            

    def _draw_info_screen(self, screen, game_state, country):
        #country = game_state.get_countries()[game_state.get_turn()]
        #print country["NAME"]
 
        country_name = "< " + country["NAME"] + " >"
        country_font = pygame.font.SysFont(None, 20)
        country_space = country_font.render(country_name, False, country["COLOR"])
        screen.blit(country_space, (360, 20))         
        
        #Oil Derrick
        country_map = country["COUNTRY_MAP"]
        oil_derrick_info = ""
        oil_derrick_info2 = ""
        i = 0
        if country_map.get_num_of_active_oil_derrick() > 0:
            map_objects = country_map.get_map_objects()
            for n in range(len(map_objects)):
                map_object = map_objects[n]
                if map_object.get_object_type() == GameConstUtil.get_game_object("OIL_DERRICK_ACTIVE") \
                    or map_object.get_object_type() == GameConstUtil.get_game_object("OIL_DERRICK_IN_SEARCH"):
                    reserved_qty = str(map_object.get_proven_reserved()) if map_object.get_object_type() == GameConstUtil.get_game_object("OIL_DERRICK_ACTIVE") else "In Search"
                    oil_derrick_info += "Oil Derrick_" + str(i) + " Defense:\nOil Reserves:\n"
                    oil_derrick_info2 += str(map_object.get_defense()) + "\n" + reserved_qty + "\n"  
                    i += 1

        info_text1 = "Support Rate:"        + "\n" \
                    + "Tax Rate:"           + "\n" \
                    + "Money:"              + "\n" \
                    + "Oil:"                + "\n" \
                    + "Capital Defense:"    + "\n" \
                    + "Army:"               + "\n" \
                    + "Battle Plane:"       + "\n" \
                    + "ICBM:"               + "\n" \
                    + "\n" \
                    + oil_derrick_info
        info_font1 = pygame.font.SysFont(None, 20)
        info_rect1 = pygame.Rect((0, 0, 160, 288))
                    
        rendered_text1 = render_textrect(info_text1, info_font1, info_rect1, GameConstUtil.get_color("WHITE"), GameConstUtil.get_color("BLACK"), 0)        
        screen.blit(rendered_text1, (360, 40))

        info_text2 = str(country["SUPPORT_RATE"])           + "\n" \
                    + str(country["TAX_RATE"])              + "\n" \
                    + str(country["MONEY"])                 + "\n" \
                    + str(country["OIL"])                   + "\n" \
                    + str(country["COUNTRY_MAP"].get_capital().get_defense()) + "\n" \
                    + str(country["ARMY"])                  + "\n" \
                    + str(country["PLANE"])                 + "\n" \
                    + str(country["ICBM"])                  + "\n" \
                    + "\n" \
                    + oil_derrick_info2
                                        
        info_font2 = pygame.font.SysFont(None, 20)
        info_rect2 = pygame.Rect((0, 0, 80, 288))
                    
        rendered_text2 = render_textrect(info_text2, info_font2, info_rect2, GameConstUtil.get_color("WHITE"), GameConstUtil.get_color("BLACK"), 2)        
        screen.blit(rendered_text2, (520, 40))

        info_text3 = "Oil Exchg Rate: " + str(game_state.get_oil_exchg_rate()) + \
                    " Plane Price: " + str(game_state.get_plane_price()) + \
                    " ICBM Price: " + str(game_state.get_icbm_price())
        info_font3 = pygame.font.SysFont(None, 20)                    
        info_rect3 = pygame.Rect((0, 0, 240, 40))
        rendered_text3 = render_textrect(info_text3, info_font3, info_rect3, GameConstUtil.get_color("CYAN"), GameConstUtil.get_color("BLACK"), 0)        
        screen.blit(rendered_text3, (360, 310))       
    
    def _draw_command_screen(self, screen, game_state):
        ############################
        #Message Part
        ############################
        pygame.time.wait(GameConstUtil.get_wait_millisec("NORMAL"))
        
        result = self._strategy_result
        message_text1 = result["MESSAGE"]
        message_font1 = pygame.font.SysFont(None, 20)
        message_rect1 = pygame.Rect((0, 0, 560, 80))
        
        if result["RESULT"] == GameConstUtil.get_game_event("ERROR"):
            msg_color = GameConstUtil.get_color("RED")
        else:
            msg_color = GameConstUtil.get_color("WHITE")
            
        rendered_text1 = render_textrect(message_text1, message_font1, message_rect1, msg_color, GameConstUtil.get_color("BLACK"), 0)        
        screen.blit(rendered_text1, (40, 350))
        
        ############################
        #Key Input Part
        ############################
        keyinput_font = pygame.font.SysFont(None, 20)
        keyinput = keyinput_font.render(game_state.get_keyinput(), False, GameConstUtil.get_color("CYAN"))
        screen.blit(keyinput, (40, 420))

        
    ############################################################################
    # Public methods            
    ############################################################################
    def draw(self, screen, game_state):
        country = game_state.get_countries()[game_state.get_turn()]
        self._draw_backdrop(screen, game_state, country)
        self._draw_info_screen(screen, game_state, country)
        self._draw_command_screen(screen, game_state)

class StrategySpyScreen(StrategyExecScreen):
    
    def draw(self, screen, game_state):
        country = game_state.get_spied_country()
        self._draw_backdrop(screen, game_state, country)
        self._draw_info_screen(screen, game_state, country)
        self._draw_command_screen(screen, game_state)

class StrategyOilDerrickScreen(StrategyExecScreen):
    
    def _draw_info_screen(self, screen, game_state):
        pass
