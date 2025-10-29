import tkinter as tk
from PIL import Image, ImageTk
import random
import os

# --- CONFIGURACIÓN ---
SPRITE_FOLDER = "sprites/"
ANIMATION_DELAY_MS = 250   # Velocidad de la animación (tiempo entre frames)
# --- CONFIGURACIÓN DE MOVIMIENTO (DESACTIVADA) ---
MOVEMENT_DELAY_MS = 100    # Frecuencia de actualización de la posición
STEP_SIZE = 1              # Cantidad de píxeles que se mueve por paso
SPRITE_PREFIX = 'B_witch_charge' # <--- ¡Nuevo prefijo para tu animación!

class DesktopPet:
    def __init__(self, master):
        self.master = master
        
        # 1. Cargar la secuencia de sprites de 'carga'
        self.animation_sprites = self.load_sprites(SPRITE_PREFIX)
        if not self.animation_sprites:
            print(f"ERROR: No se encontraron sprites con el prefijo: {SPRITE_PREFIX}_xx.png en la carpeta 'sprites/'.")
            master.destroy()
            return
            
        self.current_frame = 0 # Índice del sprite actual
        
        # 2. Configuración de la Ventana
        # Hace la ventana sin bordes y transparente
        master.overrideredirect(True) 
        master.wm_attributes("-transparentcolor", "gray")
        master.attributes("-topmost", True)
        master.config(bg='gray') 
        
        # 3. Canvas y Posición Inicial
        self.photo = self.animation_sprites[0]
        window_width = self.photo.width()
        window_height = self.photo.height()
        
        self.canvas = tk.Canvas(master, width=window_width, height=window_height, 
                                bg='gray', highlightthickness=0)
        self.canvas.pack()
        self.image_item = self.canvas.create_image(0, 0, image=self.photo, anchor='nw')

        # Posicionamiento (Ej: Inferior derecha, Fijo)
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        initial_x = screen_width - window_width - 50 
        initial_y = screen_height - window_height - 50
        master.geometry(f'{window_width}x{window_height}+{initial_x}+{initial_y}')
        
        # 4. Variables y Bucle de Animación
        self.is_moving = False # Controla el movimiento automático
        self.animate() # ¡Inicia el bucle de animación!
        
        # 5. Funciones de Arrastre (Mantenemos la posibilidad de moverlo con el mouse)
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<ButtonRelease-1>", self.stop_move)
        self.canvas.bind("<B1-Motion>", self.do_move)
        self.offset_x = 0
        self.offset_y = 0
        
        # self.direction = random.choice([1, -1]) 
        # self.move_pet() # <--- LÍNEA DE MOVIMIENTO AUTOMÁTICO COMENTADA

    # --- FUNCIÓN DE UTILIDAD: Carga de Sprites ---
    def load_sprites(self, prefix):
        """Carga todos los archivos PNG que comienzan con un prefijo dado."""
        sprites = []
        # Lista los archivos, asegurando el orden correcto
        filenames = sorted([f for f in os.listdir(SPRITE_FOLDER) if f.startswith(prefix) and f.endswith('.png')])
        for filename in filenames:
            try:
                img = Image.open(SPRITE_FOLDER + filename)
                sprites.append(ImageTk.PhotoImage(img))
            except Exception as e:
                print(f"Error al cargar {filename}: {e}")
        return sprites

    # --- FUNCIÓN DE ANIMACIÓN (Bucle) ---
    def animate(self):
        """Cambia el sprite para crear el efecto de movimiento."""
        
        # Pasa al siguiente frame, ciclando si llega al final
        self.current_frame = (self.current_frame + 1) % len(self.animation_sprites)
        new_photo = self.animation_sprites[self.current_frame]

        # Si quieres que la animación se refleje al moverse (opcional, aunque ahora fijo)
        # if self.is_moving and self.direction == -1: 
        #     original_image = Image.open(SPRITE_FOLDER + f"{SPRITE_PREFIX}_{self.current_frame+1:02}.png")
        #     mirrored_image = original_image.transpose(Image.FLIP_LEFT_RIGHT)
        #     new_photo = ImageTk.PhotoImage(mirrored_image)
        
        # Actualiza la imagen en el Canvas
        self.canvas.itemconfig(self.image_item, image=new_photo)
        self.photo = new_photo 
            
        # Repite la animación después del tiempo de retardo
        self.master.after(ANIMATION_DELAY_MS, self.animate)

    # --- FUNCIÓN DE MOVIMIENTO (COMENTADA) ---
    # def move_pet(self):
    #     """Calcula el nuevo X y Y y mueve la ventana (actualmente desactivado)."""
    #     if self.is_moving:
    #         current_x = self.master.winfo_x()
    #         new_x = current_x + (self.direction * STEP_SIZE)
            
    #         screen_width = self.master.winfo_screenwidth()
    #         window_width = self.master.winfo_width()
            
    #         # Lógica de Rebote 
    #         if new_x < 0 or new_x > screen_width - window_width:
    #             self.direction *= -1 
    #             new_x = current_x 

    #         # Aplicar el movimiento
    #         self.master.geometry(f"+{new_x}+{self.master.winfo_y()}")

    #     # Repite el movimiento después del tiempo de retardo
    #     self.master.after(MOVEMENT_DELAY_MS, self.move_pet)

    # --- Funciones de Arrastre ---
    def start_move(self, event):
        # self.is_moving = False # Detiene el movimiento automático si estuviera activo
        self.offset_x = event.x
        self.offset_y = event.y

    def stop_move(self, event):
        # self.is_moving = True # Reanuda el movimiento automático si estuviera activo
        self.offset_x = 0
        self.offset_y = 0

    def do_move(self, event):
        x = self.master.winfo_x() + event.x - self.offset_x
        y = self.master.winfo_y() + event.y - self.offset_y
        self.master.geometry(f"+{x}+{y}")

# --- Ejecución del Programa ---
if __name__ == "__main__":
    root = tk.Tk()
    pet = DesktopPet(root)
    root.mainloop()