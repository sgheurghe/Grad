import os
import tkinter as tk
import threading
import google.generativeai as genai

os.environ["GOOGLE_API_USE_MTLS"] = "never"

AI_API_KEY = "AIzaSyA4WnnJWnvNDRR9rJ1ZPxYi2jFXqHBa1zk"
SYSTEM_INSTRUCTIONS = """
You are the AI Tutorial for the game 2D action-platformer projectile-based (no melees) game 'Blocky Adventures' which is a difficulty scaling game. 
Personality: Witty, summary-focused, and straight to the point.

GAME KNOWLEDGE:
1. DIMENSIONS & TIME:
   - Grasslands: Normal time scale.
   - Underworld: Time is 2x slower (affects projectiles and movement).
   - Inverse: Time is reversed (Controls are REVERSED: A = Right, D = Left).

2. ENEMIES & BOSSES:
   - Grasslands: Crawlers, Stone Golems. BOSS: The Crimson Pulse.
   - Underworld: Husker, Specter. BOSS: Magma Colossus.
   - Inverse: Weaver, Stalker. BOSS: Entropy (The Final Boss).

3. CONTROLS:
   - Press [F] to shoot a Fireball trajectory.
   - Press [E] for a Jump Boost.

RULES:
- If asked about features NOT in this list, say: 'I'm sorry but that kind of stuff is not yet implemented in this game.'
- Stay in character as a technical terminal.
"""

genai.configure(api_key=AI_API_KEY)
model = genai.GenerativeModel(
    model_name='gemini-flash-latest',
    system_instruction=SYSTEM_INSTRUCTIONS
)

def ai_logic_thread(query):
    try:
        response = model.generate_content(query)
        ai_text = response.text
        
        output_box.config(state="normal")
        output_box.insert("end", f"TERMINAL: {ai_text}\n\n")
        output_box.see("end")
    except Exception as e:
        output_box.config(state="normal")
        if "429" in str(e):
            output_box.insert("end", "TERMINAL: [ ERROR ] Chronal Flare detected. Data stream temporarily unstable. Please recalibrate (wait 60s).\n\n")
        else:
            output_box.insert("end", f"SYSTEM ERROR: {e}\n\n")
    
    finally:
        output_box.config(state="disabled")
        send_button.config(text="SEND", state="normal")

def handle_send():
    query = input_bar.get()
    if query:
        output_box.config(state="normal")
        output_box.insert("end", f"USER: {query}\n")
        input_bar.delete(0, "end")
        output_box.config(state="disabled")
        
        send_button.config(text="PROCESSING...", state="disabled")
 
        thread = threading.Thread(target=ai_logic_thread, args=(query,))
        thread.start() 

root = tk.Tk()
root.title("Interdimensional Terminal v1.0")
root.geometry("600x700")
root.configure(bg="#0a0a0a")

output_box = tk.Text(
    root, 
    height=20, 
    width=70, 
    state="disabled", 
    wrap="word",
    bg="#0d0d0d", 
    fg="#00ff41",
    insertbackground="white",
    font=("Courier", 11)
)
output_box.pack(pady=15, padx=15)

# Styling the Input Bar
input_bar = tk.Entry(
    root, 
    width=60, 
    bg="#1a1a1a", 
    fg="white", 
    insertbackground="white",
    font=("Courier", 12)
)
input_bar.pack(pady=10)
input_bar.focus_set()

root.bind('<Return>', lambda event: handle_send())

send_button = tk.Button(
    root, 
    text="SEND", 
    command=handle_send,
    bg="#333333",
    fg="white",
    font=("Courier", 10, "bold"),
    activebackground="#00ff41"
)
send_button.pack(pady=10)

root.mainloop()
