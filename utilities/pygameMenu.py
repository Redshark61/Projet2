import pygame
import menu


def createBGSurface(text: pygame.Rect, offset: int = 10, color: tuple[int] = (0, 0, 0)) -> pygame.Surface:
    """
    Create a background surface for a given rect (text)
    """
    bgBack = pygame.Surface((text.width + offset, text.height + offset))
    bgBack.fill(color)
    bgBack.set_alpha(200)
    return bgBack


def clearSurface(surface: pygame.Surface):
    """
    Clear the surface with a black color
    """
    surface.fill((0, 0, 0))


def createButton(screen, incomingState: bool, goingState: bool, text: str, position: str = 'bl') -> tuple[int, int]:
    """
    Create a simple button to switch between states :
        - incomingState : the state the menu IS on click
        - goingState : the state the menu WILL be on click

    The position argument is a string that can be :
        - `bl` : bottom left
        - `br` : bottom right
        - `tl` : top left
        - `tr` : top right
    """

    # Load the font
    backButton = menu.Menu.buttonFont.render(text, True, (0, 0, 0))
    # Get its rect
    backButtonRect = backButton.get_rect()

    # Create a background surface
    bg = createBGSurface(backButtonRect, color=(255, 255, 255))
    bgRect = bg.get_rect()
    bg.set_alpha(255)
    # Center the text in the middle of the background
    backButtonRect.centerx = bgRect.width / 2
    # Display the text on the background
    bg.blit(backButton, backButtonRect)

    # check the position argument
    if 'b' in position:
        bgRect.y = screen.get_height() - bgRect.height - 50
    if 'l' in position:
        bgRect.x = 50
    if 'r' in position:
        bgRect.x = screen.get_width() - bgRect.width - 100
    if 't' in position:
        bgRect.y = 50

    # If the mouse is on the button, change the color
    if bgRect.collidepoint(pygame.mouse.get_pos()):
        bg.set_alpha(100)
        # Detect the click on the button
        if pygame.mouse.get_pressed()[0]:
            incomingState = False
            goingState = True

    # Display the button
    screen.blit(bg, bgRect)
    return incomingState, goingState


# Get a dict wich store the key (int) and value of the letters
letters = {x: pygame.key.key_code(x) for x in "abcdefghijklmnopqrstuvwxyz1234567890"}


def textInput(screen: pygame.Surface, activeColor: tuple[int, int, int], passiveColor: tuple[int, int, int]):
    """
    Create a text input, and get the input of the player
    """

    # Get the size of the input button
    width = screen.get_width() / 3
    height = menu.Menu.buttonFont.get_height() + 10
    centerx = screen.get_width() / 2 - width / 2
    centery = screen.get_height() / 2 - height / 2
    inputRect = pygame.Rect(centerx, centery, width, height)

    # Toggle the active state of the input button
    if pygame.mouse.get_pressed()[0]:
        menu.Menu.active = inputRect.collidepoint(pygame.mouse.get_pos())

    # Get the pressed key
    pressed = pygame.key.get_pressed()
    if pressed and menu.Menu.active:

        # Check for backspace
        if pressed[pygame.K_BACKSPACE]:

            # get text input from 0 to -1 i.e. end.
            menu.Menu.userText = menu.Menu.userText[:-1]
        # Check for enter
        elif pressed[pygame.K_RETURN]:
            # Stop the loop, deactivate the input button and close the menu
            menu.Menu.active = False
            menu.Menu.running = False
            menu.Menu.isNameMenuOpen = False

        # If the player doesn't press backspace or enter, add the key to the text input
        else:
            # We want the player to only click once
            if not menu.Menu.pressedOnce:
                for key in letters:
                    # Check wich key is pressed
                    if pressed[letters[key]]:
                        menu.Menu.userText += key[0]
                        menu.Menu.pressedOnce = True
                        break
            else:
                menu.Menu.pressedOnce = False

    # Change the color of the input button
    if menu.Menu.active:
        color = activeColor
    else:
        color = passiveColor

    # draw rectangle and argument passed which should be on screen
    pygame.draw.rect(screen, color, inputRect)
    textSurface = menu.Menu.buttonFont.render(menu.Menu.userText, True, (255, 255, 255))

    # render at position stated in arguments
    screen.blit(textSurface, (inputRect.x+5, inputRect.y+5))

    # set width of textfield so that text cannot get
    # outside of user's text input
    inputRect.w = max(100, textSurface.get_width()+10)
