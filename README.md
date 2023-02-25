![](ui/gnapper.png)

# Cnipe

Application to generate beautiful screenshots

### Features:

1. Take Screenshots
2. Add beautiful gradients to the background
3. Save the image and share it to others

### Usage

1. Working directory : ``~\cnipe\src``
2. ``
   python ui.py
   ``

## Build

```
pyinstaller --noconfirm --onedir --windowed --icon "E:/Others/GNapper/ui/gnapper.ico" --name "Cnipe" --add-data "E:/Others/GNapper/src;src/" --add-data "E:/Others/GNapper/ui;ui/" --add-data "E:/Others/GNapper/venv/Lib/site-packages/customtkinter;customtkinter/"  "E:/Others/GNapper/cnipe.py"
```


# Sample Images
![fc](temp/fscshot.jpg)
