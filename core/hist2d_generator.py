from core.base_generator import BaseGenerator
from core.hist2d_class import Hist2dManager, Hist2dSettings


class Hist2dCodeGenerator(BaseGenerator):
    def generate(self, manager: Hist2dManager) -> str:
        lines = []

        lines.append('import matplotlib.pyplot as plt')
        lines.append('')
        lines.append('')

        lines.extend(self._write_labels(manager))
        lines.extend(self._draw_h2(manager))

        lines.append('plt.show()')

        return '\n'.join(lines)

    def _write_labels(self, manager: Hist2dManager):
        lines = []
        lines.append('fig, ax = plt.subplots()')
        if manager.title != '':
            title = f'ax.set_title("{manager.title}")'
            lines.append(title)
        if manager.label_xaxis != '':
            xlabel = f'ax.set_xlabel("{manager.label_xaxis}")'
            lines.append(xlabel)
        if manager.label_yaxis != '':
            ylabel = f'ax.set_ylabel("{manager.label_yaxis}")'
            lines.append(ylabel)
        return lines

    def _draw_h2(self, plot: Hist2dSettings) -> str:
        lines = []
        code = (
            'h2 = ax.hist2d(x, y, '
            f'bins=({plot.xbin_count}, {plot.ybin_count}), '
            f'range=(({plot.xmin}, {plot.ymax}), ({plot.ymin}, {plot.ymax})), '
            f'{"norm=LogNorm(), " if plot.is_zlog else ""}'
            f'cmap="{plot.colormap}")'
        )
        lines.append(code)
        if plot.has_colorbar:
            lines.append('fig.colorbar(h2[3], ax=ax)')
        return lines
