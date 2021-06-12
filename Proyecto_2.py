import pygame 
import random
pygame.font.init()


# display settings 
width = 700
height = 1000
window = pygame.display.set_mode((width,height))
pygame.display.set_caption("Meteorite rain")
font_type = pygame.font.SysFont("Blacklight",40)
#Background = pygame.transform.scale(pygame.image.load(r"C:\Users\Brad\Desktop\Intro-Taller\Proyecto 1. Brad Sardi\Files\background.png"),(width,height))

#player settings

player_list =[50,300,800,10] # 0-health 1-x value 2-y value 3-player speed 

enemies = []
for i in range (0,5):
    
    enemy_x = random.randrange(0,width-20) 
    enemy_y = random.choice ([0,height-20])
    enemyx_speed = random.randrange(5,10)
    enemyy_speed = random.randrange(5,10)
    enemy = [enemy_x,enemy_y,enemyx_speed,enemyy_speed]
    enemies.append(enemy)

def main():
    #main game loop 
    FPS = 60
    run = True 
    #movement for enemy
    def enemy_move (enemy_list):
        for enemy in enemies: 

            x = enemy [0]
            y = enemy [1]
            x_speed = enemy [2]
            y_speed = enemy [3]
        #print (x_speed)
            if x + x_speed + 20 < width and x + x_speed > 2:
                enemy[0] = enemy[0]+x_speed
                #print(x)

            elif x + x_speed + 20 >= width or x + x_speed <= 15:
            
                enemy[2] = enemy[2]*-1
                #print(enemy[2])
            
            if y + y_speed + 20 < height and y + y_speed > 0:
                enemy [1] += y_speed
            elif  y + y_speed + 20 >= width or y + y_speed <= 0:
                enemy[3] = y_speed * -1
            

    clock = pygame.time.Clock()
    # refreshes the new image on the screen  
    def refresh():
       
        #background
        pygame.draw.rect (window,(0,0,0),(0,0,width,height))
        #window.blit(Background,(0,0))
        #player
        pygame.draw.rect (window,(255,0,0),(player_list[1],player_list[2],70,70))
        #enemy 
       for enemy in enemies:
            pygame.draw.rect (window,(0,255,0),(enemy[0],enemy[1],20,20))
               
        pygame.display.update()

    while run :
        clock.tick(FPS)



        refresh()
        #Checks if the user has quit the game 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                
            pressed_keys= pygame.key.get_pressed()
            #checkes which key the user has pressed and acts accordingly 
            if pressed_keys[pygame.K_a] and player_list[1] - player_list[3] > 0:
                player_list[1] -= player_list[3]
            if pressed_keys[pygame.K_d] and player_list[1] + player_list[3] + 70-5 < width:
                player_list[1] += player_list[3]
            if pressed_keys[pygame.K_w] and player_list[2] - player_list[3] > 0:
                player_list[2] -= player_list[3]
            if pressed_keys[pygame.K_s] and player_list[2] + player_list[3] + 70-5< height:
                player_list[2] += player_list[3]
            

def main_menu():

    runmain = True
    title_font = pygame.font.SysFont("comicsansms",90)
    menu_items_font = pygame.font.SysFont("comicsansms",50)
    menu_instructions_font = pygame.font.SysFont("comicsansms",15)

    selector = 1
    Level = 1
    choice = False 
    FPS = 20
    clock = pygame.time.Clock()
    
    def about(window):
        run = True
        while run:     
              window.blit(About_image,(0,0) )
              pygame.display.update()
              for event in pygame.event.get():
                  if event.type == pygame.KEYDOWN:
                     run = False 
                     main_menu()

    def Instructions_screen():
            run = True
            print ("instructions")
            while run:     
                
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        run = False 
                        main_menu()

    def highscore_screen(window, highscore_path):
        run = True    
        print ("highscore")
        while run:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    run = False
                    main_menu()

    def Name_write (window, Level):
        run = True
        base_font = pygame.font.SysFont("NONE",70)
        base_font1 = pygame.font.SysFont("NONE",40)
        base_label = base_font1.render("Type your name and press enter to start..",1,(255,255,255))
        user_text = ""
        
        
        print ("write name")
        while run:
            window.blit(Background,(0,0))
            window.blit (base_label,(width/2-base_label.get_width()/2,20))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 
                    main_menu()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        run = False
                        main()
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else: 
                        user_text += event.unicode
                   
                    
                        
                

            user_label = base_font.render(user_text,1,(255,255,255))
            window.blit(user_label,(width/2 -user_label.get_width()/2,height/2))

            pygame.display.update()

                                                



    
   


    while runmain:
        clock.tick(FPS)
        window.blit(Background,(0,0))
        
        title_label= title_font.render ("Main Menu",1,(255,255,255))
        start_game_label = menu_items_font.render ( "Start!",1,(255,255,255)) 
        about_label = menu_items_font.render ("About the game",1,(255,255,255)) 
        instructions_label = menu_items_font.render ("How to play",1,(255,255,255))
        menu_instructions_label = menu_instructions_font.render("Use the W or S keys to navigate the menu and the space bar to select",1,(255,255,255))
        level_label = menu_instructions_font.render("Level: {}".format(Level),1,(255,255,255))
        highscore_label = menu_items_font.render("Highscore Board",1,(255,255,255))
        

        window.blit ( title_label,(width/2 - title_label.get_width()/2,50))
        pygame.draw.rect(window,(0,255,0),((width/2)-start_game_label.get_width()/2,title_label.get_height()+50,start_game_label.get_width(),start_game_label.get_height()))
        pygame.draw.rect(window,(0,255,0),((width/2)-instructions_label.get_width()/2,title_label.get_height()+50+start_game_label.get_height()+50,instructions_label.get_width(),instructions_label.get_height()))
        pygame.draw.rect(window,(0,255,0),((width/2)-about_label.get_width()/2,title_label.get_height()+50+start_game_label.get_height()+50+about_label.get_height()+50,about_label.get_width(),about_label.get_height()))
        pygame.draw.rect(window,(0,255,0),((width/2)-highscore_label.get_width()/2,title_label.get_height()+50+start_game_label.get_height()+50+about_label.get_height()+50+highscore_label.get_height()+50,highscore_label.get_width(),highscore_label.get_height()))
        if selector == 1:
            pygame.draw.rect(window,(0,110,0),((width/2)-start_game_label.get_width()/2,title_label.get_height()+50,start_game_label.get_width(),start_game_label.get_height()))
        elif selector == 2:
            pygame.draw.rect(window,(0,110,0),((width/2)-instructions_label.get_width()/2,title_label.get_height()+50+start_game_label.get_height()+50,instructions_label.get_width(),instructions_label.get_height()))
        elif selector == 3:
            pygame.draw.rect(window,(0,110,0),((width/2)-about_label.get_width()/2,title_label.get_height()+50+start_game_label.get_height()+50+about_label.get_height()+50,about_label.get_width(),about_label.get_height()))
        elif selector == 4:
             pygame.draw.rect(window,(0,110,0),((width/2)-highscore_label.get_width()/2,title_label.get_height()+50+start_game_label.get_height()+50+about_label.get_height()+50+highscore_label.get_height()+50,highscore_label.get_width(),highscore_label.get_height()))


        window.blit (start_game_label,(width/2 - start_game_label.get_width()/2,title_label.get_height()+50))
        window.blit (instructions_label,(width/2 -instructions_label.get_width()/2,title_label.get_height()+50+start_game_label.get_height()+50))
        window.blit (about_label,(width/2 -about_label.get_width()/2,title_label.get_height()+50+start_game_label.get_height()+50+about_label.get_height()+50))
        window.blit (highscore_label,(width/2 -highscore_label.get_width()/2,title_label.get_height()+50+start_game_label.get_height()+50+about_label.get_height()+50+highscore_label.get_height()+50))
        window.blit (menu_instructions_label,(10,height-menu_instructions_label.get_height()-10))
        window.blit (level_label,(width-level_label.get_width()-5,height-level_label.get_height()-10))
        

        if selector == 1 and choice == True:

            main ()
        elif selector == 2 and choice == True:
             Instructions_screen()
        elif selector == 3 and choice == True:
             about (window)
        elif selector == 4 and choice == True:
             highscore_screen(window, highscore_path)



        


        pygame.display.update() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pressed_keys= pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            if selector >1:
               selector -= 1 
        if pressed_keys[pygame.K_s]:
            if selector < 4:
               selector += 1
        if pressed_keys[pygame.K_a]:
            if Level > 1:
               Level -= 1
        if pressed_keys[pygame.K_d]:
            if Level < 3:
               Level += 1
        if pressed_keys[pygame.K_SPACE]:
            choice = True 



main()
