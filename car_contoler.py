import pygame
import socket


def check(speed, route, stop="00"):
    sock = socket.socket()
    sock.connect(('172.24.1.1', 1080))
    line = "{}/{}/{}".format(stop, speed, route).encode("utf-8")
    sock.send(line)
    sock.close()


speed = 1500
route = 90

pygame.init()
screen_size = (300, 300)
screen = pygame.display.set_mode(screen_size)
screen.fill(pygame.Color("black"))



check(speed, route)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                speed = 1580
                check(speed, route)
            if event.key == pygame.K_UP:
                speed = 1380
                check(speed, route)
            if event.key == pygame.K_LEFT:
                route = 100
                check(speed, route)
            if event.key == pygame.K_RIGHT:
                route = 80
                check(speed, route)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                speed = 1500
                check(speed, route)
            if event.key == pygame.K_UP:
                speed = 1500
                check(speed, route)
            if event.key == pygame.K_LEFT:
                route = 90
                check(speed, route)
            if event.key == pygame.K_RIGHT:
                route = 90
                check(speed, route)
    pygame.display.flip()
check(1500, 90, "00")
#sock.close()
pygame.quit()
