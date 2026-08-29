Route142_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route142_EventScript_Fletch::
	trainerbattle_single TRAINER_FLETCH, Route142_Text_FletchIntro, Route142_Text_FletchDefeat
	msgbox Route142_Text_FletchPostBattle, MSGBOX_AUTOCLOSE
	end

Route142_Text_FletchIntro:
	.string "The fish can wait. You can't.$"

Route142_Text_FletchDefeat:
	.string "Should've stuck to the water.$"

Route142_Text_FletchPostBattle:
	.string "They bite better at dusk out here.$"

Route142_EventScript_Forrest::
	trainerbattle_single TRAINER_FORREST, Route142_Text_ForrestIntro, Route142_Text_ForrestDefeat
	msgbox Route142_Text_ForrestPostBattle, MSGBOX_AUTOCLOSE
	end

Route142_Text_ForrestIntro:
	.string "You've a look about you. A biting\nlook.$"

Route142_Text_ForrestDefeat:
	.string "A fine catch you are.$"

Route142_Text_ForrestPostBattle:
	.string "Still waters. Deep POKéMON.$"

Route142_EventScript_Frankie::
	trainerbattle_single TRAINER_FRANKIE, Route142_Text_FrankieIntro, Route142_Text_FrankieDefeat
	msgbox Route142_Text_FrankiePostBattle, MSGBOX_AUTOCLOSE
	end

Route142_Text_FrankieIntro:
	.string "I hook things that fight back.\pLike you.$"

Route142_Text_FrankieDefeat:
	.string "Slipped right through.$"

Route142_Text_FrankiePostBattle:
	.string "I'll be here till the light goes.$"

