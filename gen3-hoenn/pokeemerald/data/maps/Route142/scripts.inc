Route142_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route142_EventScript_Harlow::
	trainerbattle_single TRAINER_HARLOW, Route142_Text_HarlowIntro, Route142_Text_HarlowDefeat
	msgbox Route142_Text_HarlowPostBattle, MSGBOX_AUTOCLOSE
	end

Route142_Text_HarlowIntro:
	.string "I've been waiting for someone like\nyou.$"

Route142_Text_HarlowDefeat:
	.string "Beaten.$"

Route142_Text_HarlowPostBattle:
	.string "Rest before the next stretch.$"

Route142_EventScript_Hazel::
	trainerbattle_single TRAINER_HAZEL, Route142_Text_HazelIntro, Route142_Text_HazelDefeat
	msgbox Route142_Text_HazelPostBattle, MSGBOX_AUTOCLOSE
	end

Route142_Text_HazelIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route142_Text_HazelDefeat:
	.string "Well fought.$"

Route142_Text_HazelPostBattle:
	.string "Good luck out there.$"

Route142_EventScript_Hollis::
	trainerbattle_single TRAINER_HOLLIS, Route142_Text_HollisIntro, Route142_Text_HollisDefeat
	msgbox Route142_Text_HollisPostBattle, MSGBOX_AUTOCLOSE
	end

Route142_Text_HollisIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route142_Text_HollisDefeat:
	.string "I underestimated you.$"

Route142_Text_HollisPostBattle:
	.string "I'll be training when you come\nback.$"

