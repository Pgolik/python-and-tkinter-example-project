import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog

RootDir = os.path.curdir
FilePathToSavedDirPaths = os.path.join(RootDir, "saved_dirs.txt")
LinuxPath = "~/Pulpit"

class Window(tk.Frame):
    widgets_list = []
    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.pack(fill=BOTH, expand=True)

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World"
        self.hi_there["command"] = self.browse_files
        self.hi_there.pack(fill=tk.X, pady=4, expand=False)
        self.load_treeview()
        self.quit = tk.Button(self, text="QUIT", fg="blue", command=self.master.destroy)
        self.quit.pack(fill=tk.X, pady=4, expand=False)

    def load_treeview(self, f_handle=None):
        if not os.path.exists(FilePathToSavedDirPaths):
            return
        self.treeview =ttk.Treeview(self, columns=("Zapisane_ścieżki"))
        self.scrollbar = tk.Scrollbar(self.treeview)
        self.treeview.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview.heading('#0', text='Id')
        self.treeview.heading('#1', text='Ścieżka')
        self.treeview.column('#0', stretch=tk.YES)
        self.treeview.column('#1', stretch=tk.YES)
        self.treeview.pack(fill=tk.X, pady=4, expand=False)
        self.scrollbar.config(command=self.treeview.yview)
        if not f_handle: 
            with open(FilePathToSavedDirPaths) as f_handle:
                [self.insert_to_tree_view(id,line) for id,line in enumerate(f_handle.readlines())]
        else :
            [self.insert_to_tree_view(id,line) for id,line in enumerate(f_handle.readlines())]


    def insert_to_tree_view(self, id, line):
        self.treeview.insert('', 'end', text=str(id), values=(line))

    def browse_files(self):
        dirpath = filedialog.askdirectory(initialdir=LinuxPath, title="Wybierz katalog")
        if not os.path.exists(FilePathToSavedDirPaths) :
            open(FilePathToSavedDirPaths, mode="w")
        with open(FilePathToSavedDirPaths, mode="r+") as f_handle:
            tmp_id = 0
            for line in f_handle.read().splitlines():
                tmp_id = tmp_id + 1 
                if line == dirpath :
                    return
            if tmp_id == 0:
                self.load_treeview()
            self.insert_to_tree_view(tmp_id, dirpath)
            f_handle.write(dirpath + '\n')


def main() :
    root = tk.Tk()
    root.title("Pobieranie z excela!")
    window = Window(root)
    root.geometry(str(int(root.winfo_screenwidth()/3)) + "x" + str(root.winfo_screenheight()))
    window.mainloop()

if __name__ == "__main__":
    main()