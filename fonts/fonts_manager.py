from matplotlib.font_manager import FontProperties

from fonts.fonts_defaults import rcparams
from fonts.fonts_settings import FontsSettings
from fonts.fonts_generator import FontCodeGenerator


class FontsManager:
    def __init__(self):
        self.default_settings = rcparams
        self.user_settings: FontsSettings = FontsSettings()
        self.code: FontCodeGenerator = FontCodeGenerator(self.user_settings)

        for _, v in self.default_settings.items():
            if isinstance(v['Size'], str):
                v['Size'] = self.get_font_size_value(v['Size'])

    def get_font_size_value(self, font_size):
        return FontProperties(font_size).get_size_in_points()

    @property
    def target(self) -> str:
        return self.user_settings.target

    @target.setter
    def target(self, value: str):
        self.user_settings.target = value

    @property
    def font(self) -> str:
        return self.user_settings.font

    @font.setter
    def font(self, value: str):
        self.user_settings.font = value

    @property
    def style(self) -> str:
        return self.user_settings.style

    @style.setter
    def style(self, value: str):
        self.user_settings.style = value

    @property
    def size(self) -> float:
        return self.user_settings.size

    @size.setter
    def size(self, value: float):
        self.user_settings.size = value

    @property
    def weight(self) -> str:
        return self.user_settings.weight

    @weight.setter
    def weight(self, value: str):
        self.user_settings.weight = value

    @property
    def foreground(self) -> str:
        return self.user_settings.foreground

    @foreground.setter
    def foreground(self, value: str):
        self.user_settings.foreground = value

    @property
    def background(self) -> str:
        return self.user_settings.background

    @background.setter
    def background(self, value: str):
        self.user_settings.background = value

    def generate_code(self):
        return self.code.generate()
