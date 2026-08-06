	object_const_def
	const_export ROUTE26_RARE_CANDY
	const_export ROUTE26_CARBOS

Route26_Object:
	db $f ; border block

	def_warp_events

	def_bg_events

	def_object_events
	object_event 16, 12, SPRITE_POKE_BALL, STAY, NONE, TEXT_ROUTE26_RARE_CANDY, RARE_CANDY
	object_event 16, 66, SPRITE_POKE_BALL, STAY, NONE, TEXT_ROUTE26_CARBOS, CARBOS

	def_warps_to ROUTE_26
