import tkinter as tk

root = tk.Tk()
# keep the window from showing
root.withdraw()

# read the clipboard
c = root.clipboard_get()
print(c)