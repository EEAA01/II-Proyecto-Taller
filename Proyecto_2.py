import pygame 
import random
pygame.font.init()
pygame.mixer.init()


# display settings 
width = 700 #ANCHO DE LA VENTANA
height = 700 #ALTO DE LA VENTANA
window = pygame.display.set_mode((width,height))
pygame.display.set_caption("Operation Moon Light")
font_type = pygame.font.SysFont("Blacklight",40)
Background = pygame.transform.scale(pygame.image.load("Imagenes\\background.png"),(width,height))
pygame.key.set_repeat(10,5)

#Import files 
player_img = pygame.image.load("Imagenes\\player.png")
enemy_img = pygame.image.load("Imagenes\\meteor1.png")

#Masks
player_mask = pygame.mask.from_surface(player_img)
enemy_mask = pygame.mask.from_surface(enemy_img)

#CARGAR SONIDO DE COLISION
collision_sound = pygame.mixer.Sound("Sonidos\\colision.wav")

#player settings

player_list =[50,300,500,5,player_img,player_mask] # 0-health 1-x value 2-y value 3-player speed 4-player img 5-player mask 

#enemies list
enemies = []

# creates all enemies and puts them on a list
for i in range (0,9):
    
    enemy_x = random.randrange(0,width-20) 
    enemy_y = random.choice ([0,height-20])
    enemyx_speed = random.randrange(0,5)
    enemyy_speed = random.randrange(0,5)
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


def main(lvl):
    FPS = 60
    run = True 
    
    #permite verificar cúal musica se va a reproducir
    if lvl == 1:
        pygame.mixer.music.load("Sonidos\\level_1.wav")#CARGA LA MUSICA
        pygame.mixer.music.play(loops=-1) #PERMITE REPRODUCIR LA MUSICA DE MANERA INFINITA

    elif lvl == 2:
         pygame.mixer.music.load("Sonidos\\level_2.ogg")#CARGA LA MUSICA
         pygame.mixer.music.play(loops=-1) #PERMITE REPRODUCIR LA MUSICA DE MANERA INFINITA
    else:
        pass
        pygame.mixer.music.load("Sonidos\\level_3.wav")#CARGA LA MUSICA
        pygame.mixer.music.play(loops=-1) #PERMITE REPRODUCIR LA MUSICA DE MANERA INFINITA

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
        enemy_move(enemies)

        pygame.draw.rect (window,(0,0,0),(0,0,width,height))
        window.blit(player_list[4],(player_list[1],player_list[2]))
        for enemy in enemies:

            if collision_detect([enemy[0],enemy[1],enemy[5]],[player_list[1],player_list[2],player_list[5]]):
                enemies.remove(enemy)
            window.blit(enemy[4],(enemy[0],enemy[1]))
               
        pygame.display.update()

    while run :
        clock.tick(FPS)

        refresh()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                
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
            pygame.mixer.music.stop()
            main (Level)

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



main_menu()
