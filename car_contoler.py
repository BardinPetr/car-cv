import pygame
import socket
import os


def check(speed, route, stop="00"):
    sock = socket.socket()
    sock.connect(('172.24.1.1', 1080))
    line = "{}/{}/{}".format(stop, speed, route).encode("utf-8")
    sock.send(line)
    sock.close()


signs = {}
for d, dirs, files in os.walk("res"):
    for file_name in files:
        file = pygame.image.load("res/" + file_name)
        file = pygame.transform.scale(file, (100, 100))
        signs[file_name.replace('.png', '')] = file

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('', 1092)
s.bind(server_address)
s.listen(1)
conn, addr = s.accept()


speed = 1500
route = 90

pygame.init()
screen_size = (400, 100)
screen = pygame.display.set_mode(screen_size)
screen.fill(pygame.Color("black"))


running = True

while running:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    speed = 1580
                    check(speed, route)
                if event.key == pygame.K_UP:
                    speed = 1390
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
        screen.fill((0, 0, 0))
        packet = conn.recv(1024)
        if packet:
            files = packet.decode("utf-8").split(",")
            length = len(files)
            k = 0
            for file_name in files:
                screen.blit(signs[file_name], (k * 100, 0))
                k += 1

        pygame.display.flip()
    except KeyboardInterrupt:
        break
    except Exception:
        pass
check(1500, 90, "00")
conn.close()
pygame.quit()
