import random


def rotate(speed, speed_x, speed_y):
    direction = random.choice(["up", "right", "down", "left"])
    angle = 0
    if direction == "up":
        angle = 180
        speed_x = 0
        speed_y = -speed
    elif direction == "right":
        angle = 90
        speed_x = speed
        speed_y = 0
    elif direction == "down":
        angle = 0
        speed_x = 0
        speed_y = speed
    elif direction == "left":
        angle = -90
        speed_x = -speed
        speed_y = 0
    
    return angle, speed_x, speed_y

def rotate_incorrect(speed, speed_x, speed_y):
    direction = random.choice(["up", "right", "down", "left"])
    angle = 0
    if direction == "up":
        angle = 180
        speed_x = 0
        speed_y = speed
    elif direction == "right":
        angle = 90
        speed_x = -speed
        speed_y = 0
    elif direction == "down":
        angle = 0
        speed_x = 0
        speed_y = -speed
    elif direction == "left":
        angle = -90
        speed_x = speed
        speed_y = 0
    
    return angle, speed_x, speed_y

def test_rotate(rotate_function, direction, speed, speed_x, speed_y):
    rotate = rotate_function
    direction = direction
    speed = speed
    speed_x = speed_x
    speed_y = speed_y

    speed_x_previous = speed_x
    speed_y_previous = speed_y

    result1 = False
    result2 = False

    result = False

    angle, speed_x, speed_y = rotate(speed, speed_x, speed_y)

    if angle == 180:
        if speed_x == speed_x_previous:
            result1 = True
        if speed_y == -speed_y_previous:
            result2 = True

    if angle == 90:
        if speed_x - speed  == speed_x_previous:
            result1 = True
        if speed_y_previous - speed == speed_y:
            result2 = True

    if angle == 0:
        if speed_x == speed_x_previous:
            result1 = True
        if speed_y == speed_y_previous:
            result2 = True

    if angle == -90:
        if speed_x_previous - speed == speed_x:
            result1 = True
        if speed_y_previous - speed == speed_y:
            result2 = True

    if result1 and result2:
        result = True

    return angle, result

def test_double_rotate(rotate_function, direction, speed, speed_x, speed_y):
    rotate = rotate_function
    direction = direction
    speed = speed
    speed_x = speed_x
    speed_y = speed_y

    speed_x_previous = speed_x
    speed_y_previous = speed_y

    result = True

    angle, speed_x, speed_y = rotate(speed, speed_x, speed_y)
    rotate(speed, speed_x, speed_y)

    return result


speed = 1

start_direction = "down"

speed_x = 0
speed_y = speed

print(speed)
print(speed_x, speed_y)

angle, result = test_rotate(rotate, start_direction, speed, speed_x, speed_y)

print(angle)
print(result)
print()

angle, result = test_rotate(rotate_incorrect, start_direction, speed, speed_x, speed_y)

print(angle)
print(result)
