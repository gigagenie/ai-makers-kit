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
const proto_path='../data/gigagenieRPC.proto';

//aikit.initialize(client_id,client_key,client_secret,proto_path);
aikit.initializeJson(json_path,proto_path);
kttts=aikit.getText2VoiceStream({text:'안녕하세요. 반갑습니다.',lang:0,mode:0});
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
});
function finish(){
	console.log('tts played');
};
setTimeout(finish,5000);
