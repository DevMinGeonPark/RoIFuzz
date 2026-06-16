# RoIFuzz — 보안 정책을 켠 상태에서 돌리는 ROS 2 IDL 퍼저

ROS 2 로봇 시스템을 테스트하는 퍼저입니다. 보통 퍼저와 다른 점은 SROS 2 보안 정책을 강제한
채로 메시지를 IDL 타입 단위로 변이시킨다는 것입니다. 커버리지를 피드백으로 받아 입력을 만듭니다.

발표: 정보보호학회 학술대회 구두발표,
"RoIFuzz: 강화된 로봇 보안 정책을 적용한 ROS IDL 퍼저 연구".
기반 연구는 RoboFuzz(FSE '22, https://dl.acm.org/doi/10.1145/3540250.3549164)입니다.

## 왜 했나

로보틱스 퍼저는 대개 보안이 꺼진 개방 환경에서 노드를 테스트합니다. 그런데 실제 배포 환경은
SROS 2로 돌아갑니다. DDS 단에서 인증, 암호화, 접근제어가 걸립니다. 그래서 질문이 생깁니다.
보안 정책이 걸린 상태에서도 로봇 프로그램이 여전히 제대로 동작할까요? RoIFuzz는 그 보안 계층을
켜둔 채 ROS IDL 인터페이스를 퍼징합니다.

## 하는 일

- ROS 2 IDL 타입을 빠짐없이 변이합니다. Bool·Byte·Char·Float32/64·Int8 같은 기본형부터
  Fixed/Bounded/Unbounded 배열까지 다룹니다 (watchlist/idltest.json, librcl_apis/).
- SROS 2 접근제어 정책(policies/sros2_node.policy.xml 등)을 적용한 채 타깃을 띄웁니다.
- 커버리지와 상태를 피드백으로 받아 캠페인을 끌고 갑니다 (coverage/, feedback.py).
- PX4(드론 오토파일럿)·TurtleBot·MoveIt 각각에 맞는 오라클(oracles/)로 크래시뿐 아니라
  동작이 틀어지는 의미적 버그까지 잡습니다.
- PX4 SITL 미션(이륙, 경유지 비행)을 PX4-ROS-MAVLink 브리지로 실제로 돌립니다.

## 구조

```
fuzzer.py     메인 루프. IDL 메시지를 변이해 발행하고 결과를 본다
mutator.py    IDL 타입별 변이
scheduler.py  캠페인과 시드 스케줄링
executor.py   ROS 2 / PX4 타깃 실행과 제어
feedback.py   커버리지와 상태 피드백
oracles/      px4.py, turtlebot.py, moveit.py
policies/     퍼징 중 강제하는 SROS 2 보안 정책
missions/     PX4 비행 시나리오
```

## 요구사항과 실행

ROS 2와 SROS 2, PX4(SITL), Python 3가 필요합니다. 의존성은 `pip install -r requirements.txt`로
설치합니다.

```bash
python fuzzer.py     # 타깃과 캠페인 설정은 config.py, constants.py 참고
```

RoboFuzz를 IDL 수준 변이와 SROS 2 정책 강제로 확장한 보안 연구 코드입니다.
