# 🚀 Quick Start Guide

Get ChatBox running in **5 minutes**!

## Prerequisites
- Python 3.6+
- Windows, Mac, or Linux

## Step 1: Start the Server

Open **Command Prompt** or **PowerShell** and run:

```bash
python server.py
```

You should see the Server Control GUI appear with a blue header saying "ChatBox Server Control".

Click the **"▶️ Start Server"** button.

You should see:
- Status changes to **"🟢 Online"** (green)
- Log shows: **"✅ Server started on 127.0.0.1:5555"**

✅ **Server is now running!**

---

## Step 2: Start First Client

Open a **NEW Command Prompt** (keep server running) and run:

```bash
python client.py
```

You should see the ChatBox login screen.

Fill in:
- **Username**: `Alice`
- **Server IP**: `127.0.0.1` (already filled)
- **Port**: `5555` (already filled)

Click **"🚀 CONNECT"** button.

You should see the main chat screen with sidebar and empty chat area.

✅ **First client connected!**

---

## Step 3: Start Second Client

Open a **THIRD Command Prompt** and run:

```bash
python client.py
```

Fill in:
- **Username**: `Bob`
- **Server IP**: `127.0.0.1`
- **Port**: `5555`

Click **"🚀 CONNECT"** button.

You should see the main chat screen.

---

## Step 4: Send Your First Message

**In Alice's window:**
1. Click on **"● Bob"** in the left sidebar
2. Type message: `"Hi Bob! How are you?"`
3. Click **"Send"** button OR press **Enter** key

✅ **Message appears in your chat as a green bubble on the right!**

---

## Step 5: Receive Message

**In Bob's window:**
1. Look at the left sidebar
2. You should see **"● Alice"** (click it if not already selected)
3. You should see Alice's message in a **white bubble on the left**

✅ **Bob received the message!**

---

## Step 6: Reply Back

**In Bob's window:**
1. Type: `"I'm doing great! Thanks for asking!"`
2. Press **Enter** key

**In Alice's window:**
- Alice should immediately see Bob's reply in a white bubble

✅ **Two-way messaging works!**

---

## 🎯 Key Features to Try

### Message History
- Click on a user in sidebar
- See all messages with that user in order

### Multiple Conversations
- Open 3rd client (Charlie)
- Send messages to different users
- Notice each conversation is separate

### Unread Messages
- Have Bob send a message while Alice is chatting with Charlie
- Notice Alice's sidebar shows: `● Bob (1)` with unread count
- Click Bob to read and counter resets

### Server Features
- Watch the server window
- See user joins: ✅ Green text
- See messages: 💬 Message count increases
- See "Connected: 2" indicator

---

## ⌨️ Keyboard Shortcuts

| Action | How |
|--------|-----|
| Send Message | Press **Enter** key |
| Select User | Click username in sidebar |
| Connect | Press **Enter** in Port field |
| Disconnect | Click **"🔌 Disconnect"** button |

---

## ⚙️ Configuration Tips

### Change Server Port
1. In server.py login screen, change port in "🔌 Port" field
2. Must match in client connection
3. Some ports like 80, 443 may require admin privileges

### Use Different IP
1. If connecting from different machine:
   - Find server machine IP: `ipconfig` (Windows)
   - In client, enter that IP instead of 127.0.0.1

### Multiple Servers
1. Each server must run on different port
2. Example: 5555, 5556, 5557

---

## 🐛 Troubleshooting

### "Connection refused" error
- ❌ Server not running
- ✅ Click "Start Server" in server window

### Button not visible
- ❌ Window too small
- ✅ Maximize window or resize

### Messages not appearing
- ❌ Didn't select recipient in sidebar
- ✅ Click on username first

### Port already in use
- ❌ Another program using port 5555
- ✅ Try different port or close other app

### "Username already taken"
- ❌ Another client has same username
- ✅ Connect with different username

---

## 📊 Architecture Overview

```
Terminal 1              Terminal 2              Terminal 3
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  Server.py   │      │ Alice Client │      │  Bob Client  │
│              │      │              │      │              │
│ socket port  │      │ socket port  │      │ socket port  │
│  5555        │◄────►│  12345       │      │  12346       │
│              │      │              │      │              │
│ User Dict    │      │ Chat UI      │      │ Chat UI      │
│ alice->sock  │      │              │      │              │
│ bob->sock    │◄────►│ alice router │      │              │
│              │      │ message->bob │      │              │
└──────────────┘      └──────────────┘      └──────────────┘
```

---

## ✅ Success Checklist

- [ ] Server window shows "🟢 Online"
- [ ] Both clients show usernames in header
- [ ] Users visible in each other's sidebar
- [ ] Send message from Alice → appears as green bubble
- [ ] Receive message in Bob → appears as white bubble
- [ ] Reply from Bob → appears in Alice's chat
- [ ] Server shows message count increasing
- [ ] No error messages in either terminal

If all checked ✅ you're ready to chat!

---

## 📞 Getting Help

Check these files:
- `README.md` - Full feature documentation
- `TESTING_GUIDE.md` - Detailed test instructions
- `server.py` - Server source code with comments
- `client.py` - Client source code with comments

---

**Enjoy chatting!** 🎉

Made with ❤️ for socket programming
