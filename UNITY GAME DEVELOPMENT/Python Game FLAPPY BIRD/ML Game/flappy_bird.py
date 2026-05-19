import pygame
import random
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load images
bird_img = pygame.image.load('bluebird-downflap.png')
pipe_img = pygame.image.load('pipe-red.png')
pipe_img = pygame.transform.scale(pipe_img, (50, HEIGHT))
ground_img = pygame.image.load('base.png')
ground_img = pygame.transform.scale(ground_img, (WIDTH, ground_img.get_height()))
background_img = pygame.image.load('background-day.png')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Bird settings
bird = pygame.Rect(50, 300, 30, 30)
bird_velocity = 0
gravity = 0.5

# Pipe settings
pipe_width = 50
pipe_gap = 150
pipe_velocity = -3
pipes = []

def create_pipe():
    height = random.randint(50, 300)  # Adjusted maximum height
    print(f"Creating pipe with height: {height}")  # Debugging statement
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap)
    return top_pipe, bottom_pipe

pipes.append(create_pipe())

# Create a neural network model
model = Sequential([
    Dense(24, input_dim=4, activation='relu'),
    Dense(24, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='mse')

def get_state(bird, pipes):
    bird_y = bird.y
    pipe_x = pipes[0][0].x
    pipe_gap_y = pipes[0][0].height
    return np.array([bird_y, bird_velocity, pipe_x, pipe_gap_y])

def get_reward(bird, pipes):
    if bird.colliderect(pipes[0][0]) or bird.colliderect(pipes[0][1]):
        return -1  # Collision penalty
    return 0.1  # Reward for staying alive

training_data = []

def train_model(model, epochs=10):
    states, rewards = zip(*training_data)
    states = np.array(states)
    rewards = np.array(rewards)
    model.fit(states, rewards, epochs=epochs)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_velocity = -8

    # Bird movement
    bird_velocity += gravity
    bird.y += bird_velocity

    # Pipe movement
    for pipe in pipes:
        pipe[0].x += pipe_velocity
        pipe[1].x += pipe_velocity

    # Remove pipes off the screen
    if pipes[0][0].x < -pipe_width:
        pipes.pop(0)
        pipes.append(create_pipe())

    # Collision detection and reward calculation
    reward = get_reward(bird, pipes)
    state = get_state(bird, pipes)
    training_data.append((state, reward))

    if reward == -1:
        running = False

    # Clear the screen and draw the background
    screen.blit(background_img, (0, 0))

    # Draw the bird
    screen.blit(bird_img, bird.topleft)

    # Draw the pipes
    for pipe in pipes:
        top_pipe_img = pygame.transform.scale(pipe_img, (pipe_width, pipe[0].height))
        bottom_pipe_img = pygame.transform.scale(pipe_img, (pipe_width, HEIGHT - pipe[0].height - pipe_gap))
        screen.blit(top_pipe_img, pipe[0].topleft)
        screen.blit(pygame.transform.flip(bottom_pipe_img, False, True), pipe[1].topleft)

    # Draw the ground
    screen.blit(ground_img, (0, HEIGHT - ground_img.get_height()))

    pygame.display.flip()
    clock.tick(30)

# Train the model with collected data
train_model(model)

pygame.quit()
