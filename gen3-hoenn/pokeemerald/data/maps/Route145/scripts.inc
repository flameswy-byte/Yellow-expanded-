Route145_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

// Open Hoenn - tools/trainers.py

Route145_EventScript_Logan::
	trainerbattle_single TRAINER_LOGAN, Route145_Text_LoganIntro, Route145_Text_LoganDefeat
	msgbox Route145_Text_LoganPostBattle, MSGBOX_AUTOCLOSE
	end

Route145_Text_LoganIntro:
	.string "Fly at me, then.$"

Route145_Text_LoganDefeat:
	.string "Back to the nest.$"

Route145_Text_LoganPostBattle:
	.string "Safe travels.$"

Route145_EventScript_Lorcan::
	trainerbattle_single TRAINER_LORCAN, Route145_Text_LorcanIntro, Route145_Text_LorcanDefeat
	msgbox Route145_Text_LorcanPostBattle, MSGBOX_AUTOCLOSE
	end

Route145_Text_LorcanIntro:
	.string "Look up. That's mine.\pNow look here - battle me.$"

Route145_Text_LorcanDefeat:
	.string "Grounded.$"

Route145_Text_LorcanPostBattle:
	.string "Keep heading on. It opens out.$"

Route145_EventScript_Ludo::
	trainerbattle_single TRAINER_LUDO, Route145_Text_LudoIntro, Route145_Text_LudoDefeat
	msgbox Route145_Text_LudoPostBattle, MSGBOX_AUTOCLOSE
	end

Route145_Text_LudoIntro:
	.string "They circle when a battle's coming.$"

Route145_Text_LudoDefeat:
	.string "You clipped us.$"

Route145_Text_LudoPostBattle:
	.string "There's more of us further along.$"

