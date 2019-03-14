const gpio=require('rpi-gpio');
const record=require('node-record-lpcm16');
const aikit=require('./aimakerskitutil');

//PCM 사운드 출력을 위한 모듈 설정
const Speaker=require('speaker');
const fs=require('fs');
//Sample Sound 데이터 로드
const soundBuffer=fs.readFileSync('../data/sample_sound.wav');
const pcmplay=new Speaker({
	channels:1,
	bitDepth:16,
	sampleRate:16000
});

//GPIO 설정
gpio.setup(29,gpio.DIR_IN,gpio.EDGE_BOTH);//버튼 핀은 입력으로
gpio.setup(31,gpio.DIR_LOW,write);//LED 는 출력으로 설정
//GPIO Output에 대한 오류를 전달하는 콜백
function write(err){
	if(err) console.log('write Error:'+err);
};

const client_id='';
const client_key='';
const client_secret='';
const json_path='';
const proto_path='../data/gigagenieRPC.proto';

let pcm=null;
function initMic(){
        return record.start({
                sampleRateHertz: 16000,
                threshold: 0,
                verbose: false,
                recordProgram: 'arecord',
        })
};

aikit.initializeJson(json_path,proto_path);

let sysStat=0;//0:버튼이 눌려지고 서비스를 제공할 준비가 되어 있음, 1: 서비스를 제공중임

//GPIO에서 변화를 Detect 함
gpio.on('change',(channel,value)=>{
	//29번 핀에 변화가 있는 경우
	if(channel===29){
		console.log('Channel:'+channel+' value is '+value);
		//버튼이 눌려졌을 경우
		if(value===false){
			//서비스를 제공할 준비가 되어 있으면
			if(sysStat===0) {
				sysStat=1;
				console.log('Button Pressed. Start Service');
				//LED를 켜고
				gpio.write(31,true);
				//샘플 사운드를 출력하고
				pcmplay.write(soundBuffer);
				//1초후 queryVoice를 시작함
				setTimeout(startQueryVoice,1000);
			} 
		}
	}
});

function startQueryVoice(){
	let ktstt=aikit.queryByVoice((err,msg)=>{
		if(err){
			console.log(JSON.stringify(err));
			record.stop();
		} else {
			console.log('Msg:'+JSON.stringify(msg));
			const action=msg.action[0];
			if(action){
				const actType=action.actType;
				const mesg=action.mesg;
				console.log('actType:'+actType+' mesg:'+mesg);
				//actType에 따라 전문 영역 대화 구별
				if(actType==='99' || actType==='601' || actType==='631' || actType==='607' || actType==='608' || actType==='606'){
					//전문 영역 대화인 경우 TTS 플래이
					let kttts=aikit.getText2VoiceStream({text:mesg,lang:0,mode:0});
					kttts.on('error',(error)=>{
						console.log('Error:'+error);
					});
					kttts.on('data',(data)=>{
						if(data.streamingResponse==='resOptions' && data.resOptions.resultCd===200) console.log('Stream send. format:'+data.resOptions.format);
						if(data.streamingResponse==='audioContent') {
							pcmplay.write(data.audioContent);
						} else console.log('msg received:'+JSON.stringify(data));
					});
					kttts.on('end',()=>{
						console.log('pcm end');
						record.stop();
					});
				} else record.stop();
			} else record.stop();

			gpio.write(31,false);
			sysStat=0;
		}
	});
	ktstt.write({reqOptions:{lang:0,userSession:'12345',deviceId:'D06190914TP808IQKtzq'}});
	//마이크 입력을 처리함
	let mic=initMic();
	mic.on('data',(data)=>{
    		ktstt.write({audioContent:data});
	});
};
