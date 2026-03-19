# ══════════════════════════════════════════════════════════════════════════════
#  Port Monitor — Gerenciador de Portas e Processos
#  Criado por Gabriel Vasconcellos
#  GitHub : https://github.com/GabrielVasconcellos/port-monitor
#  Licença: MIT
# ══════════════════════════════════════════════════════════════════════════════

__author__  = "Gabriel Vasconcellos"
__version__ = "1.0.0"
__github__  = "https://github.com/GabrielVasconcellos/port-monitor"
__license__ = "MIT"

import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import os
import signal
import threading
import time
from datetime import datetime


# ── Theme colors ──────────────────────────────────────────────────────────────
BG       = "#0d1117"
BG2      = "#161b22"
BG3      = "#21262d"
ACCENT   = "#58a6ff"
ACCENT2  = "#3fb950"
DANGER   = "#f85149"
WARNING  = "#d29922"
FG       = "#e6edf3"
FG2      = "#8b949e"
BORDER   = "#30363d"

FONT_TITLE  = ("Consolas", 15, "bold")
FONT_HEADER = ("Consolas", 10, "bold")
FONT_BODY   = ("Consolas", 10)
FONT_SMALL  = ("Consolas",  9)
FONT_BIG    = ("Consolas", 22, "bold")


def get_connections():
    """Return list of dicts with port info for TCP/UDP connections."""
    rows = []
    try:
        conns = psutil.net_connections(kind="inet")
    except Exception:
        return rows

    seen = set()
    for c in conns:
        if not c.laddr or not c.laddr.port:
            continue
        key = (c.laddr.port, c.pid or 0, c.status)
        if key in seen:
            continue
        seen.add(key)

        pid  = c.pid or 0
        name = path = ""
        try:
            if pid:
                proc = psutil.Process(pid)
                name = proc.name()
                exe  = proc.exe()
                path = exe if exe else ""
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            name = "Acesso negado"
            path = ""

        rows.append({
            "porta":     c.laddr.port,
            "protocolo": c.type.name if hasattr(c.type, "name") else str(c.type),
            "status":    c.status or "—",
            "pid":       pid,
            "processo":  name,
            "caminho":   path,
            "ip_local":  c.laddr.ip,
        })

    rows.sort(key=lambda r: r["porta"])
    return rows


class PortMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Port Monitor")
        self.geometry("1200x700")
        self.minsize(900, 500)
        self.configure(bg=BG)
        self._auto_refresh = tk.BooleanVar(value=True)
        self._filter_text  = tk.StringVar()
        self._filter_text.trace_add("write", lambda *_: self._apply_filter())
        self._all_rows: list[dict] = []
        self._build_ui()
        self._refresh()
        self._schedule_auto()

    # ── UI construction ──────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Top bar ──────────────────────────────────────────────────────────
        top = tk.Frame(self, bg=BG, pady=12, padx=18)
        top.pack(fill="x")

        tk.Label(top, text="⬡  PORT MONITOR", font=FONT_TITLE,
                 bg=BG, fg=ACCENT).pack(side="left")

        self._lbl_time = tk.Label(top, text="", font=FONT_SMALL, bg=BG, fg=FG2)
        self._lbl_time.pack(side="left", padx=18)

        # right-side controls
        ctrl = tk.Frame(top, bg=BG)
        ctrl.pack(side="right")

        tk.Checkbutton(ctrl, text="Auto-refresh (5s)",
                       variable=self._auto_refresh,
                       bg=BG, fg=FG2, selectcolor=BG3,
                       activebackground=BG, activeforeground=FG,
                       font=FONT_SMALL).pack(side="right", padx=8)

        self._btn_refresh = tk.Button(
            ctrl, text="↻  Atualizar", command=self._refresh,
            bg=BG3, fg=ACCENT, font=FONT_SMALL,
            relief="flat", padx=10, pady=4,
            cursor="hand2", activebackground=BORDER, activeforeground=ACCENT)
        self._btn_refresh.pack(side="right", padx=4)

        # ── Filter bar ───────────────────────────────────────────────────────
        fbar = tk.Frame(self, bg=BG2, padx=18, pady=8)
        fbar.pack(fill="x")

        tk.Label(fbar, text="Filtrar:", font=FONT_SMALL, bg=BG2, fg=FG2).pack(side="left")
        tk.Entry(fbar, textvariable=self._filter_text,
                 bg=BG3, fg=FG, insertbackground=ACCENT,
                 relief="flat", font=FONT_BODY,
                 width=40).pack(side="left", padx=8, ipady=4)

        tk.Label(fbar, text="(porta, processo, PID, caminho...)",
                 font=FONT_SMALL, bg=BG2, fg=FG2).pack(side="left")

        self._lbl_count = tk.Label(fbar, text="", font=FONT_SMALL, bg=BG2, fg=FG2)
        self._lbl_count.pack(side="right")

        # ── Table ────────────────────────────────────────────────────────────
        cols = ("porta", "protocolo", "status", "pid", "processo", "caminho")
        col_labels = {
            "porta":     "Porta",
            "protocolo": "Protocolo",
            "status":    "Status",
            "pid":       "PID",
            "processo":  "Processo",
            "caminho":   "Caminho do Executável",
        }
        col_widths = {
            "porta":     70,
            "protocolo": 90,
            "status":    110,
            "pid":       70,
            "processo":  160,
            "caminho":   520,
        }

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                        background=BG2, foreground=FG,
                        rowheight=26, fieldbackground=BG2,
                        borderwidth=0, font=FONT_BODY)
        style.configure("Custom.Treeview.Heading",
                        background=BG3, foreground=ACCENT,
                        borderwidth=0, relief="flat", font=FONT_HEADER)
        style.map("Custom.Treeview",
                  background=[("selected", BG3)],
                  foreground=[("selected", ACCENT)])
        style.map("Custom.Treeview.Heading",
                  background=[("active", BORDER)])

        frame_tree = tk.Frame(self, bg=BG)
        frame_tree.pack(fill="both", expand=True, padx=0, pady=0)

        self._tree = ttk.Treeview(frame_tree, columns=cols,
                                  show="headings", style="Custom.Treeview",
                                  selectmode="extended")
        for c in cols:
            self._tree.heading(c, text=col_labels[c],
                               command=lambda _c=c: self._sort_by(_c))
            self._tree.column(c, width=col_widths[c],
                              minwidth=50, anchor="w")

        vsb = ttk.Scrollbar(frame_tree, orient="vertical",
                            command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # alternating row colors
        self._tree.tag_configure("even",    background=BG2)
        self._tree.tag_configure("odd",     background="#191f26")
        self._tree.tag_configure("listen",  foreground=ACCENT2)
        self._tree.tag_configure("estab",   foreground=FG)
        self._tree.tag_configure("closing", foreground=WARNING)

        # ── Bottom action bar ────────────────────────────────────────────────
        bot = tk.Frame(self, bg=BG3, padx=18, pady=10)
        bot.pack(fill="x", side="bottom")

        self._btn_kill = tk.Button(
            bot, text="✕  Finalizar processo(s) selecionado(s)",
            command=self._kill_selected,
            bg=DANGER, fg="white", font=FONT_HEADER,
            relief="flat", padx=14, pady=6,
            cursor="hand2", activebackground="#c9322c", activeforeground="white")
        self._btn_kill.pack(side="left")

        tk.Label(bot,
                 text="Selecione uma ou mais linhas e clique em Finalizar. "
                      "Shift+clique para selecionar múltiplos.",
                 font=FONT_SMALL, bg=BG3, fg=FG2).pack(side="left", padx=14)

        self._lbl_status = tk.Label(bot, text="", font=FONT_SMALL, bg=BG3, fg=FG2)
        self._lbl_status.pack(side="right", padx=12)

        # ── Branding — sempre visível, lado direito ───────────────────────
        tk.Button(
            bot, text="?  Sobre", command=self._show_about,
            bg=BG3, fg=FG2, font=FONT_SMALL,
            relief="flat", padx=8, pady=4,
            cursor="hand2", activebackground=BORDER, activeforeground=FG,
            bd=0).pack(side="right")

        tk.Label(bot,
                 text="by Gabriel Vasconcellos",
                 font=("Consolas", 9, "italic"),
                 bg=BG3, fg=ACCENT,
                 cursor="hand2").pack(side="right", padx=6)

    # ── About ─────────────────────────────────────────────────────────────────

    def _show_about(self):
        win = tk.Toplevel(self)
        win.title("Sobre o Port Monitor")
        win.geometry("420x260")
        win.configure(bg=BG)
        win.resizable(False, False)
        win.grab_set()

        tk.Label(win, text="⬡  PORT MONITOR", font=FONT_TITLE,
                 bg=BG, fg=ACCENT).pack(pady=(28, 4))

        tk.Label(win, text=f"Versão {__version__}", font=FONT_SMALL,
                 bg=BG, fg=FG2).pack()

        tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=30, pady=16)

        tk.Label(win, text="Criado por Gabriel Vasconcellos",
                 font=FONT_BODY, bg=BG, fg=FG).pack()

        link = tk.Label(win, text=__github__,
                        font=FONT_SMALL, bg=BG, fg=ACCENT,
                        cursor="hand2")
        link.pack(pady=4)
        link.bind("<Button-1>", lambda e: self._open_url(__github__))

        tk.Label(win, text=f"Licença {__license__}  •  Python + Tkinter + psutil",
                 font=FONT_SMALL, bg=BG, fg=FG2).pack(pady=(8, 0))

        tk.Button(win, text="Fechar", command=win.destroy,
                  bg=BG3, fg=FG, font=FONT_SMALL,
                  relief="flat", padx=14, pady=5,
                  cursor="hand2", activebackground=BORDER).pack(pady=20)

    @staticmethod
    def _open_url(url: str):
        import webbrowser
        webbrowser.open(url)

    # ── Data ─────────────────────────────────────────────────────────────────

    def _refresh(self):
        self._lbl_status.config(text="Atualizando…", fg=FG2)
        self.update_idletasks()
        rows = get_connections()
        self._all_rows = rows
        self._apply_filter()
        now = datetime.now().strftime("%H:%M:%S")
        self._lbl_time.config(text=f"Última atualização: {now}")
        self._lbl_status.config(text=f"{len(rows)} conexões encontradas", fg=FG2)

    def _apply_filter(self):
        q = self._filter_text.get().lower().strip()
        rows = self._all_rows
        if q:
            rows = [
                r for r in rows
                if q in str(r["porta"])
                or q in r["processo"].lower()
                or q in str(r["pid"])
                or q in r["caminho"].lower()
                or q in r["status"].lower()
                or q in r["protocolo"].lower()
            ]
        self._populate(rows)
        self._lbl_count.config(text=f"{len(rows)} exibidos")

    def _populate(self, rows):
        for item in self._tree.get_children():
            self._tree.delete(item)
        for i, r in enumerate(rows):
            tag_row  = "even" if i % 2 == 0 else "odd"
            status   = r["status"].upper()
            tag_stat = ("listen"  if "LISTEN" in status else
                        "closing" if any(x in status for x in ("CLOSE", "TIME_WAIT", "FIN")) else
                        "estab")
            self._tree.insert("", "end",
                              values=(r["porta"], r["protocolo"], r["status"],
                                      r["pid"] or "—", r["processo"], r["caminho"]),
                              tags=(tag_row, tag_stat))

    # ── Sort ─────────────────────────────────────────────────────────────────

    _sort_asc: dict[str, bool] = {}

    def _sort_by(self, col):
        asc = not self._sort_asc.get(col, True)
        self._sort_asc[col] = asc
        idx = {"porta":0,"protocolo":1,"status":2,"pid":3,"processo":4,"caminho":5}[col]
        items = [(self._tree.set(k, col), k) for k in self._tree.get_children("")]
        try:
            items.sort(key=lambda t: int(t[0]) if t[0].isdigit() else t[0].lower(),
                       reverse=not asc)
        except Exception:
            items.sort(reverse=not asc)
        for pos, (_, k) in enumerate(items):
            self._tree.move(k, "", pos)

    # ── Kill ─────────────────────────────────────────────────────────────────

    def _kill_selected(self):
        selected = self._tree.selection()
        if not selected:
            messagebox.showwarning("Nada selecionado",
                                   "Selecione pelo menos um processo na tabela.")
            return

        pids = set()
        names = []
        for item in selected:
            vals = self._tree.item(item, "values")
            pid_val  = vals[3]
            proc_val = vals[4]
            if pid_val and pid_val != "—":
                pids.add(int(pid_val))
                names.append(f"  • {proc_val} (PID {pid_val})")

        if not pids:
            messagebox.showwarning("Sem PID",
                                   "Os processos selecionados não têm PID disponível.")
            return

        msg = "Deseja finalizar os seguintes processos?\n\n" + "\n".join(names)
        if not messagebox.askyesno("Confirmar", msg, icon="warning"):
            return

        killed, failed = [], []
        for pid in pids:
            try:
                proc = psutil.Process(pid)
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except psutil.TimeoutExpired:
                    proc.kill()
                killed.append(str(pid))
            except psutil.NoSuchProcess:
                killed.append(str(pid))     # já não existia
            except psutil.AccessDenied:
                failed.append(str(pid))
            except Exception as e:
                failed.append(f"{pid} ({e})")

        report = ""
        if killed:
            report += f"✔ Finalizados: PID(s) {', '.join(killed)}\n"
        if failed:
            report += f"✘ Falhou (acesso negado): PID(s) {', '.join(failed)}\n"
            report += "\nDica: execute como Administrador para processos do sistema."

        messagebox.showinfo("Resultado", report.strip())
        self._refresh()

    # ── Auto-refresh ─────────────────────────────────────────────────────────

    def _schedule_auto(self):
        def loop():
            while True:
                time.sleep(5)
                if self._auto_refresh.get():
                    self.after(0, self._refresh)
        t = threading.Thread(target=loop, daemon=True)
        t.start()


if __name__ == "__main__":
    app = PortMonitor()
    app.mainloop()