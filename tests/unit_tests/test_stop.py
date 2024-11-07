
def stop_correct(direction, rect_x, rect_y, speed_x, speed_y):
    if direction == "up":
        rect_y -= speed_y
    if direction == "right":
        rect_x -= speed_x
    if direction == "down":
        rect_y -= speed_y
    if direction == "left":
        rect_x -= speed_x
    
    speed_x = 0
    speed_y = 0

    return rect_x, rect_y, speed_x, speed_y

def stop_incorrect(direction, rect_x, rect_y, speed_x, speed_y):
    if direction == "up":
        rect_y -= 2 * speed_y
    if direction == "right":
        rect_x -= 2 * speed_x
    if direction == "down":
        rect_y -= 2 * speed_y
    if direction == "left":
        rect_x -= 2 * speed_x
    
    speed_x = 0
    speed_y = 0

    return rect_x, rect_y, speed_x, speed_y

def test_stop(stop_function, direction, rect_x, rect_y, speed_x, speed_y):
    stop = stop_function
    direction = direction
    rect_x = rect_x
    rect_y = rect_y
    speed_x = speed_x
    speed_y = speed_y

    rect_x_previous = rect_x
    rect_y_previous = rect_y
    speed_x_previous = speed_x
    speed_y_previous = speed_y

    result1 = False
    result2 = False
    result3 = False
    result4 = False

    result = False
    
    rect_x, rect_y, speed_x, speed_y = stop(direction, rect_x, rect_y, speed_x, speed_y)
    
    if direction == "right":
        if rect_x_previous - rect_x == speed_x_previous:
            result1 = True
    if direction == "left":
        if rect_x_previous - rect_x == speed_x_previous:
            result1 = True
    if direction == "up":
        if rect_y_previous - rect_y == speed_y_previous:
            result2 = True
    if direction == "down":
        if rect_y_previous - rect_y == speed_y_previous:
            result2 = True

    if speed_x == 0:
        result3 = True
    if speed_y == 0:
        result4 = True

    if direction == "right":
        if result1 and result3 and result4:
            result = True
    if direction == "left":
        if result1 and result3 and result4:
            result = True
    if direction == "up":
        if result2 and result3 and result4:
            result = True
    if direction == "down":
        if result2 and result3 and result4:
            result = True

    return result


rect_x = 100
rect_y = 100

speed_x = 1
speed_y = 1

direction = "down"

print(rect_x, rect_y)
print(speed_x, speed_y)

result = test_stop(stop_correct, direction, rect_x, rect_y, speed_x, speed_y)

print(result)

result = test_stop(stop_incorrect, direction, rect_x, rect_y, speed_x, speed_y)

print(result)
