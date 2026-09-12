# EmbroiLink
Generating an embroidery design from an image 

## Features 

- **Image Loading**
  - Imports images from the local system.
  - Displays the original image in the interface.
  - Each uploaded image is automatically saved in the *history* list.

- **History of Loaded Images**
  - The application maintains a history list of loaded images.
  - The list is saved in a JSON file in the form of a dictionary.
  - Allows previously used images to be reloaded quickly.
  - Each entry contains the full path to the image.

- **Selectable Embroidery Zones**
  - Allows you to select an area of the embroidery image by clicking.
  - Double-clicking on the selected area changes its colour.
  - The modified colour is automatically updated in the table and in the internal list.
  - Changes are saved to the JSON file under the current image’s key.

- **K-Means Colour Extraction**
  - Applies the K-Means algorithm to extract dominant colours.
  - Runs the processing in a separate thread to prevent the UI from freezing.
  - Automatically generates a colour palette for embroidery.

- **Thread Colour Table**
  - An interactive table where each cell represents a colour.
  - Right-clicking on a cell allows you to select the stitch type.
  - The selected stitch type is displayed as a number in the cell.
  - Below the table there is a *label* listing the stitch types, with a number assigned to each stitch 
  - The text in the cell is centred and its colour is automatically adjusted for visibility.

- **Scrollable Number Picker**
  - Custom menu built using `QListWidget`
  - Allows quick selection of the stitch type (number).

- **Colour Editing**
  - Manual editing of colours in the table.
  - Automatic adjustment of text colour (white/black) based on background brightness.
  - Cell colour is retained when the number changes.

- **Data Persistence (JSON)**
  - All entered information is saved to a JSON file.
  - The storage structure is a dictionary where **the key is the image path**, and the value contains:
    - the list of colours generated or modified,
    - the list of stitch types selected by the user,
  - When the application is opened, the data is automatically restored from the JSON file.

- **Image Preview & Result**
  - Display of the processed image.
  - Export of the final result.

- **Modern PyQt6 UI**
  - Interface created in Qt Designer.
  - Well-organised signals and slots.
  - Custom UI components for embroidery.

##  Development Environment

The project was developed in an isolated environment using:

- **WSL2 (Windows Subsystem for Linux 2)**
  The application runs and is developed in a real Linux environment, provided by WSL2, to ensure maximum compatibility with Python libraries and image processing tools.

- **Docker + DevContainer**
  The project uses a *Development Container* (devcontainer) to ensure:
  - a reproducible working environment,
  - the same versions of Python and libraries on any system,
  - automatic installation of dependencies,
  - complete isolation from the host system.

To open the project in VS Code, use the option:
**“Reopen in Container”**, which automatically starts the configured devcontainer.

##  Dependencies

The project uses the following Python libraries:

- **PyQt6** – graphical user interface (UI), widgets, dialogue boxes, colour palette, menus.
- **NumPy** – numerical operations, data manipulation for K-Means.
- **OpenCV (opencv-python)** – image processing, conversions, extraction of selected areas.
- **json** (standard library) – saving data to a JSON file (colours, stitches).
- **threading** – running K-Means in a separate thread to prevent the UI from freezing.
- **pathlib** – managing file paths and the project structure.

## Usage 

### 1. Launching the app
Once installed, launch the app by:
``` bash 
make run 
```

### 2. Uploading an image
  - Use the ‘Upload Image’ button to upload an image from your system.
  - The image is displayed in the main window.
  - The image path is automatically added to the history list and saved in the JSON file.
  - If the image has been used before, the application automatically loads the previously saved colours and stitch types.

### 3. Selecting an area of the image
  - Click on the image to select an area.
  - Double-click on the selected area to change its colour.
  - The modified colour is automatically added:
    - to the colour table,
    - to the internal colour list,
    - to the JSON file under the current image’s key.

### 4. Generating the colour palette (K-Means)
  - Use the ‘Create Design’  button .
  - The K-Means algorithm runs in a separate thread to prevent the UI from freezing.
  - The colour palette is displayed in the colour table.
  - The generated image is displayed in the main window

### 5. Thread Colour Table
  - An interactive table where each cell represents a colour.
  - Right-clicking on a cell allows you to select the stitch type.
  - The selected stitch type is displayed as a number in the cell.
  - Below the table there is a *label* listing the stitch types, with a number assigned to each stitch 
  - The text in the cell is centred and its colour is automatically adjusted for visibility.

### 6. Selecting the stitch type (Scrollable Number Picker)
  - Right-clicking on a cell opens a scrollable dialogue box.
  - The dialogue box is built using a QListWidget to enable scrolling.
  - Select the desired number (stitch type).
  - The number is displayed in the cell and saved in JSON.

### 7. Saving data (JSON)
  - The application automatically saves all the information to a JSON file.
The structure is as follows:
``` bash
{
  „image_path1.png”: {
    „colors”: {[...],[...],...,[...]}
    „types_of_stitches”: [...],
  }
  „image_path2.png”: {
    „colors”: {[...],[...],...,[...]}
    „types_of_stitches”: [...],
  }
  .
  .
  .
}
```

  - The key is the image path,
  - the value is a dictionary containing:
    - the list of colours generated or modified,
    - the list of stitch types selected by the user,

When the application is opened, the data is automatically restored.

### 8. Saving the result
  - The processed image can be saved using the Save Image button.
  - The file includes the colours and any changes made.