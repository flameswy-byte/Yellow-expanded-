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

Route137_EventScript_Avery::
	trainerbattle_single TRAINER_AVERY, Route137_Text_AveryIntro, Route137_Text_AveryDefeat
	msgbox Route137_Text_AveryPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_AveryIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route137_Text_AveryDefeat:
	.string "Well fought.$"

Route137_Text_AveryPostBattle:
	.string "Good luck out there.$"

Route137_EventScript_Barney::
	trainerbattle_single TRAINER_BARNEY, Route137_Text_BarneyIntro, Route137_Text_BarneyDefeat
	msgbox Route137_Text_BarneyPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_BarneyIntro:
	.string "Cold? You get used to it.$"

Route137_Text_BarneyDefeat:
	.string "I'll float here a while.$"

Route137_Text_BarneyPostBattle:
	.string "I'll race you next time.$"

Route137_EventScript_Carlotta::
	trainerbattle_single TRAINER_CARLOTTA, Route137_Text_CarlottaIntro, Route137_Text_CarlottaDefeat
	msgbox Route137_Text_CarlottaPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_CarlottaIntro:
	.string "Battle me and I'll let you pass.$"

Route137_Text_CarlottaDefeat:
	.string "That settles it.$"

Route137_Text_CarlottaPostBattle:
	.string "Safe travels.$"

Route137_EventScript_Carmen::
	trainerbattle_single TRAINER_CARMEN, Route137_Text_CarmenIntro, Route137_Text_CarmenDefeat
	msgbox Route137_Text_CarmenPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_CarmenIntro:
	.string "Not many come this far. Battle me.$"

Route137_Text_CarmenDefeat:
	.string "You've come a long way indeed.$"

Route137_Text_CarmenPostBattle:
	.string "Keep heading on. It opens out.$"

Route137_EventScript_Basil::
	trainerbattle_single TRAINER_BASIL, Route137_Text_BasilIntro, Route137_Text_BasilDefeat
	msgbox Route137_Text_BasilPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_BasilIntro:
	.string "I swam here from the last shore.\pWorth it, if you'll battle.$"

Route137_Text_BasilDefeat:
	.string "You swim better than you look.$"

Route137_Text_BasilPostBattle:
	.string "Follow the shallows and you'll be\nfine.$"

Route137_EventScript_Benno::
	trainerbattle_single TRAINER_BENNO, Route137_Text_BennoIntro, Route137_Text_BennoDefeat
	msgbox Route137_Text_BennoPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_BennoIntro:
	.string "e$"

Route137_Text_BennoDefeat:
	.string "I$"

Route137_Text_BennoPostBattle:
	.string "u$"

Route137_EventScript_Clemmie::
	trainerbattle_single TRAINER_CLEMMIE, Route137_Text_ClemmieIntro, Route137_Text_ClemmieDefeat
	msgbox Route137_Text_ClemmiePostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_ClemmieIntro:
	.string "Stop there. This ROUTE is mine to\ndefend.$"

Route137_Text_ClemmieDefeat:
	.string "Well fought.$"

Route137_Text_ClemmiePostBattle:
	.string "Good luck out there.$"

Route137_EventScript_Bertie::
	trainerbattle_single TRAINER_BERTIE, Route137_Text_BertieIntro, Route137_Text_BertieDefeat
	msgbox Route137_Text_BertiePostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_BertieIntro:
	.string "You've come a long way. Let's see\nwhy.$"

Route137_Text_BertieDefeat:
	.string "I underestimated you.$"

Route137_Text_BertiePostBattle:
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

Route137_EventScript_Cleo::
	trainerbattle_single TRAINER_CLEO, Route137_Text_CleoIntro, Route137_Text_CleoDefeat
	msgbox Route137_Text_CleoPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_CleoIntro:
	.string "Not many come this far. Battle me.$"

Route137_Text_CleoDefeat:
	.string "You've come a long way indeed.$"

Route137_Text_CleoPostBattle:
	.string "Keep heading on. It opens out.$"

Route137_EventScript_Boris::
	trainerbattle_single TRAINER_BORIS, Route137_Text_BorisIntro, Route137_Text_BorisDefeat
	msgbox Route137_Text_BorisPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_BorisIntro:
	.string "A challenger! At last.$"

Route137_Text_BorisDefeat:
	.string "The ROUTE is yours.$"

Route137_Text_BorisPostBattle:
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
	.string "You'll scare them. Battle me for\nit.$"

Route137_Text_BryceDefeat:
	.string "Beaten fair.$"

Route137_Text_BrycePostBattle:
	.string "I'll be training when you come\nback.$"

Route137_EventScript_Cairo::
	trainerbattle_single TRAINER_CAIRO, Route137_Text_CairoIntro, Route137_Text_CairoDefeat
	msgbox Route137_Text_CairoPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_CairoIntro:
	.string "Cast off! Let's battle.$"

Route137_Text_CairoDefeat:
	.string "Hah! Hooked myself.$"

Route137_Text_CairoPostBattle:
	.string "Tight lines, TRAINER.$"

Route137_EventScript_Casper::
	trainerbattle_single TRAINER_CASPER, Route137_Text_CasperIntro, Route137_Text_CasperDefeat
	msgbox Route137_Text_CasperPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_CasperIntro:
	.string "Quiet! ...Ah, you've scared them\noff.\pYou owe me a battle.$"

Route137_Text_CasperDefeat:
	.string "Reeled in and thrown back.$"

Route137_Text_CasperPostBattle:
	.string "Best water's round the bend. Try\nit.$"

Route137_EventScript_Casimir::
	trainerbattle_single TRAINER_CASIMIR, Route137_Text_CasimirIntro, Route137_Text_CasimirDefeat
	msgbox Route137_Text_CasimirPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_CasimirIntro:
	.string "Been here since dawn. Nothing\nbiting.\pYou'll do.$"

Route137_Text_CasimirDefeat:
	.string "You're the one that got away.$"

Route137_Text_CasimirPostBattle:
	.string "Bring a ROD next time and I'll show\nyou a spot.$"

Route137_EventScript_Crispin::
	trainerbattle_single TRAINER_CRISPIN, Route137_Text_CrispinIntro, Route137_Text_CrispinDefeat
	msgbox Route137_Text_CrispinPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_CrispinIntro:
	.string "The fish can wait. You can't.$"

Route137_Text_CrispinDefeat:
	.string "Should've stuck to the water.$"

Route137_Text_CrispinPostBattle:
	.string "They bite better at dusk out here.$"

Route137_EventScript_Dahlia::
	trainerbattle_single TRAINER_DAHLIA, Route137_Text_DahliaIntro, Route137_Text_DahliaDefeat
	msgbox Route137_Text_DahliaPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_DahliaIntro:
	.string "You walked. I swam. Let's settle\nit.$"

Route137_Text_DahliaDefeat:
	.string "The current's yours.$"

Route137_Text_DahliaPostBattle:
	.string "There's a beach north of here. Rest\nthere.$"

Route137_EventScript_Clive::
	trainerbattle_single TRAINER_CLIVE, Route137_Text_CliveIntro, Route137_Text_CliveDefeat
	msgbox Route137_Text_ClivePostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_CliveIntro:
	.string "I hook things that fight back.\pLike you.$"

Route137_Text_CliveDefeat:
	.string "Slipped right through.$"

Route137_Text_ClivePostBattle:
	.string "I'll be here till the light goes.$"

Route137_EventScript_Conrad::
	trainerbattle_single TRAINER_CONRAD, Route137_Text_ConradIntro, Route137_Text_ConradDefeat
	msgbox Route137_Text_ConradPostBattle, MSGBOX_AUTOCLOSE
	end

Route137_Text_ConradIntro:
	.string "Fly at me, then.$"

Route137_Text_ConradDefeat:
	.string "Back to the nest.$"

Route137_Text_ConradPostBattle:
	.string "Safe travels.$"

