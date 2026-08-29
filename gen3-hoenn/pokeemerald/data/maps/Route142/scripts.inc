Route142_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route142_EventScript_Gabe::
	trainerbattle_single TRAINER_GABE, Route142_Text_GabeIntro, Route142_Text_GabeDefeat
	msgbox Route142_Text_GabePostBattle, MSGBOX_AUTOCLOSE
	end

Route142_Text_GabeIntro:
	.string "I've been waiting for someone like\nyou.$"

Route142_Text_GabeDefeat:
	.string "Beaten.$"

Route142_Text_GabePostBattle:
	.string "Rest before the next stretch.$"

Route142_EventScript_Kendra::
	trainerbattle_single TRAINER_KENDRA, Route142_Text_KendraIntro, Route142_Text_KendraDefeat
	msgbox Route142_Text_KendraPostBattle, MSGBOX_AUTOCLOSE
	end

Route142_Text_KendraIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route142_Text_KendraDefeat:
	.string "Well fought.$"

Route142_Text_KendraPostBattle:
	.string "Good luck out there.$"

Route142_EventScript_Lacey::
	trainerbattle_single TRAINER_LACEY, Route142_Text_LaceyIntro, Route142_Text_LaceyDefeat
	msgbox Route142_Text_LaceyPostBattle, MSGBOX_AUTOCLOSE
	end

Route142_Text_LaceyIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route142_Text_LaceyDefeat:
	.string "I underestimated you.$"

Route142_Text_LaceyPostBattle:
	.string "I'll be training when you come\nback.$"

