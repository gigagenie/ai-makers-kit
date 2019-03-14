/*
##### KT AI MAKERS KIT - 예제5) 대화 서비스 활용 #####

본 예제는 https://apilink.kt.co.kr/ 사이트에서 제공하는 Dialog KIT과 연동하게 됩니다.
https://apilink.kt.co.kr/console/gigagenie/resources/reqSvc 해당 주소에서
3rd Party Device List 중 AI MAKERS KIT(Dev) 버전을 신청합니다.
서비스 신청을 완료하면, My Service 메뉴를 클릭하여, [DSS 바로가기]라는 버튼을 클릭합니다.
해당 버튼을 클릭하게 되면, Dialog Kit 페이지가 열리고 해당 페이지에서 어휘사전과 질의할 Intent를 등록할 수 있습니다.

Dialog Kit 작업 수행 예시
--------------------------------------------------------
1) 어휘사전 등록
어휘 사전명
NE-BREAD - 대표단어: 식빵
PR-EAT - 대표단어: 먹는다
--------------------------------------------------------
2) 인텐트 관리
(해당 목록에서 방금 등록한 어휘사전의 NE, PR을 조합하여 INTENT를 등록한다.
이 때 분석결과에 대한 아이콘을 클릭하여 반드시 규칙을 생성하여야 한다.)
아래 문장을 BREAD라는 INTENT명으로 등록하였다.
식빵 먹는다 ([NE-BREAD/식빵] [PR-EAT/먹는다]
--------------------------------------------------------
3) 인텐트 답변 관리
BREAD 인텐트명에 대한 답변을 등록할 수 있다.
BREAD(인텐트명) : 정말 맛있겠군요.(INTENT명에 대한 답변)
--------------------------------------------------------

본 예제는 Dialog Kit을 통해 등록된 Intent 구문을 텍스트 형태로 질의(Query)하여 
이에 대한 답변을 출력하는 예제입니다.
아래 정의된 dss_info 객체를 이용하여 대화서버에 query한 intent에 대한 사용자 정보를 저장할 수 있습니다.

*/



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
response_answer='';


/*
	###User DSS Information ###
	 Dialog KIT에서 Intent를 통해 불러온 정보를 저장하는 객체
*/
let dss_info = {
	querytext: '',
	app_id: '',
	intent_name: '',
	intent_answer: '',
	app_info: ''
};



/*
	### 대화서버에서 받아온 정보를 Parsing하는 함수 ###
	본 함수는 대화서버에 Query한 Intent에 대한 정보를 파싱하여 dss_info 객체에 저장하는 함수이다.
	
*/
function JSON_Parser(msg){
	dss_info.querytext = msg.uword;
	user_info = msg.action;
	tmp_info = JSON.stringify(user_info[0].serviceId);
	
	tmp_info = tmp_info.replace('"<![CDATA[', '');
	tmp_info = tmp_info.replace(']]>"', '');
	tmp_info =tmp_info.replace(/\\/g,'');

	// 파싱한 Dialog Kit 사용자 정보를 dss_info 객체에 저장함
	var kit_info_json = JSON.parse(tmp_info);
	dss_info.app_id = kit_info_json.VServiceID;
	dss_info.intent_name = kit_info_json.Intent;
	dss_info.intent_answer = kit_info_json.SystemMsg;
	dss_info.app_info = JSON.stringify(kit_info_json.appinfo);
	
	//Print Out User DSS INFO(인텐트에 대한 정보를 터미널로 출력함)
	console.log("Query Text : " + dss_info.querytext);
	console.log('App ID: ' + dss_info.app_id);
	console.log('Intent Name: ' + dss_info.intent_name);
	console.log('Intent에 대한 답변: ' + dss_info.intent_answer);
	console.log('App 기본정보: ' + dss_info.app_info);
	
};

//aikit.initialize(client_id,client_key,client_secret,proto_path);
aikit.initializeJson(json_path,proto_path);

// 대화서버로 Intent를 보냄 (본 코드에서는 '라면 먹는다'라는 인텐트를 대화서버로 보냄)
aikit.queryByText({queryText:'라면 먹는다',userSession:'12345',deviceId:'helloDevie'},(err,msg)=>{
	if(err){
		console.log(JSON.stringify(err));
	} else {
		//console.log('Msg:'+JSON.stringify(msg));
		JSON_Parser(msg); //해당되는 정보를 출력함
	}
})

