"""
The turtle_adventure module maintains all classes related to the Turtle's
adventure game.
"""
import random
import math
from turtle import RawTurtle
from gamelib import Game, GameElement


class TurtleGameElement(GameElement):
    """
    An abstract class representing all game elemnets related to the Turtle's
    Adventure game
    """

    def __init__(self, game: "TurtleAdventureGame"):
        super().__init__(game)
        self.__game: "TurtleAdventureGame" = game

    @property
    def game(self) -> "TurtleAdventureGame":
        """
        Get reference to the associated TurtleAnvengerGame instance
        """
        return self.__game


class Waypoint(TurtleGameElement):
    """
    Represent the waypoint to which the player will move.
    """

    def __init__(self, game: "TurtleAdventureGame"):
        super().__init__(game)
        self.__id1: int
        self.__id2: int
        self.__active: bool = False

    def create(self) -> None:
        self.__id1 = self.canvas.create_line(0, 0, 0, 0, width=2, fill="green")
        self.__id2 = self.canvas.create_line(0, 0, 0, 0, width=2, fill="green")

    def delete(self) -> None:
        self.canvas.delete(self.__id1)
        self.canvas.delete(self.__id2)

    def update(self) -> None:
        # there is nothing to update because a waypoint is fixed
        pass

    def render(self) -> None:
        if self.is_active:
            self.canvas.itemconfigure(self.__id1, state="normal")
            self.canvas.itemconfigure(self.__id2, state="normal")
            self.canvas.tag_raise(self.__id1)
            self.canvas.tag_raise(self.__id2)
            self.canvas.coords(self.__id1, self.x-10, self.y-10, self.x+10, self.y+10)
            self.canvas.coords(self.__id2, self.x-10, self.y+10, self.x+10, self.y-10)
        else:
            self.canvas.itemconfigure(self.__id1, state="hidden")
            self.canvas.itemconfigure(self.__id2, state="hidden")

    def activate(self, x: float, y: float) -> None:
        """
        Activate this waypoint with the specified location.
        """
        self.__active = True
        self.x = x
        self.y = y

    def deactivate(self) -> None:
        """
        Mark this waypoint as inactive.
        """
        self.__active = False

    @property
    def is_active(self) -> bool:
        """
        Get the flag indicating whether this waypoint is active.
        """
        return self.__active


class Home(TurtleGameElement):
    """
    Represent the player's home.
    """

    def __init__(self, game: "TurtleAdventureGame", pos: tuple[int, int], size: int):
        super().__init__(game)
        self.__id: int
        self.__size: int = size
        x, y = pos
        self.x = x
        self.y = y

    @property
    def size(self) -> int:
        """
        Get or set the size of Home
        """
        return self.__size

    @size.setter
    def size(self, val: int) -> None:
        self.__size = val

    def create(self) -> None:
        self.__id = self.canvas.create_rectangle(0, 0, 0, 0, outline="brown", width=2)

    def delete(self) -> None:
        self.canvas.delete(self.__id)

    def update(self) -> None:
        # there is nothing to update, unless home is allowed to moved
        pass

    def render(self) -> None:
        self.canvas.coords(self.__id, 
        self.x - self.size/2, 
        self.y - self.size/2, 
        self.x + self.size/2, 
        self.y + self.size/2)

    def contains(self, x: float, y: float):
        """
        Check whether home contains the point (x, y).
        """
        x1, x2 = self.x-self.size/2, self.x+self.size/2
        y1, y2 = self.y-self.size/2, self.y+self.size/2
        return x1 <= x <= x2 and y1 <= y <= y2


class Player(TurtleGameElement):
    """
    Represent the main player, implemented using Python's turtle.
    """

    def __init__(self,
    game: "TurtleAdventureGame",
    turtle: RawTurtle,
    speed: float = 5):
        super().__init__(game)
        self.__speed: float = speed
        self.__turtle: RawTurtle = turtle

    def create(self) -> None:
        turtle = RawTurtle(self.canvas)
        turtle.getscreen().tracer(False) # disable turtle's built-in animation
        turtle.shape("turtle")
        turtle.color("green")
        turtle.penup()

        self.__turtle = turtle

    @property
    def speed(self) -> float:
        """
        Give the player's current speed.
        """
        return self.__speed

    @speed.setter
    def speed(self, val: float) -> None:
        self.__speed = val

    def delete(self) -> None:
        pass

    def update(self) -> None:
        # check if player has arrived home
        if self.game.home.contains(self.x, self.y):
            self.game.game_over_win()
        turtle = self.__turtle
        waypoint = self.game.waypoint
        if self.game.waypoint.is_active:
            turtle.setheading(turtle.towards(waypoint.x, waypoint.y))
            turtle.forward(self.speed)
            if turtle.distance(waypoint.x, waypoint.y) < self.speed:
                waypoint.deactivate()

    def render(self) -> None:
        self.__turtle.goto(self.x, self.y)
        self.__turtle.getscreen().update()

    # override original property x's getter/setter to use turtle's methods
    # instead
    @property
    def x(self) -> float:
        return self.__turtle.xcor()

    @x.setter
    def x(self, val: float) -> None:
        self.__turtle.setx(val)

    # override original property y's getter/setter to use turtle's methods
    # instead
    @property
    def y(self) -> float:
        return self.__turtle.ycor()

    @y.setter
    def y(self, val: float) -> None:
        self.__turtle.sety(val)


class Enemy(TurtleGameElement):
    """
    Define an abstract enemy for the Turtle's adventure game
    """

    def __init__(self,
                game: "TurtleAdventureGame",
                size: int,
                color: str):
        super().__init__(game)
        self.__size = size
        self.__color = color

    @property
    def size(self) -> float:
        """
        Get the size of the enemy
        """
        return self.__size

    @property
    def color(self) -> str:
        """
        Get the color of the enemy
        """
        return self.__color

    def hits_player(self):
        """
        Check whether the enemy is hitting the player
        """
        return (
            (self.x - self.size/2 < self.game.player.x < self.x + self.size/2)
            and
            (self.y - self.size/2 < self.game.player.y < self.y + self.size/2)
        )


# TODO
# * Define your enemy classes
# * Implement all methods required by the GameElement abstract class
# * Define enemy's update logic in the update() method
# * Check whether the player hits this enemy, then call the
#   self.game.game_over_lose() method in the TurtleAdventureGame class.
class DemoEnemy(Enemy):
    """
    Demo enemy
    """

    def __init__(self,
                game: "TurtleAdventureGame",
                size: int,
                color: str):
        super().__init__(game, size, color)
        self.__id = None

    def create(self) -> None:
        self.__id = self.canvas.create_oval(0, 0, 0, 0, fill=self.color)

    def update(self) -> None:
        self.x += 1
        self.y += 1
        if self.hits_player():
            self.game.game_over_lose()

    def render(self) -> None:
        self.canvas.coords(self.__id,
                            self.x - self.size/2,
                            self.y - self.size/2,
                            self.x + self.size/2,
                            self.y + self.size/2)

    def delete(self) -> None:
        pass

class EnemyGenerator:
    """
    An EnemyGenerator instance is responsible for creating enemies of various
    kinds and scheduling them to appear at certain points in time.
    """

    def __init__(self, game: "TurtleAdventureGame", level: int):
        self.__game: TurtleAdventureGame = game
        self.__level: int = level

        self.__game.after(1000, self.create_random_enemy)
        self.__game.after(2000, self.create_chasing_enemy)
        self.__game.after(3000, self.create_fencing_enemy)
        self.__game.after(4000, self.create_teleporting_enemy)

    @property
    def game(self) -> "TurtleAdventureGame":
        """
        Get reference to the associated TurtleAnvengerGame instance
        """
        return self.__game

    @property
    def level(self) -> int:
        """
        Get the game level
        """
        return self.__level

    def create_random_enemy(self):
            random_enemy = RandomWalkEnemy(self.__game, 20, "red")
            if random_enemy.x != 100 and random_enemy.y != 100:
                random_enemy.x = random.randint(0, 700)
                random_enemy.y = random.randint(0, 400)
            self.game.add_element(random_enemy)
            self.game.after(1000, self.create_random_enemy)
    def create_chasing_enemy(self):
            chasing_enemy = ChasingEnemy(self.__game, size=20, color="purple")
            chasing_enemy.x = random.randint(0, self.__game.screen_width)
            chasing_enemy.y = random.randint(0, self.__game.screen_height)
            self.__game.add_enemy(chasing_enemy)
            self.__game.after(1000, self.create_chasing_enemy)
    def create_fencing_enemy(self):
            max_distance_from_home = 25
            for i in range(15):
                fencing_enemy = FencingEnemy(self.__game, 20, "blue")
                if fencing_enemy.x != self.game.home.x and fencing_enemy.y != self.game.home.y:
                    fencing_enemy.x = random.randint(self.__game.home.x - max_distance_from_home, self.__game.home.x + max_distance_from_home)
                    fencing_enemy.y = random.randint(self.__game.home.y - max_distance_from_home, self.__game.home.y + max_distance_from_home)
                while self.__game.home.contains(fencing_enemy.x, fencing_enemy.y):
                    fencing_enemy.x = random.randint(self.__game.home.x - max_distance_from_home, self.__game.home.x + max_distance_from_home)
                    fencing_enemy.y = random.randint(self.__game.home.y - max_distance_from_home, self.__game.home.y + max_distance_from_home)
                self.__game.add_enemy(fencing_enemy)
    def create_teleporting_enemy(self):
            for _ in range(5):
                teleporting_enemy = TeleportingEnemy(self.__game, size=20, color="black")
                if teleporting_enemy.x != 100 and teleporting_enemy.y != 100:
                    teleporting_enemy.x = random.randint(0, self.__game.screen_width)
                    teleporting_enemy.y = random.randint(0, self.__game.screen_height)
                self.__game.add_enemy(teleporting_enemy)
            self.__game.after(500, self.create_teleporting_enemy)
        
class RandomWalkEnemy(Enemy):
    """
    Random enemy that walks in different directions and bounces off edges
    """

    def __init__(self,
                game: "TurtleAdventureGame",
                size: int,
                color: str):
        super().__init__(game, size, color)
        self.__id = None
        self.__dx = 0  # Change in x-coordinate (speed in x-direction)
        self.__dy = 0  # Change in y-coordinate (speed in y-direction)
        self.__speed = 3  # Overall speed of the enemy

    def create(self) -> None:
        self.__id = self.canvas.create_oval(0, 0, 0, 0, fill='red')
        self.__choose_random_direction()

    def update(self) -> None:
        self.x += self.__dx
        self.y += self.__dy

        if self.x + self.size/2 >= self.game.screen_width:
            self.__dx *= -1  # Reverse x on hitting right 
        elif self.x - self.size/2 <= 0:
            self.__dx *= -1  # Reverse x on hitting left 

        if self.y + self.size/2 >= self.game.screen_height:
            self.__dy *= -1  # Reverse y on hitting top 
        elif self.y - self.size/2 <= 0:
            self.__dy *= -1  # Reverse y on hitting bottom

        if self.hits_player():
            self.game.game_over_lose()

    def render(self) -> None:
        self.canvas.coords(self.__id,
                            self.x - self.size/2,
                            self.y - self.size/2,
                            self.x + self.size/2,
                            self.y + self.size/2)

    def delete(self) -> None:
        pass

    def __choose_random_direction(self):
        """
        Chooses a random direction (up, down, left, or right) for the enemy to walk.
        """
        direction = random.choice(["up", "down", "left", "right"])
        if direction == "up":
            self.__dx = 0
            self.__dy = self.__speed
        elif direction == "down":
            self.__dx = 0
            self.__dy = -self.__speed
        elif direction == "left":
            self.__dx = -self.__speed
            self.__dy = 0
        else: 
            self.__dx = self.__speed
            self.__dy = 0

class ChasingEnemy(Enemy):
    """
    Chasing enemy
    """

    def __init__(self, game: "TurtleAdventureGame", size: int, color: str):
        super().__init__(game, size, color)
        self.__id = None
        self.__speed = 4  # Adjust speed as needed

    def create(self) -> None:
        self.__id = self.canvas.create_oval(0, 0, 0, 0, fill=self.color)

    def update(self) -> None:
        player_x = self.game.player.x
        player_y = self.game.player.y
        enemy_speed = self.__speed

        # Calculate the vector from enemy to player
        dx = player_x - self.x
        dy = player_y - self.y

        # Move towards the player along the normalized vector
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            normalized_dx = dx / distance
            normalized_dy = dy / distance

            self.x += normalized_dx * enemy_speed
            self.y += normalized_dy * enemy_speed

        if self.hits_player():
            self.game.game_over_lose()

    def render(self) -> None:
        self.canvas.coords(self.__id,
                            self.x - self.size/2,
                            self.y - self.size/2,
                            self.x + self.size/2,
                            self.y + self.size/2)

    def delete(self) -> None:
        pass

class FencingEnemy(Enemy):
    """
    Fencing enemy that moves around the home in a square form
    """

    def __init__(self, game: "TurtleAdventureGame", size: int, color: str):
        super().__init__(game, size, color)
        self.__id = None
        self.__speed = 4  # Adjust speed as needed
        self.__direction = "right"  # Initial movement direction

    def create(self) -> None:
        self.__id = self.canvas.create_oval(0, 0, 0, 0, fill=self.color)

    def update(self) -> None:
        # Determine the boundaries of the square around the home
        home_x, home_y = self.game.home.x, self.game.home.y
        square_size = 80  # Adjust the size of the square as needed
        square_left = home_x - square_size / 2
        square_right = home_x + square_size / 2
        square_top = home_y - square_size / 2
        square_bottom = home_y + square_size / 2

        # Move the enemy based on the current direction
        if self.__direction == "right":
            self.x += self.__speed
            if self.x >= square_right:
                self.x = square_right
                self.__direction = "down"
        elif self.__direction == "down":
            self.y += self.__speed
            if self.y >= square_bottom:
                self.y = square_bottom
                self.__direction = "left"
        elif self.__direction == "left":
            self.x -= self.__speed
            if self.x <= square_left:
                self.x = square_left
                self.__direction = "up"
        elif self.__direction == "up":
            self.y -= self.__speed
            if self.y <= square_top:
                self.y = square_top
                self.__direction = "right"

        if self.hits_player():
            self.game.game_over_lose()

    def render(self) -> None:
        self.canvas.coords(self.__id,
                        self.x - self.size / 2,
                        self.y - self.size / 2,
                        self.x + self.size / 2,
                        self.y + self.size / 2)

    def delete(self) -> None:
        pass    

class TeleportingEnemy(Enemy):
    """
    Teleporting Enemy appears near the player or home randomly.
    """

    def __init__(self, game: "TurtleAdventureGame", size: int, color: str):
        super().__init__(game, size, color)
        self.__id = None
        self.__teleport_cooldown = 60  # Cooldown between teleports (in frames)
        self.__teleport_counter = 0

    def create(self) -> None:
        self.__id = self.canvas.create_rectangle(0, 0, 0, 0, fill=self.color)

    def update(self) -> None:
        self.__teleport_counter += 1
        if self.__teleport_counter >= self.__teleport_cooldown:
            self.teleport()
            self.__teleport_counter = 0

        if self.hits_player():
            self.game.game_over_lose()

    def render(self) -> None:
        self.canvas.coords(self.__id,
                        self.x - self.size / 2,
                        self.y - self.size / 2,
                        self.x + self.size / 2,
                        self.y + self.size / 2)

    def delete(self) -> None:
        pass

    def teleport(self) -> None:
        """
        Teleport the enemy near the player or home randomly.
        """
        choice = random.choice(["player", "home"])
        if choice == "player":
            self.x = self.game.player.x + random.randint(-200, 200)
            self.y = self.game.player.y + random.randint(-200, 200)
        else:
            self.x = self.game.home.x + random.randint(-200, 200)
            self.y = self.game.home.y + random.randint(-200, 200)


class TurtleAdventureGame(Game): # pylint: disable=too-many-ancestors
    """
    The main class for Turtle's Adventure.
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, parent, screen_width: int, screen_height: int, level: int = 1):
        self.level: int = level
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.waypoint: Waypoint
        self.player: Player
        self.home: Home
        self.enemies: list[Enemy] = []
        self.enemy_generator: EnemyGenerator
        super().__init__(parent)

    def init_game(self):
        self.canvas.config(width=self.screen_width, height=self.screen_height)
        turtle = RawTurtle(self.canvas)
        # set turtle screen's origin to the top-left corner
        turtle.screen.setworldcoordinates(0, self.screen_height-1, self.screen_width-1, 0)

        self.waypoint = Waypoint(self)
        self.add_element(self.waypoint)
        self.home = Home(self, (self.screen_width-100, self.screen_height//2), 20)
        self.add_element(self.home)
        self.player = Player(self, turtle)
        self.add_element(self.player)
        self.canvas.bind("<Button-1>", lambda e: self.waypoint.activate(e.x, e.y))

        self.enemy_generator = EnemyGenerator(self, level=self.level)

        self.player.x = 50
        self.player.y = self.screen_height//2

    def add_enemy(self, enemy: Enemy) -> None:
        """
        Add a new enemy into the current game
        """
        self.enemies.append(enemy)
        self.add_element(enemy)

    def game_over_win(self) -> None:
        """
        Called when the player wins the game and stop the game
        """
        self.stop()
        font = ("Arial", 36, "bold")
        self.canvas.create_text(self.screen_width/2,
                                self.screen_height/2,
                                text="You Win",
                                font=font,
                                fill="green")

    def game_over_lose(self) -> None:
        """
        Called when the player loses the game and stop the game
        """
        self.stop()
        font = ("Arial", 36, "bold")
        self.canvas.create_text(self.screen_width/2,
                                self.screen_height/2,
                                text="You Lose",
                                font=font,
                                fill="red")
    
    
