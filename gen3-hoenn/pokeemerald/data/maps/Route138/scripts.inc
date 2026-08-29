Route138_MapScripts::
	.byte 0

// Open Hoenn - tools/trainers.py

Route138_EventScript_Corwin::
	trainerbattle_single TRAINER_CORWIN, Route138_Text_CorwinIntro, Route138_Text_CorwinDefeat
	msgbox Route138_Text_CorwinPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_CorwinIntro:
	.string "Not many come this far. Battle me.$"

Route138_Text_CorwinDefeat:
	.string "You've come a long way indeed.$"

Route138_Text_CorwinPostBattle:
	.string "Keep heading on. It opens out.$"

Route138_EventScript_Craig::
	trainerbattle_single TRAINER_CRAIG, Route138_Text_CraigIntro, Route138_Text_CraigDefeat
	msgbox Route138_Text_CraigPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_CraigIntro:
	.string "A challenger! At last.$"

Route138_Text_CraigDefeat:
	.string "The ROUTE is yours.$"

Route138_Text_CraigPostBattle:
	.string "There's more of us further along.$"

Route138_EventScript_Curtis::
	trainerbattle_single TRAINER_CURTIS, Route138_Text_CurtisIntro, Route138_Text_CurtisDefeat
	msgbox Route138_Text_CurtisPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_CurtisIntro:
	.string "y$"

Route138_Text_CurtisDefeat:
	.string "l$"

Route138_Text_CurtisPostBattle:
	.string "U$"

Route138_EventScript_Dahlia::
	trainerbattle_single TRAINER_DAHLIA, Route138_Text_DahliaIntro, Route138_Text_DahliaDefeat
	msgbox Route138_Text_DahliaPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_DahliaIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route138_Text_DahliaDefeat:
	.string "Well fought.$"

Route138_Text_DahliaPostBattle:
	.string "Good luck out there.$"

Route138_EventScript_Derwent::
	trainerbattle_single TRAINER_DERWENT, Route138_Text_DerwentIntro, Route138_Text_DerwentDefeat
	msgbox Route138_Text_DerwentPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_DerwentIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route138_Text_DerwentDefeat:
	.string "I underestimated you.$"

Route138_Text_DerwentPostBattle:
	.string "I'll be training when you come\nback.$"

Route138_EventScript_Darby::
	trainerbattle_single TRAINER_DARBY, Route138_Text_DarbyIntro, Route138_Text_DarbyDefeat
	msgbox Route138_Text_DarbyPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_DarbyIntro:
	.string "Battle me and I'll let you pass.$"

Route138_Text_DarbyDefeat:
	.string "That settles it.$"

Route138_Text_DarbyPostBattle:
	.string "Safe travels.$"

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

Route138_EventScript_Dennis::
	trainerbattle_single TRAINER_DENNIS, Route138_Text_DennisIntro, Route138_Text_DennisDefeat
	msgbox Route138_Text_DennisPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_DennisIntro:
	.string "A challenger! At last.$"

Route138_Text_DennisDefeat:
	.string "The ROUTE is yours.$"

Route138_Text_DennisPostBattle:
	.string "There's more of us further along.$"

Route138_EventScript_Desmond::
	trainerbattle_single TRAINER_DESMOND, Route138_Text_DesmondIntro, Route138_Text_DesmondDefeat
	msgbox Route138_Text_DesmondPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_DesmondIntro:
	.string "I've been waiting for someone like\nyou.$"

Route138_Text_DesmondDefeat:
	.string "Beaten.$"

Route138_Text_DesmondPostBattle:
	.string "Rest before the next stretch.$"

Route138_EventScript_Dexter::
	trainerbattle_single TRAINER_DEXTER, Route138_Text_DexterIntro, Route138_Text_DexterDefeat
	msgbox Route138_Text_DexterPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_DexterIntro:
	.string "You walked. I swam. Let's settle\nit.$"

Route138_Text_DexterDefeat:
	.string "The current's yours.$"

Route138_Text_DexterPostBattle:
	.string "There's a beach north of here. Rest\nthere.$"

Route138_EventScript_Driscoll::
	trainerbattle_single TRAINER_DRISCOLL, Route138_Text_DriscollIntro, Route138_Text_DriscollDefeat
	msgbox Route138_Text_DriscollPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_DriscollIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route138_Text_DriscollDefeat:
	.string "I underestimated you.$"

Route138_Text_DriscollPostBattle:
	.string "I'll be training when you come\nback.$"

