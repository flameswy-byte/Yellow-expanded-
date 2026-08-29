Route138_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

Route138_EventScript_RouteSignLittlerootTown::
	msgbox Route138_Text_RouteSignLittlerootTown, MSGBOX_SIGN
	end

Route138_Text_RouteSignLittlerootTown:
	.string "ROUTE 138\n"
	.string "{LEFT_ARROW} LITTLEROOT TOWN$"

Route138_EventScript_RouteSignOldaleTown::
	msgbox Route138_Text_RouteSignOldaleTown, MSGBOX_SIGN
	end

Route138_Text_RouteSignOldaleTown:
	.string "ROUTE 138\n"
	.string "{LEFT_ARROW} OLDALE TOWN$"

// Open Hoenn - tools/trainers.py

Route138_EventScript_Colby::
	trainerbattle_single TRAINER_COLBY, Route138_Text_ColbyIntro, Route138_Text_ColbyDefeat
	msgbox Route138_Text_ColbyPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_ColbyIntro:
	.string "Look up. That's mine.\pNow look here - battle me.$"

Route138_Text_ColbyDefeat:
	.string "Grounded.$"

Route138_Text_ColbyPostBattle:
	.string "Keep heading on. It opens out.$"

Route138_EventScript_Corwin::
	trainerbattle_single TRAINER_CORWIN, Route138_Text_CorwinIntro, Route138_Text_CorwinDefeat
	msgbox Route138_Text_CorwinPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_CorwinIntro:
	.string "They circle when a battle's coming.$"

Route138_Text_CorwinDefeat:
	.string "You clipped us.$"

Route138_Text_CorwinPostBattle:
	.string "There's more of us further along.$"

Route138_EventScript_Delia::
	trainerbattle_single TRAINER_DELIA, Route138_Text_DeliaIntro, Route138_Text_DeliaDefeat
	msgbox Route138_Text_DeliaPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_DeliaIntro:
	.string "You've walked a long way. Sit!\n...After.$"

Route138_Text_DeliaDefeat:
	.string "Beaten before dessert.$"

Route138_Text_DeliaPostBattle:
	.string "Rest before the next stretch.$"

Route138_EventScript_Dora::
	trainerbattle_single TRAINER_DORA, Route138_Text_DoraIntro, Route138_Text_DoraDefeat
	msgbox Route138_Text_DoraPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_DoraIntro:
	.string "The weather held. Let's use it.$"

Route138_Text_DoraDefeat:
	.string "How nice. And how losing.$"

Route138_Text_DoraPostBattle:
	.string "Good luck out there.$"

Route138_EventScript_Craig::
	trainerbattle_single TRAINER_CRAIG, Route138_Text_CraigIntro, Route138_Text_CraigDefeat
	msgbox Route138_Text_CraigPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_CraigIntro:
	.string "Cold? You get used to it.$"

Route138_Text_CraigDefeat:
	.string "I'll float here a while.$"

Route138_Text_CraigPostBattle:
	.string "I'll race you next time.$"

Route138_EventScript_Edith::
	trainerbattle_single TRAINER_EDITH, Route138_Text_EdithIntro, Route138_Text_EdithDefeat
	msgbox Route138_Text_EdithPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_EdithIntro:
	.string "Sandwich? No? Battle, then.$"

Route138_Text_EdithDefeat:
	.string "I'll pack up, then.$"

Route138_Text_EdithPostBattle:
	.string "Safe travels.$"

Route138_EventScript_Curtis::
	trainerbattle_single TRAINER_CURTIS, Route138_Text_CurtisIntro, Route138_Text_CurtisDefeat
	msgbox Route138_Text_CurtisPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_CurtisIntro:
	.string "I'm not lost! I'm training!\pBattle me and I'll prove it.$"

Route138_Text_CurtisDefeat:
	.string "I'm still not lost.$"

Route138_Text_CurtisPostBattle:
	.string "I'm going to battle everyone on\nthis ROUTE.$"

Route138_EventScript_Derwent::
	trainerbattle_single TRAINER_DERWENT, Route138_Text_DerwentIntro, Route138_Text_DerwentDefeat
	msgbox Route138_Text_DerwentPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_DerwentIntro:
	.string "My POKéMON is stronger than\nyesterday!$"

Route138_Text_DerwentDefeat:
	.string "Yesterday me would have lost worse.$"

Route138_Text_DerwentPostBattle:
	.string "There's tall grass back that way.\nGood grass.$"

Route138_EventScript_Darby::
	trainerbattle_single TRAINER_DARBY, Route138_Text_DarbyIntro, Route138_Text_DarbyDefeat
	msgbox Route138_Text_DarbyPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_DarbyIntro:
	.string "Hey! Nobody comes down here!\pBattle me!$"

Route138_Text_DarbyDefeat:
	.string "Aww.$"

Route138_Text_DarbyPostBattle:
	.string "When I'm big I'll have six POKéMON.$"

Route138_EventScript_Effie::
	trainerbattle_single TRAINER_EFFIE, Route138_Text_EffieIntro, Route138_Text_EffieDefeat
	msgbox Route138_Text_EffiePostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_EffieIntro:
	.string "You walked. I swam. Let's settle\nit.$"

Route138_Text_EffieDefeat:
	.string "The current's yours.$"

Route138_Text_EffiePostBattle:
	.string "There's a beach north of here. Rest\nthere.$"

Route138_EventScript_Eloise::
	trainerbattle_single TRAINER_ELOISE, Route138_Text_EloiseIntro, Route138_Text_EloiseDefeat
	msgbox Route138_Text_EloisePostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_EloiseIntro:
	.string "Show me the team that got you this\nfar.$"

Route138_Text_EloiseDefeat:
	.string "Good. Very good.$"

Route138_Text_EloisePostBattle:
	.string "I'll be training when you come\nback.$"

