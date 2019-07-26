# -*- coding: utf-8 -*-

"""The graphical part of a Forcefield step"""

import seamm
import forcefield_step
import os.path
import tkinter as tk
import tkinter.filedialog as tk_filedialog
import tkinter.ttk as ttk


class TkForcefield(seamm.TkNode):
    """The node_class is the class of the 'real' node that this
    class is the Tk graphics partner for
    """

    node_class = forcefield_step.Forcefield

    def __init__(
        self,
        tk_flowchart=None,
        node=None,
        canvas=None,
        x=None,
        y=None,
        w=200,
        h=50
    ):
        '''Initialize a node

        Keyword arguments:
        '''

        self.dialog = None

        super().__init__(
            tk_flowchart=tk_flowchart,
            node=node,
            canvas=canvas,
            x=x,
            y=y,
            w=w,
            h=h
        )

    def create_dialog(self):
        """Create the dialog!"""

        self.dialog = tk.Toplevel(master=self.toplevel)
        self.dialog.transient(self.toplevel)
        self.dialog.withdraw()
        self.dialog.title('Forcefield...')

        frame = ttk.Frame(self.dialog)
        frame.pack(side='top', fill=tk.BOTH, expand=1)

        ff_file_label = ttk.Label(frame, text='Forcefield:')
        self.ff_file_widget = ttk.Entry(frame, width=30)
        self.ff_file_widget.insert(0, self.node.ff_file)
        ff_file_button = ttk.Button(frame, text='...', command=self.ff_file_cb)
        ff_file_label.grid(row=0, column=0)
        self.ff_file_widget.grid(row=0, column=1)
        ff_file_button.grid(row=0, column=2)

        button_box = ttk.Frame(self.dialog)
        button_box.pack(side='bottom', expand=1, fill=tk.X)
        ok_button = ttk.Button(button_box, text="OK", command=self.handle_ok)
        ok_button.grid(row=0, column=0, sticky=tk.W)
        help_button = ttk.Button(
            button_box, text="Help", command=self.handle_help
        )
        help_button.grid(row=0, column=1)
        cancel_button = ttk.Button(
            button_box, text="Cancel", command=self.handle_cancel
        )
        cancel_button.grid(row=0, column=2, sticky=tk.E)
        button_box.grid_columnconfigure(0, weight=1)
        button_box.grid_columnconfigure(1, weight=1)
        button_box.grid_columnconfigure(2, weight=1)

    def ff_file_cb(self):
        """Present the file dialog for getting the forcefield"""
        name = tk_filedialog.askopenfilename(
            parent=self.dialog,
            filetypes=[('all files', '.*'), ('forcefield files', '.frc')],
            initialdir=os.path.dirname(self.node.ff_file)
        )
        if name != '':
            self.ff_file_widget.delete(0, tk.END)
            self.ff_file_widget.insert(0, name)

    def right_click(self, event):
        """Probably need to add our dialog...
        """

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def edit(self):
        """Present a dialog for editing the Forcefield flowchart
        """

        if not self.dialog:
            self.create_dialog()

        self._tmp = {'dialog': self.dialog}
        self.previous_grab = self.dialog.grab_current()
        self.dialog.grab_set()
        self.dialog.deiconify()
        self.dialog.attributes('-topmost', True)

    def handle_ok(self):
        self.dialog.grab_release()
        self.dialog.attributes('-topmost', False)
        self.dialog.withdraw()
        if self.previous_grab is not None:
            self.previous_grab().grab_set()
            self.previous_grab = None
        self.node.ff_file = self.ff_file_widget.get()

    def handle_help(self):
        print('Help')
        self.dialog.grab_release()
        self.dialog.attributes('-topmost', False)
        self.dialog.withdraw()
        if self.previous_grab is not None:
            self.previous_grab().grab_set()
            self.previous_grab = None

    def handle_cancel(self):
        self.dialog.grab_release()
        self.dialog.attributes('-topmost', False)
        self.dialog.withdraw()
        if self.previous_grab is not None:
            self.previous_grab().grab_set()
            self.previous_grab = None
