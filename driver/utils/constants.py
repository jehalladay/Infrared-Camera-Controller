# config keys

MLX_CONFIG_JSON = './config/mlx.json'
MP_CONFIG_JSON = './config/mp.json'
SPECTRO_CONFIG_JSON = './config/spectro.json'
ONCE_CONFIG_JSON = './config/once.json'
RADAR_CONFIG_JSON = './config/radar.json'
VISUALIZE_CONFIG_JSON = './config/visualize.json'
COMPOSE_CONFIG_JSON = './config/compose.json'

# Top level keys
SIZE = 'size'
STORAGE = 'storage'
RECORDING = 'recording'
TRIGGERS = 'triggers'
COLOR_CHANNELS = 'color_channels'
ALPHA = 'alpha'
PLACEMENT = 'placement'
MODE = 'mode'
MP = "MP"
MLX = "MLX"
SP = "SP"
RUN = "run"

# Size keys
WIDTH = 'width'
HEIGHT = 'height'
CHANNELS = 'channels'

# Storage keys
PRECISION = 'precision'
LOCATION = 'location'
PATH = 'path'

# Recording keys
FREQUENCY = 'frequency'
DURATION = 'duration'

# Trigger keys


# Misc constants
DATE_FORMAT = '%Y_%m_%d'
TIME_FORMAT = '%H_%M_%S'
STALL_TIME = 0.01 # seconds until we try to get a new frame after failing to get one
TIMESTAMP = 'timestamp'
DPI = 'dpi'
X = 'x'
Y = 'y'
ALPHA = 'alpha'

# Spectrometer constants
SPECTRO_ADDRESS = 0x49
SPECTRO_GPIO = 21

# Visualization constants
SCALING_FACTOR = "scaling_factor"
