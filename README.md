# The Last Hero

## Project Description
**The Last Hero** is a Python text-based adventure game developed as a final requirement for **Programming 1**.  
The player takes on the role of the only hero who escaped a powerful curse and must journey through a dangerous forest to rescue possessed friends and defeat Bowser in a final battle.

The game focuses on exploration, decision-making, and turn-based combat using text and ASCII-based maps.

## Inspiration
The game is **inspired by the story mode of *Super Smash Bros. Ultimate*** (Nintendo Switch), specifically:
- The **storyline concept** of heroes being possessed and needing to be rescued
- The **map progression idea** and exploration flow

Only the **narrative theme and map structure** were inspired.  
The **battle mechanics, game logic, scoring system, and implementation** were fully designed and coded independently for this project.

## How the Program Works
- The game runs entirely in the **terminal/console**.
- The player controls a hero who escaped a powerful curse.
- Each map must be cleared by saving all possessed friends before moving to the next area.
- The final area leads to a boss battle against Bowser.
- Player performance is graded based on HP, time played, and number of retries.

---

## 🕹️ How to Play the Game

### Game Mechanics
- The game is played entirely in the **terminal/console**.
- You explore maps using the **W, A, S, D** keys.
- Each map contains:
  - **F** – Possessed Friends to rescue  
  - **I** – Items to collect  
  - **E** – Exit (locked until all friends are saved)  
- Your HP, retries, inventory, and time are tracked throughout the game.

---

### Movement & Exploration
- You can move freely on open paths (`.`).
- Walls (`#`) block movement.
- Stepping on:
  - **F** → starts a battle with a possessed friend
  - **I** → grants a random item
  - **E** → moves to the next map (if all friends are saved)

---

### Items and Their Effects
You can use items during battles by selecting **Use Item**.

| Item | Effect |
|----|----|
| **Healing Potion** | Restores 50% of the hero’s maximum HP |
| **Power Surge** | 2x damage multiplier boosts the next attack’s damage |
| **Guardian Barrier** | Grants a shield that absorbs incoming 50 attack damage |
| **Fate Talisman** | Guarantees a lucky strike on the next attack |

Items are **consumed upon use**.

---

### Fighting Possessed Friends
When encountering a possessed friend:
- You may **Fight** or **Retreat**
- Retreating safely returns you to the map

During battle, you can:
1. **Attack** – Deal damage
2. **Heal** – Recover HP (limited to 5 heals in a row)
3. **Use Item** – Use items from your inventory

**Important Mechanics:**
- Healing too many times forces an automatic attack
- Shields absorb damage before HP is reduced
- If HP reaches 0:
  - You may **Try Again** (counts as a retry)
  - Or **Rest**, returning to the map (counts as a retry)

Saving a friend:
- Removes them from the map
- Adds them to your saved allies list
- Grants random item rewards

---

### Final Battle: Bowser
After all friends are saved, the final battle begins.

#### Special Buffs During the Final Battle
Your saved friends empower you with permanent bonuses:
- **+10 HP restored every battle round**
- **1.5× base damage multiplier on all attacks**
- **Unlimited healing**
- **100 shield at the start of the fight**

#### Bowser Battle Actions
You may:
1. **Attack**
2. **Heal**
3. **Use Item**

Bowser can:
- Attack with powerful damage
- Regenerate HP when weakened

If defeated:
- You may **Try Again** (adds to retry count)
- Or **Give Up**, ending the game

---

## Scoring System
Your final score is based on:
- **Final HP** (higher HP = higher score)
- **Time Played** (faster completion = higher score)
- **Retries** (fewer retries = higher score)

A final **grade (A–F)** is displayed after the game ends.

---

## How to Run the Program
1. Make sure Python 3 is installed.
2. Open a terminal or command prompt.
3. Navigate to the project folder.
4. Run the game using:
   ```bash
   python the_last_hero.py

---

## 👤 Author

**Andrei Eon Adducul**  
Developer of *The Last Hero*  
Final Requirement – Programming 1  
St. Paul University Philippines
