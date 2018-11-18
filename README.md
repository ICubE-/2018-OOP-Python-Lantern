# 2018-2 객체지향 프로그래밍 프로젝트 - **{Leftovers}**
구성원: 2-1 연제호 | 2-1 최호영 | 2-6 장영웅

## 1. 주제
온라인 정치 게임 : 상대평가 (와글와글 던전을 베이스로 한 2차 창작 게임)

## 2. 동기
 팀원 중 한 명이 젠가 게임을 주제로 자율연구를 진행중이다. 그 연구에서 도출된 물리학적 수식 및 결과를 이용하여 젠가 게임을 컴퓨터 시뮬레이션으로 구현할 수 있겠다는 생각이 들었다. 젠가 게임이 모두에게 친숙하면서도 무게중심과 마찰력과 같은 물리학적 내용을 전달할 수 있는 게임이라고 생각하였고, 이에 젠가 게임을 파이썬 프로그래밍을 통해 구현하고자 하였다. 

## 3. 프로그램 사용 대상
 단순히 게임의 기능만을 사용한다면 사용 대상은 컴퓨터가 있고 젠가 게임을 하고자 하는 모두일 것이다. 하지만, 본 프로젝트에서는 젠가의 물리적 특성 및 수식을 보여주는 기능을 더할 예정이므로 마찰력 및 무게중심의 개념을 쉽게 전달하고자 하는 물리 교사나 학생들을 대상으로 할 수 있다.

## 4. 목적
 기본 목적은 젠가 게임을 프로그래밍을 통해 구현하는 것이다. 젠가 게임은 나무로 만든 직육면체 형태의 블록이 쌓여 만들어진 기둥에서, 여러 명의 플레이어가 순서를 번갈아가면서 기둥을 넘어뜨리지 않게 블록을 하나씩 빼는 게임이다. 이 때 기둥이 넘어지는지 여부를 결정하는 것은 크게 기둥의 무게중심과, 각 블록에 작용하는 중력과 마찰력이다. 따라서 이러한 물리적 요소를 보여줄 수 있는 프로그램을 제작하는 것을 목적으로 한다.
  우선 본 프로그램의 기본 형태는 네트워킹을 이용하여 여러 명의 플레이어가 서버에 접속한 후 동시에 젠가 게임을 플레이하는 것이다. 이 때의 젠가 기둥의 형태는 시각적으로 드러난다. 여기에 추가적으로 젠가 기둥에 영향을 주는 물리적 요소(마찰력이나 무게중심)의 상태가 동시에 출력된다.

## 5. 주요기능
{보드게임 '젠가'를 컴퓨터에서 인터넷상으로 유저들끼리 플레이할 수 있도록 구현}

## 6. 프로젝트 핵심
{인터넷을 통해 유저들간 통신 구현, 젠가블록을 밀고 빼낼 수 있는 유저 인터페이스 구현, 젠가블록을 밀고 블록들이 무너지는 기준을 정하고 위험한 정도의 알고리즘의 구현}

## 7. 구현에 필요한 라이브러리나 기술
{pygame, threading, socket...}
네트워킹

## 8. **분업 계획**
연제호 : 
최호영 : 
장영웅 : 

## 9. 기타
<hr>

#### readme 작성관련 참고하기 [바로가기](https://heropy.blog/2017/09/30/markdown/)

#### 예시 계획서 [[예시 1]](https://docs.google.com/document/d/1hcuGhTtmiTUxuBtr3O6ffrSMahKNhEj33woE02V-84U/edit?usp=sharing) | [[예시 2]](https://docs.google.com/document/d/1FmxTZvmrroOW4uZ34Xfyyk9ejrQNx6gtsB6k7zOvHYE/edit?usp=sharing)
