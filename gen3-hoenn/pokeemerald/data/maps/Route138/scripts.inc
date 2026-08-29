Route138_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route138_EventScript_Delia::
	trainerbattle_single TRAINER_DELIA, Route138_Text_DeliaIntro, Route138_Text_DeliaDefeat
	msgbox Route138_Text_DeliaPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_DeliaIntro:
	.string "Not many come this far. Battle me.$"

Route138_Text_DeliaDefeat:
	.string "You've come a long way indeed.$"

Route138_Text_DeliaPostBattle:
	.string "Keep heading on. It opens out.$"

Route138_EventScript_Dora::
	trainerbattle_single TRAINER_DORA, Route138_Text_DoraIntro, Route138_Text_DoraDefeat
	msgbox Route138_Text_DoraPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_DoraIntro:
	.string "A challenger! At last.$"

Route138_Text_DoraDefeat:
	.string "The ROUTE is yours.$"

Route138_Text_DoraPostBattle:
	.string "There's more of us further along.$"

Route138_EventScript_Edith::
	trainerbattle_single TRAINER_EDITH, Route138_Text_EdithIntro, Route138_Text_EdithDefeat
	msgbox Route138_Text_EdithPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_EdithIntro:
	.string "I've been waiting for someone like\nyou.$"

Route138_Text_EdithDefeat:
	.string "Beaten.$"

Route138_Text_EdithPostBattle:
	.string "Rest before the next stretch.$"

Route138_EventScript_Colby::
	trainerbattle_single TRAINER_COLBY, Route138_Text_ColbyIntro, Route138_Text_ColbyDefeat
	msgbox Route138_Text_ColbyPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_ColbyIntro:
	.string "o$"

Route138_Text_ColbyDefeat:
	.string "l$"

Route138_Text_ColbyPostBattle:
	.string "T$"

Route138_EventScript_Corwin::
	trainerbattle_single TRAINER_CORWIN, Route138_Text_CorwinIntro, Route138_Text_CorwinDefeat
	msgbox Route138_Text_CorwinPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_CorwinIntro:
	.string "Cold? You get used to it.$"

Route138_Text_CorwinDefeat:
	.string "I'll float here a while.$"

Route138_Text_CorwinPostBattle:
	.string "I'll race you next time.$"

Route138_EventScript_Craig::
	trainerbattle_single TRAINER_CRAIG, Route138_Text_CraigIntro, Route138_Text_CraigDefeat
	msgbox Route138_Text_CraigPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_CraigIntro:
	.string "Battle me and I'll let you pass.$"

Route138_Text_CraigDefeat:
	.string "That settles it.$"

Route138_Text_CraigPostBattle:
	.string "Safe travels.$"

Route138_EventScript_Effie::
	trainerbattle_single TRAINER_EFFIE, Route138_Text_EffieIntro, Route138_Text_EffieDefeat
	msgbox Route138_Text_EffiePostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_EffieIntro:
	.string "Not many come this far. Battle me.$"

Route138_Text_EffieDefeat:
	.string "You've come a long way indeed.$"

Route138_Text_EffiePostBattle:
	.string "Keep heading on. It opens out.$"

Route138_EventScript_Eloise::
	trainerbattle_single TRAINER_ELOISE, Route138_Text_EloiseIntro, Route138_Text_EloiseDefeat
	msgbox Route138_Text_EloisePostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_EloiseIntro:
	.string "A challenger! At last.$"

Route138_Text_EloiseDefeat:
	.string "The ROUTE is yours.$"

Route138_Text_EloisePostBattle:
	.string "There's more of us further along.$"

Route138_EventScript_Curtis::
	trainerbattle_single TRAINER_CURTIS, Route138_Text_CurtisIntro, Route138_Text_CurtisDefeat
	msgbox Route138_Text_CurtisPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_CurtisIntro:
	.string "I've been waiting for someone like\nyou.$"

Route138_Text_CurtisDefeat:
	.string "Beaten.$"

Route138_Text_CurtisPostBattle:
	.string "Rest before the next stretch.$"

Route138_EventScript_Esme::
	trainerbattle_single TRAINER_ESME, Route138_Text_EsmeIntro, Route138_Text_EsmeDefeat
	msgbox Route138_Text_EsmePostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_EsmeIntro:
	.string "You walked. I swam. Let's settle\nit.$"

Route138_Text_EsmeDefeat:
	.string "The current's yours.$"

Route138_Text_EsmePostBattle:
	.string "There's a beach north of here. Rest\nthere.$"

Route138_EventScript_Fenella::
	trainerbattle_single TRAINER_FENELLA, Route138_Text_FenellaIntro, Route138_Text_FenellaDefeat
	msgbox Route138_Text_FenellaPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_FenellaIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route138_Text_FenellaDefeat:
	.string "I underestimated you.$"

Route138_Text_FenellaPostBattle:
	.string "I'll be training when you come\nback.$"

