# Pokeball Drop

Pokeball Drop is a Python game where you drop a Pokéball into a ditch and win a random Pokémon. It's a fun way to test your timing and discover new Pokémon.

## How to Use

You can either run the Python source code or use the pre-built executable:

### Option 1: Run the Python Source Code

1. **Install Python**  
   Download and install Python from the official site:  
   [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Install Required Packages**  
   Open your terminal or command prompt and run:

   ```bash
   pip install pandas requests pygame
   ```

3. **Clone This Repository**

   ```bash
   git clone https://github.com/johannanguyen/pokeball_drop
   ```

4. **Navigate to the Project Directory**

   ```bash
   cd pokeball_drop
   ```

5. **Run the Game**

   ```bash
   python game.py
   ```

### Option 2: Use the Executable

1. Download and unzip the `.exe` file
2. Double-click the `.exe` to start playing!

## How to Play

- Press the **spacebar** to drop the Pokéball
- Try to land it into a ditch
- Watch to see which Pokemon you win!

## Technical

This game is built using **Pygame** for the graphical interface and user interaction (loads images, moves object, spacebar keydown). It includes a custom dataset of 300 Pokemon each with a name, Pokedex number, and rarity level. 

When a Pokeball successfully lands in a ditch, the game uses **weighted probability** to select a Pokemon based on its rarity to guarantee that rare Pokemon appear less frequently than common ones.

Once a Pokemon is selected, the game uses its Pokedex number to make an API request and retrieve the corresponding sprite image which is then displayed on screen.

If the player misses, the game playfully mocks their failure and encourages them to try again.
