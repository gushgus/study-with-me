import random


URGENT_PHRASES = [
	"지금은 D-day가 아니라 D-비상사태입니다.",
	"오늘 분량, 아직 안 끝났다면 오늘이 아니라 오늘밤이 고비입니다.",
	"이건 미루기용 과제가 아니라 즉시 처리용 과제예요.",
	"남은 시간이 적을수록 집중력은 더 맛있어집니다.",
	"D-day가 코앞이니, 손보다 먼저 마음부터 달리게 해봅시다.",
]

GOOD_PHRASES = [
	"오늘 분량 완료. 이제 당신은 오늘의 승리자입니다.",
	"할 일 끝! 과제도 당신도 잠깐 숨 돌릴 자격이 있습니다.",
	"오늘 목표 달성, 이 정도면 꽤 멋진 하루예요.",
	"분량을 채웠다면 남은 건 칭찬과 약간의 뿌듯함뿐입니다.",
	"오늘 몫을 해냈으니, 나머지는 내일의 당신에게 맡겨도 됩니다.",
]

NORMAL_PHRASES = [
	"천천히 가도 괜찮아요. 중요한 건 멈추지 않는 거니까요.",
	"지금은 평온한 진행 중, 이 리듬을 잘 지키면 됩니다.",
	"오늘은 과제와 적당히 친해지는 날입니다.",
	"무리하지 말고, 할 수 있는 만큼만 착실히 가봅시다.",
	"지금 속도면 충분히 괜찮습니다. 호흡만 유지하세요.",
]


def get_phrase(status: str) -> str:
	phrases_map = {
		"urgent": URGENT_PHRASES,
		"good": GOOD_PHRASES,
		"normal": NORMAL_PHRASES,
	}

	phrases = phrases_map.get(status, NORMAL_PHRASES)
	return random.choice(phrases)
