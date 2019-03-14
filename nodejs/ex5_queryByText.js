const aikit=require('./aimakerskitutil');
const client_id='';
const client_key='';
const client_secret='';
const json_path='';
const proto_path='../data/gigagenieRPC.proto';

//aikit.initialize(client_id,client_key,client_secret,proto_path);
aikit.initializeJson(json_path,proto_path);
aikit.queryByText({queryText:'안녕',userSession:'12345',deviceId:'helloDevie'},(err,msg)=>{
	if(err){
		console.log(JSON.stringify(err));
	} else {
		console.log('Msg:'+JSON.stringify(msg));
	}
})
