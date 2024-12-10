import pygame

# Initialize Pygame font
pygame.font.init()
font = pygame.font.SysFont(None, 24)

class LogicGate:
    def __init__(self, gate_type, x, y):
        self.gate_type = gate_type
        self.x = x
        self.y = y
        self.inputs = [0] * self.num_inputs()
        self.output = 0

    def num_inputs(self):
        if self.gate_type in ['AND', 'OR', 'NAND', 'NOR', 'XOR']:
            return 2
        elif self.gate_type == 'NOT':
            return 1

    def compute_output(self):
        if self.gate_type == 'AND':
            self.output = self.inputs[0] and self.inputs[1]
        elif self.gate_type == 'OR':
            self.output = self.inputs[0] or self.inputs[1]
        elif self.gate_type == 'NOT':
            self.output = not self.inputs[0]
        elif self.gate_type == 'NAND':
            self.output = not (self.inputs[0] and self.inputs[1])
        elif self.gate_type == 'NOR':
            self.output = not (self.inputs[0] or self.inputs[1])
        elif self.gate_type == 'XOR':
            self.output = self.inputs[0] ^ self.inputs[1]

    def draw(self, screen):
        # Draw gate body
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, 80, 80))

        # Draw gate type label
        text = font.render(self.gate_type, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.x + 40, self.y + 40))
        screen.blit(text, text_rect)

        # Draw input/output lines
        if self.num_inputs() == 2:
            pygame.draw.line(screen, (150, 150, 150), (self.x - 40, self.y + 80 / 3), (self.x, self.y + 80 / 3))
            pygame.draw.line(screen, (150, 150, 150), (self.x - 40, self.y + 2 * 80 / 3), (self.x, self.y + 2 * 80 / 3))
            if self.inputs[0] == 1:
                pygame.draw.line(screen, (0, 255, 0), (self.x - 40, self.y + 80 / 3), (self.x, self.y + 80 / 3), 5)
            if self.inputs[1] == 1:
                pygame.draw.line(screen, (0, 255, 0), (self.x - 40, self.y + 2 * 80 / 3), (self.x, self.y + 2 * 80 / 3), 5)
        elif self.num_inputs() == 1:
            pygame.draw.line(screen, (150, 150, 150), (self.x - 40, self.y + 80 / 2), (self.x, self.y + 80 / 2))
            if self.inputs[0] == 1:
                pygame.draw.line(screen, (0, 255, 0), (self.x - 40, self.y + 80 / 2), (self.x, self.y + 80 / 2), 5)

        pygame.draw.line(screen, (150, 150, 150), (self.x + 80, self.y + 80 / 2), (self.x + 80 + 40, self.y + 80 / 2))
        if self.output == 1:
            pygame.draw.line(screen, (255, 0, 0), (self.x + 80, self.y + 80 / 2), (self.x + 80 + 40, self.y + 80 / 2), 5)

    def is_inside(self, pos):
        return self.x <= pos[0] <= self.x + 80 and self.y <= pos[1] <= self.y + 80

    def set_input(self, index, value):
        self.inputs[index] = value

    def get_output(self):
        return self.output

    def get_input_positions(self):
        if self.num_inputs() == 2:
            return [(self.x - 40, self.y + 80 / 3), (self.x - 40, self.y + 2 * 80 / 3)]
        else:
            return [(self.x - 40, self.y + 80 / 2)]

    def get_output_position(self):
        return (self.x + 80, self.y + 80 / 2, self.x + 80 + 40, self.y + 80 / 2)

    def get_type(self):
        return self.gate_type

    def get_output_table(self):
        if self.gate_type == 'AND':
            return ['a b | c', '0 0 | 0', '0 1 | 0', '1 0 | 0', '1 1 | 1']
        elif self.gate_type == 'OR':
            return ['a b | c', '0 0 | 0', '0 1 | 1', '1 0 | 1', '1 1 | 1']
        elif self.gate_type == 'NOT':
            return ['a | c', '0 | 1', '1 | 0']
        elif self.gate_type == 'NAND':
            return ['a b | c', '0 0 | 1', '0 1 | 1', '1 0 | 1', '1 1 | 0']
        elif self.gate_type == 'NOR':
            return ['a b | c', '0 0 | 1', '0 1 | 0', '1 0 | 0', '1 1 | 0']
        elif self.gate_type == 'XOR':
            return ['a b | c', '0 0 | 0', '0 1 | 1', '1 0 | 1', '1 1 | 0']
