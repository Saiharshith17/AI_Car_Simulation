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


## Default Simulation Parameters

| Parameter               | Default Value | Description                                  |
|------------------------|---------------|----------------------------------------------|
| Initial Speed (v)     | 2.0           | Initial speed of each car                    |
| Acceleration (a)      | 0.2           | How quickly the car speeds up                |
| Deceleration (d)      | 0.3           | How quickly the car slows down               |
| Maximum Speed (max_v) | 7.0           | The upper limit for the car's speed          |
| Angle Increment (angle_inc) | 5       | Rotation angle per step in degrees           |
| Time per Generation (max_time) | 20    | Number of seconds for each generation        |
| Number of Generations (gens) | 30      | Total number of generations to evolve        |


# How to Make the Self-Driving Car Simulation Work

Follow the steps below to set up the environment, install dependencies, select a map, and run the self-driving car simulation.

## 1. Clone the Repository

First, clone the repository to your local machine using Git:


git clone <repository_url>

cd <repository_folder>  

cd <main.py>

## 2. select maps from the available ones 
Available Maps:
map1

map2

map3

map4

map5


## 3.Specify the default values of the input parameters

    "v": 2.0,           # Initial speed
    "a": 0.2,           # Acceleration
    "d": 0.3,           # Deceleration
    "max_v": 7.0,       # Maximum speed
    "angle_inc": 5,     # Angle increment (degrees)
    "max_time": 25,     # Time per generation (seconds) 
    "gens": 30          # Number of generations
 
## 4. Run the main.py
  python main.py
### Install Dependencies

```bash
pip install pygame neat-python matplotlib numpy

