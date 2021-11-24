# Write your code here :-)
import time
import board
import displayio
import terminalio
from adafruit_gizmo import tft_gizmo
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_circuitplayground import cp
from adafruit_progressbar.progressbar import ProgressBar
from simpleio import map_range
from digitalio import DigitalInOut, Direction, Pull

button_a = DigitalInOut(board.A2)
button_a.direction = Direction.INPUT
button_a.pull = Pull.UP

button_b = DigitalInOut(board.A1)
button_b.direction = Direction.INPUT
button_b.pull = Pull.UP


#Set display constants
BACKGROUND_COLOR = 0x49523b  # Gray
TEXT_COLOR = 0xFFFF00  # Red
BORDER_COLOR = 0xAAAAAA  # Light Gray
STATUS_COLOR = BORDER_COLOR


countdown = 0 #  variable for the step goal progress bar
clock = 0 #  variable used to keep track of time for the steps per hour counter
clock_count = 0 #  holds the number of hours that the step counter has been running
clock_check = 0 #  holds the result of the clock divided by 3600 seconds (1 hour)
last_step = 0 #  state used to properly counter steps
mono = time.monotonic() #  time.monotonic() device
mode = 1 #  state used to track screen brightness
steps_log = 0 #  holds total steps to check for steps per hour
steps_remaining = 0 #  holds the remaining steps needed to reach the step goal
sph = 0 #  holds steps per hour
step_goal = 5

#-------------------- FUNCTIONS FOR BUTTON --------------------#
def touch_a():
    return not button_a.value

def touch_b():
    return not button_b.value

#-------------------- FUNCTIONS FOR DISPLAY --------------------#
def wrap_in_tilegrid(filename:str):
    # CircuitPython 6 & 7 compatible
    odb = displayio.OnDiskBitmap(open(filename, "rb"))
    return displayio.TileGrid(
        odb, pixel_shader=getattr(odb, 'pixel_shader', displayio.ColorConverter())
    )

    # # CircuitPython 7+ compatible
    # odb = displayio.OnDiskBitmap(filename)
    # return displayio.TileGrid(odb, pixel_shader=odb.pixel_shader)

def make_background(width, height, color):
    color_bitmap = displayio.Bitmap(width, height, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = color

    return displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)

def load_font(fontname, text):
    font = bitmap_font.load_font(fontname)
    font.load_glyphs(text.encode('utf-8'))
    return font

def make_label(text, x, y, color, font=terminalio.FONT):
    if isinstance(font, str):
        font = load_font(font, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    text_area = Label(font, text=text, color=color)
    text_area.x = x
    text_area.y = y
    return text_area

def set_label(label, value, max_length):
    text = "{}".format(value)
    if len(text) > max_length:
        text = text[:max_length-3] + "..."
    label.text = text

def set_status(label, action_text, player):
    label.text = "{} on {}".format(action_text, player)
    _, _, label_width, _ = label.bounding_box
    label.x = display.width - 10 - label_width

display = tft_gizmo.TFT_Gizmo()
group = displayio.Group()
display.show(group)


# Draw the text fields
#goal_label = make_label("None", 12, 30, TEXT_COLOR, font="/fonts/LibreBodoniv2002-Bold-27.bdf")
goal_label = label.Label(bitmap_font.load_font("/fonts/LibreBodoniv2002-Bold-27.bdf"),text="",color=0xFFFF00)
goal_label.x=0
goal_label.y=40
#count_label = make_label("None", 12, 60, TEXT_COLOR, font="/fonts/Roboto-Black-48.bdf")
count_label = label.Label(bitmap_font.load_font("/fonts/Anton-Regular-104.bdf"),text="None",color=0xFFFF00)
count_label.x=-20
count_label.y=150
#title_label = make_label("None", 12, 120, TEXT_COLOR, font="/fonts/LibreBodoniv2002-Bold-27.bdf")
#sph_count = make_label("None", 12, 150, TEXT_COLOR, font="/fonts/LibreBodoniv2002-Bold-27.bdf")
#sph_label = make_label("None", 12, 180, TEXT_COLOR, font="/fonts/LibreBodoniv2002-Bold-27.bdf")
#group.pop()
#group.append(make_background(240, 240, BACKGROUND_COLOR))
#border = Rect(4, 4, 232, 200, outline=BORDER_COLOR, stroke=2)
group.append(goal_label)
group.append(count_label)
#group.append(title_label)
#group.append(sph_count)
#group.append(sph_label)
#group.append(border)
step_count = 0
previous_steps = 0
press_count=0
press_count_b=0
number_when_pressed=0
to_be_reset = False
showing_prev_steps = False
#set_label(goal_label, "B", 18)
count_label.text = "{:6.0f}".format(0)
#set_label(title_label, "Steps", 18)
#set_label(sph_count, "", 18)
#set_label(sph_label, "Steps Per Hour", 18)

#  creating the ProgressBar object
bar_group = displayio.Group()
prog_bar = ProgressBar(1, 1, 239, 25, bar_color=0xFFFF00)
bar_group.append(prog_bar)
group.append(bar_group)

while True:
    if(to_be_reset==False):
        #button stuff
        if touch_b():
            showing_prev_steps = True
            while touch_b():
                cp.play_tone(1400, 0.20) #40 for testing 4000 for actual
                time.sleep(0.1)
                while(showing_prev_steps):
                    goal_label.text = "Old Steps"
                    count_label.text = "{:6.0f}".format(previous_steps)
                    if touch_b():
                        goal_label.text = ""
                        count_label.text = "{:6.0f}".format(step_count)
                        showing_prev_steps = False
        if touch_a() and step_count>0:
            if((press_count==0) or (number_when_pressed!=step_count)):
                press_count =1
                number_when_pressed=step_count
            else:
                press_count=press_count +1
            while touch_a():
                cp.play_tone(2000, 0.20) #40 for testing 4000 for actual
                time.sleep(0.1)
                if press_count==3:
                    previous_steps = step_count
                    step_count=0
                    press_count=0
                    count_label.text = "{:6.0f}".format(step_count)
                pass

        #  creating the data for the ProgressBar
        countdown = map_range(step_count, 0, step_goal, 0.0, 1.0)

        if cp.shake(shake_threshold=10):
            #if step_goal - step_count > 0:
             #   step_count = 0
            #else:
            step_count = (step_count+1)%6
            #set_label(count_label, str(step_count), 18)
            count_label.text = "{:6.0f}".format(step_count)

            step_time = time.monotonic()
            clock = step_time - mono


            #  logging steps per hour
            if clock > 3600:
                #  gets number of hours to add to total
                clock_check = clock / 3600
                #  logs the step count as of that hour
                steps_log = step_count
                #  adds the hours to get a new hours total
                clock_count += round(clock_check)
                #  divides steps by hours to get steps per hour
                sph = steps_log / clock_count
                #  adds the sph to the display
                #set_label(sph_count,'%d' % sph,set_label,18)
                #  resets clock to count to the next hour again
                clock = 0
                mono = time.monotonic()

            #  adjusting countdown to step goal
            #prog_bar.progress = float(countdown)

        #  displaying countdown to step goal
        if step_goal - step_count > 0:
            prog_bar.progress=float(countdown)
            steps_remaining = step_goal - step_count
            string = str(steps_remaining)+' Steps Remaining'
            #set_label(goal_label , string,18)
        else:
            countdown = map_range(step_count, 0, step_goal, 0.0, 1.0)
            prog_bar.progress=float(countdown)
            print(step_count)
            #set_label(goal_label,'Steps Goal Met!',18)
            #put button function here, and ADD A SOUND
            if(last_count != step_count):
                cp.play_tone(1240, 1)
                cp.play_tone(1240, 1)
                cp.play_tone(1400, 1)
                cp.stop_tone()
                to_be_reset = True
            #set_label(count_label, str(0), 18)
            #step_count = 0
            #time.sleep(5)
            #step_count = 0

        last_count = step_count
    else:
        while(to_be_reset):
            goal_label.text = "Goal Met"
            if touch_a():
                press_count_b = press_count_b +1
                while touch_a():
                    cp.play_tone(2000, 0.20)
                    time.sleep(0.1)
                    if press_count_b==3:
                        previous_steps = step_count
                        step_count=0
                        press_count=0
                        press_count_b=0
                        count_label.text = "{:6.0f}".format(step_count)
                        goal_label.text = ""
                        to_be_reset = False
                    pass

while len(group):
    group.pop()
'''
from adafruit_circuitplayground import cp

while True:
    if cp.shake(shake_threshold=20):
        print("Shake detected more easily than before!")
'''