#this is going to be my game for jimmy. 
#hexcode color for space background in art is 111327
#name will be Terrablue Moon, a water world which was discovered in deep space thought to contain new life and resources never seen before.
#play style will be a top-down shooter featuring the player as a recon ship/drone having to fight strange otherwordly water alien creatures.
#has to pass a few stages and collect energy to get back into space.
#game will feature some sort of ai prompt/follow along that will also provide interesting facts about oceans in general. (source of information will come from Google, sources will be sited in game as necessary



#start with importing all the libraries I will use
import pygame
import sys
import random
from pygame.locals import *



#initiate the program loop itself.
pygame.init()



# Clock setup
clock = pygame.time.Clock()

#decalre a window size and title
window_width = 1600
window_height = 900
pygame.display.set_caption('Terrablue Moon') 

# Screen setup
screen_width, screen_height = 1200, 650
screen = pygame.display.set_mode((screen_width, screen_height))

#variables and images loaded in the menu

# Menusplash setup
menusplash = pygame.image.load('graphics/TerrablueMoonMenu.png')
menusplash_rect = menusplash.get_rect(center=(screen_width // 2, screen_height // 2))

#menu buttons set up
#start game button
startbutton = pygame.image.load('graphics/startbutton.png')
startbutton_rect = startbutton.get_rect(topleft=(150,300))

#options button
optionsbutton = pygame.image.load('graphics/optionsbutton.png')
optionsbutton_rect = optionsbutton.get_rect(topleft=(150,375))

#credits button
creditsbutton = pygame.image.load('graphics/creditsbutton.png')
creditsbutton_rect = creditsbutton.get_rect(topleft=(150,450))

#exit button
exitbutton = pygame.image.load('graphics/exitbutton.png')
exitbutton_rect = exitbutton.get_rect(topleft=(150,525))




#images loaded for the story section

#slides for the games background story.
storyslideone = pygame.image.load('graphics/story/storyslideone.png')
storyslidetwo = pygame.image.load('graphics/story/storyslidetwo.png')
storyslidethree = pygame.image.load('graphics/story/storyslidethree.png')
storyslidefour = pygame.image.load('graphics/story/storyslidefour.png')
storyslidefive = pygame.image.load('graphics/story/storyslidefive.png')

 # To keep track of the current slide being displayed
slides = [storyslideone, storyslidetwo, storyslidethree, storyslidefour, storyslidefive]
current_slide = 0




#images and variables loaded for the gameplay state

#player
playership = pygame.image.load('graphics/Jimmy.png')
playership_rect = playership.get_rect(topleft = (644,500))
player_speed = 5
player_x, player_y = playership_rect.topleft

#ocean
oceantile_surface = pygame.image.load('graphics/oceantile.png').convert_alpha()
OCEAN = 0  # Change the tile type from GROUND to OCEAN or use any other appropriate name
TILE_SIZE = 64
tilemap = [[OCEAN for _ in range(screen_width // TILE_SIZE)] for _ in range(screen_height // TILE_SIZE)]
background_scroll = 0  # Initial scroll position
scroll_speed = 2  # Background scroll speed

#first enemy
rockfish = pygame.image.load('graphics/rockfish.png')
rockfish_rect = rockfish.get_rect(topleft=(100,100))
rockfish_list = []
max_rockfish = 3 # Or any number you choose


#ship's fire image and variables
bullet_img = pygame.image.load('graphics/shipfire.png')
bullet_speed = 8
bullet_list = []  # List to store bullet information
# Define a variable to track the time between shots
last_shot_time = 0
shot_delay = 300  # Time in milliseconds (1000 is 1 second)


#main game loop or starting game loop
#variable to allow the game to run
game_running = True
#creating a variable to establish a screen state, initial state will be menu that displays a background and buttons
game_state = "MainMenu"

#main/first game loop
while game_running:
    # Event handling
    mx, my = pygame.mouse.get_pos()
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            click = True

    current_time = pygame.time.get_ticks()

    if game_state == "MainMenu":
        screen.blit(menusplash, menusplash_rect)
        screen.blit(startbutton, startbutton_rect)
        screen.blit(optionsbutton, optionsbutton_rect)
        screen.blit(creditsbutton, creditsbutton_rect)
        screen.blit(exitbutton, exitbutton_rect)

        if startbutton_rect.collidepoint((mx, my)):  
            if click:
                game_state = "StorySlides"

        if exitbutton_rect.collidepoint((mx, my)): 
            if click: 
                pygame.quit() 
                sys.exit()

        pygame.display.update()
        clock.tick(60)





    if game_state == "StorySlides":
        screen.fill((0, 0, 0))  # Clear the screen

        keys = pygame.key.get_pressed()

        # Display current slide
        screen.blit(slides[current_slide], (0, 0))

        # Check for spacebar press to advance slides
        if keys[pygame.K_SPACE]:
            current_slide += 1
            pygame.time.delay(300)
            if current_slide >= len(slides):
                game_state = "Gameplay"

        pygame.display.update()
        clock.tick(24)

            

    elif game_state == 'Gameplay':

        #makes it appear as if the player is constantly moving foward by scrolling the background backwards.
        background_scroll += scroll_speed

         # Shooting mechanism
        current_time = pygame.time.get_ticks()  # Get the current time


        screen.fill((22, 30, 178))
        # Your gameplay logic and rendering


        keys = pygame.key.get_pressed()

        # Update player position based on key presses
        if keys[pygame.K_w]:
            player_y -= player_speed
        if keys[pygame.K_s]:
            player_y += player_speed
        if keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_d]:
            player_x += player_speed


        #GAMESTATE shooting code block START
        #fires an image of shipfire when space is pressed
        if keys[pygame.K_SPACE] and current_time - last_shot_time > shot_delay:
            # Fire bullet when spacebar is pressed and the delay has passed
            new_bullet = {
                'rect': bullet_img.get_rect(midtop=playership_rect.midtop),  # Set bullet position at the top center of the playership
                'image': bullet_img,
                'damage': 1
            }
            bullet_list.append(new_bullet)
            last_shot_time = current_time  # Update the last shot time


            # Update bullet positions and remove bullets that go off-screen
        for bullet in bullet_list:
            bullet['rect'].y -= bullet_speed  # Move the bullets upward (adjust as needed)
            if bullet['rect'].bottom < 0:  # Remove bullets that go off-screen
                bullet_list.remove(bullet)



        bullets_to_remove = []  # To store bullets that need to be removed
        for bullet in bullet_list:
            bullet['rect'].y -= bullet_speed  # Move the bullets upward (adjust as needed)
            if bullet['rect'].bottom < 0:  # Remove bullets that go off-screen
                bullets_to_remove.append(bullet)
            else:
                # Check collision with rockfish
                for rockfish in rockfish_list:
                    if bullet['rect'].colliderect(rockfish['rect']):
                        # You can handle damage here
                        # For example, reduce rockfish health by 1
                        rockfish['health'] -= 1
                        bullets_to_remove.append(bullet)  # Remove the bullet after hitting rockfish

        # Remove collided bullets from the list
        for bullet in bullets_to_remove:
            bullet_list.remove(bullet)


        #GAMESTATE shooting code block END


        # Update the ship's rect position
        playership_rect.topleft = (player_x, player_y)



        #this logic block handles spawning new enemies from the left
        # This logic block handles continuously spawning new enemies (rockfish) from the left
        while len(rockfish_list) < max_rockfish:
            new_rockfish = {
                'rect': rockfish_rect.copy(),
                'x_speed': 3,
                'image': rockfish,
                'health': 3 
            }
            # Fixed range between -50 and -600
            new_rockfish['rect'].left = random.randint(-1200, -350)
            new_rockfish['rect'].top = random.randint(0, screen_height - rockfish_rect.height)
            rockfish_list.append(new_rockfish)

 
                # Check rockfish health and remove defeated ones
        #rockfish_to_remove = []  # To store defeated rockfish
        for rockfish in rockfish_list:
            if rockfish['health'] <= 0:
                # Reset the rockfish properties
                rockfish['health'] = 3
                rockfish['rect'].left = random.randint(-1200, -350)
                rockfish['rect'].top = random.randint(0, screen_height - rockfish_rect.height)

        # Remove defeated rockfish from the list
        

        #GAMESTATE logic goes above this line rendering goes below this line


        


    # Calculate the offset within the tile based on scroll
        scroll_offset = background_scroll % TILE_SIZE

        # Render ocean tiles to create a loop
        for row in range(-1, screen_height // TILE_SIZE + 2):
            for col in range(-1, screen_width // TILE_SIZE + 2):
                tile_x = col * TILE_SIZE
                tile_y = row * TILE_SIZE + scroll_offset
                screen.blit(oceantile_surface, (tile_x, tile_y))

        #renders the rockfish inside of the list variable onto the screen and moves it towards the right
        # Renders the rockfish inside the list and moves them towards the right
        for rockfish in rockfish_list:
            rockfish_rect = rockfish['rect']
            rockfish_image = rockfish['image']
            rockfish_rect.x += rockfish['x_speed']

            # Check if the rockfish has moved off the screen to the right
            if rockfish_rect.right > screen_width + rockfish_rect.width:
                # Reset its position to the left side with a new random x
                rockfish_rect.left = random.randint(-1200, -350)
                rockfish_rect.top = random.randint(0, screen_height - rockfish_rect.height)

            screen.blit(rockfish_image, rockfish_rect)

        #displays player object on screen
        screen.blit(playership, playership_rect)

            # Render and display bullets
        for bullet in bullet_list:
            screen.blit(bullet['image'], bullet['rect'])

        pygame.display.update()
        clock.tick(60)




    # ... (Other game logic and rendering for different states)
    pygame.display.update()