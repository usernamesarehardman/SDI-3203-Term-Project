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

    python server.py --host 127.0.0.1 --port 8080

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

## 🧰 Optional Features (Stretch Goals)

- [x] Help command
- [ ] Message queuing for offline users
- [ ] TLS/SSL encryption
- [ ] Private group chats
- [ ] User authentication
- [ ] GUI using tkinter or other libraries
