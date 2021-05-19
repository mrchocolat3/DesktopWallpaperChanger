import os
import sys
import datetime
import GoogleCalendar
import time
import weekDay
from PIL import Image, ImageFont, ImageDraw

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
RESOURCE_PATH = os.path.join(BASE_PATH, "resources")

# Change the Background script
cmd = f"""/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""


bold_font = ImageFont.truetype(os.path.join(RESOURCE_PATH, "Blinker-Black.ttf"), 120)
regular_font = ImageFont.truetype(os.path.join(RESOURCE_PATH, "Blinker-Regular.ttf"), 30)
regular_text = " days left"
temp_image = os.path.join(RESOURCE_PATH, "temp.png")


def get_Image():
    image = Image.open(os.path.join(RESOURCE_PATH, "Motivation.jpg"))
    image.putalpha(245)
    imageEditable = ImageDraw.Draw(image)
    return image, imageEditable

def save_Image(image):
    image.save(temp_image)
    os.system(cmd%temp_image)
    os.system("killall Dock")

class Color:
    DarkBlue = (66, 135, 245) 
    LightBlue = (92, 198, 255)

    DarkGreen = (47, 148, 54)
    LightGreen = (70, 212, 80)

    White = (255, 255, 255)
    Black = (20, 20, 20)

    Tomato = (219, 50, 50)
    Orange = (255, 123, 0)

    Grey = (150, 150, 150)


def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)


def tW(s, f):
    return f.getmask(s).getbbox()[2]

def tH(s, f):
    return f.getmask(s).getbbox()[3] + f.getmetrics()[1]


def get_image_dimensions(Image):
    return Image.size


def align_center(image, imageEditable):
    today = datetime.date.today()
    final_date = datetime.date(2022, 1, 1)
    days_left = (final_date - today).days
    bold_text = f"{days_left}"

    imageWidth, imageHeight = get_image_dimensions(image)
    bfontWidth, bfontHeight = get_text_dimensions(bold_text, bold_font)
    rfontWidth, rfontHeight = get_text_dimensions(regular_text, regular_font)

    centerX = (bfontWidth / 2) + 40 # 780  # imageWidth / 2
    centerY = imageHeight - bfontHeight - 20 # imageHeight - 800  # imageHeight / 2

    bCenterX = centerX - (bfontWidth / 2)
    bCenterY = centerY - (bfontHeight / 2)

    rCenterX = bfontWidth + (centerX - (rfontWidth / 2) - 20)
    rCenterY = centerY + (rfontHeight / 2) + 15

    drawText(imageEditable, (rCenterX, rCenterY), regular_text, Color.Tomato, regular_font)
    drawText(imageEditable, (bCenterX, bCenterY), bold_text, Color.Tomato, bold_font)


def renderInfo(text, xy, imageEditable):
    drawText(imageEditable, xy, text, (255, 255, 255), bold_font)


def drawText(image, position, text, color, font):
    image.text(position, text, color, font)


def getTime(event):
    return event.strftime("%I:%m %p")


def updateTasks(image):
    GoogleCalendar.main(2)
    tasks = GoogleCalendar.getEvents()

    currentTask = f"Current Task: {tasks[0]['summary']} | {getTime(tasks[0]['startTime'])} - {getTime(tasks[0]['endTime'])}"
    nextTask = f"Next Task:{tasks[1]['summary']} | {getTime(tasks[1]['startTime'])} - {getTime(tasks[1]['endTime'])}"

    if currentTask.startswith("Current Task: Nothing"):
        drawText(image, (40, 50), currentTask, Color.Grey, regular_font)
        drawText(image, (40, 80), nextTask, Color.LightBlue, regular_font)
    else:
        drawText(image, (40, 50), currentTask, Color.LightBlue, regular_font)
        drawText(image, (40, 80), nextTask, Color.Grey, regular_font)

    GoogleCalendar.clearEvents()


def getSummaryColor(day):
    weekDayType = weekDay.get_weekDayType(day)
    if weekDayType == "funDay": return Color.LightGreen
    if weekDayType == "hardDay": return Color.Tomato
    if weekDayType == "demiHardDay": return Color.Orange
    if weekDayType == "normalDay": return Color.DarkBlue

def updateDay(image):
    today = datetime.datetime.now().strftime("%a")
    todaySummary = weekDay.get_weekDaySummary(today)
    activityForToday = weekDay.get_Activity(today)
    
    msg_font = ImageFont.truetype(os.path.join(RESOURCE_PATH, "Blinker-Regular.ttf"), 20)
    msg_head_font = ImageFont.truetype(os.path.join(RESOURCE_PATH, "Blinker-Black.ttf"), 40)
    main_msg = "Today is "
    msgW, msgH = get_text_dimensions(main_msg, msg_head_font)
    # -------- Update What is TODAY 
    drawText(image, (40, 200), main_msg, Color.Tomato, msg_head_font)
    drawText(image, (40 + msgW + 10, 200), todaySummary.upper(), getSummaryColor(today), msg_head_font)
    # -------- END

    # -------- Write Todays Activity
    drawText(image, (40, 200 + msgH + 10), "Home Work: ", Color.Tomato, msg_font)
    drawText(image, (45 + tW("Home Work: ", msg_font), 200 + msgH + 10), activityForToday['hw'].upper(), getSummaryColor(today), msg_font)
    
    drawText(image, (40, 200 + tH("hw", msg_font) + 40 + 15), "Study: ", Color.Tomato, msg_font)
    drawText(image, (45 + tW("Study: ", msg_font), 200 + tH("st", msg_font) + 40 + 15), activityForToday['st'].upper(), getSummaryColor(today), msg_font)

    drawText(image, (40, 200 + tH("oa", msg_font) + 70 + 10), "Other Activities: ", Color.Tomato, msg_font)
    drawText(image, (45 + tW("Other Activities: ", msg_font), 200 + tH("st", msg_font) + 70 + 10), activityForToday['oa'].upper(), getSummaryColor(today), msg_font)

def updateImage(image, imageEditable):
    print("-"*40)
    print("Updating days left next year")
    align_center(image, imageEditable)
    print("Updating the day")
    updateDay(imageEditable)
    print("Updatind today's tasks")
    updateTasks(imageEditable)
    print("Saving Image")
    save_Image(image)
    print("-"*40)
def writeOnImage(imageEditable, text, color, position):
    msg_font = ImageFont.truetype(os.path.join(RESOURCE_PATH, "Blinker-Regular.ttf"), 20)
    drawText(imageEditable, position, text, color, msg_font)


if __name__ == "__main__":
    # updateImage()
    while True:
        try:
            i, ie = get_Image()
            updateImage(i, ie) 
            with open(os.path.join(BASE_PATH, "log.txt"), "a+") as f:
                now = datetime.datetime.now()
                currentDateTime = now.strftime("%d/%m/%Y %I:%M %p")
                text = f"\n[!] [{currentDateTime}] -> Script Running"
                f.write(text)
            print("waiting 5 minutes")
            time.sleep(60 * 5)
        except Exception as e:
            print(e)
            er = f"Error:{e}"
            with open(os.path.join(BASE_PATH, "log.txt"), "a+") as f:
                now = datetime.datetime.now()
                currentDateTime = now.strftime("%d/%m/%Y %H:%M:%S")
                text = f"\n[x] [ {currentDateTime} ] -> {e}\n[!]Waiting 1 minute and trying again\n"
                f.write(text)

            if er.__contains__("server") or er.__contains__("network"):
                i, ie = get_Image()
                drawText(ie,(40, 40), "No Internet Connection!", Color.Tomato, regular_font)
                drawText(ie,(40, 70), "Waiting for 5 to 6 minutes and trying again", Color.DarkBlue, regular_font)
                updateDay(ie)
                align_center(i, ie)
                save_Image(i)
            print("\nWaiting 5 minutes")
            time.sleep(60 * 5)
            continue
        except KeyboardInterrupt: 
            with open(os.path.join(BASE_PATH, "log.txt"), "a+") as f:
                now = datetime.datetime.now()
                currentDateTime = now.strftime("%d/%m/%Y %H:%M:%S")
                text = f"\n[x] [ {currentDateTime} ] -> KeyboardInterrupted\n"
                f.write(text) 
            print("KeyboardInterrupted!")
            break

    print("exiting....")
    os.system("exit")
    sys.exit()
