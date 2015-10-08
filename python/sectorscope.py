#!/usr/bin/env python3
# view block hashes

from argparse import ArgumentParser
import math
import xml.dom.minidom
import os
import json
try:
    import tkinter
except ImportError:
    import Tkinter as tkinter

# local import
from identified_data import IdentifiedData
from menu_view import MenuView
from filters import Filters
from filters_view import FiltersView
from range_selection import RangeSelection
from range_selection_view import RangeSelectionView
from project_summary_view import ProjectSummaryView
from histogram_view import HistogramView
from sources_view import SourcesView
from forensic_path import offset_string
from open_manager import OpenManager
import colors

# compose the GUI
def build_gui(root_window, identified_data, filters, range_selection,
                                                              open_manager):
    """The left frame holds the banner, histogram, and table of selected
    sources.  The right frame holds the table of all sources."""

    # set root window attributes
    START_WIDTH = 1000
    START_HEIGHT = 800
    root_window.title("SectorScope")
    root_window.minsize(width=400,height=300)
    root_window.geometry("1000x700")
    root_window.configure(bg=colors.BACKGROUND)

    # left frame for most of view, top down
    left_frame = tkinter.Frame(root_window, bg=colors.BACKGROUND)
    left_frame.pack(side=tkinter.LEFT, anchor="n", padx=4, pady=(4,0))

    # menu
    menu_view = MenuView(left_frame, open_manager)
    menu_view.frame.pack(side=tkinter.TOP, anchor="w")

    # project summary
    project_summary_view = ProjectSummaryView(
                            left_frame, identified_data)
    project_summary_view.frame.pack(side=tkinter.TOP, anchor="w")


    # filters
    filters_view = FiltersView(left_frame, identified_data, filters,
                                                             range_selection)
    filters_view.frame.pack(side=tkinter.TOP, anchor="w", padx=4, pady=4)

    # the range selection view
    range_selection_view = RangeSelectionView(left_frame, identified_data,
                                                    filters, range_selection)
    range_selection_view.frame.pack(side=tkinter.TOP, anchor="w")

    # the histogram view
    histogram_view = HistogramView(left_frame, identified_data, filters,
                                                             range_selection)
    histogram_view.frame.pack(side=tkinter.TOP, anchor="w")

    # the whole right side for the sources view
    sources_view = SourcesView(root_window, identified_data, filters,
                                                             range_selection)
    sources_view.frame.pack(side=tkinter.LEFT, anchor="n", padx=(4,0))

# main
if __name__=="__main__":

    # parse be_dir from input
    parser = ArgumentParser(prog='sectorscope.py',
               description="View associations between scanned hashes "
                           "and their sources for the bulk_extractor "
                           "directory at path 'be_dir'.")
    parser.add_argument('-i', '--be_dir',
                        help= 'path to the bulk_extractor directory',
                        default='')
    args = parser.parse_args() 

    # initialize Tk
    root_window = tkinter.Tk()

    # the identified data dataset
    identified_data = IdentifiedData()

    # the filters data including the filter_changed trace variable
    filters = Filters()

    # the byte range selection
    range_selection = RangeSelection()

    # the open manager
    open_manager = OpenManager(root_window, identified_data, filters,
                                                            range_selection)

    # build the GUI
    build_gui(root_window, identified_data, filters, range_selection,
                                                               open_manager)

    # now open the be_dir
    open_manager.open_be_dir(args.be_dir)

    # keep Tk alive
    root_window.mainloop()

