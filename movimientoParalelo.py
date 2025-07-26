from multiprocessing import Process, Queue
import cv2
import numpy as np
import matplotlib.pyplot as plt



def GenerarFrame(queue, total_frames, index_map, paleta, SpriteLista, config):
    h, w = config["h"], config["w"]
    sy = config["sy"]
    velocidad = config["velocidad"]
    direccion = 1
    sx = 0
    pal = paleta.copy()

    for frame in range(total_frames):

        if frame % config["paletaTiempo"] == 0:
            pal = pal[1:] + [pal[0]]

        Nimagen = np.array([pal[i] for i in index_map.flatten()]).reshape((h, w, 3)).astype(np.uint8)
        if config["scroll_activado"]:
            OffsetX, OffsetY = ObtenerOffsets(frame, config["opcion"], w, h)
            Nimagen = Scroll(Nimagen, OffsetX, OffsetY)
        if config["modo_oscilacion"] in ("horizontal", "vertical", "ambas"):
            Nimagen = Oscilacion(Nimagen, frame, modo=config["modo_oscilacion"])

        sprite_rgb, sprite_mascara = SpriteLista[(frame // 10) % len(SpriteLista)]
        Nsize = (int(sprite_rgb.shape[1] * 2), int(sprite_rgb.shape[0] * 2))
        sprite_rgb_r = cv2.resize(sprite_rgb, Nsize, interpolation=cv2.INTER_NEAREST)
        sprite_mascara_r = cv2.resize(sprite_mascara.astype(np.uint8)*255, Nsize, interpolation=cv2.INTER_NEAREST)
        sprite_mascara_r = sprite_mascara_r.astype(bool)

        sh, sw = sprite_rgb_r.shape[:2]
        sx += velocidad * direccion
        if sx <= 0 or sx + sw >= w:
            direccion *= -1

        if sy + sh <= h and 0 <= sx <= w - sw:
            region = Nimagen[sy:sy+sh, sx:sx+sw]
            region[sprite_mascara_r] = sprite_rgb_r[sprite_mascara_r]
            Nimagen[sy:sy+sh, sx:sx+sw] = region

        queue.put((Nimagen, pal)) 
def SeleccionarFondo(i):
    if i < 0 or i >= TFondos:
        raise ValueError("Índice fuera de rango")
    row = i // NFilas
    col = i % NFilas
    y1 = row * AltoTile
    y2 = y1 + AltoTile
    x1 = col * AnchoTile
    x2 = x1 + AnchoTile
    return SpriteFondoRGB[y1:y2, x1:x2]
def Scroll(img, offsetX, offsetY):
    scrolly = np.vstack([img[offsetY:], img[:offsetY]])
    scrollxy = np.hstack([scrolly[:, offsetX:], scrolly[:, :offsetX]])
    return scrollxy
def ObtenerOffsets(frame, opcion, w, h):
    dx = frame % w
    dy = frame % h
    if opcion == 1:
        return dx, dy
    elif opcion == 2:
        return w - dx, dy
    elif opcion == 3:
        return w - dx, h - dy
    elif opcion == 4:
        return dx, h - dy
    else:
        raise ValueError("Opción debe ser 1, 2, 3 o 4")
def Oscilacion(img, frame, modo="horizontal", amplitud=20, frecuencia=0.015):
    h, w, _ = img.shape
    salida = np.copy(img)

    if modo == "horizontal" or modo == "ambas":
        for y in range(h):
            shift = int(amplitud * np.sin(2 * np.pi * frecuencia * y + frame * 0.15))
            salida[y] = np.roll(salida[y], shift, axis=0)

    if modo == "vertical" or modo == "ambas":
        temp = np.copy(salida)
        for x in range(w):
            shift = int(amplitud * np.sin(2 * np.pi * frecuencia * x + frame * 0.15))
            salida[:, x] = np.roll(temp[:, x], shift, axis=0)

    return salida
def CargarSprites(sheetRGB, ancho):
    sprites = []
    cols = sheetRGB.shape[1] // ancho
    for i in range(cols):
        sub = sheetRGB[:, i*ancho:(i+1)*ancho]
        rgb = sub[..., :3]
        mask = np.any(rgb != [255, 255, 255], axis=-1)
        sprites.append((rgb, mask))
    return sprites

# ---------- PUNTO DE ENTRADA ----------
if __name__ == "__main__":
    
    SpriteFondo = cv2.imread("fondosheet.png")
    SpriteFondoRGB = cv2.cvtColor(SpriteFondo, cv2.COLOR_BGR2RGB)
    NFilas = SpriteFondo.shape[1] // 256
    NColum = SpriteFondo.shape[0] // 224
    TFondos = NFilas * NColum

    AnchoTile = 256
    AltoTile = 224
    i = 89
    tile = SeleccionarFondo(i)
    h, w, _ = tile.shape
    pixels = tile.reshape(-1, 3)
    colors, inverso = np.unique(pixels, axis=0, return_inverse=True)
    paleta = colors.tolist()
    index_map = inverso.reshape(h, w)

    sprite_sheet = cv2.imread("sprite.png", cv2.IMREAD_UNCHANGED)  
    sprite_rgba = cv2.cvtColor(sprite_sheet, cv2.COLOR_BGR2RGB)   
    SpriteLista = CargarSprites(sprite_rgba, 13)

    config = {
        "h": h,
        "w": w,
        "sy": 128,
        "velocidad": 1,
        "opcion": 4,
        "modo_oscilacion": "horizontal",
        "scroll_activado": True,
        "paletaTiempo": 8,
    }

    # --- PROCESO PRODUCTOR ---
    queue = Queue(maxsize=5)
    total_frames = 230

    proceso = Process(target=GenerarFrame, args=(queue, total_frames, index_map, paleta, SpriteLista, config))
    proceso.start()

    # --- RENDER PRINCIPAL ---
    plt.ion()
    fig, ax = plt.subplots()
    img = ax.imshow(np.zeros((h, w, 3), dtype=np.uint8))
    plt.axis("off")

    for _ in range(total_frames):
        Nimagen, paleta = queue.get()
        img.set_data(Nimagen)
        plt.draw()
        plt.pause(0.015)
        
    proceso.join()
    plt.ioff()
    plt.show()