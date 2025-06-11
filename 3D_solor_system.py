# Import necessary libraries
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
import time
from datetime import datetime

# Initialize pygame and set up display
pygame.init()  # Initialize all pygame modules
width, height = 1200, 800  # Window dimensions
# Create OpenGL display window with double buffering
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
# Set window title
pygame.display.set_caption("3D Solar System Simulation - Modern Edition")

# Modern color palette using RGBA values (Red, Green, Blue, Alpha)
COLORS = {
    'background': (0.02, 0.03, 0.07, 1.0),  # Dark space background
    'sun': (0.98, 0.85, 0.37, 1.0),         # Yellowish sun
    'mercury': (0.75, 0.75, 0.75, 1.0),     # Gray Mercury
    'venus': (0.90, 0.70, 0.50, 1.0),       # Pale orange Venus
    'earth': (0.30, 0.50, 0.90, 1.0),       # Blue Earth
    'mars': (0.90, 0.30, 0.20, 1.0),        # Red Mars
    'jupiter': (0.80, 0.60, 0.40, 1.0),     # Brownish Jupiter
    'saturn': (0.90, 0.85, 0.60, 1.0),      # Pale yellow Saturn
    'uranus': (0.50, 0.85, 0.90, 1.0),      # Cyan Uranus
    'neptune': (0.20, 0.30, 0.90, 1.0),     # Deep blue Neptune
    'orbit': (0.40, 0.40, 0.50, 0.3),       # Semi-transparent orbit paths
    'ring': (0.85, 0.75, 0.60, 0.7),        # Saturn's rings color
    'moon': (0.80, 0.80, 0.85, 1.0),        # Grayish moon color
    'star': (1.0, 1.0, 1.0, 1.0),           # White stars
    'text': (1.0, 1.0, 1.0, 1.0),           # White text
    'highlight': (1.0, 0.0, 0.0, 1.0)       # Red selection highlight
}

# Set up 3D perspective projection
gluPerspective(45, (width / height), 0.1, 500.0)  # 45° FOV, aspect ratio, near/far planes
glTranslatef(0.0, 0.0, -50)  # Move camera back to see the scene

# Enable depth testing for proper 3D rendering
glEnable(GL_DEPTH_TEST)

# Set up lighting for 3D effect
glEnable(GL_LIGHTING)          # Enable lighting calculations
glEnable(GL_LIGHT0)            # Enable light source 0
# Position the light at the origin (sun position)
glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 0, 1])
# Set ambient (background) light level
glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1])
# Set diffuse (direct) light level
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])
# Set specular (highlight) light level
glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1])

# Enable color material properties
glEnable(GL_COLOR_MATERIAL)
# Define how colors interact with lighting
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

def create_starfield(num_stars=1000):
    """Create random star positions in 3D space"""
    stars = []
    for _ in range(num_stars):
        # Random positions in a 200 unit cube centered at origin
        x = (random.random() - 0.5) * 200
        y = (random.random() - 0.5) * 200
        z = (random.random() - 0.5) * 200
        # Random size between 0.1 and 0.3
        size = random.random() * 0.2 + 0.1
        stars.append((x, y, z, size))
    return stars

# Generate starfield background
stars = create_starfield()

# Planet data structure: 
# (name, radius, distance from sun, orbit speed, rotation speed, color, has rings, has moons)
planets = [
    ("Sun", 5.0, 0, 0, 0.02, COLORS['sun'], False, False),
    ("Mercury", 0.4, 7, 0.04, 0.004, COLORS['mercury'], False, False),
    ("Venus", 0.6, 9, 0.015, 0.002, COLORS['venus'], False, False),
    ("Earth", 0.7, 12, 0.01, 0.02, COLORS['earth'], False, True),
    ("Mars", 0.5, 15, 0.008, 0.018, COLORS['mars'], False, True),
    ("Jupiter", 1.5, 20, 0.002, 0.04, COLORS['jupiter'], False, True),
    ("Saturn", 1.2, 25, 0.0009, 0.038, COLORS['saturn'], True, True),
    ("Uranus", 0.9, 30, 0.0004, 0.03, COLORS['uranus'], False, True),
    ("Neptune", 0.9, 35, 0.0001, 0.032, COLORS['neptune'], False, True)
]

# Moons data structure:
# (name, parent planet index, radius, distance from planet, orbit speed, color)
moons = [
    ("Moon", 3, 0.2, 1.5, 0.05, COLORS['moon']),
    ("Phobos", 4, 0.1, 1.0, 0.08, (0.7, 0.7, 0.7, 1.0)),
    ("Deimos", 4, 0.08, 1.3, 0.04, (0.6, 0.6, 0.6, 1.0)),
    ("Io", 5, 0.15, 2.0, 0.1, (0.9, 0.8, 0.5, 1.0)),
    ("Europa", 5, 0.13, 2.5, 0.08, (0.8, 0.8, 0.9, 1.0)),
    ("Ganymede", 5, 0.18, 3.0, 0.06, (0.7, 0.7, 0.8, 1.0)),
    ("Callisto", 5, 0.16, 3.5, 0.04, (0.6, 0.6, 0.7, 1.0)),
    ("Titan", 6, 0.15, 2.5, 0.03, (0.9, 0.8, 0.7, 1.0)),
    ("Rhea", 6, 0.1, 3.0, 0.02, (0.8, 0.8, 0.8, 1.0)),
    ("Titania", 7, 0.12, 2.0, 0.025, (0.7, 0.8, 0.9, 1.0)),
    ("Oberon", 7, 0.11, 2.3, 0.02, (0.6, 0.7, 0.8, 1.0)),
    ("Triton", 8, 0.14, 2.0, 0.015, (0.8, 0.9, 0.9, 1.0))
]

def create_sphere(radius, slices=30, stacks=30):
    """Create a 3D sphere using GLU quadric"""
    quad = gluNewQuadric()              # Create new quadric object
    gluQuadricNormals(quad, GLU_SMOOTH) # Generate smooth normals
    gluQuadricTexture(quad, GL_TRUE)    # Enable texture coordinates
    gluSphere(quad, radius, slices, stacks)  # Draw sphere

def create_ring(inner_radius, outer_radius, slices=30):
    """Create a flat ring (for Saturn)"""
    quad = gluNewQuadric()              # Create new quadric object
    gluQuadricNormals(quad, GLU_SMOOTH) # Generate smooth normals
    gluDisk(quad, inner_radius, outer_radius, slices, 1)  # Draw disk with hole

def draw_orbit(radius):
    """Draw a circular orbit path"""
    glBegin(GL_LINE_LOOP)  # Start drawing connected line segments
    for i in range(100):   # 100 segments for smooth circle
        angle = 2 * math.pi * i / 100  # Current angle
        x = math.cos(angle) * radius   # X coordinate
        y = math.sin(angle) * radius   # Y coordinate
        glVertex3f(x, 0, y)           # Add vertex to line loop
    glEnd()

def draw_stars():
    """Draw the starfield background"""
    glDisable(GL_LIGHTING)  # Stars don't need lighting
    glPointSize(2.0)        # Set star size
    glBegin(GL_POINTS)      # Start drawing points
    for star in stars:
        glColor4fv(COLORS['star'])  # Set star color
        glVertex3f(star[0], star[1], star[2])  # Draw star at position
    glEnd()
    glEnable(GL_LIGHTING)   # Re-enable lighting

def draw_moon(name, radius, distance, orbit_speed, color, current_time):
    """Draw a moon orbiting its planet"""
    glPushMatrix()  # Save current transformation matrix
    
    # Calculate moon position in orbit
    moon_orbit = (current_time * orbit_speed) % (2 * math.pi)
    glRotatef(moon_orbit * 180 / math.pi, 0, 1, 0)  # Rotate to orbit position
    glTranslatef(distance, 0, 0)  # Move to orbit distance
    glColor4fv(color)             # Set moon color
    create_sphere(radius)         # Draw moon sphere
    
    # Draw moon's orbit path
    glDisable(GL_LIGHTING)
    glColor4f(*COLORS['orbit'])
    draw_orbit(distance)
    glEnable(GL_LIGHTING)
    
    glPopMatrix()  # Restore transformation matrix

def draw_planet_info(name, distance):
    """Display planet name and distance information"""
    glDisable(GL_LIGHTING)  # Text doesn't need lighting
    glColor4fv(COLORS['text'])  # Set text color
    
    # Create font and render text
    font = pygame.font.SysFont('Arial', 16)
    text = font.render(f"{name} - {distance:.1f} AU", True, (255, 255, 255))
    text_data = pygame.image.tostring(text, "RGBA", True)
    
    # Position text slightly above the planet
    glRasterPos3f(0, radius * 1.5, 0)
    # Draw the text pixels
    glDrawPixels(text.get_width(), text.get_height(), 
                GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glEnable(GL_LIGHTING)  # Re-enable lighting

def render():
    """Main rendering function that draws the entire scene"""
    global rotation_x, rotation_y, zoom_level, selected_planet
    
    # Clear buffers and set background color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*COLORS['background'])
    
    glPushMatrix()  # Save current transformation matrix
    
    # Apply camera transformations
    glRotatef(rotation_x, 1, 0, 0)  # X-axis rotation (up/down)
    glRotatef(rotation_y, 0, 1, 0)  # Y-axis rotation (left/right)
    glTranslatef(0, 0, zoom_level)  # Zoom in/out
    
    draw_stars()  # Draw starfield background
    
    current_time = time.time()  # Get current time for animations
    
    # Draw all planets
    for i, planet in enumerate(planets):
        name, radius, distance, orbit_speed, rotation_speed, color, has_rings, has_moons = planet
        
        glPushMatrix()  # Save transformation matrix for planet
        
        if name != "Sun":
            # Calculate planet position in orbit
            orbit_pos = (current_time * orbit_speed) % (2 * math.pi)
            # Rotate to orbit position
            glRotatef(orbit_pos * 180 / math.pi, 0, 1, 0)
            # Move to orbit distance from sun
            glTranslatef(distance, 0, 0)
            
            # Draw orbit path
            glDisable(GL_LIGHTING)
            glColor4fv(COLORS['orbit'])
            draw_orbit(distance)
            glEnable(GL_LIGHTING)
        
        # Highlight selected planet with red outline
        if selected_planet == i:
            glDisable(GL_LIGHTING)
            glColor4fv(COLORS['highlight'])
            create_sphere(radius * 1.1)  # Slightly larger sphere
            glEnable(GL_LIGHTING)
        
        # Planet rotation around its axis
        glRotatef((current_time * rotation_speed * 360) % 360, 0, 1, 0)
        glColor4fv(color)  # Set planet color
        create_sphere(radius)  # Draw planet
        
        # Draw rings for Saturn
        if has_rings:
            glColor4fv(COLORS['ring'])
            glRotatef(30, 1, 0, 0)  # Tilt rings
            create_ring(radius * 1.5, radius * 2.2)  # Inner and outer radius
        
        # Display planet info if selected
        if selected_planet == i:
            draw_planet_info(name, distance)
        
        # Draw moons for this planet
        if has_moons:
            # Find all moons belonging to this planet
            for moon in [m for m in moons if m[1] == i]:
                draw_moon(*moon[1:], current_time)  # Unpack moon parameters
        
        glPopMatrix()  # Restore planet transformation matrix
    
    glPopMatrix()  # Restore camera transformation matrix
    
    # Draw UI overlay
    draw_ui()

def draw_ui():
    """Draw user interface elements in 2D overlay"""
    glDisable(GL_LIGHTING)  # UI doesn't need lighting
    
    # Switch to orthographic projection for 2D rendering
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)  # 2D coordinate system
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Get current date/time
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Draw main title
    font = pygame.font.SysFont('Arial', 24, bold=True)
    title = font.render("Solar System Simulation", True, (255, 255, 255))
    text_data = pygame.image.tostring(title, "RGBA", True)
    glRasterPos2d(20, height - 40)  # Position at top-left
    glDrawPixels(title.get_width(), title.get_height(), 
                GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    # Draw date/time
    font = pygame.font.SysFont('Arial', 18)
    time_text = font.render(date_str, True, (200, 200, 200))
    text_data = pygame.image.tostring(time_text, "RGBA", True)
    glRasterPos2d(20, height - 70)
    glDrawPixels(time_text.get_width(), time_text.get_height(), 
                GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    # Draw controls information
    controls = [
        "Controls:",
        "- Left click + drag: Rotate view",
        "- Mouse wheel: Zoom in/out",
        "- Number keys 1-9: Select planet",
        "- R: Reset view"
    ]
    
    # Draw each control line
    for i, line in enumerate(controls):
        text = font.render(line, True, (200, 200, 200))
        text_data = pygame.image.tostring(text, "RGBA", True)
        glRasterPos2d(width - 250, height - 40 - i * 25)  # Right-aligned
        glDrawPixels(text.get_width(), text.get_height(), 
                    GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    # Restore 3D projection
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glEnable(GL_LIGHTING)  # Re-enable lighting

def reset_view():
    """Reset camera to default position"""
    global rotation_x, rotation_y, zoom_level, selected_planet
    rotation_x = 20  # Tilted down slightly
    rotation_y = 0    # No rotation
    zoom_level = -50  # Default zoom distance
    selected_planet = -1  # No planet selected

# Initialize camera controls
rotation_x = 20      # Initial X rotation (tilt)
rotation_y = 0       # Initial Y rotation
zoom_level = -50     # Initial zoom distance
mouse_dragging = False  # Track mouse drag state
last_mouse_pos = (0, 0)  # Store last mouse position
selected_planet = -1     # No planet selected initially

# Main game loop
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_dragging = True
                last_mouse_pos = event.pos
            elif event.button == 4:  # Mouse wheel up
                zoom_level += 1
            elif event.button == 5:  # Mouse wheel down
                zoom_level -= 1
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if mouse_dragging:
                x, y = event.pos
                dx = x - last_mouse_pos[0]  # X movement
                dy = y - last_mouse_pos[1]  # Y movement
                rotation_y += dx * 0.5      # Rotate around Y axis
                rotation_x += dy * 0.5      # Rotate around X axis
                # Clamp X rotation to avoid flipping
                rotation_x = max(-90, min(90, rotation_x))
                last_mouse_pos = (x, y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Reset view
                reset_view()
            elif pygame.K_1 <= event.key <= pygame.K_9:
                planet_index = event.key - pygame.K_1  # Convert key to index
                if planet_index < len(planets):
                    selected_planet = planet_index
    
    render()  # Draw the scene
    pygame.display.flip()  # Swap buffers
    pygame.time.wait(10)   # Small delay to control frame rate

pygame.quit()  # Clean up pygame
