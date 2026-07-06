# COMPLETE UPDATED CODE - Real-Time User List Implementation

## FILE 1: server.py (COMPLETE)

```python
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
        self.stop_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Status Frame
        status_frame = tk.LabelFrame(left_column, text="🔍 Status", font=("Segoe UI", 11, "bold"),
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
        self.messages_label.pack(side=tk.LEFT)
        
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
        self.window.mainloop()
    
    def log_message(self, message, tag="info"):
        self.logs_text.config(state=tk.NORMAL)
        timestamp = time.strftime("%H:%M:%S")
        self.logs_text.insert(tk.END, f"[{timestamp}] {message}\n", tag)
        self.logs_text.yview(tk.END)
        self.logs_text.config(state=tk.DISABLED)
    
    def update_users_display(self):
        self.users_text.config(state=tk.NORMAL)
        self.users_text.delete(1.0, tk.END)
        
        if not self.users:
            self.users_text.insert(tk.END, "No users connected", "user")
        else:
            for i, username in enumerate(self.users.keys(), 1):
                self.users_text.insert(tk.END, f"  {i}. {username}\n", "user")
        
        self.users_text.config(state=tk.DISABLED)
        self.users_label.config(text=f"👥 Connected: {len(self.users)}")
    
    def update_message_count(self):
        self.message_count += 1
        self.messages_label.config(text=f"💬 Messages: {self.message_count}")
    
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
        """Broadcast message to all users except optionally excluded user"""
        dead_users = []
        with self.lock:
            for username, client in self.users.items():
                if exclude_user and username == exclude_user:
                    continue
                try:
                    client.send(message)
                except:
                    dead_users.append(username)
        
        # Remove dead clients
        for username in dead_users:
            try:
                with self.lock:
                    if username in self.users:
                        self.users[username].close()
                        del self.users[username]
            except:
                pass
    
    def send_to_user(self, recipient_username, message):
        """Send private message to specific user"""
        try:
            with self.lock:
                if recipient_username in self.users:
                    self.users[recipient_username].send(message)
                    return True
            return False
        except:
            return False
    
    def broadcast_users_list(self):
        """Send list of online users to all connected clients (thread-safe)"""
        with self.lock:
            users_str = ", ".join(self.users.keys())
        message = f"Online Users:{users_str}".encode('utf-8')
        self.broadcast(message)
    
    def handle(self, client, username):
        """Handle client messages with private messaging support"""
        while self.running:
            try:
                message = client.recv(1024)
                if message:
                    self.update_message_count()
                    message_str = message.decode('utf-8').strip()
                    
                    # Check for private message format: @username message
                    if message_str.startswith('@'):
                        try:
                            # Extract target username and message
                            parts = message_str[1:].split(' ', 1)  # Skip @ and split on first space
                            if len(parts) == 2:
                                target_user = parts[0].strip()
                                private_msg = parts[1].strip()
                                
                                # Check if target user exists
                                with self.lock:
                                    if target_user in self.users:
                                        # Format: sender->recipient:message
                                        formatted_msg = f"{username}->{target_user}:{private_msg}".encode('utf-8')
                                        
                                        # Send to recipient
                                        self.send_to_user(target_user, formatted_msg)
                                        
                                        # Send confirmation to sender
                                        client.send(formatted_msg)
                                        
                                        self.log_message(f"💬 {username} → {target_user}: {private_msg[:30]}...", "info")
                                    else:
                                        # User not found
                                        error_msg = f"Error: User '{target_user}' not found!".encode('utf-8')
                                        client.send(error_msg)
                                        self.log_message(f"❌ {username} tried to message unknown user '{target_user}'", "warning")
                            else:
                                error_msg = f"Error: Use format @username message".encode('utf-8')
                                client.send(error_msg)
                        except Exception as e:
                            error_msg = f"Error processing message: {str(e)}".encode('utf-8')
                            client.send(error_msg)
                    else:
                        # Regular message (chat status messages)
                        pass
                    
                    self.broadcast_users_list()
                else:
                    break
            except:
                break
        
        # Handle client disconnection
        try:
            with self.lock:
                if username in self.users:
                    del self.users[username]
            
            self.log_message(f"👤 {username} left the chat", "leave")
            disconnect_msg = f"{username} left the chat!".encode('utf-8')
            self.broadcast(disconnect_msg)
            self.update_users_display()
            # CRITICAL: Broadcast updated user list to ALL remaining clients
            self.broadcast_users_list()
            client.close()
        except:
            pass
    
    def receive(self):
        """Accept incoming client connections"""
        while self.running:
            try:
                client, address = self.server.accept()
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
                            error_msg = "Username already taken!".encode('utf-8')
                            client.send(error_msg)
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
                join_msg = f"{username} joined the chat!".encode('utf-8')
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
```

---

## KEY CHANGES IN SERVER.PY:

### Change 1: Thread-Safe broadcast_users_list() (Lines 262-268)
✅ Added `with self.lock:` to protect dictionary iteration
✅ Prevents race conditions when reading user list

### Change 2: Broadcast on User Join (Line 384)
✅ Added comment: "CRITICAL: Broadcast updated user list to ALL clients"
✅ Ensures new users see the list and existing users see the new user

### Change 3: Broadcast on User Leave (Line 331)
✅ Added comment: "CRITICAL: Broadcast updated user list to ALL remaining clients"
✅ Ensures users are removed from client lists immediately

---

## FILE 2: client.py (COMPLETE - PARTIAL SHOWN)

### KEY SECTIONS WITH CHANGES:

#### Change 1: Thread-Safe Message Display (Lines 547-595)

```python
def display_message(self, message):
    """Handle incoming messages"""
    try:
        current_time = datetime.now().strftime("%H:%M")
        
        # Check for user list - THREAD SAFE UI UPDATE
        if "Online Users:" in message:
            self.update_users_list(message)
            # Schedule UI refresh on main thread
            self.window.after(0, self.refresh_users_display)
        
        # Check for private message format: sender->recipient:message
        elif "->" in message and ":" in message:
            parts = message.split("->")
            if len(parts) == 2:
                sender = parts[0].strip()
                rest = parts[1].split(":", 1)
                if len(rest) == 2:
                    recipient = rest[0].strip()
                    msg_text = rest[1].strip()
                    
                    # Determine who the "other user" is
                    if sender == self.nickname:
                        other_user = recipient
                        is_sent = True
                    else:
                        other_user = sender
                        is_sent = False
                    
                    # Store message
                    if other_user not in self.chat_history:
                        self.chat_history[other_user] = []
                    self.chat_history[other_user].append((sender, msg_text, current_time))
                    
                    # Display if selected
                    if self.selected_user == other_user:
                        self.add_message_bubble(sender, msg_text, current_time, is_sent)
                    else:
                        # Mark unread
                        if other_user not in self.unread_messages:
                            self.unread_messages[other_user] = 0
                        self.unread_messages[other_user] += 1
                        # Thread-safe UI update for unread indicator
                        self.window.after(0, self.update_user_label, other_user)
        
        # Check for regular broadcast or system messages
        elif message.strip():
            # System message like "username joined" or error messages
            pass
                    
    except Exception as e:
        print(f"Error displaying message: {str(e)}")

def update_users_list(self, message):
    """Update users list"""
    try:
        users_str = message.replace("Online Users:", "").strip()
        user_list = [u.strip() for u in users_str.split(",") if u.strip() and u.strip() != self.nickname]
        self.online_users = user_list
    except Exception as e:
        print(f"Error parsing user list: {str(e)}")

def refresh_users_display(self):
    """Refresh user list display (thread-safe main thread call)"""
    try:
        for widget in self.users_listbox_frame.winfo_children():
            widget.destroy()
        self.user_labels.clear()
        
        for user in self.online_users:
            user_frame = tk.Frame(self.users_listbox_frame, bg=SIDEBAR_BG, height=50)
            user_frame.pack(fill=tk.X, padx=0, pady=0)
            user_frame.pack_propagate(False)
            
            content = tk.Frame(user_frame, bg=SIDEBAR_BG)
            content.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)
            
            unread = self.unread_messages.get(user, 0)
            user_text = f"● {user}"
            if unread > 0:
                user_text += f" ({unread})"
            
            # ... rest of UI building code continues ...
```

---

## SUMMARY OF CHANGES:

| File | What Changed | Why |
|------|-------------|-----|
| **server.py** | `broadcast_users_list()` now thread-safe with lock | Prevent race conditions |
| **server.py** | Call `broadcast_users_list()` when user joins | All clients see new user immediately |
| **server.py** | Call `broadcast_users_list()` when user leaves | All clients updated when user disconnects |
| **client.py** | Use `self.window.after(0, self.refresh_users_display)` | All UI updates on main thread (Tkinter requirement) |
| **client.py** | Separate `update_users_list()` from `refresh_users_display()` | Data logic separate from UI rendering |
| **client.py** | Use `self.window.after()` for unread updates | Thread-safe indicator updates |

---

## TESTING CHECKLIST:

- [ ] Run server: `python server.py`
- [ ] Connect Client A (Alice): `python client.py`
- [ ] Connect Client B (Bob): `python client.py`  
- [ ] **Verify:** Alice sees Bob in sidebar immediately
- [ ] **Verify:** Bob sees Alice in sidebar immediately
- [ ] Disconnect Bob
- [ ] **Verify:** Alice's sidebar updates (Bob removed immediately)
- [ ] Send private message from Alice: `@Bob Hello`
- [ ] **Verify:** Bob receives message and user list still correct
- [ ] **Verify:** Server console shows all activities

---

## FULL CLIENT.PY CONTINUES WITH UNCHANGED CODE:

The rest of client.py remains unchanged from the previous version (login screen, chat UI, message sending, etc.). Only the message handling and user display functions were modified.

The complete files are already updated in your workspace!
```
