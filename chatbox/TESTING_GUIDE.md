# 🧪 ChatBox Testing Guide

Complete testing checklist to verify all fixes are working.

## ✅ Test 1: CONNECT BUTTON VISIBILITY

**Objective**: Verify Connect button is clearly visible and properly sized

**Steps**:
1. Run `python client.py`
2. Observe the login screen
3. Look for "🚀 CONNECT" button

**Expected Result**:
- ✅ Button is clearly visible below Port field
- ✅ Button is large with good height (approximately 2x normal button)
- ✅ Button shows green color (#25D366)
- ✅ Button spans full width with padding on sides
- ✅ Button has white text in Arial 11 bold

**Status**: Pass / Fail: ___________

---

## ✅ Test 2: CONNECTION WORKS

**Objective**: Verify client can connect to server

**Steps**:
1. Open terminal 1 and run: `python server.py`
2. Wait 2 seconds for server to initialize
3. Click "Start Server" button
4. In server logs, verify "✅ Server started on 127.0.0.1:5555"
5. Open terminal 2 and run: `python client.py`
6. Enter username: "TestUser1"
7. Enter IP: "127.0.0.1"
8. Enter Port: "5555"
9. Click "CONNECT"

**Expected Result**:
- ✅ No error message appears
- ✅ Chat UI appears (sidebar with users + chat area)
- ✅ Server logs show "✅ TestUser1 joined the chat"
- ✅ Window title changes to "💬 ChatBox - TestUser1"

**Status**: Pass / Fail: ___________

---

## ✅ Test 3: MULTIPLE USERS CONNECT

**Objective**: Verify multiple clients can connect simultaneously

**Steps**:
1. Open terminal 3 and run: `python client.py`
2. Enter username: "TestUser2"
3. Enter IP: "127.0.0.1"
4. Enter Port: "5555"
5. Click "CONNECT"
6. Look at sidebar in both clients

**Expected Result**:
- ✅ Both clients connect without error
- ✅ TestUser1 sees "● TestUser2" in sidebar
- ✅ TestUser2 sees "● TestUser1" in sidebar
- ✅ Server logs show both users connected
- ✅ Server displays "👥 Connected: 2"

**Status**: Pass / Fail: ___________

---

## ✅ Test 4: MESSAGE RECEIVED INSTANTLY

**Objective**: Verify messages appear immediately when received

**Steps**:
1. In TestUser1 client, click on "● TestUser2" in sidebar
2. Chat header should show "💬 TestUser2"
3. Type message: "Hello TestUser2!"
4. Click Send button OR press Enter

**Expected Result**:
- ✅ Message appears immediately in green bubble on right side
- ✅ Message shows timestamp (HH:MM format)
- ✅ Input field clears
- ✅ Chat auto-scrolls to show new message

**Status**: Pass / Fail: ___________

---

## ✅ Test 5: MESSAGE RECEIVED BY OTHER USER

**Objective**: Verify recipient sees the message instantly

**Steps**:
1. In TestUser2 client, look for messages
2. If TestUser2 hasn't selected TestUser1 yet, click "● TestUser1" in sidebar

**Expected Result**:
- ✅ TestUser2 sees the message "Hello TestUser2!" in white bubble on left side
- ✅ Message shows sender name "TestUser1" above the bubble
- ✅ Message shows timestamp
- ✅ Message appears without delay (instant)

**Status**: Pass / Fail: ___________

---

## ✅ Test 6: TWO-WAY MESSAGES

**Objective**: Verify both users can send and receive messages

**Steps**:
1. In TestUser2 client, with TestUser1 selected
2. Type: "Hi TestUser1! How are you?"
3. Click Send or press Enter
4. Switch to TestUser1 client
5. Look for message from TestUser2

**Expected Result**:
- ✅ TestUser2's message appears in green bubble (sent) on right side
- ✅ TestUser1 instantly sees it in white bubble (received) on left side
- ✅ No delays or missing messages
- ✅ Both show sender/timestamp info

**Status**: Pass / Fail: ___________

---

## ✅ Test 7: MESSAGE HISTORY

**Objective**: Verify conversation history is maintained

**Steps**:
1. In TestUser1 client, click on "● TestUser2" again
2. Review all previous messages in order

**Expected Result**:
- ✅ All messages are shown in conversation history
- ✅ Messages are in chronological order
- ✅ Sent messages on right (green), received on left (white)
- ✅ All timestamps and sender names visible

**Status**: Pass / Fail: ___________

---

## ✅ Test 8: MULTIPLE CONVERSATIONS

**Objective**: Verify separate chat history per user

**Steps**:
1. In TestUser1 client, add TestUser3 (open new terminal, run client)
2. Connect TestUser3 to server
3. From TestUser1, send message to TestUser3
4. Switch back to TestUser2 chat
5. Switch back to TestUser3 chat

**Expected Result**:
- ✅ Each user has separate message history
- ✅ TestUser2 chat doesn't show messages intended for TestUser3
- ✅ TestUser3 chat shows only messages from TestUser1 to TestUser3
- ✅ No message mixing between conversations

**Status**: Pass / Fail: ___________

---

## ✅ Test 9: UNREAD MESSAGE INDICATORS

**Objective**: Verify unread message counter works

**Steps**:
1. In TestUser1 client, hold TestUser2 selected
2. From TestUser3 client, send 2 messages to TestUser1
3. In TestUser1, without clicking TestUser3, count unread in sidebar

**Expected Result**:
- ✅ TestUser3 shows "● TestUser3 (2)" in sidebar
- ✅ Counter indicates unread message count
- ✅ When clicking TestUser3, counter resets to "● TestUser3"
- ✅ No "(0)" shown, just the username

**Status**: Pass / Fail: ___________

---

## ✅ Test 10: ERROR HANDLING

**Objective**: Verify error messages for invalid input

**Steps**:

**Test A - Empty Username**:
1. Run `python client.py`
2. Leave username empty
3. Click CONNECT

Expected: ✅ Error message "⚠ Please enter your username"

**Test B - Invalid Port**:
1. Enter username: "TestUser"
2. Enter Port: "99999"
3. Click CONNECT

Expected: ✅ Error message "⚠ Invalid port: ..."

**Test C - Server Not Running**:
1. Kill server
2. Try to connect from client

Expected: ✅ Error message "❌ Connection refused" or similar

**Status**: Pass / Fail: ___________

---

## ✅ Test 11: DISCONNECT AND RECONNECT

**Objective**: Verify disconnect and re-login works

**Steps**:
1. In TestUser1 client, click "🔌 Disconnect"
2. Should return to login screen
3. Enter same username "TestUser1"
4. Click CONNECT

**Expected Result**:
- ✅ Login screen appears after disconnect
- ✅ Can reconnect without errors
- ✅ Old chat history is cleared (fresh start)
- ✅ Can see other users in sidebar

**Status**: Pass / Fail: ___________

---

## ✅ Test 12: SERVER LOGGING

**Objective**: Verify server shows activity correctly

**Steps**:
1. Observe server window while users connect/send messages
2. Check:
   - User joins: ✅ "✅ username joined"
   - Messages: ✅ "💬 sender → recipient: message"
   - Disconnects: ✅ "👤 username left"
   - User list: ✅ "👥 Connected: N"
   - Message count: ✅ "💬 Messages: N"

**Expected Result**:
- ✅ All activity properly logged with timestamps
- ✅ Logs show detailed info
- ✅ Color-coded: green for join, red for errors, etc.

**Status**: Pass / Fail: ___________

---

## ✅ Test 13: UI RESPONSIVENESS

**Objective**: Verify UI doesn't freeze or lag

**Steps**:
1. Send several messages rapidly between 2-3 users
2. Switch between users quickly
3. Resize window

**Expected Result**:
- ✅ No freezing or hanging
- ✅ Messages display instantly
- ✅ UI remains responsive
- ✅ Window resizing works smoothly
- ✅ No "Not Responding" issues

**Status**: Pass / Fail: ___________

---

## ✅ Test 14: ENTER KEY TO SEND

**Objective**: Verify pressing Enter sends message

**Steps**:
1. Click on a user
2. Type message: "Testing Enter key"
3. Press Enter key (don't click Send button)

**Expected Result**:
- ✅ Message is sent
- ✅ Message appears in chat
- ✅ Input field clears
- ✅ Cursor remains in input field

**Status**: Pass / Fail: ___________

---

## ✅ Test 15: MESSAGE FORMATTING

**Objective**: Verify message bubbles display correctly

**Steps**:
1. Send a message with long text (80+ characters)
2. Send message with special characters: "Hello! @#$%^&*()"
3. Send message with emoji: "Hi 😊"

**Expected Result**:
- ✅ Long text wraps properly in bubble (wraplength=280)
- ✅ Special characters display correctly
- ✅ Message stays within bubble bounds
- ✅ No text overflow or truncation

**Status**: Pass / Fail: ___________

---

## 📊 Summary

**Total Tests**: 15
**Passed**: _____ / 15
**Failed**: _____ / 15

### Overall Status: 
- ✅ **ALL FIXED** (if all 15 pass)
- ⚠️ **MOSTLY WORKING** (if 13-14 pass)
- ❌ **NEEDS WORK** (if < 13 pass)

---

## 🐛 If Tests Fail

1. **Messages not showing**: 
   - Check that receiver has selected sender in sidebar
   - Check server logs for message delivery

2. **Connect button not visible**:
   - Check tkinter version is current
   - Try resizing window

3. **Slow message delivery**:
   - Check network connection
   - Reduced server load (too many messages)

4. **Server crashes**:
   - Check port 5555 not in use: `netstat -ano | findstr :5555`
   - Try different port in server config

---

**Test Date**: _______________
**Tester**: _______________
**Overall Assessment**: _______________
