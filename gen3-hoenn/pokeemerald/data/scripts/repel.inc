EventScript_RepelWoreOff::
	specialvar VAR_RESULT, CanUseAnotherRepel
	compare VAR_RESULT, FALSE
	goto_if_eq EventScript_RepelNoMoreLeft
	msgbox Text_RepelWoreOffUseAnother, MSGBOX_YESNO
	compare VAR_RESULT, NO
	goto_if_eq EventScript_RepelDone
	special UseAnotherRepel
	playse SE_REPEL
	waitse
	msgbox Text_UsedAnotherRepel, MSGBOX_SIGN
	end

EventScript_RepelNoMoreLeft::
	msgbox Text_RepelWoreOff, MSGBOX_SIGN
EventScript_RepelDone::
	end

Text_RepelWoreOff:
	.string "REPEL's effect wore off…$"

Text_RepelWoreOffUseAnother:
	.string "REPEL's effect wore off…\p"
	.string "Use another {STR_VAR_1}?$"

Text_UsedAnotherRepel:
	.string "{PLAYER} used the\n{STR_VAR_1}.$"
