Route140_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route140_EventScript_Garland::
	trainerbattle_single TRAINER_GARLAND, Route140_Text_GarlandIntro, Route140_Text_GarlandDefeat
	msgbox Route140_Text_GarlandPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_GarlandIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route140_Text_GarlandDefeat:
	.string "Well fought.$"

Route140_Text_GarlandPostBattle:
	.string "Good luck out there.$"

Route140_EventScript_Gavin::
	trainerbattle_single TRAINER_GAVIN, Route140_Text_GavinIntro, Route140_Text_GavinDefeat
	msgbox Route140_Text_GavinPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_GavinIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route140_Text_GavinDefeat:
	.string "I underestimated you.$"

Route140_Text_GavinPostBattle:
	.string "I'll be training when you come\nback.$"

Route140_EventScript_Gwendolen::
	trainerbattle_single TRAINER_GWENDOLEN, Route140_Text_GwendolenIntro, Route140_Text_GwendolenDefeat
	msgbox Route140_Text_GwendolenPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_GwendolenIntro:
	.string "u$"

Route140_Text_GwendolenDefeat:
	.string "e$"

Route140_Text_GwendolenPostBattle:
	.string "T$"

Route140_EventScript_Gilda::
	trainerbattle_single TRAINER_GILDA, Route140_Text_GildaIntro, Route140_Text_GildaDefeat
	msgbox Route140_Text_GildaPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_GildaIntro:
	.string "The water's fine! Come in and\nbattle.$"

Route140_Text_GildaDefeat:
	.string "Out of my depth.$"

Route140_Text_GildaPostBattle:
	.string "Careful past the point. It's\ndeeper.$"

Route140_EventScript_Glenn::
	trainerbattle_single TRAINER_GLENN, Route140_Text_GlennIntro, Route140_Text_GlennDefeat
	msgbox Route140_Text_GlennPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_GlennIntro:
	.string "A challenger! At last.$"

Route140_Text_GlennDefeat:
	.string "The ROUTE is yours.$"

Route140_Text_GlennPostBattle:
	.string "There's more of us further along.$"

Route140_EventScript_Griselda::
	trainerbattle_single TRAINER_GRISELDA, Route140_Text_GriseldaIntro, Route140_Text_GriseldaDefeat
	msgbox Route140_Text_GriseldaPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_GriseldaIntro:
	.string "I've been waiting for someone like\nyou.$"

Route140_Text_GriseldaDefeat:
	.string "Beaten.$"

Route140_Text_GriseldaPostBattle:
	.string "Rest before the next stretch.$"

Route140_EventScript_Griffin::
	trainerbattle_single TRAINER_GRIFFIN, Route140_Text_GriffinIntro, Route140_Text_GriffinDefeat
	msgbox Route140_Text_GriffinPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_GriffinIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route140_Text_GriffinDefeat:
	.string "Well fought.$"

Route140_Text_GriffinPostBattle:
	.string "Good luck out there.$"

