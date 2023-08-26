import pygame
import random
import os 

pygame.init()

#게임 배경 크기
screen_width=640
screen_height=480

screen=pygame.display.set_mode((screen_width,screen_height))

#게임 이름
pygame.display.set_caption("pang")

clock=pygame.time.Clock()
current_path=os.path.dirname(__file__)
image_path= os.path.join(current_path,"img")

background=pygame.image.load(os.path.join(image_path,"배경.png"))

#스테이지 만들기
stage=pygame.image.load(os.path.join(image_path,"바닥.png"))
stage_size=stage.get_rect().size
stage_height=stage_size[1]

#캐릭터#################################################################
character=pygame.image.load(os.path.join(image_path,"캐릭터.png"))
character_size=character.get_rect().size
character_width=character_size[0]
character_height=character_size[1]
character_x_pos=(screen_width/2)-(character_width/2)
character_y_pos=(screen_height-character_height-stage_height)


#캐익터 이동 방향
character_to_x=0
character_to_y=0
#캐릭터  스피드
character_speed=0.25
#######################################################################

# 무기 만들기
weapon=pygame.image.load(os.path.join(image_path,"무기.png"))
weapon_size =weapon.get_rect().size
weapon_width=weapon_size[0]

#무기는 한 번에 여러 발 발사 가능
weapons=[]

weapon_speed=10
#########################################################################

#공 만들기
ball_images = [  
    pygame.image.load(os.path.join(image_path,"공1.png")),
    pygame.image.load(os.path.join(image_path,"공2.png")),
    pygame.image.load(os.path.join(image_path,"공3.png")),
    pygame.image.load(os.path.join(image_path,"공4.png"))]

#공 크기에 따른 최초 스피드
ball_speed_y=[-18,-14,-12,-10]

balls=[]

balls.append({
    "pos_x":50,#공의 x좌표
    "pos_y":50,#공의 y좌표
    "img_idx":0,#공의 이미지 인덱스
    "to_x":3,#x축 이동방향
    "to_y":-6,#y축 이동방향
    "init_speed_y": ball_speed_y[0]})

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove=-1
ball_to_remove=-1

game_font=pygame.font.Font(None, 40)
retry_font=pygame.font.Font(None,60)


#총 시간
total_time=30

#시작 시간
start_ticks=pygame.time.get_ticks()#시작 tick을 받아옴
#배경 음악
bgsound= pygame.mixer.Sound("C:/Users/isacc/Desktop/panggame/배경음악.wav")
bgsound.play(-1)

running = True#게임이 진행 중인가?
while running:
    dt=clock.tick(50)
    for event in pygame.event.get():
        if event.type==pygame.QUIT: #창 종료 이벤트 발생 하였는가?
            running=False#게임 진행 중이 아님
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key==pygame.K_RIGHT:
                character_to_x+=character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos=character_x_pos+(character_width/2)-(weapon_width/2)
                weapon_y_pos=character_y_pos
                weapons.append([weapon_x_pos,weapon_y_pos])
            if character_y_pos==screen_height-character_height-stage_height:
                if event.key==pygame.K_UP:#캐릭터 위로
                    character_to_y-=2
        if event.type==pygame.KEYUP: #방향키를 떼면 멈춤
            if event.key == pygame.K_LEFT or event.key ==pygame.K_RIGHT:
                character_to_x=0
            elif event.key == pygame.K_UP or event.key ==pygame.K_DOWN:
                character_to_y=0
    character_x_pos+=character_to_x*dt
    character_y_pos+=(character_to_y *dt)+10

    
    #가로 경계값 처리
    if character_x_pos<0:
        character_x_pos=0
    elif character_x_pos>screen_width-character_width:
        character_x_pos=screen_width-character_width
    #세로 경계값 처리
    if character_y_pos<=200:
        character_y_pos=200 
    elif character_y_pos>screen_height-character_height-stage_height:
        character_y_pos=screen_height-character_height-stage_height
   #무기 위치 조정
    weapons=[[w[0],w[1] -weapon_speed] for w in weapons]#무기 위치를 위로  올림
    weapons=[[w[0],w[1]]for w in weapons if w[1]>0] #천장에 닿은 무기 없애기

    #공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x=ball_val["pos_x"]
        ball_pos_y=ball_val["pos_y"]
        ball_img_idx=ball_val["img_idx"]
        
        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width=ball_size[0]
        ball_height=ball_size[1]

        if ball_pos_x<0 or ball_pos_x>screen_width-ball_width:
            ball_val["to_x"]= ball_val["to_x"]*-1

        if ball_pos_y>= screen_height-stage_height-ball_height:
            ball_val["to_y"]=ball_val["init_speed_y"]
        else:
            ball_val["to_y"]+=0.5#포물선 효과
        ball_val["pos_x"]+=ball_val["to_x"]
        ball_val["pos_y"]+=ball_val["to_y"]


    #화면 그리기
    screen.blit(background,(0,0))


    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon,(weapon_x_pos,weapon_y_pos))
    
    for idx,val in enumerate(balls):
        ball_pos_x=val["pos_x"]
        ball_pos_y=val["pos_y"]
        ball_img_idx=val["img_idx"]
        screen.blit(ball_images[ball_img_idx],(ball_pos_x,ball_pos_y))
    screen.blit(stage,(0,screen_height-stage_height))
    screen.blit(character,(character_x_pos,character_y_pos))
    #충돌 처리

    retry=retry_font.render(('retry: Enter'),True,(0,0,0))
    quit= retry_font.render(('quit: ESC'),True,(0,0,0))

    #캐릭터 rect 정보 
    character_rect=character.get_rect()
    character_rect.left=character_x_pos 
    character_rect.top =character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x=ball_val["pos_x"]
        ball_pos_y=ball_val["pos_y"]
        ball_img_idx=ball_val["img_idx"]
        
        #공 rect 정보
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left=ball_pos_x
        ball_rect.top=ball_pos_y
        over=game_font.render(('GAME OVER'), True, (0,0,0))
        if character_rect.colliderect(ball_rect):
            screen.blit(over,(240,20))
            running=False
            break
        
        Win = game_font.render(('Win'),True,(0,0,0))
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            weapon_rect=weapon.get_rect()
            weapon_rect.left=weapon_pos_x
            weapon_rect.top=weapon_pos_y

            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove=weapon_idx
                ball_to_remove=ball_idx
                
                #가장 작은 공이 아니라면 다음 단계의 공으로 나뉘어짐
                if ball_img_idx <3:
                    ball_width=ball_rect.size[0]
                    ball_height=ball_rect.size[1]

                    small_ball_rect=ball_images[ball_img_idx+1].get_rect()
                    small_ball_width=small_ball_rect.size[0]
                    small_ball_height=small_ball_rect.size[1]

                    balls.append({
                        "pos_x":ball_pos_x+(ball_width/2)-(small_ball_width/2),#공의 x좌표
                        "pos_y":ball_pos_y+(ball_height/2)-(small_ball_height/2),#공의 y좌표
                        "img_idx":ball_img_idx+1,#공의 이미지 인덱스
                        "to_x":-3,#x축 이동방향
                        "to_y":-6,#y축 이동방향
                        "init_speed_y": ball_speed_y[ball_img_idx+1]})
                       
                
                    balls.append({
                        "pos_x":ball_pos_x+(ball_width/2)-(small_ball_width/2),#공의 x좌표
                        "pos_y":ball_pos_y+(ball_height/2)-(small_ball_height/2),#공의 y좌표
                        "img_idx":ball_img_idx+1,#공의 이미지 인덱스
                        "to_x": 3,#x축 이동방향
                        "to_y":-  6,#y축 이동방향
                        "init_speed_y": ball_speed_y[ball_img_idx+1]})
                break
        else: # 공 오류 해결
            continue
        break

    #충돌되 공, 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove=-1
    if weapon_to_remove>-1:
        del weapons[weapon_to_remove]
        weapon_to_remove=-1
    
    #승리
    if len(balls)==0:
        screen.blit(Win,(240,20))
        running=False

   
    
    #타이머 집어 넣기
    #경과 시간 계산
    elapsed_time=(pygame.time.get_ticks()-start_ticks)/1000 #경과시간을 초 단위로 표시
    timer =game_font.render(str(int(total_time-elapsed_time)),True,(255,255,255))
    
    #출력할 글자, True,글자 색상
    screen.blit(timer,(590,10))
    if total_time-elapsed_time<=0:
        screen.blit(over,(240,20))
        running=False
    
    
    
    pygame.display.update()#게임화면 다시 그리기
pygame.time.delay(2000)
#pygame 종료
pygame.quit()