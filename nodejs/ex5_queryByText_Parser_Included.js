const Speaker=require('speaker');
const pcmplay=new Speaker({
	channels:1,
	bitDepth:16,
	sampleRate:16000
});

const aikit=require('./aimakerskitutil');
const client_id='';
const client_key='';
const client_secret='';
const json_path='';
const cert_path='../data/ca-bundle.pem';
const proto_path='../data/gigagenieRPC.proto';
response_answer='';

// ###User DSS Information ###
let dss_info = {
	querytext: '',
	app_id: '',
	intent_name: '',
	intent_answer: '',
	app_info: ''
};


function JSON_Parser(msg){
	dss_info.querytext = msg.uword;
	user_info = msg.action;
	tmp_info = JSON.stringify(user_info[0].serviceId);
	
	tmp_info = tmp_info.replace('"<![CDATA[', '');
	tmp_info = tmp_info.replace(']]>"', '');
	tmp_info =tmp_info.replace(/\\/g,'');
	
	var kit_info_json = JSON.parse(tmp_info);
	dss_info.app_id = kit_info_json.VServiceID;
	dss_info.intent_name = kit_info_json.Intent;
	dss_info.intent_answer = kit_info_json.SystemMsg;
	dss_info.app_info = JSON.stringify(kit_info_json.appinfo);
	
	//Print Out User DSS INFO
	console.log("Query Text : " + dss_info.querytext);
	console.log('App ID: ' + dss_info.app_id);
	console.log('Intent Name: ' + dss_info.intent_name);
	console.log('Intent에 대한 답변: ' + dss_info.intent_answer);
	console.log('App 기본정보: ' + dss_info.app_info);
	
};

//aikit.initialize(client_id,client_key,client_secret,cert_path,proto_path);
aikit.initializeJson(json_path,cert_path,proto_path);
aikit.queryByText({queryText:'라면 먹는다',userSession:'12345',deviceId:'helloDevie'},(err,msg)=>{
	if(err){
		console.log(JSON.stringify(err));
	} else {
		//console.log('Msg:'+JSON.stringify(msg));
		JSON_Parser(msg);
	}
})

