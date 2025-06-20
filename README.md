# 🦖 Dino AI Agents — Reflex & Heuristic Control

This project enhances the classic Chrome Dino game by integrating two types of AI agents — a **Reflex Agent** and a **Heuristic Agent** — to compare decision-making strategies in a dynamic game environment.

---

## 🎯 Project Objective

The main goal is to simulate and compare how two different agent strategies perform under the same game conditions by reacting to approaching obstacles (cacti and birds) using distinct logic.

---

## 🧠 Agent Types

### 🔁 Reflex Agent

- Makes immediate decisions based on simple condition checks.
- When an obstacle is near:
  - **Cactus** → jump
  - **Bird** → jump or duck based on vertical position
- Adjusts **jump power** and **duck duration** proportionally with the game’s speed (based on score).

### 🧮 Heuristic Agent

- Uses rule-based logic with more detailed checks.
- Determines bird height:
  - High → jump
  - Medium → duck
  - Low → jump
- Uses different **distance thresholds** for cacti and birds.
- Both **jump distance** and **duck duration** scale dynamically with game speed.

---

## 🕹️ How to Run

### Requirements

```bash
pip install pygame
```

### Launch the Game

```bash
python dino_ai_game.py
```

You’ll be prompted to choose:
- `r` → Run Reflex Agent
- `h` → Run Heuristic Agent

---

## 📊 Performance Comparison

Each agent logs its final score to a file:
- `scores_reflex.txt`
- `scores_heuristic.txt`

These files can be visualized with bar charts or used for further analysis.

---

## 🖼️ Features

- 🎮 Real-time gameplay with `pygame`
- 🧠 Two distinct AI control strategies
- 📈 Score logging and evaluation
- ⏱️ Dynamic difficulty scaling
- ⚖️ Side-by-side performance comparison

---

## 📂 Project Structure

```
├── dino_ai_game.py
├── reflex_agent.py
├── heuristic_agent.py
├── assets/              # Game images
├── scores_reflex.txt
├── scores_heuristic.txt
```

---

## 👤 Developer Note

> This project was developed as part of an Artificial Intelligence course to explore decision-making models in a controlled interactive environment.
