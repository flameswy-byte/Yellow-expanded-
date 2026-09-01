Route142_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

Route142_EventScript_RouteSignPetalburgCity::
	msgbox Route142_Text_RouteSignPetalburgCity, MSGBOX_SIGN
	end

Route142_Text_RouteSignPetalburgCity:
	.string "ROUTE 142\n"
	.string "{LEFT_ARROW} PETALBURG CITY$"

// Open Hoenn - tools/trainers.py

Route142_EventScript_Griffin::
	trainerbattle_single TRAINER_GRIFFIN, Route142_Text_GriffinIntro, Route142_Text_GriffinDefeat
	msgbox Route142_Text_GriffinPostBattle, MSGBOX_AUTOCLOSE
	end

Route142_Text_GriffinIntro:
	.string "I've been waiting for someone like\nyou.$"

Route142_Text_GriffinDefeat:
	.string "Beaten.$"

Route142_Text_GriffinPostBattle:
	.string "Rest before the next stretch.$"

Route142_EventScript_Gustav::
	trainerbattle_single TRAINER_GUSTAV, Route142_Text_GustavIntro, Route142_Text_GustavDefeat
	msgbox Route142_Text_GustavPostBattle, MSGBOX_AUTOCLOSE
	end

Route142_Text_GustavIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route142_Text_GustavDefeat:
	.string "Well fought.$"

Route142_Text_GustavPostBattle:
	.string "Good luck out there.$"

Route142_EventScript_Hadley::
	trainerbattle_single TRAINER_HADLEY, Route142_Text_HadleyIntro, Route142_Text_HadleyDefeat
	msgbox Route142_Text_HadleyPostBattle, MSGBOX_AUTOCLOSE
	end

Route142_Text_HadleyIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route142_Text_HadleyDefeat:
	.string "I underestimated you.$"

Route142_Text_HadleyPostBattle:
	.string "I'll be training when you come\nback.$"

