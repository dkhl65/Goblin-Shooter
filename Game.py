from Classes import *

#objects shown on the screen
goblins = []
bullets = []
platforms = []
golds = []
decorations = []
man = Player(playerSpawnX, playerSpawnY, 64,64)
buttons = {
    "Retry": Button(100, 300, 100, "Retry"),
    "Quit": Button(300, 300, 100, "Quit"),
    "Survival": Button(windowWidth/2 - 110, 240, 240, "Survival"),
    "Swarm": Button(windowWidth/2 - 110, 290, 240, "Swarm"),
    "Adventure": Button(windowWidth/2 - 110, 340, 240, "Adventure")
}

gameMode = 0 #0 for menu, 1 for Survival, 2 for Swarm, 3 for Adventurea
goblinLoop = 0 #cycle for spawning goblins in Survival and Swarm
shootLoop = 0 #cycle for limiting the bulet firing rate
endingLoop = 0 #cycle for the death and success screens
score = 0 #player's score in Survival
timer = 0 #keeping time in Swarm and Adventure
frames = -1 #counter for 1 second to update timer
goblinsRemaining = 50 #number of goblins to kill in Swarm
goldCollected = 0 #number of gold collected in Adventure
cameraX = 0 #scrolling of objects in Adventure
backgroundX = 0 #scrolling of the background in Adventure
floor = 418 #the location of the bottom floor

#draws each frame
def redrawGameWindow():
    if gameMode == 3: #drawing the seamless scrolling background in Adventure
        window.blit(hills, (backgroundX + backgroundX // -hills.get_width() * hills.get_width(), 0))
        window.blit(hills, (backgroundX + backgroundX // -hills.get_width() * hills.get_width() + hills.get_width(), 0))
    else: #static background otherwise
        window.blit(bg, (0,0))

    if gameMode > 0:
        if gameMode == 1: #draw the score for Survival mode
            font = pygame.font.Font("arial.ttf", 20)
            text = font.render("Score: " + str(score), 1, (0,0,0))
            window.blit(text, (windowWidth-text.get_width()-10, 10))
        elif gameMode == 2 or gameMode == 3: #draw the timer
            seconds = timer
            timeString = str(timer // 60) + ":"
            seconds -= timer // 60 * 60
            if seconds < 10: timeString += "0"
            timeString += str(seconds)
            font = pygame.font.Font("arial.ttf", 20)
            text = font.render(timeString, 1, (0,0,0))
            window.blit(text, (windowWidth-text.get_width()-10, 10))

            if gameMode == 2: #draw the number of goblins remaining
                font = pygame.font.Font("arial.ttf", 20)
                text = font.render("Goblins Remaining: " + str(goblinsRemaining) + "/50", 1, (0,0,0))
                window.blit(text, (windowWidth-text.get_width()-10, 30))
            elif gameMode == 3: #draw the amount of gold collected
                font = pygame.font.Font("arial.ttf", 20)
                text = font.render("Gold: " + str(goldCollected) + "/130", 1, (0,0,0))
                window.blit(text, (windowWidth-text.get_width()-10, 30))

            #draw the HP of the player character
            font = pygame.font.Font("arial.ttf", 20)
            colour = (0,100,0)
            if man.health <= 50 and man.health >= 20: #change colour to warn of low health
                colour = (200,200,0)
            elif man.health < 20:
                colour = (150,0,0)
            text = font.render(str(man.health) + " HP", 1, colour)
            window.blit(text, (windowWidth-text.get_width()-10, 50))
            pygame.draw.rect(window, (128,128,128), (320, 55, 102, 15), 1) #health bar background
            if man.health > 0: pygame.draw.rect(window, colour, (321, 56, man.health, 13)) #health bar

        #draw game objects
        for platform in platforms:
            platform.draw(window)
        for decoration in decorations:
            decoration.draw(window)
        for goblin in goblins:
            goblin.draw(window, man.health > 0)
        for bullet in bullets:
            bullet.draw(window)
        man.draw(window)
        if gameMode == 3:
            for gold in golds:
                gold.draw(window)

        if man.health <= 0: #text shown when the player dies
            font1 = pygame.font.Font("arial.ttf", 75)
            font1.set_bold(True)
            text = font1.render("Game Over", 1, (255,0,0))
            if gameMode == 2 or gameMode == 3: text = font1.render("Failure", 1, (255,0,0))
            window.blit(text, (windowWidth/2 - (text.get_width()/2),200))
        elif (goblinsRemaining <= 0 and len(goblins) == 0) or (cameraX > 5780 and len(golds)+len(goblins) == 0 and man.land >= 0): #text shown for finishing Swarm or Adventure
            font1 = pygame.font.Font("arial.ttf", 80)
            font2 = pygame.font.Font("arial.ttf", 81)
            font1.set_bold(True)
            font2.set_bold(True)
            text = font1.render("Success", 1, (0,255,0))
            text2 = font2.render("Success", 1, (0,100,0))
            window.blit(text2, (windowWidth/2 - (text2.get_width()/2),200))
            window.blit(text, (windowWidth/2 - (text.get_width()/2),200))
    else:
        window.blit(pygame.image.load("GoblinShooter.png"), (47, 10)) #show game title on menu screen

    #draw buttons
    for k, button in buttons.items():
        button.draw(window)
        
    pygame.display.update()

#main loop
run = True
while run:
    clock.tick(frameRate)

    #check for closing of window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if gameMode == 0: #main menu
        buttons["Survival"].visible = True
        buttons["Swarm"].visible = True
        buttons["Adventure"].visible = True

        #adjust game object layouts and properties based on selected game mode
        if buttons["Survival"].checkClicked():
            gameMode = 1
            buttons["Survival"].visible = False
            buttons["Swarm"].visible = False
            buttons["Adventure"].visible = False
            pygame.mixer.music.play(-1)
            
            platforms = [Platform(windowWidth*0.5-50, 370, 122, 1),
                Platform(windowWidth*0.5-50, 170, 122, 1),
                Platform(50, 270, 122, 1),
                Platform(windowWidth-172, 270, 122, 1)]
            decorations = []
            goblins = []
            gold = []
            floor = 418
        if buttons["Swarm"].checkClicked():
            gameMode = 2
            buttons["Survival"].visible = False
            buttons["Swarm"].visible = False
            buttons["Adventure"].visible = False
            pygame.mixer.music.play(-1)
            
            platforms = [
                Platform(-5, 375, windowWidth, 1),
                Platform(-5, 155, windowWidth, 1),
                Platform(-5, 265, windowWidth, 1)]
            decorations = []
            goblins = []
            gold = []
            floor = 418
        if buttons["Adventure"].checkClicked():
            gameMode = 3
            buttons["Survival"].visible = False
            buttons["Swarm"].visible = False
            buttons["Adventure"].visible = False
            pygame.mixer.music.play(-1)
            
            platforms = [ 
                Platform(0, 450, 375, 0), 
                Platform(620, 350, 1041, 0),
                Platform(1750, 410, 375, 0),
                Platform(2200, 329, 301, 0),
                Platform(3200, 400, 301, 0),
                Platform(3870, 230, 153, 0),
                Platform(3800, 340, 301, 0),
                Platform(3700, 450, 549, 0),
                Platform(4350, 329, 227, 0),
                Platform(4970, 200, 227, 0),
                Platform(4896, 250, 301, 0),
                Platform(4822, 300, 375, 0),
                Platform(4748, 350, 449, 0),
                Platform(4674, 400, 523, 0),
                Platform(4600, 450, 597, 0),
                Platform(5500, 329, 153, 0),
                Platform(5400, 379, 153, 0),
                Platform(5300, 429, 153, 0),
                Platform(5700, 450, 597, 0),
                
                Platform(400, 400, 122, 1),
                Platform(500, 300, 122, 1),
                Platform(900, 250, 527, 1),
                Platform(1000, 150, 122, 1),
                Platform(2220, 430, 122, 1),
                Platform(2540, 250, 122, 1),
                Platform(2740, 250, 122, 1),
                Platform(2940, 250, 122, 1),
                Platform(3100, 300, 496, 1), 
                Platform(3750, 130, 122, 1),
                Platform(4403, 420, 122, 1),
                Platform(5200, 100, 122, 1),
                Platform(5322, 140, 122, 1),
                Platform(5444, 180, 122, 1),
                Platform(5566, 220, 122, 1),
                Platform(5460, 450, 153, 1)]
            golds = [Gold(420, 380), Gold(500, 380), Gold(550, 280),
                     Gold(620, 330),  Gold(720, 330), Gold(820, 330), Gold(920, 330), Gold(1020, 330), Gold(1120, 330), Gold(1220, 330), Gold(1320, 330), Gold(1420, 330), Gold(1520, 330), Gold(1620, 330),
                     Gold(900, 230), Gold(1000, 230), Gold(1100, 230), Gold(1200, 230), Gold(1300, 230), Gold(1400, 230),
                     Gold(1056, 120), Gold(1056, 40),
                     Gold(1630, 304), Gold(1650, 248), Gold(1666, 222), Gold(1695, 251), Gold(1720, 303), Gold(1750, 350),
                     Gold(1770, 380), Gold(1870, 380), Gold(1970, 380), Gold(2090, 380),
                     Gold(2222, 400), Gold(2322, 400),
                     Gold(2220, 300), Gold(2320, 300), Gold(2420, 300),
                     Gold(2640, 230), Gold(2680, 85), Gold(2740, 230), Gold(2840, 230), Gold(2880, 85), Gold(2940, 230), Gold(3090, 260),
                     Gold(3150, 280), Gold(3250, 280), Gold(3350, 280), Gold(3450, 280), Gold(3550, 280),
                     Gold(3200, 380), Gold(3300, 380), Gold(3400, 380), Gold(3500, 380),
                     Gold(3620, 300), Gold(3650, 340), Gold(3680, 400),
                     Gold(3740, 430), Gold(3840, 430), Gold(3940, 430), Gold(4040, 430), Gold(4140, 430), Gold(4240, 430),
                     Gold(3800, 320), Gold(3900, 320), Gold(4000, 320), Gold(4100, 320),
                     Gold(3890, 210), Gold(3990, 210), Gold(3806, 110),
                     Gold(4360, 350), Gold(4413, 400), Gold(4505, 400), Gold(4355, 309), Gold(4455, 309), Gold(4555, 309),
                     Gold(4975, 180), Gold(5075, 180), Gold(5175, 180), Gold(4896, 230), Gold(4996, 230), Gold(5096, 230), Gold(4852, 280), Gold(4952, 280), Gold(5052, 280), Gold(5152, 280),
                     Gold(4758, 330), Gold(4858, 330), Gold(4958, 330), Gold(5058, 330), Gold(5158, 330), Gold(4680, 380), Gold(4780, 380), Gold(4880, 380), Gold(4990, 380), Gold(5090, 380), Gold(5190, 380),
                     Gold(4640, 430), Gold(4740, 430), Gold(4840, 430), Gold(4940, 430), Gold(5040, 430), Gold(5140, 430),
                     Gold(5256, 80), Gold(5378, 120), Gold(5500, 160), Gold(5622, 200),
                     Gold(5500, 309), Gold(5400, 359), Gold(5300, 409), Gold(5441, 409), Gold(5490, 430), Gold(5590, 430)] #112 gold
            goblins = [Enemy(620, 285, 64, 64, 620, 1630), Enemy(1000, 285, 64, 64, 620, 1630), Enemy(1200, 285, 64, 64, 620, 1630), Enemy(1400, 285, 64, 64, 620, 1630), Enemy(1600, 285, 64, 64, 620, 1630),
                       Enemy(1750, 345, 64, 64, 1750, 2094), Enemy(1750, 345, 64, 64, 1750, 2094), Enemy(2200, 264, 64, 64, 2200, 2470), Enemy(3200, 235, 64, 64, 3200, 3470),
                       Enemy(3970, 385, 64, 64, 3700, 4218), Enemy(3970, 275, 64, 64, 3700, 4218), Enemy(3970, 165, 64, 64, 3700, 4218), Enemy(4350, 264, 64, 64, 4350, 4546),
                       Enemy(4600, 385, 64, 64, 4600, 5166), Enemy(4700, 335, 64, 64, 4600, 5166), Enemy(4800, 285, 64, 64, 4600, 5166), Enemy(4900, 235, 64, 64, 4600, 5166), Enemy(5000, 185, 64, 64, 4600, 5166)]
            decorations = [Decoration(5780+windowWidth/2-32, 450, sign)]
            floor = 519 #the location of the bottom floor
    elif man.health > 0 and not(goblinsRemaining <= 0 and len(goblins) == 0) and not(cameraX > 5780 and len(golds)+len(goblins) == 0 and man.land >= 0): #game is playing
        if gameMode <= 2:
            #goblin spawning
            goblinTimer = 189
            if gameMode == 1: #survival: spawn rate depends on score
                if score <= 0: goblinTimer = 7 * frameRate
                elif score >= 60: goblinTimer = 2 * frameRate
                else: goblinTimer = round(7 * frameRate - score * 2)
            elif gameMode == 2: #swarm: fixed 3 second spawn rate
                goblinTimer = 3 * frameRate
            goblinLoop += 1
            if goblinLoop == 1 and len(goblins) < 6 and goblinsRemaining-len(goblins) > 0: #spawn goblin at the end of spawn cycle
                goblins.append(Enemy(random.randint(0, 450), random.randint(0, floor-64), 64, 64, 0, 450))
                man.invincible = True #player is invincible when new goblin spawns
                man.invincibility = 1
            if goblinLoop >= goblinTimer: #repeat cycle
                goblinLoop = 0

        #count the time in Swarm and Adventure
        if gameMode == 2 or gameMode == 3:
            frames += 1
            if frames == frameRate:
                frames = 0
                timer += 1

        #processing the goblins
        for goblin in goblins:
            #deal damage to the player on collision
            if goblin.health > 0 and not(man.invincible):
                if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
                    if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2] and man.health > 0:
                        if gameMode == 1: man.hit(100)
                        elif gameMode == 2: man.hit(10)
                        else: man.hit(15)

            #remove dead goblins
            if goblin.health <= 0: 
                if gameMode == 2:
                    goblinsRemaining -= 1
                elif gameMode == 3:
                    golds.append(Gold(goblin.hitbox[0], goblin.hitbox[1]))
                goblins.pop(goblins.index(goblin))

            #goblin falling
            if goblin.jumpCount < 0 or not(goblin.isJump):
                jumpValue = (goblin.fallCount ** 2) * 0.3 #goblins fall distance due to gravity

                #check for landing on platforms
                for platform in platforms:
                    if goblin.y + jumpValue >= platform.y-goblin.height and goblin.y < platform.y-goblin.height and goblin.hitbox[0] >= platform.x-goblin.hitbox[2] and goblin.hitbox[0] <= platform.x+platform.width and goblin.land < 0 and goblin.y < floor:
                        goblin.y = platform.y-goblin.height
                        goblin.land = platforms.index(platform)

                #goblin is in the air
                if goblin.land < 0 and goblin.y < floor:
                    if goblin.y + jumpValue > floor: #check for landing on the floor
                         goblin.y = floor
                         goblin.isJump = False
                    else: #continue falling
                         goblin.y += jumpValue
                         goblin.fallCount += 1
                elif goblin.jumpCount < 0 or not(goblin.isJump): #start falling after peak of jump
                    goblin.isJump = False
                    goblin.fallCount = 0
                    goblin.jumpCount = jumpHeight

                #fall off platform if off the edge
                if goblin.land >= 0 and (goblin.hitbox[0] < platforms[goblin.land].x-goblin.hitbox[2] or goblin.hitbox[0] > platforms[goblin.land].x+platforms[goblin.land].width):
                    goblin.land = -1

            #keep track of bullets hitting goblins
            for bullet in bullets:
                if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                    if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2] and goblin.health > 0:
                        hitSound.play()
                        goblin.hit(bullet.damage)
                        score += 1
                        bullets.pop(bullets.index(bullet))

            #goblin random jumping
            if not(goblin.isJump):
                if random.randint(0, 3*frameRate) == 3 and goblin.fallCount == 0:
                    goblin.isJump = True
                    goblin.walkCount = 0
                    goblin.land = -1
                    goblin.fallCount = 0
            elif goblin.jumpCount >= 0:
                jumpValue = (goblin.jumpCount ** 2) * 0.4
                goblin.y -= jumpValue
                goblin.jumpCount -= 1

            #random reversing
            if random.randint(0, 200) == 1:
                goblin.vel = goblin.vel * -1
                goblin.walkCount = 0

            #random platform descent
            if random.randint(0, 3*frameRate) == 1 and goblin.land >= 0 and platforms[goblin.land].variety == 1:
                goblin.land = -1

        #limit player's bullet firing rate
        if shootLoop > 0:
            shootLoop += 1
        if shootLoop > 10:
            shootLoop = 0

        #move the bullets                
        for bullet in bullets:         
            if bullet.x < windowWidth + 30 and bullet.x > -30:
                bullet.x += bullet.vel
            else: #remove off-screen bullets
               bullets.pop(bullets.index(bullet))

        #keep track of collisions with gold pieces for collecting
        for gold in golds:
            if man.hitbox[1] < gold.hitbox[1] + gold.hitbox[3] and man.hitbox[1] + man.hitbox[3] > gold.hitbox[1]:
                if man.hitbox[0] + man.hitbox[2] > gold.hitbox[0] and man.hitbox[0] < gold.hitbox[0] + gold.hitbox[2]:
                    golds.pop(golds.index(gold))
                    goldCollected += 1
           
        #key controls
        keys = pygame.key.get_pressed()

        #shoot a bullet
        if (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]) and shootLoop == 0:
            bulletSound.play()
            if man.left:
                facing = -1
            else:
                facing = 1
            bullets.append(Projectile(round(man.x + man.width //2), round(man.y + man.height//2), 6, (0,0,0), facing, 3, 20))
            shootLoop = 1

        #directional movement
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and man.x > 0: #move the player left
            if gameMode <= 2 or cameraX <= 0: #actualy moving the sprite
                man.x -= man.vel
            else: #in Adventure, move all objects so it looks like the camera is moving
                for platform in platforms:
                    platform.x += man.vel
                for gold in golds:
                    gold.x += man.vel
                for decoration in decorations:
                    decoration.x += man.vel
                for goblin in goblins:
                    goblin.path[0] += man.vel
                    goblin.path[1] += man.vel
                    goblin.x += man.vel
                    
                backgroundX += man.vel/5 #move the background image slower

            cameraX -= man.vel #keep track of the player's position in the world
            man.left = True
            man.right = False
            man.standing = False
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (man.x < windowWidth - man.width or gameMode > 2): #move the player right
            if gameMode <= 2 or cameraX < 0: #actually moving the sprite
                man.x += man.vel
            else: #in Adventure, move all objects so it looks like the camera is moving
                for platform in platforms:
                    platform.x -= man.vel
                for gold in golds:
                    gold.x -= man.vel
                for decoration in decorations:
                    decoration.x -= man.vel
                for goblin in goblins:
                    goblin.path[0] -= man.vel
                    goblin.path[1] -= man.vel
                    goblin.x -= man.vel
                backgroundX -= man.vel/5 #move the background image slower

            cameraX += man.vel #keep track of the player's position in the world
            man.right = True
            man.left = False
            man.standing = False
        else: #stand still, facing the same way
            man.standing = True
            man.walkCount = 0

        #jumping
        if not(man.isJump):
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and man.fallCount == 0 and (man.y == floor or man.land >= 0): #jumping works only when touching a surface
                man.isJump = True
                man.walkCount = 0
                man.land = -1
                man.fallCount = 0
        elif man.jumpCount >= 0: #moving up in the air 
            jumpValue = (man.jumpCount ** 2) * 0.4
            man.y -= jumpValue
            man.jumpCount -= 1

        #going down from platforms
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and man.land > -1 and platforms[man.land].variety == 1:
            man.land = -1

        #man falling
        if man.jumpCount < 0 or not(man.isJump):
            jumpValue = (man.fallCount ** 2) * 0.3
            if jumpValue > 20: jumpValue = 20

            #check for landing on platforms
            for platform in platforms:
                if man.y + jumpValue >= platform.y-man.height and man.y < platform.y-man.height and man.hitbox[0] >= platform.x-man.hitbox[2] and man.hitbox[0] <= platform.x+platform.width and man.land < 0 and man.y < floor:
                    man.y = platform.y-man.height
                    man.land = platforms.index(platform)

            #man is in the air
            if man.land < 0 and man.y < floor:
                if man.y + jumpValue > floor: #landing on floor
                     man.y = floor
                     man.isJump = False
                else: #keep falling
                     man.y += jumpValue
                     man.fallCount += 1
            elif man.jumpCount < 0 or not(man.isJump): #start falling after peak of jump
                man.isJump = False
                man.fallCount = 0
                man.jumpCount = jumpHeight

            if man.land >= 0 and (man.hitbox[0] < platforms[man.land].x-man.hitbox[2] or man.hitbox[0] > platforms[man.land].x+platforms[man.land].width): #walking off a platform
                man.land = -1
        if man.y > 500: man.hit(100) #falling to death
    elif man.health <= 0 and endingLoop < 8*frameRate: #man has just died
        if endingLoop == frameRate//9: #start death sound a few frames after man is dead
            pygame.mixer.music.stop()
            deathSound.play()
        if endingLoop > 4*frameRate: man.y += 10 #man slides down the screen
        endingLoop += 1 #count the death screen cycle
    elif (goblinsRemaining <= 0 and len(goblins) == 0) or (cameraX > 5780 and man.land >= 0): #success conditions for Swarm and Adventure
        if endingLoop == 0:
            pygame.mixer.music.stop()
            successSound.play()
            man.standing = True #man stands still
            man.walkCount = 0
        endingLoop += 1 #count the success screen cycle

    #handle quitting or retrying game
    if endingLoop >= 8*frameRate or (((goblinsRemaining <= 0 and len(goblins) == 0) or (cameraX > 5780 and len(golds)+len(goblins) == 0 and man.land >= 0)) and endingLoop >= 3*frameRate):
        buttons["Retry"].visible = True
        buttons["Quit"].visible = True
        retry = buttons["Retry"].checkClicked()
        menu = buttons["Quit"].checkClicked()
        
        if retry or menu:
            if retry:
                pygame.mixer.music.play(-1)
                if cameraX > 0 and gameMode == 3: #return platforms and decorations to initial positions
                    for platform in platforms:
                        platform.x += cameraX
                    for decoration in decorations:
                        decoration.x += cameraX

                    #reset Adventure removable objects
                    golds = [Gold(420, 380), Gold(500, 380), Gold(550, 280),
                        Gold(620, 330),  Gold(720, 330), Gold(820, 330), Gold(920, 330), Gold(1020, 330), Gold(1120, 330), Gold(1220, 330), Gold(1320, 330), Gold(1420, 330), Gold(1520, 330), Gold(1620, 330),
                        Gold(900, 230), Gold(1000, 230), Gold(1100, 230), Gold(1200, 230), Gold(1300, 230), Gold(1400, 230),
                        Gold(1056, 120), Gold(1056, 40),
                        Gold(1630, 304), Gold(1650, 248), Gold(1666, 222), Gold(1695, 251), Gold(1720, 303), Gold(1750, 350),
                        Gold(1770, 380), Gold(1870, 380), Gold(1970, 380), Gold(2090, 380),
                        Gold(2222, 400), Gold(2322, 400),
                        Gold(2220, 300), Gold(2320, 300), Gold(2420, 300),
                        Gold(2640, 230), Gold(2680, 85), Gold(2740, 230), Gold(2840, 230), Gold(2880, 85), Gold(2940, 230), Gold(3090, 260),
                        Gold(3150, 280), Gold(3250, 280), Gold(3350, 280), Gold(3450, 280), Gold(3550, 280),
                        Gold(3200, 380), Gold(3300, 380), Gold(3400, 380), Gold(3500, 380),
                        Gold(3620, 300), Gold(3650, 340), Gold(3680, 400),
                        Gold(3740, 430), Gold(3840, 430), Gold(3940, 430), Gold(4040, 430), Gold(4140, 430), Gold(4240, 430),
                        Gold(3800, 320), Gold(3900, 320), Gold(4000, 320), Gold(4100, 320),
                        Gold(3890, 210), Gold(3990, 210), Gold(3806, 110),
                        Gold(4360, 350), Gold(4413, 400), Gold(4505, 400), Gold(4355, 309), Gold(4455, 309), Gold(4555, 309),
                        Gold(4975, 180), Gold(5075, 180), Gold(5175, 180), Gold(4896, 230), Gold(4996, 230), Gold(5096, 230), Gold(4852, 280), Gold(4952, 280), Gold(5052, 280), Gold(5152, 280),
                        Gold(4758, 330), Gold(4858, 330), Gold(4958, 330), Gold(5058, 330), Gold(5158, 330), Gold(4680, 380), Gold(4780, 380), Gold(4880, 380), Gold(4990, 380), Gold(5090, 380), Gold(5190, 380),
                        Gold(4640, 430), Gold(4740, 430), Gold(4840, 430), Gold(4940, 430), Gold(5040, 430), Gold(5140, 430),
                        Gold(5256, 80), Gold(5378, 120), Gold(5500, 160), Gold(5622, 200),
                        Gold(5500, 309), Gold(5400, 359), Gold(5300, 409), Gold(5441, 409), Gold(5490, 430), Gold(5590, 430)] 
                    goblins = [Enemy(620, 285, 64, 64, 620, 1630), Enemy(1000, 285, 64, 64, 620, 1630), Enemy(1200, 285, 64, 64, 620, 1630), Enemy(1400, 285, 64, 64, 620, 1630), Enemy(1600, 285, 64, 64, 620, 1630),
                               Enemy(1750, 345, 64, 64, 1750, 2094), Enemy(1750, 345, 64, 64, 1750, 2094), Enemy(2200, 264, 64, 64, 2200, 2470), Enemy(3200, 235, 64, 64, 3200, 3470),
                               Enemy(3970, 385, 64, 64, 3700, 4218), Enemy(3970, 275, 64, 64, 3700, 4218), Enemy(3970, 165, 64, 64, 3700, 4218), Enemy(4350, 264, 64, 64, 4350, 4546),
                               Enemy(4600, 385, 64, 64, 4600, 5166), Enemy(4700, 335, 64, 64, 4600, 5166), Enemy(4800, 285, 64, 64, 4600, 5166), Enemy(4900, 235, 64, 64, 4600, 5166), Enemy(5000, 185, 64, 64, 4600, 5166)]
            if menu:
                gameMode = 0 #quit to main menu

            #reset game properties
            man.reset()
            score = 0
            if gameMode != 3:
                goblins.clear()
            bullets.clear()
            goblinLoop = 0
            shootLoop = 0
            endingLoop = 0
            score = 0
            timer = 0
            frames = -1
            goblinsRemaining = 50
            cameraX = 0
            backgroundX = 0
            goldCollected = 0

            buttons["Retry"].visible = False
            buttons["Quit"].visible = False
            
    redrawGameWindow()

pygame.quit()
