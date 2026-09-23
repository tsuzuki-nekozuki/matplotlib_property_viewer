import matplotlib.pyplot as plt

rcparams: dict = {
    'suptitle': {
        'Font Family': plt.rcParams['font.family'][0],
        'Font Style': plt.rcParams['font.style'],
        'Size': plt.rcParams['figure.titlesize'],
        'Weight': plt.rcParams['figure.titleweight'],
        'Foreground Color': plt.rcParams['text.color'],
        'Background Color': 'none',
    },
    'title': {
        'Font Family': plt.rcParams['font.family'][0],
        'Font Style': plt.rcParams['font.style'],
        'Size': plt.rcParams['axes.titlesize'],
        'Weight': plt.rcParams['axes.titleweight'],
        'Foreground Color': plt.rcParams['axes.titlecolor'],
        'Background Color': 'none',
    },
    'xlabel': {
        'Font Family': plt.rcParams['font.family'][0],
        'Font Style': plt.rcParams['font.style'],
        'Size': plt.rcParams['axes.labelsize'],
        'Weight': plt.rcParams['axes.labelweight'],
        'Foreground Color': plt.rcParams['axes.labelcolor'],
        'Background Color': 'none',
    },
    'ylabel': {
        'Font Family': plt.rcParams['font.family'][0],
        'Font Style': plt.rcParams['font.style'],
        'Size': plt.rcParams['axes.labelsize'],
        'Weight': plt.rcParams['axes.labelweight'],
        'Foreground Color': plt.rcParams['axes.labelcolor'],
        'Background Color': 'none',
    },
    'xtick': {
        'Font Family': plt.rcParams['font.family'][0],
        'Font Style': plt.rcParams['font.style'],
        'Size': plt.rcParams['xtick.labelsize'],
        'Weight': plt.rcParams['font.weight'],
        'Foreground Color': plt.rcParams['xtick.color'],
        'Background Color': 'none',
    },
    'ytick': {
        'Font Family': plt.rcParams['font.family'][0],
        'Font Style': plt.rcParams['font.style'],
        'Size': plt.rcParams['ytick.labelsize'],
        'Weight': plt.rcParams['font.weight'],
        'Foreground Color': plt.rcParams['ytick.color'],
        'Background Color': 'none',
    },
    'legend': {
        'Font Family': plt.rcParams['font.family'][0],
        'Font Style': plt.rcParams['font.style'],
        'Size': plt.rcParams['legend.fontsize'],
        'Weight': plt.rcParams['font.weight'],
        'Foreground Color': plt.rcParams['text.color'],
        'Background Color': plt.rcParams['legend.facecolor'],
    },
    'colorbar': {
        'Font Family': plt.rcParams['font.family'][0],
        'Font Style': plt.rcParams['font.style'],
        'Size': plt.rcParams['xtick.labelsize'],
        'Weight': plt.rcParams['font.weight'],
        'Foreground Color': plt.rcParams['xtick.color'],
        'Background Color': plt.rcParams['axes.facecolor'],
    },
    'annotation': {
        'Font Family': plt.rcParams['font.family'][0],
        'Font Style': plt.rcParams['font.style'],
        'Size': plt.rcParams['font.size'],
        'Weight': plt.rcParams['font.weight'],
        'Foreground Color': plt.rcParams['text.color'],
        'Background Color': 'none',
    },
    'text': {
        'Font Family': plt.rcParams['font.family'][0],
        'Font Style': plt.rcParams['font.style'],
        'Size': plt.rcParams['font.size'],
        'Weight': plt.rcParams['font.weight'],
        'Foreground Color': plt.rcParams['text.color'],
        'Background Color': 'none',
    }
}

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
