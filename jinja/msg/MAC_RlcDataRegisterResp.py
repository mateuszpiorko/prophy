import aprot

class MAC_RlcDataRegisterResp(aprot.struct):
	__metaclass__ = aprot.struct_generator
	_descriptor = [('messageResult',SMessageResult),('ueId',TUeId)]
	
	