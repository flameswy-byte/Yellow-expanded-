Route136_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route136_EventScript_Aubrey::
	trainerbattle_single TRAINER_AUBREY, Route136_Text_AubreyIntro, Route136_Text_AubreyDefeat
	msgbox Route136_Text_AubreyPostBattle, MSGBOX_AUTOCLOSE
	end

Route136_Text_AubreyIntro:
	.string "Cold? You get used to it.$"

Route136_Text_AubreyDefeat:
	.string "I'll float here a while.$"

Route136_Text_AubreyPostBattle:
	.string "I'll race you next time.$"

Route136_EventScript_Avery::
	trainerbattle_single TRAINER_AVERY, Route136_Text_AveryIntro, Route136_Text_AveryDefeat
	msgbox Route136_Text_AveryPostBattle, MSGBOX_AUTOCLOSE
	end

Route136_Text_AveryIntro:
	.string "Battle me and I'll let you pass.$"

Route136_Text_AveryDefeat:
	.string "That settles it.$"

Route136_Text_AveryPostBattle:
	.string "Safe travels.$"

Route136_EventScript_Barney::
	trainerbattle_single TRAINER_BARNEY, Route136_Text_BarneyIntro, Route136_Text_BarneyDefeat
	msgbox Route136_Text_BarneyPostBattle, MSGBOX_AUTOCLOSE
	end

Route136_Text_BarneyIntro:
	.string "Made camp here last night.\pBattle before I strike it?$"

Route136_Text_BarneyDefeat:
	.string "Time to pack.$"

Route136_Text_BarneyPostBattle:
	.string "Keep heading on. It opens out.$"

Route136_EventScript_Basil::
	trainerbattle_single TRAINER_BASIL, Route136_Text_BasilIntro, Route136_Text_BasilDefeat
	msgbox Route136_Text_BasilPostBattle, MSGBOX_AUTOCLOSE
	end

Route136_Text_BasilIntro:
	.string "Don't hold back. I won't.$"

Route136_Text_BasilDefeat:
	.string "You didn't waste my time.$"

Route136_Text_BasilPostBattle:
	.string "There's more of us further along.$"

Route136_EventScript_Becca::
	trainerbattle_single TRAINER_BECCA, Route136_Text_BeccaIntro, Route136_Text_BeccaDefeat
	msgbox Route136_Text_BeccaPostBattle, MSGBOX_AUTOCLOSE
	end

Route136_Text_BeccaIntro:
	.string "You look like you've been climbing\ntoo.\pProve it.$"

Route136_Text_BeccaDefeat:
	.string "Well climbed.$"

Route136_Text_BeccaPostBattle:
	.string "There's water further on. Fill up.$"

