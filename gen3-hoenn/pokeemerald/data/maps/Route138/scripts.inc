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

Route138_EventScript_Clive::
	trainerbattle_single TRAINER_CLIVE, Route138_Text_CliveIntro, Route138_Text_CliveDefeat
	msgbox Route138_Text_ClivePostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_CliveIntro:
	.string "Quiet! ...Ah, you've scared them\noff.\pYou owe me a battle.$"

Route138_Text_CliveDefeat:
	.string "Reeled in and thrown back.$"

Route138_Text_ClivePostBattle:
	.string "Best water's round the bend. Try\nit.$"

Route138_EventScript_Conrad::
	trainerbattle_single TRAINER_CONRAD, Route138_Text_ConradIntro, Route138_Text_ConradDefeat
	msgbox Route138_Text_ConradPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_ConradIntro:
	.string "They circle when a battle's coming.$"

Route138_Text_ConradDefeat:
	.string "You clipped us.$"

Route138_Text_ConradPostBattle:
	.string "There's more of us further along.$"

Route138_EventScript_Colby::
	trainerbattle_single TRAINER_COLBY, Route138_Text_ColbyIntro, Route138_Text_ColbyDefeat
	msgbox Route138_Text_ColbyPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_ColbyIntro:
	.string "My birds saw you before I did.$"

Route138_Text_ColbyDefeat:
	.string "Down we come.$"

Route138_Text_ColbyPostBattle:
	.string "Rest before the next stretch.$"

Route138_EventScript_Corwin::
	trainerbattle_single TRAINER_CORWIN, Route138_Text_CorwinIntro, Route138_Text_CorwinDefeat
	msgbox Route138_Text_CorwinPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_CorwinIntro:
	.string "The sky's clear. Perfect for it.$"

Route138_Text_CorwinDefeat:
	.string "The sky's yours today.$"

Route138_Text_CorwinPostBattle:
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

Route138_EventScript_Curtis::
	trainerbattle_single TRAINER_CURTIS, Route138_Text_CurtisIntro, Route138_Text_CurtisDefeat
	msgbox Route138_Text_CurtisPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_CurtisIntro:
	.string "Fly at me, then.$"

Route138_Text_CurtisDefeat:
	.string "Back to the nest.$"

Route138_Text_CurtisPostBattle:
	.string "Safe travels.$"

Route138_EventScript_Edith::
	trainerbattle_single TRAINER_EDITH, Route138_Text_EdithIntro, Route138_Text_EdithDefeat
	msgbox Route138_Text_EdithPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_EdithIntro:
	.string "Lovely spot for lunch.\pAnd a battle.$"

Route138_Text_EdithDefeat:
	.string "Well, that's the afternoon gone.$"

Route138_Text_EdithPostBattle:
	.string "Keep heading on. It opens out.$"

Route138_EventScript_Effie::
	trainerbattle_single TRAINER_EFFIE, Route138_Text_EffieIntro, Route138_Text_EffieDefeat
	msgbox Route138_Text_EffiePostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_EffieIntro:
	.string "I packed for two. Battle first?$"

Route138_Text_EffieDefeat:
	.string "You've earned lunch.$"

Route138_Text_EffiePostBattle:
	.string "There's more of us further along.$"

Route138_EventScript_Eloise::
	trainerbattle_single TRAINER_ELOISE, Route138_Text_EloiseIntro, Route138_Text_EloiseDefeat
	msgbox Route138_Text_EloisePostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_EloiseIntro:
	.string "You've walked a long way. Sit!\n...After.$"

Route138_Text_EloiseDefeat:
	.string "Beaten before dessert.$"

Route138_Text_EloisePostBattle:
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

Route138_EventScript_Derwent::
	trainerbattle_single TRAINER_DERWENT, Route138_Text_DerwentIntro, Route138_Text_DerwentDefeat
	msgbox Route138_Text_DerwentPostBattle, MSGBOX_AUTOCLOSE
	end

Route138_Text_DerwentIntro:
	.string "You look tough. I'm tougher.$"

Route138_Text_DerwentDefeat:
	.string "I'll train more.$"

Route138_Text_DerwentPostBattle:
	.string "I'll remember you!$"

