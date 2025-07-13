import streamlit as st
import re
import matplotlib.pyplot as plt

# 손실 함수
def sonsil(line, lis):
    result = 0
    for i in range(12):
        result += ((line[0]*(5+5*i) + line[1]- lis[i])**2) / 12
    return result


# 최적화 함수
def choijukhwa(lis, mval, yval, kval, a):
    if a==0:
        mplus=[mval+kval, yval]
        mminus=[mval-kval, yval]
        if sonsil(mplus, lis)>sonsil(mminus, lis):
            return mminus
        else:
            return mplus
    else:
        yplus=[mval, yval+kval]
        yminus=[mval, yval-kval]
        if sonsil(yplus, lis)>sonsil(yminus, lis):
            return yminus
        else:
            return yplus
        
# 그래프 출력 함수
def grap(lis, line):
    x = list(range(5, 65, 5))
    y = lis
    line_x = x
    line_y = [line[0] * xi + line[1] for xi in line_x]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(x, y, color='blue', label='data points')
    ax.plot(line_x, line_y, color='red', label=f'y = {line[0]:.2f}x + {line[1]:.2f}')
    ax.legend()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Data points & fitted line')
    ax.set_xlim(0, 70)
    ax.set_ylim(0, 160)
    
    ax.grid(True)
    st.pyplot(fig)


st.title('경사하강법을 통한 추세선 구하기')
st.divider()

# 학습률 입력
learn = st.slider('학습률', 0.0, 1.0, 0.01)

# 최적화 대상 선택
option = st.selectbox(
    label='최적화 대상',
    options=['기울기', 'y절편'],
    index=None,
    placeholder='최적화 대상 선택'
)

# 직선 방정식 입력
string = st.text_input(
    '초기 직선의 방정식',
    placeholder='ex)y=2x+4',
)
if string and option:
    # 데이터
    lis = [6, 9, 10.5, 9, 46, 71.5, 141, 43, 44, 46, 46, 44.5]

    # 초기 값 설정
    if string:
        match = re.match(r"y=([+-]?\d*)x([+-]\d+)", string)

        if match:
            mval = float(match.group(1) if match.group(1) else 1)  # 기울기 기본값 1
            yval = float(match.group(2))
            line = [mval, yval]

    a = 0 if option == '기울기' else 1
    st.button('실행')
    
    if 'line' in st.session_state:
        line = st.session_state['line']

    line = choijukhwa(lis, line[0], line[1], learn, a)

    st.session_state['line'] = line

    grap(lis, line)
    st.write(f'최적화된 직선의 방정식: y = {line[0]:.2f}x + {line[1]:.2f}')
    st.write(f'손실 함수 값: {sonsil(line, lis):.2f}')

else:
    st.warning('초기 직선의 방정식과 최적화 대상을 입력해주세요.')



