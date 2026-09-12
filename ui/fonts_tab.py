import matplotlib.pyplot as plt

from matplotlib.gridspec import GridSpec
from PySide6.QtCore import Qt, QStringListModel, QItemSelectionModel
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QComboBox, QSlider,
    QDoubleSpinBox, QLineEdit, QPushButton, QCheckBox, QListView, QButtonGroup,
    QPlainTextEdit, QRadioButton, QStackedWidget, QSplitter, QSizePolicy,
    QApplication, QGroupBox, QGridLayout
)

from core.mpl_properties import (
    get_fonts_list, get_color_list, get_font_style_list, get_font_weight_list
)
from core.fonts_class import FontsManager
# from core.plot_generator import CodeGenerator
from ui.aspect_ratio import AspectRatioWidget


class FontsTab(QWidget):
    def __init__(self, canvas):
        super().__init__()

        # FontsManager
        self.fontm = FontsManager()

        # text
        self.text_data = 'write your text here.'
        self.fontm.target = list(self.fontm.default_rcparams.keys())[0]

        # Layout
        self.layout = QHBoxLayout()

        # Splitter
        splitter = QSplitter()

        # canvas
        self.canvas = canvas
        self.ax2 = None
        canvas.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        split_canvas = AspectRatioWidget(canvas, ratio=4/3)
        self.layout.addWidget(split_canvas, alignment=Qt.AlignCenter)

        # options
        split_options = QWidget()
        split_options.setFixedWidth(350)
        self.layout_options = QVBoxLayout(split_options)

        splitter.addWidget(split_canvas)
        splitter.addWidget(split_options)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)

        # text
        self.label_text = QLabel('Text')
        self.label_text.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_text)

        self.text_edit = QLineEdit()
        self.text_edit.setText(self.text_data)
        self.text_edit.textChanged.connect(self.changed_text)
        self.layout_options.addWidget(self.text_edit)

        hline1 = QFrame()
        hline1.setFrameShape(QFrame.HLine)
        hline1.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline1)

        self.label_settings = QLabel('Settings')
        self.label_settings.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_settings)
        self.layout_font = QHBoxLayout()
        self.label_font = QLabel('font')
        self.layout_font.addWidget(self.label_font)
        self.combobox_font = QComboBox()
        font_list = get_fonts_list()
        self.combobox_font.addItems(font_list)
        self.combobox_font.setFixedWidth(260)
        index = self.combobox_font.findText(self.fontm.default_font)
        if index >= 0:
            self.combobox_font.setCurrentIndex(index)
        self.combobox_font.currentTextChanged.connect(self.on_changed_font)
        self.layout_font.addWidget(self.combobox_font)
        self.layout_options.addLayout(self.layout_font)

        self.layout_style = QHBoxLayout()
        self.label_style = QLabel('style')
        self.layout_style.addWidget(self.label_style)
        self.combobox_style = QComboBox()
        style_list = get_font_style_list()
        self.combobox_style.addItems(style_list)
        self.combobox_style.setFixedWidth(260)
        self.layout_style.addWidget(self.combobox_style)
        self.layout_options.addLayout(self.layout_style)

        # size and weight
        self.layout_size_weight = QHBoxLayout()
        self.label_size = QLabel('Size')
        self.layout_size_weight.addWidget(self.label_size)

        self.spinbox_size = QDoubleSpinBox()
        self.spinbox_size.setFixedWidth(90)
        self.spinbox_size.setMinimum(0.1)
        self.spinbox_size.setMaximum(50)
        self.spinbox_size.setDecimals(1)
        self.spinbox_size.setSingleStep(0.1)
        self.spinbox_size.setValue(self.fontm.default_size)
        self.spinbox_size.valueChanged.connect(self.on_size_changed)
        self.layout_size_weight.addWidget(self.spinbox_size)

        self.label_weight = QLabel('Weight')
        self.layout_size_weight.addWidget(self.label_weight)

        self.combobox_weight = QComboBox()
        weight_list = get_font_weight_list()
        self.combobox_weight.addItems(weight_list)
        self.combobox_weight.setFixedWidth(90)
        index = self.combobox_weight.findText(self.fontm.default_weight)
        if index >= 0:
            self.combobox_weight.setCurrentIndex(index)
        self.combobox_weight.setFixedWidth(90)
        self.combobox_weight.currentTextChanged.connect(self.on_weight_changed)
        self.layout_size_weight.addWidget(self.combobox_weight)
        self.layout_options.addLayout(self.layout_size_weight)

        # color
        font_color = get_color_list()
        self.layout_color1 = QHBoxLayout()
        self.label_color1 = QLabel('foreground color')
        self.layout_color1.addWidget(self.label_color1)
        self.combobox_color1 = QComboBox()
        self.combobox_color1.setFixedWidth(200)
        self.combobox_color1.addItems(font_color)
        for i, icolor in enumerate(font_color):
            if icolor.startswith('- '):
                self.combobox_color1.model().item(i).setEnabled(False)
        self.combobox_color1.currentTextChanged.connect(
            self.on_foreground_changed)
        self.layout_color1.addWidget(self.combobox_color1)
        self.layout_options.addLayout(self.layout_color1)

        self.layout_color2 = QHBoxLayout()
        self.label_color2 = QLabel('background color')
        self.layout_color2.addWidget(self.label_color2)
        self.combobox_color2 = QComboBox()
        self.combobox_color2.setFixedWidth(200)
        self.combobox_color2.addItems(['none'] + font_color)
        for i, icolor in enumerate(['none'] + font_color):
            if icolor.startswith('- '):
                self.combobox_color2.model().item(i).setEnabled(False)
        self.combobox_color2.currentTextChanged.connect(
            self.on_background_changed)
        self.layout_color2.addWidget(self.combobox_color2)
        self.layout_options.addLayout(self.layout_color2)

        hline2 = QFrame()
        hline2.setFrameShape(QFrame.HLine)
        hline2.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline2)

        # target
        self.label_size = QLabel('Target')
        self.label_size.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_size)
        font_targets = {
            'Figure': [
                ('Figure Title', 'suptitle'),
            ],
            'Axes': [
                ('Title', 'title'),
                ('X Label', 'xlabel'),
                ('Y Label', 'ylabel'),
                ('X Tick Labels', 'xtick'),
                ('Y Tick Labels', 'ytick'),
            ],
            'Other': [
                ('Legend', 'legend'),
                ('Colorbar', 'colorbar'),
                ('Annotation', 'annotation'),
                ('Text', 'text'),
            ],
        }
        self.layout_target = QGridLayout()
        self.layout_target.setVerticalSpacing(2)
        self.layout_target.setHorizontalSpacing(10)
        self.button_group = QButtonGroup(self)
        self.button_to_key = {}
        self.buttons = {}
        row = 0
        for category, targets in font_targets.items():
            category_label = QLabel(category)
            self.layout_target.addWidget(category_label, row, 0)
            for i, (label, key) in enumerate(targets):
                button = QRadioButton(label)
                self.button_group.addButton(button)
                self.button_to_key[button] = key
                self.buttons[key] = button
                self.layout_target.addWidget(button, row + i, 1)
            row += len(targets)
        self.layout_options.addLayout(self.layout_target)
        self.buttons['suptitle'].setChecked(True)
        self.button_group.buttonClicked.connect(self.on_target_changed)

        hline3 = QFrame()
        hline3.setFrameShape(QFrame.HLine)
        hline3.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline3)

        # code
        self.label_code = QLabel('Codes')
        self.label_code.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(self.label_code)
        self.text_code = QPlainTextEdit()
        self.text_code.setFixedWidth(340)
        self.text_code.setPlainText('This is a text.')
        self.layout_options.addWidget(self.text_code, stretch=1)
        self.button_copy = QPushButton('Copy')
        self.button_copy.setFixedWidth(80)
        self.button_copy.clicked.connect(self.on_button_copy_clicked)
        self.layout_options.addWidget(
            self.button_copy, alignment=Qt.AlignRight)

        # layouts
        self.layout.addWidget(split_options)
        self.setLayout(self.layout)

        # initial plot
        self.update_plot()

    def changed_text(self, text):
        self.text_data = text
        self.update_plot()

    def on_changed_font(self, font: str):
        self.fontm.font = font
        self.update_plot()

    def on_button_copy_clicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_code.toPlainText())

    def on_target_changed(self, button):
        self.fontm.target = self.button_to_key[button]
        self.update_plot()

    def on_size_changed(self, size: float):
        self.fontm.size = size
        self.update_plot()

    def on_weight_changed(self, weight: str):
        self.fontm.weight = weight
        self.update_plot()

    def on_foreground_changed(self, color: str):
        self.fontm.foreground = color
        self.update_plot()

    def on_background_changed(self, color: str):
        self.fontm.background = color
        self.update_plot()

    def update_plot(self):
        self.canvas.fig.clear()
        self.canvas.ax.axis('off')

        # Layout
        # Target
        # Default:
        #   settings
        #   preview
        # User:
        #   settings
        #   preview
        gs = GridSpec(
            3,
            1,
            figure=self.canvas.fig,
            height_ratios=[1, 4, 4],
            hspace=0.15,
        )

        ax_target = self.canvas.fig.add_subplot(gs[0])
        ax_default = self.canvas.fig.add_subplot(gs[1])
        ax_user = self.canvas.fig.add_subplot(gs[2])

        for ax in (ax_target, ax_default, ax_user):
            ax.axis('off')

        # Target
        ax_target.text(
            0.5,
            0.5,
            f'Target: {self.fontm.target}',
            ha='center',
            va='center',
            fontsize=14,
            fontweight='bold',
            transform=ax_target.transAxes,
        )

        # Default
        self.draw_font_section(
            ax_default,
            title='Default',
            settings=self.fontm.get_default_settings(),
        )

        # User Setting
        user_settings = {
            'Font Family': self.fontm.font,
            'Font Style': self.fontm.style,
            'Size': self.fontm.size,
            'Weight': self.fontm.weight,
            'Foreground Color': self.fontm.foreground,
            'Background Color': self.fontm.background
        }
        self.draw_font_section(
            ax_user,
            title='User Setting',
            settings=user_settings,
        )

        self.canvas.fig.subplots_adjust(
            left=0.05,
            right=0.95,
            top=0.95,
            bottom=0.05,
        )
        self.canvas.draw()

    def draw_font_section(self, ax, title, settings):
        # Section title / settings / preview
        gs = ax.get_subplotspec().subgridspec(
            3, 1,
            height_ratios=[0.4, 1.0, 1.2],
            hspace=0.0,
        )

        # Title
        ax_title = ax.figure.add_subplot(gs[0])
        ax_title.axis('off')
        ax_title.text(
            0.5, 0.5, title,
            ha='center',
            va='center',
            fontweight='bold',
        )

        # Settings
        ax_settings = ax.figure.add_subplot(gs[1])
        ax_settings.axis('off')

        columns = [
            [
                ('Font Family', settings['Font Family']),
                ('Font Style', settings['Font Style']),
            ],
            [
                ('Size', settings['Size']),
                ('Weight', settings['Weight']),
            ],
            [
                ('Foreground Color', settings['Foreground Color']),
                ('Background Color', settings['Background Color']),
            ],
        ]

        # 3 columns × 2 rows (for each item preview "label | : | value")
        settings_gs = ax_settings.get_subplotspec().subgridspec(
            2, 9,
            width_ratios=[
                1.5, 0.15, 1.3,
                1.3, 0.15, 1.0,
                1.7, 0.15, 1.2,
            ],
            hspace=0.0,
            wspace=0.15,
        )

        for col, items in enumerate(columns):
            col2 = col * 3
            for row, (label, value) in enumerate(items):
                ax_label = ax.figure.add_subplot(settings_gs[row, col2])
                ax_colon = ax.figure.add_subplot(settings_gs[row, col2 + 1])
                ax_value = ax.figure.add_subplot(settings_gs[row, col2 + 2])
                for a in (ax_label, ax_colon, ax_value):
                    a.axis('off')
                ax_label.text(1.0, 0.5, label, ha='right', va='center')
                ax_colon.text(0.5, 0.5, ':', ha='center', va='center')
                ax_value.text(0.0, 0.5, str(value), ha='left', va='center')

        # Preview text
        ax_preview = ax.figure.add_subplot(gs[2])
        # ax_preview.axis('off')
        ax_preview.set_xticks([])
        ax_preview.set_yticks([])
        color = settings['Foreground Color']
        if settings['Foreground Color'] == 'auto':
            color = 'black'
        ax_preview.text(
            0.5, 0.5,
            self.text_data,
            ha='center',
            va='center',
            fontfamily=settings['Font Family'],
            fontsize=settings['Size'],
            fontstyle=settings['Font Style'],
            fontweight=settings['Weight'],
            color=color,
            backgroundcolor=settings['Background Color']
        )
