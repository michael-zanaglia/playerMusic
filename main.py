import pygame
import os
import re

pygame.init()

screen = pygame.display.set_mode((300, 500))
pygame.display.set_caption("Player Musique")
ico = pygame.image.load("icone.png")
pygame.display.set_icon(ico)
bg = pygame.Color("#00FFFF")
play = pygame.image.load("play.png").convert_alpha()
pause = pygame.image.load("pause.png").convert_alpha()
current = pause
skip = pygame.image.load("skip.png").convert_alpha()
ret = pygame.image.load("return.png").convert_alpha()
infini = pygame.image.load("infini.png").convert_alpha()
fleche = pygame.image.load("fleche.png").convert_alpha()
state = fleche
plus = pygame.image.load("plus.png").convert_alpha()
moins = pygame.image.load("moins.png").convert_alpha()
max = pygame.image.load("plus_max.png").convert_alpha()
mute = pygame.image.load("mute.png").convert_alpha()
updown = None
running = True
playing = True
x, y = 120, 300
sound = 0.5

SONG_END = pygame.USEREVENT + 1

###################################################### FONCTION ################################################
def lister_track(chemin):
    list_track = []
    for namefile in os.listdir(chemin):
        if re.search(".mp3$", namefile):
            list_track.append(namefile)
    return list_track

def image_song(chemin):
    list_image = []
    for namefile in os.listdir(chemin):
        if re.search(".png$", namefile) or re.search(".jpg$", namefile) or re.search(".jpeg$", namefile) :
            list_image.append(namefile)
    return list_image

def next_song(n_index, n_txt) :
    next = (n_index + 1) % len(playlist)
    n_index = next
    n_txt = police.render(playlist[n_index], 3, (1, 1, 1))
    pygame.mixer.music.load(f"playlist\\{playlist[n_index]}")
    pygame.mixer.music.play()
    for k, v in dico.items() :
        if k == playlist[n_index] :
            cover = pygame.image.load(f"cover\\{v}")
    return n_index, n_txt, cover

###################################################### FONCTION ################################################   

cd = r"C:\Users\mikad\Desktop\LaPlateforme\code\python\playerMusic\playlist"
cdi = r"C:\Users\mikad\Desktop\LaPlateforme\code\python\playerMusic\cover"
default_img = "default.png"
playlist = lister_track(cd)
img = image_song(cdi)
dico = {}
# J'associe une image avec un son et si j'ai moins d'image que prevu je veux qu'il me mette uniquement l'image par default
for i in range(len(playlist)):
    if i < len(img) :
        dico[playlist[i]] = img[i]
    else :
        dico[playlist[i]] = default_img   
index = 0
pygame.mixer.music.load(f"playlist\\{playlist[index]}")
pygame.mixer.music.play()
for k, v in dico.items() :
    if k == playlist[index] :
        cover = pygame.image.load(f"cover\\{v}")
police = pygame.font.Font(None, 20)
txt = police.render(playlist[index], 3, (1, 1, 1))

# Définir l'événement de fin de musique en dehors de la boucle d'événements
pygame.mixer.music.set_endevent(SONG_END)

# Boucle importante afin d'afficher en permanence les éléments de notre écran ainsi que lui-même
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Gere tout les cliques de souris possible sur l'application
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current.get_rect(topleft=(x, y)).collidepoint(event.pos):
                if playing:
                    pygame.mixer.music.pause()
                    current = play
                    print(pygame.mixer.music.get_pos() / 1000)
                else:
                    pygame.mixer.music.unpause()
                    current = pause
            # Si je clique, je passe a la prochaine piste.
            elif skip.get_rect(topleft=(x + 70, y + 5)).collidepoint(event.pos):
                index, txt, cover = next_song(index, txt)
                if current == play:
                    current = pause
                    pygame.mixer.music.unpause()
            # Si je clique, je rertourne a la précédente piste.
            elif ret.get_rect(topleft=(x - 60, y + 5)).collidepoint(event.pos):
                next = index - 1
                if next < 0:
                    next = 0
                index = next
                txt = police.render(playlist[index], 3, (1, 1, 1))
                pygame.mixer.music.load(f"playlist\\{playlist[index]}")
                pygame.mixer.music.play()
                for k, v in dico.items() :
                    if k == playlist[index] :
                        cover = pygame.image.load(f"cover\\{v}")
                if current == play:
                    current = pause
                    pygame.mixer.music.unpause()
            elif state.get_rect(topleft=(x + 140, y + 165)).collidepoint(event.pos):
                if state == infini:
                    pygame.mixer.music.play(loops=0)
                    state = fleche
                else:
                    # A l'instant ou je clique state represente une fleche donc j'affiche le mode active ici la repetition d'une musique
                    pygame.mixer.music.play(loops=-1)
                    state = infini

            playing = not playing
        # Tout ce qui gere le volume sonore avec la fleche du bas et celle du haut    
        elif event.type == pygame.KEYDOWN :
            if event.key == pygame.K_UP :
                if sound <= 1.0 :
                    updown = plus
                    sound += 0.1
                    pygame.mixer.music.set_volume(sound)
                else :
                    updown = max
            elif event.key == pygame.K_DOWN:
                if sound >= 0.0 :
                    updown = moins
                    sound -= 0.1
                    pygame.mixer.music.set_volume(sound)
                else :
                    updown = mute
        elif event.type == pygame.KEYUP :
            pygame.time.delay(500)
            updown = None
            

    if event.type == SONG_END and state == fleche :
        if not pygame.mixer.music.get_busy():
            index, txt, cover = next_song(index, txt)
        
        

    screen.fill(bg)
    screen.blit(cover, (x - 70, y - 250))
    screen.blit(current, (x, y))
    screen.blit(skip, (x + 70, y + 5))
    screen.blit(ret, (x - 60, y + 5))
    screen.blit(state, (x + 140, y + 165))
    screen.blit(txt, (x - 113, y - 25))
    if updown is not None :
        screen.blit(updown, (x - 20, y - 100))

    pygame.display.flip()

pygame.quit()
