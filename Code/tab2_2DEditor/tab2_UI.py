import tkinter as tk
from tkinter import messagebox, simpledialog
import math

def setup_ui(self):
    """Setup the UI for the 2D editor tab"""
    # Main frame
    main_frame = tk.Frame(self.parent, bg=self.colors['bg'])
    main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Left: Canvas area
    self.left_frame = tk.Frame(main_frame, bg=self.colors['bg'])
    self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Header frame with title and position indicator
    header_frame = tk.Frame(self.left_frame, bg=self.colors['bg'])
    header_frame.pack(fill=tk.X)

    self.canvas_label = tk.Label(header_frame, text="2D View", 
                                font=("Arial", 12, "bold"),
                                bg=self.colors['bg'], fg=self.colors['fg'])
    self.canvas_label.pack(side=tk.LEFT)

    # Position indicator (matplotlib-like) - top right corner
    self.position_label = tk.Label(header_frame, text="x=0.00, y=0.00, z=0.00 | Layer 0", 
                                  font=("Arial", 9, "bold"),
                                  bg=self.colors['bg'], fg=self.colors['success'],
                                  anchor=tk.E)
    self.position_label.pack(side=tk.RIGHT, padx=10)

    # Container for canvas(es)
    self.canvas_container = tk.Frame(self.left_frame, bg=self.colors['bg'])
    self.canvas_container.pack(fill=tk.BOTH, expand=True)

    # Single canvas (normal mode)
    self.canvas = tk.Canvas(self.canvas_container, 
                            bg=self.colors['canvas_bg'], 
                            width=self.canvas_width, 
                            height=self.canvas_height,
                            highlightthickness=1,
                            highlightbackground=self.colors['border'])
    self.canvas.pack(fill=tk.BOTH, expand=True)
    self.canvas.bind("<Button-1>", self.on_canvas_click)
    self.setup_canvas_bindings(self.canvas)

    # Control buttons at bottom
    button_frame = tk.Frame(self.left_frame, bg=self.colors['bg'])
    button_frame.pack(fill=tk.X, pady=5)

    tk.Button(button_frame, text="🔍 Fit All", command=self.fit_all_view,
             bg=self.colors['button_bg'], fg=self.colors['button_fg'],
             font=("Arial", 10, "bold"), relief=tk.FLAT,
             activebackground=self.colors['button_active'],
             activeforeground=self.colors['button_fg'],
             cursor='hand2').pack(side=tk.LEFT, padx=5)

    tk.Label(button_frame, text="Pan: Right-drag | Zoom: Scroll",
            font=("Arial", 9), fg=self.colors['fg'],
            bg=self.colors['bg']).pack(side=tk.LEFT, padx=10)

    # Right: Controls with scrolling
    right_container = tk.Frame(main_frame, width=350, bg=self.colors['secondary'])
    right_container.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
    right_container.pack_propagate(False)

    # Create canvas for scrolling
    right_canvas = tk.Canvas(right_container, bg=self.colors['secondary'], 
                            highlightthickness=0, width=330)
    right_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add scrollbar
    scrollbar = tk.Scrollbar(right_container, orient="vertical", 
                            command=right_canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure canvas scrolling
    right_canvas.configure(yscrollcommand=scrollbar.set)

    # Style the scrollbar
    scrollbar.config(
        bg=self.colors['secondary'],
        troughcolor=self.colors['bg'],
        activebackground=self.colors['accent']
    )

    # Create frame inside canvas for controls
    right_frame = tk.Frame(right_canvas, bg=self.colors['secondary'], width=330)

    # Create window inside canvas
    controls_window = right_canvas.create_window((0, 0), window=right_frame, anchor="nw")

    # Update scrollregion function
    def update_scrollregion(event=None):
        right_canvas.update_idletasks()
        bbox = right_canvas.bbox("all")
        if bbox:
            right_canvas.configure(scrollregion=bbox)
        right_canvas.itemconfig(controls_window, width=right_canvas.winfo_width())

    # Bind to frame resize
    right_frame.bind("<Configure>", update_scrollregion)
    right_canvas.bind("<Configure>", update_scrollregion)

    # Mouse wheel scrolling
    def on_mousewheel(event):
        right_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        return "break"

    # Bind mousewheel
    def bind_mousewheel_to_all(widget):
        widget.bind("<MouseWheel>", on_mousewheel)
        widget.bind("<Button-4>", lambda e: right_canvas.yview_scroll(-1, "units"))
        widget.bind("<Button-5>", lambda e: right_canvas.yview_scroll(1, "units"))
        for child in widget.winfo_children():
            bind_mousewheel_to_all(child)

    # Store reference
    self._bind_mousewheel = bind_mousewheel_to_all

    # Bind to canvas, scrollbar, and container
    right_canvas.bind("<MouseWheel>", on_mousewheel)
    right_canvas.bind("<Button-4>", lambda e: right_canvas.yview_scroll(-1, "units"))
    right_canvas.bind("<Button-5>", lambda e: right_canvas.yview_scroll(1, "units"))
    scrollbar.bind("<MouseWheel>", on_mousewheel)
    right_container.bind("<MouseWheel>", on_mousewheel)
    right_container.bind("<Button-4>", lambda e: right_canvas.yview_scroll(-1, "units"))
    right_container.bind("<Button-5>", lambda e: right_canvas.yview_scroll(1, "units"))

    # Store references
    self.right_canvas = right_canvas
    self.right_scrollbar = scrollbar
    self.right_frame = right_frame

    # Build controls
    self._setup_mode_controls(right_frame)
    self._setup_add_point_controls(right_frame)  # Add point mode controls
    self._setup_edit_point_button(right_frame)   # NEW: Edit Selected Point button here
    self._setup_layer_controls(right_frame)
    self._setup_manual_entry(right_frame)
    self._setup_connection_controls(right_frame)

    # Bind mousewheel to all created widgets recursively
    bind_mousewheel_to_all(right_frame)

    # Force update scrollregion after everything is created
    right_frame.update_idletasks()
    update_scrollregion()

    self.update_plot()