# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Getting Things GNOME! - a personal organizer for the GNOME desktop
# Copyright (c) 2008-2012 - Lionel Dricot & Bertrand Rousseau
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

import gtk

from GTG.backends import BackendFactory


class BackendsCombo(gtk.ComboBoxEntry):
    '''
    A combobox listing all the available backends types
    '''

    COLUMN_NAME = 0  # unique name for the backend type. It's never
                            # displayed, it's used to find which backend has
                            # been selected
    COLUMN_HUMAN_NAME = 1  # human friendly name (which is localized).
    COLUMN_ICON = 2

    def __init__(self, backends_dialog):
        '''
        Constructor, itializes gtk widgets.
        @param backends_dialog: reference to the dialog in which this combo is
                                loaded.
        '''
        super(BackendsCombo, self).__init__()
        self.dialog = backends_dialog
        self._liststore_init()
        self._renderers_init()
        self.set_size_request(-1, 30)
        self.show_all()

    def _liststore_init(self):
        '''Setup the gtk.ListStore'''
        self.liststore = gtk.ListStore(str, str, gtk.gdk.Pixbuf)
        self.set_model(self.liststore)

    def _renderers_init(self):
        '''Configure the cell renderers'''
        # Text renderer
        text_cell = gtk.CellRendererText()
        self.pack_start(text_cell, False)
        self.set_text_column(self.COLUMN_HUMAN_NAME)
        # Icon renderer
        pixbuf_cell = gtk.CellRendererPixbuf()
        self.pack_start(pixbuf_cell, False)
        self.add_attribute(pixbuf_cell, "pixbuf", self.COLUMN_ICON)

    def refresh(self):
        '''
        Populates the combo box with the available backends
        '''
        self.liststore.clear()
        backend_types = BackendFactory().get_all_backends()
        #print "backend_types = " + str(backend_types)
        for name, module in backend_types.iteritems():
            #print "name = " + str(name) + " module = " + str(module)
            # FIXME: Disable adding another localfile backend.
            # It just produce many warnings, provides no use case
            # See LP bug #940917 (Izidor)
            if name == "backend_localfile":
                continue
            pixbuf = self.dialog.get_pixbuf_from_icon_name(name, 16)
            self.liststore.append((name,
                                   module.Backend.get_human_default_name(),
                                   pixbuf))
        if backend_types:
            # triggers a "changed" signal, which is used in the AddPanel to
            # refresh the backend description and icon
            self.set_active(0)

    def get_selected(self):
        '''
        Returns the name of the selected backend, or None
        '''
        selected_iter = self.get_active_iter()
        if selected_iter:
            column_name = BackendsCombo.COLUMN_NAME
            return self.liststore.get_value(selected_iter, column_name)
        else:
            return None
