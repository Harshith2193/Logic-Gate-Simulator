import pygame
import sys

# Initialize Pygame
pygame.init()

# Display size
DISPLAY_WIDTH = 1500
DISPLAY_HEIGHT = 800

# Logic gate dimensions
GATE_SIZE = 80
GATE_PADDING = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
DARK_GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (150, 150, 0)

# Set up the display
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Interactive Logic Gate Simulator")

# Font
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

    def draw(self):
        # Draw gate body
        pygame.draw.rect(screen, BLACK, (self.x, self.y, GATE_SIZE, GATE_SIZE))

        # Draw gate type label
        text = font.render(self.gate_type, True, WHITE)
        text_rect = text.get_rect(center=(self.x + GATE_SIZE / 2, self.y + GATE_SIZE / 2))
        pygame.draw.rect(screen, BLACK, (text_rect.left - 5, text_rect.top - 5, text_rect.width + 10, text_rect.height + 10))
        screen.blit(text, text_rect)

        # Draw input/output lines and set inputs
        if self.num_inputs() == 2:
            pygame.draw.line(screen, GRAY, (self.x - GATE_PADDING, self.y + GATE_SIZE / 3), (self.x, self.y + GATE_SIZE / 3))
            pygame.draw.line(screen, GRAY, (self.x - GATE_PADDING, self.y + 2 * GATE_SIZE / 3), (self.x, self.y + 2 * GATE_SIZE / 3))
            # Input lines
            if self.inputs[0] == 1:
                pygame.draw.line(screen, GREEN, (self.x - GATE_PADDING, self.y + GATE_SIZE / 3), (self.x, self.y + GATE_SIZE / 3), 5)
            if self.inputs[1] == 1:
                pygame.draw.line(screen, GREEN, (self.x - GATE_PADDING, self.y + 2 * GATE_SIZE / 3), (self.x, self.y + 2 * GATE_SIZE / 3), 5)
        else:
            pygame.draw.line(screen, GRAY, (self.x - GATE_PADDING, self.y + GATE_SIZE / 2), (self.x, self.y + GATE_SIZE / 2))
            # Input line
            if self.inputs[0] == 1:
                pygame.draw.line(screen, GREEN, (self.x - GATE_PADDING, self.y + GATE_SIZE / 2), (self.x, self.y + GATE_SIZE / 2), 5)

        pygame.draw.line(screen, GRAY, (self.x + GATE_SIZE, self.y + GATE_SIZE / 2), (self.x + GATE_SIZE + GATE_PADDING, self.y + GATE_SIZE / 2))
        # Output line
        if self.output == 1:
            pygame.draw.line(screen, RED, (self.x + GATE_SIZE, self.y + GATE_SIZE / 2), (self.x + GATE_SIZE + GATE_PADDING, self.y + GATE_SIZE / 2), 5)

    def is_inside(self, pos):
        return self.x <= pos[0] <= self.x + GATE_SIZE and self.y <= pos[1] <= self.y + GATE_SIZE

    def set_input(self, index, value):
        self.inputs[index] = value

    def get_output(self):
        return self.output

    def get_input_positions(self):
        if self.num_inputs() == 2:
            return [(self.x - GATE_PADDING, self.y + GATE_SIZE / 3), (self.x - GATE_PADDING, self.y + 2 * GATE_SIZE / 3)]
        else:
            return [(self.x - GATE_PADDING, self.y + GATE_SIZE / 2)]

    def get_output_position(self):
        return (self.x + GATE_SIZE, self.y + GATE_SIZE / 2)

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

def main():
    gates = []
    connections = []
    selected_gate = None
    dragging = False
    connecting = False
    start_pos = None
    end_pos = None
    mouse_offset = (0, 0)
    gate_types = ['AND', 'OR', 'NOT', 'NAND', 'NOR', 'XOR']
    
    new_gate_index = 0  # Initialize new_gate_index here

    delete_box = pygame.Rect(DISPLAY_WIDTH - 150, DISPLAY_HEIGHT - 80, 120, 60)

    def create_gate(gate_type, x, y):
        gates.append(LogicGate(gate_type, x, y))

    def delete_gate(gate):
        gates.remove(gate)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Exit the program
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check if clicked on gate types in the menu
                    for i, gate_type in enumerate(gate_types):
                        menu_rect = pygame.Rect(10 + i * 150, 10, 140, 30)
                        if menu_rect.collidepoint(event.pos):
                            create_gate(gate_type, 50, 400)
                            break

                    # Check if clicked on inputs or outputs
                    for gate in gates:
                        if gate.is_inside(event.pos):
                            selected_gate = gate
                            dragging = True
                            mouse_offset = (event.pos[0] - gate.x, event.pos[1] - gate.y)
                            # Check output line
                            if gate.get_output_position()[0] <= event.pos[0] <= gate.get_output_position()[0] + GATE_PADDING:
                                connecting = True
                                start_pos = gate.get_output_position()
                            break
                    else:
                        selected_gate = None
                elif event.button == 3:
                    for gate in gates:
                        if gate.is_inside(event.pos):
                            connecting = True
                            start_pos = gate.get_output_position()
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                    connecting = False
                    end_pos = event.pos
                    # Check if connecting
                    if start_pos and end_pos:
                        for gate in gates:
                            if gate.is_inside(end_pos):
                                connections.append((start_pos, gate.get_input_positions()[0]))
                                gate.set_input(0, 1)  # Set the input to 1 for now
                                break
                        start_pos = None
                        end_pos = None
                    # Check if dropped over delete box
                    if selected_gate and delete_box.collidepoint(event.pos):
                        delete_gate(selected_gate)
                        selected_gate = None
            elif event.type == pygame.MOUSEMOTION:
                if dragging and selected_gate:
                    selected_gate.x = event.pos[0] - mouse_offset[0]
                    selected_gate.y = event.pos[1] - mouse_offset[1]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset all gates
                    for gate in gates:
                        gate.inputs = [0] * gate.num_inputs()
                        gate.output = 0
                elif event.key == pygame.K_n:
                    # Create new gate
                    new_gate_type = gate_types[new_gate_index]
                    create_gate(new_gate_type, 400, 300)
                    new_gate_index = (new_gate_index + 1) % len(gate_types)
                elif event.key == pygame.K_d:
                    # Delete selected gate
                    if selected_gate:
                        delete_gate(selected_gate)
                        selected_gate = None
                elif event.key == pygame.K_e:
                    # Edit selected gate
                    if selected_gate:
                        selected_gate.gate_type = gate_types[(gate_types.index(selected_gate.gate_type) + 1) % len(gate_types)]
                elif event.key == pygame.K_1:
                    # Toggle first input
                    if selected_gate and len(selected_gate.inputs) > 0:
                        selected_gate.inputs[0] = 1 - selected_gate.inputs[0]
                elif event.key == pygame.K_2:
                    # Toggle second input
                    if selected_gate and len(selected_gate.inputs) > 1:
                        selected_gate.inputs[1] = 1 - selected_gate.inputs[1]

        # Clear screen
        screen.fill(WHITE)

        # Draw all gates
        for gate in gates:
            gate.compute_output()
            gate.draw()

        # Draw connections
        for connection in connections:
            pygame.draw.line(screen, BLACK, connection[0], connection[1], 3)

        # Draw connecting line
        if connecting and start_pos:
            pygame.draw.line(screen, RED, start_pos, pygame.mouse.get_pos(), 3)

        # Draw output table on hover
        mouse_pos = pygame.mouse.get_pos()
        for gate in gates:
            if gate.is_inside(mouse_pos):
                output_table = gate.get_output_table()
                text_height = len(output_table) * 20
                pygame.draw.rect(screen, WHITE, (mouse_pos[0] + 20, mouse_pos[1], 160, text_height + 10))
                for idx, line in enumerate(output_table):
                    text_surface = font.render(line, True, BLACK)
                    screen.blit(text_surface, (mouse_pos[0] + 30, mouse_pos[1] + 5 + idx * 20))

        # Draw delete box
        pygame.draw.rect(screen, RED, delete_box)
        delete_text = font.render("DELETE", True, WHITE)
        delete_text_rect = delete_text.get_rect(center=delete_box.center)
        screen.blit(delete_text, delete_text_rect)

        # Draw horizontal menu
        for i, gate_type in enumerate(gate_types):
            menu_rect = pygame.Rect(10 + i * 150, 10, 140, 30)
            if menu_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, DARK_GRAY, menu_rect)
            else:
                pygame.draw.rect(screen, GRAY, menu_rect)
            text_surface = font.render(gate_type, True, WHITE)
            text_rect = text_surface.get_rect(center=menu_rect.center)
            screen.blit(text_surface, text_rect)

        # Update display
        pygame.display.flip()

if __name__ == "__main__":
    main()