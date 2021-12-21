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


def createButton(screen, incomingState, goingState, text, position: str = 'bl'):

    buttonFont = pygame.font.Font(
        "./assets/font/Knewave-Regular.ttf", 50)
    # Create a back button
    backButton = buttonFont.render(text, True, (0, 0, 0))
    backButtonRect = backButton.get_rect()
    bg = createBGSurface(backButtonRect, color=(255, 255, 255))
    bgRect = bg.get_rect()
    bg.set_alpha(255)
    backButtonRect.centerx = bgRect.width / 2
    bg.blit(backButton, backButtonRect)
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


letters = {x: pygame.key.key_code(x) for x in "abcdefghijklmnopqrstuvwxyz1234567890"}


def textInput(screen, activeColor, passiveColor):
    width = screen.get_width() / 3
    height = menu.Menu.buttonFont.get_height() + 10
    centerx = screen.get_width() / 2 - width / 2
    centery = screen.get_height() / 2 - height / 2
    input_rect = pygame.Rect(centerx, centery, width, height)

    if pygame.mouse.get_pressed()[0]:
        menu.Menu.active = input_rect.collidepoint(pygame.mouse.get_pos())

    pressed = pygame.key.get_pressed()
    if pressed and menu.Menu.active:

        # Check for backspace
        if pressed[pygame.K_BACKSPACE]:

            # get text input from 0 to -1 i.e. end.
            menu.Menu.userText = menu.Menu.userText[:-1]
        elif pressed[pygame.K_RETURN]:
            menu.Menu.active = False
            menu.Menu.running = False
            menu.Menu.isNameMenuOpen = False
        else:
            if not menu.Menu.pressedOnce:
                for key in letters:
                    if pressed[letters[key]]:
                        menu.Menu.userText += key[0]
                        print(key)
                        menu.Menu.pressedOnce = True
                        break
            else:
                menu.Menu.pressedOnce = False
            # menu.Menu.userText += pygame.key.name(pressed)
            print(menu.Menu.userText)

    if menu.Menu.active:
        color = activeColor
    else:
        color = passiveColor

    # draw rectangle and argument passed which should
    # be on screen
    pygame.draw.rect(screen, color, input_rect)
    textSurface = menu.Menu.buttonFont.render(menu.Menu.userText, True, (255, 255, 255))

    # render at position stated in arguments
    screen.blit(textSurface, (input_rect.x+5, input_rect.y+5))

    # set width of textfield so that text cannot get
    # outside of user's text input
    input_rect.w = max(100, textSurface.get_width()+10)
