"""
  颜色寻找并返回坐标

"""
import PIL.ImageGrab

# 坐标数组
coord = []


# screenshot = PIL.ImageGrab.grab(bbox=(710, 290,1210, 790))
# screenshot_pixels = screenshot.load()
# target_color = (254, 43, 51)

def color_search(target_color, screenshot, difference_lv):
    # print("-->",target_color)
    d_x = screenshot[0]
    d_y = screenshot[1]
    screenshot = PIL.ImageGrab.grab(bbox=screenshot)
    screenshot_pixels = screenshot.load()
    target_color = target_color
    for x in range(screenshot.size[0]):
        for y in range(screenshot.size[1]):
            pixel_color = screenshot_pixels[x, y]
            # 计算与目标颜色的差距
            diff = abs(pixel_color[0] - target_color[0]) + abs(pixel_color[1] - target_color[1]) + abs(
                pixel_color[2] - target_color[2])
            # 判断是否为目标颜色
            if diff < difference_lv:
                print("坐标--->", x + d_x, y + d_y)
                coord = (x + d_x, y + d_y)
                return coord

