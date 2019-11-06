# -*- coding: utf-8 -*-

"""The graphical part of a Forcefield step"""

import seamm
import seamm_widgets as sw
import tkinter as tk


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

    def create_dialog(self):
        """Create the dialog for editing the Forcefield flowchart
        """

        frame = super().create_dialog('Edit Forcefield Step')

        # Create the widgets and grid them in
        P = self.node.parameters
        row = 0
        widgets = []
        for key in P:
            self[key] = P[key].widget(frame)
            self[key].grid(row=row, column=0, sticky=tk.EW)
            row += 1
            widgets.append(self[key])

        sw.align_labels(widgets)
