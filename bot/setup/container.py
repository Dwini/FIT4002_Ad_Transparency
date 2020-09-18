from pyvirtualdisplay import Display

# Setup for container builds
# if this is running in the container, import and create virtual display.
def start_display():
    display = Display(visible=0, size=(800, 600))
    display.start()
    return display