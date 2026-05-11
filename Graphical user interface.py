import tkinter as tk
from tkinter import scrolledtext
import re
import math

class ExpIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("ExpStudio v3.1 - Universal Singularity")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1e1e1e")

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

        tk.Label(root, text="EXPSTUDIO v3.1 - UNIVERSAL ENGINE", bg="#1e1e1e", fg="white", font=("Courier", 12)).pack()
        self.editor = scrolledtext.ScrolledText(root, width=135, height=15, bg="#2d2d2d", fg="#dcdcdc", font=("Courier", 11))
        self.editor.pack(pady=5)
        
        # Default Hello World
        self.editor.insert(tk.INSERT, 'run @IDE(print "Hello World!")\nrun @physics(speed distance:200km / time:7200s)')

        self.run_btn = tk.Button(root, text="RUN @exp PROGRAM", command=self.run_code, bg="#007acc", fg="white", font=("Arial", 10, "bold"))
        self.run_btn.pack(pady=5)

        self.bottom_frame = tk.Frame(root, bg="#1e1e1e")
        self.bottom_frame.pack(fill="both", expand=True, padx=20)
        self.console = scrolledtext.ScrolledText(self.bottom_frame, width=80, height=20, bg="black", fg="#00ff00", font=("Courier", 10))
        self.console.pack(side="left", padx=5, pady=5, fill="both", expand=True)
        self.display = tk.Canvas(self.bottom_frame, width=450, height=350, bg="#333333", highlightthickness=1, highlightbackground="white")
        self.display.pack(side="right", padx=5, pady=5)

    def log(self, trigger, agent, msg):
        self.console.insert(tk.END, f"[{trigger.upper()} @{agent}] {msg}\n")

    def trigger_error(self, agent, line):
        msg = self.errors.get(agent, "General Error")
        self.console.insert(tk.END, f"[@{agent}] {msg} (Line {line})\n", "err")
        self.console.tag_config("err", foreground="red")

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
            
            try:
                # --- UNIVERSAL AGENT LOGIC ---
                if agent == "IDE":
                    if "print" in content:
                        output_text = re.findall(r"['\"](.*?)['\"]", content)
                        if output_text:
                            self.console.insert(tk.END, f"> {output_text[0]}\n", "print_out")
                            self.console.tag_config("print_out", foreground="white", font=("Courier", 10, "bold"))
                        else: self.log(trigger, agent, content)
                    else: self.log(trigger, agent, content)

                elif agent == "physics":
                    nums = [float(n) for n in re.findall(r"(\d+\.?\d*)", content)]
                    if "/" in content and len(nums) >= 2:
                        self.log(trigger, agent, f"Result: {nums[0]/nums[1]} units/s")
                    else: self.log(trigger, agent, f"Physics Active: {content}")

                elif agent == "math":
                    clean = content.replace("^", "**")
                    for k, v in self.kb.items(): clean = clean.replace(k, str(v))
                    self.log(trigger, agent, f"Result: {eval(clean, {'__builtins__': None}, math.__dict__)}")

                elif agent == "penWIN":
                    vals = [float(n) for n in re.findall(r"(\d+\.?\d*)", content)]
                    colors = re.findall(r'[a-zA-Z#]+', content)
                    self.display.create_rectangle(vals[0], vals[1], vals[2], vals[3], outline=colors[-1])
                    self.log(trigger, agent, "Rendered Object")

                elif agent in self.errors:
                    self.log(trigger, agent, "Command Validated")

            except:
                self.trigger_error(agent, i)

if __name__ == "__main__":
    root = tk.Tk()
    ExpIDE(root)
    root.mainloop()
