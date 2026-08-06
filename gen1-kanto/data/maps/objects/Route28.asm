	object_const_def
	const_export ROUTE28_POKE_BALL

Route28_Object:
	db $f ; border block

	def_warp_events

	def_bg_events

	def_object_events
	object_event 16, 6, SPRITE_POKE_BALL, STAY, NONE, TEXT_ROUTE28_POKE_BALL, POKE_BALL

	def_warps_to ROUTE_28
