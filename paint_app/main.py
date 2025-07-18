import tkinter as tk
from MainPaint import MainPaint
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Графический растровый редактор")
    parser.add_argument('--batch', action='store_true',
                        help="Запуск в пакетном режиме")
    args = parser.parse_args()
    if args.batch:
        print("Запуск в пакетном режиме...")
    root = tk.Tk()
    app = MainPaint(root)
    root.mainloop()
