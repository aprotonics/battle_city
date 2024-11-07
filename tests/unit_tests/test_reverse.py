
def reverse(direction, speed, speed_x, speed_y):
    if direction == "up":
        direction = "down"
        speed_y = speed
    elif direction == "right":
        direction = "left"
        speed_x = -speed
    elif direction == "down":
        direction = "up"
        speed_y = -speed
    elif direction == "left":
        direction = "right"
        speed_x = speed
    
    return direction, speed_x, speed_y

def reverse_incorrect(direction, speed, speed_x, speed_y):
    if direction == "up":
        direction = "down"
        speed_y = -speed
    elif direction == "right":
        direction = "left"
        speed_x = speed
    elif direction == "down":
        direction = "up"
        speed_y = speed
    elif direction == "left":
        direction = "right"
        speed_x = -speed
    
    return direction, speed_x, speed_y

def test_reverse(reverse_function, direction, speed, speed_x, speed_y):
    reverse = reverse_function
    direction = direction
    speed = speed
    speed_x = speed_x
    speed_y = speed_y

    direction_previous = direction
    speed_x_previous = speed_x
    speed_y_previous = speed_y

    result1 = False
    result2 = False
    result3 = False
    result4 = False

    result = False

    direction, speed_x, speed_y = reverse(direction, speed, speed_x, speed_y)

    if direction_previous == "up":
        if direction == "down" and speed_y == speed:
            result1 = True

    if direction_previous == "right":
        if direction == "left" and speed_x == -speed:
            result2 = True
    
    if direction_previous == "down":
        if direction == "up" and speed_y == -speed:
            result3 = True
    
    if direction_previous == "left":
        if direction == "right" and speed_x == speed:
            result4 = True

    if result1 or result2 or result3 or result4:
        result = True

    return result


speed = 1

speed_x = 1
speed_y = 1

direction = "down"

result = test_reverse(reverse, direction, speed, speed_x, speed_y)

print(result)

result = test_reverse(reverse_incorrect, direction, speed, speed_x, speed_y)

print(result)
