from source.game import Game

if __name__ == "__main__":
    game = Game()
    game.setup()
    
    while True:
        game.run()