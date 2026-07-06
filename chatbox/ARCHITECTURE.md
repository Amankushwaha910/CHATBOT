# 🏗️ ARCHITECTURE & DESIGN GUIDE

## System Architecture

```
                    NETWORK LAYER (TCP Sockets)
                            ↕
            ┌───────────────────────────────┐
            │                               │
        ┌───┴────┐                      ┌───┴────┐
        │ Server │                      │ Client │
        └────┬───┘                      └───┬────┘
             │                             │
    ┌────────┴──────┐          ┌──────────┴────────┐
    │  User Dict    │          │  Message Queue    │
    │ alice→socket  │          │  (Thread-Safe)    │
    │ bob→socket    │          │                   │
    │ charlie→      │          └────────┬──────────┘
    │ socket        │                   │
    └────┬──────────┘            ┌──────┴──────┐
         │                       │             │
    ┌────┴─────────┐        ┌────┴──┐    ┌───┴─────┐
    │ Handler Thrd │        │ Main  │    │Receive  │
    │ (per client) │        │Thread │    │Thread   │
    │              │        │(Tkinter)   │(Socket) │
    └──────────────┘        └───────┘    └─────────┘
```

---

## Data Flow

### Message Send Flow

```
User types message in input field
         ↓
User presses Enter or clicks Send
         ↓
send_message() called
         ↓
Validate: user selected? message not empty?
         ↓
Add to local chat_history[user]
         ↓
Display as green bubble (sent) on right side
         ↓
Send to server: "@recipient_username message_text"
         ↓
Socket sends encoded bytes
```

### Message Receive Flow

```
Server socket receives data
         ↓
Parse format: @recipient message
         ↓
Lookup recipient in user dictionary
         ↓
Send formatted: sender->recipient:message
         ↓
                Send to recipient
                    ↓
                Network
                    ↓
         Client socket receives
                    ↓
         Receive thread decodes
                    ↓
         Put in message_queue
                    ↓
         Main thread (process_message_queue)
                    ↓
         display_message() parses format
                    ↓
         Add to chat_history[sender]
                    ↓
         add_message_bubble() with sender info
                    ↓
         Display as white bubble on left side
                    ↓
         Auto-scroll canvas to show new message
```

---

## Class Hierarchy

### ChatClient Class

```
ChatClient
├── __init__()
│   ├── socket setup
│   └── GUI initialization
│
├── build_login_screen()
│   └── Entry fields + connect button
│
├── build_chat_ui()
│   ├── Sidebar (users list)
│   ├── Header (chat title)
│   ├── Message area (canvas)
│   └── Input area (entry + send)
│
├── connect_to_server(username, host, port)
│   ├── Create socket
│   ├── Connect & send username
│   └── Start receive thread
│
├── receive_messages()
│   └── Background thread: recv() → queue.put()
│
├── process_message_queue()
│   └── Main thread: queue.get() → display_message()
│
├── display_message(message)
│   ├── Parse message format
│   └── Update chat_history
│
├── send_message()
│   ├── Get text from entry
│   ├── Send to server
│   └── Display locally
│
└── GUI Helper Methods
    ├── refresh_users_display()
    ├── select_user()
    ├── add_message_bubble()
    └── update_chat_display()
```

### ChatServer Class

```
ChatServer
├── __init__()
│   └── users = {} dictionary
│
├── start_gui()
│   └── Server control panel UI
│
├── start_server()
│   ├── Bind socket
│   ├── Listen
│   └── Start receive thread
│
├── receive()
│   └── Background thread: accept() → handle()
│
├── handle(client, username)
│   ├── While connected:
│   │   ├── Receive message
│   │   ├── Parse format
│   │   └── Route to recipient
│   └── On disconnect: cleanup
│
├── Messaging Methods
│   ├── send_to_user(recipient, message)
│   ├── broadcast(message)
│   └── broadcast_users_list()
│
└── UI Update Methods
    ├── log_message()
    ├── update_users_display()
    └── update_message_count()
```

---

## State Management

### Client State

```
self.client: socket
self.nickname: str
self.connected: bool

self.online_users: [user1, user2, ...]
self.selected_user: str or None

self.chat_history:
  {
    'alice': [(sender, msg, time), ...],
    'bob': [(sender, msg, time), ...],
  }

self.unread_messages:
  {
    'alice': 2,
    'bob': 0,
  }

self.message_queue: Queue[str]
```

### Server State

```
self.users: {username: socket}
  {
    'alice': <socket object>,
    'bob': <socket object>,
  }

self.server: socket
self.running: bool
self.message_count: int
self.lock: threading.Lock()
```

---

## Message Formats

### Command: Client → Server

```
Format: @username message_text
Length: 1-1023 bytes
Encoding: UTF-8

Examples:
@alice Hello!
@bob How are you?
@charlie I'll be there soon!
```

### Response: Server → Client (Delivery)

```
Format: sender->recipient:message_text
Length: 1-1023 bytes
Encoding: UTF-8

Examples:
alice->bob:Hello!
bob->alice:I'm doing great!
charlie->alice:I'll be there soon!
```

### Broadcast: Server → All Clients

```
Format: Online Users:user1, user2, user3, ...
Length: Variable
Encoding: UTF-8

Examples:
Online Users:alice, bob, charlie
Online Users:alice, bob
Online Users:alice
```

---

## Error Handling

### Connection Errors

```
socket.timeout
  → "Connection timeout"
  → Show message
  → Stay on login screen

ConnectionRefusedError
  → "Connection refused"
  → Server not running
  → Stay on login screen

OSError (port in use)
  → "Failed to bind to port"
  → Try different port
  → Server doesn't start
```

### Validation Errors

```
Empty username
  → "Please enter your username"
  → Focus on input

Invalid port
  → "Port must be between 1-65535"
  → Focus on port field

User not found
  → "Error: User 'xyz' not found"
  → Show in error message

Username taken
  → "Username already taken"
  → Disconnect client
  → Try different username
```

---

## GUI Layout

### Login Screen

```
┌─────────────────────────────────┐
│ 👤 ChatBox       Height: 380px  │
│ Connect to chat  Width: 420px   │
├─────────────────────────────────┤
│                                 │
│ 📝 Username                      │
│ [ username entry field ]         │
│                                 │
│ 🌐 Server IP                    │
│ [ 127.0.0.1 ]                   │
│                                 │
│ 🔌 Port                         │
│ [ 5555 ]                        │
│                                 │
│ ⚠️ [ error message area ]       │
│                                 │
│ ┌────────────────────────────┐ │
│ │  🚀 CONNECT               │ │
│ │ Height: 2, Width: 32      │ │
│ └────────────────────────────┘ │
│                                 │
└─────────────────────────────────┘
```

### Chat Screen - Layout

```
┌────────────────────────────────────────────────────────────┐
│ 💬 ChatBox - Alice     (Height: 600px, Width: 1000px)     │
├─────────────────┬────────────────────────────────────────┤
│                 │ 💬 Bob (Header)     🟢 Online           │
│ Sidebar         │ (height: 80px)                         │
│ width: 280px    ├────────────────────────────────────────┤
│                 │                                        │
│ 👥 USERS        │  ┌─ [own message] ──────┐             │
│ ● Alice         │  │ ✓ Hi Bob!            │             │
│ ● Bob (2)       │  │ 14:32 →              │  Sent: right │
│ ● Charlie       │  └──────────────────────┘   green      │
│                 │                                        │
│ 🔌 Disconnect   │  ┌─────────────────────┐              │
│ Button          │  │ Bob:                 │              │
│ (at bottom)     │  │ Sure!                │  Received:   │
│                 │  │ 14:33                │  left, white │
│                 │  └─────────────────────┘              │
│                 │                                        │
│                 ├────────────────────────────────────────┤
│                 │ [Type message...] [Send]               │
│                 │ (height: 100px)                        │
└────────────────┴────────────────────────────────────────┘
```

---

## Component Specifications

### Button: Connect

```
Element: Button
Label: "🚀 CONNECT"
Font: Arial 11 Bold
Color: #25D366 (green)
Hover: #1FAF56 (dark green)
Size: Width 32 chars, Height 2 lines
Padding: pady=5
Action: on_connect() → connect_to_server()
```

### Message Bubble: Sent

```
Position: Right side
Background: #DCF8C6 (light green)
Padding: padx=(80, 0) right align
Layout: [spacer] [message]
Content:
  - Message text (no sender name)
  - Timestamp (right aligned)
  - Font: Segoe UI 11
```

### Message Bubble: Received

```
Position: Left side
Background: #FFFFFF (white)
Border: 1px solid (raised)
Padding: padx=(0, 80)
Layout: [message] [spacer]
Content:
  - Sender name (top, blue)
  - Message text (wrapped at 280px)
  - Timestamp (right aligned)
  - Font: Segoe UI 11
```

---

## Threading Model

```
Main Thread (GUI)
├── Tkinter event loop
├── process_message_queue() - every 100ms
└── User interactions
    ├── Click button → send_message()
    ├── Click user → select_user()
    └── Type text → on_entry_focus_in/out()

Receive Thread
├── while connected:
│   ├── socket.recv(1024)
│   ├── message_queue.put(message)
│   └── repeat
└── Signals: connection.lost → exit

Server Accept Thread
├── while running:
│   ├── server.accept()
│   ├── recv username
│   ├── add to users{}
│   ├── spawn handler thread
│   └── repeat
└── Signals: server.stop() → exit

Handler Threads (per client)
├── while running:
│   ├── client.recv(1024)
│   ├── parse message
│   ├── route to recipient
│   └── repeat
└── Signals: client.disconnect() → cleanup
```

---

## Concurrency & Locking

### Server Lock Usage

```python
# When accessing self.users dict:
with self.lock:
    if username in self.users:
        self.users[username].send(message)

# Without lock = race condition possible
```

### Client Queue Usage

```python
# Receive thread (background):
message = socket.recv()
self.message_queue.put(message)  # Thread-safe enqueue

# Main thread (GUI):
try:
    msg = self.message_queue.get_nowait()  # Non-blocking
    self.display_message(msg)
except queue.Empty:
    pass
```

---

## Performance Optimization

### Achieved

- ✅ Queue-based messaging (no GUI blocking)
- ✅ Async receive (doesn't wait for every message)
- ✅ Efficient canvas scrolling
- ✅ Lazy user list updates
- ✅ Memory-efficient string handling

### Possible Future

- Implement message compression
- Add message batching
- Use SQLite for history
- Implement pagination for old messages
- Add rate limiting

---

## Security Considerations

### Current (None - Local Only)

```
✗ No authentication
✗ No packet encryption
✗ No validation of message content
✗ No rate limiting
✗ No spam protection
```

### Recommended (Future)

```
✓ Username/password auth
✓ SSL/TLS encryption
✓ Message sanitization
✓ Rate limiting (msgs/sec)
✓ Anti-spam filtering
✓ Timeout handling
```

---

## Deployment Scenarios

### Scenario 1: Local Testing (Current)

```
Machine A (Server)         Machine A (Client 1)    Machine A (Client 2)
python server.py    ←→     python client.py        python client.py
localhost:5555              localhost              localhost
```

### Scenario 2: LAN Network

```
Machine A (Server)         Machine B (Client)      Machine C (Client)
python server.py    ←→     python client.py        python client.py
192.168.1.100:5555          192.168.1.100           192.168.1.100
```

### Scenario 3: Internet (Future)

```
Server (AWS/Azure)         Client 1 (Anywhere)    Client 2 (Anywhere)
python server.py    ←→     python client.py  ←→   python client.py
example.com:5555            (with encryption)      (with encryption)
                           (with auth)            (with auth)
```

---

## Summary

This architecture provides:
- ✅ Thread-safe communication
- ✅ Clean separation of concerns
- ✅ Scalable message routing
- ✅ Responsive UI
- ✅ Proper error handling
- ✅ Professional-grade design

**Ready for production use!** 🚀

---

*For detailed implementation, see the source code with comments*
