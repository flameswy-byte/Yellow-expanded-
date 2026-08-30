FortreeCity_House2_MapScripts::
	.byte 0

FortreeCity_House2_EventScript_SwiftGiver::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_TM_SWIFT, FortreeCity_House2_EventScript_ExplainSwift
	call_if_unset FLAG_MET_TM_SWIFT_GIVER, FortreeCity_House2_EventScript_Greeting
	msgbox FortreeCity_House2_Text_CoinInWhichHand, MSGBOX_DEFAULT
	multichoice 21, 8, MULTI_RIGHTLEFT, TRUE
	switch VAR_RESULT
	case 1, FortreeCity_House2_EventScript_WrongGuess
	msgbox FortreeCity_House2_Text_CorrectTryAgainWhichHand, MSGBOX_DEFAULT
	multichoice 21, 8, MULTI_RIGHTLEFT, TRUE
	switch VAR_RESULT
	case 1, FortreeCity_House2_EventScript_WrongGuess
	msgbox FortreeCity_House2_Text_CorrectTryAgainWhichHand2, MSGBOX_DEFAULT
	multichoice 21, 8, MULTI_RIGHTLEFT, TRUE
	switch VAR_RESULT
	case 0, FortreeCity_House2_EventScript_WrongGuess
	msgbox FortreeCity_House2_Text_YourSixthSenseHasAwoken, MSGBOX_DEFAULT
	giveitem ITEM_TM_SWIFT
	goto_if_eq VAR_RESULT, 0, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_TM_SWIFT
	msgbox FortreeCity_House2_Text_ExplainSwift, MSGBOX_DEFAULT
	release
	end

FortreeCity_House2_EventScript_Greeting::
	msgbox FortreeCity_House2_Text_SensesArousedByNature, MSGBOX_DEFAULT
	setflag FLAG_MET_TM_SWIFT_GIVER
	return

FortreeCity_House2_EventScript_ExplainSwift::
	msgbox FortreeCity_House2_Text_ExplainSwift, MSGBOX_DEFAULT
	release
	end

FortreeCity_House2_EventScript_WrongGuess::
	msgbox FortreeCity_House2_Text_YouGuessedWrong, MSGBOX_DEFAULT
	release
	end

FortreeCity_House2_Text_SensesArousedByNature:
	.string "People… POKéMON…\p"
	.string "Their senses are sharpened by living\n"
	.string "in natural environments…$"

FortreeCity_House2_Text_CoinInWhichHand:
	.string "Let this old woman see if your sixth\n"
	.string "sense has awoken…\p"
	.string "I hold a coin in my hand.\p"
	.string "Now, tell me, have I palmed it in\n"
	.string "the right hand? Or in the left?$"

FortreeCity_House2_Text_CorrectTryAgainWhichHand:
	.string "Oh! Yes, correct!\p"
	.string "We shall try again.\p"
	.string "In which hand have I palmed the coin?\n"
	.string "The right or left?$"

FortreeCity_House2_Text_CorrectTryAgainWhichHand2:
	.string "Oh! Yes, correct!\p"
	.string "We shall try again.\p"
	.string "In which hand have I palmed the coin?\n"
	.string "The right or left?$"

FortreeCity_House2_Text_YourSixthSenseHasAwoken:
	.string "Oh! Splendid!\n"
	.string "Your sixth sense has awoken!\p"
	.string "Here. Take this, and let your POKéMON\n"
	.string "strike what the eye cannot follow.$"

FortreeCity_House2_Text_ExplainSwift:
	.string "SWIFT throws stars that always find\n"
	.string "their mark. Nothing dodges them.$"

FortreeCity_House2_Text_YouGuessedWrong:
	.string "No, too bad.\n"
	.string "You guessed wrong.$"

