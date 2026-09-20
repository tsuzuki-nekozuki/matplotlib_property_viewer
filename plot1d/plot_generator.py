from common.base_generator import BaseGenerator
from plot1d.plot_defaults import (
    default_colors, default_line_style, default_line_width,
    default_marker_size, default_marker_style
)
from plot1d.plot_settings import PlotSettings


class PlotGenerator(BaseGenerator):
    def __init__(self, settings: PlotSettings):
        self.settings = settings
        self.has_twin_axes = False

    def generate(self) -> str:
        lines = []
        self.has_twin_axes = (
            self.settings.has_twin_axes and
            any(ip.yaxis == 1 for ip in self.settings.plots)
        )

        lines.append('import matplotlib.pyplot as plt')
        lines.append('')
        lines.append('')

        lines.extend(self._set_axes())
        lines.extend(self._write_labels())
        for i, iplot in enumerate(self.settings.plots):
            ax = 'ax1' if iplot.yaxis == 0 else 'ax2'
            lines.append(self._plot_line(i, ax))
        lines.append('plt.show()')

        return '\n'.join(lines)

    def _set_axes(self):
        lines = []
        lines.append('fig, ax1 = plt.subplots()')
        if self.has_twin_axes:
            lines.append('ax2 = ax1.twinx()')
        if self.settings.is_xlog:
            lines.append('ax1.set_xscale("log")')
        if self.settings.is_y1log:
            lines.append('ax1.set_yscale("log")')
        if self.has_twin_axes and self.settings.is_y2log:
            lines.append('ax2.set_yscale("log")')
        if self.settings.has_grid:
            lines.append('ax1.grid(True)')
        return lines

    def _write_labels(self):
        lines = []
        if self.settings.title != '':
            title = f'ax1.set_title("{self.settings.title}")'
            lines.append(title)
        if self.settings.label_xaxis != '':
            xlabel = f'ax1.set_xlabel("{self.settings.label_xaxis}")'
            lines.append(xlabel)
        if self.settings.label_yaxis != '':
            ylabel1 = f'ax1.set_ylabel("{self.settings.label_yaxis}")'
            lines.append(ylabel1)
        if self.has_twin_axes and self.settings.label_yaxis2 != '':
            ylabel2 = f'ax2.set_ylabel("{self.settings.label_yaxis2}")'
            lines.append(ylabel2)
        return lines

    def _plot_line(self, idx: int, ax: str) -> str:
        plot = self.settings.plots[idx]
        if self.is_marker_invisible(idx) and self.is_line_invisible(idx):
            msg_invisible = (
                f'# {plot.name} is invisible because marker and line settings'
                'are both not visibly set.'
            )
            return msg_invisible
        code_data = f'x{idx}, y{idx}'
        code_mc = ''
        code_lc = ''
        if not self.has_same_base_color(idx):
            if (plot.marker_style != 'None' and
                    not self.is_default_marker_color(idx)):
                code_mc = f'mec="{plot.marker_color}", '
                code_mc = code_mc + f'mfc="{plot.marker_color}"'
            if (plot.line_style != 'None' and
                    not self.is_default_line_color(idx)):
                code_lc = f'c="{plot.line_color}"'
        c = plot.marker_color if self.has_same_base_color(idx) else ''
        m = '' if plot.marker_style == 'None' else plot.marker_style
        l = '' if plot.line_style == 'None' else plot.line_style
        code_fmt = f'"{c}{m}{l}"'
        code_ms = ''
        if not self.is_default_marker_size(idx):
            code_ms = f'ms={round(plot.marker_size, 1)}'
        code_lw = ''
        if not self.is_default_line_width(idx):
            code_lw = f'lw={round(plot.line_width, 1)}'
        codes = [code_data, code_fmt, code_mc, code_lc, code_ms, code_lw]
        codes = [i for i in codes if i != '']
        return f'{ax}.plot(' + ', '.join(codes) + ')'

    def is_marker_invisible(self, idx: int):
        plot = self.settings.plots[idx]
        if plot.marker_size == 0 or plot.marker_style == 'None':
            return True
        return False

    def is_line_invisible(self, idx: int):
        plot = self.settings.plots[idx]
        if plot.line_width == 0 or plot.line_style == 'None':
            return True
        return False

    def has_same_base_color(self, idx: int):
        plot = self.settings.plots[idx]
        if plot.marker_color != plot.line_color:
            return False
        if self.is_marker_invisible(idx):
            return False
        if self.is_line_invisible(idx):
            return False
        return True

    def is_default_marker_style(self, idx: int):
        plot = self.settings.plots[idx]
        return plot.marker_style == default_marker_style

    def is_default_marker_color(self, idx: int):
        plot = self.settings.plots[idx]
        return plot.marker_color == default_colors[idx]

    def is_default_marker_size(self, idx: int):
        plot = self.settings.plots[idx]
        return plot.marker_size == default_marker_size

    def is_default_line_style(self, idx: int):
        plot = self.settings.plots[idx]
        return plot.line_style == default_line_style

    def is_default_line_color(self, idx: int):
        plot = self.settings.plots[idx]
        return plot.line_color == default_colors[idx]

    def is_default_line_width(self, idx: int):
        plot = self.settings.plots[idx]
        return plot.line_width == default_line_width
