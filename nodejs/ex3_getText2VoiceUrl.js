const aikit=require('./aimakerskitutil');
const client_id='';
const client_key='';
const client_secret='';
const json_path='';
const proto_path='../data/gigagenieRPC.proto';

//aikit.initialize(client_id,client_key,client_secret,proto_path);
aikit.initializeJson(json_path,proto_path);
aikit.getText2VoiceUrl({lang:0,text:'안녕하세요. 만나서 반갑습니다.'},(err,msg)=>{
	console.log('err:'+JSON.stringify(err)+' msg:'+JSON.stringify(msg));
})
