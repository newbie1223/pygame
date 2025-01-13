import pygame
from transformers import pipeline

# Set up a text generation model that runs locally
generator = pipeline("text-generation", model="gpt2")

def generate_typing_problems():
    """Generate typing problems using the local model"""
    prompt = "Generate 5 simple and meaningful typing problems, each consisting of a short sentence or phrase."
    response = generator(prompt, max_length=100, num_return_sequences=1, truncation=True)
    problems = response[0]["generated_text"]
    print("Generated problems:", problems)  # Debugging line to check generated text
    # Create a list of problems split by newline
    return [line.strip() for line in problems.split("\n") if line.strip()]

def typing_game():
    """Main typing game logic"""
    pygame.init()
    screen = pygame.display.set_mode((1500, 800))
    pygame.display.set_caption("Typing Game")
    clock = pygame.time.Clock()

    problems = generate_typing_problems()
    print("Problems list:", problems)  # Debugging line to check the problem list
    font = pygame.font.Font(None, 36)
    running = True
    current_problem = problems.pop(0) if problems else ""
    user_input = ""
    correct = False  # To track if the current input matches the problem

    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input == current_problem:
                        if problems:
                            current_problem = problems.pop(0)
                            user_input = ""
                            correct = False  # Reset when moving to the next problem
                        else:
                            running = False
                    else:
                        user_input = ""  # Reset the input on wrong answer
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]  # Remove last character
                else:
                    user_input += event.unicode  # Add character to input

        # Render the problem and the user's input
        problem_surface = font.render(current_problem, True, (0, 0, 0))
        input_surface = font.render(user_input, True, (0, 0, 255))

        # Highlight the part of the input that the user is currently typing
        highlighted_problem = ""
        for i, char in enumerate(current_problem):
            if i < len(user_input):
                if user_input[i] == char:
                    highlighted_problem += char  # Correctly typed character
                else:
                    highlighted_problem += "_"  # Incorrect character
            else:
                highlighted_problem += "_"

        highlighted_surface = font.render(highlighted_problem, True, (255, 0, 0))
        
        # Blit everything to the screen
        screen.blit(problem_surface, (50, 50))
        screen.blit(highlighted_surface, (50, 100))  # Display the highlighted problem
        screen.blit(input_surface, (50, 150))  # Display user input

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    typing_game()
