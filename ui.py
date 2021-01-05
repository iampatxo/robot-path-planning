import streamlit as st
import cv2
import numpy as np
import path_planning
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


def draw_path(img, pathway, thickness=2):
    # For-Loop with path, start with the first point, and join sequential points with line function
    start_x, start_y = pathway[0]
    for next_path in pathway[1:]:
        end_x, end_y = next_path
        cv2.line(img, (start_x, start_y), (end_x, end_y), (255, 0, 0), thickness)
        start_x, start_y = end_x, end_y


def solve_and_draw(name, algorithm, maze_image, start_x, start_y, finish_x, finish_y, scaled=False):
    # Set the grid with only 1D instead of RGB, if white space(or very clear) the way is clear, if not then obstacle
    grid = np.transpose(cv2.bitwise_not(cv2.inRange(maze_image, np.array([0, 0, 0]), np.array([245, 245, 245]))))
    # Solve maze
    with st.spinner(f"Solving your maze {name} way..."):
        pathway = algorithm(grid, (start_x, start_y), (finish_x, finish_y), scaled)
    # Draw solved maze
    maze_draw = maze_image.copy()
    thickness = max((maze_draw.shape[0] + maze_draw.shape[0]) // 300, 1)
    draw_path(maze_draw, pathway, thickness)
    st.image(maze_draw, channels="RGB", width=768)


def visualize_buttons(maze_image, start_x, start_y, finish_x, finish_y):
    # Choose a button, then apply the algorithm and draw
    if st.button('Solve Maze Dijstrka'):
        solve_and_draw('Dijstrka', path_planning.findDijkstra, maze_image, start_x, start_y, finish_x, finish_y)

    if st.button('Solve Maze A*'):
        solve_and_draw('A*', path_planning.findA, maze_image, start_x, start_y, finish_x, finish_y)


def visualize_maze(maze_image):
    # Set max values depending on image shape
    max_value_x = maze_image.shape[1]
    max_value_y = maze_image.shape[0]

    # Show the sliders in the middle
    st.subheader('Use the sliders to move the points! :)')
    start_x = st.sidebar.slider("Start(Green) X", value=max_value_x//2 - 5, min_value=0, max_value=max_value_x)
    start_y = st.sidebar.slider("Start(Green) Y", value=max_value_y//2 - 5, min_value=0, max_value=max_value_y)
    finish_x = st.sidebar.slider("Finish(Red) X", value=max_value_x//2 + 5, min_value=0, max_value=max_value_x)
    finish_y = st.sidebar.slider("Finish(Red) Y", value=max_value_y//2 + 5, min_value=0, max_value=max_value_y)

    # Draw circle thickness depending on image size
    circle_thickness = max((maze_image.shape[0] + maze_image.shape[0]) // 300, 1)
    cv2.circle(maze_image, (start_x, start_y), circle_thickness, (0, 255,), -1)
    cv2.circle(maze_image, (finish_x, finish_y), circle_thickness, (255, 0, 0), -1)
    st.image(maze_image, channels="RGB", width=768)

    visualize_buttons(maze_image, start_x, start_y, finish_x, finish_y)


def main():
    # Use Streamlit to create an UI
    st.title('Solve your maze!')
    upload = st.file_uploader("Upload an image (jpg/jpeg/png/svg)", ["jpg", "jpeg", "png", "svg"])
    checkbox = st.checkbox('Use default')

    # Check box and upload
    if checkbox:
        opencv_image = cv2.imread('default_maze.png')
        visualize_maze(opencv_image)
    elif upload is not None:
        # If the format is svg(a vector) we need to create a png and use it as the original image
        if '.svg' in upload.name:
            drawing = svg2rlg(upload.name)
            renderPM.drawToFile(drawing, "temporal_maze.png", fmt="PNG")
            opencv_image = cv2.imread("temporal_maze.png")
        else:
            opencv_image = cv2.imread(upload.name)
        visualize_maze(opencv_image)


if __name__ == "__main__":
    main()
