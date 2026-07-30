class Theme:
    # Colori generali
    BACKGROUND = (0.10, 0.10, 0.10, 1)
    SURFACE = (0.18, 0.18, 0.18, 1)

    TEXT = (1, 1, 1, 1)
    TEXT_SECONDARY = (0.78, 0.78, 0.78, 1)

    # Colori fazioni
    GOOD = (0.09, 0.39, 0.75, 1)
    EVIL = (0.72, 0.11, 0.10, 1)
    NEUTRAL = (0.50, 0.50, 0.50, 1)

    # Pulsanti
    BUTTON = (0.23, 0.23, 0.23, 1)
    BUTTON_HOVER = (0.30, 0.30, 0.30, 1)

    CARD_RADIUS = 18

    CARD_ELEVATION = 6

    PADDING = 20

    SPACING = 15


from kivy.utils import get_color_from_hex


class LupusTheme:

    BACKGROUND = get_color_from_hex("#121212")

    CARD = get_color_from_hex("#1E1E1E")

    WHITE = get_color_from_hex("#FFFFFF")

    RED = get_color_from_hex("#B71C1C")

    BLUE = get_color_from_hex("#1565C0")

    GREY = get_color_from_hex("#616161")