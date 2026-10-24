# -*- coding: utf-8 -*-
"""
Find Differences asset generator (pure Python, no dependencies).

  fdcore.py           rasterizer, lighting shaders, Unity meta/asset writers, previews
  levels_classic.py   Level01-03 (flat cartoon)
  levels_fairy.py     Level04-05 (fairy-tale fantasy, lit / volumetric look)
  paper.py            paper-craft helpers (cut-out pieces, white borders, layered shadows, grain)
  levels_paper.py     Level06-07 (paper-craft / paper-cut diorama, side view)
  levels_topdown.py   Level08-09 (paper-craft, top-down view)
  levels_views.py     Level10-11 (paper-craft, side cross-section / 45-degree isometric view)
  weather.py          paper weather effects (rain, snow, fog, lightning, heat haze ...) for WeatherCycle
  stylekit.py         shared helpers for the themed packs (sun/moon, neon, cel shading, figures ...)
  levels_classic2.py  Level63-65 perspective paper 2.5D (persp + paper25) (amusement park / harbour market / winter village)
  levels_horror.py    Level66-68 psychological horror interiors (persp.Cam + paper25)
  levels_europe.py    Level69-73 Europe 15th-19th c. (Florence / Venice / Holland / Versailles / London), paper side views
  levels_heian.py     Level74-76 Heian Japan (shinden garden / Aoi festival / moonlit boating), paper side views
  levels_heian2.py    Level77-78 Heian Japan part 2 (Phoenix Hall / snowy morning)
  levels_sengoku.py   Level79-83 Sengoku Japan (castle town / battle / tea house / Nanban ship / castle at night)
  levels_meiji.py     Level84-88 Meiji Japan (Ginza / Shinbashi station / Rokumeikan / Yokohama / Tomioka silk mill)
  levels_edo.py       Level89-93 Edo Japan (Nihonbashi / great wave / kabuki / Ryogoku fireworks / Tokaido)
  levels_sanguo.py    Level94-98 Three Kingdoms (peach garden / Red Cliffs / empty city / thatched cottage / straw boats)
  levels_tangsong.py  Level99-103 Tang / Song China (Chang'an market / Qingming river / spring outing / West Lake / lantern festival)
  levels_andersen.py  Level104-108 Andersen fairy tales
  levels_xiyou.py     Level109-113 Journey to the West
  levels_akiba.py     Level114-118 Akihabara (electric town / maid cafe / figure shop / arcade / pedestrian street)
  levels_misc.py      Level119-122 street-fighting stages (original fighters) / Age of Discovery
  levels_oblique.py   Level123 paper campsite in 45-degree overhead view with cast shadows (oblique.py)
  levels_gothic.py    Level124-128 gothic: vampire castle / werewolf night / the count's hall / castle courtyard / midnight graveyard
  levels_portrait.py  Level129 portrait gallery (old-master style portraits, a painter at his easel)
  levels_modern.py    Level130-135 modern life (football match / concert / expo hall / gas station / shopping mall / future city)
  levels_daily.py     Level500-509 everyday town (zoo / airport / supermarket / schoolyard / fire station / bakery / lakeside park / ski resort / lighthouse / library)
  levels_festival.py  Level145-154 festivals (Spring Festival dinner / dragon boats / Mid-Autumn / Halloween / Christmas Eve / Christmas market / birthday / egg hunt / New Year countdown / carnival)
  levels_retro.py     Level155-159 80s/90s video-game nostalgia (bedroom / rental shop / pixel platformer / pixel space shooter / arcade hall)
  levels_sports2.py   Level215-224 sports part 2 (volleyball / table tennis / boxing / ice hockey / road cycling / golf / gymnastics / show jumping / archery / beach volleyball)
  levels_gamecontent6.py Level225-234 inside video games part 6 (falling blocks / brick breaker / brawler / snake / whack-a-mole / star map / digging sandbox / magic school / pirate map / dinosaur park)
  levels_mix1.py      Level235-244 mixed themes 1 (coral reef / rainforest / ancient Egypt / Arctic / orchard / night market / space station / candy kingdom / dinosaurs / balloon festival)
  levels_mix2.py      Level245-254 mixed themes 2 (savanna / construction site / train platform / container port / glasshouse / insect garden / toy room / circus / pirate deck / desert bazaar)
  levels_mix3.py      Level255-264 mixed themes 3 (Greek temple / jungle ruins / vineyard / dairy farm / fishing village / ice-cream parlour / flower shop / observatory / music classroom / snowy cabin)
  levels_mix4.py      Level265-274 mixed themes 4 (bamboo pandas / aquarium / natural history museum / art studio / sushi bar / pet shop / barber shop / cafe / laundromat / clock shop)
  levels_mix5.py      Level275-284 mixed themes 5 (tulip windmills / alpine pasture / rice terraces / red canyon / maple valley / firefly night / mangrove / lavender fields / treehouse village / fjord)
  levels_mix6.py      Level285-294 mixed themes 6 (post office / vet clinic / skate park / water park / drive-in cinema / bowling alley / gym / flea market / rooftop garden / subway car)
  levels_mix7.py      Level295-304 mixed themes 7 (apiary / tea plantation / castle kitchen / submarine / ice fishing / mushroom village / moon base / robot factory / sandcastle beach / island resort)
  levels_mix8.py      Level305-314 mixed themes 8 (kite festival / canal town / wheat harvest / cherry-blossom river / snow festival / pumpkin farm / wetland / fish market / watermill / mountain railway)
  levels_mix9.py      Level315-324 mixed themes 9 (toy shop / antique shop / doughnut shop / pizzeria / tailor / pottery studio / carpentry / sweet shop / hat shop / tea house)
  levels_mix10.py     Level325-334 mixed themes 10 (undersea palace / rainbow valley / snowman village / penguin colony / pirate cove / alien garden / chocolate factory / weather station / rowing regatta / Roman forum)
  levels_mix11.py     Level335-344 mixed themes 11 (Viking village / yurt grassland / whitewashed cliff village / hot-spring lagoon / aviary / morning market / pit stop / horse stable / bamboo rafting / aurora town)
  levels_homes.py     Level136-144 home interiors (modern apartment / old American apartment / European manor: three rooms each)
  levels_daily3.py    Level520-529 everyday town 3: shops and services (car wash / optician / bookshop / stationery / music shop / bike repair / photo studio / breakfast shop / hot pot / shoe shop)
  levels_daily4.py    Level530-539 everyday town 4: city outdoors (bus terminal / fountain square / window cleaners / interchange / parking garage / ferry / arcade street / community garden / street performers / snowy bus stop)
  levels_daily5.py    Level540-549 everyday town 5: nature trips (waterfall / sea lions / deer glade / snow foxes / snow monkeys / lotus pond / sunflowers / cactus desert / turtle beach / autumn trail)
  levels_daily2.py    Level510-519 everyday town 2 (aquarium / circus / flower shop / construction site / train platform / dinosaur museum / rainy cafe / pumpkin farm / ice rink / pet shop)
  levels_medieval.py  Level19-21 medieval (castle / market / tavern)
  levels_cyber.py     Level22-24 cyberpunk (rain street / rooftop / crossroads)
  levels_anime.py     Level25-27 anime cel style (sakura slope / shrine festival / summer sky)
  orbit3d.py          tiny 3D paper-diorama renderer + builder for camera-orbit levels
  kit.py              prop library + post filters (oil painting, pencil sketch, tilt-shift) for the theme levels
  themes1..5.py       Level29-59 one level per theme (steampunk ... miniature world)
  levels_vehicle.py   Level60-62 looking out of a vehicle window (train / taxi / airliner), parallax scenery
  levels_orbit.py     Level28 paper village on a turntable, camera orbits 3 views (120° apart, 6 s each)
  levels_weather.py   Level16-18 (weather cycles: farm storm / mountain snow & fog / beach heat & rain)
  levels_more.py      Level12-15 (paper-craft: doll's-house cut-away / worm's-eye / through a window / isometric)

Usage:
  python generate_assets.py                      all levels + UI sprites
  python generate_assets.py Level04 Level05      only those levels
  options:
    --preview[=DIR]   static preview (t = 0, differences circled)   default DIR: Tools~/Previews
    --anim[=DIR]      animated APNG preview (both pictures, 4 s)    default DIR: Tools~/Previews
"""
import os
import sys

import fdcore
import levels_classic
import levels_fairy
import levels_paper
import levels_topdown
import levels_views
import levels_more
import levels_weather
import levels_medieval
import levels_cyber
import levels_anime
import levels_orbit
import themes1
import themes2
import themes3
import themes4
import themes5
import levels_vehicle
import levels_classic2
import levels_horror
import levels_europe
import levels_heian
import levels_heian2
import levels_sengoku
import levels_meiji
import levels_edo
import levels_sanguo
import levels_tangsong
import levels_andersen
import levels_xiyou
import levels_akiba
import levels_misc
import levels_oblique
import levels_gothic
import levels_portrait
import levels_modern
import levels_daily
import levels_homes
import levels_festival
import levels_retro
import levels_sports
import levels_gamecontent
import levels_gamecontent2
import levels_gamecontent3
import levels_gamecontent4
import levels_gamecontent5
import levels_dragon
import levels_sports2
import levels_gamecontent6
import levels_mix1
import levels_mix2
import levels_mix3
import levels_mix4
import levels_mix5
import levels_mix6
import levels_mix7
import levels_mix8
import levels_mix9
import levels_mix10
import levels_mix11
import levels_daily2
import levels_daily3
import levels_daily4
import levels_daily5

ALL_LEVELS = (levels_classic.LEVELS + levels_fairy.LEVELS + levels_paper.LEVELS + levels_topdown.LEVELS
              + levels_views.LEVELS + levels_more.LEVELS + levels_weather.LEVELS
              + levels_medieval.LEVELS + levels_cyber.LEVELS + levels_anime.LEVELS + levels_orbit.LEVELS
              + themes1.LEVELS + themes2.LEVELS + themes3.LEVELS + themes4.LEVELS + themes5.LEVELS
              + levels_vehicle.LEVELS + levels_classic2.LEVELS
              + levels_horror.LEVELS + levels_europe.LEVELS + levels_heian.LEVELS
              + levels_heian2.LEVELS + levels_sengoku.LEVELS + levels_meiji.LEVELS
              + levels_edo.LEVELS + levels_sanguo.LEVELS + levels_tangsong.LEVELS
              + levels_andersen.LEVELS + levels_xiyou.LEVELS + levels_akiba.LEVELS
              + levels_misc.LEVELS + levels_oblique.LEVELS + levels_gothic.LEVELS + levels_portrait.LEVELS
              + levels_modern.LEVELS + levels_homes.LEVELS + levels_festival.LEVELS + levels_retro.LEVELS + levels_daily.LEVELS
              + levels_sports.LEVELS + levels_gamecontent.LEVELS + levels_dragon.LEVELS
              + levels_gamecontent2.LEVELS + levels_gamecontent3.LEVELS
              + levels_gamecontent4.LEVELS + levels_gamecontent5.LEVELS
              + levels_sports2.LEVELS + levels_gamecontent6.LEVELS
              + levels_mix1.LEVELS + levels_mix2.LEVELS + levels_mix3.LEVELS
              + levels_mix4.LEVELS + levels_mix5.LEVELS + levels_mix6.LEVELS + levels_mix7.LEVELS
              + levels_mix8.LEVELS + levels_mix9.LEVELS + levels_mix10.LEVELS + levels_mix11.LEVELS + levels_daily2.LEVELS
              + levels_daily3.LEVELS + levels_daily4.LEVELS + levels_daily5.LEVELS)


def main():
    default_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Previews")
    preview_dir = anim_dir = None
    names = []
    for arg in sys.argv[1:]:
        if arg.startswith("--preview"):
            preview_dir = arg.partition("=")[2] or default_dir
        elif arg.startswith("--anim"):
            anim_dir = arg.partition("=")[2] or default_dir
        else:
            names.append(arg)

    os.makedirs(fdcore.ART_DIR, exist_ok=True)
    os.makedirs(fdcore.LEVEL_DIR, exist_ok=True)
    if not names:
        for name, (size, rows, border) in fdcore.gen_ui().items():
            fdcore.save_image(name + ".png", size, size, rows, alpha=True, max_size=256, border=border)

    for name, title, background, elements, diffs, time_limit, *opts in ALL_LEVELS:
        if names and name not in names:
            continue
        if opts and "custom" in opts[0]:          # e.g. camera-orbit levels have their own builder
            opts[0]["custom"](name, title, time_limit, preview_dir=preview_dir, anim_dir=anim_dir)
            continue
        fdcore.build_level(name, title, background, elements, diffs, time_limit,
                           preview_dir=preview_dir, anim_dir=anim_dir, **(opts[0] if opts else {}))


if __name__ == "__main__":
    main()
