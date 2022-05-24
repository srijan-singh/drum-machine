import pygame
from pygame import mixer

pygame.init()

WIDTH = 940
HEIGHT = 560

black = (0,0,0)
gray = (128,128,128)
white = (255,255,255)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Beat Maker")
label_font = pygame.font.Font("Roboto-Bold.ttf", 32)

fps = 60
timer = pygame.time.Clock()
beats = 16
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 1
beat_changed = True

# load in sounds
hi_hat = mixer.Sound('sounds\hi hat.wav')
snare = mixer.Sound('sounds\snare.wav')
kick = mixer.Sound('sounds\kick.wav')
crash = mixer.Sound('sounds\crash.wav')
clap = mixer.Sound('sounds\clap.wav')
tom = mixer.Sound("sounds\\tom.wav")
pygame.mixer.set_num_channels(instruments*3)

def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1:
            if i==0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()

def draw_grid(clicks, beat):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 100], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 105, WIDTH, 200], 5)
    boxes = []
    colors = [gray, white, gray]
    # Hi Hat
    hi_hat_text = label_font.render("Hi Hat", True, white)
    screen.blit(hi_hat_text, (30, 20))
    # Snare
    snare_text = label_font.render("Snare", True, white)
    screen.blit(snare_text, (30, 95))
    # Kick
    kick_text = label_font.render("Bass Drum", True, white)
    screen.blit(kick_text, (30, 170))
    # Crash
    crash_text = label_font.render("Crash", True, white)
    screen.blit(crash_text, (30, 245))
    # Clap
    clap_text = label_font.render("Clap", True, white)
    screen.blit(clap_text, (30, 320))
    # Floor Tom
    floor_tom_text = label_font.render("Floor Tom", True, white)
    screen.blit(floor_tom_text, (30, 395))

    for i in range(6):
        pygame.draw.line(screen, gray, (0, (i*75)), (195, (i*75)))

    for i in range(beats):
        for j in range(instruments):

            if clicks[j][i] == -1:
                color = gray

            else:
                color = green

            rect = pygame.draw.rect(screen, color,
                                    [i * ((WIDTH - 195) // beats) + 200, (j * 75), ((WIDTH - 195) // beats) - 10,
                                     65], 0, 1)
            pygame.draw.rect(screen, gold, [i * ((WIDTH - 195) // beats) + 200, j * 75, ((WIDTH - 195) // beats), 75],
                             5, 5)
            pygame.draw.rect(screen, black,
                             [i * ((WIDTH - 195) // beats) + 200, j * 75, ((WIDTH - 195) // beats), 75],
                             2, 2)
            
            boxes.append((rect, (i,j)))

        active = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 195)//beats) + 200, 0, ((WIDTH - 195)//beats), instruments*75], 5, 3)
    
    return boxes



run = True

while run:

    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat)

    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1


    beat_length = fps*60 // bpm

    if playing:
        if active_length < beat_length:
            active_length+=1

        else:
            active_length = 0
            
            if active_beat < beats - 1:
                active_beat+=1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True



    pygame.display.flip()

pygame.quit()