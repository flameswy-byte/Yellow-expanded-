Route147_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route147_EventScript_Paige::
	trainerbattle_single TRAINER_PAIGE, Route147_Text_PaigeIntro, Route147_Text_PaigeDefeat
	msgbox Route147_Text_PaigePostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_PaigeIntro:
	.string "Sandwich? No? Battle, then.$"

Route147_Text_PaigeDefeat:
	.string "I'll pack up, then.$"

Route147_Text_PaigePostBattle:
	.string "Safe travels.$"

Route147_EventScript_Oakley::
	trainerbattle_single TRAINER_OAKLEY, Route147_Text_OakleyIntro, Route147_Text_OakleyDefeat
	msgbox Route147_Text_OakleyPostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_OakleyIntro:
	.string "The water's fine! Come in and\nbattle.$"

Route147_Text_OakleyDefeat:
	.string "Out of my depth.$"

Route147_Text_OakleyPostBattle:
	.string "Careful past the point. It's\ndeeper.$"

Route147_EventScript_Orson::
	trainerbattle_single TRAINER_ORSON, Route147_Text_OrsonIntro, Route147_Text_OrsonDefeat
	msgbox Route147_Text_OrsonPostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_OrsonIntro:
	.string "My POKéMON is stronger than\nyesterday!$"

Route147_Text_OrsonDefeat:
	.string "Yesterday me would have lost worse.$"

Route147_Text_OrsonPostBattle:
	.string "There's tall grass back that way.\nGood grass.$"

Route147_EventScript_Oscar::
	trainerbattle_single TRAINER_OSCAR, Route147_Text_OscarIntro, Route147_Text_OscarDefeat
	msgbox Route147_Text_OscarPostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_OscarIntro:
	.string "Hey! Nobody comes down here!\pBattle me!$"

Route147_Text_OscarDefeat:
	.string "Aww.$"

Route147_Text_OscarPostBattle:
	.string "When I'm big I'll have six POKéMON.$"

Route147_EventScript_Petronella::
	trainerbattle_single TRAINER_PETRONELLA, Route147_Text_PetronellaIntro, Route147_Text_PetronellaDefeat
	msgbox Route147_Text_PetronellaPostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_PetronellaIntro:
	.string "Let's not waste each other's time.$"

Route147_Text_PetronellaDefeat:
	.string "I'll take that loss.$"

Route147_Text_PetronellaPostBattle:
	.string "Good luck out there.$"

Route147_EventScript_Piper::
	trainerbattle_single TRAINER_PIPER, Route147_Text_PiperIntro, Route147_Text_PiperDefeat
	msgbox Route147_Text_PiperPostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_PiperIntro:
	.string "Show me the team that got you this\nfar.$"

Route147_Text_PiperDefeat:
	.string "Good. Very good.$"

Route147_Text_PiperPostBattle:
	.string "I'll be training when you come\nback.$"

Route147_EventScript_Ramona::
	trainerbattle_single TRAINER_RAMONA, Route147_Text_RamonaIntro, Route147_Text_RamonaDefeat
	msgbox Route147_Text_RamonaPostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_RamonaIntro:
	.string "Ready when you are.$"

Route147_Text_RamonaDefeat:
	.string "You've earned the ROUTE.$"

Route147_Text_RamonaPostBattle:
	.string "Safe travels.$"

