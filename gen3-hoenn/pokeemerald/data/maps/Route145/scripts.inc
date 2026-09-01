Route145_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

// Open Hoenn - tools/trainers.py

Route145_EventScript_Lorcan::
	trainerbattle_single TRAINER_LORCAN, Route145_Text_LorcanIntro, Route145_Text_LorcanDefeat
	msgbox Route145_Text_LorcanPostBattle, MSGBOX_AUTOCLOSE
	end

Route145_Text_LorcanIntro:
	.string "Cast off! Let's battle.$"

Route145_Text_LorcanDefeat:
	.string "Hah! Hooked myself.$"

Route145_Text_LorcanPostBattle:
	.string "Tight lines, TRAINER.$"

Route145_EventScript_Ludo::
	trainerbattle_single TRAINER_LUDO, Route145_Text_LudoIntro, Route145_Text_LudoDefeat
	msgbox Route145_Text_LudoPostBattle, MSGBOX_AUTOCLOSE
	end

Route145_Text_LudoIntro:
	.string "Look up. That's mine.\pNow look here - battle me.$"

Route145_Text_LudoDefeat:
	.string "Grounded.$"

Route145_Text_LudoPostBattle:
	.string "Keep heading on. It opens out.$"

Route145_EventScript_Magnus::
	trainerbattle_single TRAINER_MAGNUS, Route145_Text_MagnusIntro, Route145_Text_MagnusDefeat
	msgbox Route145_Text_MagnusPostBattle, MSGBOX_AUTOCLOSE
	end

Route145_Text_MagnusIntro:
	.string "They circle when a battle's coming.$"

Route145_Text_MagnusDefeat:
	.string "You clipped us.$"

Route145_Text_MagnusPostBattle:
	.string "There's more of us further along.$"

