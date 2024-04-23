import pygame
from settings import *
from sprites import *

## the game class
class Game:
    def __init__(self):
        ## initialize Pygame
        pygame.init()

        ## create the window, set the title, and create a clock
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    ## create a new game
    def new(self):
        self.board = Board()
        self.board.display_board()

    ## the main game loop
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
        else:
            self.end_screen()

    ## draw the tiles
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.board.draw(self.screen)
        pygame.display.flip()

    ## check if we won
    def check_win(self):
        for row in self.board.board_list:
            for tile in row:
                if tile.type != 'X' and not tile.revealed: ## if a tile is not a mine and is not revealed, continue the game
                    return False
        return True

    ## get the user clicks
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx //= TILESIZE
                my //= TILESIZE

                if event.button == 1: ## left click
                    if not self.board.board_list[mx][my].flagged:
                        ## dig and check if its exploded
                        if not self.board.dig(mx, my):
                            ## explode
                            for row in self.board.board_list:
                                for tile in row:
                                    if tile.flagged and tile.type != 'X':
                                        tile.flagged = False
                                        tile.revealed = True
                                        tile.image = tile_not_mine
                                    elif tile.type == 'X':
                                        tile.reveal = True
                            self.playing = False


                if event.button == 3: ## right click
                    if not self.board.board_list[mx][my].revealed:
                        self.board.board_list[mx][my].flagged = not self.board.board_list[mx][my].flagged

                if self.check_win():
                    self.win = True
                    self.playing = False
                    for row in self.board.board_list:
                        for tile in row:
                            if not tile.revealed:
                                tile.flagged = True

    ##
    def end_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    return

game = Game()
while True:
    game.new()
    game.run()