import pygame
import menu
import Variables as var
import utilities


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


def createButton(screen, incomingState: bool, goingState: bool, text: str, position: str = 'bl', **kwargs) -> tuple[bool, bool]:
    """
    Create a simple button to switch between states :
        - `incomingState` : the state the menu IS on click
        - `goingState` : the state the menu WILL be on click

    The position argument is a string that can be :
        - `bl` : bottom left
        - `br` : bottom right
        - `tl` : top left
        - `tr` : top right

    The kwargs is used to pass other arguments when the button is clicked. To do so,
    add a pair of 'name', 'value' parameters to the kwargs, for example :
    `name="menu.Menu.running", value=False` if you want to stop the menu to run.

    The only things, think like if you
    were inside the createButton function, so instead of writing `name = "Menu.running"` you should write `name = "menu.Menu.running"`.
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

            # Maybe there are other arguments to assign value, so we use kwargs
            for key, value in kwargs.items():
                if key == 'name':
                    propertyName = value
                else:
                    propertyValue = value
                    exec(f"{propertyName} = {propertyValue}")

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


def slider(soundType: str, offsetY: int = 0):

    # x position of slider
    x = 500

    # Get the width of the slider depending on its type
    if soundType == 'sfx':
        width = menu.Menu.sliderWidthSfx
        index = 0
    elif soundType == 'ambient':
        width = menu.Menu.sliderWidthAmbient
        index = 1

    height = var.screen.get_height() / 2 + offsetY

    # Create a surface for the slider (background and foreground)
    bg = pygame.Surface((300, 20))
    fg = pygame.Surface((width, 20))

    # Colors
    bg.fill((255, 0, 0))
    fg.fill((0, 255, 0))

    # Position of the slider
    fgRect = fg.get_rect()
    bgRect = bg.get_rect()
    bgRect.centery = height
    fgRect.centery = height
    bgRect.x = x
    fgRect.x = x

    # Display the sliders
    var.screen.blit(bg, bgRect)
    var.screen.blit(fg, fgRect)

    # Display the circle wich you can drag
    dot = pygame.draw.circle(var.screen, (0, 0, 0), (x + width, height), 13)

    # If the player is hovering, are still clicking the current slider
    isClicking = (dot.collidepoint(pygame.mouse.get_pos()) or menu.Menu.sliderClicked[index])

    # If the player is hovering over the slider, and is clicking on the current slider
    if isClicking and pygame.mouse.get_pressed()[0] and menu.Menu.sliderType in (soundType, ''):
        menu.Menu.handled = True
        menu.Menu.sliderClicked[index] = True

        # slider type define wich slider is currently being dragged
        menu.Menu.sliderType = soundType

        if soundType == "ambient":
            menu.Menu.soundStateAmbient = True
            # Get the min between the width of the slider and 300px (not to go further than 300px)
            # and get the max between the width of the slider and 0px (not to go below than 0px)
            menu.Menu.sliderWidthAmbient = max(min(pygame.mouse.get_pos()[0] - x, 300), 0)
            soundVolume = menu.Menu.sliderWidthAmbient / 300
            var.volumeAmbient = soundVolume
        elif soundType == "sfx":
            menu.Menu.soundStateSfx = True
            menu.Menu.sliderWidthSfx = max(min(pygame.mouse.get_pos()[0] - x, 300), 0)
            soundVolume = menu.Menu.sliderWidthSfx / 300
            var.volumeSfx = soundVolume

        # In any case, re adjust the volume with the new values
        utilities.sounds.setVolume()

    # If the previous condition is false, then it means that the player is not clicking on the slider anymore
    else:
        menu.Menu.sliderClicked[index] = False
        menu.Menu.handled = False
        menu.Menu.sliderType = ''


def displayTitle(text: str, font: pygame.font.Font):
    """
    Display the title of the menu
    """
    title = font.render(text, True, (255, 255, 255))
    titleRect = title.get_rect()
    titleRect.center = ((var.screen.get_width() / 2), 50)
    var.screen.blit(title, titleRect)
