Route147_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route147_EventScript_Olive::
	trainerbattle_single TRAINER_OLIVE, Route147_Text_OliveIntro, Route147_Text_OliveDefeat
	msgbox Route147_Text_OlivePostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_OliveIntro:
	.string "Battle me and I'll let you pass.$"

Route147_Text_OliveDefeat:
	.string "That settles it.$"

Route147_Text_OlivePostBattle:
	.string "Safe travels.$"

Route147_EventScript_Orson::
	trainerbattle_single TRAINER_ORSON, Route147_Text_OrsonIntro, Route147_Text_OrsonDefeat
	msgbox Route147_Text_OrsonPostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_OrsonIntro:
	.string "The water's fine! Come in and\nbattle.$"

Route147_Text_OrsonDefeat:
	.string "Out of my depth.$"

Route147_Text_OrsonPostBattle:
	.string "Careful past the point. It's\ndeeper.$"

Route147_EventScript_Oscar::
	trainerbattle_single TRAINER_OSCAR, Route147_Text_OscarIntro, Route147_Text_OscarDefeat
	msgbox Route147_Text_OscarPostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_OscarIntro:
	.string "A challenger! At last.$"

Route147_Text_OscarDefeat:
	.string "The ROUTE is yours.$"

Route147_Text_OscarPostBattle:
	.string "There's more of us further along.$"

Route147_EventScript_Otto::
	trainerbattle_single TRAINER_OTTO, Route147_Text_OttoIntro, Route147_Text_OttoDefeat
	msgbox Route147_Text_OttoPostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_OttoIntro:
	.string "I've been waiting for someone like\nyou.$"

Route147_Text_OttoDefeat:
	.string "Beaten.$"

Route147_Text_OttoPostBattle:
	.string "Rest before the next stretch.$"

Route147_EventScript_Paige::
	trainerbattle_single TRAINER_PAIGE, Route147_Text_PaigeIntro, Route147_Text_PaigeDefeat
	msgbox Route147_Text_PaigePostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_PaigeIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route147_Text_PaigeDefeat:
	.string "Well fought.$"

Route147_Text_PaigePostBattle:
	.string "Good luck out there.$"

Route147_EventScript_Percy::
	trainerbattle_single TRAINER_PERCY, Route147_Text_PercyIntro, Route147_Text_PercyDefeat
	msgbox Route147_Text_PercyPostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_PercyIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route147_Text_PercyDefeat:
	.string "I underestimated you.$"

Route147_Text_PercyPostBattle:
	.string "I'll be training when you come\nback.$"

Route147_EventScript_Petronella::
	trainerbattle_single TRAINER_PETRONELLA, Route147_Text_PetronellaIntro, Route147_Text_PetronellaDefeat
	msgbox Route147_Text_PetronellaPostBattle, MSGBOX_AUTOCLOSE
	end

Route147_Text_PetronellaIntro:
	.string "Battle me and I'll let you pass.$"

Route147_Text_PetronellaDefeat:
	.string "That settles it.$"

Route147_Text_PetronellaPostBattle:
	.string "Safe travels.$"

