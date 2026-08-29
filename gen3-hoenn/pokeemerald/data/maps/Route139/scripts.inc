Route139_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route139_EventScript_Dennis::
	trainerbattle_single TRAINER_DENNIS, Route139_Text_DennisIntro, Route139_Text_DennisDefeat
	msgbox Route139_Text_DennisPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_DennisIntro:
	.string "Battle me and I'll let you pass.$"

Route139_Text_DennisDefeat:
	.string "That settles it.$"

Route139_Text_DennisPostBattle:
	.string "Safe travels.$"

Route139_EventScript_Desmond::
	trainerbattle_single TRAINER_DESMOND, Route139_Text_DesmondIntro, Route139_Text_DesmondDefeat
	msgbox Route139_Text_DesmondPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_DesmondIntro:
	.string "Not many come this far. Battle me.$"

Route139_Text_DesmondDefeat:
	.string "You've come a long way indeed.$"

Route139_Text_DesmondPostBattle:
	.string "Keep heading on. It opens out.$"

Route139_EventScript_Esme::
	trainerbattle_single TRAINER_ESME, Route139_Text_EsmeIntro, Route139_Text_EsmeDefeat
	msgbox Route139_Text_EsmePostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_EsmeIntro:
	.string "A challenger! At last.$"

Route139_Text_EsmeDefeat:
	.string "The ROUTE is yours.$"

Route139_Text_EsmePostBattle:
	.string "There's more of us further along.$"

Route139_EventScript_Fenella::
	trainerbattle_single TRAINER_FENELLA, Route139_Text_FenellaIntro, Route139_Text_FenellaDefeat
	msgbox Route139_Text_FenellaPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_FenellaIntro:
	.string "I've been waiting for someone like\nyou.$"

Route139_Text_FenellaDefeat:
	.string "Beaten.$"

Route139_Text_FenellaPostBattle:
	.string "Rest before the next stretch.$"

Route139_EventScript_Dexter::
	trainerbattle_single TRAINER_DEXTER, Route139_Text_DexterIntro, Route139_Text_DexterDefeat
	msgbox Route139_Text_DexterPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_DexterIntro:
	.string "Bugs first, battles second. Or the\nother way.$"

Route139_Text_DexterDefeat:
	.string "I'll catch a better one.$"

Route139_Text_DexterPostBattle:
	.string "Good luck out there.$"

Route139_EventScript_Fiona::
	trainerbattle_single TRAINER_FIONA, Route139_Text_FionaIntro, Route139_Text_FionaDefeat
	msgbox Route139_Text_FionaPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_FionaIntro:
	.string "My POKéMON smell of the field.$"

Route139_Text_FionaDefeat:
	.string "I'll tend the beds instead.$"

Route139_Text_FionaPostBattle:
	.string "I'll be training when you come\nback.$"

Route139_EventScript_Flora::
	trainerbattle_single TRAINER_FLORA, Route139_Text_FloraIntro, Route139_Text_FloraDefeat
	msgbox Route139_Text_FloraPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_FloraIntro:
	.string "A short battle, before the light\ngoes.$"

Route139_Text_FloraDefeat:
	.string "Well grown.$"

Route139_Text_FloraPostBattle:
	.string "Safe travels.$"

Route139_EventScript_Driscoll::
	trainerbattle_single TRAINER_DRISCOLL, Route139_Text_DriscollIntro, Route139_Text_DriscollDefeat
	msgbox Route139_Text_DriscollPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_DriscollIntro:
	.string "Not many come this far. Battle me.$"

Route139_Text_DriscollDefeat:
	.string "You've come a long way indeed.$"

Route139_Text_DriscollPostBattle:
	.string "Keep heading on. It opens out.$"

Route139_EventScript_Dustin::
	trainerbattle_single TRAINER_DUSTIN, Route139_Text_DustinIntro, Route139_Text_DustinDefeat
	msgbox Route139_Text_DustinPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_DustinIntro:
	.string "A challenger! At last.$"

Route139_Text_DustinDefeat:
	.string "The ROUTE is yours.$"

Route139_Text_DustinPostBattle:
	.string "There's more of us further along.$"

Route139_EventScript_Gwendolen::
	trainerbattle_single TRAINER_GWENDOLEN, Route139_Text_GwendolenIntro, Route139_Text_GwendolenDefeat
	msgbox Route139_Text_GwendolenPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_GwendolenIntro:
	.string "I've been waiting for someone like\nyou.$"

Route139_Text_GwendolenDefeat:
	.string "Beaten.$"

Route139_Text_GwendolenPostBattle:
	.string "Rest before the next stretch.$"

Route139_EventScript_Earl::
	trainerbattle_single TRAINER_EARL, Route139_Text_EarlIntro, Route139_Text_EarlDefeat
	msgbox Route139_Text_EarlPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_EarlIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route139_Text_EarlDefeat:
	.string "Well fought.$"

Route139_Text_EarlPostBattle:
	.string "Good luck out there.$"

Route139_EventScript_Eldon::
	trainerbattle_single TRAINER_ELDON, Route139_Text_EldonIntro, Route139_Text_EldonDefeat
	msgbox Route139_Text_EldonPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_EldonIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route139_Text_EldonDefeat:
	.string "I underestimated you.$"

Route139_Text_EldonPostBattle:
	.string "I'll be training when you come\nback.$"

Route139_EventScript_Gilda::
	trainerbattle_single TRAINER_GILDA, Route139_Text_GildaIntro, Route139_Text_GildaDefeat
	msgbox Route139_Text_GildaPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_GildaIntro:
	.string "Battle me and I'll let you pass.$"

Route139_Text_GildaDefeat:
	.string "That settles it.$"

Route139_Text_GildaPostBattle:
	.string "Safe travels.$"

Route139_EventScript_Elias::
	trainerbattle_single TRAINER_ELIAS, Route139_Text_EliasIntro, Route139_Text_EliasDefeat
	msgbox Route139_Text_EliasPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_EliasIntro:
	.string "Not many come this far. Battle me.$"

Route139_Text_EliasDefeat:
	.string "You've come a long way indeed.$"

Route139_Text_EliasPostBattle:
	.string "Keep heading on. It opens out.$"

Route139_EventScript_Emmet::
	trainerbattle_single TRAINER_EMMET, Route139_Text_EmmetIntro, Route139_Text_EmmetDefeat
	msgbox Route139_Text_EmmetPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_EmmetIntro:
	.string "A challenger! At last.$"

Route139_Text_EmmetDefeat:
	.string "The ROUTE is yours.$"

Route139_Text_EmmetPostBattle:
	.string "There's more of us further along.$"

Route139_EventScript_Griselda::
	trainerbattle_single TRAINER_GRISELDA, Route139_Text_GriseldaIntro, Route139_Text_GriseldaDefeat
	msgbox Route139_Text_GriseldaPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_GriseldaIntro:
	.string "I've been waiting for someone like\nyou.$"

Route139_Text_GriseldaDefeat:
	.string "Beaten.$"

Route139_Text_GriseldaPostBattle:
	.string "Rest before the next stretch.$"

Route139_EventScript_Harriet::
	trainerbattle_single TRAINER_HARRIET, Route139_Text_HarrietIntro, Route139_Text_HarrietDefeat
	msgbox Route139_Text_HarrietPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_HarrietIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route139_Text_HarrietDefeat:
	.string "Well fought.$"

Route139_Text_HarrietPostBattle:
	.string "Good luck out there.$"

Route139_EventScript_Hazel::
	trainerbattle_single TRAINER_HAZEL, Route139_Text_HazelIntro, Route139_Text_HazelDefeat
	msgbox Route139_Text_HazelPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_HazelIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route139_Text_HazelDefeat:
	.string "I underestimated you.$"

Route139_Text_HazelPostBattle:
	.string "I'll be training when you come\nback.$"

Route139_EventScript_Imogen::
	trainerbattle_single TRAINER_IMOGEN, Route139_Text_ImogenIntro, Route139_Text_ImogenDefeat
	msgbox Route139_Text_ImogenPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_ImogenIntro:
	.string "Battle me and I'll let you pass.$"

Route139_Text_ImogenDefeat:
	.string "That settles it.$"

Route139_Text_ImogenPostBattle:
	.string "Safe travels.$"

Route139_EventScript_Enzo::
	trainerbattle_single TRAINER_ENZO, Route139_Text_EnzoIntro, Route139_Text_EnzoDefeat
	msgbox Route139_Text_EnzoPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_EnzoIntro:
	.string "Not many come this far. Battle me.$"

Route139_Text_EnzoDefeat:
	.string "You've come a long way indeed.$"

Route139_Text_EnzoPostBattle:
	.string "Keep heading on. It opens out.$"

Route139_EventScript_Evans::
	trainerbattle_single TRAINER_EVANS, Route139_Text_EvansIntro, Route139_Text_EvansDefeat
	msgbox Route139_Text_EvansPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_EvansIntro:
	.string "A challenger! At last.$"

Route139_Text_EvansDefeat:
	.string "The ROUTE is yours.$"

Route139_Text_EvansPostBattle:
	.string "There's more of us further along.$"

Route139_EventScript_Ingrid::
	trainerbattle_single TRAINER_INGRID, Route139_Text_IngridIntro, Route139_Text_IngridDefeat
	msgbox Route139_Text_IngridPostBattle, MSGBOX_AUTOCLOSE
	end

Route139_Text_IngridIntro:
	.string "I've been waiting for someone like\nyou.$"

Route139_Text_IngridDefeat:
	.string "Beaten.$"

Route139_Text_IngridPostBattle:
	.string "Rest before the next stretch.$"

