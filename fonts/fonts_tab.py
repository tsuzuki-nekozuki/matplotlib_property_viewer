from matplotlib.gridspec import GridSpec
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QComboBox, QGridLayout,
    QDoubleSpinBox, QLineEdit, QPushButton, QButtonGroup, QRadioButton,
    QPlainTextEdit, QSplitter, QSizePolicy, QApplication
)

from common.mpl_properties import (
    get_fonts_list, get_color_list, get_font_style_list, get_font_weight_list
)
from common.aspect_ratio import AspectRatioWidget
from fonts.fonts_defaults import font_targets, rcparams
from fonts.fonts_manager import FontsManager


class FontsTab(QWidget):
    def __init__(self, canvas):
        super().__init__()

        # FontsManager
        self.fm = FontsManager()
        # target and its default params
        self.fm.target = next(iter(rcparams))
        self.def_params = rcparams[self.fm.target]

        # text
        self.text_data = 'write your text here.'

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
        self.text_edit = QLineEdit()
        self.construct_text()

        hline1 = QFrame()
        hline1.setFrameShape(QFrame.HLine)
        hline1.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline1)

        # target
        self.button_group = QButtonGroup(self)
        self.button_to_key = {}
        self.buttons = {}
        self.construct_target()

        hline2 = QFrame()
        hline2.setFrameShape(QFrame.HLine)
        hline2.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline2)

        # settings
        self.combobox_font = QComboBox()
        self.combobox_style = QComboBox()
        self.spinbox_size = QDoubleSpinBox()
        self.combobox_weight = QComboBox()
        self.combobox_color1 = QComboBox()
        self.combobox_color2 = QComboBox()
        self.construct_settings()

        hline3 = QFrame()
        hline3.setFrameShape(QFrame.HLine)
        hline3.setFrameShadow(QFrame.Sunken)
        self.layout_options.addWidget(hline3)

        # code
        label_code = QLabel('Codes')
        label_code.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(label_code)
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

    def construct_text(self):
        label_text = QLabel('Text')
        label_text.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(label_text)

        self.text_edit.setText(self.text_data)
        self.text_edit.textChanged.connect(self.changed_text)
        self.layout_options.addWidget(self.text_edit)

    def changed_text(self, text):
        self.text_data = text
        self.update_plot()

    def construct_target(self):
        label_size = QLabel('Target')
        label_size.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(label_size)

        layout_target = QGridLayout()
        layout_target.setVerticalSpacing(2)
        layout_target.setHorizontalSpacing(10)
        row = 0
        for category, targets in font_targets.items():
            category_label = QLabel(category)
            layout_target.addWidget(category_label, row, 0)
            for i, (label, key) in enumerate(targets):
                button = QRadioButton(label)
                self.button_group.addButton(button)
                self.button_to_key[button] = key
                self.buttons[key] = button
                layout_target.addWidget(button, row + i, 1)
            row += len(targets)
        self.layout_options.addLayout(layout_target)
        self.buttons['suptitle'].setChecked(True)
        self.button_group.buttonClicked.connect(self.on_target_changed)

    def on_target_changed(self, button):
        self.fm.target = self.button_to_key[button]
        self.def_params = rcparams[self.fm.target]
        # set defaults
        index = self.combobox_font.findText(self.def_params['Font Family'])
        if index >= 0:
            self.combobox_font.setCurrentIndex(index)
        index = self.combobox_style.findText(self.def_params['Font Style'])
        if index >= 0:
            self.combobox_style.setCurrentIndex(index)
        self.spinbox_size.setValue(self.def_params['Size'])
        index = self.combobox_weight.findText(self.def_params['Weight'])
        if index >= 0:
            self.combobox_weight.setCurrentIndex(index)
        color1 = self.def_params['Foreground Color']
        if color1 == 'auto':
            color1 = 'black'
        index = self.combobox_color1.findText(color1)
        if index >= 0:
            self.combobox_color1.setCurrentIndex(index)
        color2 = self.def_params['Background Color']
        if color2 == 'auto':
            color2 = 'black'
        index = self.combobox_color2.findText(color2)
        if index >= 0:
            self.combobox_color2.setCurrentIndex(index)
        self.update_plot()

    def construct_settings(self):
        label_settings = QLabel('Settings')
        label_settings.setStyleSheet('font-size: 18px;')
        self.layout_options.addWidget(label_settings)
        layout_font = QHBoxLayout()
        label_font = QLabel('font')
        layout_font.addWidget(label_font)
        font_list = get_fonts_list()
        self.combobox_font.addItems(font_list)
        self.combobox_font.setFixedWidth(260)
        index = self.combobox_font.findText(self.def_params['Font Family'])
        if index >= 0:
            self.combobox_font.setCurrentIndex(index)
        self.combobox_font.currentTextChanged.connect(self.on_changed_font)
        layout_font.addWidget(self.combobox_font)
        self.layout_options.addLayout(layout_font)

        layout_style = QHBoxLayout()
        label_style = QLabel('style')
        layout_style.addWidget(label_style)
        style_list = get_font_style_list()
        self.combobox_style.addItems(style_list)
        self.combobox_style.setFixedWidth(260)
        index = self.combobox_style.findText(self.def_params['Font Style'])
        if index >= 0:
            self.combobox_style.setCurrentIndex(index)
        self.combobox_style.currentTextChanged.connect(self.on_changed_style)
        layout_style.addWidget(self.combobox_style)
        self.layout_options.addLayout(layout_style)

        # size and weight
        layout_size_weight = QHBoxLayout()
        label_size = QLabel('Size')
        layout_size_weight.addWidget(label_size)

        self.spinbox_size.setFixedWidth(90)
        self.spinbox_size.setMinimum(0.1)
        self.spinbox_size.setMaximum(50)
        self.spinbox_size.setDecimals(1)
        self.spinbox_size.setSingleStep(0.1)
        self.spinbox_size.setValue(self.def_params['Size'])
        self.spinbox_size.valueChanged.connect(self.on_changed_size)
        layout_size_weight.addWidget(self.spinbox_size)

        label_weight = QLabel('Weight')
        layout_size_weight.addWidget(label_weight)

        weight_list = get_font_weight_list()
        self.combobox_weight.addItems(weight_list)
        self.combobox_weight.setFixedWidth(90)
        index = self.combobox_weight.findText(self.def_params['Weight'])
        if index >= 0:
            self.combobox_weight.setCurrentIndex(index)
        self.combobox_weight.setFixedWidth(90)
        self.combobox_weight.currentTextChanged.connect(self.on_changed_weight)
        layout_size_weight.addWidget(self.combobox_weight)
        self.layout_options.addLayout(layout_size_weight)

        # color
        font_color = get_color_list()
        layout_color1 = QHBoxLayout()
        label_color1 = QLabel('foreground color')
        layout_color1.addWidget(label_color1)
        self.combobox_color1.setFixedWidth(200)
        self.combobox_color1.addItems(font_color)
        for i, icolor in enumerate(font_color):
            if icolor.startswith('- '):
                self.combobox_color1.model().item(i).setEnabled(False)
        color1 = self.def_params['Foreground Color']
        if color1 == 'auto':
            color1 = 'black'
        index = self.combobox_color1.findText(color1)
        if index >= 0:
            self.combobox_color1.setCurrentIndex(index)
        self.combobox_color1.currentTextChanged.connect(self.on_changed_color1)
        layout_color1.addWidget(self.combobox_color1)
        self.layout_options.addLayout(layout_color1)

        layout_color2 = QHBoxLayout()
        label_color2 = QLabel('background color')
        layout_color2.addWidget(label_color2)
        self.combobox_color2.setFixedWidth(200)
        self.combobox_color2.addItems(['none'] + font_color)
        for i, icolor in enumerate(['none'] + font_color):
            if icolor.startswith('- '):
                self.combobox_color2.model().item(i).setEnabled(False)
        color2 = self.def_params['Background Color']
        if color2 == 'auto':
            color2 = 'black'
        index = self.combobox_color2.findText(color2)
        if index >= 0:
            self.combobox_color2.setCurrentIndex(index)
        self.combobox_color2.currentTextChanged.connect(self.on_changed_color2)
        layout_color2.addWidget(self.combobox_color2)
        self.layout_options.addLayout(layout_color2)

    def on_changed_font(self, font: str):
        self.fm.font = font
        self.update_plot()

    def on_changed_style(self, style: str):
        self.fm.style = style
        self.update_plot()

    def on_changed_size(self, size: float):
        self.fm.size = size
        self.update_plot()

    def on_changed_weight(self, weight: str):
        self.fm.weight = weight
        self.update_plot()

    def on_changed_color1(self, color: str):
        self.fm.foreground = color
        self.update_plot()

    def on_changed_color2(self, color: str):
        self.fm.background = color
        self.update_plot()

    def update_plot(self):
        self.canvas.fig.clear()
        self.canvas.ax.axis('off')

        # Layout
        # Target
        # User:
        #   settings
        #   preview
        # Default:
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
        ax_user = self.canvas.fig.add_subplot(gs[1])
        ax_default = self.canvas.fig.add_subplot(gs[2])

        for ax in (ax_target, ax_user, ax_default):
            ax.axis('off')

        # Target
        ax_target.text(
            0.5,
            0.5,
            f'Target: {self.fm.target}',
            ha='center',
            va='center',
            fontsize=14,
            fontweight='bold',
            transform=ax_target.transAxes,
        )

        # User Setting
        user_settings = {
            'Font Family': self.fm.font,
            'Font Style': self.fm.style,
            'Size': self.fm.size,
            'Weight': self.fm.weight,
            'Foreground Color': self.fm.foreground,
            'Background Color': self.fm.background
        }
        self.draw_font_section(
            ax_user,
            title='User Setting',
            settings=user_settings,
        )

        # Default
        self.draw_font_section(
            ax_default,
            title='Default Setting',
            settings=self.def_params,
        )

        self.canvas.fig.subplots_adjust(
            left=0.05,
            right=0.95,
            top=0.95,
            bottom=0.05,
        )

        self.canvas.draw()
        self.text_code.setPlainText(self.fm.generate_code())

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

    def on_button_copy_clicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_code.toPlainText())
