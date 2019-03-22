import queue
import tkinter as tk

USER_LABEL = 1


class LearningGUI(object):
    def __init__(self, root):
        self.root = root

        root.protocol('WM_DELETE_WINDOW', self.callback_quit)
        root.after(200, self.poll)
        root.minsize(width=20, height=200)

        self.main_container = tk.Frame(root, width=20, height=100)
        self.main_container.pack(side="top", fill="both", expand=True)

        self.top_frame = tk.Frame(self.main_container)
        self.top_frame.pack(side="top", fill="x", expand=False)

        self.number_label = tk.Label(self.top_frame, bg='white')
        self.number_label.grid(row=0, column=0, padx=20, pady=10)

        self.choose_letter = tk.Frame(self.top_frame)
        self.choose_letter.grid(row=1, column=0, padx=20, pady=10)

        self.letter_entry = tk.Entry(self.choose_letter, width=5)
        self.letter_entry.bind("<Return>", self.callback_letter)
        self.letter_entry.grid(row=0, column=1, padx=0, pady=0)

        self.msg_label = tk.Label(self.top_frame, font=("Helvetica", 15), wraplength=20, width=20,
                                  justify=tk.LEFT)
        self.msg_label.grid(row=2, column=0, padx=20, pady=10)

        self.root.resizable(width=tk.FALSE, height=tk.FALSE)

        self.input_queue = queue.Queue()
        self.task_queue = queue.Queue()

    def poll(self):
        while not self.task_queue.empty():
            task = self.task_queue.get()
            task()
        self.root.after(200, self.poll)

    def add_task(self, task):
        self.task_queue.put(task)

    def get_input(self):
        return self.input_queue.get(block=True)

    def update_gui(self, image, msg, title):
        self.number_label.config(image=image)
        self.number_label.image = image

        self.msg_label.config(text=msg, fg='red')

        self.root.title(title)

    def callback_letter(self, _):
        letter = self.letter_entry.get()
        self.input_queue.put((USER_LABEL, letter))
        self.letter_entry.delete(0, 'end')

    def destroy(self):
        self.root.destroy()

    def callback_quit(self):
        self.root.destroy()
