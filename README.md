# AI_tic-tac-toe
# 🧠 3D Tic-Tac-Toe with AI (4x4x4)

An advanced Python-based 3D Tic-Tac-Toe game featuring an intelligent AI opponent and an interactive GUI built with Tkinter. This project elevates the classic game to a 4x4x4 three-dimensional format and introduces AI opponents with variable difficulty levels powered by the minimax algorithm with alpha-beta pruning.

---

## 🎮 Game Overview

- **Board:** 4x4x4 3D grid using NumPy arrays
- **Interface:** Responsive GUI using Tkinter with scrollable layers and dynamic turn indication
- **AI Engine:** Implements Minimax with Alpha-Beta Pruning
- **Difficulty Levels:**
  - 🟢 Easy (depth: 2)
  - 🟡 Difficult (depth: 4)
  - 🔴 Insane (depth: 6)

---

## 🧠 Key Features

- AI decision-making simulates different skill levels
- GUI includes controls for difficulty, rules, and reset
- Highlights winning lines and provides end-of-game feedback
- Scrollable board design improves 3D spatial clarity

---

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **Libraries:** Tkinter, NumPy, random

---

## 📊 AI Methodology

- **Minimax Algorithm:** Recursively evaluates future moves
- **Alpha-Beta Pruning:** Optimizes search by eliminating suboptimal branches
- **Evaluation Logic:** +1 (AI win), -1 (Player win), 0 (draw)
- **Dynamic Depth:** Based on difficulty for balance between speed and strategy

---

## 📐 Winning Logic

- Considers all possible 3D winning lines:
  - Horizontal, vertical, and diagonal (within and across layers)
  - Cross-layer and multi-axis combinations
- Uses precalculated win vectors for performance

---

## 🖼️ GUI & User Experience

- Layer-based grid with scrollable canvas
- Buttons for each cell, rules popup, and game state indicators
- Prevents invalid moves, gives real-time game feedback

---

## 🚀 How to Run

1. Ensure Python 3.x is installed
2. Install dependencies (if needed):
   ```bash
   pip install numpy
