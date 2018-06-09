const record=require('node-record-lpcm16');
const mplayer=require('mplayer');
const aikit=require('./aimakerskitutil');
const ktkws=require('./ktkws');
const player=new mplayer();

const client_id='';
const client_key='';
const client_secret='';
const json_path='';
const cert_path='../data/ca-bundle.pem';
const proto_path='../data/gigagenieRPC.proto';

const kwstext=['기가지니','지니야','친구야','자기야'];
const kwsflag=parseInt(process.argv[2]);
let pcm=null;
function initMic(){
        return record.start({
                sampleRateHertz: 16000,
                threshold: 0,
                verbose: false,
                recordProgram: 'arecord',
        })
};
ktkws.initialize('../data/kwsmodel.pack');
ktkws.startKws(kwsflag);
let mic=initMic();

//aikit.initialize(client_id,client_key,client_secret,cert_path,proto_path);
aikit.initializeJson(json_path,cert_path,proto_path);

let mode=0;//0:kws, 1:stt
let ktstt=null;
mic.on('data',(data)=>{
	if(mode===0){
		result=ktkws.pushBuffer(data);
		if(result===1) {
			console.log("KWS Detected");
			player.openFile('../data/sample_sound.wav');
			setTimeout(startStt,1000);
			startStt();
		}
	} else {
    		ktstt.write({audioContent:data});
	}
});
console.log('say :'+kwstext[kwsflag]);
function startStt(){
	ktstt=aikit.getVoice2Text();
	ktstt.on('error',(error)=>{
	    console.log('Error:'+error);
	});
	ktstt.on('data',(data)=>{
		console.log('stt result:'+JSON.stringify(data));
		if(data.resultCd!==200) mode=0;
	});
	ktstt.on('end',()=>{
		console.log('stt text stream end');
		mode=0;
	});
	ktstt.write({reqOptions:{mode:0,lang:0}});
	mode=1;
};
