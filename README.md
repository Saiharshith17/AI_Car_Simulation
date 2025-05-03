# AI CAR SIMULATION USING NEAT

This project is a Python-based simulation of a self-driving car that uses the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to evolve and learn how to navigate a track autonomously. Built with the Pygame library, the simulation visually demonstrates how artificial intelligence can learn driving behavior over multiple generations through neuroevolution. The car is equipped with virtual radar sensors that detect obstacles (walls) and make real-time decisions using a neural network trained via NEAT.

## Key Features

- *NEAT Algorithm*: Evolves neural networks to control car behavior over generations.
- *Sensor System*: Simulates radar to detect distances to walls.
- *Collision Detection*: Ends simulation for a car upon hitting walls.
- *Real-Time Display*: Visual feedback of car movement, rotation, and sensor rays.
- *Customizable Settings*: Speed, acceleration, turning angles, and evolution parameters are user-configurable.
- *Performance Visualization*: Graph of fitness per generation using matplotlib.
- *Best Genome Storage*: Saves top-performing neural network for reuse.

## Requirements

- Python 3.x
- Pygame
- NEAT-Python
- Matplotlib
- NumPy

### Install Dependencies

```bash
pip install pygame neat-python matplotlib numpy