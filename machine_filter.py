import os
import re
from tkinter import filedialog, messagebox, Tk

def filter_gcode(file):
    lines = file.splitlines()
    output = []
    has_T0 = any("T0" in line for line in lines)
    has_G54 = any("G54" in line for line in lines)

    for line in lines:
        line = line.strip()

        if any(cmd in line for cmd in ['M3', 'M106', 'M104', 'M109', 'M140', 'M190', 'M141', 'M191', 'M980']):
            continue

        if re.match(r'^G1 X[\d\.\-]+ Y[\d\.\-]+', line):
            line = re.sub(r'F[\d]+', '', line)
            line += ' F20000'

        if re.match(r'^G1 Z[\d\.\-]+', line):
            line = re.sub(r'F[\d]+', '', line)
            line += ' F6000'

        line = re.sub(r'(E[\d]+\.\d{3})\d*', r'\1', line)

        output.append(line)

    if not has_T0:
        output.insert(0, 'T0')
    if not has_G54:
        output.insert(1, 'G54')

    return "\n".join(output)

def main():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select G-code file", filetypes=[("G-code files", "*.gcode")])
    if not file_path:
        return

    with open(file_path, 'r') as file:
        original = file.read()

    filtered = filter_gcode(original)

    out_dir = os.path.join(os.path.dirname(file_path), "filtered_file")
    os.makedirs(out_dir, exist_ok=True)
    filename = os.path.basename(file_path)
    out_path = os.path.join(out_dir, f"filtered_{filename}")

    with open(out_path, 'w') as file:
        file.write(filtered)

    messagebox.showinfo("Complete", f"Filtered G-code saved at:\n{out_path}")

if __name__ == "__main__":
    main()
