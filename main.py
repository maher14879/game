from source.game import Game
import cProfile

def main():
    game = Game()
    game.setup()
    
    while True:
        game.run()

if __name__ == "__main__":
    #cProfile.run("main()", sort="time")
    main()