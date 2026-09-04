from PyQt6.QtGui import QFont, QFontDatabase

current_dir = os.path.dirname(os.path.realpath(__file__))

def load_font():
    id = QFontDatabase.addApplicationFont(os.path.join(current_dir, "ui/VINERITC.TTF"))
    if id < 0:
        raise Exception("Failed to load font")