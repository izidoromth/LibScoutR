direction = "Backwards"

def get_index(matrix, value):
    return next(
        (row.index(value), index) for index, row in enumerate(matrix) if value in row
    )


def get_relative_direction(start_color, end_color):
    movement = None

    start_x, start_y = start_color
    end_x, end_y = end_color

    if (start_x - end_x) == 1:
        movement = "Left"
    # Going Right
    elif (start_x - end_x) == -1:
        movement = "Right"
    # Going Up
    if (start_y - end_y) == 1:
        movement = "Up"
    # Going Down
    elif (start_y - end_y) == -1:
        movement = "Down"

    return movement


def next_direction(came_from_color, current_color, going_to_color):
    dir = [
        ["Orange", "Red", "Blue"],
        ["Brown", "Purple", "Yellow"],
    ]
    global direction

    came_from_index = get_index(dir, came_from_color)
    current_index = get_index(dir, current_color)
    going_to_index = get_index(dir, going_to_color)

    last_movement_direction = get_relative_direction(came_from_index, current_index)
    going_to_position = get_relative_direction(current_index, going_to_index)
    output_direction = None

    if last_movement_direction == "Left":
        if going_to_position == "Right":
            if direction == "Foward":
                output_direction = "Backwards"
                direction = output_direction
            else:
               output_direction = "Foward" 
               direction = output_direction
        elif going_to_position == "Left":
                output_direction = direction
        elif going_to_position == "Up":
            output_direction = "Right"
        elif going_to_position == "Down":
            output_direction = "Left"

    elif last_movement_direction == "Right":
        if going_to_position == "Right":
            output_direction = direction
        elif going_to_position == "Left":
            if direction == "Foward":
                output_direction = "Backwards"
                direction = output_direction
            else:
               output_direction = "Foward" 
               direction = output_direction
        elif going_to_position == "Up":
            output_direction = "Left"
        elif going_to_position == "Down":
            output_direction = "Right"

    elif last_movement_direction == "Up":
        if going_to_position == "Right":
            output_direction = "Right"
        elif going_to_position == "Left":
            output_direction = "Left"
        elif going_to_position == "Up":
            output_direction = direction
        elif going_to_position == "Down":
            if direction == "Foward":
                output_direction = "Backwards"
                direction = output_direction
            else:
               output_direction = "Foward" 
               direction = output_direction

    elif last_movement_direction == "Down":
        if going_to_position == "Right":
            output_direction = "Left"
        elif going_to_position == "Left":
            output_direction = "Right"
        elif going_to_position == "Up":
            if direction == "Foward":
                output_direction = "Backwards"
                direction = output_direction
            else:
               output_direction = "Foward" 
               direction = output_direction
        elif going_to_position == "Down":
            output_direction = direction

    return output_direction

print(next_direction("Orange", "Red", "Orange"))