# Minecraft Python Scripts

Collection of Python scripts for enhancing PvP gameplay in Minecraft using the Minescript mod.

## Requirements

- Minecraft Java Edition
- Minescript mod ([minescript.net](https://minescript.net))
- Python 3.8 or higher (see Minescript [installation guide](https://github.com/maxuser0/minescript/blob/main/README.md) for details)

## Installation

1. Install Minescript mod and Python following the [official instructions](https://github.com/maxuser0/minescript/blob/main/README.md)

2. Place `.py` scripts from this repository into your Minecraft instance's `minescript` folder:  
   `.../.minecraft/minescript/`

3. Launch Minecraft using the Minescript mod.

## Usage

- To run a script, open the Minecraft chat and enter:

  ```
  \script_name
  ```

  For example:
  ```
  \aimbot
  \triggerbot
  ```

- To stop a running script, open chat, enter:
  ```
  \jobs
  ```
  Find the job number for your script, then:
  ```
  \killjob <job number>
  ```

## Scripts

- `aimbot.py`: Automatically aims at the nearest player with smooth camera movement.
- `triggerbot.py`: Automatically attacks a target when your crosshair is over an entity.

## Configuration

Edit constants at the top of each script file using any IDE you prefer: PyCharm, VSC, Cursor (if u are a faggot) or whatever works for you.

## Why Python?

<details>
<summary>Explanation</summary>

# why not
![](https://i.imgur.com/T2ncrlQ.jpeg)
</details>
