# Snake Game

Welcome to the Snake Game repository featuring a fully functional Python implementation with exciting additional features! This repo includes not only the classic game but also two AI Players and multiple user interfaces to choose from. Deployment is made simple using Docker, allowing you to play the game on any platform.

## Table of Contents

- [Features](#features)
- [User Interfaces](#user-interfaces)
- [Gameplay](#gameplay)
- [Performance Evaluation](#performance-evaluation)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Help Menu](#help-menu)

## Features

- **Three Unique User Interfaces**: Choose between GUI, CLI, and CUI for an optimal experience.

- **Two Intelligent AI Opponents**: Explore the capabilities of a Neural Network and a Hamiltonian Cycle based player.

- **Progress Analysis Tools**: Analyze AI performance locally or inside Docker containers.

- **Effortless Deployment**: Utilize Docker for seamless cross-platform gaming.
  User Interfaces

### User Interfaces

- **Graphical User Interface (GUI)** – Experience vibrant visuals and smooth animation with Pygame.
- **Command Line Interface (CLI)** – Play effortlessly in terminal environments using the stylish Python Blessed library.
- **Curses User Interface (CUI)** – Originally built as the default CLI, this version was migrated to Blessed for improved compatibility. If your machine supports it, feel free to utilize this simplistic yet aesthetic interface.

### Gameplay

Select one of these three distinct players at the start of the game:

### Players

- **Human** – Take control and test your skills in the various user interfaces.
- **Neural Network** – Engage with a machine learning model that learns from its interactions.
- **Hamiltonian Cycle** – Observe the elegance of the Hamiltonian cycle algorithm solving the game whenever possible.

### Performance Evaluation

Evaluate machine learning models' effectiveness by hosting sessions directly on your device or within Docker containers. Adjust the scripts and Docker files settings to fit your specific testing criteria.

## Getting Started

### Prerequisites

Ensure you have met the following requirements before proceeding:

- Python 3.x
- Optional: Docker installation for cross-platform compatibility

### Installation

To quickly get started playing the snake game, follow these steps:

- Clone this repository git clone and change into the newly created directory.
- Run the game using the appropriate command depending on your desired UI:

```bash
bash run.sh gui human     # Play in the GUI as a human
bash run.sh cui demo      # Watch your models perform in the CUI
bash run.sh cli ham       # Watch the game complete itself in the CLI
bash run.sh neural train  # Train your model in headless mode
```

- Alteratively, use docker-compose to easily build and run the containerized versions

### Help Menu

Access detailed information regarding usage, commands, and options with the following command:

```bash
bash run.sh -h
```
