import tkinter as tk
from tkinter import messagebox
import platform


def beep():
    system = platform.system()
    try:
        if system == "Windows":
            import winsound
            for _ in range(3):
                winsound.Beep(1000, 500)
        elif system == "Darwin":
            for _ in range(3):
                print("\a", end="", flush=True)
        else:
            for _ in range(3):
                print("\a", end="", flush=True)
    except Exception:
        print("\a", end="", flush=True)


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minuteur")
        self.root.resizable(False, False)
        self.root.configure(padx=20, pady=15)

        self.total_seconds = 0
        self.remaining = 0
        self.running = False
        self.job = None

        self.settings_frame = tk.Frame(self.root)
        self.settings_frame.pack()

        self.vars = {}
        for label in ("Heures", "Minutes", "Secondes"):
            frame = tk.Frame(self.settings_frame)
            frame.pack(side="left", padx=8)
            var = tk.StringVar(value="00")
            entry = tk.Entry(frame, textvariable=var, width=4, justify="center",
                             font=("Helvetica", 14))
            entry.pack()
            tk.Label(frame, text=label).pack()
            self.vars[label] = var

        self.label = tk.Label(self.root, text="00:00:00",
                              font=("Helvetica", 48, "bold"), fg="#222222")
        self.label.pack(pady=15)

        buttons = tk.Frame(self.root)
        buttons.pack()

        self.start_btn = tk.Button(buttons, text="Démarrer", width=10,
                                   command=self.start)
        self.start_btn.pack(side="left", padx=5)

        self.pause_btn = tk.Button(buttons, text="Pause", width=10,
                                   state="disabled", command=self.pause)
        self.pause_btn.pack(side="left", padx=5)

        self.reset_btn = tk.Button(buttons, text="Réinitialiser", width=10,
                                   state="disabled", command=self.reset)
        self.reset_btn.pack(side="left", padx=5)

        self.root.bind("<Return>", lambda e: self.start())

    def read_inputs(self):
        values = []
        for label in ("Heures", "Minutes", "Secondes"):
            text = self.vars[label].get().strip()
            if not text.isdigit():
                raise ValueError(f"Valeur invalide pour {label} : {text!r}")
            values.append(int(text))
        h, m, s = values
        if m > 59 or s > 59:
            raise ValueError("Minutes et secondes doivent être entre 0 et 59")
        return h * 3600 + m * 60 + s

    def format_time(self, seconds):
        h, rem = divmod(max(seconds, 0), 3600)
        m, s = divmod(rem, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    def start(self):
        if self.running:
            return
        if self.remaining <= 0:
            try:
                self.total_seconds = self.read_inputs()
            except ValueError as e:
                messagebox.showerror("Erreur", str(e))
                return
            if self.total_seconds <= 0:
                messagebox.showerror("Erreur", "Entrez une durée supérieure à 0")
                return
            self.remaining = self.total_seconds
        self.running = True
        self.label.config(fg="#0a7d0a")
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        self.reset_btn.config(state="normal")
        for var in self.vars.values():
            var.set("")
        self.tick()

    def tick(self):
        if not self.running:
            return
        self.label.config(text=self.format_time(self.remaining))
        if self.remaining <= 0:
            self.finish()
            return
        self.remaining -= 1
        self.job = self.root.after(1000, self.tick)

    def pause(self):
        self.running = False
        if self.job is not None:
            self.root.after_cancel(self.job)
            self.job = None
        self.label.config(fg="#b8860b")
        self.start_btn.config(text="Reprendre", state="normal")
        self.pause_btn.config(state="disabled")

    def reset(self):
        self.running = False
        if self.job is not None:
            self.root.after_cancel(self.job)
            self.job = None
        self.remaining = 0
        self.total_seconds = 0
        self.label.config(text="00:00:00", fg="#222222")
        self.start_btn.config(text="Démarrer", state="normal")
        self.pause_btn.config(state="disabled")
        self.reset_btn.config(state="disabled")
        for var in self.vars.values():
            var.set("00")

    def finish(self):
        self.running = False
        self.job = None
        self.label.config(text="00:00:00", fg="#b00000")
        self.start_btn.config(text="Démarrer", state="normal")
        self.pause_btn.config(state="disabled")
        self.reset_btn.config(state="disabled")
        for var in self.vars.values():
            var.set("00")
        beep()
        messagebox.showinfo("Minuteur", "Temps écoulé !")


if __name__ == "__main__":
    root = tk.Tk()
    TimerApp(root)
    root.mainloop()
