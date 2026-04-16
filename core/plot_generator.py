from core.plot_class import PlotManager, PlotSettings


class CodeGenerator:
    def generate(self, manager: PlotManager) -> str:
        lines = []

        lines.append('import matplotlib.pyplot as plt')
        lines.append('')

        lines.append('fig, ax1 = plt.subplots()')

        if manager.has_twin_axes:
            lines.append('ax2 = ax1.twinx()')

        for plot in manager.plots:
            ax = 'ax1' if plot.yaxis == 0 else 'ax2'
            lines.append(self._plot_line(plot, ax))

        if manager.has_grid:
            lines.append('ax1.grid(True)')

        lines.append('plt.show()')

        return '\n'.join(lines)

    def _plot_line(self, plot: PlotSettings, ax: str) -> str:
        return (f'{ax}.plot(x, y, color="{plot.line_color}", linestyle="{plot.line_style}")')
