# Importes
from turtle import Screen , Turtle
from onstartup import onStartup
from snake import Snake
from food import Food, BigFood
from score import Score
import time

# Game Controller Variable
gameOver = False
haveFood = True
haveBigFood = False
onMenu = False

# Create Screen
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("green")
screen.tracer(0)

# Create Screen Border
border = Turtle()
border.penup()
border.color("white")
border.goto(-300, -300)
border.pendown()
border.pensize(3)
for _ in range(4):
    border.forward(600)
    border.left(90)
border.hideturtle()

# Creating Instances
start = onStartup()
snake = Snake()
food = Food()
bigfood = BigFood()
score = Score()
screen.listen()


def gameMenu():
    # Game Menu
    print("gameMenu")
    global onMenu
    onMenu = True
    score.hide()
    start.showStartupMessage()
    score.showOnlyHighScore()


def gameIsOver():
    # Game Over
    print("gameIsOver")
    score.gameOver()
    snake.hide()
    food.hide()
    bigfood.hide()
    screen.update()
    time.sleep(1)
    gameMenu()


def startGame():
    # Start Game
    print("startGame")
    global haveFood, haveBigFood, gameOver

    # Key Map For Snake Movement
    screen.onkey(fun=snake.up, key="Up")
    screen.onkey(fun=snake.up, key="w")

    screen.onkey(fun=snake.down, key="Down")
    screen.onkey(fun=snake.down, key="s")

    screen.onkey(fun=snake.left, key="Left")
    screen.onkey(fun=snake.left, key="a")

    screen.onkey(fun=snake.right, key="Right")
    screen.onkey(fun=snake.right, key="d")

    # Game Main Loop
    while not gameOver:
        # Start Rendering
        screen.update()

        # Snake Speed Control As Per The Score
        if score.score < 50:
            time.sleep(0.3)
        elif 50 < score.score < 100:
            time.sleep(0.25)
        elif 100 < score.score < 175:
            time.sleep(0.20)
        elif 175 < score.score < 250:
            time.sleep(0.15)
        else:
            time.sleep(0.1)

        # Start Moving
        snake.move()

        # Collision With Food
        if snake.head.distance(food) < 20 and haveFood:
            food.refresh()
            score.updateScore()
            snake.extendSnake()

        # Create Big Food
        if score.score > 4 and score.score % 5 == 0 and not haveBigFood:
            haveFood = False
            food.hide()
            bigfood.showFood()
            haveBigFood = True

        # Collision With Big Food
        if snake.head.distance(bigfood) < 30 and haveBigFood:
            haveBigFood = False
            score.updateExtraScore()
            snake.extendSnake()
            haveFood = True
            food.show()
            bigfood.hide()

        # Collision With Wall
        if not (-300 < snake.head.xcor() < 300 and -300 < snake.head.ycor() < 300):
            gameOver = True
            gameIsOver()

        # Collision With Tail
        for segment in snake.snake[1:]:
            if snake.head.distance(segment) < 10:
                gameOver = True
                gameIsOver()


def playButton():
    # Play Button
    global gameOver, onMenu
    if onMenu:
        print("playButton")
        gameOver = False
        onMenu = False
        start.hideAllMessage()
        snake.reset()
        food.show()
        food.refresh()
        score.hide()
        score.reset()
        score.showScore()
        startGame()


def controlsButton():
    # Controls Button
    global onMenu
    onMenu = False
    if not onMenu:
        print("controlsButton")
        start.hideAllMessage()
        start.showControls()


def backButton():
    # Back Button
    global onMenu
    if not onMenu:
        print("backButton")
        start.hideAllMessage()
        gameMenu()


def resetHighScore():
    # Reset High Score Button
    print("resetHighScore")
    global onMenu
    if onMenu:
        score.hide()
        score.resetHighScore()
        score.showOnlyHighScore()


def exitButton():
    # Exit Button
    global onMenu
    if onMenu:
        print("exitButton")
        screen.bye()


# Key Map For Buttons
screen.onkey(fun=playButton, key="1")

screen.onkey(fun=controlsButton, key="5")

screen.onkey(fun=backButton, key="b")

screen.onkey(fun=exitButton, key="0")

screen.onkey(fun=resetHighScore, key="r")

# Will Execute On First Run
if __name__ == "__main__":
    gameMenu()

# Activate Exit Button
screen.exitonclick()
