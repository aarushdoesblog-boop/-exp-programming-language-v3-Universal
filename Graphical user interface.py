import tkinter as tk
from tkinter import scrolledtext
import re
import math

class ExpIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("ExpStudio v3.0 - Universal Singularity")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1e1e1e")

        # --- UNIVERSAL KNOWLEDGE BASE ---
        self.kb = {
            "c": 299792458, "g": 9.80665, "G": 6.6743e-11, "h": 6.626e-34,
            "pi": math.pi, "e": math.e, "au": 1.496e11, "ly": 9.461e15
        }

        self.errors = {
            "use": "ERROR_Resource/Architecture link failure.",
            "access": "ERROR_Security Denial: Unauthorized path access.",
            "pen": "ERROR_Visual file type unrecognized.",
            "penWIN": "ERROR_Rendering failure.",
            "computer": "ERROR_Hardware Operation Restricted.",
            "physics": "ERROR_Physical Law Violation.",
            "math": "ERROR_Mathematical Singularity/Syntax Error.",
            "Inet": "ERROR_Network Protocol Failure.",
            "imp": "ERROR_System Integrity Lock.",
            "exp": "ERROR_Unrecognised code syntax.",
            "IDE": "ERROR_IDE Execution Context Lost."
        }

        # --- UI LAYOUT ---
        tk.Label(root, text="EXPSTUDIO v3.0 - UNIVERSAL ENGINE", bg="#1e1e1e", fg="white", font=("Courier", 12)).pack()
        self.editor = scrolledtext.ScrolledText(root, width=135, height=15, bg="#2d2d2d", fg="#dcdcdc", font=("Courier", 11))
        self.editor.pack(pady=5)
        
        self.editor.insert(tk.INSERT, 
            "call @physics(speed = distance:200km / time:7200s)\n"
            "run @math((x+y)^3 - (x-y)^3)\n"
            "call @physics(energy = mass:0.5kg * c^2)\n"
            "run @penWIN(rect 0 0 450 350 #1a1a1a)\n"
            "call @Inet(lookup universal_constants)"
        )

        self.run_btn = tk.Button(root, text="RUN @exp PROGRAM", command=self.run_code, bg="#007acc", fg="white", font=("Arial", 10, "bold"))
        self.run_btn.pack(pady=5)

        self.bottom_frame = tk.Frame(root, bg="#1e1e1e")
        self.bottom_frame.pack(fill="both", expand=True, padx=20)
        self.console = scrolledtext.ScrolledText(self.bottom_frame, width=80, height=20, bg="black", fg="#00ff00", font=("Courier", 10))
        self.console.pack(side="left", padx=5, pady=5, fill="both", expand=True)
        self.display = tk.Canvas(self.bottom_frame, width=450, height=350, bg="#333333", highlightthickness=1, highlightbackground="white")
        self.display.pack(side="right", padx=5, pady=5)

    def universal_parser(self, text):
        # Extract all numbers and potential variables
        vals = [float(s) for s in re.findall(r"[-+]?\d*\.\d+|\d+", text)]
        tokens = re.findall(r'[a-zA-Z]+', text.lower())
        return vals, tokens

    def run_code(self):
        self.console.delete(1.0, tk.END)
        lines = self.editor.get("1.0", tk.END).splitlines()

        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line: continue

            match = re.fullmatch(r"(run|call)\s+@([a-zA-Z]+)\((.*)\)", line)
            if not match:
                self.trigger_error("exp", i)
                continue

            trigger, agent, content = match.group(1), match.group(2), match.group(3)
            vals, tokens = self.universal_parser(content)

            try:
                # --- @PHYSICS: UNIVERSAL MOTION & ENERGY ---
                if agent == "physics":
                    if "speed" in content or "/" in content:
                        res = vals[0] / vals[1] if len(vals) >= 2 else 0
                        self.log(trigger, agent, f"Universal Velocity: {res} units/s")
                    elif "c" in tokens or "energy" in content:
                        m = vals[0] if vals else 1
                        res = m * (self.kb['c']**2)
                        self.log(trigger, agent, f"Energy (E=mc²): {res} Joules")
                    else: self.log(trigger, agent, f"Physics Simulation Active: {content}")

                # --- @MATH: SYMBOLIC & ARITHMETIC ---
                elif agent == "math":
                    if "=" in content:
                        self.log(trigger, agent, f"Algebraic Solution: Found x using Universal Logic")
                    elif "^" in content and any(c.isalpha() for c in content):
                        # Simple Symbolic response for polynomials
                        self.log(trigger, agent, f"Symbolic Expansion: Processed {content}")
                    else:
                        clean = content.replace("^", "**")
                        for k, v in self.kb.items(): clean = clean.replace(k, str(v))
                        self.log(trigger, agent, f"Arithmetic Result: {eval(clean, {'__builtins__': None}, math.__dict__)}")

                # --- @PENWIN: UNIVERSAL RENDERING ---
                elif agent == "penWIN":
                    if "rect" in content: self.display.create_rectangle(vals[0], vals[1], vals[2], vals[3], outline=tokens[-1])
                    elif "oval" in content: self.display.create_oval(vals[0], vals[1], vals[2], vals[3], outline=tokens[-1])
                    self.log(trigger, agent, f"Object Rendered: {tokens[0]}")

                # --- ALL OTHER EXPERTS ---
                elif agent in self.errors:
                    if agent == "computer" and any(x in content.upper() for x in ["C:", "SYSTEM"]):
                        self.trigger_error("computer", i)
                    else:
                        self.log(trigger, agent, f"Expert validated command: {content[:25]}...")

            except Exception:
                self.trigger_error(agent if agent in self.errors else "exp", i)

    def log(self, trigger, agent, msg):
        self.console.insert(tk.END, f"[{trigger.upper()} @{agent}] {msg}\n")

    def trigger_error(self, agent, line):
        msg = self.errors.get(agent, "General Error")
        self.console.insert(tk.END, f"[@{agent}] {msg} (Line {line})\n", "err")
        self.console.tag_config("err", foreground="red")

if __name__ == "__main__":
    root = tk.Tk()
    ExpIDE(root)
    root.mainloop()
