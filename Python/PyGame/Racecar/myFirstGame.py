import pygame
import time
import random

'''Basic pygame template'''

pygame.init() #Creates an instance of pygame

'''---------------Define the constants----------------'''
display_width = 876 #Make these varables so we can programmatically assign new values later if neeeded
display_height = 800
gameDisplay = pygame.display.set_mode((display_width,display_height)) #Defines the window frame size top left corner is 0,0

car_width = (89) #Size values are in px
car_height = (177)

pygame.display.set_caption('myRacecar Game') #Defines the window title
carImg = pygame.image.load('racecar.png')
background_image = pygame.image.load('roadway.jpg').convert()

black = (0,0,0) #RGB Values
white = (255,255,255)
red = (255,0,0)

clock = pygame.time.Clock() #Create an in-game clock
'''--------------End Constants--------------------'''

'''--------------Define the function---------------'''
def things(thingx, thingy, thingw, thingh, thingColor): #Width, hieght, xy coord, and color
    pygame.draw.rect(gameDisplay, thingColor, [thingx, thingy, thingw, thingh])


def bg(x,y):
    gameDisplay.blit(background_image, (0,0))


def car(x,y):
    gameDisplay.blit(carImg, (x,y)) #blit means painting something to the surface
    

def crash():
    message_display('You have crashed!')


def text_objects(text, font): #Passing in text and font objects to define the text_objects()
    textSurface = font.render(text, True, red) #x,x,x first is text, second is antialiasing, 3rd is color
    return textSurface, textSurface.get_rect() #Creates a rectangle around the text message
    #This is so the message_display() will know how to position the rectangle of text defined here


def message_display(text): #Define how pygame will display messages when called, can be any message
    largeText = pygame.font.Font('freesansbold.ttf', 35) #Set the font family and size
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2)) #Display text as center on screen
    gameDisplay.blit(TextSurf, TextRect) #Actually assigns the text to the screen once we call update()
    pygame.display.update()
    
    time.sleep(1) #Sleep value in secondsfor a breif pause

    game_loop() #Start game all over by calling the game loop once again
'''----------------End the Function------------------'''
            

'''----------Begin the event listening loop----------'''
def game_loop():
    x = (display_width * 0.45)  #0,0 is upper Left Corner of Screen
    y = (display_height * 0.08)  #values in px or in this case, relative percentage of px in relation to the screen

    x_change = 0
    y_change = 0
    score = 0
    count = 0
    wrecks = 0
    thing_startx = random.randrange(0, display_width) #x=0 is far left edge of screen
    thing_starty = -600 #y=0 is top left corner of screen, so we are painting objects offscreen
    thing_speed = 7
    thing_width = 100 #value in px, This will make a 100x 100 box
    thing_height = 100
    gameExit = False

    while not gameExit: #Could have been anything, in this case for a race car game, I chose crashed
        for event in pygame.event.get(): #Get all events that are occuring within the game per frame per second
            if event.type == pygame.QUIT: #This is the top right X in the window titlebar for exiting program
                pygame.quit() #End the Pygame engine
                quit() #Quit program

            if event.type == pygame.KEYDOWN: #Listening for a keyboard key press event
                if event.key == pygame.K_LEFT: #Left arrow key
                    x_change = -5

                elif event.key == pygame.K_RIGHT: #Right arrow key
                    x_change = 5
                    
            if event.type == pygame.KEYUP: #Key is released
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0 #Stops the movement

            if event.type == pygame.KEYDOWN: #Listening for a keyboard key press event
                if event.key == pygame.K_UP: #Left arrow key
                    y_change = -5
                    
                elif event.key == pygame.K_DOWN: #Right arrow key
                    y_change = 5
                    
            if event.type == pygame.KEYUP: #Key is released
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0 #Stops the movement

        x += x_change #So this will either +-5, +5, or +0 depending on the condition
        y += y_change #So this will either +-5, +5, or +0 depending on the condition
        
        bg(x,y)
        #gameDisplay.fill(white) This sets background color and needs to be painted first before any images
        #things(thingx, thingy, thingw, thingh, thingColor)
        things(thing_startx, thing_starty, thing_width, thing_height, black)
        thing_starty += thing_speed #which is currently set to 7. This creates random moving squares
        car(x,y) #To represent car movement, this coordinate value will change frequently
        
        if (x > (display_width - car_width)) or (x < 0):
            if wrecks <= 1:
                crash()
                count = count + 1
            
        if (y > (display_height - car_height)) or (y < 0):
                crash()
                count = count + 1

        #creating the random obsticles
        '''since display_height is full length from top to bottom of screen''' 
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
        
        pygame.display.update() #Update the event or the entire window...redrawing of the frames in a frame-by-frame
        clock.tick(60) #Frames per second
'''----------End the event listening loop------------'''


game_loop() #Start the Game loop function when program begins
pygame.quit() #Stop pygame from running
quit() #Quit program

