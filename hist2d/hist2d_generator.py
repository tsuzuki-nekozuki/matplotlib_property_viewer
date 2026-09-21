from common.base_generator import BaseGenerator
from hist2d.hist2d_settings import Hist2dSettings


class Hist2dCodeGenerator(BaseGenerator):
    def __init__(self, settings: Hist2dSettings):
        self.settings = settings

    def generate(self) -> str:
        lines = []

        lines.append('import matplotlib.pyplot as plt')
        if self.settings.is_zlog:
            lines.append('from matplotlib.colors import LogNorm')

        lines.append('')
        lines.append('')

        lines.extend(self._write_labels())
        lines.extend(self._draw_h2())

        lines.append('plt.show()')

        return '\n'.join(lines)

    def _write_labels(self):
        lines = []
        lines.append('fig, ax = plt.subplots()')
        if self.settings.title != '':
            title = f'ax.set_title("{self.settings.title}")'
            lines.append(title)
        if self.settings.label_xaxis != '':
            xlabel = f'ax.set_xlabel("{self.settings.label_xaxis}")'
            lines.append(xlabel)
        if self.settings.label_yaxis != '':
            ylabel = f'ax.set_ylabel("{self.settings.label_yaxis}")'
            lines.append(ylabel)
        return lines

    def _draw_h2(self) -> str:
        lines = []
        code = (
            'h2 = ax.hist2d(x, y, '
            f'bins=({self.settings.xbin_count}, {self.settings.ybin_count}), '
            f'range=(({self.settings.xmin}, {self.settings.xmax}), '
            f'({self.settings.ymin}, {self.settings.ymax})), '
            f'{"norm=LogNorm(), " if self.settings.is_zlog else ""}'
            f'cmap="{self.settings.colormap}")'
        )
        lines.append(code)
        if self.settings.has_colorbar:
            lines.append('fig.colorbar(h2[3], ax=ax)')
        return lines
