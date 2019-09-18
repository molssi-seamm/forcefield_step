# -*- coding: utf-8 -*-

"""The graphical part of a Forcefield step"""

import seamm
import seamm_widgets as sw
import Pmw
import tkinter as tk
import tkinter.ttk as ttk


class TkForcefield(seamm.TkNode):
    """The graphical part of a forcefield step
    """

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

    def right_click(self, event):
        """Probably need to add our dialog...
        """

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def edit(self):
        """Present a dialog for editing the Forcefield flowchart
        """

        self.dialog = Pmw.Dialog(
            self.toplevel,
            buttons=('OK', 'Help', 'Cancel'),
            defaultbutton='OK',
            master=self.toplevel,
            title='Edit Forcefield parameters',
            command=self.handle_dialog
        )
        self.dialog.withdraw()

        frame = ttk.Frame(self.dialog.interior())
        frame.pack(expand=tk.YES, fill=tk.BOTH)
        self['frame'] = frame

        # Create the widgets and grid them in
        P = self.node.parameters
        row = 0
        widgets = []
        for key in P:
            self[key] = P[key].widget(frame)
            widgets.append(self[key])
            self[key].grid(row=row, column=0, sticky=tk.EW)
            row += 1

        sw.align_labels(widgets)

        self.dialog.activate(geometry='centerscreenfirst')

    def handle_dialog(self, result):

        if result is None or result == 'Cancel':
            self.dialog.deactivate(result)
            return

        if result == 'Help':
            # display help!!!
            return

        if result != "OK":
            self.dialog.deactivate(result)
            raise RuntimeError(
                "Don't recognize dialog result '{}'".format(result)
            )

        self.dialog.deactivate(result)

        # Shortcut for parameters
        P = self.node.parameters

        for key in P:
            P[key].set_from_widget()
