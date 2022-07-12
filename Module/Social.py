import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm
from Module import init as dir

class Social:
    '''
    사회적 요소 모델링
    '''
    def ChangeType(self,df, col_name, type):
        '''
        데이터 프레임 특정 컬럼 타입 변경
        :param df: 대상 DataFrame
        :param col_name: 컬럼 이름
        :return:
        '''
        df[col_name] = df[col_name].astype(type)
        return df
    def cal_norm(slef, mean, std, min, max, value):
        '''
        정규분포 출력 메서드
        :param mean: 평균값
        :param std: 표준편차 값
        :param min: 데이터의 최소값
        :param max: 데이터의 최대값
        :param value: 데이터의 측정값
        :return: 정규분포 객체, 참.거짓 확률
        '''

        min = min - std
        red = 'rgb(239,85,59)'
        blue = 'rgb(100,110,250)'
        fig = go.Figure()

        # 확률 값을 구할 특정 구간의 범위 설정
        cum_a = np.linspace(min, value, 100)
        cum_b = np.linspace(value, max, 100)

        pro = norm(mean, std).cdf(value) - norm(mean, std).cdf(min).round(3)
        # 구간 사이에 색을 채움
        fig.add_trace(go.Scatter(x=cum_a, y=norm.pdf(cum_a, mean, std), fill='tozeroy', name='적합', text=pro,
                                 line=dict(color=blue)))
        fig.add_trace(go.Scatter(x=cum_b, y=norm.pdf(cum_b, mean, std), fill='tozeroy', name='부적합', text=pro,
                                 line=dict(color=red)))
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        annotations = []
        annotations.append(dict(x=value, y=norm.pdf(value, loc=mean, scale=std), showarrow=False, text=round(pro, 3),
                                font=dict(size=15, color=blue), xshift=-40, yshift=-100, bordercolor=blue,
                                borderwidth=2))
        annotations.append(
            dict(x=value, y=norm.pdf(value, loc=mean, scale=std), showarrow=False, text=round(1 - pro, 3),
                 font=dict(size=15, color=red), xshift=40, yshift=-100, bordercolor=red, borderwidth=2))
        fig.update_layout(annotations=annotations)
        # value까지의 누적확률에서 min까지의 누적확률을 뺌

        # 최종 누적확률 반환
        return fig, pro, 1-pro
class Population(Social):
    '''
    사회적 요소 - 행정구역별 인구
    '''
    def __init__(self, district):
        '''
        :param district: 대상 행정 구역.
        '''
        self.file_path = dir.getdir("행정구역 인구 데이터.csv")
        self.df_people = pd.read_csv(self.file_path, encoding='cp949', header=1)
        self.df_busan_people = self.df_people[28:44].sort_values('행정구역(시군구)별').set_index('행정구역(시군구)별', inplace=True)
        Social.ChangeType(self, self.df_people, "총인구수 (명)", "float")
        Social.cal_norm(self, self.df_busan_people['총인구수 (명)'].mean(),
                        self.df_busan_people['총인구수 (명)'].std(),
                        self.df_busan_people['총인구수 (명)'].min(),
                        self.df_busan_people['총인구수 (명)'].max(),
                        self.df_busan_people.loc[district]['총인구수 (명)']
                        )