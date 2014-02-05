import aprot

class MAC_ErrorInd(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('lnCelId',TCellId),('crnti',TCrnti),('ueId',TUeId),('sRbList', aprot.bytes(size = MAX_NUM_SRB_PER_USER)),('dRbList', aprot.bytes(size = MAX_NUM_DRB_PER_USER))]
	
	