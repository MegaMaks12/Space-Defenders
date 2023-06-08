import pygame, controls
from gun import Gun
from pygame.sprite import Group
from stats import Stats
from scores import Scores
from sqlite import edit_scores, read_scores, get_best


pygame.init()
screen = pygame.display.set_mode((700, 800))
arial_36 = pygame.font.SysFont('arial', 36)
bg_image = pygame.image.load("space.jpg")
timer = pygame.time.Clock()

def run(name):
    last_scores = read_scores(name)
    print(last_scores)

    pygame.display.set_caption("Космические защитники")
    bg_color = (0, 0, 0)
    gun = Gun(screen)
    bullets = Group()
    inos = Group()
    controls.create_army(screen, inos)
    stats = Stats()
    sc = Scores(screen, stats)

    while True:
        controls.events(screen, gun, bullets)
        if stats.run_game:
            gun.update_gun()
            controls.update(bg_color, screen, stats, sc, gun, inos, bullets)
            controls.update_bullets(screen, stats, sc, inos, bullets)
            controls.update_inos(stats, screen, sc, gun, inos, bullets)
        else:
            if stats.score > last_scores:
                edit_scores(name, stats.score)
            break

def show_best():
    items = get_best()
    arial_36 = pygame.font.SysFont('arial', 36)
    screen.fill((0, 0, 0))
    for i, (name, _, scores) in enumerate(items, start=1):
        text = arial_36.render(str(i) + ". " + str(name) + " " + str(scores) + " очков ", True, (255, 255, 255))
        screen.blit(text, (100, 100 + i * 50))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        pygame.display.update()
        timer.tick(60)
