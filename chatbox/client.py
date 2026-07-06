import socket
import threading
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import queue

# ===== COLOR SYSTEM =====
PRIMARY_COLOR   = "#075E54"   # Sidebar header
SECONDARY_COLOR = "#128C7E"   # Chat header / accents
ACCENT_COLOR    = "#25D366"   # Buttons / active
ACCENT_HOVER    = "#1FAF56"   # Button hover
BACKGROUND_COLOR = "#ECE5DD"  # App background
SURFACE_COLOR   = "#FFFFFF"   # Cards / sidebar bg
SENT_BUBBLE     = "#DCF8C6"   # Sent message bubble
RECEIVED_BUBBLE = "#FFFFFF"   # Received message bubble
TEXT_PRIMARY    = "#111B21"   # Main text
TEXT_SECONDARY  = "#667781"   # Secondary / placeholder
ERROR_COLOR     = "#FF3B30"   # Danger buttons
BORDER_COLOR    = "#E0E0E0"   # Dividers
SELECTED_BG     = "#E8F5E9"   # Selected user row
HOVER_BG        = "#F5F5F5"   # Hovered user row

# ===== TYPOGRAPHY =====
FONT            = "Segoe UI"
F_TITLE         = (FONT, 16, "bold")
F_HEADER        = (FONT, 14, "bold")
F_BODY          = (FONT, 11)
F_BODY_BOLD     = (FONT, 11, "bold")
F_SMALL         = (FONT, 9)
F_SMALL_BOLD    = (FONT, 9, "bold")
F_TINY          = (FONT, 8)

# ===== SPACING =====
PAD_SM = 5
PAD_MD = 10
PAD_LG = 15


class ChatClient:
    def __init__(self):
        self.client = None
        self.nickname = None
        self.host = '127.0.0.1'
        self.port = 5555
        self.connected = False
        self.message_queue = queue.Queue()  # Thread-safe message queue
        
        # Main window
        self.window = tk.Tk()
        self.window.title("💬 ChatBox")
        self.window.geometry("1000x600")
        self.window.configure(bg=BACKGROUND_COLOR)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Chat UI elements
        self.users_listbox_frame = None
        self.user_labels = {}
        self.selected_user = None
        self.selected_user_label = None
        self.msg_entry = None
        self.chat_header_label = None
        self.chat_status_label = None
        self.chat_canvas = None
        self.chat_inner_frame = None
        self.send_button = None
        
        # Chat data
        self.online_users = []
        self.chat_history = {}
        self.sent_message_ids = set()
        self.unread_messages = {}
        self.total_unread = 0
        self.notification_label = None
        self.pulse_state = False
        
        # Start listening to message queue
        self.process_message_queue()
        
        # Show login first
        self.build_login_screen()
        self.window.mainloop()
    
    def center_window(self, width, height):
        """Center window on screen"""
        self.window.geometry(f"{width}x{height}")
        self.window.update_idletasks()
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.window.geometry(f"+{x}+{y}")
    
    # ===== LOGIN SCREEN =====
    def build_login_screen(self):
        """Build login screen"""
        for widget in self.window.winfo_children():
            widget.destroy()

        self.window.resizable(False, False)
        self.center_window(420, 520)

        main_frame = tk.Frame(self.window, bg=BACKGROUND_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Frame(main_frame, bg=PRIMARY_COLOR, height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        header_inner = tk.Frame(header, bg=PRIMARY_COLOR)
        header_inner.pack(fill=tk.BOTH, expand=True, padx=PAD_LG, pady=PAD_MD)
        tk.Label(header_inner, text="� ChatBox", font=F_TITLE,
                 fg=SURFACE_COLOR, bg=PRIMARY_COLOR).pack(anchor=tk.W)
        tk.Label(header_inner, text="Connect to chat", font=F_SMALL,
                 fg=ACCENT_COLOR, bg=PRIMARY_COLOR).pack(anchor=tk.W, pady=(3, 0))

        # Form
        form_container = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
        form_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        form_frame = tk.Frame(form_container, bg=SURFACE_COLOR, relief="flat", bd=0,
                              highlightthickness=1, highlightbackground=BORDER_COLOR)
        form_frame.pack(fill=tk.X)

        def _field(parent, label_text):
            tk.Label(parent, text=label_text, font=F_SMALL_BOLD,
                     bg=SURFACE_COLOR, fg=TEXT_PRIMARY).pack(anchor=tk.W, padx=PAD_MD, pady=(PAD_MD, 3))
            e = tk.Entry(parent, font=F_BODY, relief="flat", bd=0,
                         bg=BACKGROUND_COLOR, fg=TEXT_PRIMARY,
                         insertbackground=SECONDARY_COLOR, width=35,
                         highlightthickness=1, highlightbackground=BORDER_COLOR,
                         highlightcolor=SECONDARY_COLOR)
            e.pack(padx=PAD_MD, pady=(0, PAD_MD), ipady=6, fill=tk.X)
            return e

        username_entry = _field(form_frame, "📝 Username")
        username_entry.focus()
        ip_entry = _field(form_frame, "🌐 Server IP")
        ip_entry.insert(0, self.host)
        port_entry = _field(form_frame, "🔌 Port")
        port_entry.insert(0, str(self.port))

        error_label = tk.Label(form_frame, text="", font=F_SMALL,
                               fg=ERROR_COLOR, bg=SURFACE_COLOR, wraplength=280)
        error_label.pack(anchor=tk.W, padx=PAD_MD, pady=(0, PAD_MD))

        btn_frame = tk.Frame(form_frame, bg=SURFACE_COLOR)
        btn_frame.pack(fill=tk.X, padx=PAD_MD, pady=(0, PAD_LG))

        def on_connect():
            error_label.config(text="", fg=ERROR_COLOR)
            username = username_entry.get().strip()
            if not username:
                error_label.config(text="⚠ Please enter your username")
                username_entry.focus()
                return
            server_ip = ip_entry.get().strip() or '127.0.0.1'
            try:
                server_port = int(port_entry.get().strip() or '5555')
                if not (1 <= server_port <= 65535):
                    raise ValueError("Port must be 1–65535")
            except ValueError as ex:
                error_label.config(text=f"⚠ Invalid port: {ex}")
                port_entry.focus()
                return
            error_label.config(text="🔄 Connecting...", fg=ACCENT_COLOR)
            self.window.update()
            if self.connect_to_server(username, server_ip, server_port):
                self.build_chat_ui()
            else:
                error_label.config(text="❌ Connection failed. Try again.", fg=ERROR_COLOR)

        connect_btn = tk.Button(btn_frame, text="CONNECT", command=on_connect,
                                font=F_BODY_BOLD, bg=ACCENT_COLOR, fg=SURFACE_COLOR,
                                padx=30, pady=10, cursor="hand2", relief="flat", bd=0,
                                activebackground=ACCENT_HOVER, activeforeground=SURFACE_COLOR)
        connect_btn.pack(expand=True)
        connect_btn.bind("<Enter>", lambda e: connect_btn.config(bg=ACCENT_HOVER))
        connect_btn.bind("<Leave>", lambda e: connect_btn.config(bg=ACCENT_COLOR))

        username_entry.bind('<Return>', lambda e: ip_entry.focus())
        ip_entry.bind('<Return>', lambda e: port_entry.focus())
        port_entry.bind('<Return>', lambda e: on_connect())
    
    # ===== CONNECTION =====
    def connect_to_server(self, username, host, port):
        """Connect to server"""
        try:
            self.nickname = username
            self.host = host
            self.port = port
            
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(5)
            self.client.connect((self.host, self.port))
            
            # Remove timeout for receive loop (we want to listen indefinitely)
            self.client.settimeout(None)
            
            # Send username
            self.client.send(self.nickname.encode('utf-8'))
            
            self.connected = True
            
            # Start receiving messages in background thread
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()
            
            return True
            
        except socket.timeout:
            messagebox.showerror("Connection Error", 
                               f"Connection timeout. Server not responding on {host}:{port}")
            return False
        except ConnectionRefusedError:
            messagebox.showerror("Connection Error",
                               f"Connection refused. No server running on {host}:{port}")
            return False
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
            return False
    
    # ===== MESSAGE QUEUE PROCESSOR (THREAD-SAFE) =====
    # ===== MESSAGE QUEUE PROCESSOR (THREAD-SAFE) =====
    def process_message_queue(self):
        """Drain the queue on the main thread — one message per iteration to stay responsive."""
        try:
            # Process up to 10 messages per tick to avoid blocking the UI
            for _ in range(10):
                try:
                    message = self.message_queue.get_nowait()
                except queue.Empty:
                    break
                try:
                    self.display_message(message)
                except Exception as e:
                    print(f"[QUEUE] display_message error: {e}")
        except Exception as e:
            print(f"[QUEUE] Unexpected error: {e}")
        finally:
            # Always reschedule — never let the processor die silently
            self.window.after(50, self.process_message_queue)
    
    def pulse_notification(self):
        """Pulse notification badge for new messages"""
        if self.notification_label and self.total_unread > 0:
            self.pulse_state = not self.pulse_state
            color = "#c0392b" if self.pulse_state else ERROR_COLOR
            self.notification_label.config(bg=color)
            self.window.after(500, self.pulse_notification)
    
    def update_notification_badge(self):
        """Recompute total unread and update badge — must be called on main thread."""
        if not self.notification_label:
            return
        # Sum only positive values; ignore zero/stale keys
        self.total_unread = sum(v for v in self.unread_messages.values() if v > 0)
        if self.total_unread > 0:
            self.notification_label.config(
                text=f"🔔 {self.total_unread} unread",
                bg=ERROR_COLOR, fg=SURFACE_COLOR, state=tk.NORMAL)
            if not self.pulse_state:
                self.pulse_notification()
        else:
            self.pulse_state = False  # stop pulse loop
            self.notification_label.config(
                text="✅ No new messages",
                bg="#2E7D32", fg=SURFACE_COLOR, state=tk.NORMAL)

    def show_toast(self, sender, message):
        """Toast disabled — unread badge handles notifications instead"""
        return
    
    # ===== CHAT UI =====
    def _make_btn(self, parent, text, command, bg, hover_bg):
        """Reusable premium-styled button with simulated depth"""
        # Derive a slightly darker shade for the highlight border
        btn = tk.Button(parent, text=text, command=command,
                        font=F_BODY_BOLD, bg=bg, fg=SURFACE_COLOR,
                        padx=16, pady=11, cursor="hand2",
                        relief=tk.FLAT, bd=0,
                        activebackground=hover_bg, activeforeground=SURFACE_COLOR,
                        highlightthickness=1, highlightbackground=hover_bg)

        def on_enter(e):
            btn.config(bg=hover_bg, highlightbackground=hover_bg)

        def on_leave(e):
            btn.config(bg=bg, highlightbackground=hover_bg)

        def on_press(e):
            btn.config(pady=10)   # subtle press-down feel

        def on_release(e):
            btn.config(pady=11)

        btn.bind("<Enter>",          on_enter)
        btn.bind("<Leave>",          on_leave)
        btn.bind("<ButtonPress-1>",  on_press)
        btn.bind("<ButtonRelease-1>", on_release)
        return btn

    def build_chat_ui(self):
        """Build chat interface"""
        for widget in self.window.winfo_children():
            widget.destroy()

        self.window.resizable(True, True)
        self.window.geometry("1000x600")
        self.window.title(f"💬 ChatBox — {self.nickname}")

        root = tk.Frame(self.window, bg=BACKGROUND_COLOR)
        root.pack(fill=tk.BOTH, expand=True)

        # ===== SIDEBAR =====
        sidebar = tk.Frame(root, bg=SURFACE_COLOR, width=270)
        sidebar.pack(side=tk.LEFT, fill=tk.BOTH)
        sidebar.pack_propagate(False)

        # Sidebar header
        sb_header = tk.Frame(sidebar, bg=PRIMARY_COLOR, height=90)
        sb_header.pack(fill=tk.X)
        sb_header.pack_propagate(False)
        tk.Label(sb_header, text=f"� {self.nickname}", font=F_HEADER,
                 fg=SURFACE_COLOR, bg=PRIMARY_COLOR).pack(anchor=tk.W, padx=PAD_LG, pady=(PAD_MD, 2))
        tk.Label(sb_header, text="● Online", font=F_SMALL,
                 fg=ACCENT_COLOR, bg=PRIMARY_COLOR).pack(anchor=tk.W, padx=PAD_LG)
        self.notification_label = tk.Label(sb_header, text="✅ No new messages",
                 font=F_SMALL_BOLD, fg=SURFACE_COLOR, bg="#2E7D32", padx=8, pady=2)
        self.notification_label.pack(anchor=tk.W, padx=PAD_LG)

        # Section label
        tk.Label(sidebar, text="CONTACTS", font=(FONT, 9, "bold"),
                 fg=TEXT_SECONDARY, bg=SURFACE_COLOR).pack(anchor=tk.W, padx=PAD_LG, pady=(PAD_MD, PAD_SM))
        tk.Frame(sidebar, bg=BORDER_COLOR, height=1).pack(fill=tk.X, padx=PAD_MD)

        # User list
        self.users_listbox_frame = tk.Frame(sidebar, bg=SURFACE_COLOR)
        self.users_listbox_frame.pack(fill=tk.BOTH, expand=True)

        # Bottom buttons
        btn_area = tk.Frame(sidebar, bg=SURFACE_COLOR)
        btn_area.pack(fill=tk.X, padx=PAD_MD, pady=PAD_MD, side=tk.BOTTOM)
        tk.Frame(sidebar, bg=BORDER_COLOR, height=1).pack(fill=tk.X, side=tk.BOTTOM)

        self._make_btn(btn_area, "🔄  Refresh", self.refresh_users,
                       ACCENT_COLOR, ACCENT_HOVER).pack(fill=tk.X, pady=(0, 6))
        self._make_btn(btn_area, "⏏  Disconnect", self.disconnect_from_server,
                       ERROR_COLOR, "#c0392b").pack(fill=tk.X, pady=(0, 6))
        self._make_btn(btn_area, "✕  Exit", self.exit_application,
                       "#4a4a4a", "#2f2f2f").pack(fill=tk.X)

        # ===== CHAT AREA =====
        chat_area = tk.Frame(root, bg=BACKGROUND_COLOR)
        chat_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Chat header
        ch = tk.Frame(chat_area, bg=SECONDARY_COLOR, height=70)
        ch.pack(fill=tk.X)
        ch.pack_propagate(False)
        ch_inner = tk.Frame(ch, bg=SECONDARY_COLOR)
        ch_inner.pack(fill=tk.BOTH, expand=True, padx=PAD_LG, pady=PAD_MD)
        self.chat_header_label = tk.Label(ch_inner, text="Select a contact",
                 font=F_HEADER, fg=SURFACE_COLOR, bg=SECONDARY_COLOR)
        self.chat_header_label.pack(side=tk.LEFT)
        self.chat_status_label = tk.Label(ch_inner, text="",
                 font=F_SMALL, fg=ACCENT_COLOR, bg=SECONDARY_COLOR)
        self.chat_status_label.pack(side=tk.RIGHT)

        # Message canvas
        msg_frame = tk.Frame(chat_area, bg=BACKGROUND_COLOR)
        msg_frame.pack(fill=tk.BOTH, expand=True)

        self.chat_canvas = tk.Canvas(msg_frame, bg=BACKGROUND_COLOR,
                                     highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(msg_frame, command=self.chat_canvas.yview)
        self.chat_inner_frame = tk.Frame(self.chat_canvas, bg=BACKGROUND_COLOR)

        self.chat_inner_frame.bind("<Configure>",
            lambda e: self.chat_canvas.configure(
                scrollregion=self.chat_canvas.bbox("all")))
        self.chat_canvas_window = self.chat_canvas.create_window(
            0, 0, window=self.chat_inner_frame, anchor="nw")
        self.chat_canvas.config(yscrollcommand=scrollbar.set)

        def _on_canvas_resize(e):
            self.chat_canvas.itemconfig(self.chat_canvas_window, width=e.width)
        self.chat_canvas.bind("<Configure>", _on_canvas_resize)

        self.chat_canvas.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)

        self.chat_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.chat_canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.chat_canvas.bind_all("<Button-5>", self._on_mousewheel)

        # Input bar
        input_bar = tk.Frame(chat_area, bg=SURFACE_COLOR, height=70)
        input_bar.pack(fill=tk.X, side=tk.BOTTOM)
        input_bar.pack_propagate(False)
        tk.Frame(chat_area, bg=BORDER_COLOR, height=1).pack(fill=tk.X, side=tk.BOTTOM)

        input_inner = tk.Frame(input_bar, bg=SURFACE_COLOR)
        input_inner.pack(fill=tk.BOTH, expand=True, padx=PAD_LG, pady=PAD_MD)

        self.msg_entry = tk.Entry(input_inner, font=F_BODY,
                                  bg=BACKGROUND_COLOR, fg=TEXT_SECONDARY,
                                  relief=tk.FLAT, bd=0,
                                  insertbackground=ACCENT_COLOR,
                                  highlightthickness=1,
                                  highlightbackground=BORDER_COLOR,
                                  highlightcolor=SECONDARY_COLOR)
        self.msg_entry.insert(0, "Type a message...")
        self.msg_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True,
                            padx=(0, PAD_MD), ipady=8)

        def on_entry_focus_in(e):
            if self.msg_entry.get() == "Type a message...":
                self.msg_entry.delete(0, tk.END)
                self.msg_entry.config(fg=TEXT_PRIMARY)

        def on_entry_focus_out(e):
            if self.msg_entry.get().strip() == "":
                self.msg_entry.delete(0, tk.END)
                self.msg_entry.insert(0, "Type a message...")
                self.msg_entry.config(fg=TEXT_SECONDARY)

        def on_key_press(e):
            if self.msg_entry.get() == "Type a message...":
                self.msg_entry.delete(0, tk.END)
                self.msg_entry.config(fg=TEXT_PRIMARY)

        self.msg_entry.bind("<FocusIn>", on_entry_focus_in)
        self.msg_entry.bind("<FocusOut>", on_entry_focus_out)
        self.msg_entry.bind("<KeyPress>", on_key_press)
        self.msg_entry.bind("<Return>", lambda e: self.send_message())

        self.send_button = tk.Button(input_inner, text="Send",
                                     command=self.send_message,
                                     font=F_BODY_BOLD, bg=ACCENT_COLOR,
                                     fg=SURFACE_COLOR, padx=25, pady=8,
                                     cursor="hand2", relief=tk.FLAT, bd=0,
                                     activebackground=ACCENT_HOVER)
        self.send_button.pack(side=tk.RIGHT)
        self.send_button.bind("<Enter>", lambda e: self.send_button.config(bg=ACCENT_HOVER))
        self.send_button.bind("<Leave>", lambda e: self.send_button.config(bg=ACCENT_COLOR))

        # Welcome placeholder
        welcome = tk.Frame(self.chat_inner_frame, bg=BACKGROUND_COLOR)
        welcome.pack(fill=tk.X, padx=20, pady=60)
        tk.Label(welcome, text="👋 Welcome to ChatBox!",
                 font=F_HEADER, fg=SECONDARY_COLOR, bg=BACKGROUND_COLOR).pack()
        tk.Label(welcome, text="Select a contact to start chatting",
                 font=F_BODY, fg=TEXT_SECONDARY, bg=BACKGROUND_COLOR).pack(pady=PAD_SM)

        self.window.bind('<F5>', lambda e: self.refresh_users())
        self.window.bind('<Control-q>', lambda e: self.exit_application())
        self.window.bind('<Control-w>', lambda e: self.disconnect_from_server())
    
    # ===== MESSAGE HANDLING =====
    def display_message(self, message):
        """Handle one incoming message — called on main thread via process_message_queue."""
        message = message.strip()
        if not message:
            return

        if "->" not in message or ":" not in message:
            return

        parts = message.split("->", 1)
        if len(parts) != 2:
            return
        sender = parts[0].strip()
        rest = parts[1].split(":", 1)
        if len(rest) != 2:
            return
        recipient = rest[0].strip()
        msg_text  = rest[1].strip()

        if sender in ("ERROR", "SYSTEM"):
            return

        # Echo-back: we already stored + displayed this in send_message()
        if sender == self.nickname:
            return

        current_time = datetime.now().strftime("%H:%M")
        chat_user = sender  # conversation key is always the other person

        # Store exactly once — no duplication possible since echo is filtered above
        if chat_user not in self.chat_history:
            self.chat_history[chat_user] = []
        self.chat_history[chat_user].append((sender, msg_text, current_time))

        if self.selected_user == chat_user:
            # Chat is open — render bubble immediately (already on main thread)
            self.add_message_bubble(sender, msg_text, current_time, False)
        else:
            # Chat not open — increment unread, then update badge + label via after(0)
            self.unread_messages[chat_user] = self.unread_messages.get(chat_user, 0) + 1
            self.window.after(0, self.update_user_label, chat_user)
            self.window.after(0, self.update_notification_badge)
    
    def update_users_list(self, user_list_str):
        """Update users list"""
        try:
            users_str = user_list_str.replace("USER_LIST:", "").strip()
            print(f"[CLIENT] Parsing user list string: '{users_str}'")
            
            if not users_str:
                self.online_users = []
                print("[CLIENT] Empty user list")
            else:
                user_list = [u.strip() for u in users_str.split(",") if u.strip()]
                # Remove self from the list
                self.online_users = [u for u in user_list if u != self.nickname]
                print(f"[CLIENT] Online users: {self.online_users}")
        except Exception as e:
            print(f"Error parsing user list: {str(e)}")
            self.online_users = []
    
    def handle_user_list(self, user_list_str):
        """Handle USER_LIST messages directly without queue"""
        try:
            self.update_users_list(user_list_str)
            self.window.after(0, self.refresh_users_display)
        except Exception as e:
            print(f"Error handling user list: {str(e)}")
    
    @staticmethod
    def _avatar_color(username):
        """Deterministic soft color based on username"""
        colors = ["#6C63FF", "#FF8A65", "#4DB6AC", "#BA68C8", "#64B5F6",
                  "#F06292", "#81C784", "#FFB74D", "#4FC3F7", "#A1887F"]
        return colors[hash(username) % len(colors)]

    def refresh_users_display(self):
        """Refresh user list display with avatar icons"""
        try:
            if not self.users_listbox_frame or not self.users_listbox_frame.winfo_exists():
                return

            for widget in self.users_listbox_frame.winfo_children():
                widget.destroy()
            self.user_labels.clear()

            if not self.online_users:
                tk.Label(self.users_listbox_frame, text="No contacts online",
                         font=F_SMALL, fg=TEXT_SECONDARY, bg=SURFACE_COLOR).pack(pady=20)
                return

            for user in self.online_users:
                user_frame = tk.Frame(self.users_listbox_frame, bg=SURFACE_COLOR, height=56)
                user_frame.pack(fill=tk.X)
                user_frame.pack_propagate(False)

                content = tk.Frame(user_frame, bg=SURFACE_COLOR)
                content.pack(fill=tk.BOTH, expand=True, padx=PAD_MD, pady=PAD_SM)

                # Round avatar using Canvas
                avatar_color = self._avatar_color(user)
                icon = tk.Canvas(content, width=32, height=32,
                                 highlightthickness=0, bg=SURFACE_COLOR,
                                 cursor="hand2")
                icon.pack(side=tk.LEFT, padx=(0, PAD_MD))
                icon.create_oval(2, 2, 30, 30, fill=avatar_color, outline=avatar_color)
                icon.create_text(16, 16, text=user[0].upper(),
                                 fill=SURFACE_COLOR, font=F_SMALL_BOLD)

                # Username + unread badge
                unread = self.unread_messages.get(user, 0)
                user_text = user + (f"  ({unread})" if unread > 0 else "")
                fg = ERROR_COLOR if unread > 0 else TEXT_PRIMARY

                user_label = tk.Label(content, text=user_text, font=F_BODY_BOLD,
                                      fg=fg, bg=SURFACE_COLOR, cursor="hand2")
                user_label.pack(side=tk.LEFT, anchor="w")

                self.user_labels[user] = {
                    'frame': user_frame, 'label': user_label,
                    'content': content, 'icon': icon
                }

                def make_click(u): return lambda e: self.select_user(u)
                def make_in(u):    return lambda e: self._hover_user_in(u)
                def make_out(u):   return lambda e: self._hover_user_out(u)

                for w in (user_frame, content, icon, user_label):
                    w.bind("<Button-1>", make_click(user))
                    w.bind("<Enter>",    make_in(user))
                    w.bind("<Leave>",    make_out(user))

        except Exception as e:
            print(f"[DISPLAY] Error refreshing users: {e}")
    
    def _hover_user_in(self, user):
        if user != self.selected_user and user in self.user_labels:
            for k in ('frame', 'label', 'content'):
                self.user_labels[user][k].config(bg=HOVER_BG)

    def _hover_user_out(self, user):
        if user != self.selected_user and user in self.user_labels:
            for k in ('frame', 'label', 'content'):
                self.user_labels[user][k].config(bg=SURFACE_COLOR)

    def update_user_label(self, user):
        if user in self.user_labels:
            unread = self.unread_messages.get(user, 0)
            text = user + (f"  ({unread})" if unread > 0 else "")
            fg = ERROR_COLOR if unread > 0 else TEXT_PRIMARY
            self.user_labels[user]['label'].config(text=text, fg=fg)
    
    def select_user(self, user):
        """Select a user — resets its unread count immediately."""
        try:
            # Deselect previous
            if self.selected_user_label and self.selected_user_label in self.user_labels:
                for k in ('frame', 'label', 'content'):
                    self.user_labels[self.selected_user_label][k].config(bg=SURFACE_COLOR)

            self.selected_user = user
            self.selected_user_label = user

            # Highlight selected row
            if user in self.user_labels:
                for k in ('frame', 'label', 'content'):
                    self.user_labels[user][k].config(bg=SELECTED_BG)

            # Clear unread for this user — delete key so sum() stays accurate
            if self.unread_messages.pop(user, 0) > 0:
                self.update_user_label(user)
                self.update_notification_badge()

            self.update_chat_display(user)
            self.msg_entry.focus()

        except Exception as e:
            print(f"[SELECT ERROR] {e}")
    
    def update_chat_display(self, user):
        """Clear UI and reload full chat history for user"""
        try:
            self.chat_header_label.config(text=f"💬 {user}")
            self.chat_status_label.config(text="● Online")

            for widget in self.chat_inner_frame.winfo_children():
                widget.destroy()

            history = self.chat_history.get(user, [])
            print(f"[DISPLAY] Loading chat for '{user}': {len(history)} messages")

            if history:
                for sender, msg_text, time_str in history:
                    self.add_message_bubble(sender, msg_text, time_str, sender == self.nickname)
            else:
                empty = tk.Frame(self.chat_inner_frame, bg=BACKGROUND_COLOR)
                empty.pack(fill=tk.BOTH, expand=True, pady=60)
                tk.Label(empty, text=f"👋 Say hello to {user}!",
                         font=F_HEADER, fg=SECONDARY_COLOR, bg=BACKGROUND_COLOR).pack()
                tk.Label(empty, text="Start a new conversation",
                         font=F_BODY, fg=TEXT_SECONDARY, bg=BACKGROUND_COLOR).pack(pady=PAD_SM)

            self.chat_inner_frame.update_idletasks()
            self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
            self.chat_canvas.yview_moveto(1.0)

        except Exception as e:
            print(f"[DISPLAY ERROR] update_chat_display: {e}")
    
    def _rounded_rect(self, canvas, x1, y1, x2, y2, r=20, **kw):
        """Draw a smooth rounded rectangle on a canvas."""
        pts = [
            x1+r, y1,  x2-r, y1,
            x2,   y1,  x2,   y1+r,
            x2,   y2-r, x2,  y2,
            x2-r, y2,  x1+r, y2,
            x1,   y2,  x1,   y2-r,
            x1,   y1+r, x1,  y1,
        ]
        return canvas.create_polygon(pts, smooth=True, splinesteps=36, **kw)

    def add_message_bubble(self, sender, msg_text, time_str, is_sent):
        """Add rounded message bubble — sent RIGHT, received LEFT"""
        try:
            canvas_w = self.chat_canvas.winfo_width()
            max_text_w = max(220, int(canvas_w * 0.62))
            margin     = max(50,  int(canvas_w * 0.22))
            bg_color   = SENT_BUBBLE if is_sent else RECEIVED_BUBBLE
            PAD_X, PAD_Y = 8, 5

            # measure text size
            tmp = tk.Label(self.window, text=msg_text, font=(FONT, 10),
                           wraplength=max_text_w, justify="left")
            tmp.update_idletasks()
            tw = min(tmp.winfo_reqwidth(), max_text_w)
            th = tmp.winfo_reqheight()
            tmp.destroy()

            # time label width
            tmp_t = tk.Label(self.window, text=time_str, font=(FONT, 7))
            tmp_t.update_idletasks()
            ttw = tmp_t.winfo_reqwidth()
            tmp_t.destroy()

            # canvas dimensions — tight fit
            inner_w = max(tw, ttw) + PAD_X * 2
            inner_h = th + 14 + PAD_Y * 2   # 14px for time row

            # row container
            container = tk.Frame(self.chat_inner_frame, bg=BACKGROUND_COLOR)
            container.pack(fill="x", padx=10, pady=3)

            if is_sent:
                tk.Frame(container, bg=BACKGROUND_COLOR).pack(side="left", fill="x", expand=True)
                c = tk.Canvas(container, width=inner_w, height=inner_h,
                              bg=BACKGROUND_COLOR, highlightthickness=0)
                c.pack(side="right", anchor="e", padx=(margin, 4))
            else:
                c = tk.Canvas(container, width=inner_w, height=inner_h,
                              bg=BACKGROUND_COLOR, highlightthickness=0)
                c.pack(side="left", anchor="w", padx=(4, margin))
                tk.Frame(container, bg=BACKGROUND_COLOR).pack(side="right", fill="x", expand=True)

            # rounded background
            r = 25 if is_sent else 20
            self._rounded_rect(c, 2, 2, inner_w-2, inner_h-2,
                               r=r, fill=bg_color, outline=bg_color)

            # message text
            c.create_text(PAD_X, PAD_Y,
                          text=msg_text, anchor="nw",
                          width=max_text_w, font=(FONT, 10),
                          fill=TEXT_PRIMARY)

            # timestamp — bottom right
            c.create_text(inner_w - 6, inner_h - 3,
                          text=time_str, anchor="se",
                          font=(FONT, 7), fill=TEXT_SECONDARY)

            self.chat_inner_frame.update_idletasks()
            self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
            self.chat_canvas.yview_moveto(1.0)

        except Exception as e:
            print(f"[BUBBLE ERROR] {str(e)}")
    
    def send_message(self):
        """Send message — display instantly, don't wait for server echo"""
        msg = self.msg_entry.get().strip()

        # Block placeholder text and empty input
        if not msg or msg == "Type a message...":
            if not self.selected_user:
                messagebox.showwarning("Select User", "Click on a user to start messaging!")
            return

        if not self.selected_user:
            messagebox.showwarning("Select User", "Click on a user to start messaging!")
            return

        print(f"[SEND] Sending: '{msg}' to '{self.selected_user}'")

        try:
            current_time = datetime.now().strftime("%H:%M")

            # Store in history immediately
            if self.selected_user not in self.chat_history:
                self.chat_history[self.selected_user] = []
            self.chat_history[self.selected_user].append((self.nickname, msg, current_time))
            print(f"[SEND] Stored under '{self.selected_user}', total={len(self.chat_history[self.selected_user])}")

            # Show bubble immediately (instant feedback)
            self.add_message_bubble(self.nickname, msg, current_time, is_sent=True)

            # Send to server
            self.client.sendall(f"@{self.selected_user} {msg}".encode('utf-8'))

            # Reset input field
            self.msg_entry.delete(0, tk.END)
            self.msg_entry.insert(0, "Type a message...")
            self.msg_entry.config(fg=TEXT_SECONDARY)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to send: {str(e)}")
    
    def _on_mousewheel(self, event):
        """Mousewheel scrolling"""
        try:
            if event.num == 5 or event.delta < 0:
                self.chat_canvas.yview_scroll(1, "units")
            elif event.num == 4 or event.delta > 0:
                self.chat_canvas.yview_scroll(-1, "units")
        except:
            pass
    
    def receive_messages(self):
        """Receive messages from server (runs in background thread).
        Uses a buffer to handle TCP stream fragmentation — a single recv()
        may contain partial messages or multiple messages joined together.
        Messages are delimited by '\\n'.
        """
        print(f"[RECEIVE] Started for {self.nickname}")
        buffer = ""
        while True:
            try:
                data = self.client.recv(4096)
                if not data:
                    print("[RECEIVE] Connection closed by server")
                    break
                buffer += data.decode('utf-8')
                # Process all complete messages in the buffer
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    if not line:
                        continue
                    print(f"[RECEIVE] Message: {line[:80]}")
                    if line.startswith("USER_LIST:"):
                        self.window.after(0, self.handle_user_list, line)
                    else:
                        self.message_queue.put(line)
            except Exception as e:
                print(f"[RECEIVE] Error: {e}")
                break
        print("[RECEIVE] Thread ended")
        self.connected = False
    
    def disconnect_from_server(self):
        """Disconnect and go back to login"""
        self.connected = False
        if self.client:
            try:
                self.client.close()
            except:
                pass
        
        self.build_login_screen()
    
    def refresh_users(self):
        """Manually refresh user list"""
        try:
            if self.client:
                # Simply refresh the display of existing users
                self.refresh_stats()
                messagebox.showinfo("Refresh", "✅ User list refreshed!")
            else:
                messagebox.showwarning("Not Connected", "You are not connected to the server.")
        except Exception as e:
            messagebox.showerror("Refresh Error", f"Failed to refresh: {str(e)}")
    
    def refresh_stats(self):
        """Refresh display statistics"""
        self.refresh_users_display()
    
    def exit_application(self):
        """Exit application with confirmation"""
        if messagebox.askyesno("Exit ChatBox", "Are you sure you want to exit?"):
            self.on_closing()
    
    def on_closing(self):
        """Handle window close"""
        self.connected = False
        if self.client:
            try:
                self.client.close()
            except:
                pass
        self.window.destroy()


if __name__ == "__main__":
    try:
        app = ChatClient()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application error: {str(e)}")