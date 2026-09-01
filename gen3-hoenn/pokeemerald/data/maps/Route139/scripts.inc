Route139_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

Route139_EventScript_RouteSignVerdanturfTown::
	msgbox Route139_Text_RouteSignVerdanturfTown, MSGBOX_SIGN
	end

Route139_Text_RouteSignVerdanturfTown:
	.string "ROUTE 139\n"
	.string "{UP_ARROW} VERDANTURF TOWN$"

// Open Hoenn - tools/trainers.py

Route139_EventScript_Darby::
	trainerbattle_single TRAINER_DARBY, Route139_Text_DarbyIntro, Route139_Text_DarbyDefeat
	msgbox Route139_Text_DarbyPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_DarbyIntro:
	.string "Battle me and I'll let you pass.$"

Route139_Text_DarbyDefeat:
	.string "That settles it.$"

Route139_Text_DarbyPostBattle:
	.string "Safe travels.$"

Route139_EventScript_Dennis::
	trainerbattle_single TRAINER_DENNIS, Route139_Text_DennisIntro, Route139_Text_DennisDefeat
	msgbox Route139_Text_DennisPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_DennisIntro:
	.string "Not many come this far. Battle me.$"

Route139_Text_DennisDefeat:
	.string "You've come a long way indeed.$"

Route139_Text_DennisPostBattle:
	.string "Keep heading on. It opens out.$"

Route139_EventScript_Desmond::
	trainerbattle_single TRAINER_DESMOND, Route139_Text_DesmondIntro, Route139_Text_DesmondDefeat
	msgbox Route139_Text_DesmondPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_DesmondIntro:
	.string "A challenger! At last.$"

Route139_Text_DesmondDefeat:
	.string "The ROUTE is yours.$"

Route139_Text_DesmondPostBattle:
	.string "There's more of us further along.$"

Route139_EventScript_Dexter::
	trainerbattle_single TRAINER_DEXTER, Route139_Text_DexterIntro, Route139_Text_DexterDefeat
	msgbox Route139_Text_DexterPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_DexterIntro:
	.string "I've been waiting for someone like\nyou.$"

Route139_Text_DexterDefeat:
	.string "Beaten.$"

Route139_Text_DexterPostBattle:
	.string "Rest before the next stretch.$"

Route139_EventScript_Driscoll::
	trainerbattle_single TRAINER_DRISCOLL, Route139_Text_DriscollIntro, Route139_Text_DriscollDefeat
	msgbox Route139_Text_DriscollPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_DriscollIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route139_Text_DriscollDefeat:
	.string "Well fought.$"

Route139_Text_DriscollPostBattle:
	.string "Good luck out there.$"

Route139_EventScript_Fenella::
	trainerbattle_single TRAINER_FENELLA, Route139_Text_FenellaIntro, Route139_Text_FenellaDefeat
	msgbox Route139_Text_FenellaPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_FenellaIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route139_Text_FenellaDefeat:
	.string "I underestimated you.$"

Route139_Text_FenellaPostBattle:
	.string "I'll be training when you come\nback.$"

Route139_EventScript_Fiona::
	trainerbattle_single TRAINER_FIONA, Route139_Text_FionaIntro, Route139_Text_FionaDefeat
	msgbox Route139_Text_FionaPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_FionaIntro:
	.string "Battle me and I'll let you pass.$"

Route139_Text_FionaDefeat:
	.string "That settles it.$"

Route139_Text_FionaPostBattle:
	.string "Safe travels.$"

Route139_EventScript_Dustin::
	trainerbattle_single TRAINER_DUSTIN, Route139_Text_DustinIntro, Route139_Text_DustinDefeat
	msgbox Route139_Text_DustinPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_DustinIntro:
	.string "Shh - I've almost -\pAh. Battle me instead.$"

Route139_Text_DustinDefeat:
	.string "It got away. So did the win.$"

Route139_Text_DustinPostBattle:
	.string "Keep heading on. It opens out.$"

Route139_EventScript_Earl::
	trainerbattle_single TRAINER_EARL, Route139_Text_EarlIntro, Route139_Text_EarlDefeat
	msgbox Route139_Text_EarlPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_EarlIntro:
	.string "There's a rare one on this ROUTE.\nReally!$"

Route139_Text_EarlDefeat:
	.string "You're quicker than a bug.$"

Route139_Text_EarlPostBattle:
	.string "There's more of us further along.$"

Route139_EventScript_Flora::
	trainerbattle_single TRAINER_FLORA, Route139_Text_FloraIntro, Route139_Text_FloraDefeat
	msgbox Route139_Text_FloraPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_FloraIntro:
	.string "Everything on this ROUTE flowers\neventually.$"

Route139_Text_FloraDefeat:
	.string "Beaten among the flowers.$"

Route139_Text_FloraPostBattle:
	.string "Rest before the next stretch.$"

Route139_EventScript_Eldon::
	trainerbattle_single TRAINER_ELDON, Route139_Text_EldonIntro, Route139_Text_EldonDefeat
	msgbox Route139_Text_EldonPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_EldonIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route139_Text_EldonDefeat:
	.string "Well fought.$"

Route139_Text_EldonPostBattle:
	.string "Good luck out there.$"

Route139_EventScript_Elias::
	trainerbattle_single TRAINER_ELIAS, Route139_Text_EliasIntro, Route139_Text_EliasDefeat
	msgbox Route139_Text_EliasPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_EliasIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route139_Text_EliasDefeat:
	.string "I underestimated you.$"

Route139_Text_EliasPostBattle:
	.string "I'll be training when you come\nback.$"

Route139_EventScript_Gwendolen::
	trainerbattle_single TRAINER_GWENDOLEN, Route139_Text_GwendolenIntro, Route139_Text_GwendolenDefeat
	msgbox Route139_Text_GwendolenPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_GwendolenIntro:
	.string "Battle me and I'll let you pass.$"

Route139_Text_GwendolenDefeat:
	.string "That settles it.$"

Route139_Text_GwendolenPostBattle:
	.string "Safe travels.$"

Route139_EventScript_Emmet::
	trainerbattle_single TRAINER_EMMET, Route139_Text_EmmetIntro, Route139_Text_EmmetDefeat
	msgbox Route139_Text_EmmetPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_EmmetIntro:
	.string "Not many come this far. Battle me.$"

Route139_Text_EmmetDefeat:
	.string "You've come a long way indeed.$"

Route139_Text_EmmetPostBattle:
	.string "Keep heading on. It opens out.$"

Route139_EventScript_Enzo::
	trainerbattle_single TRAINER_ENZO, Route139_Text_EnzoIntro, Route139_Text_EnzoDefeat
	msgbox Route139_Text_EnzoPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_EnzoIntro:
	.string "A challenger! At last.$"

Route139_Text_EnzoDefeat:
	.string "The ROUTE is yours.$"

Route139_Text_EnzoPostBattle:
	.string "There's more of us further along.$"

Route139_EventScript_Gilda::
	trainerbattle_single TRAINER_GILDA, Route139_Text_GildaIntro, Route139_Text_GildaDefeat
	msgbox Route139_Text_GildaPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_GildaIntro:
	.string "I've been waiting for someone like\nyou.$"

Route139_Text_GildaDefeat:
	.string "Beaten.$"

Route139_Text_GildaPostBattle:
	.string "Rest before the next stretch.$"

Route139_EventScript_Evans::
	trainerbattle_single TRAINER_EVANS, Route139_Text_EvansIntro, Route139_Text_EvansDefeat
	msgbox Route139_Text_EvansPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_EvansIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route139_Text_EvansDefeat:
	.string "Well fought.$"

Route139_Text_EvansPostBattle:
	.string "Good luck out there.$"

Route139_EventScript_Fenwick::
	trainerbattle_single TRAINER_FENWICK, Route139_Text_FenwickIntro, Route139_Text_FenwickDefeat
	msgbox Route139_Text_FenwickPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_FenwickIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route139_Text_FenwickDefeat:
	.string "I underestimated you.$"

Route139_Text_FenwickPostBattle:
	.string "I'll be training when you come\nback.$"

Route139_EventScript_Griselda::
	trainerbattle_single TRAINER_GRISELDA, Route139_Text_GriseldaIntro, Route139_Text_GriseldaDefeat
	msgbox Route139_Text_GriseldaPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_GriseldaIntro:
	.string "Battle me and I'll let you pass.$"

Route139_Text_GriseldaDefeat:
	.string "That settles it.$"

Route139_Text_GriseldaPostBattle:
	.string "Safe travels.$"

Route139_EventScript_Harriet::
	trainerbattle_single TRAINER_HARRIET, Route139_Text_HarrietIntro, Route139_Text_HarrietDefeat
	msgbox Route139_Text_HarrietPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_HarrietIntro:
	.string "Not many come this far. Battle me.$"

Route139_Text_HarrietDefeat:
	.string "You've come a long way indeed.$"

Route139_Text_HarrietPostBattle:
	.string "Keep heading on. It opens out.$"

Route139_EventScript_Ferris::
	trainerbattle_single TRAINER_FERRIS, Route139_Text_FerrisIntro, Route139_Text_FerrisDefeat
	msgbox Route139_Text_FerrisPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_FerrisIntro:
	.string "A challenger! At last.$"

Route139_Text_FerrisDefeat:
	.string "The ROUTE is yours.$"

Route139_Text_FerrisPostBattle:
	.string "There's more of us further along.$"

Route139_EventScript_Hazel::
	trainerbattle_single TRAINER_HAZEL, Route139_Text_HazelIntro, Route139_Text_HazelDefeat
	msgbox Route139_Text_HazelPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_HazelIntro:
	.string "I've been waiting for someone like\nyou.$"

Route139_Text_HazelDefeat:
	.string "Beaten.$"

Route139_Text_HazelPostBattle:
	.string "Rest before the next stretch.$"

