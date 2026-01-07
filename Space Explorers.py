import pygame
import random
import math

pygame.init()

dis = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Space Explorers') 
pygame.display.set_icon(pygame.transform.scale(pygame.image.load("EARTH.png"), (50, 50)))

clr = 0, 0, 0
gmode = 0
SC = 100, 100, 100
playr_clr = 0, 150, 0
CAPSULEc = [15, 20]
Tc = [15, 180]
ENGINEc = [15, 260]
BEc = [15, 340]
NCc = [28, 110]
SKY_c = [0, -9500]
maxskyc = [0, -9500]
groundc = [0, 460]
fh = 200
th = 200
g = 9.8
MCoords = [390, 299]
VCoords = [300, 257.5]
MryCoords = [240, 125]
JCoords = [400, 355]
launchinitialize = 0
planet = "EARTH"
LA = 0

CAPSULEclicked = False
Tclicked = False
ENGINEclicked = False
BEclicked = False
NCclicked = False
MarsLanding = False
MercuryLanding = False
VenusLanding = False
JupiterLanding = False
lift = True
Fire = False

placed_objects = {"CAPSULE": [], "T": [], "ENGINE": [], "BE": [], "NC": []}
specs = {"Fuel" : 1, "Weight" : 1}

CAPSULE = pygame.transform.scale(pygame.image.load("CAPSULE.png"), (80, 80))
T = pygame.transform.scale(pygame.image.load("T.png"), (80, 80))
ENGINE = pygame.transform.scale(pygame.image.load("ENGINE.png"), (80, 80))
BE = pygame.transform.scale(pygame.image.load("BOOSTER ENGINE.png"), (80, 80))
NC = pygame.transform.scale(pygame.image.load("NC.png"), (55, 55))
sky = pygame.transform.scale(pygame.image.load("SkyBox.jpg"), (500, 10000))
ground = pygame.transform.scale(pygame.image.load("G.jpg"), (500, 500))
Sun = pygame.transform.scale(pygame.image.load("SUN.png"), (250, 250))
Mercury = pygame.transform.scale(pygame.image.load("MERCURY.png"), (25, 25))
Venus = pygame.transform.scale(pygame.image.load("VENUS.png"), (50, 50))
Earth = pygame.transform.scale(pygame.image.load("EARTH.png"), (50, 50))
Mars = pygame.transform.scale(pygame.image.load("MARS.png"), (30, 30))
Jupiter = pygame.transform.scale(pygame.image.load("JUPITER.png"), (100, 100))

class Star:
    def __init__(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(-50, 600)
        self.speed = random.randint(5, 20)
        self.size = random.randint(1, 3)

    def move(self):
        self.y += self.speed
        if self.y > 600:
            self.y = random.randint(-50, 0)
            self.x = random.randint(0, 800)
            self.speed = random.randint(5, 20)

    def draw(self):
        pygame.draw.circle(dis, (255, 255, 255), (self.x, self.y), self.size)

stars = [Star() for _ in range(50)]

Start = pygame.Rect(100, 150, 300, 100)
playr = pygame.Rect(414, 15, 76, 20)
fuel = pygame.Rect(25, 240, 25, fh)
fuelr = pygame.Rect(25, 240, 25, 200)
thrust = pygame.Rect(450, 240, 25, th)
thrustr = pygame.Rect(450, 240, 25, 200)
Mrect = pygame.Rect(464, 5, 33, 15)

fps = 60
clock = pygame.time.Clock()

assembled_angle = 0
assembly_active = False
assembled_surface = None

surfaces = {
    "CAPSULE": CAPSULE,
    "T": T,
    "ENGINE": ENGINE,
    "BE": BE,
    "NC": NC
}

def combine_parts(placed_objects):
    min_x, min_y, max_x, max_y = float("inf"), float("inf"), float("-inf"), float("-inf")

    for part, positions in placed_objects.items():
        for pos in positions:
            part_surface = surfaces[part]
            width, height = part_surface.get_size()
            x, y = pos

            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x + width)
            max_y = max(max_y, y + height)

    combined_width = max_x - min_x
    combined_height = max_y - min_y

    combined_surface = pygame.Surface((combined_width, combined_height), pygame.SRCALPHA)

    for part, positions in placed_objects.items():
        for pos in positions:
            part_surface = surfaces[part]
            x, y = pos
            combined_surface.blit(part_surface, (x - min_x, y - min_y))

    return combined_surface

r = True
while r:
    dis.fill((clr))

    if gmode == 0:
        for star in stars:
            star.move()
            star.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            r = False
        
    crsr = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        if Start.collidepoint(crsr) and gmode == 0:
            gmode = 1
        if playr.collidepoint(crsr) and gmode == 1:
            gmode = 2
            MAX_FUEL = specs["Fuel"]  
            MIN_FUEL = 0
            MIN_WEIGHT = -specs["Weight"]
            MAX_WEIGHT = 0
        if playr.collidepoint(crsr) and gmode ==  3:
            gmode = 2
        if Mrect.collidepoint(crsr) and gmode == 2  and int(Latitude) > 12000:
            gmode = 3
        if gmode == 3:
            if (MCoords[0] <= crsr[0] <= MCoords[0] + 30 and MCoords[1] <= crsr[1] <= MCoords[1] + 30):
                MarsLanding = True 
                MercuryLanding = VenusLanding = JupiterLandingLanding = False
                planet = "MARS"
                LA = 45
            elif (MryCoords[0] <= crsr[0] <= MryCoords[0] + 25 and MryCoords[1] <= crsr[1] <= MryCoords[1] + 25):
                MercuryLanding = True 
                MarsLanding = VenusLanding = JupiterLanding = False
                planet = "MERCURY"
                LA = 280
            elif (VCoords[0] <= crsr[0] <= VCoords[0] + 50 and VCoords[1] <= crsr[1] <= VCoords[1] + 50):
                VenusLanding = True 
                MercuryLanding = MarsLanding = JupiterLanding = False
                planet = "VENUS"
                LA = 270
            elif (JCoords[0] <= crsr[0] <= JCoords[0] + 100 and JCoords[1] <= crsr[1] <= JCoords[1] + 100):
                JupiterLanding = True 
                MercuryLanding = VenusLanding = MarsLanding = False
                planet = "JUPITER"
                LA = 35
        if gmode == 1:
            if not allclicked and (CAPSULEc[0] <= crsr[0] <= CAPSULEc[0] + 80 and CAPSULEc[1] <= crsr[1] <= CAPSULEc[1] + 80):
                CAPSULEclicked = True
                Tclicked = ENGINEclicked = BEclicked = NCclicked = False
            elif not allclicked and (Tc[0] <= crsr[0] <= Tc[0] + 80 and Tc[1] <= crsr[1] <= Tc[1] + 80):
                Tclicked = True
                CAPSULEclicked = ENGINEclicked = BEclicked = NCclicked = False
            elif not allclicked and (ENGINEc[0] <= crsr[0] <= ENGINEc[0] + 80 and ENGINEc[1] <= crsr[1] <= ENGINEc[1] + 80):
                ENGINEclicked = True
                CAPSULEclicked = Tclicked = BEclicked = NCclicked = False
            elif not allclicked and (BEc[0] <= crsr[0] <= BEc[0] + 80 and BEc[1] <= crsr[1] <= BEc[1] + 80):
                BEclicked = True
                CAPSULEclicked = Tclicked = ENGINEclicked = NCclicked = False
            elif not allclicked and (NCc[0] <= crsr[0] <= NCc[0] + 80 and NCc[1] <= crsr[1] <= NCc[1] + 80):
                NCclicked = True
                CAPSULEclicked = Tclicked = ENGINEclicked = BEclicked = False
            
    if CAPSULEclicked or NCclicked or Tclicked or BEclicked or ENGINEclicked:
        allclicked = True
    else:
        allclicked = False


    if event.type == pygame.MOUSEBUTTONUP and gmode == 1:
        if CAPSULEclicked:
            placed_objects["CAPSULE"].append(CAPSULEc[:])
            specs["Weight"] -= 2
            CAPSULEc = [15, 20]
            CAPSULEclicked = False

        if Tclicked:
            placed_objects["T"].append(Tc[:])
            specs["Weight"] -= 2
            specs["Fuel"] += 20
            Tc = [15, 180]
            Tclicked = False

        if ENGINEclicked:
            placed_objects["ENGINE"].append(ENGINEc[:])
            specs["Weight"] += 15
            ENGINEc = [15, 260]
            ENGINEclicked = False

        if BEclicked:
            placed_objects["BE"].append(BEc[:])
            specs["Weight"] += 20
            BEc = [15, 340]
            BEclicked = False
        
        if NCclicked:
            placed_objects["NC"].append(NCc[:])
            specs["Weight"] -= 1
            NCc = [28, 110]
            NCclicked = False

    if gmode == 1:
        clr = 0, 0, 0
        if CAPSULEclicked:
            CAPSULEc[0] = crsr[0] - 40
            CAPSULEc[1] = crsr[1] - 40
        if NCclicked:
            NCc[0] = crsr[0] - 27.5
            NCc[1] = crsr[1] - 27.5
        if Tclicked:
            if "NC" in placed_objects and placed_objects["NC"]:
                Tc[0] = placed_objects["NC"][-1][0] -12.5
                Tc[1] = crsr[1] - 40
            elif "CAPSULE" in placed_objects and placed_objects["CAPSULE"]:
                Tc[0] = placed_objects["CAPSULE"][-1][0] + 1
                Tc[1] = crsr[1] - 40
            else:
                Tc[0] = crsr[0] - 40
                Tc[1] = crsr[1] - 40
            
        if ENGINEclicked:
            if "NC" in placed_objects and placed_objects["NC"]:
                ENGINEc[0] = placed_objects["NC"][-1][0] -12.5
                ENGINEc[1] = crsr[1] - 40
            elif "CAPSULE" in placed_objects and placed_objects["CAPSULE"]:
                ENGINEc[0] = placed_objects["CAPSULE"][-1][0]
                ENGINEc[1] = crsr[1] - 40
            else:
                ENGINEc[0] = crsr[0] - 40
                ENGINEc[1] = crsr[1] - 40
        if BEclicked:
            if "NC" in placed_objects and placed_objects["NC"]:
                BEc[0] = placed_objects["NC"][-1][0] -13
                BEc[1] = crsr[1] - 40
            elif "CAPSULE" in placed_objects and placed_objects["CAPSULE"]:
                BEc[0] = placed_objects["CAPSULE"][-1][0]
                BEc[1] = crsr[1] - 40
            else:
                BEc[0] = crsr[0] - 40
                BEc[1] = crsr[1] - 40

        for pos in placed_objects["CAPSULE"]:
            dis.blit(CAPSULE, pos)
        for pos in placed_objects["T"]:
            dis.blit(T, pos)
        for pos in placed_objects["ENGINE"]:
            dis.blit(ENGINE, pos)
        for pos in placed_objects["BE"]:
            dis.blit(BE, pos)
        for pos in placed_objects["NC"]:
            dis.blit(NC, pos)
        
        pygame.draw.rect(dis, (0, 155, 155), pygame.Rect(0, 0, 100, 500))
        pygame.draw.rect(dis, (playr_clr), playr)
        dis.blit(CAPSULE, CAPSULEc)
        dis.blit(T, Tc)
        dis.blit(ENGINE, ENGINEc)
        dis.blit(BE, BEc)
        dis.blit(NC, NCc) 
        dis.blit(pygame.transform.scale(pygame.image.load('play.png'), (20, 20)), (470, 15))
        dis.blit((pygame.font.Font(None, 20).render("LAUNCH", True, (0, 0, 0))), (414, 19))

    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE] and gmode == 1:
        gmode = 0
        clr = 0, 0, 0
        placed_objects["CAPSULE"] = []
        placed_objects["BE"] = []
        placed_objects["ENGINE"] = []
        placed_objects["NC"] = []
        placed_objects["T"] = []

    if gmode == 0:
        pygame.draw.rect(dis, (SC), Start, 5)
        start = pygame.font.Font(None, 100).render("START", True, (255, 255, 255))
        credit = pygame.font.Font(None, 20).render("By: Zeus Sharma.", True, (0, 155, 155))
        dis.blit(credit, (160, 260))
        dis.blit(start, (140, 170))
    
    if gmode == 2:
        dis.blit(sky, (SKY_c))
        dis.blit(ground, (groundc))
        if key[pygame.K_a] and not RocketRect.colliderect(Grect):
            assembled_angle += 5
            if assembled_angle >= 360:
                assembled_angle = 0
        elif key[pygame.K_d] and not RocketRect.colliderect(Grect):
            assembled_angle -= 5
            if assembled_angle <= 0:
                assembled_angle += 360 

        if assembled_angle >= 360:
            assembled_angle = 0

        def update_sky_position(angle):
            if 90 < angle < 270:
                f = 500
            else:
                f = -500
            return f
        
        f = update_sky_position(assembled_angle)
        
        if key[pygame.K_s]:
            if specs["Fuel"] > MIN_FUEL:
                specs["Weight"] = min(specs["Weight"] + 0.5, MAX_WEIGHT + 0.1)
            else:
                specs["Weight"] = MIN_WEIGHT      
        elif key[pygame.K_w]:
            specs["Weight"] = max(specs["Weight"] - 0.5, MIN_WEIGHT + 0.1)

        if specs["Weight"] > MIN_WEIGHT and specs["Fuel"] > MIN_FUEL and lift:
            fuel_depletion_rate = (specs["Weight"] / MIN_WEIGHT) * 0.05
            specs["Fuel"] -= fuel_depletion_rate
            SKY_c[1] -= fuel_depletion_rate * f
            groundc[1] -= fuel_depletion_rate * f
        else:
            specs["Fuel"] = max(specs["Fuel"], MIN_FUEL)
            fuel_depletion_rate = (specs["Weight"] / MIN_WEIGHT) * 0.05
            lift = False

        specs["Fuel"] = max(MIN_FUEL, specs["Fuel"])
        specs["Weight"] = max(MIN_WEIGHT, min(specs["Weight"], MAX_WEIGHT))
    
        fh = (specs["Fuel"] / MAX_FUEL) * 200
        th = (specs["Weight"] / MIN_WEIGHT) * 200

        fuel = pygame.Rect(25 , 440 - fh, 25, fh)
        thrust = pygame.Rect(450 , 440 - th , 25, th)
        dis.blit(pygame.font.Font(None, 20).render("FUEL", True, (255, 255, 255)), (20, 455))
        dis.blit(pygame.font.Font(None, 20).render("THRUST", True, (255, 255, 255)), (430, 455))
        Latitude = str(int((356 - groundc[1])*-1))
        v = int(fuel_depletion_rate * f * -100)
        vs = str('VELOCITY = ' + str(v) + " mtrs Up")
        AS = str(360 - assembled_angle)
        ASS = str('ANGLE = ' + AS + '°')
        LatitudeS = str("ALTITUDE : " + Latitude )
        dis.blit(pygame.font.Font(None, 20).render(ASS, True, (255, 255, 255)), (5, 35))
        dis.blit(pygame.font.Font(None, 20).render(LatitudeS, True, (255, 255, 255)), (375, 25))
        if lift:
            dis.blit(pygame.font.Font(None, 20).render(vs, True, (255, 255, 255)), (5, 15))
        if int(Latitude) > 12000:
            Mrect = pygame.Rect(464, 5, 33, 15)
            if Mrect.collidepoint(crsr) == False:
                pygame.draw.rect(dis, (200, 200, 200), Mrect)
            dis.blit(pygame.font.Font(None, 20).render("MAP", True, (255, 255, 255)), (466, 5))
        
        if (MarsLanding or VenusLanding or MercuryLanding or JupiterLanding) and launchinitialize < 1:
            launchinitializeS = str("Required Distance to be covered: " + str(int((1 - launchinitialize) * -1000)))
            AngleS = str("Required Angle: " + str(LA))
            dis.blit(pygame.font.Font(None, 20).render(launchinitializeS, True, (255, 255, 255)), (5, 55))
            dis.blit(pygame.font.Font(None, 20).render(AngleS, True, (255, 255, 255)), (5, 65))

        if (360 - assembled_angle) == LA and th > 150 and MarsLanding and lift:
            launchinitialize = launchinitialize + v/abs(v) * 0.0007
        
        if (360 - assembled_angle) == LA and th > 160 and VenusLanding and lift:
            launchinitialize = launchinitialize + v/abs(v) * 0.00009
        
        if (360 - assembled_angle) == LA and th > 195 and MercuryLanding and lift:
            launchinitialize = launchinitialize + v/abs(v) * 0.0006
        
        if (360 - assembled_angle) == LA and th > 195 and JupiterLanding and lift:
            launchinitialize = launchinitialize + v/abs(v) * 0.0003
                
        if launchinitialize > 1:
            if MarsLanding:
                g = 3.87
                sky = pygame.transform.scale(pygame.image.load("MarsAtmos.jpg"), (500, 10000))
                ground = pygame.transform.scale(pygame.image.load("MarsG.jpg"), (500, 500))
            elif VenusLanding:
                g = 8.87
                sky = pygame.transform.scale(pygame.image.load("VenusAtmos.jpg"), (500, 10000))
                ground = pygame.transform.scale(pygame.image.load("VenusG.jpg"), (500, 500))
            elif MercuryLanding:
                g = 3.7
                sky = pygame.transform.scale(pygame.image.load("SkyBox.jpg"), (0.1, 0.1))
                ground = pygame.transform.scale(pygame.image.load("MercuryG.jpg"), (500, 500))
            elif JupiterLanding:
                g = 24.7
                sky = pygame.transform.scale(pygame.image.load("JupiterAtmos.jpg"), (500, 10000))
                ground = pygame.transform.scale(pygame.image.load("VenusG.jpg"), (500, 500))

        assembled_surface = combine_parts(placed_objects)
    
        if assembled_surface:
            rotated_surface = pygame.transform.rotate(assembled_surface, assembled_angle)
            rect = rotated_surface.get_rect(center=(250, 250))
            dis.blit(rotated_surface, rect.topleft)
        RocketRect = assembled_surface.get_rect(center=(250, 250))
        Grect = ground.get_rect(topleft = (groundc))
        if not RocketRect.colliderect(Grect) and SKY_c[1] != 0:
            SKY_c[1] -= g 
            groundc[1] -= g

        if abs(int(v)) > 0 and lift:
            BE = pygame.transform.scale(pygame.image.load("BOOSTERENGINEwithfire.png"), (90, 160))
        elif abs(int(v)) <= 0 or lift == False:
            BE = pygame.transform.scale(pygame.image.load("BOOSTER ENGINE.png"), (80, 80))

        surfaces = {
        "CAPSULE": CAPSULE,
        "T": T,
        "ENGINE": ENGINE,
        "BE": BE,
        "NC": NC
        }

        pygame.draw.rect(dis, (255, 255, 255), fuel)
        pygame.draw.rect(dis, (255, 255, 255), fuelr, 5)
        pygame.draw.rect(dis, (255, 255, 255), thrust)
        pygame.draw.rect(dis, (255, 255, 255), thrustr, 5)
    
    if gmode == 3:
        EC = [300 + Earth.get_width() / 2 , 257.5 + Earth.get_height() / 2]
        MC = [240 + Mercury.get_width() / 2 , 125 + Mercury.get_height() / 2]
        VC = [270 + Mercury.get_width() / 2 , 50 + Mercury.get_height() / 2]
        MrC = [390 + Mars.get_width() / 2 , 299 + Mars.get_height() / 2]
        JC = [400 + Jupiter.get_width() / 2 , 355 + Jupiter.get_height() / 2]
        Eradius = math.sqrt((EC[0] - 125)**2 + (EC[1] - 250)**2)
        Mradius = math.sqrt((MC[0] - 125)**2 + (MC[1] - 250)**2)
        Vradius = math.sqrt((VC[0] - 125)**2 + (VC[1] - 250)**2)
        Mrradius = math.sqrt((MrC[0] - 125)**2 + (MrC[1] - 250)**2)
        Jradius = math.sqrt((JC[0] - 125)**2 + (JC[1] - 250)**2)
        pygame.draw.circle(dis, (255, 255, 255), (125, 250), Mradius, 2)
        pygame.draw.circle(dis, (255, 255, 255), (125, 250), Vradius, 2)
        pygame.draw.circle(dis, (255, 255, 255), (125, 250), Eradius, 2)
        pygame.draw.circle(dis, (255, 255, 255), (125, 250), Mrradius, 2)
        pygame.draw.circle(dis, (255, 255, 255), (125, 250), Jradius, 2)
        dis.blit(Sun, (0, 125))
        dis.blit(Mercury, (MryCoords))
        dis.blit(Venus, (VCoords))
        dis.blit(Earth, (270, 50))
        dis.blit(Mars, (MCoords))
        dis.blit(Jupiter, (JCoords))

        dis.blit(pygame.transform.scale(pygame.image.load('play.png'), (20, 20)), (470, 15))
        dis.blit(pygame.font.Font(None, 20).render("BACK", True, (255, 255, 255)), (414, 19))
        dis.blit(pygame.font.Font(None, 20).render(str("Planet = " + planet) , True, (0, 255, 0)), (10, 19))
    
    if Start.collidepoint(crsr):
        SC = 0,0,0
    else:
        SC = 155, 155, 155
    
    if playr.collidepoint(crsr):
        playr_clr = 255, 255, 255
    else:
        playr_clr = 0, 150, 0

    clock.tick(fps)
    pygame.display.flip()

pygame.quit()