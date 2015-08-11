# coding: utf-8

from pygame.locals import * 
import sys
#from FontFile import WIDTH
from gamescreen import *
from gamecontroller import *
from gameutil import *
from gamestate import *

################################################################################
class GameLauncher:
    
    def __init__(self):
        pygame.init()
        #self.screen = pygame.display.set_mode(GameConstUtil.get_scr_rect().size, FULLSCREEN)
        self.screen = pygame.display.set_mode(GameConstUtil.get_scr_rect().size)
        pygame.display.set_caption(GameConstUtil.get_game_title())

        self._cur_str = []
        self._cur_str_break_flag = False
        
        self._init_game()
        ########################################################################
        #Main Loop
        ########################################################################
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self._update()
            self._draw()
            pygame.display.update()
            if self.game_state.get_sound_to_play() != None:
                self.game_state.get_sound_to_play().play()
            
            self._setup_key_handlers()
    
    def _init_game(self):
        self.game_state = GameState()
        
        #Game Screens
        self._start_screen = StartScreen()
        self._big_map_screen = BigMapScreen()
        self._strategy_exec_screen = StrategyExecScreen()
        self._strategy_spy_screen = StrategySpyScreen()

        #Game Controllers           
        self._big_map_controller = BigMapController()
        self._strategy_exec_controller = StrategyExecController()
        self._strategy_spy_controller = StrategySpyController()

    def _get_screen(self):
        status = self.game_state.get_status()
        if status == GameConstUtil.get_game_status("START"):
            return self._start_screen
        elif status == GameConstUtil.get_game_status("BIG_MAP"):
            return self._big_map_screen
        elif status == GameConstUtil.get_game_status("STRATEGY_EXEC"):
            return self._strategy_exec_screen        
        elif status == GameConstUtil.get_game_status("STRATEGY_SPY"):
            return self._strategy_spy_screen        

    def _get_game_controller(self):
        status = self.game_state.get_status()
        if status == GameConstUtil.get_game_status("START"):
            return None
        elif status == GameConstUtil.get_game_status("BIG_MAP"):
            return self._big_map_controller
        elif status == GameConstUtil.get_game_status("STRATEGY_EXEC"):
            return self._strategy_exec_controller        
        elif status == GameConstUtil.get_game_status("STRATEGY_SPY"):
            return self._strategy_spy_controller        
        
    def _update(self):
        #Key Input Control
        key_input = "".join(self._cur_str)
        self.game_state.set_keyinput(key_input)
        if self._cur_str_break_flag:
            self.game_state.set_keyinput_confirmed(key_input)
            self.game_state.set_keyinput_confirmed_flag(True)
            self._cur_str = []
            self._cur_str_break_flag = False
        else:
            self.game_state.set_keyinput_confirmed_flag(False)
        
        #Call Game Controller
        if self._get_game_controller() != None:
            self._get_game_controller().control_scene(self._get_screen(), self.game_state)
                                    
    def _draw(self):
        self.screen.fill(GameConstUtil.get_color("BLACK"))
        self._get_screen().draw(self.screen, self.game_state)
            
    def _setup_key_handlers(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if self.game_state.get_status() == GameConstUtil.get_game_status("START"):
                    self.game_state.set_status(GameConstUtil.get_game_status("BIG_MAP"))
                elif self.game_state.get_status() == GameConstUtil.get_game_status("GLORIOUS_ENDING"):
                    self._init_game()
                elif self.game_state.get_status() == GameConstUtil.get_game_status("GAMEOVER"):
                    self._init_game()
            ##############################################################
            # User Key Input Handling
            # Numeric inpur is accepted. 
            # Carriage Return confirms the input.
            ##############################################################
            elif event.type == KEYDOWN and (K_0 <= event.key <= K_9):
                self._cur_str.append(chr(event.key).upper())
            elif event.type == KEYDOWN and event.key == K_BACKSPACE:
                self._cur_str = self._cur_str[0:-1]
            elif event.type == KEYDOWN and event.key == K_RETURN:
                self._cur_str_break_flag = True  
                                        
################################################################################
# Kick the program
################################################################################
if __name__ == "__main__":
    GameLauncher()
    
