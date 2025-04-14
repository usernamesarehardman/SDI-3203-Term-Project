# SDI-3203-Term-Project

# Push-Style Client-Server Chat System

## Overview

This project implements a simple push-style client-server chat application designed for local networks. It supports multiple clients connected to a single server, each registering with a unique username and exchanging messages in real time. The server pushes messages directly to recipients without requiring periodic polling.

---

## 📦 Project Structure

    chat_project/
    ├── client.py  
    ├── server.py   
    └── README.md

---

## 🚀 Getting Started

### Prerequisites

- Python 3.6+

### Dependencies

- Uses only standard libraries:
  - `socket`
  - `threading`
  - `logging`
  - `argparse`

### Setup

1. Clone this repository or download the source code.
2. Open a terminal and navigate to the project directory.

### Running the Server

    python server.py --port 8080

### Running a Client

    python client.py --host 127.0.0.1 --port 8080

---

## 💡 Usage

- Upon starting, each client will be prompted to enter a unique username.
- To send a message:  
  `recipient_username:message_text`
- To check who is online:  
  `server:who`
- To exit the chat:  
  `server:exit`
- To check available commands:  
  `server:help`

---

## ✅ Functional Requirements Checklist

### Core Features

- [x] Prompt client for username on startup
- [x] Register username automatically at client startup
- [x] Reject duplicate usernames on server
- [x] Maintain a server-side dictionary of active users
- [x] Immediately push messages from sender to recipient
- [x] Print messages on client side as soon as they arrive
- [x] Support sending messages in format `<recipient>:<message>`
- [x] Support command `server:who` to request list of online users
- [x] Support command `server:exit` to disconnect gracefully
- [x] Remove user from dictionary upon client exit
- [x] Threaded server: one thread per client
- [x] Threaded client: one thread listens, one handles input
- [x] Server handles commands: register, who, exit, message
- [x] Client displays server responses and chat messages

---

## 🧰 Optional Features (Stretch Goals)

- [ ] Message queuing for offline users
- [ ] TLS/SSL encryption
- [ ] Private group chats
- [ ] User authentication
- [ ] GUI using tkinter or other libraries

---

## 📬 Contact

For any questions or troubleshooting, please contact your project partners or instructor.
