Route141_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

Route141_EventScript_RouteSignRustboroCity::
	msgbox Route141_Text_RouteSignRustboroCity, MSGBOX_SIGN
	end

Route141_Text_RouteSignRustboroCity:
	.string "ROUTE 141\n"
	.string "{LEFT_ARROW} RUSTBORO CITY$"

Route141_EventScript_RouteSignVerdanturfTown::
	msgbox Route141_Text_RouteSignVerdanturfTown, MSGBOX_SIGN
	end

Route141_Text_RouteSignVerdanturfTown:
	.string "ROUTE 141\n"
	.string "{RIGHT_ARROW} VERDANTURF TOWN$"

// Open Hoenn - tools/trainers.py

Route141_EventScript_Gabe::
	trainerbattle_single TRAINER_GABE, Route141_Text_GabeIntro, Route141_Text_GabeDefeat
	msgbox Route141_Text_GabePostBattle, MSGBOX_AUTOCLOSE
	end

Route141_Text_GabeIntro:
	.string "Show me the team that got you this\nfar.$"

Route141_Text_GabeDefeat:
	.string "Good. Very good.$"

Route141_Text_GabePostBattle:
	.string "I'll be training when you come\nback.$"

Route141_EventScript_Garland::
	trainerbattle_single TRAINER_GARLAND, Route141_Text_GarlandIntro, Route141_Text_GarlandDefeat
	msgbox Route141_Text_GarlandPostBattle, MSGBOX_AUTOCLOSE
	end

Route141_Text_GarlandIntro:
	.string "Battle me and I'll let you pass.$"

Route141_Text_GarlandDefeat:
	.string "That settles it.$"

Route141_Text_GarlandPostBattle:
	.string "Safe travels.$"

Route141_EventScript_Gavin::
	trainerbattle_single TRAINER_GAVIN, Route141_Text_GavinIntro, Route141_Text_GavinDefeat
	msgbox Route141_Text_GavinPostBattle, MSGBOX_AUTOCLOSE
	end

Route141_Text_GavinIntro:
	.string "Not many come this far. Battle me.$"

Route141_Text_GavinDefeat:
	.string "You've come a long way indeed.$"

Route141_Text_GavinPostBattle:
	.string "Keep heading on. It opens out.$"

Route141_EventScript_Glenn::
	trainerbattle_single TRAINER_GLENN, Route141_Text_GlennIntro, Route141_Text_GlennDefeat
	msgbox Route141_Text_GlennPostBattle, MSGBOX_AUTOCLOSE
	end

Route141_Text_GlennIntro:
	.string "I've walked every rise in HOENN.\pLet's see what you've walked.$"

Route141_Text_GlennDefeat:
	.string "You've got the legs for it.$"

Route141_Text_GlennPostBattle:
	.string "Take the high path. It's kinder\nthan it looks.$"

