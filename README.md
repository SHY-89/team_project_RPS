# team_project_RPS
## 1조 퍼스트 코딩

## 가위 바위 보 게임 웹 버전

	단순히 휘발성으로 가위,바위,보 게임을 하는게 아닌 예전의 기록도 노출 할 수 있는 웹을 제작
 	웹으로 하는 거라 불특정 다수가 게임을 진행 할 수 있기에 각 유저별로 게임을 기록 할 수있도록 회원가입과 로그인을 구현
  	신규 사용자의 경우 회원가입 과 로그인 후 게임을 진행 하여 본인 만의 가위,바위,보 게임을 진행 하며 기존 사용자의 경우 본인의 전적이
   	별로 마음에 들지 않을 경우 새로 가입하여 언제든지 새로운 게임을 진행 할 수 있다

	랭킹 시스템을 도입하여 유저간의 순위를 확인 할 수 있게 하여 게임의 재미를 추가!!
     
## 개발 일정

	07.04 ~ 07.09
 
## 요구사항

	-회원 가입 페이지
 		회원 정보를 입력하여 회원 가입
		-회원 정보
			이름
			아이디
			비밀번호

	-로그인 페이지
		회원 가입한 이메일 과 비밀번호를 입력

	-게임 페이지
		플레이어가 가위, 바위, 보 중 하나를 선택
		컴퓨터도 무작위로 가위, 바위, 보 중 하나를 선택
		플레이어와 컴퓨터의 선택을 비교하여 승패를 판정
		결과를 출력하여 플레이어가 이겼는지, 컴퓨터가 이겼는지, 비겼는지를 노출

	-전적
		게임의 승,무,패를 리스트 형식으로 노출
		최대 노출 수만큼 노출 후 페이징
		회원 수정
		비밀번호만 수정 가능
		변경시 로그인 변경전 비밀번호 입력 필요
	
	-데이터베이스
 		SqlLite
		회원정보(Users)
			idx		Int		primarykey
			user_id		String		유저 아이디
			user_name	String		유저 이름
			user_pw		String		유저 패스워드
			join_date	DateTime	가입일자
   
		게임기록(GameLog)
			idx		Int		primarykey
			user_id		String		유저 아이디
			player		String		유저가 선택한 가위,바위,보
			computer	String		컴퓨터가 선택한 가위,바위,보
			result		String		가위,바위,보 결과
			w_date		DateTime	게임 일자
   
   	- 랭킹
    		유저별로 가장 높은 승률을 가진 유저 10 순위까지 지정하여 노출

## 개발환경 & 사용기술

	Python 				3.8.6
	flask				3.0.3
	jquery 				1.11.1
	sweetalert 			2.1.2
	Flask-Cors         		4.0.1
	Flask-SQLAlchemy		3.1.1
	Flask-WTF			1.2.1
 	WTForms				3.1.2
	random

## 개발사항

	회원 가입 페이지 		서영환, 조민희 개발 
	로그인 페이지			서영환, 조민희 개발 
	게임&전적			김동민, 김한규, 서영환, 조민희 개발
 	랭킹 				서영환 개발


## API
|API 호출 주소|method type|parameter|return|설명|
|---|---|---|---|------|
|/user/create|POST|user_id,user_pw,user_name|{'reuslt': result}|result: 'fail' & 'sussece' 회원가입 요청하여 회원이 등록되면 sussece  등록이 실패되면 fail를 리턴|
|/check/user|GET|user_id|{'reuslt': result}|result: 'fail' & 'sussece' 회원 가입시 중복된 user_id를 확인 하여 중복 된 아이디가 있으면 fail를 중복된 아이디가 없으면 sussece를 리턴|
|/login|POST|user_id,user_pw||로그인에 성공하면 서버에서 해당 유저의 세션을 생성 후 게임화면으로 이동 아니라면 로그인 페이지 그대로 새로고침|
|/logout|GET|||로그인 세션 값을 파기 후 로그인 페이지로 이동|
|/game/winlose|GET|user_choise|{'computer': computer, 'result': reuslt, 'rank': rank_list}|유저가 선택한 user_choise(가위,바위,보)를 확인하여 컴퓨터가 선택한 computer(가위,바위,보)를 비교하여 그 결과 값을 데이터베이스에 저장 후 computer가 선택한 (가위,바위,보)와 결과값과 함께 랭킹 정보를 담은 rank를 리턴|
|/submit|POST|user_input|{'user_choice': user_choice, 'computer_choice': computer_choice, 'result': result, 'game_results': game_results }||유저가 선택한 user_input(1:가위,2:바위,3:보)와 컴퓨터가 선택한 computer_choice(가위,바위,보)를 비교하여 그 결과 값을 데이터베이스에 저장 후 유저가 선택한 user_choice(가위,바위,보) computer가 선택한 computer_choice(가위,바위,보)와 결과값과 해당 유저 최근 전적 10개를 담은 game_results 값을 리턴 |
|/game/kdm|POST|player_choice|{ "player_choice": player_choice, "computer_choice": computer_choice, "game_win_lose": game_win_lose, "win_count": win_count, "draw_count": draw_count, "lose_count": lose_count }|유저가 선택한 player_choice('가위', '바위', '보') 와 컴퓨터가 선택한 computer_choice(가위,바위,보)를 비교하여 그 결과 값 game_win_lose 을 데이터베이스에 저장 후 현재 유저가 선택한 값(player_choice)과 컴퓨터가 선택한값(computer_choice), 결과 값(game_win_lose), 유저 전체 승(win_count), 무(draw_count), 패(lose_count) 데이틀 리턴|
|/game/cmh|GET,POST|---|---|------|
