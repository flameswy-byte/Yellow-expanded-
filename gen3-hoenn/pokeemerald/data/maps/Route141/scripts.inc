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

Route141_EventScript_Finlay::
	trainerbattle_single TRAINER_FINLAY, Route141_Text_FinlayIntro, Route141_Text_FinlayDefeat
	msgbox Route141_Text_FinlayPostBattle, MSGBOX_AUTOCLOSE
	end

Route141_Text_FinlayIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route141_Text_FinlayDefeat:
	.string "I underestimated you.$"

Route141_Text_FinlayPostBattle:
	.string "I'll be training when you come\nback.$"

Route141_EventScript_Fletch::
	trainerbattle_single TRAINER_FLETCH, Route141_Text_FletchIntro, Route141_Text_FletchDefeat
	msgbox Route141_Text_FletchPostBattle, MSGBOX_AUTOCLOSE
	end

Route141_Text_FletchIntro:
	.string "Six legs beat two!$"

Route141_Text_FletchDefeat:
	.string "Back to the grass.$"

Route141_Text_FletchPostBattle:
	.string "Safe travels.$"

Route141_EventScript_Forrest::
	trainerbattle_single TRAINER_FORREST, Route141_Text_ForrestIntro, Route141_Text_ForrestDefeat
	msgbox Route141_Text_ForrestPostBattle, MSGBOX_AUTOCLOSE
	end

Route141_Text_ForrestIntro:
	.string "Look up. That's mine.\pNow look here - battle me.$"

Route141_Text_ForrestDefeat:
	.string "Grounded.$"

Route141_Text_ForrestPostBattle:
	.string "Keep heading on. It opens out.$"

Route141_EventScript_Frankie::
	trainerbattle_single TRAINER_FRANKIE, Route141_Text_FrankieIntro, Route141_Text_FrankieDefeat
	msgbox Route141_Text_FrankiePostBattle, MSGBOX_AUTOCLOSE
	end

Route141_Text_FrankieIntro:
	.string "They circle when a battle's coming.$"

Route141_Text_FrankieDefeat:
	.string "You clipped us.$"

Route141_Text_FrankiePostBattle:
	.string "There's more of us further along.$"

