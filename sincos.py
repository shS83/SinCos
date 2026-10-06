import math
from datetime import datetime
from pathlib import Path
import pygame as pg

CENTER_CHAR = ""
EDGE_CHAR = "S"
EDGE_COUNT = 225
ORBIT_RADIUS = 200  # Distance between the center and each edge character's center.
ORBIT_SPEED = 30  # Degrees per second.
CENTER_SWING_ANGLE = 20  # Maximum tilt in degrees to either side.
CENTER_SWING_PERIOD = 4  # Seconds for a full left-and-right cycle.
CENTER_COLOR = (160, 255, 255)
CENTER_PULSE_PERIOD = 8  # Seconds for a full grow-and-shrink cycle.
EDGE_SPIN_SPEED = 180
RAINBOW_SPEED = 120  # Hue degrees per second.
CLOCK_COLOR = (255, 255, 255)


def draw_rotating_char(surface, font, char, position, angle, color, scale=1):
    letter = font.render(char, True, color)
    rotated = pg.transform.rotozoom(letter, angle, scale)
    surface.blit(rotated, rotated.get_rect(center=position))


def draw_rainbow_circle(surface, font, elapsed, center_image):
    center = surface.get_rect().center
    # center_scale = 1.5 - 0.5 * math.cos(math.tau * elapsed / CENTER_PULSE_PERIOD)
    center_scale = 0.75 + 0.25 * math.cos(math.tau * elapsed / CENTER_PULSE_PERIOD)
    center_angle = CENTER_SWING_ANGLE * math.sin(math.tau * elapsed / CENTER_SWING_PERIOD)
    rotated = pg.transform.rotozoom(center_image, center_angle, center_scale)
    surface.blit(rotated, rotated.get_rect(center=center))
    # draw_rotating_char(
    #     surface, font, CENTER_CHAR, center,
    #     center_angle, CENTER_COLOR, center_scale,
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
            surface,
            font,
            EDGE_CHAR,
            position,
            (phase * 360 + elapsed * EDGE_SPIN_SPEED) % 360,
            color,
        )


def draw_clock(surface, time_font, date_font):
    now = datetime.now()
    time_text = time_font.render(now.strftime("%H:%M:%S"), True, CLOCK_COLOR)
    date_text = date_font.render(now.strftime("%d.%m.%Y"), True, CLOCK_COLOR)
    date_rect = date_text.get_rect(
        midbottom=(surface.get_width() // 2, surface.get_height() - 40)
    )
    time_rect = time_text.get_rect(midbottom=(date_rect.centerx, date_rect.top - 6))
    surface.blit(time_text, time_rect)
    surface.blit(date_text, date_rect)


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
        clock_font_path = str(Path(__file__).with_name("FiraCode-Light.ttf"))
        time_font = pg.font.Font(clock_font_path, 36)
        date_font = pg.font.Font(clock_font_path, 22)
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
            draw_clock(screen, time_font, date_font)
            pg.display.flip()
    finally:
        pg.quit()


if __name__ == "__main__":
    main()
