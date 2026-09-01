Route140_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

// Open Hoenn - tools/trainers.py

Route140_EventScript_Finlay::
	trainerbattle_single TRAINER_FINLAY, Route140_Text_FinlayIntro, Route140_Text_FinlayDefeat
	msgbox Route140_Text_FinlayPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_FinlayIntro:
	.string "The sky's clear. Perfect for it.$"

Route140_Text_FinlayDefeat:
	.string "The sky's yours today.$"

Route140_Text_FinlayPostBattle:
	.string "Good luck out there.$"

Route140_EventScript_Imogen::
	trainerbattle_single TRAINER_IMOGEN, Route140_Text_ImogenIntro, Route140_Text_ImogenDefeat
	msgbox Route140_Text_ImogenPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_ImogenIntro:
	.string "My POKéMON eat better than I do.$"

Route140_Text_ImogenDefeat:
	.string "A picnic and a defeat.$"

Route140_Text_ImogenPostBattle:
	.string "I'll be training when you come\nback.$"

Route140_EventScript_Ingrid::
	trainerbattle_single TRAINER_INGRID, Route140_Text_IngridIntro, Route140_Text_IngridDefeat
	msgbox Route140_Text_IngridPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_IngridIntro:
	.string "Sandwich? No? Battle, then.$"

Route140_Text_IngridDefeat:
	.string "I'll pack up, then.$"

Route140_Text_IngridPostBattle:
	.string "Safe travels.$"

Route140_EventScript_Iris::
	trainerbattle_single TRAINER_IRIS, Route140_Text_IrisIntro, Route140_Text_IrisDefeat
	msgbox Route140_Text_IrisPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_IrisIntro:
	.string "The water's fine! Come in and\nbattle.$"

Route140_Text_IrisDefeat:
	.string "Out of my depth.$"

Route140_Text_IrisPostBattle:
	.string "Careful past the point. It's\ndeeper.$"

Route140_EventScript_Fletch::
	trainerbattle_single TRAINER_FLETCH, Route140_Text_FletchIntro, Route140_Text_FletchDefeat
	msgbox Route140_Text_FletchPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_FletchIntro:
	.string "My POKéMON is stronger than\nyesterday!$"

Route140_Text_FletchDefeat:
	.string "Yesterday me would have lost worse.$"

Route140_Text_FletchPostBattle:
	.string "There's tall grass back that way.\nGood grass.$"

Route140_EventScript_Forrest::
	trainerbattle_single TRAINER_FORREST, Route140_Text_ForrestIntro, Route140_Text_ForrestDefeat
	msgbox Route140_Text_ForrestPostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_ForrestIntro:
	.string "Hey! Nobody comes down here!\pBattle me!$"

Route140_Text_ForrestDefeat:
	.string "Aww.$"

Route140_Text_ForrestPostBattle:
	.string "When I'm big I'll have six POKéMON.$"

Route140_EventScript_Frankie::
	trainerbattle_single TRAINER_FRANKIE, Route140_Text_FrankieIntro, Route140_Text_FrankieDefeat
	msgbox Route140_Text_FrankiePostBattle, MSGBOX_AUTOCLOSE
	end

Route140_Text_FrankieIntro:
	.string "I walked all this way for a battle.$"

Route140_Text_FrankieDefeat:
	.string "You're really strong!$"

Route140_Text_FrankiePostBattle:
	.string "Do you know the way out? ...Me\nneither.$"

