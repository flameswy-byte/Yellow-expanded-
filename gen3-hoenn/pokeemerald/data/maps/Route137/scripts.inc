Route137_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

Route137_EventScript_RouteSignLittlerootTown::
	msgbox Route137_Text_RouteSignLittlerootTown, MSGBOX_SIGN
	end

Route137_Text_RouteSignLittlerootTown:
	.string "ROUTE 137\n"
	.string "{UP_ARROW} LITTLEROOT TOWN$"

// Open Hoenn - tools/trainers.py

Route137_EventScript_Barney::
	trainerbattle_single TRAINER_BARNEY, Route137_Text_BarneyIntro, Route137_Text_BarneyDefeat
	msgbox Route137_Text_BarneyPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_BarneyIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route137_Text_BarneyDefeat:
	.string "Well fought.$"

Route137_Text_BarneyPostBattle:
	.string "Good luck out there.$"

Route137_EventScript_Basil::
	trainerbattle_single TRAINER_BASIL, Route137_Text_BasilIntro, Route137_Text_BasilDefeat
	msgbox Route137_Text_BasilPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_BasilIntro:
	.string "Cold? You get used to it.$"

Route137_Text_BasilDefeat:
	.string "I'll float here a while.$"

Route137_Text_BasilPostBattle:
	.string "I'll race you next time.$"

Route137_EventScript_Branwen::
	trainerbattle_single TRAINER_BRANWEN, Route137_Text_BranwenIntro, Route137_Text_BranwenDefeat
	msgbox Route137_Text_BranwenPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_BranwenIntro:
	.string "Battle me and I'll let you pass.$"

Route137_Text_BranwenDefeat:
	.string "That settles it.$"

Route137_Text_BranwenPostBattle:
	.string "Safe travels.$"

Route137_EventScript_Benno::
	trainerbattle_single TRAINER_BENNO, Route137_Text_BennoIntro, Route137_Text_BennoDefeat
	msgbox Route137_Text_BennoPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_BennoIntro:
	.string "Not many come this far. Battle me.$"

Route137_Text_BennoDefeat:
	.string "You've come a long way indeed.$"

Route137_Text_BennoPostBattle:
	.string "Keep heading on. It opens out.$"

Route137_EventScript_Bertie::
	trainerbattle_single TRAINER_BERTIE, Route137_Text_BertieIntro, Route137_Text_BertieDefeat
	msgbox Route137_Text_BertiePostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_BertieIntro:
	.string "I swam here from the last shore.\pWorth it, if you'll battle.$"

Route137_Text_BertieDefeat:
	.string "You swim better than you look.$"

Route137_Text_BertiePostBattle:
	.string "Follow the shallows and you'll be\nfine.$"

Route137_EventScript_Carlotta::
	trainerbattle_single TRAINER_CARLOTTA, Route137_Text_CarlottaIntro, Route137_Text_CarlottaDefeat
	msgbox Route137_Text_CarlottaPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_CarlottaIntro:
	.string "I've been waiting for someone like\nyou.$"

Route137_Text_CarlottaDefeat:
	.string "Beaten.$"

Route137_Text_CarlottaPostBattle:
	.string "Rest before the next stretch.$"

Route137_EventScript_Carmen::
	trainerbattle_single TRAINER_CARMEN, Route137_Text_CarmenIntro, Route137_Text_CarmenDefeat
	msgbox Route137_Text_CarmenPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_CarmenIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route137_Text_CarmenDefeat:
	.string "Well fought.$"

Route137_Text_CarmenPostBattle:
	.string "Good luck out there.$"

Route137_EventScript_Clemmie::
	trainerbattle_single TRAINER_CLEMMIE, Route137_Text_ClemmieIntro, Route137_Text_ClemmieDefeat
	msgbox Route137_Text_ClemmiePostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_ClemmieIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route137_Text_ClemmieDefeat:
	.string "I underestimated you.$"

Route137_Text_ClemmiePostBattle:
	.string "I'll be training when you come\nback.$"

Route137_EventScript_Bramwell::
	trainerbattle_single TRAINER_BRAMWELL, Route137_Text_BramwellIntro, Route137_Text_BramwellDefeat
	msgbox Route137_Text_BramwellPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_BramwellIntro:
	.string "Wave to me and I'll take it as a\nchallenge!$"

Route137_Text_BramwellDefeat:
	.string "Washed up, that's me.$"

Route137_Text_BramwellPostBattle:
	.string "Mind the tide.$"

Route137_EventScript_Boris::
	trainerbattle_single TRAINER_BORIS, Route137_Text_BorisIntro, Route137_Text_BorisDefeat
	msgbox Route137_Text_BorisPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_BorisIntro:
	.string "Not many come this far. Battle me.$"

Route137_Text_BorisDefeat:
	.string "You've come a long way indeed.$"

Route137_Text_BorisPostBattle:
	.string "Keep heading on. It opens out.$"

Route137_EventScript_Cleo::
	trainerbattle_single TRAINER_CLEO, Route137_Text_CleoIntro, Route137_Text_CleoDefeat
	msgbox Route137_Text_CleoPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_CleoIntro:
	.string "A challenger! At last.$"

Route137_Text_CleoDefeat:
	.string "The ROUTE is yours.$"

Route137_Text_CleoPostBattle:
	.string "There's more of us further along.$"

Route137_EventScript_Bruno::
	trainerbattle_single TRAINER_BRUNO, Route137_Text_BrunoIntro, Route137_Text_BrunoDefeat
	msgbox Route137_Text_BrunoPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_BrunoIntro:
	.string "I've been waiting for someone like\nyou.$"

Route137_Text_BrunoDefeat:
	.string "Beaten.$"

Route137_Text_BrunoPostBattle:
	.string "Rest before the next stretch.$"

Route137_EventScript_Coral::
	trainerbattle_single TRAINER_CORAL, Route137_Text_CoralIntro, Route137_Text_CoralDefeat
	msgbox Route137_Text_CoralPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_CoralIntro:
	.string "You walked. I swam. Let's settle\nit.$"

Route137_Text_CoralDefeat:
	.string "The current's yours.$"

Route137_Text_CoralPostBattle:
	.string "There's a beach north of here. Rest\nthere.$"

Route137_EventScript_Bryce::
	trainerbattle_single TRAINER_BRYCE, Route137_Text_BryceIntro, Route137_Text_BryceDefeat
	msgbox Route137_Text_BrycePostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_BryceIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route137_Text_BryceDefeat:
	.string "I underestimated you.$"

Route137_Text_BrycePostBattle:
	.string "I'll be training when you come\nback.$"

Route137_EventScript_Dahlia::
	trainerbattle_single TRAINER_DAHLIA, Route137_Text_DahliaIntro, Route137_Text_DahliaDefeat
	msgbox Route137_Text_DahliaPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_DahliaIntro:
	.string "Battle me and I'll let you pass.$"

Route137_Text_DahliaDefeat:
	.string "That settles it.$"

Route137_Text_DahliaPostBattle:
	.string "Safe travels.$"

Route137_EventScript_Cairo::
	trainerbattle_single TRAINER_CAIRO, Route137_Text_CairoIntro, Route137_Text_CairoDefeat
	msgbox Route137_Text_CairoPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_CairoIntro:
	.string "Not many come this far. Battle me.$"

Route137_Text_CairoDefeat:
	.string "You've come a long way indeed.$"

Route137_Text_CairoPostBattle:
	.string "Keep heading on. It opens out.$"

Route137_EventScript_Delia::
	trainerbattle_single TRAINER_DELIA, Route137_Text_DeliaIntro, Route137_Text_DeliaDefeat
	msgbox Route137_Text_DeliaPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_DeliaIntro:
	.string "A challenger! At last.$"

Route137_Text_DeliaDefeat:
	.string "The ROUTE is yours.$"

Route137_Text_DeliaPostBattle:
	.string "There's more of us further along.$"

Route137_EventScript_Casper::
	trainerbattle_single TRAINER_CASPER, Route137_Text_CasperIntro, Route137_Text_CasperDefeat
	msgbox Route137_Text_CasperPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_CasperIntro:
	.string "The fish can wait. You can't.$"

Route137_Text_CasperDefeat:
	.string "Should've stuck to the water.$"

Route137_Text_CasperPostBattle:
	.string "They bite better at dusk out here.$"

Route137_EventScript_Dora::
	trainerbattle_single TRAINER_DORA, Route137_Text_DoraIntro, Route137_Text_DoraDefeat
	msgbox Route137_Text_DoraPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_DoraIntro:
	.string "You walked. I swam. Let's settle\nit.$"

Route137_Text_DoraDefeat:
	.string "The current's yours.$"

Route137_Text_DoraPostBattle:
	.string "There's a beach north of here. Rest\nthere.$"

Route137_EventScript_Casimir::
	trainerbattle_single TRAINER_CASIMIR, Route137_Text_CasimirIntro, Route137_Text_CasimirDefeat
	msgbox Route137_Text_CasimirPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_CasimirIntro:
	.string "I hook things that fight back.\pLike you.$"

Route137_Text_CasimirDefeat:
	.string "Slipped right through.$"

Route137_Text_CasimirPostBattle:
	.string "I'll be here till the light goes.$"

Route137_EventScript_Crispin::
	trainerbattle_single TRAINER_CRISPIN, Route137_Text_CrispinIntro, Route137_Text_CrispinDefeat
	msgbox Route137_Text_CrispinPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_CrispinIntro:
	.string "Cast off! Let's battle.$"

Route137_Text_CrispinDefeat:
	.string "Hah! Hooked myself.$"

Route137_Text_CrispinPostBattle:
	.string "Tight lines, TRAINER.$"

