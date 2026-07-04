import tkinter as tk
from tkinter import scrolledtext
import threading
import ollama
import time

# ---------------- AI FUNCTION ----------------

def generate_story(topic):
    prompt = f"""
You are a professional story writer.
Write a 1000–1500 word emotional story.
Theme: {topic}
Rules:
- Strictly follow theme
- Simple English
- Strong emotions
- Movie style storytelling
- Beginning, problem, struggle, climax, ending
"""
    try:
        # Puthu light-weight model use panrom
        response = ollama.generate(
            model='llama3.2:1b',
            prompt=prompt
        )
        return response['response']
    except Exception as e:
        return f"Error occurred: {e}\n\nOllama background-la run aaguthannu check pannikonga!"


# ---------------- UI & ANIMATION LOGIC ----------------

def animate_loading(stop_event):
    """Story generate aagumpothu loading text animation kaata"""
    loading_symbols = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    i = 0
    while not stop_event.is_set():
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, f"🌌 {loading_symbols[i]} AI is thinking deep into the universe... Please wait 🔥\n")
        output_box.update()
        time.sleep(0.1)
        i = (i + 1) % len(loading_symbols)

def type_text(text):
    """ChatGPT style text typing effect"""
    output_box.delete(1.0, tk.END)
    for char in text:
        output_box.insert(tk.END, char)
        output_box.update()
        output_box.see(tk.END) # Auto-scroll down
        time.sleep(0.01) # Ultra smooth speed

def start_generation():
    topic = entry.get()
    if not topic.strip():
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, "⚠️ Please enter a story topic first!")
        return

    # Button-ah temporarily disable panna multiple clicks thavirka
    btn.config(state=tk.DISABLED, text="Generating... ⏳")

    stop_animation = threading.Event()
    
    # Background animation thread start panrom
    threading.Thread(target=animate_loading, args=(stop_animation,)).start()

    def task():
        story = generate_story(topic)
        stop_animation.set() # Animation-ah niruthu
        time.sleep(0.2)
        type_text(story) # Story-ah type pannu
        btn.config(state=tk.NORMAL, text="Generate Story 🚀") # Button restore

    # Main AI task thread
    threading.Thread(target=task).start()


# ---------------- MODERN UI DESIGN ----------------

window = tk.Tk()
window.title("🌌 PREMIUM AI STORY GENERATOR")
window.geometry("950x750")
window.configure(bg="#0d1117") # Deep Cyberpunk Dark Blue/Black

# Title Style
title = tk.Label(
    window,
    text="🌌 AI STORY GENERATOR",
    font=("Segoe UI", 24, "bold"),
    fg="#00f2fe", # Neon Cyan
    bg="#0d1117"
)
title.pack(pady=15)

subtitle = tk.Label(
    window,
    text="Enter your theme and watch the AI weave magic",
    font=("Segoe UI", 10, "italic"),
    fg="#8b949e",
    bg="#0d1117"
)
subtitle.pack(pady=2)

# Input Label
lbl = tk.Label(window, text="Story Topic / Theme:", font=("Segoe UI", 12), fg="white", bg="#0d1117")
lbl.pack(pady=5)

# Modern Styled Entry Box
entry = tk.Entry(
    window, 
    font=("Segoe UI", 14), 
    width=55, 
    bg="#161b22", 
    fg="white", 
    insertbackground="white", # Cursor color
    bd=2, 
    relief=tk.FLAT
)
entry.pack(pady=5, ipady=5)
entry.focus()

# Modern Gradient Accent Button
btn = tk.Button(
    window,
    text="Generate Story 🚀",
    font=("Segoe UI", 14, "bold"),
    bg="#00f2fe", 
    fg="#0d1117",
    activebackground="#4facfe",
    activeforeground="white",
    bd=0,
    cursor="hand2",
    padx=20,
    pady=5,
    command=start_generation
)
btn.pack(pady=20)

# Output Box (Premium ChatGPT/VS Code style)
output_box = scrolledtext.ScrolledText(
    window,
    width=100,
    height=25,
    bg="#090d16", # Darker black-blue for contrast
    fg="#e6edf3", # Soft white easy for eyes
    insertbackground="white",
    font=("Consolas", 12), # Clean programming style font
    bd=0,
    padx=15,
    pady=15,
    wrap=tk.WORD
)
output_box.pack(pady=10, fill=tk.BOTH, expand=True, padx=30)

# Footer
footer = tk.Label(window, text="Powered by Ollama (Llama 3.2 1B)", font=("Segoe UI", 9), fg="#58a6ff", bg="#0d1117")
footer.pack(pady=10)

window.mainloop()