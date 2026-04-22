from core.base_generator import BaseGenerator
from core.plot_class import PlotManager, PlotSettings


class CodeGenerator(BaseGenerator):
    def generate(self, manager: PlotManager) -> str:
        lines = []

        lines.append('import matplotlib.pyplot as plt')
        lines.append('')
        lines.append('')

        lines.extend(self._set_axes(manager))
        lines.extend(self._write_labels(manager))
        for iplot in manager.plots:
            ax = 'ax1' if iplot.yaxis == 0 else 'ax2'
            lines.append(self._plot_line(iplot, ax))
        lines.append('plt.show()')

        return '\n'.join(lines)

    def _set_axes(self, manager: PlotManager):
        lines = []
        lines.append('fig, ax1 = plt.subplots()')
        if manager.need_two_axes():
            lines.append('ax2 = ax1.twinx()')
        if manager.is_xlog:
            lines.append('ax1.set_xscale("log")')
        if manager.is_y1log:
            lines.append('ax1.set_yscale("log")')
        if manager.need_two_axes() and manager.is_y2log:
            lines.append('ax2.set_yscale("log")')
        if manager.has_grid:
            lines.append('ax1.grid(True)')
        return lines

    def _write_labels(self, manager: PlotManager):
        lines = []
        if manager.title != '':
            title = f'ax1.set_title("{manager.title}")'
            lines.append(title)
        if manager.label_xaxis != '':
            xlabel = f'ax1.set_xlabel("{manager.label_xaxis}")'
            lines.append(xlabel)
        if manager.label_yaxis != '':
            ylabel1 = f'ax1.set_ylabel("{manager.label_yaxis}")'
            lines.append(ylabel1)
        if manager.need_two_axes() and manager.label_yaxis2 != '':
            ylabel2 = f'ax2.set_ylabel("{manager.label_yaxis2}")'
            lines.append(ylabel2)
        return lines

    def _plot_line(self, plot: PlotSettings, ax: str) -> str:
        if ((plot.marker_size == 0 or plot.marker_style == 'None') and
                (plot.line_width == 0 or plot.line_style == 'None')):
            msg_invisible = (
                f'# {plot.name} is invisible because marker and line settings'
                'are both not visibly set.'
            )
            return msg_invisible
        code_data = f'x{plot.id + 1}, y{plot.id + 1}'
        code_mc = ''
        code_lc = ''
        if not plot.has_same_base_color():
            if (plot.marker_style != 'None' and
                    not plot.is_default_marker_color()):
                code_mc = f'mec="{plot.marker_color}", '
                code_mc = code_mc + f'mfc="{plot.marker_color}"'
            if (plot.line_style != 'None' and
                    not plot.is_default_line_color()):
                code_lc = f'c="{plot.line_color}"'
        c = plot.marker_color if plot.has_same_base_color() else ''
        m = '' if plot.marker_style == 'None' else plot.marker_style
        l = '' if plot.line_style == 'None' else plot.line_style
        code_fmt = f'"{c}{m}{l}"'
        code_ms = ''
        if not plot.is_default_marker_size():
            code_ms = f'ms={round(plot.marker_size, 1)}'
        code_lw = ''
        if not plot.is_default_line_width():
            code_lw = f'ms={round(plot.line_width, 1)}'
        codes = [code_data, code_fmt, code_mc, code_lc, code_ms, code_lw]
        codes = [i for i in codes if i != '']
        return f'{ax}.plot(' + ', '.join(codes) + ')'
