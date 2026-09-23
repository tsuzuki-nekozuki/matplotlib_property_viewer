from typing import Callable

from common.base_generator import BaseGenerator
from fonts.fonts_settings import FontsSettings


class FontCodeGenerator(BaseGenerator):
    def __init__(self, settings: FontsSettings):
        self.settings = settings

    def generate(self) -> str:
        generators: dict[str, Callable[[FontsSettings], str]] = {
            'suptitle': self._generate_suptitle,
            'title': self._generate_title,
            'xlabel': self._generate_xlabel,
            'ylabel': self._generate_ylabel,
            'xtick': self._generate_xtick,
            'ytick': self._generate_ytick,
            'legend': self._generate_legend,
            'colorbar': self._generate_colorbar,
            'annotation': self._generate_annotation,
            'text': self._generate_text,
        }

        try:
            generator = generators[self.settings.target]
        except KeyError as exc:
            raise ValueError(
                f'Unsupported font target: {self.settings.target!r}'
            ) from exc
        return generator()

    def _generate_suptitle(self) -> str:
        return (
            'fig.suptitle(\n'
            "    'Figure Title',\n"
            f'{self._format_kwargs()}\n'
            ')'
        )

    def _generate_title(self) -> str:
        return (
            'ax.set_title(\n'
            "    'Axes Title',\n"
            f'{self._format_kwargs()}\n'
            ')'
        )

    def _generate_xlabel(self) -> str:
        return (
            'ax.set_xlabel(\n'
            "    'X Label',\n"
            f'{self._format_kwargs()}\n'
            ')'
        )

    def _generate_ylabel(self) -> str:
        return (
            'ax.set_ylabel(\n'
            "    'Y Label',\n"
            f'{self._format_kwargs()}\n'
            ')'
        )

    def _generate_xtick(self) -> str:
        return self._generate_tick_labels('ax.get_xticklabels()')

    def _generate_ytick(self) -> str:
        return self._generate_tick_labels('ax.get_yticklabels()')

    def _generate_tick_labels(
        self,
        labels: str,
    ) -> str:
        setters = self._format_setters('label')

        return (
            f'for label in {labels}:\n'
            f'{self._indent(setters, 4)}'
        )

    def _generate_legend(self) -> str:
        setters = self._format_setters('text')

        return (
            'legend = ax.get_legend()\n'
            'if legend is not None:\n'
            '    for text in legend.get_texts():\n'
            f'{self._indent(setters, 8)}'
        )

    def _generate_colorbar(self) -> str:
        setters = self._format_setters('label')

        return (
            'for label in colorbar.ax.get_yticklabels():\n'
            f'{self._indent(setters, 4)}'
        )

    def _generate_annotation(self) -> str:
        return (
            'ax.annotate(\n'
            "    'Annotation',\n"
            '    xy=(0.5, 0.5),\n'
            '    xytext=(0.6, 0.6),\n'
            f'{self._format_kwargs()}\n'
            ')'
        )

    def _generate_text(self) -> str:
        return (
            'ax.text(\n'
            '    0.5,\n'
            '    0.5,\n'
            "    'Text', \n"
            f'{self._format_kwargs()}\n'
            ')'
        )

    def _format_kwargs(self) -> str:
        kwargs = [
            f'    fontfamily={self.settings.font!r},',
            f'    fontstyle={self.settings.style!r},',
            f'    fontsize={self.settings.size!r},',
            f'    fontweight={self.settings.weight!r},',
            f'    color={self.settings.foreground!r},',
            f'    backgroundcolor={self.settings.background!r},',
        ]
        return '\n'.join(kwargs)

    def _format_setters(self, val: str) -> str:
        setters = [
            f'{val}.set_fontfamily({self.settings.font!r})',
            f'{val}.set_fontstyle({self.settings.style!r})',
            f'{val}.set_fontsize({self.settings.size!r})',
            f'{val}.set_fontweight({self.settings.weight!r})',
            f'{val}.set_color({self.settings.foreground!r})',
            f'{val}.set_backgroundcolor({self.settings.background!r})',
        ]
        return '\n'.join(setters)

    @staticmethod
    def _indent(text: str, spaces: int) -> str:
        prefix = ' ' * spaces

        return '\n'.join(
            f'{prefix}{line}'
            for line in text.splitlines()
        )
