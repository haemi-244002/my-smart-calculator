# ==========================================
# 1. 데이터 불러오기 및 구조 확인
# ==========================================
from sklearn import datasets
import matplotlib.pyplot as plt

# 사이킷런에 내장된 손글씨 데이터셋 불러오기 (총 1797개)
digits = datasets.load_digits()

# digits 데이터의 3가지 핵심 요소
# - digits.images: 8x8 2차원 배열 (눈으로 보는 이미지 형태)
# - digits.data: 64개(8x8)짜리 1차원 배열 (컴퓨터가 학습하기 좋게 한 줄로 편 형태)
# - digits.target: 실제 정답 (예: 이 이미지는 '3'이다)

# ==========================================
# 2. 분류기 학습 (Support Vector Machine)
# ==========================================
from sklearn import svm

# SVM 분류기 모델 생성 (gamma는 학습의 정교함을 조절하는 옵션)
clf = svm.SVC(gamma=0.001, probability=True)

# 모델 학습시키기 (fit): 처음 1700개의 데이터와 정답을 던져주고 공부시킴
clf.fit(digits.data[:1700], digits.target[:1700])

# ==========================================
# 3. 모델 테스트 및 예측
# ==========================================
# 공부에 쓰지 않은 나머지 97개의 데이터(1700번 이후)로 시험을 봄
expected = digits.target[1700:] # 실제 정답지
predicted = clf.predict(digits.data[1700:]) # 컴퓨터가 예측한 답안지

# ==========================================
# 4. 결과 분석 (성능 지표 및 오답 노트)
# ==========================================
from sklearn import metrics

# 정밀도, 재현율 등 종합 성적표 출력
print(metrics.classification_report(expected, predicted))

# 혼동 행렬 출력 (대각선에 숫자가 몰려있어야 다 맞춘 것!)
print(metrics.confusion_matrix(expected, predicted))

# 틀린 문제만 모아서 오답 노트 출력하기 (시각화)
plt.rcParams["figure.figsize"] = [1.6, 1.2]
for index, (expect, predict) in enumerate(zip(expected, predicted)):
    if expect != predict: # 정답과 예측값이 다르면(틀렸으면)
        print(f"Image {index+1700}: 정답 {expect}, 모델 예측 {predict}")
        
        # 틀린 이미지를 화면에 그려서 사람이 직접 눈으로 확인해봄
        plt.imshow(digits.images[index+1700], cmap=plt.cm.gray)
        plt.show()
