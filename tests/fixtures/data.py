from sacaar_battles.app import Character, Race
import datetime

asgard = Race(name='asgardian')
human = Race(name='human')
mutant = Race(name='mutant')

frigga = Character(name='frigga', victory=3, defeat=6, race=asgard)
volstagg = Character(name='volstagg', victory=4, defeat=3, race=asgard)
bl_widow = Character(name='black widow', victory=6, defeat=3, race=human)
iron_man = Character(name='iron man', victory=7, defeat=3, race=human)
cyclops = Character(name='cyclops', victory=4, defeat=6, race=mutant)
wolverine = Character(name='wolverine', victory=8, defeat=6, race=mutant)
green_goblin = Character(name='green goblin', victory=5, defeat=7, race=mutant, death_date=datetime.datetime.utcnow())
sabretooth = Character(name='sabretooth', victory=7, defeat=4, race=mutant, death_date=datetime.datetime.utcnow())

heroes = [frigga, volstagg, bl_widow, iron_man, cyclops, wolverine, green_goblin, sabretooth]
