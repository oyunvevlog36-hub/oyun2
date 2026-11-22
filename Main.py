import tkinter as tk
import random

pencere = tk.Tk()
pencere.title("3D Savas")

tuval = tk.Canvas(pencere, bg="#1b2636", highlightthickness=0)
tuval.pack(fill="both", expand=True)

oyuncu_x = 0.0
nisan_y = 20.0
puan = 0
can = 100
mermi = 15
bolum = 1
bitti = False
yon = None
sayac = 0

dusmanlar = []
mermiler = []
d_mermiler = []

def ates():
    global mermi, bitti, puan, can, oyuncu_x, nisan_y, bolum
    if bitti:
        oyuncu_x = 0.0
        nisan_y = 20.0
        dusmanlar.clear()
        mermiler.clear()
        d_mermiler.clear()
        puan = 0
        can = 100
        mermi = 15
        bolum = 1
        bitti = False
        return
    if mermi > 0:
        mermi -= 1
        mermiler.append([oyuncu_x, nisan_y, 50.0])
    else:
        mermi = 15

def dokun(e):
    global yon
    w = tuval.winfo_width()
    h = tuval.winfo_height()
    if bitti:
        ates()
        return
    if e.y > int(h * 0.72):
        if e.x < int(w * 0.52):
            mx, my = int(w * 0.26), int(h * 0.85)
            dx, dy = e.x - mx, e.y - my
            if abs(dx) > abs(dy):
                yon = "SOL" if dx < 0 else "SAG"
            else:
                yon = "YUKARI" if dy < 0 else "ASAGI"
        else:
            ates()
    else:
        ates()

def birak(e):
    global yon
    yon = None

tuval.bind("<ButtonPress-1>", dokun)
tuval.bind("<ButtonRelease-1>", birak)

def dongu():
    global oyuncu_x, nisan_y, puan, can, mermi, bitti, sayac, bolum
    w = tuval.winfo_width()
    h = tuval.winfo_height()
    if w < 20 or h < 20:
        pencere.after(50, dongu)
        return

    ufuk = int(h * 0.42)
    tuval.delete("all")
    tuval.create_rectangle(0, 0, w, ufuk, fill="#385475", outline="")
    tuval.create_rectangle(0, ufuk, w, h, fill="#2c2921", outline="")

    if not bitti:
        if yon == "SOL":
            oyuncu_x = max(-200.0, oyuncu_x - 10.0)
        elif yon == "SAG":
            oyuncu_x = min(200.0, oyuncu_x + 10.0)
        elif yon == "YUKARI":
            nisan_y = max(-100.0, nisan_y - 6.0)
        elif yon == "ASAGI":
            nisan_y = min(55.0, nisan_y + 6.0)

        bolum = (puan // 150) + 1
        sayac += 1
        if sayac >= 55 and len(dusmanlar) < 3:
            sayac = 0
            r = random.randint(1, 100)
            if bolum == 1:
                tur = "asker" if r <= 75 else ("helikopter" if r <= 90 else "tank")
            elif bolum == 2:
                tur = "tank" if r <= 65 else ("helikopter" if r <= 85 else "asker")
            else:
                tur = "helikopter" if r <= 50 else ("tank" if r <= 80 else "asker")

            y_pos = -70.0 if tur == "helikopter" else 45.0
            hp = 3 if tur == "helikopter" else (4 if tur == "tank" else 2)
            dusmanlar.append([tur, random.uniform(-140, 140), y_pos, 900.0, hp, 60])

        for m in mermiler[:]:
            m[2] += 50.0
            if m[2] > 950:
                mermiler.remove(m)

        for d in dusmanlar[:]:
            if d[3] > 200:
                d[3] -= 4.0
            d[5] -= 1
            if d[5] <= 0:
                d[5] = 85
                d_mermiler.append([d[1], d[2], d[3] - 15])

            vurdu = False
            for m in mermiler[:]:
                if abs(m[0] - d[1]) < 48 and abs(m[1] - d[2]) < 38 and abs(m[2] - d[3]) < 58:
                    mermiler.remove(m)
                    vurdu = True
                    break
            if vurdu:
                d[4] -= 1
                if d[4] <= 0:
                    puan += 50 if d[0] != "asker" else 25
                    dusmanlar.remove(d)

        for dm in d_mermiler[:]:
            dm[2] -= 16.0
            if dm[2] <= 45:
                if abs(dm[0] - oyuncu_x) < 42:
                    can -= 15
                    if can <= 0:
                        bitti = True
                d_mermiler.remove(dm)

        for d in sorted(dusmanlar, key=lambda x: x[3], reverse=True):
            olcek = 400.0 / max(25.0, d[3])
            ex = int(w / 2 + (d[1] - oyuncu_x) * olcek)
            ey = int(ufuk + d[2] * olcek)
            if d[0] == "helikopter":
                hw, hh = max(34, int(130 * olcek)), max(14, int(44 * olcek))
                tuval.create_oval(ex - hw // 3, ey - hh // 3, ex + hw // 3, ey + hh // 3, fill="#2b382c", outline="#8f8")
                tuval.create_line(ex - hw // 2, ey - hh // 2, ex + hw // 2, ey - hh // 2, fill="#fff", width=2)
            elif d[0] == "tank":
                tw, th = max(32, int(115 * olcek)), max(18, int(55 * olcek))
                gy = int(ufuk + 95 * olcek)
                tuval.create_rectangle(ex - tw // 2, gy - th // 3, ex + tw // 2, gy, fill="#111", outline="#666")
                tuval.create_rectangle(ex - tw // 3, gy - th, ex + tw // 3, gy - th // 3, fill="#4d5943", outline="#9b9")
            else:
                boy, en = max(26, int(110 * olcek)), max(12, int(38 * olcek))
                gy = int(ufuk + 95 * olcek)
                tuval.create_rectangle(ex - en // 2, ey - boy // 3, ex + en // 2, gy, fill="#3c4a35", outline="#111")
                kr = max(5, int(13 * olcek))
                tuval.create_oval(ex - kr, ey - boy // 2 - kr, ex + kr, ey - boy // 2 + kr, fill="#d9a882")

        for m in mermiler:
            olcek = 400.0 / max(25.0, m[2])
            mx = int(w / 2 + (m[0] - oyuncu_x) * olcek)
            my = int(ufuk + m[1] * olcek)
            r = max(3, int(6 * olcek))
            tuval.create_oval(mx - r, my - r, mx + r, my + r, fill="#ffd746")

        for dm in d_mermiler:
            olcek = 400.0 / max(25.0, dm[2])
            mx = int(w / 2 + (dm[0] - oyuncu_x) * olcek)
            my = int(ufuk + dm[1] * olcek)
            r = max(3, int(7 * olcek))
            tuval.create_oval(mx - r, my - r, mx + r, my + r, fill="#ff3333")

        ox, oy = w // 2, int(ufuk + nisan_y * 0.9)
        renk = "#55ccff" if nisan_y < -15 else "#32ff82"
        tuval.create_oval(ox - 18, oy - 18, ox + 18, oy + 18, outline=renk, width=2)
        tuval.create_line(ox - 26, oy, ox + 26, oy, fill=renk, width=2)
        tuval.create_line(ox, oy - 26, ox, oy + 26, fill=renk, width=2)

        tuval.create_text(15, 22, anchor="w", text=f"BOLUM {bolum} | SKOR: {puan} | CAN: {max(0, can)}", fill="#32ff82", font=("Arial", 13, "bold"))
        tuval.create_text(w - 15, 22, anchor="e", text=f"MERMI: {mermi}/15", fill="#ffd746", font=("Arial", 13, "bold"))

        cx, cy = int(w * 0.26), int(h * 0.85)
        bw, bh = int(w * 0.13), int(h * 0.06)
        tuval.create_rectangle(cx - bw, cy - bh * 2, cx + bw, cy - int(bh * 0.6), fill="#2d3744", outline="#55ccff")
        tuval.create_text(cx, cy - int(bh * 1.3), text="HAVA", fill="#55ccff", font=("Arial", 11, "bold"))
        tuval.create_rectangle(cx - bw, cy + int(bh * 0.6), cx + bw, cy + bh * 2, fill="#2d3744", outline="#32ff82")
        tuval.create_text(cx, cy + int(bh * 1.3), text="YER", fill="#32ff82", font=("Arial", 11, "bold"))
        tuval.create_rectangle(cx - int(bw * 2.5), cy - int(bh * 0.7), cx - int(bw * 1.1), cy + int(bh * 0.7), fill="#2d3744", outline="#888")
        tuval.create_text(cx - int(bw * 1.8), cy, text="SOL", fill="white", font=("Arial", 11, "bold"))
        tuval.create_rectangle(cx + int(bw * 1.1), cy - int(bh * 0.7), cx + int(bw * 2.5), cy + int(bh * 0.7), fill="#2d3744", outline="#888")
        tuval.create_text(cx + int(bw * 1.8), cy, text="SAG", fill="white", font=("Arial", 11, "bold"))
        tuval.create_rectangle(int(w * 0.60), int(h * 0.76), int(w * 0.96), int(h * 0.95), fill="#b92b1e", outline="#fff", width=2)
        tuval.create_text(int(w * 0.78), int(h * 0.855), text="ATES ET", fill="white", font=("Arial", 17, "bold"))
    else:
        tuval.create_text(w // 2, int(h * 0.45), text=f"BITTI! SKOR: {puan}", fill="#ff4141", font=("Arial", 22, "bold"))
        tuval.create_text(w // 2, int(h * 0.55), text="Tekrar icin dokun", fill="white", font=("Arial", 15))

    pencere.after(30, dongu)

dongu()
pencere.mainloop()
