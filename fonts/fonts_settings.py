from dataclasses import dataclass, field

from fonts.fonts_defaults import rcparams


@dataclass
class FontsSettings:
    first_target = next(iter(rcparams))
    params = rcparams[first_target]
    target: str = field(init=False, default=first_target)
    font: str = field(init=False, default=params['Font Family'])
    style: str = field(init=False, default=params['Font Style'])
    size: float | str = field(init=False, default=params['Size'])
    weight: int = field(init=False, default=params['Weight'])
    foreground: str = field(init=False, default=params['Foreground Color'])
    background: str = field(init=False, default=params['Background Color'])
