import curses
import random
import time
import math

class NewYearScene:
    COLOR_RED = 1
    COLOR_YELLOW = 2
    COLOR_GREEN = 3
    COLOR_WHITE = 4
    COLOR_PINK = 5
    COLOR_CYAN = 6
    COLOR_MAGENTA = 7

    INIT_TREE_LAYERS = 7
    MAX_TREE_LAYERS = 15
    TREE_SWAY_SPEED = 0.12

    STAR_BLINK_FRAMES = 8
    HORSE_MOVE_INTERVAL = 12
    SNOW_COUNT = 30

    STAR_COUNT = 25
    MAX_WISHES_DISPLAY = 3

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.sh, self.sw = 0, 0
        
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(self.COLOR_RED, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_PINK, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(self.COLOR_MAGENTA, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

        self.ricardo_ascii = [
            "     ,--,   ",
            "    /    \\  ",
            "   | 0  0 | ",
            "   |  >   | ",
            "    \\  ~  /  ",
            "     `--`   ",
            "     /  \\   ",
            "    /    \\  ",
            "作者自画像(Ricardo)"
        ]

        self.panel_commands = [
            ("w: 许 愿", self.COLOR_YELLOW),
            ("a: 挂灯笼", self.COLOR_RED),
            ("s: 树长大", self.COLOR_GREEN),
            ("d: 红包雨", self.COLOR_RED),
            ("f: 放烟花", self.COLOR_YELLOW),
            ("k: 中国结", self.COLOR_PINK),
            ("r: 重置", self.COLOR_WHITE),
            ("q: 退出", self.COLOR_WHITE)
        ]

        self.reset()

    def reset(self):
        self.tree_layers = self.INIT_TREE_LAYERS
        self.tree_sway_current = 0.0
        self.tree_sway_target = 0.0
        self.frame_count = 0
        
        self.decorations = {"lanterns": [], "knots": []}
        self.red_packets = []
        self.fireworks = []
        self.wishes = []
        self.stars = []
        self.snowflakes = []
        
        self.input_mode = False
        self.wish_text = ""
        self.running = True

        self.horse_x = 2
        self.horse_dir = 1

        # 修复：先获取当前窗口大小
        self.sh, self.sw = self.stdscr.getmaxyx()
        # 修复：重置时重新生成星星和雪花
        self.stars = [(random.randint(0, self.sw-1), random.randint(0, max(1, self.sh//3))) for _ in range(self.STAR_COUNT)]
        self.snowflakes = [(random.randint(0, self.sw-1), random.randint(0, self.sh-1), random.random()*0.5+0.2) for _ in range(self.SNOW_COUNT)]
        self.stdscr.clear()

    def update_size(self):
        new_sh, new_sw = self.stdscr.getmaxyx()
        if (new_sh, new_sw) != (self.sh, self.sw):
            self.sh, self.sw = new_sh, new_sw
            self.stars = [(random.randint(0, self.sw-1), random.randint(0, max(1, self.sh//3))) for _ in range(self.STAR_COUNT)]
            self.snowflakes = [(random.randint(0, self.sw-1), random.randint(0, self.sh-1), random.random()*0.5+0.2) for _ in range(self.SNOW_COUNT)]
            self.stdscr.clear()

    def safe_addch(self, y, x, char, color_pair=None):
        try:
            if 0 <= y < self.sh and 0 <= x < self.sw:
                args = [y, x, char]
                if color_pair: args.append(curses.color_pair(color_pair))
                self.stdscr.addch(*args)
        except:
            pass

    def safe_addstr(self, y, x, text, color_pair=None):
        try:
            if 0 <= y < self.sh and 0 <= x < self.sw:
                display_text = text[:(self.sw - x - 1)]
                args = [y, x, display_text]
                if color_pair: args.append(curses.color_pair(color_pair))
                self.stdscr.addstr(*args)
        except:
            pass

    def draw_tree(self):
        trunk_y = self.sh - 5
        trunk_x = (self.sw - 20) // 2 + int(self.tree_sway_current)
        
        for layer in range(5):
            y = trunk_y - layer
            width = 3 - layer // 2
            for dx in range(-width, width + 1):
                self.safe_addch(y, trunk_x + dx, "█", self.COLOR_YELLOW)
        
        leaf_chars = ["*", "o", "~", "#", "@", "%"]
        tree_rel_positions = []
        
        for layer in range(self.tree_layers):
            y = trunk_y - 5 - layer
            width = (self.tree_layers - layer) + 4
            
            for dx in range(-width, width + 1):
                x = trunk_x + dx
                if random.random() < 0.85:
                    char = leaf_chars[(x + y + layer) % len(leaf_chars)]
                    if layer < self.tree_layers // 3:
                        color = self.COLOR_GREEN
                    elif layer < 2 * self.tree_layers // 3:
                        color = self.COLOR_YELLOW if (x + y) % 3 == 0 else self.COLOR_GREEN
                    else:
                        color = self.COLOR_RED if (x + y) % 2 == 0 else self.COLOR_GREEN
                    self.safe_addch(y, x, char, color)
                    tree_rel_positions.append((y, dx))
        
        if self.frame_count % 3 < 2:
            self.safe_addstr(trunk_y - 5 - self.tree_layers, trunk_x - 1, "✨⭐✨")
        
        return trunk_y, trunk_x, tree_rel_positions

    def draw_decorations(self, trunk_y, trunk_x):
        for i, (y, rel_x) in enumerate(self.decorations["lanterns"]):
            sway = (-1)**i * (self.frame_count % 5 // 2)
            x = trunk_x + rel_x + sway
            self.safe_addstr(y, x, "🏮")
            
        for (y, rel_x) in self.decorations["knots"]:
            x = trunk_x + rel_x
            self.safe_addstr(y, x, "🎀")

    def add_decoration(self, deco_type, tree_rel_positions):
        if tree_rel_positions:
            pos = random.choice(tree_rel_positions)
            self.decorations[deco_type].append(pos)

    def draw_red_packets(self):
        if random.random() < 0.15:
            self.red_packets.append([random.randint(0, self.sw-1), 0, random.choice([-1, 0, 1])])
        
        new_packets = []
        for (x, y, sway) in self.red_packets:
            if y < self.sh - 1:
                self.safe_addstr(y, x, "🧧")
                new_x = max(0, min(self.sw-1, x + sway))
                new_sway = sway if random.random() > 0.1 else random.choice([-1, 0, 1])
                new_packets.append([new_x, y + 1, new_sway])
        self.red_packets[:] = new_packets

    def draw_fireworks(self):
        new_fireworks = []
        for (x, y, life, color) in self.fireworks:
            if life < 30:
                if life < 10:
                    self.safe_addch(y, x, "│", self.COLOR_YELLOW)
                    if y > 0: self.safe_addch(y-1, x, "│", self.COLOR_YELLOW)
                    if y > 1: self.safe_addch(y-2, x, "•", self.COLOR_CYAN)
                elif life < 20:
                    radius = life - 10
                    for angle in range(0, 360, 20):
                        rad = math.radians(angle)
                        dx = int(math.cos(rad) * radius)
                        dy = int(math.sin(rad) * radius)
                        char = random.choice(["*", "#", "@", "•", "~"])
                        c = color if (angle + life) % 2 == 0 else self.COLOR_CYAN
                        self.safe_addch(y + dy, x + dx, char, c)
                else:
                    radius = life - 10
                    for angle in range(0, 360, 30):
                        rad = math.radians(angle)
                        dx = int(math.cos(rad) * radius)
                        dy = int(math.sin(rad) * radius)
                        if random.random() < 0.5:
                            self.safe_addch(y + dy, x + dx, ".", color)
                
                new_y = y - 1 if life < 10 else y
                new_fireworks.append([x, new_y, life + 1, color])
        self.fireworks[:] = new_fireworks

    def trigger_fireworks(self, count=5):
        for _ in range(count):
            x = random.randint(3, self.sw-4)
            y = random.randint(self.sh//2, self.sh-5)
            color = random.choice([self.COLOR_RED, self.COLOR_YELLOW, self.COLOR_PINK, self.COLOR_CYAN])
            self.fireworks.append([x, y, 0, color])

    def trigger_red_packets(self, count=30):
        for _ in range(count):
            self.red_packets.append([random.randint(0, self.sw-1), 0, random.choice([-1, 0, 1])])

    def draw_stars(self):
        for (x, y) in self.stars:
            if self.frame_count % self.STAR_BLINK_FRAMES < 4:
                self.safe_addstr(y, x, "✨")
            elif self.frame_count % self.STAR_BLINK_FRAMES < 6:
                self.safe_addstr(y, x, "⭐")
            else:
                self.safe_addch(y, x, '.', self.COLOR_WHITE)

    def draw_snow(self):
        new_snow = []
        for (x, y, speed) in self.snowflakes:
            self.safe_addch(int(y), x, "❄", self.COLOR_CYAN)
            new_y = y + speed
            new_x = x + random.choice([-0.2, 0, 0.2])
            if new_y < self.sh - 1:
                new_snow.append((new_x % self.sw, new_y, speed))
            else:
                new_snow.append((random.randint(0, self.sw-1), 0, speed))
        self.snowflakes[:] = new_snow

    def draw_ground(self):
        for x in range(self.sw):
            char = random.choice(["▁", "▂", "▃", "▄"])
            self.safe_addch(self.sh - 4, x, char, self.COLOR_WHITE)

    def draw_panel(self):
        panel_x = max(0, self.sw - 22)
        if panel_x < 5: return

        for y in range(1, self.sh - 1):
            self.safe_addch(y, panel_x, "┃", self.COLOR_RED)
        
        self.safe_addstr(1, panel_x + 2, "  🎊 新年快乐 🎊  ", self.COLOR_YELLOW)
        self.safe_addstr(3, panel_x + 2, f"树层数: {self.tree_layers}", self.COLOR_GREEN)
        self.safe_addstr(5, panel_x + 2, f"🏮 灯笼: {len(self.decorations['lanterns'])}", self.COLOR_RED)
        self.safe_addstr(7, panel_x + 2, f"🎀 中国结: {len(self.decorations['knots'])}", self.COLOR_PINK)
        self.safe_addstr(9, panel_x + 2, f"🧧 愿望: {len(self.wishes)}", self.COLOR_YELLOW)
        
        self.safe_addstr(11, panel_x + 1, "━━━━━━━━━━━━━━━━━━", self.COLOR_RED)
        
        start_y = 13
        for i, (text, col) in enumerate(self.panel_commands):
            self.safe_addstr(start_y + i*2, panel_x + 3, text, col)

    def draw_ricardo(self):
        if self.frame_count % self.HORSE_MOVE_INTERVAL == 0:
            ricardo_width = max(len(line) for line in self.ricardo_ascii)
            self.horse_x += self.horse_dir
            
            if self.horse_x + ricardo_width >= self.sw - 1:
                self.horse_dir = -1
            elif self.horse_x <= 0:
                self.horse_dir = 1

        ricardo_y = self.sh - len(self.ricardo_ascii) - 5
        if ricardo_y > 0:
            for i, line in enumerate(self.ricardo_ascii):
                color = self.COLOR_YELLOW if i < len(self.ricardo_ascii)-1 else self.COLOR_RED
                self.safe_addstr(ricardo_y + i, self.horse_x, line, color)

    def draw_input_box(self):
        if not self.input_mode: return
            
        box_w = min(50, self.sw - 5)
        box_h = 6
        box_x = (self.sw - box_w) // 2
        box_y = (self.sh - box_h) // 2
        
        self.safe_addstr(box_y, box_x, "╔" + "═"*(box_w-2) + "╗", self.COLOR_RED)
        for y in range(box_y+1, box_y+box_h-1):
            self.safe_addch(y, box_x, "║", self.COLOR_RED)
            self.safe_addch(y, box_x + box_w - 1, "║", self.COLOR_RED)
        self.safe_addstr(box_y+box_h-1, box_x, "╚" + "═"*(box_w-2) + "╝", self.COLOR_RED)

        self.safe_addstr(box_y + 1, box_x + 3, "✨ 许下你的新年愿望 ✨", self.COLOR_YELLOW)
        display_txt = self.wish_text.ljust(box_w - 6)
        self.safe_addstr(box_y + 2, box_x + 3, display_txt, self.COLOR_WHITE)
        self.safe_addstr(box_y + 3, box_x + 3, "─"*(box_w-6), self.COLOR_CYAN)
        self.safe_addstr(box_y + 4, box_x + 3, "[Enter 确认]  [ESC 取消]", self.COLOR_PINK)

    def run(self):
        self.stdscr.nodelay(1)
        tree_rel_positions_global = []
        
        while self.running:
            self.update_size()
            self.stdscr.clear()
            self.frame_count += 1
            
            if self.frame_count % 15 == 0:
                self.tree_sway_target = random.randint(-2, 2)
            if abs(self.tree_sway_current - self.tree_sway_target) > 0.01:
                self.tree_sway_current += (self.tree_sway_target - self.tree_sway_current) * self.TREE_SWAY_SPEED

            self.draw_snow()
            self.draw_stars()
            trunk_y, trunk_x, tree_rel_pos = self.draw_tree()
            tree_rel_positions_global = tree_rel_pos
            
            self.draw_decorations(trunk_y, trunk_x)
            self.draw_red_packets()
            self.draw_fireworks()
            self.draw_ground()
            self.draw_panel()
            self.draw_ricardo()
            
            if not self.input_mode and self.wishes:
                for i, wish in enumerate(self.wishes[-self.MAX_WISHES_DISPLAY:]):
                    self.safe_addstr(2 + i, 8, f"🧧 {wish[:self.sw-38]}", self.COLOR_YELLOW)
            
            self.draw_input_box()
            
            self._handle_input(tree_rel_positions_global)
            
            if not self.input_mode:
                self.stdscr.nodelay(1)
            
            self.stdscr.refresh()
            time.sleep(0.05)

    def _handle_input(self, tree_rel_positions_global):
        try:
            key = self.stdscr.getch()
        except:
            key = -1
        
        if key == -1:
            return
        elif key == curses.KEY_RESIZE:
            self.update_size()
        elif self.input_mode:
            self._handle_input_mode(key)
        else:
            self._handle_normal_mode(key, tree_rel_positions_global)

    def _handle_input_mode(self, key):
        if key == 10:
            if self.wish_text:
                self.wishes.append(self.wish_text)
                self.trigger_fireworks(3)
                self.trigger_red_packets(15)
            self.input_mode = False
            self.wish_text = ""
        elif key == 27:
            self.input_mode = False
            self.wish_text = ""
        elif key in (127, 8, curses.KEY_BACKSPACE):
            self.wish_text = self.wish_text[:-1]
        elif key != -1 and len(self.wish_text) < 45:
            if 32 <= key <= 126:
                self.wish_text += chr(key)

    def _handle_normal_mode(self, key, tree_rel_positions_global):
        if key == ord('q'): self.running = False
        elif key == ord('w'): 
            self.input_mode = True
            self.stdscr.nodelay(0)
        elif key == ord('a'): self.add_decoration("lanterns", tree_rel_positions_global)
        elif key == ord('k'): self.add_decoration("knots", tree_rel_positions_global)
        elif key == ord('s'): 
            if self.tree_layers < self.MAX_TREE_LAYERS: self.tree_layers += 1
        elif key == ord('d'): self.trigger_red_packets(30)
        elif key == ord('f'): self.trigger_fireworks(5)
        elif key == ord('r'): self.reset()

def main(stdscr):
    scene = NewYearScene(stdscr)
    scene.run()

if __name__ == "__main__":
    curses.wrapper(main)
