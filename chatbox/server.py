import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
import time

# Modern WhatsApp-style color palette
SIDEBAR_GREEN = "#075E54"
HEADER_TEAL = "#128C7E"
BUTTON_GREEN = "#25D366"
WHITE = "#FFFFFF"
BACKGROUND_LIGHT = "#ECE5DD"
SIDEBAR_BG = "#FFFFFF"
DARK_GRAY = "#333333"
MEDIUM_GRAY = "#BDBDBD"
LIGHT_TEXT = "#757575"
SENT_BUBBLE = "#DCF8C6"
RECEIVED_BUBBLE = "#FFFFFF"
RED = "#FF3B30"
TIME_TEXT = "#999999"
BORDER_COLOR = "#E0E0E0"
DIVIDER_COLOR = "#EFEFEF"

class ChatServer:
    def __init__(self):
        self.users = {}  # Dictionary: {username: socket}
        self.server = None
        self.host = '127.0.0.1'
        self.port = 5555
        self.running = False
        self.message_count = 0
        self.users_text = None
        self.messages_label = None
        self.lock = threading.Lock()
        self.start_time = None
        self.uptime_label = None
        self.status_indicator = None
        self.pulse_state = False
        self.total_connections = 0  # Track total connections ever made
        self.connection_history = []  # Track connection events
        
    def start_gui(self):
        self.window = tk.Tk()
        self.window.title("💬 ChatBox Server Control")
        self.window.geometry("700x650")
        self.window.configure(bg=WHITE)
        
        # Header
        header = tk.Frame(self.window, bg=HEADER_TEAL, height=90)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_inner = tk.Frame(header, bg=HEADER_TEAL)
        header_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        title_label = tk.Label(header_inner, text="📱 ChatBox Server Control", font=("Segoe UI", 24, "bold"), 
                              fg=WHITE, bg=HEADER_TEAL)
        title_label.pack(anchor=tk.W)
        
        subtitle = tk.Label(header_inner, text="Professional Chat Server Management Console", 
                           font=("Segoe UI", 9), fg=LIGHT_TEXT, bg=HEADER_TEAL)
        subtitle.pack(anchor=tk.W, pady=(5, 0))
        
        # Main container
        main_container = tk.Frame(self.window, bg=WHITE)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left column - Configuration
        left_column = tk.Frame(main_container, bg=WHITE)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        
        # Server Configuration Frame
        config_frame = tk.LabelFrame(left_column, text="⚙️ Server Configuration", font=("Segoe UI", 11, "bold"),
                                     bg=BACKGROUND_LIGHT, padx=15, pady=15, fg=DARK_GRAY)
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Host Input
        tk.Label(config_frame, text="Host:", font=("Segoe UI", 10, "bold"), bg=BACKGROUND_LIGHT).pack(anchor=tk.W, pady=(0, 3))
        self.host_entry = tk.Entry(config_frame, font=("Segoe UI", 10), width=35, relief=tk.FLAT, bd=2)
        self.host_entry.insert(0, self.host)
        self.host_entry.pack(fill=tk.X, pady=(0, 12), ipady=5)
        
        # Port Input
        tk.Label(config_frame, text="Port:", font=("Segoe UI", 10, "bold"), bg=BACKGROUND_LIGHT).pack(anchor=tk.W, pady=(0, 3))
        self.port_entry = tk.Entry(config_frame, font=("Segoe UI", 10), width=35, relief=tk.FLAT, bd=2)
        self.port_entry.insert(0, str(self.port))
        self.port_entry.pack(fill=tk.X, pady=(0, 15), ipady=5)
        
        # Start/Stop Buttons
        button_frame = tk.Frame(config_frame, bg=BACKGROUND_LIGHT)
        button_frame.pack(fill=tk.X)
        
        self.start_button = tk.Button(button_frame, text="▶️  Start Server", command=self.start_server,
                                      bg=SIDEBAR_GREEN, fg=WHITE, font=("Segoe UI", 11, "bold"),
                                      padx=20, pady=10, cursor="hand2", relief=tk.FLAT, bd=0,
                                      activebackground=BUTTON_GREEN, activeforeground=WHITE)
        self.start_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        
        self.stop_button = tk.Button(button_frame, text="⏹️  Stop Server", command=self.stop_server,
                                     bg=RED, fg=WHITE, font=("Segoe UI", 11, "bold"),
                                     padx=20, pady=10, cursor="hand2", relief=tk.FLAT, bd=0,
                                     state=tk.DISABLED, activebackground="#D70015", activeforeground=WHITE)
        self.stop_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        
        # Exit button
        exit_server_btn = tk.Button(button_frame, text="❌ Exit", command=self.exit_server,
                                   bg="#8B0000", fg=WHITE, font=("Segoe UI", 11, "bold"),
                                   padx=20, pady=10, cursor="hand2", relief=tk.FLAT, bd=0,
                                   activebackground="#CC0000", activeforeground=WHITE)
        exit_server_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Status Frame
        status_frame = tk.LabelFrame(left_column, text="🔍 Real-Time Status", font=("Segoe UI", 11, "bold"),
                                    bg=BACKGROUND_LIGHT, padx=15, pady=15, fg=DARK_GRAY)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = tk.Label(status_frame, text="⚫ Offline", font=("Segoe UI", 14, "bold"),
                                    fg=RED, bg=BACKGROUND_LIGHT)
        self.status_label.pack(pady=5)
        
        # Stats Frame
        stats_frame = tk.Frame(status_frame, bg=BACKGROUND_LIGHT)
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.users_label = tk.Label(stats_frame, text="👥 Connected: 0", font=("Segoe UI", 10, "bold"),
                                   fg=SIDEBAR_GREEN, bg=BACKGROUND_LIGHT)
        self.users_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.messages_label = tk.Label(stats_frame, text="💬 Messages: 0", font=("Segoe UI", 10, "bold"),
                                      fg=BUTTON_GREEN, bg=BACKGROUND_LIGHT)
        self.messages_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Uptime label
        self.uptime_label = tk.Label(stats_frame, text="⏱️ Uptime: 00:00:00", font=("Segoe UI", 10, "bold"),
                                    fg=HEADER_TEAL, bg=BACKGROUND_LIGHT)
        self.uptime_label.pack(side=tk.LEFT)
        
        # Monitoring info frame
        monitor_frame = tk.Frame(status_frame, bg=BACKGROUND_LIGHT)
        monitor_frame.pack(fill=tk.X, pady=(12, 0))
        
        self.total_conn_label = tk.Label(monitor_frame, text="📊 Total Connections: 0", font=("Segoe UI", 9),
                                        fg=LIGHT_TEXT, bg=BACKGROUND_LIGHT)
        self.total_conn_label.pack(anchor=tk.W, pady=(3, 0))
        
        # Refresh button
        refresh_frame = tk.Frame(status_frame, bg=BACKGROUND_LIGHT)
        refresh_frame.pack(fill=tk.X, pady=(12, 0))
        
        refresh_btn = tk.Button(refresh_frame, text="🔄 Refresh Now", command=self.manual_refresh,
                               bg=BUTTON_GREEN, fg=WHITE, font=("Segoe UI", 9, "bold"),
                               padx=15, pady=6, cursor="hand2", relief=tk.FLAT, bd=0,
                               activebackground="#1FAF56")
        refresh_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        self.auto_refresh_status = tk.Label(refresh_frame, text="🔄 Auto-refresh: ON", font=("Segoe UI", 9, "bold"),
                                           fg=SIDEBAR_GREEN, bg=BACKGROUND_LIGHT)
        self.auto_refresh_status.pack(side=tk.LEFT)
        
        # Right column - Logs and Users
        right_column = tk.Frame(main_container, bg=WHITE)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Users List Frame
        users_frame = tk.LabelFrame(right_column, text="👨‍💼 Online Users", font=("Segoe UI", 11, "bold"),
                                   bg=BACKGROUND_LIGHT, padx=10, pady=10, fg=DARK_GRAY, height=120)
        users_frame.pack_propagate(False)
        users_frame.pack(fill=tk.BOTH, expand=False, pady=(0, 8))
        
        self.users_text = scrolledtext.ScrolledText(users_frame, font=("Segoe UI", 9),
                                                   bg=WHITE, fg=DARK_GRAY,
                                                   height=5, state=tk.DISABLED, relief=tk.FLAT, bd=0)
        self.users_text.pack(fill=tk.BOTH, expand=True)
        self.users_text.tag_configure("user", foreground=SIDEBAR_GREEN, font=("Segoe UI", 9, "bold"))
        
        # Logs Frame
        logs_frame = tk.LabelFrame(right_column, text="📋 Activity Logs", font=("Segoe UI", 11, "bold"),
                                  bg=WHITE, padx=10, pady=10, fg=DARK_GRAY)
        logs_frame.pack(fill=tk.BOTH, expand=True)
        
        self.logs_text = scrolledtext.ScrolledText(logs_frame, font=("Segoe UI", 8),
                                                   bg=WHITE, fg=DARK_GRAY,
                                                   state=tk.DISABLED, relief=tk.FLAT, bd=0)
        self.logs_text.pack(fill=tk.BOTH, expand=True)
        self.logs_text.tag_configure("info", foreground=SIDEBAR_GREEN, font=("Segoe UI", 8))
        self.logs_text.tag_configure("warning", foreground=RED, font=("Segoe UI", 8, "bold"))
        self.logs_text.tag_configure("join", foreground=SIDEBAR_GREEN, font=("Segoe UI", 8))
        self.logs_text.tag_configure("leave", foreground=RED, font=("Segoe UI", 8))
        
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Keyboard shortcuts
        self.window.bind('<F5>', lambda e: self.manual_refresh())
        self.window.bind('<Control-q>', lambda e: self.exit_server())
        
        # Start auto-monitoring
        self.start_monitoring()
        
        self.window.mainloop()
    
    def start_monitoring(self):
        """Start real-time monitoring with auto-refresh"""
        self.update_uptime()
        self.auto_refresh_status.config(text="🟢 Auto-refresh: ON")
    
    def update_uptime(self):
        """Update uptime display and refresh stats periodically"""
        if self.running and self.start_time:
            elapsed = time.time() - self.start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            uptime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.uptime_label.config(text=f"⏱️ Uptime: {uptime_str}")
        
        # Auto-refresh every 1 second
        if self.window.winfo_exists():
            self.window.after(1000, self.update_uptime)
    
    def manual_refresh(self):
        """Manual refresh of all statistics"""
        try:
            self.refresh_stats()
            messagebox.showinfo("Refresh", "✅ Server stats refreshed!")
        except:
            messagebox.showerror("Error", "Failed to refresh")
    
    def refresh_stats(self):
        """Refresh all statistics display"""
        self.update_users_display()
        self.messages_label.config(text=f"💬 Messages: {self.message_count}")
        self.total_conn_label.config(text=f"📊 Total Connections: {self.total_connections}")
    
    def log_message(self, message, tag="info"):
        # Always schedule on main thread — called from background threads
        def _log():
            try:
                self.logs_text.config(state=tk.NORMAL)
                timestamp = time.strftime("%H:%M:%S")
                self.logs_text.insert(tk.END, f"[{timestamp}] {message}\n", tag)
                self.logs_text.yview(tk.END)
                self.logs_text.config(state=tk.DISABLED)
            except:
                pass
        if self.window.winfo_exists():
            self.window.after(0, _log)
    
    def update_users_display(self):
        def _update():
            try:
                self.users_text.config(state=tk.NORMAL)
                self.users_text.delete(1.0, tk.END)
                if not self.users:
                    self.users_text.insert(tk.END, "No users connected", "user")
                else:
                    for i, username in enumerate(self.users.keys(), 1):
                        self.users_text.insert(tk.END, f"  {i}. {username}\n", "user")
                self.users_text.config(state=tk.DISABLED)
                self.users_label.config(text=f"👥 Connected: {len(self.users)}")
            except:
                pass
        if self.window.winfo_exists():
            self.window.after(0, _update)
    
    def update_message_count(self):
        self.message_count += 1
        # Schedule UI update on main thread
        if self.window.winfo_exists():
            self.window.after(0, lambda: self.messages_label.config(text=f"💬 Messages: {self.message_count}"))
    
    def start_server(self):
        """Start server"""
        try:
            try:
                self.host = self.host_entry.get().strip() or '127.0.0.1'
                self.port = int(self.port_entry.get().strip())
                if self.port < 1024 or self.port > 65535:
                    raise ValueError("Port must be between 1024 and 65535")
            except ValueError as ve:
                messagebox.showerror("Invalid Input", f"Configuration error: {str(ve)}")
                return
            
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            
            self.running = True
            self.start_time = time.time()
            self.status_label.config(text="🟢 Online", fg=BUTTON_GREEN)
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.host_entry.config(state=tk.DISABLED)
            self.port_entry.config(state=tk.DISABLED)
            
            self.log_message(f"✅ Server started on {self.host}:{self.port}", "join")
            
            receive_thread = threading.Thread(target=self.receive, daemon=True)
            receive_thread.start()
        except OSError as oe:
            messagebox.showerror("Error", f"Failed to bind to port: {str(oe)}")
            self.running = False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start server: {str(e)}")
            self.running = False
            self.log_message(f"❌ Error: {str(e)}", "warning")
    
    def stop_server(self):
        self.running = False
        if self.server:
            try:
                self.server.close()
            except:
                pass
        self.status_label.config(text="⚫ Offline", fg=RED)
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.host_entry.config(state=tk.NORMAL)
        self.port_entry.config(state=tk.NORMAL)
        self.log_message("🛑 Server stopped")
    
    def broadcast(self, message, exclude_user=None):
        """Broadcast message to all users"""
        with self.lock:
            targets = [(u, s) for u, s in self.users.items() if u != exclude_user]
        for username, sock in targets:
            try:
                sock.sendall(message + b'\n')
            except:
                pass

    def broadcast_users_list(self):
        """Send updated user list to all connected clients"""
        with self.lock:
            users_str = ",".join(self.users.keys())
            targets = list(self.users.values())
        message = f"USER_LIST:{users_str}\n".encode('utf-8')
        for sock in targets:
            try:
                sock.sendall(message)
            except:
                pass

    def send_to_user(self, recipient_username, message, recipient_socket=None):
        """Send private message to specific user.
        If recipient_socket is provided, use it directly (avoids lock re-entry).
        """
        try:
            sock = recipient_socket
            if sock is None:
                with self.lock:
                    sock = self.users.get(recipient_username)
            if sock is None:
                print(f"[SERVER] ❌ User {recipient_username} not found")
                return False
            sock.sendall(message + b'\n')
            print(f"[SERVER] ✅ Sent to {recipient_username}: {message.decode('utf-8')[:50]}")
            self.log_message(f"✉️ Sent to {recipient_username}: {message.decode('utf-8')[:30]}", "info")
            return True
        except Exception as e:
            print(f"[SERVER ERROR] send_to_user({recipient_username}): {e}")
            self.log_message(f"❌ Failed to send to {recipient_username}: {e}", "warning")
            return False
    
    def handle(self, client, username):
        """Handle client messages with private messaging support"""
        print(f"[HANDLE] Started handling {username}")

        while self.running:
            try:
                message = client.recv(4096)
                if not message:
                    print(f"[HANDLE] {username} disconnected (empty message)")
                    break

                self.update_message_count()
                message_str = message.decode('utf-8').strip()
                print(f"[HANDLE] {username} sent: {message_str[:80]}")

                if message_str.startswith('@'):
                    parts = message_str[1:].split(' ', 1)
                    if len(parts) == 2:
                        target_user = parts[0].strip()
                        private_msg = parts[1].strip()
                        formatted_msg = f"{username}->{target_user}:{private_msg}".encode('utf-8')

                        # Grab both sockets under lock, send outside lock — avoids deadlock
                        with self.lock:
                            recipient_sock = self.users.get(target_user)
                            sender_sock = self.users.get(username)

                        if recipient_sock:
                            try:
                                recipient_sock.sendall(formatted_msg + b'\n')
                                print(f"[HANDLE] ✅ Delivered to {target_user}")
                            except Exception as e:
                                print(f"[HANDLE] ❌ Failed to deliver to {target_user}: {e}")

                            try:
                                sender_sock.sendall(formatted_msg + b'\n')
                                print(f"[HANDLE] ✅ Echo sent to {username}")
                            except Exception as e:
                                print(f"[HANDLE] ❌ Failed to echo to {username}: {e}")

                            self.log_message(f"💬 {username} → {target_user}: {private_msg[:30]}", "info")
                        else:
                            print(f"[HANDLE] ❌ User {target_user} not found")
                            error_msg = f"ERROR->SERVER:User '{target_user}' not found!\n".encode('utf-8')
                            try:
                                client.sendall(error_msg)
                            except:
                                pass
                            self.log_message(f"❌ {username} → unknown '{target_user}'", "warning")
                    else:
                        try:
                            client.sendall(f"ERROR->SERVER:Use format @username message\n".encode('utf-8'))
                        except:
                            pass

                self.broadcast_users_list()

            except Exception as e:
                print(f"[HANDLE] Error for {username}: {e}")
                break

        # Disconnection cleanup
        try:
            with self.lock:
                if username in self.users:
                    del self.users[username]
            self.log_message(f"👤 {username} left the chat", "leave")
            self.update_users_display()
            self.broadcast_users_list()
            client.close()
        except:
            pass
    
    def receive(self):
        """Accept incoming client connections"""
        while self.running:
            try:
                client, address = self.server.accept()
                self.total_connections += 1  # Increment connection counter
                self.log_message(f"🔗 Connection from {str(address)}", "info")
                
                # Set timeout for nickname handshake
                client.settimeout(10)
                
                try:
                    # Receive username from client
                    username_data = client.recv(1024).decode('utf-8').strip()
                    
                    if not username_data:
                        client.close()
                        continue
                    
                    username = username_data
                    
                    # Check if username already exists
                    with self.lock:
                        if username in self.users:
                            error_msg = "ERROR->SERVER:Username already taken!\n".encode('utf-8')
                            client.sendall(error_msg)
                            client.close()
                            self.log_message(f"❌ Duplicate username: {username}", "warning")
                            continue
                
                except socket.timeout:
                    self.log_message(f"❌ Username timeout from {str(address)}", "warning")
                    client.close()
                    continue
                
                # Reset timeout for normal communication
                client.settimeout(None)
                
                # Add user to dictionary
                with self.lock:
                    self.users[username] = client
                
                # Notify everyone
                self.log_message(f"✅ {username} joined the chat", "join")
                join_msg = f"SYSTEM->SERVER:{username} joined the chat!".encode('utf-8')
                self.broadcast(join_msg)
                
                self.update_users_display()
                # CRITICAL: Broadcast updated user list to ALL clients (including new user)
                self.broadcast_users_list()
                
                # Start handling this client's messages
                thread = threading.Thread(target=self.handle, args=(client, username), daemon=True)
                thread.start()
            except Exception as e:
                if self.running:
                    self.log_message(f"❌ Server error: {str(e)}", "warning")
    
    def exit_server(self):
        """Exit server application with confirmation"""
        if self.running:
            if messagebox.askyesno("Exit Server", "Stop server and exit?"):
                self.stop_server()
                self.on_closing()
        else:
            if messagebox.askyesno("Exit Server", "Exit application?"):
                self.on_closing()
    
    def on_closing(self):
        try:
            if self.running:
                self.stop_server()
            if self.window:
                self.window.destroy()
        except:
            pass

if __name__ == "__main__":
    server = ChatServer()
    server.start_gui()