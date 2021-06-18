import pygame 
import random
import time
pygame.font.init()
pygame.mixer.init()


# display settings 
width = 700 #ANCHO DE LA VENTANA
height = 700 #ALTO DE LA VENTANA
window = pygame.display.set_mode((width,height))
pygame.display.set_caption("Operation Moon Light")
font_type = pygame.font.SysFont("Blacklight",40)
Background = pygame.transform.scale(pygame.image.load("Imagenes\\background.png"),(width,height))


#Import files 
player_img = pygame.image.load("Imagenes\\player.png")
enemy_img = pygame.image.load("Imagenes\\meteor1.png")
instructions = pygame.image.load("Imagenes\\instrucciones.png")
about = pygame.image.load("Imagenes\\about.png")
highscore_path = ("Imagenes\\highscore.txt")

#Masks
player_mask = pygame.mask.from_surface(player_img)
enemy_mask = pygame.mask.from_surface(enemy_img)

#CARGAR SONIDO DE COLISION
collision_sound = pygame.mixer.Sound("Sonidos\\colision.wav")

#player settings

player_list =[3,300,500,5,player_img,player_mask,0,""] # 0-health 1-x value 2-y value 3-player speed 4-player img 5-player mask 6-Score 7- Name

#enemies list
enemies = []

#Timer
time_list = [0,55]

#controls time and score based on time
def Timer (time_list,lvl):
    if time_list[0] == 60: # counts seconds
        time_list[1] += 1
        time_list[0] = 0 
        if lvl == 1:
            player_list[6] +=1
        if lvl == 2:
            player_list[6] += 3
        if lvl == 3:
            player_list[6] += 5
    else:
        time_list[0] +=1
    

# creates all enemies and puts them on a list
def enemy_creation (num):
    for i in range (0,num):
    
        enemy_x = random.randrange(2,width-20) 
        enemy_y = random.choice ([2,height-20])
        enemyx_speed = random.randrange(0,8)
        enemyy_speed = random.randrange(0,8)
        enemy = [enemy_x,enemy_y,enemyx_speed,enemyy_speed,enemy_img,enemy_mask] # 0- x 1-y 2-x speed 3- y speed 4-image 5-mask
        enemies.append(enemy)

def collision_detect (obj1,obj2): #FUNCION PARA DETECTAR COLISIONES 
    obj1_x = obj1[0]
    obj1_y = obj1[1]
    obj2_x = obj2[0]
    obj2_y = obj2[1]
    obj1_mask = obj1[2]
    obj2_mask = obj2[2]
    

    offsetx = int(obj2_x - obj1_x)
    offsety = int(obj2_y - obj1_y)
    result = obj1_mask.overlap (obj2_mask,(offsetx,offsety))
    
    if result != None:
        collision_sound.play()
        return True 
    else:

        return False

def Lost(window): # Game over screen 
     run = True
     lost_font = pygame.font.SysFont("comicsansms",100) # creates a font
     lost_label = lost_font.render("GAME OVER!",1,(255,255,255))# Creates the label
     while run:     
        window.blit (lost_label,((width/2)-(lost_label.get_width()/2),(height/2)-lost_label.get_height()/2))# puts the label on screen 
        pygame.display.update()
        time.sleep(2)
        for event in pygame.event.get():# checks for any pressed key
           if event.type == pygame.KEYDOWN:
                main_menu()

def level_passed(window,Level):
    pygame.key.set_repeat(50,5)
    run = True
    bonus = 0
    if Level == 1:
        bonus = 5* player_list[0]
    if Level == 2:
        bonus = 10* player_list[0]

        

    win_font = pygame.font.SysFont("comicsansms",80)
    bonus_font = pygame.font.SysFont("comicsansms",50)
    game_text = pygame.font.SysFont("Blacklight",40)
    win_label = win_font.render("LEVEL PASSED!",1,(255,255,255))
    bonus_label = bonus_font.render ("Perfect level! +10 points",1,(255,255,255))
    live_bonus_label = bonus_font.render("Live bonus! +" + str(bonus) +" points" ,1,(255,255,255))
    if player_list[0] == 3:     
        
        player_list[6] += 10
    
    player_list[6] += bonus
    while run:
        window.blit (win_label,((width/2)-(win_label.get_width()/2),(height/2)-win_label.get_height()/2))
        
        window.blit(live_bonus_label,((width/2)-(live_bonus_label.get_width()/2),height-live_bonus_label.get_height()-bonus_label.get_height()-10))
        if player_list[0] == 3:     
            window.blit (bonus_label,((width/2)-(bonus_label.get_width()/2),height-bonus_label.get_height()-10))
            player_list[6] += 10

        score_label = game_text.render("Score: {}".format(player_list[6]),1,(255,255,255))

        pygame.display.update()
        time.sleep(2)
        for event in pygame.event.get():
           if event.type == pygame.KEYDOWN:
                run = False
                time_list[0] = 0
                time_list[1] = 55
                main(Level+1,player_list[6],player_list[7])
           if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    
def score_screen (window,score,name):
    run = True
    if player_list[0] != 0:
       player_list[6] += 15* player_list[0]

    score_font = pygame.font.SysFont("comicsansms",60)
    bonus_font = pygame.font.SysFont("comicsansms",50)
    score_label = score_font.render("YOU WIN!",1,(255,255,255))
    score2_label = score_font.render ("Your score is: {}".format(score),1,(255,255,255))
    bonus_label = bonus_font.render ("Perfect level! +10 points",1,(255,255,255))
    high_label = bonus_font.render ("High Score!",1,(255,255,255))
    

   
    added = False
    #function to check if the player's score is a highscore

    def highscore_check (added,name):
        #opens the txtfile
        highscore_file = open(highscore_path, "r+")
        highscore_list = []
        #creates a list of the highscore names and scores
        highscore_list = highscore_file.readlines()

        #removes the \n character and splits each individual into a list, getting a matrix [[name,score],[name2,score2]
        for i in range (0,len(highscore_list)-1):
            highscore_list[i] = highscore_list[i].rstrip("\n")
            highscore_list[i] = highscore_list[i].split(",")
            #checks for the score element of the matrix and adds the highscore if needed
            if score > int (highscore_list[i][1]) and added != True:
                highscore_list[i][0] = name 
                highscore_list[i][1] = score
                window.blit (high_label,((width/2)-(high_label.get_width()/2),(height/2)-high_label.get_height()+50+score_label.get_height()+50+score2_label.get_height()+50))
                added= True
        #sets the cursor back to the begining of the file
        highscore_file.seek(0)
        #writes the list of highscore on the same format it was readed.
        for i in range (0,len(highscore_list)-1):
            new_text = highscore_list[i][0] +  "," + str(highscore_list[i][1]) + "\n"
            highscore_file.write (new_text)
        #closes file to save changes.
        highscore_file.close()
        print(score)
        print(highscore_list)

    highscore_check(False,name)

    while run: 
        #sets a screen for the last level passed, shows the score and any bonus obtained 
        window.blit (score_label,((width/2)-(score_label.get_width()/2),(height/2)-score_label.get_height()/2))
        window.blit (score2_label,((width/2)-(score2_label.get_width()/2),(height/2)-score2_label.get_height()+50+score_label.get_height()+50))
       
        pygame.display.update()
        for event in pygame.event.get():
           if event.type == pygame.KEYDOWN:
                run = False
                main_menu()

   

def main(lvl,score, name):
    FPS = 60
    run = True 
    pygame.key.set_repeat(50,5)

    if lvl == 1:
        pygame.mixer.music.load("Sonidos\\level_1.wav")#CARGA LA MUSICA
        pygame.mixer.music.play(loops=-1) #PERMITE REPRODUCIR LA MUSICA DE MANERA INFINITA
        enemy_creation (7)

    elif lvl == 2:
         pygame.mixer.music.load("Sonidos\\level_2.ogg")#CARGA LA MUSICA
         pygame.mixer.music.play(loops=-1) #PERMITE REPRODUCIR LA MUSICA DE MANERA INFINITA
         enemy_creation (9)
    else:
        pass
        pygame.mixer.music.load("Sonidos\\level_3.wav")#CARGA LA MUSICA
        pygame.mixer.music.play(loops=-1) #PERMITE REPRODUCIR LA MUSICA DE MANERA INFINITA
        enemy_creation (11)

    game_text = pygame.font.SysFont("Blacklight",40)

    
    
    #permite verificar cúal musica se va a reproducir


    def enemy_move (enemy_list):
        for enemy in enemies: 

            x = enemy [0]
            y = enemy [1]
            x_speed = enemy [2]
            y_speed = enemy [3]
        
            if x + x_speed + 20 < width and x + x_speed > 2:
                enemy[0] = enemy[0]+x_speed

            elif x + x_speed + 20 >= width or x + x_speed <= 15:
        
                enemy[2] = enemy[2]*-1
            
            if y + y_speed + 20 < height and y + y_speed > 0:
                enemy [1] += y_speed
            elif  y + y_speed + 20 >= width or y + y_speed <= 0:
                enemy[3] = y_speed * -1
            

    
    clock = pygame.time.Clock()
    # refreshes all functions and the screen 
    def refresh():
        Timer (time_list,lvl)
        enemy_move(enemies)
        window.blit(Background,(0,0))
        health_label = game_text.render("Lives: {}".format(player_list[0]),1,(255,255,255))
        level_label = game_text.render("Level: {}".format(lvl),1,(255,255,255))
        score_label = game_text.render("Score: {}".format(player_list[6]),1,(255,255,255))
        time_label = game_text.render("Time: {}".format(time_list[1]),1,(255,255,255))
        name_label = game_text.render (name,1,(255,255,255))
        window.blit(player_list[4],(player_list[1],player_list[2]))
        

        for enemy in enemies:

            if collision_detect([enemy[0],enemy[1],enemy[5]],[player_list[1],player_list[2],player_list[5]]):
                enemies.remove(enemy)
                player_list[0] -=1
            


            window.blit(enemy[4],(enemy[0],enemy[1]))

        window.blit(health_label,(10,height - health_label.get_height() -10 ))
        window.blit(level_label,(width - 10 - level_label.get_width(), height- level_label.get_height() -10) )
        window.blit(name_label,(width/2-name_label.get_width()/2,10))
        window.blit(score_label,(10,10))
        window.blit(time_label,(width-time_label.get_width()-10,10))
        if player_list[0] <= 0:
            Lost(window)
        if time_list[1] == 60:
            if lvl == 3:
                score_screen (window, player_list[6],player_list[7])
            else:
                level_passed(window,lvl)
            
       
               
        pygame.display.update()

    while run :
        clock.tick(FPS)
        

        refresh()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            pressed_keys= pygame.key.get_pressed()
            if pressed_keys[pygame.K_LEFT] and player_list[1] - player_list[3] > 0:
                player_list[1] -= player_list[3]
            if pressed_keys[pygame.K_RIGHT] and player_list[1] + player_list[3] + player_img.get_width() - 5 < width:
                player_list[1] += player_list[3]
            if pressed_keys[pygame.K_UP] and player_list[2] - player_list[3] > 0:
                player_list[2] -= player_list[3]
            if pressed_keys[pygame.K_DOWN] and player_list[2] + player_list[3] + player_img.get_height() -5 < height:
                player_list[2] += player_list[3]
            

def main_menu():

    runmain = True
    title_font = pygame.font.SysFont("comicsansms",90)
    menu_items_font = pygame.font.SysFont("comicsansms",50)
    menu_instructions_font = pygame.font.SysFont("comicsansms",15)
    
    #PERMITE INGRESAR LA MUSICA DE FONDO
    pygame.mixer.music.load("Sonidos\\principal.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)

    selector = 1
    Level = 1
    choice = False 
    FPS = 20
    clock = pygame.time.Clock()
    
    def about(window):
        run = True
        while run:     
              window.blit(about,(0,0) )
              pygame.display.update()
              for event in pygame.event.get():
                  if event.type == pygame.KEYDOWN:
                     run = False 
                     main_menu()

    def Instructions_screen():
            run = True
            window.blit(instructions,(0,0))
            pygame.display.update()
            time.sleep(1)
            while run:     

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        run = False 
                        main_menu()

    def highscore_screen(window, highscore_path):
        run = True
        highscore_font = pygame.font.SysFont("comicsansms",30)
        highscore_font2 = pygame.font.SysFont("comicsansms",70)
        highscore_label1 = highscore_font2.render("High score board",1,(255,255,255))
        file = open(highscore_path, "r")
        text = file.readlines()
        
        window.blit(Background,(0,0))
        window.blit (highscore_label1,((width/2)-highscore_label1.get_width()/2,15))
        
        while run:
            l = 0 
            
            for i in range (0,len(text)):
                l += 50

                highscore_label = highscore_font.render(str(text[i].rstrip("\n")),1,(255,255,255))
                
                window.blit (highscore_label,((width/2 -highscore_label.get_width()/2),highscore_label1.get_height()+20+l))
                pygame.display.update()

            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    run = False
                    main_menu()

    def Name_write (window, Level):
        run = True
        base_font = pygame.font.SysFont("NONE",70)
        base_font1 = pygame.font.SysFont("NONE",40)
        base_label = base_font1.render("Type your name and press enter to start..",1,(255,255,255))
        pygame.key.set_repeat(100,1)
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
                        player_list[0] = 3
                        player_list[6] = 0
                        player_list [7] = user_text
                        time_list[0] = 0
                        #time_list[1]= 0
                        main(Level,0,player_list[7])
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
        menu_instructions_label = menu_instructions_font.render("Use the UP or DOWN keys to navigate the menu and the space bar to select",1,(255,255,255))
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
            pygame.mixer.music.stop()
            player_list[0] = 3  
            Name_write(window,Level)

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
        if pressed_keys[pygame.K_UP]:
            if selector >1:
               selector -= 1 
        if pressed_keys[pygame.K_DOWN]:
            if selector < 4:
               selector += 1
        if pressed_keys[pygame.K_LEFT]:
            if Level > 1:
               Level -= 1
        if pressed_keys[pygame.K_RIGHT]:
            if Level < 3:
               Level += 1
        if pressed_keys[pygame.K_SPACE]:
            choice = True 



main_menu()
