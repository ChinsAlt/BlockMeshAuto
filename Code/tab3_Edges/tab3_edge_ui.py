
import tkinter as tk
from tkinter import ttk


class EdgeEditorUI:
    """Professional UI for edge editor matching tab2 style"""

    def __init__(self, parent, colors, callbacks):
        self.parent = parent
        self.colors = colors
        self.callbacks = callbacks

        # UI element references
        self.notebook = None
        self.tab_create = None
        self.tab_manage = None
        self.tab_edit = None
        self.info_label = None
        self.status_label = None
        self.edge_listbox = None
        self.edge_details = None
        self.spline_listbox = None
        self.arc_config = None
        self.spline_config = None
        self.config_frame = None
        self.edit_type_label = None
        self.edit_start_var = None
        self.edit_end_var = None
        self.edit_info_label = None
        self.edit_intermediate_listbox = None
        self.edit_intermediate_frame = None
        self.manual_coords = None
        self.arc_notebook = None
        self.radius_var = None
        self.side_var = None

        # Arc point selection variables
        self.arc_point_var = None
        self.arc_point_label = None
        self.arc_manual_point_var = None
        self.arc_center_var = None
        self.arc_center_label = None
        self.arc_manual_center_var = None

    def setup_main_ui(self):
        """Setup main UI with tab2-style layout - single line title, status at bottom left"""
        # Main container with padding
        main_container = tk.Frame(self.parent, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header - SINGLE LINE TITLE like tab2
        header = tk.Frame(main_container, bg=self.colors['bg'])
        header.pack(fill=tk.X, pady=(0, 10))

        # Single line title "Edge Editor" like tab2's "2D View"
        tk.Label(header, text="Edge Editor", font=("Arial", 16, "bold"),
                bg=self.colors['bg'], fg=self.colors['accent']).pack(side=tk.LEFT)

        # Content area - split into viewer (left) and controls (right)
        content = tk.Frame(main_container, bg=self.colors['bg'])
        content.pack(fill=tk.BOTH, expand=True)

        # Left side - 3D Viewer (expands to fill space)
        viewer_container = tk.Frame(content, bg=self.colors['secondary'])
        viewer_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Viewer frame (actual canvas goes here)
        viewer_frame = tk.Frame(viewer_container, bg=self.colors['canvas_bg'],
                               highlightbackground=self.colors['border'],
                               highlightthickness=1)
        viewer_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Right side - Controls (fixed width to allow viewer to stretch horizontally)
        controls_container = tk.Frame(content, bg=self.colors['secondary'], width=350)
        controls_container.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        controls_container.pack_propagate(False)

        # Create styled notebook
        style = ttk.Style()
        style.theme_use('default')

        # Configure notebook style
        style.configure("Edge.TNotebook", 
                       background=self.colors['secondary'],
                       borderwidth=0)
        style.configure("Edge.TNotebook.Tab",
                       background=self.colors['secondary'],
                       foreground=self.colors['fg'],
                       padding=[15, 8],
                       font=("Segoe UI", 9, "bold"))
        style.map("Edge.TNotebook.Tab",
                 background=[("selected", self.colors['accent']),
                           ("active", self.colors['button_active'])],
                 foreground=[("selected", "white"),
                           ("active", "white")])

        self.notebook = ttk.Notebook(controls_container, style="Edge.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create tabs
        self.tab_create = tk.Frame(self.notebook, bg=self.colors['secondary'])
        self.tab_manage = tk.Frame(self.notebook, bg=self.colors['secondary'])
        self.tab_edit = tk.Frame(self.notebook, bg=self.colors['secondary'])

        self.notebook.add(self.tab_create, text="  Create  ")
        self.notebook.add(self.tab_manage, text="  Manage  ")
        self.notebook.add(self.tab_edit, text="  Edit  ")

        # Status at bottom left (like tab2)
        self.info_label = tk.Label(viewer_container, 
                                  text="Select start point",
                                  font=("Consolas", 9),
                                  bg=self.colors['secondary'], 
                                  fg=self.colors['success'],
                                  anchor=tk.W)
        self.info_label.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=2)

        return viewer_frame, controls_container

    def _create_section_frame(self, parent, title):
        """Create a styled section frame with WHITE BORDER through text (tab2 style)"""
        frame = tk.LabelFrame(parent, text=title,
                             bg=self.colors['secondary'],
                             fg=self.colors['fg'],
                             font=("Arial", 10, "bold"),
                             relief=tk.FLAT,
                             bd=1,
                             highlightbackground='white',  # WHITE BORDER
                             highlightthickness=1,
                             highlightcolor='white')
        frame.pack(fill=tk.X, padx=8, pady=5)

        # Inner padding frame
        inner = tk.Frame(frame, bg=self.colors['secondary'])
        inner.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        return inner

    def _create_button(self, parent, text, command, color_key='button_bg', 
                      width=None, small=False):
        """Create a styled button"""
        height = 1 if small else 1
        padx = 8 if small else 15
        pady = 2 if small else 5

        btn = tk.Button(parent, text=text, command=command,
                       bg=self.colors[color_key],
                       fg=self.colors['button_fg'],
                       font=("Arial", 8 if small else 9, "bold"),
                       relief=tk.FLAT,
                       cursor='hand2',
                       width=width,
                       padx=padx,
                       pady=pady)
        btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Hover effects
        def on_enter(e, btn=btn, key=color_key):
            btn.config(bg=self.colors.get(key + '_active', self.colors[key]))
        def on_leave(e, btn=btn, key=color_key):
            btn.config(bg=self.colors[key])

        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)

        return btn

    def _create_scrollable_canvas(self, parent):
        """Create scrollable canvas with BLACK/DARK scrollbar (tab2 style)"""
        # Create canvas
        canvas = tk.Canvas(parent, bg=self.colors['secondary'], 
                          highlightthickness=0)

        # Create BLACK scrollbar like tab2
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)

        # Style the scrollbar - BLACK/DARK theme like tab2
        scrollbar.config(
            bg=self.colors['secondary'],  # Dark background
            troughcolor=self.colors['bg'],  # Darker trough
            activebackground=self.colors['accent'],  # Accent color when active
            highlightbackground=self.colors['border'],
            highlightthickness=0
        )

        scrollable_frame = tk.Frame(canvas, bg=self.colors['secondary'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Mousewheel binding function
        def on_mousewheel(event):
            if event.num == 4 or event.delta > 0:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                canvas.yview_scroll(1, "units")
            return "break"

        # Bind mousewheel to all widgets recursively
        def bind_mousewheel_to_all(widget):
            widget.bind("<MouseWheel>", on_mousewheel)
            widget.bind("<Button-4>", on_mousewheel)
            widget.bind("<Button-5>", on_mousewheel)
            for child in widget.winfo_children():
                bind_mousewheel_to_all(child)

        bind_mousewheel_to_all(scrollable_frame)
        canvas.bind("<MouseWheel>", on_mousewheel)
        canvas.bind("<Button-4>", on_mousewheel)
        canvas.bind("<Button-5>", on_mousewheel)

        return canvas, scrollbar, scrollable_frame

    def setup_create_tab(self, current_edge_type_var, manual_coords):
        """Setup the Create Edge tab with clean layout"""
        self.manual_coords = manual_coords

        # Use scrollable canvas with black scrollbar
        canvas, scrollbar, scrollable_frame = self._create_scrollable_canvas(self.tab_create)

        # Edge Type Section - WHITE BORDER
        type_frame = self._create_section_frame(scrollable_frame, "Edge Type")

        edge_types = [
            ('arc', 'Arc', 'Curved edge through 3 points'),
            ('spline', 'Spline', 'Smooth curve through multiple points'),
            ('polyLine', 'PolyLine', 'Straight segments between points'),
            ('line', 'Line', 'Straight line (default)')
        ]

        for i, (val, name, desc) in enumerate(edge_types):
            row = tk.Frame(type_frame, bg=self.colors['secondary'])
            row.pack(fill=tk.X, pady=3)

            rb = tk.Radiobutton(row, variable=current_edge_type_var, value=val,
                               command=self.callbacks.get('on_edge_type_changed'),
                               bg=self.colors['secondary'],
                               fg=self.colors['accent'],
                               selectcolor=self.colors['bg'],
                               activebackground=self.colors['secondary'],
                               font=("Arial", 9, "bold"))
            rb.pack(side=tk.LEFT)

            tk.Label(row, text=name, font=("Arial", 9, "bold"),
                    bg=self.colors['secondary'], fg=self.colors['fg']).pack(side=tk.LEFT, padx=(5, 0))

            tk.Label(row, text=desc, font=("Arial", 8),
                    bg=self.colors['secondary'], fg='#888888').pack(side=tk.LEFT, padx=(10, 0))

        # Configuration Section (dynamic based on edge type) - WHITE BORDER
        self.config_frame = self._create_section_frame(scrollable_frame, "Configuration")

        # Arc Configuration
        self.arc_config = tk.Frame(self.config_frame, bg=self.colors['secondary'])

        # Instructions
        inst_frame = tk.Frame(self.arc_config, bg=self.colors['secondary'])
        inst_frame.pack(fill=tk.X, pady=5)

        instructions = [
            ("1. Start point", self.colors['success']),
            ("2. End point", self.colors['error']),
            ("3. Mid point on arc", self.colors['warning'])
        ]

        for text, color in instructions:
            tk.Label(inst_frame, text="● " + text, font=("Arial", 9),
                    bg=self.colors['secondary'], fg=color).pack(anchor=tk.W, pady=1)

        # Arc Helper Tabs - WHITE BORDER
        helper_frame = tk.LabelFrame(self.arc_config, text="Arc Helper",
                                    bg=self.colors['secondary'],
                                    fg=self.colors['fg'],
                                    font=("Arial", 9, "bold"),
                                    relief=tk.FLAT, bd=1,
                                    highlightbackground='white',  # WHITE BORDER
                                    highlightthickness=1,
                                    highlightcolor='white')
        helper_frame.pack(fill=tk.X, pady=10)

        self.arc_notebook = ttk.Notebook(helper_frame, style="Edge.TNotebook")
        self.arc_notebook.pack(fill=tk.X, padx=5, pady=5)

        # Point on Arc tab
        tab1 = tk.Frame(self.arc_notebook, bg=self.colors['secondary'])
        self.arc_notebook.add(tab1, text="Point")

        # Point selection frame
        point_sel_frame = tk.Frame(tab1, bg=self.colors['secondary'])
        point_sel_frame.pack(fill=tk.X, pady=10, padx=5)

        self.arc_point_var = tk.StringVar(value="None selected")
        tk.Label(point_sel_frame, text="Selected Point:", 
                bg=self.colors['secondary'], fg=self.colors['fg'],
                font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.arc_point_label = tk.Label(point_sel_frame, textvariable=self.arc_point_var,
                                       bg=self.colors['secondary'], fg=self.colors['accent'],
                                       font=("Consolas", 10, "bold"))
        self.arc_point_label.pack(anchor=tk.W, pady=(2, 5))

        btn_row = tk.Frame(point_sel_frame, bg=self.colors['secondary'])
        btn_row.pack(fill=tk.X, pady=5)

        self._create_button(btn_row, "🎯 Choose Point", 
                           self.callbacks.get('choose_arc_point', lambda: None),
                           'accent', width=12)
        self._create_button(btn_row, "✓ Use This Point", 
                           self.callbacks.get('use_chosen_arc_point', lambda: None),
                           'success', width=12)

        # Manual entry row
        manual_row = tk.Frame(point_sel_frame, bg=self.colors['secondary'])
        manual_row.pack(fill=tk.X, pady=10)

        tk.Label(manual_row, text="Or enter Point ID:", 
                bg=self.colors['secondary'], fg=self.colors['fg'],
                font=("Arial", 9)).pack(side=tk.LEFT)

        self.arc_manual_point_var = tk.StringVar()
        tk.Entry(manual_row, textvariable=self.arc_manual_point_var, width=8,
                bg=self.colors['text_bg'], fg=self.colors['text_fg'],
                font=("Consolas", 9), relief=tk.FLAT,
                highlightbackground=self.colors['border'],
                highlightthickness=1).pack(side=tk.LEFT, padx=5)

        self._create_button(manual_row, "Set",
                           self.callbacks.get('set_arc_point_manual', lambda: None),
                           'button_bg', small=True)

        tk.Label(tab1, text="Click 'Choose Point' then click a point in 3D view", 
                bg=self.colors['secondary'], fg='#888888',
                font=("Arial", 8), wraplength=300).pack(pady=5)

        # Center Point tab
        tab2 = tk.Frame(self.arc_notebook, bg=self.colors['secondary'])
        self.arc_notebook.add(tab2, text="Center")

        # Center point selection frame
        center_sel_frame = tk.Frame(tab2, bg=self.colors['secondary'])
        center_sel_frame.pack(fill=tk.X, pady=10, padx=5)

        self.arc_center_var = tk.StringVar(value="None selected")
        tk.Label(center_sel_frame, text="Center Point:", 
                bg=self.colors['secondary'], fg=self.colors['fg'],
                font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.arc_center_label = tk.Label(center_sel_frame, textvariable=self.arc_center_var,
                                        bg=self.colors['secondary'], fg=self.colors['warning'],
                                        font=("Consolas", 10, "bold"))
        self.arc_center_label.pack(anchor=tk.W, pady=(2, 5))

        btn_row = tk.Frame(center_sel_frame, bg=self.colors['secondary'])
        btn_row.pack(fill=tk.X, pady=5)

        self._create_button(btn_row, "🎯 Choose Center", 
                           self.callbacks.get('choose_center_point', lambda: None),
                           'warning', width=12)
        self._create_button(btn_row, "✓ Use This Center", 
                           self.callbacks.get('use_chosen_center', lambda: None),
                           'success', width=12)

        # Manual entry row
        manual_row = tk.Frame(center_sel_frame, bg=self.colors['secondary'])
        manual_row.pack(fill=tk.X, pady=10)

        tk.Label(manual_row, text="Or enter Point ID:", 
                bg=self.colors['secondary'], fg=self.colors['fg'],
                font=("Arial", 9)).pack(side=tk.LEFT)

        self.arc_manual_center_var = tk.StringVar()
        tk.Entry(manual_row, textvariable=self.arc_manual_center_var, width=8,
                bg=self.colors['text_bg'], fg=self.colors['text_fg'],
                font=("Consolas", 9), relief=tk.FLAT,
                highlightbackground=self.colors['border'],
                highlightthickness=1).pack(side=tk.LEFT, padx=5)

        self._create_button(manual_row, "Set",
                           self.callbacks.get('set_center_manual', lambda: None),
                           'button_bg', small=True)

        tk.Label(tab2, text="Click 'Choose Center' then click a point in 3D view", 
                bg=self.colors['secondary'], fg='#888888',
                font=("Arial", 8), wraplength=300).pack(pady=5)

        # Radius tab
        tab3 = tk.Frame(self.arc_notebook, bg=self.colors['secondary'])
        self.arc_notebook.add(tab3, text="Radius")

        radius_frame = tk.Frame(tab3, bg=self.colors['secondary'])
        radius_frame.pack(fill=tk.X, pady=5)

        tk.Label(radius_frame, text="Radius:", bg=self.colors['secondary'],
                fg=self.colors['fg'], font=("Arial", 9)).pack(side=tk.LEFT, padx=5)

        self.radius_var = tk.DoubleVar(value=1.0)
        tk.Entry(radius_frame, textvariable=self.radius_var, width=8,
                bg=self.colors['text_bg'], fg=self.colors['text_fg'],
                font=("Arial", 9), relief=tk.FLAT,
                highlightbackground=self.colors['border'],
                highlightthickness=1).pack(side=tk.LEFT, padx=5)

        self._create_button(radius_frame, "Preview",
                           self.callbacks.get('preview_radius_arcs', lambda: None),
                           'accent', small=True)

        # Side selection frame - WHITE BORDER
        side_frame = tk.LabelFrame(tab3, text="Select Side", 
                                  bg=self.colors['secondary'],
                                  fg=self.colors['fg'],
                                  font=("Arial", 9, "bold"),
                                  relief=tk.FLAT, bd=1,
                                  highlightbackground='white',  # WHITE BORDER
                                  highlightthickness=1,
                                  highlightcolor='white')
        side_frame.pack(fill=tk.X, pady=10, padx=5)

        # Info label
        self.radius_side_var = tk.StringVar(value="Click 'Preview' to see both options")
        tk.Label(side_frame, textvariable=self.radius_side_var,
                bg=self.colors['secondary'], fg='#888888',
                font=("Arial", 9), wraplength=350).pack(pady=5)

        # Side selection buttons
        btn_row = tk.Frame(side_frame, bg=self.colors['secondary'])
        btn_row.pack(fill=tk.X, pady=5)

        self._create_button(btn_row, "🎯 Select Side A", 
                           self.callbacks.get('select_side_a', lambda: None),
                           'success', width=14)
        self._create_button(btn_row, "🎯 Select Side B", 
                           self.callbacks.get('select_side_b', lambda: None),
                           'warning', width=14)

        # Selected side display
        self.selected_side_var = tk.StringVar(value="No side selected")
        tk.Label(side_frame, text="Selected:", bg=self.colors['secondary'],
                fg=self.colors['fg'], font=("Arial", 9, "bold")).pack(anchor=tk.W, padx=5, pady=(5,0))
        tk.Label(side_frame, textvariable=self.selected_side_var,
                bg=self.colors['secondary'], fg=self.colors['accent'],
                font=("Consolas", 10, "bold")).pack(anchor=tk.W, padx=5, pady=(0,5))

        self._create_button(tab3, "✓ Use This Arc",
                           self.callbacks.get('use_selected_radius_arc', lambda: None),
                           'success', width=15)

        # Spline/PolyLine Configuration
        self.spline_config = tk.Frame(self.config_frame, bg=self.colors['secondary'])

        tk.Label(self.spline_config, text="Intermediate Points",
                font=("Arial", 9, "bold"), bg=self.colors['secondary'],
                fg=self.colors['fg']).pack(anchor=tk.W, pady=5)

        # Listbox with frame
        list_frame = tk.Frame(self.spline_config, bg=self.colors['secondary'],
                             highlightbackground=self.colors['border'],
                             highlightthickness=1)
        list_frame.pack(fill=tk.X, pady=5)

        self.spline_listbox = tk.Listbox(list_frame, height=5,
                                        bg=self.colors['text_bg'],
                                        fg=self.colors['text_fg'],
                                        font=("Consolas", 9),
                                        relief=tk.FLAT,
                                        selectbackground=self.colors['accent'],
                                        selectforeground='white')
        self.spline_listbox.pack(fill=tk.X, padx=1, pady=1)

        # Spline buttons
        spline_btn_frame = tk.Frame(self.spline_config, bg=self.colors['secondary'])
        spline_btn_frame.pack(fill=tk.X, pady=5)

        self._create_button(spline_btn_frame, "Add",
                           self.callbacks.get('add_spline_point', lambda: None),
                           'success', small=True)
        self._create_button(spline_btn_frame, "Remove",
                           self.callbacks.get('remove_spline_point', lambda: None),
                           'warning', small=True)
        self._create_button(spline_btn_frame, "Clear",
                           self.callbacks.get('clear_spline_points', lambda: None),
                           'error', small=True)

        # Manual Entry Section - WHITE BORDER
        manual_frame = self._create_section_frame(scrollable_frame, "Manual Point Entry")

        coord_grid = tk.Frame(manual_frame, bg=self.colors['secondary'])
        coord_grid.pack(fill=tk.X, pady=5)

        for i, (label, var) in enumerate(zip(['X', 'Y', 'Z'], manual_coords)):
            tk.Label(coord_grid, text=label + ":",
                    bg=self.colors['secondary'], fg=self.colors['fg'],
                    font=("Arial", 9, "bold"), width=3).grid(row=0, column=i*2, padx=2)

            entry = tk.Entry(coord_grid, textvariable=var, width=8,
                           bg=self.colors['text_bg'], fg=self.colors['text_fg'],
                           font=("Consolas", 9), relief=tk.FLAT,
                           highlightbackground=self.colors['border'],
                           highlightthickness=1)
            entry.grid(row=0, column=i*2+1, padx=2)
            entry.bind('<Return>', lambda e: self.callbacks.get('add_manual_point', lambda: None)())

        # Only Add Point button
        manual_btn_frame = tk.Frame(manual_frame, bg=self.colors['secondary'])
        manual_btn_frame.pack(fill=tk.X, pady=8)

        self._create_button(manual_btn_frame, "Add Point",
                           self.callbacks.get('add_manual_point', lambda: None),
                           'accent', small=True)

        # Status Section - WHITE BORDER
        status_frame = self._create_section_frame(scrollable_frame, "Status")

        self.status_label = tk.Label(status_frame, 
                                    text="Ready - Select start point",
                                    font=("Consolas", 9),
                                    bg=self.colors['secondary'],
                                    fg=self.colors['success'],
                                    justify=tk.LEFT)
        self.status_label.pack(anchor=tk.W)

        # Action Buttons
        action_frame = tk.Frame(scrollable_frame, bg=self.colors['secondary'])
        action_frame.pack(fill=tk.X, padx=8, pady=15)

        self._create_button(action_frame, "✓ Create Edge",
                           self.callbacks.get('create_edge', lambda: None),
                           'success', width=18)
        self._create_button(action_frame, "✗ Reset",
                           self.callbacks.get('reset_creation', lambda: None),
                           'error', width=12)

    def setup_manage_tab(self):
        """Setup the Manage Edges tab with black scrollbar"""
        # Use scrollable canvas with black scrollbar
        canvas, scrollbar, scrollable_frame = self._create_scrollable_canvas(self.tab_manage)

        # Edge List Section - WHITE BORDER
        list_frame = self._create_section_frame(scrollable_frame, "Defined Edges")

        # Listbox with frame
        list_container = tk.Frame(list_frame, bg=self.colors['secondary'],
                                 highlightbackground=self.colors['border'],
                                 highlightthickness=1)
        list_container.pack(fill=tk.BOTH, expand=True, pady=5)

        self.edge_listbox = tk.Listbox(list_container, height=12,
                                      bg=self.colors['text_bg'],
                                      fg=self.colors['text_fg'],
                                      font=("Consolas", 9),
                                      relief=tk.FLAT,
                                      selectbackground=self.colors['accent'],
                                      selectforeground='white')
        self.edge_listbox.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        self.edge_listbox.bind('<<ListboxSelect>>', 
                              self.callbacks.get('on_edge_select', lambda e: None))

        # Action buttons
        btn_frame = tk.Frame(list_frame, bg=self.colors['secondary'])
        btn_frame.pack(fill=tk.X, pady=8)

        self._create_button(btn_frame, "Edit",
                           self.callbacks.get('edit_selected_edge', lambda: None),
                           'accent', small=True)
        self._create_button(btn_frame, "Delete",
                           self.callbacks.get('delete_edge', lambda: None),
                           'error', small=True)
        self._create_button(btn_frame, "Delete All",
                           self.callbacks.get('delete_all_edges', lambda: None),
                           'warning', small=True)
        self._create_button(btn_frame, "Highlight",
                           self.callbacks.get('highlight_edge', lambda: None),
                           'success', small=True)

        # Details Section - WHITE BORDER
        details_frame = self._create_section_frame(scrollable_frame, "Edge Details")

        self.edge_details = tk.Label(details_frame, 
                                    text="Select an edge to view details",
                                    font=("Consolas", 9),
                                    bg=self.colors['secondary'],
                                    fg='#888888',
                                    justify=tk.LEFT,
                                    wraplength=320)
        self.edge_details.pack(anchor=tk.W, pady=5)

    def setup_edit_tab(self):
        """Setup the Edit Edge tab with black scrollbar"""
        # Use scrollable canvas with black scrollbar
        canvas, scrollbar, scrollable_frame = self._create_scrollable_canvas(self.tab_edit)

        # Edit Info
        self.edit_info_label = tk.Label(scrollable_frame,
                                       text="Select an edge from Manage tab",
                                       font=("Arial", 10, "bold"),
                                       bg=self.colors['secondary'],
                                       fg=self.colors['warning'])
        self.edit_info_label.pack(pady=10)

        # Type Display
        type_frame = tk.Frame(scrollable_frame, bg=self.colors['secondary'])
        type_frame.pack(fill=tk.X, padx=8, pady=5)

        tk.Label(type_frame, text="Type:",
                bg=self.colors['secondary'], fg=self.colors['fg'],
                font=("Arial", 9, "bold")).pack(side=tk.LEFT)

        self.edit_type_label = tk.Label(type_frame, text="—",
                                       bg=self.colors['secondary'],
                                       fg=self.colors['accent'],
                                       font=("Arial", 9, "bold"))
        self.edit_type_label.pack(side=tk.LEFT, padx=10)

        # Endpoints Section - WHITE BORDER
        points_frame = self._create_section_frame(scrollable_frame, "Endpoints")

        # Start point
        start_row = tk.Frame(points_frame, bg=self.colors['secondary'])
        start_row.pack(fill=tk.X, pady=5)

        tk.Label(start_row, text="Start:",
                bg=self.colors['secondary'], fg=self.colors['success'],
                font=("Arial", 9, "bold"), width=8).pack(side=tk.LEFT)

        self.edit_start_var = tk.StringVar(value="—")
        tk.Label(start_row, textvariable=self.edit_start_var,
                bg=self.colors['secondary'], fg=self.colors['fg'],
                font=("Consolas", 9)).pack(side=tk.LEFT, fill=tk.X, expand=True)

        start_btn_frame = tk.Frame(start_row, bg=self.colors['secondary'])
        start_btn_frame.pack(side=tk.RIGHT)
        self._create_button(start_btn_frame, "Click",
                           lambda: self.callbacks.get('change_edit_point', lambda x: None)('start'),
                           'accent', small=True)
        self._create_button(start_btn_frame, "Manual",
                           lambda: self.callbacks.get('change_edit_point_manual', lambda x: None)('start'),
                           'button_bg', small=True)

        # End point
        end_row = tk.Frame(points_frame, bg=self.colors['secondary'])
        end_row.pack(fill=tk.X, pady=5)

        tk.Label(end_row, text="End:",
                bg=self.colors['secondary'], fg=self.colors['error'],
                font=("Arial", 9, "bold"), width=8).pack(side=tk.LEFT)

        self.edit_end_var = tk.StringVar(value="—")
        tk.Label(end_row, textvariable=self.edit_end_var,
                bg=self.colors['secondary'], fg=self.colors['fg'],
                font=("Consolas", 9)).pack(side=tk.LEFT, fill=tk.X, expand=True)

        end_btn_frame = tk.Frame(end_row, bg=self.colors['secondary'])
        end_btn_frame.pack(side=tk.RIGHT)
        self._create_button(end_btn_frame, "Click",
                           lambda: self.callbacks.get('change_edit_point', lambda x: None)('end'),
                           'accent', small=True)
        self._create_button(end_btn_frame, "Manual",
                           lambda: self.callbacks.get('change_edit_point_manual', lambda x: None)('end'),
                           'button_bg', small=True)

        # Intermediate Points Section - WHITE BORDER
        self.edit_intermediate_frame = self._create_section_frame(
            scrollable_frame, "Intermediate Points")

        list_container = tk.Frame(self.edit_intermediate_frame,
                                 bg=self.colors['secondary'],
                                 highlightbackground=self.colors['border'],
                                 highlightthickness=1)
        list_container.pack(fill=tk.X, pady=5)

        self.edit_intermediate_listbox = tk.Listbox(list_container, height=6,
                                                    bg=self.colors['text_bg'],
                                                    fg=self.colors['text_fg'],
                                                    font=("Consolas", 9),
                                                    relief=tk.FLAT,
                                                    selectbackground=self.colors['accent'],
                                                    selectforeground='white')
        self.edit_intermediate_listbox.pack(fill=tk.X, padx=1, pady=1)

        # Intermediate buttons
        int_btn_frame = tk.Frame(self.edit_intermediate_frame,
                                bg=self.colors['secondary'])
        int_btn_frame.pack(fill=tk.X, pady=5)

        self._create_button(int_btn_frame, "Add Click",
                           self.callbacks.get('edit_add_point', lambda: None),
                           'success', small=True)
        self._create_button(int_btn_frame, "Add Manual",
                           self.callbacks.get('edit_add_point_manual', lambda: None),
                           'accent', small=True)
        self._create_button(int_btn_frame, "Remove",
                           self.callbacks.get('edit_remove_point', lambda: None),
                           'warning', small=True)
        self._create_button(int_btn_frame, "Clear",
                           self.callbacks.get('edit_clear_points', lambda: None),
                           'error', small=True)

        # Save/Cancel buttons
        action_frame = tk.Frame(scrollable_frame, bg=self.colors['secondary'])
        action_frame.pack(fill=tk.X, padx=8, pady=15)

        self._create_button(action_frame, "💾 Save Changes",
                           self.callbacks.get('save_edit_changes', lambda: None),
                           'success', width=18)
        self._create_button(action_frame, "Cancel",
                           self.callbacks.get('cancel_edit', lambda: None),
                           'error', width=12)