from typing import Callable

from common.base_generator import BaseGenerator
from fonts.fonts_class import FontsSettings


class FontCodeGenerator(BaseGenerator):

    def generate(self, settings: FontsSettings) -> str:
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
            generator = generators[settings.target]
        except KeyError as exc:
            raise ValueError(
                f'Unsupported font target: {settings.target!r}'
            ) from exc

        return generator(settings)

    def _generate_suptitle(self, settings: FontsSettings) -> str:
        return (
            'fig.suptitle(\n'
            "    'Figure Title',\n"
            f'{self._format_kwargs(settings)}\n'
            ')'
        )

    def _generate_title(self, settings: FontsSettings) -> str:
        return (
            'ax.set_title(\n'
            "    'Axes Title',\n"
            f'{self._format_kwargs(settings)}\n'
            ')'
        )

    def _generate_xlabel(self, settings: FontsSettings) -> str:
        return (
            'ax.set_xlabel(\n'
            "    'X Label',\n"
            f'{self._format_kwargs(settings)}\n'
            ')'
        )

    def _generate_ylabel(self, settings: FontsSettings) -> str:
        return (
            'ax.set_ylabel(\n'
            "    'Y Label',\n"
            f'{self._format_kwargs(settings)}\n'
            ')'
        )

    def _generate_xtick(self, settings: FontsSettings) -> str:
        return self._generate_tick_labels(
            'ax.get_xticklabels()',
            settings,
        )

    def _generate_ytick(self, settings: FontsSettings) -> str:
        return self._generate_tick_labels(
            'ax.get_yticklabels()',
            settings,
        )

    def _generate_tick_labels(
        self,
        labels: str,
        settings: FontsSettings,
    ) -> str:
        setters = self._format_setters('label', settings)

        return (
            f'for label in {labels}:\n'
            f'{self._indent(setters, 4)}'
        )

    def _generate_legend(self, settings: FontsSettings) -> str:
        setters = self._format_setters('text', settings)

        return (
            'legend = ax.get_legend()\n'
            'if legend is not None:\n'
            '    for text in legend.get_texts():\n'
            f'{self._indent(setters, 8)}'
        )

    def _generate_colorbar(self, settings: FontsSettings) -> str:
        setters = self._format_setters('label', settings)

        return (
            'for label in colorbar.ax.get_yticklabels():\n'
            f'{self._indent(setters, 4)}'
        )

    def _generate_annotation(self, settings: FontsSettings) -> str:
        return (
            'ax.annotate(\n'
            "    'Annotation',\n"
            '    xy=(0.5, 0.5),\n'
            '    xytext=(0.6, 0.6),\n'
            f'{self._format_kwargs(settings)}\n'
            ')'
        )

    def _generate_text(self, settings: FontsSettings) -> str:
        return (
            'ax.text(\n'
            '    0.5,\n'
            '    0.5,\n'
            "    'Text', \n"
            f'{self._format_kwargs(settings)}\n'
            ')'
        )

    @staticmethod
    def _format_kwargs(settings: FontsSettings) -> str:
        kwargs = [
            f'    fontfamily={settings.font!r},',
            f'    fontstyle={settings.style!r},',
            f'    fontsize={settings.size!r},',
            f'    fontweight={settings.weight!r},',
            f'    color={settings.foreground!r},',
            f'    backgroundcolor={settings.background!r},',
        ]

        return '\n'.join(kwargs)

    @staticmethod
    def _format_setters(
        variable: str,
        settings: FontsSettings,
    ) -> str:
        setters = [
            f'{variable}.set_fontfamily({settings.font!r})',
            f'{variable}.set_fontstyle({settings.style!r})',
            f'{variable}.set_fontsize({settings.size!r})',
            f'{variable}.set_fontweight({settings.weight!r})',
            f'{variable}.set_color({settings.foreground!r})',
            f'{variable}.set_backgroundcolor({settings.background!r})',
        ]

        return '\n'.join(setters)

    @staticmethod
    def _indent(text: str, spaces: int) -> str:
        prefix = ' ' * spaces

        return '\n'.join(
            f'{prefix}{line}'
            for line in text.splitlines()
        )
