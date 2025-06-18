# Python Snake Game

This repository contains a simple terminal-based snake ("지렁이 키우기") game implemented in Python.

## Requirements

- Python 3
- Unix-like terminal with `curses` support (Linux, macOS)

No external packages are required. The game window requires a terminal of at least 20x40 characters. The integrated terminal in GitHub Codespaces meets this requirement, so you can run the game there as well.

## Running the Game

Execute the following command in a terminal:

```bash
python3 snake_game.py
```

Use the arrow keys to control the snake. Eat food (`*`) to grow longer. Avoid running into the walls, your own body, or the moving enemy (`X`). After the game ends, press `r` to restart or `q` to quit.

## 게임 실행 방법 (Korean)

터미널에서 아래 명령을 실행하세요:

```bash
python3 snake_game.py
```

화살표 키로 뱀을 조작하며, `*` 모양의 먹이를 먹으면 길이가 길어집니다. 벽이나 자신의 몸, 그리고 움직이는 적군(`X`)에 부딪히면 게임이 종료됩니다. 게임이 끝난 뒤에는 `r` 키로 다시 시작하거나 `q` 키로 종료할 수 있습니다.
게임 화면을 제대로 보려면 최소 20x40 크기의 터미널이 필요합니다.
GitHub Codespaces의 기본 터미널도 이 조건을 만족하므로 실행할 수 있습니다.
