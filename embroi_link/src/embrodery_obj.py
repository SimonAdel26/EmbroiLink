import cv2
import json
from pathlib import Path

PROJECT_DIR = Path.cwd() / "embroi_link"
IMAGES_DIR_PATH = PROJECT_DIR / "backup/images"
IMAGES_RESULTS_DIR_PATH = PROJECT_DIR / "backup/results"
HISTORY_FILE_PATH = PROJECT_DIR / "backup/projects.json"


class EmbroderyObj:
    def __init__(self):
        self.image_path = None
        self.cv_image = None
        self.cv_image_result = None
        self.list_colors = []

        self._init_projects_backup()

    def _init_projects_backup(self):
        if not IMAGES_RESULTS_DIR_PATH.exists():
            IMAGES_RESULTS_DIR_PATH.mkdir(parents=True, exist_ok=True)

        if not IMAGES_DIR_PATH.exists():
            IMAGES_DIR_PATH.mkdir(parents=True, exist_ok=True)

        if not HISTORY_FILE_PATH.exists():
            with open(HISTORY_FILE_PATH, "w") as f:
                json.dump({}, f, indent=4)

    def _save_to_file(self, data):
        try:
            with open(HISTORY_FILE_PATH, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as ex:
            print(f"Save failed! {ex}")

    def load_image(self, image_path, uploaded=False):
        if uploaded:
            with open(HISTORY_FILE_PATH, "r") as f:
                data = json.load(f)

            self.cv_image = cv2.imread(image_path)
            self.image_path = IMAGES_DIR_PATH / Path(image_path).name
            if not self.image_path in data.keys():
                data[str(self.image_path)] = {}

                if cv2.imwrite(self.image_path, self.cv_image):
                    self._save_to_file(data)
                else:
                    print(f"Image {self.image_path} NOT saved ")

            self._save_to_file(data)
            return

        self.image_path = Path(image_path)
        self.cv_image = cv2.imread(self.image_path)
        self.cv_image_result = self.get_generated_file()

    def save_image(self):
        if self.cv_image_result is None:
            print("No image to save")
            return

        image_name_base = self.image_path.stem
        extension = self.image_path.suffix
        last_saved_path = self.get_last_saved_path()
        contor = 0
        if last_saved_path:
            contor = int(last_saved_path.split("-")[1].split(".")[0]) + 1

        current_image_name = f"{image_name_base}-{contor}{extension}"
        image_path = IMAGES_RESULTS_DIR_PATH / Path(current_image_name)

        if not cv2.imwrite(image_path, self.cv_image_result):
            print(f"Image {image_path} NOT saved ")

    def get_last_saved_path(self):
        image_name_base = self.image_path.stem
        extension = self.image_path.suffix

        list_image = []
        for element in IMAGES_RESULTS_DIR_PATH.iterdir():
            if element.is_file():
                if image_name_base in element.name:
                    list_image.append(element.name)

        list_image = sorted(list_image)
        if len(list_image):
            return list_image[-1]

        return None

    def get_generated_file(self):
        last_saved_path = self.get_last_saved_path()
        if last_saved_path:
            return cv2.imread(IMAGES_RESULTS_DIR_PATH / Path(last_saved_path))
        return last_saved_path

    def colors(self, list_colors, added=False):
        with open(HISTORY_FILE_PATH, "r") as f:
            data = json.load(f)

        if added:
            self.list_colors = list_colors
            data[str(self.image_path)]["colors"] = self.list_colors
            self._save_to_file(data)
            return

        if "colors" in data[str(self.image_path)].keys():
            self.list_colors = data[str(self.image_path)]["colors"]
        else:
            self.list_colors = []
