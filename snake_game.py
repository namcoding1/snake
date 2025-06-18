import curses
import random
import time

# 게임 설정
HEIGHT = 20
WIDTH = 40
SNAKE_CHAR = '#'
FOOD_CHAR = '*'


def create_food(snake):
    while True:
        food = (random.randint(1, HEIGHT - 2), random.randint(1, WIDTH - 2))
        if food not in snake:
            return food


def main(stdscr):
    curses.curs_set(0)  # 커서 숨기기
    stdscr.nodelay(True)
    stdscr.timeout(100)

    # 초기 뱀 설정
    snake = [(HEIGHT // 2, WIDTH // 2 + i) for i in range(3)]
    direction = curses.KEY_LEFT

    food = create_food(snake)
    score = 0

    while True:
        key = stdscr.getch()
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            # 반대 방향으로 바로 이동하는 것 방지
            if (direction == curses.KEY_UP and key != curses.KEY_DOWN) or \
               (direction == curses.KEY_DOWN and key != curses.KEY_UP) or \
               (direction == curses.KEY_LEFT and key != curses.KEY_RIGHT) or \
               (direction == curses.KEY_RIGHT and key != curses.KEY_LEFT):
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

        # 벽 충돌 또는 자기 자신과 충돌 시 게임 종료
        if (
            head_y in [0, HEIGHT - 1] or
            head_x in [0, WIDTH - 1] or
            new_head in snake
        ):
            msg = 'Game Over! Score: {}'.format(score)
            stdscr.addstr(HEIGHT // 2, (WIDTH - len(msg)) // 2, msg)
            stdscr.refresh()
            time.sleep(2)
            break

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = create_food(snake)
        else:
            snake.pop()

        stdscr.clear()

        # 경계 그리기
        for x in range(WIDTH):
            stdscr.addch(0, x, '#')
            stdscr.addch(HEIGHT - 1, x, '#')
        for y in range(HEIGHT):
            stdscr.addch(y, 0, '#')
            stdscr.addch(y, WIDTH - 1, '#')

        # 음식 그리기
        stdscr.addch(food[0], food[1], FOOD_CHAR)

        # 뱀 그리기
        for y, x in snake:
            stdscr.addch(y, x, SNAKE_CHAR)

        score_text = 'Score: {}'.format(score)
        try:
            stdscr.addstr(0, WIDTH + 2, score_text)
        except curses.error:
            # 터미널 크기가 충분하지 않을 때는 점수 표시를 생략
            pass

        stdscr.refresh()


if __name__ == '__main__':
    curses.wrapper(main)
