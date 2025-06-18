import curses
import random
import curses.ascii

# 게임 설정
HEIGHT = 20
WIDTH = 40
SNAKE_CHAR = '#'
FOOD_CHAR = '*'
ENEMY_CHAR = 'X'
NORMAL_TIMEOUT = 100  # ms
BOOST_TIMEOUT = 50
BOOST_DURATION = 5  # iterations


def create_food(snake, enemy=None):
    while True:
        food = (
            random.randint(1, HEIGHT - 2),
            random.randint(1, WIDTH - 2),
        )
        if food not in snake and (enemy is None or food != enemy):
            return food


def create_enemy(snake, food):
    while True:
        enemy = (
            random.randint(1, HEIGHT - 2),
            random.randint(1, WIDTH - 2),
        )
        if enemy not in snake and enemy != food:
            return enemy


def draw_borders(stdscr):
    for x in range(WIDTH):
        stdscr.addch(0, x, '#')
        stdscr.addch(HEIGHT - 1, x, '#')
    for y in range(HEIGHT):
        stdscr.addch(y, 0, '#')
        stdscr.addch(y, WIDTH - 1, '#')


def game_loop(stdscr):
    stdscr.nodelay(True)
    boost_ticks = 0

    snake = [(HEIGHT // 2, WIDTH // 2 + i) for i in range(3)]
    direction = curses.KEY_LEFT

    enemy = create_enemy(snake, None)
    food = create_food(snake, enemy)
    score = 0

    stdscr.clear()
    draw_borders(stdscr)
    for y, x in snake:
        stdscr.addch(y, x, SNAKE_CHAR)
    stdscr.addch(food[0], food[1], FOOD_CHAR)
    stdscr.addch(enemy[0], enemy[1], ENEMY_CHAR)
    stdscr.refresh()

    while True:
        stdscr.timeout(BOOST_TIMEOUT if boost_ticks > 0 else NORMAL_TIMEOUT)
        key = stdscr.getch()
        if 0 <= key <= 31:
            boost_ticks = BOOST_DURATION
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            if (
                (direction == curses.KEY_UP and key != curses.KEY_DOWN) or
                (direction == curses.KEY_DOWN and key != curses.KEY_UP) or
                (direction == curses.KEY_LEFT and key != curses.KEY_RIGHT) or
                (direction == curses.KEY_RIGHT and key != curses.KEY_LEFT)
            ):
                direction = key

        head_y, head_x = snake[0]
        if direction == curses.KEY_UP:
            head_y -= 1
        elif direction == curses.KEY_DOWN:
            head_y += 1
        elif direction == curses.KEY_LEFT:
            head_x -= 1
        elif direction == curses.KEY_RIGHT:
            head_x += 1

        new_head = (head_y, head_x)

        # 적군 이동
        move_y, move_x = random.choice([
            (0, 0),
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ])
        enemy_y = enemy[0] + move_y
        enemy_x = enemy[1] + move_x
        if (
            1 <= enemy_y < HEIGHT - 1 and
            1 <= enemy_x < WIDTH - 1 and
            (enemy_y, enemy_x) not in snake and
            (enemy_y, enemy_x) != food
        ):
            stdscr.addch(enemy[0], enemy[1], ' ')
            enemy = (enemy_y, enemy_x)

        # 벽, 자기 자신, 적군과 충돌 시 게임 종료
        if (
            head_y in [0, HEIGHT - 1] or
            head_x in [0, WIDTH - 1] or
            new_head in snake or
            new_head == enemy
        ):
            return score

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = create_food(snake, enemy)
            stdscr.addch(food[0], food[1], FOOD_CHAR)
        else:
            tail = snake.pop()
            stdscr.addch(tail[0], tail[1], ' ')

        # 적군 그리기
        stdscr.addch(enemy[0], enemy[1], ENEMY_CHAR)

        # 뱀 그리기
        stdscr.addch(new_head[0], new_head[1], SNAKE_CHAR)

        score_text = 'Score: {}'.format(score)
        try:
            stdscr.addstr(0, WIDTH + 2, score_text + '  ')
        except curses.error:
            pass

        stdscr.refresh()
        if boost_ticks > 0:
            boost_ticks -= 1


def main(stdscr):
    curses.curs_set(0)

    max_y, max_x = stdscr.getmaxyx()
    if max_y < HEIGHT or max_x < WIDTH:
        stdscr.clear()
        msg = f"Terminal must be at least {HEIGHT}x{WIDTH}"
        stdscr.addstr(0, 0, msg)
        stdscr.refresh()
        stdscr.getch()
        return

    while True:
        score = game_loop(stdscr)

        msg = f"Game Over! Score: {score}"
        prompt = "Press r to restart or q to quit"
        stdscr.addstr(HEIGHT // 2, (WIDTH - len(msg)) // 2, msg)
        stdscr.addstr(HEIGHT // 2 + 1, (WIDTH - len(prompt)) // 2, prompt)
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key in (ord('q'), ord('Q')):
                return
            if key in (ord('r'), ord('R')):
                stdscr.clear()
                break

if __name__ == '__main__':
    curses.wrapper(main)
