# COMP9001_final_project
# Space Ship - A Python Pygame Project

## Overview

Space Ship is a retro-style arcade shooter game reminiscent of classics like "Raiden Fighters." Players control a starfighter navigating through treacherous space, dodging meteorites and battling cosmic pirates. The game is built using Python and the Pygame library.

The core gameplay involves maneuvering the starfighter left and right across three distinct lanes. Forward movement is simulated by the continuous downward scroll of background elements and obstacles. Players must react quickly to avoid incoming meteorites or destroy pirate ships with their infinite ammunition.

## Game Mechanics

*   **Player Control**:
    *   The player's starfighter is fixed to the second row from the bottom of the screen.
    *   Use the **LEFT ARROW KEY** to hold the starfighter in the left lane.
    *   Use the **RIGHT ARROW KEY** to hold the starfighter in the right lane.
    *   If neither LEFT nor RIGHT arrow key is pressed, the starfighter automatically returns to and stays in the middle lane.
    *   Press the **SPACEBAR** to fire weapons. Ammunition is unlimited.
*   **Lanes & Rows**:
    *   The game window's vertical axis is divided into three lanes for starfighter and obstacle movement.
    *   The horizontal axis is conceptually divided into six rows for visual spacing and player positioning.
*   **Obstacles**:
    *   **Meteorites**: Indestructible space rocks that must be dodged. Collision results in game over.
    *   **Pirate Ships**: Enemy spacecraft that can be destroyed by player fire. Collision also results in game over.
*   **Obstacle Spawning**:
    *   Obstacles appear from the top edge of the screen and move downwards.
    *   New rows of obstacles are generated at regular intervals (every two "row heights" of scrolling).
    *   To ensure fair gameplay, a newly spawned row of obstacles will never consist entirely of meteorites; at least one pirate ship (a destroyable path) will always be present.
*   **Scoring**:
    *   Players earn **1 point** for successfully destroying a pirate ship.
    *   Players earn **1 point** each time a new row of obstacles is generated (signifying survival and progression).
    *   The current score is displayed in the top-right corner of the screen.
*   **Game Over**:
    *   The game ends if the player's starfighter collides with any obstacle (meteorite or pirate ship).
    *   The game can also be ended prematurely by pressing the **ESCAPE (ESC) KEY**.
    *   Upon game over, an end screen displays "GAME OVER" and the player's final score. Players can then choose to play again or quit.
*   **Visuals & Audio**:
    *   The game features custom sprites for the player, meteorites, pirate ships, and a scrolling space background.
    *   Background music plays throughout the game to enhance the arcade experience.
*   **Language**: All in-game text and code comments are in English.

## How to Play

1.  **Prerequisites**:
    *   Python 3.x installed.
    *   Pygame library installed. You can install it via pip:
        ```bash
        pip install pygame
        ```
2.  **Setup**:
    *   Clone or download the game repository/files.
    *   Ensure you have an `assets` folder in the same directory as the main game script (`.py` file).
    *   The `assets` folder should contain:
        *   An `images` subfolder with:
            *   `player_ship.png` (your starfighter image)
            *   `meteorite.png` (your meteorite image)
            *   `pirate_ship.png` (your pirate ship image)
            *   `background.png` (your scrolling background image)
        *   A `sounds` subfolder with:
            *   `background_music.mp3` (or `.ogg`, your background music file)
        *(Note: Actual filenames might differ based on your specific asset files; ensure they match the paths defined in the game script.)*
3.  **Running the Game**:
    *   Navigate to the game's directory in your terminal.
    *   Run the main Python script:
        ```bash
        python space_ship_game.py
        ```
        (Replace `space_ship_game.py` with the actual name of your Python game file if different.)

## Controls Summary

*   **LEFT ARROW**: Move and hold in left lane
*   **RIGHT ARROW**: Move and hold in right lane
*   **(NO KEY PRESSED)**: Return to/stay in middle lane
*   **SPACEBAR**: Fire weapon
*   **ESC**: End game / Quit from game over screen

## Future Enhancements (Potential Ideas)

*   Sound effects for shooting, explosions, and collisions.
*   Increasing difficulty over time (e.g., faster obstacles, more complex patterns).
*   Player power-ups (e.g., temporary shield, spread shot).
*   Different enemy types with unique behaviors.
*   High score saving/leaderboard.
*   Animated sprites for explosions and thrusters.

Enjoy your flight through the cosmos in Space Ship!
