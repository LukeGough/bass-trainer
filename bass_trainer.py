import tkinter as tk
import random
import numpy as np
import sounddevice as sd

# -----------------------------
# Bass Data
# -----------------------------
bass_frequencies = {4:41.20,3:55.00,2:73.42,1:98.00}
bass_strings = {1:"G",2:"D",3:"A",4:"E"}
notes_sharps = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
notes_flats  = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]

# -----------------------------
# Trainer Class
# -----------------------------
class BassNoteTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("🎸 Bass Note Trainer")
        self.allowed_strings = [1,2,3,4]
        self.max_fret = 12
        self.note_style = "both"
        self.quiz_type = None  # 'bass_note' or 'note_order'
        self.total_attempts = 0
        self.correct_attempts = 0

        self.setup_settings()
        self.setup_quiz_area()

    # -----------------------------
    # Settings GUI
    # -----------------------------
    def setup_settings(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        # Strings
        tk.Label(frame,text="Strings:").grid(row=0,column=0)
        self.string_vars={}
        for i in range(1,5):
            var = tk.IntVar(value=1)
            tk.Checkbutton(frame,text=f"{i} ({bass_strings[i]})",variable=var).grid(row=0,column=i)
            self.string_vars[i]=var

        # Max fret
        tk.Label(frame,text="Max Fret:").grid(row=1,column=0)
        self.fret_entry = tk.Entry(frame,width=5)
        self.fret_entry.insert(0,"12")
        self.fret_entry.grid(row=1,column=1)

        # Note style
        tk.Label(frame,text="Note Style:").grid(row=1,column=2)
        self.note_style_var = tk.StringVar(value="both")
        tk.OptionMenu(frame,self.note_style_var,"sharp","flat","both").grid(row=1,column=3)

        # Apply
        tk.Button(frame,text="Apply Settings",command=self.apply_settings).grid(row=1,column=4)

        # Fretboard chart
        tk.Button(frame,text="Show Notes Chart",command=self.show_notes_chart).grid(row=1,column=5,padx=5)

        # Quiz type selection
        tk.Button(frame, text="Bass Note Quiz", command=lambda: self.start_quiz("bass_note")).grid(row=1, column=6)
        tk.Button(frame, text="Note Order Quiz", command=lambda: self.start_quiz("note_order")).grid(row=1, column=7)

    def apply_settings(self):
        self.allowed_strings=[s for s,v in self.string_vars.items() if v.get()==1]
        try:
            self.max_fret=max(0,min(20,int(self.fret_entry.get())))
        except:
            self.max_fret=12
        self.note_style=self.note_style_var.get()

    # -----------------------------
    # Start quiz
    # -----------------------------
    def start_quiz(self, quiz_type):
        self.quiz_type = quiz_type
        self.total_attempts = 0
        self.correct_attempts = 0
        self.score_label.config(text="Score: 0/0 (0%)")
        self.feedback_label.config(text="")
        self.next_question()

    # -----------------------------
    # Quiz GUI
    # -----------------------------
    def setup_quiz_area(self):
        frame=tk.Frame(self.root)
        frame.pack(pady=10)

        self.question_label=tk.Label(frame,text="",font=("Arial",16))
        self.question_label.pack()

        self.answer_entry=tk.Entry(frame,font=("Arial",14))
        self.answer_entry.pack(pady=5)
        self.answer_entry.bind("<Return>", lambda e:self.check_answer())

        tk.Button(frame,text="Submit",command=self.check_answer).pack()

        self.feedback_label=tk.Label(frame,text="",font=("Arial",12))
        self.feedback_label.pack(pady=5)

        self.score_label=tk.Label(frame,text="Score: 0/0 (0%)",font=("Arial",12))
        self.score_label.pack()

    # -----------------------------
    # Note helpers
    # -----------------------------
    def _sharp_flat_for(self,open_note,fret):
        idx = (notes_sharps.index(open_note)+fret)%12
        return notes_sharps[idx], notes_flats[idx]

    def get_note_for_style(self,open_note,fret):
        sharp,flat=self._sharp_flat_for(open_note,fret)
        if self.note_style=="sharp": return sharp
        if self.note_style=="flat": return flat
        return sharp if sharp==flat else f"{sharp}\n{flat}"

    def get_frequency_from_fret(self,string_num,fret):
        return bass_frequencies[string_num]*(2**(fret/12))

    def play_note_sound(self,freq,duration=1.0):
        sample_rate=44100
        t=np.linspace(0,duration,int(sample_rate*duration),endpoint=False)
        waveform=0.3*np.sin(2*np.pi*freq*t)
        sd.play(waveform,sample_rate)
        sd.wait()

    # -----------------------------
    # Note Order helpers
    # -----------------------------
    def get_notes_list(self):
        # Always use sharps for sequencing
        return notes_sharps

    def get_next_note(self,note):
        notes=self.get_notes_list()
        return notes[(notes.index(note)+1)%12]

    def get_previous_note(self,note):
        notes=self.get_notes_list()
        return notes[(notes.index(note)-1)%12]

    # -----------------------------
    # Question generators
    # -----------------------------
    def next_question(self):
        if self.quiz_type=="bass_note":
            if not self.allowed_strings:
                self.question_label.config(text="⚠ No strings selected!")
                return
            self.current_string = random.choice(self.allowed_strings)
            self.current_fret = random.randint(0,self.max_fret)
            sharp, flat = self._sharp_flat_for(bass_strings[self.current_string],self.current_fret)
            self.correct_note_sharp = sharp
            self.correct_note_flat = flat
            self.question_label.config(text=f"String {self.current_string} ({bass_strings[self.current_string]}), Fret {self.current_fret}")
            # Play note only for Bass Note Quiz
            freq = self.get_frequency_from_fret(self.current_string,self.current_fret)
            self.play_note_sound(freq)
        else:  # Note Order Quiz
            self.current_note = random.choice(self.get_notes_list())
            self.direction = random.choice(["next","previous"])
            if self.direction=="next":
                self.correct_note=self.get_next_note(self.current_note)
                self.question_label.config(text=f"What is the {self.direction.upper()} note after {self.current_note}?")
            else:
                self.correct_note=self.get_previous_note(self.current_note)
                self.question_label.config(text=f"What is the {self.direction.upper()} note before {self.current_note}?")
        self.answer_entry.delete(0,tk.END)
        self.feedback_label.config(text="")

    # -----------------------------
    # Answer checking
    # -----------------------------
    def check_answer(self):
        ans=self.answer_entry.get().strip().capitalize()
        self.total_attempts += 1
        correct = False

        if self.quiz_type=="bass_note":
            if self.note_style=="both":
                if ans in [self.correct_note_sharp,self.correct_note_flat]:
                    correct = True
            else:
                correct_note = self.correct_note_sharp if self.note_style=="sharp" else self.correct_note_flat
                if ans == correct_note:
                    correct = True
        else:  # Note Order Quiz
            # Accept enharmonic equivalents if note_style=="both"
            idx = notes_sharps.index(self.correct_note)
            valid_answers = [notes_sharps[idx]]
            if self.note_style=="both":
                valid_answers.append(notes_flats[idx])
            if ans in valid_answers:
                correct = True

        if correct:
            self.correct_attempts += 1
            self.feedback_label.config(text="✅ Correct!", fg="green")
        else:
            if self.quiz_type=="bass_note":
                text=self.correct_note_sharp if self.note_style=="sharp" else self.correct_note_flat
                if self.note_style=="both":
                    text=f"{self.correct_note_sharp} / {self.correct_note_flat}"
            else:
                text=self.correct_note
                if self.note_style=="both":
                    idx = notes_sharps.index(self.correct_note)
                    text=f"{notes_sharps[idx]} / {notes_flats[idx]}"
            self.feedback_label.config(text=f"❌ Nope! {text}", fg="red")

        accuracy = (self.correct_attempts/self.total_attempts)*100 if self.total_attempts>0 else 0
        self.score_label.config(text=f"Score: {self.correct_attempts}/{self.total_attempts} ({accuracy:.1f}%)")

        self.root.after(1000,self.next_question)

    # -----------------------------
    # Graphical Notes Chart
    # -----------------------------
    def show_notes_chart(self):
        frets=list(range(0,13))
        strings_order=[1,2,3,4]
        cell_w,cell_h=70,48
        left_label_w=60
        top_label_h=30
        width=left_label_w+len(frets)*cell_w+1
        height=top_label_h+len(strings_order)*cell_h+1

        win=tk.Toplevel(self.root)
        win.title("Bass Fretboard Chart (0–12)")

        container=tk.Frame(win)
        container.pack(fill="both",expand=True)
        canvas=tk.Canvas(container,width=min(width,900),height=min(height+10,400))
        hbar=tk.Scrollbar(container,orient="horizontal",command=canvas.xview)
        vbar=tk.Scrollbar(container,orient="vertical",command=canvas.yview)
        canvas.configure(xscrollcommand=hbar.set,yscrollcommand=vbar.set)
        hbar.pack(side="bottom",fill="x")
        vbar.pack(side="right",fill="y")
        canvas.pack(side="left",fill="both",expand=True)

        inner=tk.Frame(canvas,bg="#ffffff")
        canvas.create_window((0,0),window=inner,anchor="nw")

        # Header
        header=tk.Canvas(inner,width=width,height=top_label_h,highlightthickness=0,bg="#ffffff")
        header.grid(row=0,column=0,sticky="w")
        for i,f in enumerate(frets):
            x0=left_label_w+i*cell_w
            header.create_text(x0+cell_w/2,top_label_h/2,text=str(f),font=("Arial",10,"bold"))

        # Strings grid
        for r,s in enumerate(strings_order,start=1):
            row_canvas=tk.Canvas(inner,width=width,height=cell_h,highlightthickness=0,bg="#ffffff")
            row_canvas.grid(row=r,column=0,sticky="w")
            row_canvas.create_rectangle(0,0,left_label_w,cell_h,fill="#f5f5f5",outline="#dddddd")
            row_canvas.create_text(left_label_w/2,cell_h/2,text=f"{bass_strings[s]} string",font=("Arial",10,"bold"))
            for i,f in enumerate(frets):
                x0=left_label_w+i*cell_w
                x1=x0+cell_w
                row_canvas.create_rectangle(x0,0,x1,cell_h,fill="#ffffff" if f!=12 else "#eef7ff",outline="#dddddd")
                text=self.get_note_for_style(bass_strings[s],f)
                row_canvas.create_text((x0+x1)/2,cell_h/2,text=text,font=("Arial",10),justify="center")

        # Fret markers
        marker_row=tk.Canvas(inner,width=width,height=24,highlightthickness=0,bg="#ffffff")
        marker_row.grid(row=len(strings_order)+1,column=0,sticky="w",pady=(6,0))
        markers=[3,5,7,9,12]
        for f in markers:
            x0=left_label_w+f*cell_w
            cx=x0+cell_w/2
            cy=12
            radius=4 if f!=12 else 6
            marker_row.create_oval(cx-radius,cy-radius,cx+radius,cy+radius,fill="#888888",outline="")
        inner.update_idletasks()
        canvas.configure(scrollregion=(0,0,width,inner.winfo_height()))

# -----------------------------
# Run
# -----------------------------
if __name__=="__main__":
    root=tk.Tk()
    app=BassNoteTrainer(root)
    root.mainloop()
