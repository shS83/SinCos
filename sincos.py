import math
from pathlib import Path
import pygame as pg


CENTER_CHAR = ""
EDGE_CHAR = "|"
EDGE_COUNT = 250
ORBIT_RADIUS = 200  # Distance between the center and each edge character's center.
ORBIT_SPEED = 30  # Degrees per second.
CENTER_SPIN_SPEED = 0
CENTER_COLOR = (160, 255, 255)
CENTER_PULSE_PERIOD = 8  # Seconds for a full grow-and-shrink cycle.
EDGE_SPIN_SPEED = 180
RAINBOW_SPEED = 120  # Hue degrees per second.


def draw_rotating_char(surface, font, char, position, angle, color, scale=1):
    letter = font.render(char, True, color)
    rotated = pg.transform.rotozoom(letter, angle, scale)
    surface.blit(rotated, rotated.get_rect(center=position))


def draw_rainbow_circle(surface, font, elapsed, center_image):
    center = surface.get_rect().center
    # center_scale = 1.5 - 0.5 * math.cos(math.tau * elapsed / CENTER_PULSE_PERIOD)
    center_scale = 0.75 + 0.25 * math.cos(
        math.tau * elapsed / CENTER_PULSE_PERIOD
    )
    rotated = pg.transform.rotozoom(center_image, elapsed * CENTER_SPIN_SPEED % 360, center_scale)
    surface.blit(rotated, rotated.get_rect(center=center))
    # draw_rotating_char(
    #     surface, font, CENTER_CHAR, center,
    #     elapsed * CENTER_SPIN_SPEED % 360, CENTER_COLOR, center_scale,
    # )

    for i in range(EDGE_COUNT):
        phase = i / EDGE_COUNT
        orbit_angle = math.radians(phase * 360 + elapsed * ORBIT_SPEED)
        position = (
            center[0] + math.cos(orbit_angle) * ORBIT_RADIUS,
            center[1] + math.sin(orbit_angle) * ORBIT_RADIUS,
        )
        color = pg.Color(0, 0, 0)
        color.hsva = ((phase * 360 + elapsed * RAINBOW_SPEED) % 360, 100, 100, 100)
        draw_rotating_char(
            surface, font, EDGE_CHAR, position,
            (phase * 360 + elapsed * EDGE_SPIN_SPEED) % 360, color,
        )


def main():
    pg.init()
    try:
        screen = pg.display.set_mode((1280, 720))
        pg.display.set_caption("SinCos – Rainbow Circle")
        clock = pg.time.Clock()
        center_image = pg.image.load(
            str(Path(__file__).with_name("arch.png"))
        ).convert_alpha()
        center_image = pg.transform.smoothscale(center_image, (232, 232))
        font = pg.font.Font(str(Path(__file__).with_name("JBSemibold.ttf")), 64)
        elapsed = 0.0
        running = True

        while running:
            elapsed += clock.tick(120) / 1000
            for event in pg.event.get():
                if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
                ):
                    running = False
            if not running:
                break

            screen.fill((0, 0, 0))
            draw_rainbow_circle(screen, font, elapsed, center_image)
            pg.display.flip()
    finally:
        pg.quit()


if __name__ == "__main__":
    main()
